"""DatabaseAtRevision implementation."""

from __future__ import annotations

from collections.abc import AsyncIterator
from datetime import datetime

import grpc
from evidentsource_core import (
    DatabaseError,
    DatabaseName,
    DatabaseServerError,
    Event,
    EventAttribute,
    EventSelector,
    ProspectiveEvent,
    QueryDirection,
    QueryOptions,
    StateView,
    StateViewName,
)

from evidentsource_client.conversions import (
    datetime_to_timestamp,
    proto_to_event,
    selector_to_proto,
    timestamp_to_datetime,
)
from evidentsource_client.proto import domain_pb2 as domain_proto
from evidentsource_client.proto import service_pb2 as proto
from evidentsource_client.proto import service_pb2_grpc as service_grpc


class DatabaseAtRevisionImpl:
    """A database view at a specific revision.

    This implementation provides access to query events and state views
    at a specific revision of the database.

    Example:
        ```python
        # Get the latest database state
        db = await conn.latest_database()

        # Query events
        selector = Selector.stream("orders")
        async for event in db.query_events(selector):
            print(f"Event: {event.id}")

        # View state
        state = await db.view_state(StateViewName("account-balance"), 1)
        print(f"State: {state.content}")
        ```
    """

    def __init__(
        self,
        stub: service_grpc.EvidentSourceStub,
        name: DatabaseName,
        created_at: datetime,
        revision: int,
        revision_timestamp: datetime,
    ) -> None:
        """Create a DatabaseAtRevisionImpl instance."""
        self._stub = stub
        self._name = name
        self._created_at = created_at
        self._revision = revision
        self._revision_timestamp = revision_timestamp

    # =========================================================================
    # DatabaseIdentity
    # =========================================================================

    @property
    def name(self) -> DatabaseName:
        """Get the database name."""
        return self._name

    @property
    def created_at(self) -> datetime:
        """Get the timestamp when this database was created."""
        return self._created_at

    # =========================================================================
    # DatabaseAtRevision
    # =========================================================================

    @property
    def revision(self) -> int:
        """Get this view's revision number."""
        return self._revision

    @property
    def revision_timestamp(self) -> datetime:
        """Get the timestamp when this revision was committed."""
        return self._revision_timestamp

    def at_effective_timestamp(
        self, effective_timestamp: datetime
    ) -> DatabaseAtRevisionAndEffectiveTimestampImpl:
        """Get a view scoped to a specific effective timestamp (for bi-temporal queries)."""
        return DatabaseAtRevisionAndEffectiveTimestampImpl(
            stub=self._stub,
            name=self._name,
            created_at=self._created_at,
            revision=self._revision,
            revision_timestamp=self._revision_timestamp,
            effective_timestamp=effective_timestamp,
        )

    async def at_revision(self, revision: int) -> DatabaseAtRevisionImpl:
        """Get a view at a different revision."""
        request = proto.AwaitDatabaseRequest(
            database_name=str(self._name),
            at_revision=revision,
        )

        try:
            reply = await self._stub.AwaitDatabase(request)
        except grpc.aio.AioRpcError as e:
            raise _to_database_error(e, str(self._name)) from e

        db = reply.database
        revision_timestamp = timestamp_to_datetime(db.revision_timestamp)

        return DatabaseAtRevisionImpl(
            stub=self._stub,
            name=self._name,
            created_at=self._created_at,
            revision=db.revision,
            revision_timestamp=revision_timestamp,
        )

    def speculate_with_transaction(self, events: list[ProspectiveEvent]) -> SpeculativeDatabaseImpl:
        """Create a speculative view with additional uncommitted events."""
        return SpeculativeDatabaseImpl(
            basis=self,
            speculated_transactions=[events],
        )

    async def query_events(self, selector: EventSelector) -> AsyncIterator[Event]:
        """Query events matching a selector."""
        async for event in self.query_events_with_options(selector, QueryOptions()):
            yield event

    async def query_events_with_options(
        self, selector: EventSelector, options: QueryOptions
    ) -> AsyncIterator[Event]:
        """Query events matching a selector with options."""
        proto_selector = selector_to_proto(selector)

        # Build query
        query = domain_proto.DatabaseQuery(
            selector=proto_selector,
            direction=(
                domain_proto.QueryDirection.FORWARD
                if options.get_direction() == QueryDirection.FORWARD
                else domain_proto.QueryDirection.REVERSE
            ),
        )

        # Add default revision range (required by server, per Rust reference)
        revision_range = domain_proto.QueryRange.RevisionRange(start_at=0)
        query.range.revision.CopyFrom(revision_range)

        limit = options.get_limit()
        if limit is not None:
            query.limit = limit

        request = proto.EventQueryRequest(
            database_name=str(self._name),
            revision=self._revision,
            include_event_detail=True,
            query=query,
        )

        try:
            async for reply in self._stub.QueryEvents(request):
                if reply.HasField("detail"):
                    yield proto_to_event(reply.detail)
        except grpc.aio.AioRpcError as e:
            raise _to_database_error(e, str(self._name)) from e

    async def view_state(self, name: StateViewName, version: int) -> StateView:
        """Fetch a state view."""
        return await self.view_state_with_params(name, version, [])

    async def view_state_with_params(
        self,
        name: StateViewName,
        version: int,
        params: list[tuple[str, EventAttribute]],
    ) -> StateView:
        """Fetch a state view with parameter bindings."""
        identity = domain_proto.StateViewIdentity(
            database_name=str(self._name),
            state_view_name=str(name),
            state_view_version=version,
        )

        # Build parameter bindings
        bindings = {}
        for param_name, attr in params:
            bindings[param_name] = _event_attribute_to_proto(attr)

        request = proto.FetchStateViewRequest(
            state_view_identity=identity,
            database_revision=self._revision,
            parameters=domain_proto.ParameterBindings(bindings=bindings),
        )

        try:
            reply = await self._stub.FetchStateViewAtRevision(request)
        except grpc.aio.AioRpcError as e:
            raise _to_database_error(e, str(self._name)) from e

        sv = reply.state_view

        # Build event selector from proto
        from evidentsource_client.conversions import proto_to_selector

        event_selector = proto_to_selector(sv.event_selector)

        # Get content
        content = None
        content_which = sv.WhichOneof("content")
        if content_which == "data":
            content = sv.data

        # Get timestamps
        last_modified_timestamp = None
        if sv.HasField("last_modified"):
            last_modified_timestamp = timestamp_to_datetime(sv.last_modified)

        return StateView(
            database=self._name,
            name=StateViewName(sv.identity.state_view_name),
            version=sv.identity.state_view_version,
            event_selector=event_selector,
            last_modified_revision=sv.last_modified_revision if sv.last_modified_revision else None,
            last_modified_timestamp=last_modified_timestamp,
            content_type=sv.content_type,
            content_schema_url=sv.content_schema_url if sv.content_schema_url else None,
            content=content,
        )


class DatabaseAtRevisionAndEffectiveTimestampImpl:
    """A database view at both a revision and effective timestamp.

    This enables bi-temporal queries where you want to see the database
    state as it was understood at a particular point in effective time.
    """

    def __init__(
        self,
        stub: service_grpc.EvidentSourceStub,
        name: DatabaseName,
        created_at: datetime,
        revision: int,
        revision_timestamp: datetime,
        effective_timestamp: datetime,
    ) -> None:
        """Create a DatabaseAtRevisionAndEffectiveTimestampImpl instance."""
        self._stub = stub
        self._name = name
        self._created_at = created_at
        self._revision = revision
        self._revision_timestamp = revision_timestamp
        self._effective_timestamp = effective_timestamp
        self._basis = DatabaseAtRevisionImpl(
            stub=stub,
            name=name,
            created_at=created_at,
            revision=revision,
            revision_timestamp=revision_timestamp,
        )

    @property
    def name(self) -> DatabaseName:
        """Get the database name."""
        return self._name

    @property
    def created_at(self) -> datetime:
        """Get the timestamp when this database was created."""
        return self._created_at

    @property
    def revision(self) -> int:
        """Get this view's revision number."""
        return self._revision

    @property
    def revision_timestamp(self) -> datetime:
        """Get the timestamp when this revision was committed."""
        return self._revision_timestamp

    @property
    def basis(self) -> DatabaseAtRevisionImpl:
        """Get the base database view (without effective timestamp scope)."""
        return self._basis

    @property
    def effective_timestamp(self) -> datetime:
        """Get the effective timestamp this view is scoped to."""
        return self._effective_timestamp

    async def at_revision_with_effective_timestamp(
        self, revision: int
    ) -> DatabaseAtRevisionAndEffectiveTimestampImpl:
        """Get a view at a different revision while keeping the same effective timestamp."""
        new_basis = await self._basis.at_revision(revision)

        return DatabaseAtRevisionAndEffectiveTimestampImpl(
            stub=self._stub,
            name=self._name,
            created_at=self._created_at,
            revision=new_basis.revision,
            revision_timestamp=new_basis.revision_timestamp,
            effective_timestamp=self._effective_timestamp,
        )

    def speculate_with_transaction(self, events: list[ProspectiveEvent]) -> SpeculativeDatabaseImpl:
        """Create a speculative view with additional uncommitted events."""
        return SpeculativeDatabaseImpl(
            basis=self._basis,
            speculated_transactions=[events],
            effective_timestamp=self._effective_timestamp,
        )

    async def query_events(self, selector: EventSelector) -> AsyncIterator[Event]:
        """Query events matching a selector with effective timestamp filter."""
        async for event in self.query_events_with_options(selector, QueryOptions()):
            yield event

    async def query_events_with_options(
        self, selector: EventSelector, options: QueryOptions
    ) -> AsyncIterator[Event]:
        """Query events matching a selector with options and effective timestamp filter."""
        proto_selector = selector_to_proto(selector)

        # Build query with effective time range
        query = domain_proto.DatabaseQuery(
            selector=proto_selector,
            direction=(
                domain_proto.QueryDirection.FORWARD
                if options.get_direction() == QueryDirection.FORWARD
                else domain_proto.QueryDirection.REVERSE
            ),
        )

        # Add effective time range to filter events by effective timestamp
        effective_time_range = domain_proto.QueryRange.EffectiveTimeRange(
            end_at=datetime_to_timestamp(self._effective_timestamp),
        )
        query.range.effective_time.CopyFrom(effective_time_range)

        limit = options.get_limit()
        if limit is not None:
            query.limit = limit

        request = proto.EventQueryRequest(
            database_name=str(self._name),
            revision=self._revision,
            include_event_detail=True,
            query=query,
        )

        try:
            async for reply in self._stub.QueryEvents(request):
                if reply.HasField("detail"):
                    yield proto_to_event(reply.detail)
        except grpc.aio.AioRpcError as e:
            raise _to_database_error(e, str(self._name)) from e

    async def view_state(self, name: StateViewName, version: int) -> StateView:
        """Fetch a state view at the effective timestamp."""
        return await self.view_state_with_params(name, version, [])

    async def view_state_with_params(
        self,
        name: StateViewName,
        version: int,
        params: list[tuple[str, EventAttribute]],
    ) -> StateView:
        """Fetch a state view with parameter bindings at the effective timestamp."""
        identity = domain_proto.StateViewIdentity(
            database_name=str(self._name),
            state_view_name=str(name),
            state_view_version=version,
        )

        # Build parameter bindings
        bindings = {}
        for param_name, attr in params:
            bindings[param_name] = _event_attribute_to_proto(attr)

        request = proto.FetchStateViewRequest(
            state_view_identity=identity,
            database_revision=self._revision,
            parameters=domain_proto.ParameterBindings(bindings=bindings),
            effective_time_end_at=datetime_to_timestamp(self._effective_timestamp),
        )

        try:
            reply = await self._stub.FetchStateViewAtRevision(request)
        except grpc.aio.AioRpcError as e:
            raise _to_database_error(e, str(self._name)) from e

        sv = reply.state_view

        # Build event selector from proto
        from evidentsource_client.conversions import proto_to_selector

        event_selector = proto_to_selector(sv.event_selector)

        # Get content
        content = None
        content_which = sv.WhichOneof("content")
        if content_which == "data":
            content = sv.data

        # Get timestamps
        last_modified_timestamp = None
        if sv.HasField("last_modified"):
            last_modified_timestamp = timestamp_to_datetime(sv.last_modified)

        return StateView(
            database=self._name,
            name=StateViewName(sv.identity.state_view_name),
            version=sv.identity.state_view_version,
            event_selector=event_selector,
            last_modified_revision=sv.last_modified_revision if sv.last_modified_revision else None,
            last_modified_timestamp=last_modified_timestamp,
            content_type=sv.content_type,
            content_schema_url=sv.content_schema_url if sv.content_schema_url else None,
            content=content,
        )


class SpeculativeDatabaseImpl:
    """A speculative database view with uncommitted events.

    This allows querying the database as if certain events had been committed,
    useful for validation and preview scenarios.
    """

    def __init__(
        self,
        basis: DatabaseAtRevisionImpl,
        speculated_transactions: list[list[ProspectiveEvent]],
        effective_timestamp: datetime | None = None,
    ) -> None:
        """Create a SpeculativeDatabaseImpl instance."""
        self._basis = basis
        self._speculated_transactions = speculated_transactions
        self._effective_timestamp = effective_timestamp

    @property
    def name(self) -> DatabaseName:
        """Get the database name."""
        return self._basis.name

    @property
    def created_at(self) -> datetime:
        """Get the timestamp when this database was created."""
        return self._basis.created_at

    @property
    def revision(self) -> int:
        """Get this view's revision number."""
        return self._basis.revision

    @property
    def revision_timestamp(self) -> datetime:
        """Get the timestamp when this revision was committed."""
        return self._basis.revision_timestamp

    @property
    def basis(self) -> DatabaseAtRevisionImpl:
        """Get the committed view this speculation is based on."""
        return self._basis

    @property
    def speculated_transactions(self) -> list[list[ProspectiveEvent]]:
        """Get the transactions of speculated (uncommitted) events."""
        return self._speculated_transactions

    @property
    def speculated_event_count(self) -> int:
        """Get the total count of speculated events."""
        return sum(len(txn) for txn in self._speculated_transactions)

    @property
    def effective_timestamp(self) -> datetime | None:
        """Get the effective timestamp this view is scoped to, if any."""
        return self._effective_timestamp

    def at_effective_timestamp(self, effective_timestamp: datetime) -> SpeculativeDatabaseImpl:
        """Get a view scoped to a specific effective timestamp."""
        return SpeculativeDatabaseImpl(
            basis=self._basis,
            speculated_transactions=self._speculated_transactions,
            effective_timestamp=effective_timestamp,
        )

    def speculate_with_transaction(self, events: list[ProspectiveEvent]) -> SpeculativeDatabaseImpl:
        """Add another transaction of speculative events."""
        return SpeculativeDatabaseImpl(
            basis=self._basis,
            speculated_transactions=[*self._speculated_transactions, events],
            effective_timestamp=self._effective_timestamp,
        )


def _to_database_error(e: grpc.aio.AioRpcError, db_name: str) -> DatabaseError:
    """Convert a gRPC error to a DatabaseError."""
    from evidentsource_core import DatabaseNotFound

    code = e.code()

    if code == grpc.StatusCode.NOT_FOUND:
        return DatabaseNotFound(db_name)
    else:
        return DatabaseServerError(str(e.details()))


def _event_attribute_to_proto(attr: EventAttribute) -> domain_proto.EventAttribute:
    """Convert an EventAttribute to a proto EventAttribute."""
    from evidentsource_core import (
        EventTypeAttribute,
        StreamAttribute,
        SubjectAttribute,
    )

    if isinstance(attr, StreamAttribute):
        return domain_proto.EventAttribute(stream=str(attr.stream))
    elif isinstance(attr, SubjectAttribute):
        if attr.subject is None:
            return domain_proto.EventAttribute(
                subject=domain_proto.EventAttribute.SubjectValue(has_value=False, value="")
            )
        return domain_proto.EventAttribute(
            subject=domain_proto.EventAttribute.SubjectValue(
                has_value=True, value=str(attr.subject)
            )
        )
    elif isinstance(attr, EventTypeAttribute):
        return domain_proto.EventAttribute(event_type=str(attr.event_type))
    raise TypeError(f"Unknown attribute type: {type(attr)}")
