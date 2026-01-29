"""Connection - A database connection for transactions and queries."""

from __future__ import annotations

from collections.abc import AsyncIterator
from datetime import datetime
from typing import TYPE_CHECKING

import grpc
from evidentsource_core import (
    AppendCondition,
    CommandRequest,
    DatabaseError,
    DatabaseName,
    DatabaseNotFound,
    DatabaseServerError,
    ProspectiveEvent,
    StateChangeName,
    Transaction,
    TransactionOptions,
    TransactionSummary,
)

from evidentsource_client.conversions import (
    constraint_to_proto,
    datetime_to_timestamp,
    prospective_event_to_proto,
    proto_to_transaction,
    proto_to_transaction_summary,
    timestamp_to_datetime,
)
from evidentsource_client.proto import service_pb2 as proto
from evidentsource_client.proto import service_pb2_grpc as service_grpc

if TYPE_CHECKING:
    from evidentsource_client.database import DatabaseAtRevisionImpl


class Connection:
    """A database connection capable of performing transactions.

    Connection implements the DatabaseProvider and DatabaseConnection protocols.
    It maintains a live subscription to database updates and provides access
    to the database at various revisions.

    Example:
        ```python
        # Get the latest database state
        db = await conn.latest_database()
        print(f"Latest revision: {db.revision}")

        # Transact events
        events = [
            ProspectiveEvent(
                id="evt-1",
                stream="orders",
                event_type="OrderCreated",
                data=StringEventData('{"orderId": "123"}'),
            )
        ]
        db = await conn.transact(events)
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
        """Create a Connection instance."""
        self._stub = stub
        self._name = name
        self._created_at = created_at
        self._revision = revision
        self._revision_timestamp = revision_timestamp

    @classmethod
    async def connect(cls, stub: service_grpc.EvidentSourceStub, name: DatabaseName) -> Connection:
        """Connect to a database.

        This fetches the latest database state and returns a Connection instance.

        Args:
            stub: The gRPC service stub
            name: The database name

        Returns:
            A connected Connection instance

        Raises:
            DatabaseNotFound: If the database does not exist
            DatabaseServerError: If the server returns an error
        """
        request = proto.LatestDatabaseRequest(database_name=str(name))

        try:
            reply = await stub.FetchLatestDatabase(request)
        except grpc.aio.AioRpcError as e:
            raise _to_database_error(e, str(name)) from e

        db = reply.database
        db_name = DatabaseName(db.name)
        created_at = timestamp_to_datetime(db.created_at)
        revision_timestamp = timestamp_to_datetime(db.revision_timestamp)

        return cls(
            stub=stub,
            name=db_name,
            created_at=created_at,
            revision=db.revision,
            revision_timestamp=revision_timestamp,
        )

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
    # DatabaseProvider
    # =========================================================================

    def local_database(self) -> DatabaseAtRevisionImpl:
        """Get the latest local database (may be stale)."""
        from evidentsource_client.database import DatabaseAtRevisionImpl

        return DatabaseAtRevisionImpl(
            stub=self._stub,
            name=self._name,
            created_at=self._created_at,
            revision=self._revision,
            revision_timestamp=self._revision_timestamp,
        )

    async def latest_database(self) -> DatabaseAtRevisionImpl:
        """Get the latest revision on the server committed to storage."""
        from evidentsource_client.database import DatabaseAtRevisionImpl

        request = proto.LatestDatabaseRequest(database_name=str(self._name))

        try:
            reply = await self._stub.FetchLatestDatabase(request)
        except grpc.aio.AioRpcError as e:
            raise _to_database_error(e, str(self._name)) from e

        db = reply.database
        revision_timestamp = timestamp_to_datetime(db.revision_timestamp)

        # Update local state
        self._revision = db.revision
        self._revision_timestamp = revision_timestamp

        return DatabaseAtRevisionImpl(
            stub=self._stub,
            name=self._name,
            created_at=self._created_at,
            revision=db.revision,
            revision_timestamp=revision_timestamp,
        )

    async def database_at_revision(self, revision: int) -> DatabaseAtRevisionImpl:
        """Get the database at a specific revision, awaiting if necessary."""
        from evidentsource_client.database import DatabaseAtRevisionImpl

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

    async def database_at_timestamp(self, revision_timestamp: datetime) -> DatabaseAtRevisionImpl:
        """Get the database at the revision effective at a specific timestamp."""
        from evidentsource_client.database import DatabaseAtRevisionImpl

        request = proto.DatabaseEffectiveAtTimestampRequest(
            database_name=str(self._name),
            at_timestamp=datetime_to_timestamp(revision_timestamp),
        )

        try:
            reply = await self._stub.DatabaseEffectiveAtTimestamp(request)
        except grpc.aio.AioRpcError as e:
            raise _to_database_error(e, str(self._name)) from e

        db = reply.database
        rev_timestamp = timestamp_to_datetime(db.revision_timestamp)

        return DatabaseAtRevisionImpl(
            stub=self._stub,
            name=self._name,
            created_at=self._created_at,
            revision=db.revision,
            revision_timestamp=rev_timestamp,
        )

    # =========================================================================
    # DatabaseConnection
    # =========================================================================

    async def transact(
        self,
        events: list[ProspectiveEvent],
        constraints: list[AppendCondition] | None = None,
    ) -> DatabaseAtRevisionImpl:
        """Transact events with constraints.

        Args:
            events: Non-empty list of events to transact
            constraints: Optional list of constraints to check

        Returns:
            Database view at the new revision

        Raises:
            DatabaseError: If the transaction fails
        """
        from evidentsource_client.database import DatabaseAtRevisionImpl

        proto_events = [prospective_event_to_proto(e) for e in events]
        proto_constraints = [constraint_to_proto(c) for c in constraints] if constraints else []

        request = proto.TransactionRequest(
            database_name=str(self._name),
            events=proto_events,
            conditions=proto_constraints,
        )

        try:
            reply = await self._stub.Transact(request)
        except grpc.aio.AioRpcError as e:
            raise _to_database_error(e, str(self._name)) from e

        summary = reply.result.transaction_summary
        revision_timestamp = timestamp_to_datetime(summary.timestamp)

        # Update local state
        self._revision = summary.revision
        self._revision_timestamp = revision_timestamp

        return DatabaseAtRevisionImpl(
            stub=self._stub,
            name=self._name,
            created_at=self._created_at,
            revision=summary.revision,
            revision_timestamp=revision_timestamp,
        )

    async def transact_with_id(
        self,
        transaction_id: str,
        events: list[ProspectiveEvent],
        constraints: list[AppendCondition] | None = None,
    ) -> DatabaseAtRevisionImpl:
        """Transact events with a custom transaction ID.

        This is useful for idempotency - if a transaction with the same ID has
        already been committed, the existing result is returned.

        Args:
            transaction_id: Unique identifier for the transaction
            events: Non-empty list of events to transact
            constraints: Optional list of constraints to check

        Returns:
            Database view at the new revision

        Raises:
            DatabaseError: If the transaction fails
        """
        from evidentsource_client.database import DatabaseAtRevisionImpl

        proto_events = [prospective_event_to_proto(e) for e in events]
        proto_constraints = [constraint_to_proto(c) for c in constraints] if constraints else []

        request = proto.TransactionRequest(
            database_name=str(self._name),
            events=proto_events,
            conditions=proto_constraints,
            transaction_id=transaction_id,
        )

        try:
            reply = await self._stub.Transact(request)
        except grpc.aio.AioRpcError as e:
            raise _to_database_error(e, str(self._name)) from e

        summary = reply.result.transaction_summary
        revision_timestamp = timestamp_to_datetime(summary.timestamp)

        # Update local state
        self._revision = summary.revision
        self._revision_timestamp = revision_timestamp

        return DatabaseAtRevisionImpl(
            stub=self._stub,
            name=self._name,
            created_at=self._created_at,
            revision=summary.revision,
            revision_timestamp=revision_timestamp,
        )

    async def transact_with_options(
        self,
        events: list[ProspectiveEvent],
        constraints: list[AppendCondition] | None = None,
        options: TransactionOptions | None = None,
    ) -> DatabaseAtRevisionImpl:
        """Transact events with full options including correlation metadata.

        This method provides complete control over transaction parameters including
        transaction ID for idempotency and CloudEvents correlation extensions.

        Args:
            events: Non-empty list of events to transact
            constraints: Optional list of constraints to check
            options: Optional transaction options for correlation metadata

        Returns:
            Database view at the new revision

        Raises:
            DatabaseError: If the transaction fails

        Example:
            options = TransactionOptions(
                transaction_id="txn-123",
                correlation_id="order-flow-456",
                causation_id="parent-event-789",
            )
            db = await conn.transact_with_options(events, constraints, options)

        See:
            https://github.com/cloudevents/spec/blob/main/cloudevents/extensions/correlation.md
        """
        from evidentsource_client.database import DatabaseAtRevisionImpl

        proto_events = [prospective_event_to_proto(e) for e in events]
        proto_constraints = [constraint_to_proto(c) for c in constraints] if constraints else []

        request = proto.TransactionRequest(
            database_name=str(self._name),
            events=proto_events,
            conditions=proto_constraints,
        )

        if options:
            if options.transaction_id:
                request.transaction_id = options.transaction_id
            if options.correlation_id:
                request.correlation_id = options.correlation_id
            if options.causation_id:
                request.causation_id = options.causation_id

        try:
            reply = await self._stub.Transact(request)
        except grpc.aio.AioRpcError as e:
            raise _to_database_error(e, str(self._name)) from e

        summary = reply.result.transaction_summary
        revision_timestamp = timestamp_to_datetime(summary.timestamp)

        # Update local state
        self._revision = summary.revision
        self._revision_timestamp = revision_timestamp

        return DatabaseAtRevisionImpl(
            stub=self._stub,
            name=self._name,
            created_at=self._created_at,
            revision=summary.revision,
            revision_timestamp=revision_timestamp,
        )

    async def execute_state_change(
        self,
        name: StateChangeName,
        version: int,
        request: CommandRequest,
    ) -> DatabaseAtRevisionImpl:
        """Execute a state change.

        Args:
            name: The state change name
            version: The state change version
            request: The command request containing body and content type

        Returns:
            Database view at the new revision

        Raises:
            DatabaseError: If execution fails

        Example:
            # Using JSON helper
            request = CommandRequest.json({"account_id": "123", "amount": 100})
            db = await conn.execute_state_change(state_change_name, 1, request)
        """
        from evidentsource_client.database import DatabaseAtRevisionImpl

        proto_command = proto.CommandRequest(
            body=request.body or b"",
            content_type=request.content_type or "",
        )

        proto_request = proto.ExecuteStateChangeRequest(
            database_name=str(self._name),
            state_change_name=str(name),
            version=version,
            request=proto_command,
        )

        try:
            reply = await self._stub.ExecuteStateChange(proto_request)
        except grpc.aio.AioRpcError as e:
            raise _to_database_error(e, str(self._name)) from e

        summary = reply.result.transaction_summary
        revision_timestamp = timestamp_to_datetime(summary.timestamp)

        # Update local state
        self._revision = summary.revision
        self._revision_timestamp = revision_timestamp

        return DatabaseAtRevisionImpl(
            stub=self._stub,
            name=self._name,
            created_at=self._created_at,
            revision=summary.revision,
            revision_timestamp=revision_timestamp,
        )

    async def execute_state_change_with_id(
        self,
        name: StateChangeName,
        version: int,
        request: CommandRequest,
        transaction_id: str,
    ) -> DatabaseAtRevisionImpl:
        """Execute a state change with a custom transaction ID.

        This is useful for idempotency - if a transaction with the same ID has
        already been committed, the existing result is returned.

        Args:
            name: The state change name
            version: The state change version
            request: The command request containing body and content type
            transaction_id: Unique identifier for the transaction

        Returns:
            Database view at the new revision

        Raises:
            DatabaseError: If execution fails
        """
        return await self.execute_state_change_with_options(
            name, version, request, TransactionOptions(transaction_id=transaction_id)
        )

    async def execute_state_change_with_options(
        self,
        name: StateChangeName,
        version: int,
        request: CommandRequest,
        options: TransactionOptions | None = None,
    ) -> DatabaseAtRevisionImpl:
        """Execute a state change with full options including correlation metadata.

        This method provides complete control over state change parameters including
        transaction ID for idempotency and CloudEvents correlation extensions.

        Args:
            name: The state change name
            version: The state change version
            request: The command request containing body and content type
            options: Optional transaction options for correlation metadata

        Returns:
            Database view at the new revision

        Raises:
            DatabaseError: If execution fails

        Example:
            options = TransactionOptions(
                transaction_id="txn-123",
                correlation_id="order-flow-456",
                causation_id="parent-event-789",
            )
            db = await conn.execute_state_change_with_options(
                state_change_name, 1, request, options
            )

        See:
            https://github.com/cloudevents/spec/blob/main/cloudevents/extensions/correlation.md
        """
        from evidentsource_client.database import DatabaseAtRevisionImpl

        proto_command = proto.CommandRequest(
            body=request.body or b"",
            content_type=request.content_type or "",
        )

        proto_request = proto.ExecuteStateChangeRequest(
            database_name=str(self._name),
            state_change_name=str(name),
            version=version,
            request=proto_command,
        )

        if options:
            if options.transaction_id:
                proto_request.transaction_id = options.transaction_id
            if options.correlation_id:
                proto_request.correlation_id = options.correlation_id
            if options.causation_id:
                proto_request.causation_id = options.causation_id

        try:
            reply = await self._stub.ExecuteStateChange(proto_request)
        except grpc.aio.AioRpcError as e:
            raise _to_database_error(e, str(self._name)) from e

        summary = reply.result.transaction_summary
        revision_timestamp = timestamp_to_datetime(summary.timestamp)

        # Update local state
        self._revision = summary.revision
        self._revision_timestamp = revision_timestamp

        return DatabaseAtRevisionImpl(
            stub=self._stub,
            name=self._name,
            created_at=self._created_at,
            revision=summary.revision,
            revision_timestamp=revision_timestamp,
        )

    async def log(self) -> AsyncIterator[TransactionSummary]:
        """Get the transaction log (summary only)."""
        request = proto.LogScanRequest(
            database_name=str(self._name),
            start_at_revision=0,
            include_event_detail=False,
        )

        try:
            async for reply in self._stub.ScanDatabaseLog(request):
                if reply.HasField("summary"):
                    yield proto_to_transaction_summary(reply.summary)
        except grpc.aio.AioRpcError as e:
            raise _to_database_error(e, str(self._name)) from e

    async def log_detail(self) -> AsyncIterator[Transaction]:
        """Get the transaction log with full event details."""
        request = proto.LogScanRequest(
            database_name=str(self._name),
            start_at_revision=0,
            include_event_detail=True,
        )

        try:
            async for reply in self._stub.ScanDatabaseLog(request):
                if reply.HasField("detail"):
                    yield proto_to_transaction(reply.detail)
        except grpc.aio.AioRpcError as e:
            raise _to_database_error(e, str(self._name)) from e

    async def log_from(self, from_revision: int) -> AsyncIterator[TransactionSummary]:
        """Get the transaction log starting from a specific revision."""
        request = proto.LogScanRequest(
            database_name=str(self._name),
            start_at_revision=from_revision,
            include_event_detail=False,
        )

        try:
            async for reply in self._stub.ScanDatabaseLog(request):
                if reply.HasField("summary"):
                    yield proto_to_transaction_summary(reply.summary)
        except grpc.aio.AioRpcError as e:
            raise _to_database_error(e, str(self._name)) from e

    async def log_detail_from(self, from_revision: int) -> AsyncIterator[Transaction]:
        """Get the transaction log with full event details, starting from a revision."""
        request = proto.LogScanRequest(
            database_name=str(self._name),
            start_at_revision=from_revision,
            include_event_detail=True,
        )

        try:
            async for reply in self._stub.ScanDatabaseLog(request):
                if reply.HasField("detail"):
                    yield proto_to_transaction(reply.detail)
        except grpc.aio.AioRpcError as e:
            raise _to_database_error(e, str(self._name)) from e

    async def close(self) -> None:
        """Close the connection.

        This releases any resources held by the connection.
        Currently a no-op as Python does not maintain background subscriptions.
        """
        pass


def _to_database_error(e: grpc.aio.AioRpcError, db_name: str) -> DatabaseError:
    """Convert a gRPC error to a DatabaseError."""
    code = e.code()

    if code == grpc.StatusCode.NOT_FOUND:
        return DatabaseNotFound(db_name)
    else:
        return DatabaseServerError(str(e.details()))
