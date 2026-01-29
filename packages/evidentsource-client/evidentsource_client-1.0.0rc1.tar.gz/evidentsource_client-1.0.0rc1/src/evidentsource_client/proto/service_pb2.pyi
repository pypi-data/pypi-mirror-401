import datetime

import domain_pb2 as _domain_pb2
import cloudevents_pb2 as _cloudevents_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateDatabaseRequest(_message.Message):
    __slots__ = ("database_name",)
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    database_name: str
    def __init__(self, database_name: _Optional[str] = ...) -> None: ...

class CreateDatabaseReply(_message.Message):
    __slots__ = ("database",)
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    database: _domain_pb2.Database
    def __init__(self, database: _Optional[_Union[_domain_pb2.Database, _Mapping]] = ...) -> None: ...

class TransactionRequest(_message.Message):
    __slots__ = ("database_name", "events", "conditions", "transaction_id", "last_read_revision", "principal_attributes", "commit_message", "correlation_id", "causation_id")
    class PrincipalAttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_READ_REVISION_FIELD_NUMBER: _ClassVar[int]
    PRINCIPAL_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    COMMIT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    CAUSATION_ID_FIELD_NUMBER: _ClassVar[int]
    database_name: str
    events: _containers.RepeatedCompositeFieldContainer[_cloudevents_pb2.CloudEvent]
    conditions: _containers.RepeatedCompositeFieldContainer[_domain_pb2.AppendCondition]
    transaction_id: str
    last_read_revision: int
    principal_attributes: _containers.ScalarMap[str, str]
    commit_message: str
    correlation_id: str
    causation_id: str
    def __init__(self, database_name: _Optional[str] = ..., events: _Optional[_Iterable[_Union[_cloudevents_pb2.CloudEvent, _Mapping]]] = ..., conditions: _Optional[_Iterable[_Union[_domain_pb2.AppendCondition, _Mapping]]] = ..., transaction_id: _Optional[str] = ..., last_read_revision: _Optional[int] = ..., principal_attributes: _Optional[_Mapping[str, str]] = ..., commit_message: _Optional[str] = ..., correlation_id: _Optional[str] = ..., causation_id: _Optional[str] = ...) -> None: ...

class TransactionReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: _domain_pb2.TransactionResult
    def __init__(self, result: _Optional[_Union[_domain_pb2.TransactionResult, _Mapping]] = ...) -> None: ...

class DeleteDatabaseRequest(_message.Message):
    __slots__ = ("database_name",)
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    database_name: str
    def __init__(self, database_name: _Optional[str] = ...) -> None: ...

class DeleteDatabaseReply(_message.Message):
    __slots__ = ("database",)
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    database: _domain_pb2.Database
    def __init__(self, database: _Optional[_Union[_domain_pb2.Database, _Mapping]] = ...) -> None: ...

class CatalogRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CatalogReply(_message.Message):
    __slots__ = ("database_name",)
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    database_name: str
    def __init__(self, database_name: _Optional[str] = ...) -> None: ...

class LatestDatabaseRequest(_message.Message):
    __slots__ = ("database_name",)
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    database_name: str
    def __init__(self, database_name: _Optional[str] = ...) -> None: ...

class AwaitDatabaseRequest(_message.Message):
    __slots__ = ("database_name", "at_revision")
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    AT_REVISION_FIELD_NUMBER: _ClassVar[int]
    database_name: str
    at_revision: int
    def __init__(self, database_name: _Optional[str] = ..., at_revision: _Optional[int] = ...) -> None: ...

class DatabaseEffectiveAtTimestampRequest(_message.Message):
    __slots__ = ("database_name", "at_timestamp")
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    AT_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    database_name: str
    at_timestamp: _timestamp_pb2.Timestamp
    def __init__(self, database_name: _Optional[str] = ..., at_timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class DatabaseUpdatesSubscriptionRequest(_message.Message):
    __slots__ = ("database_name",)
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    database_name: str
    def __init__(self, database_name: _Optional[str] = ...) -> None: ...

class DatabaseReply(_message.Message):
    __slots__ = ("database",)
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    database: _domain_pb2.Database
    def __init__(self, database: _Optional[_Union[_domain_pb2.Database, _Mapping]] = ...) -> None: ...

class FetchTransactionByIdRequest(_message.Message):
    __slots__ = ("database_name", "transaction_id")
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_ID_FIELD_NUMBER: _ClassVar[int]
    database_name: str
    transaction_id: str
    def __init__(self, database_name: _Optional[str] = ..., transaction_id: _Optional[str] = ...) -> None: ...

class FetchTransactionReply(_message.Message):
    __slots__ = ("transaction",)
    TRANSACTION_FIELD_NUMBER: _ClassVar[int]
    transaction: _domain_pb2.Transaction
    def __init__(self, transaction: _Optional[_Union[_domain_pb2.Transaction, _Mapping]] = ...) -> None: ...

class LogScanRequest(_message.Message):
    __slots__ = ("database_name", "start_at_revision", "include_event_detail")
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    START_AT_REVISION_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_EVENT_DETAIL_FIELD_NUMBER: _ClassVar[int]
    database_name: str
    start_at_revision: int
    include_event_detail: bool
    def __init__(self, database_name: _Optional[str] = ..., start_at_revision: _Optional[int] = ..., include_event_detail: bool = ...) -> None: ...

class DatabaseLogReply(_message.Message):
    __slots__ = ("summary", "detail")
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    summary: _domain_pb2.TransactionSummary
    detail: _domain_pb2.Transaction
    def __init__(self, summary: _Optional[_Union[_domain_pb2.TransactionSummary, _Mapping]] = ..., detail: _Optional[_Union[_domain_pb2.Transaction, _Mapping]] = ...) -> None: ...

class IndexKeyScanRequest(_message.Message):
    __slots__ = ("database_name", "revision", "index_key_type")
    class IndexKeyType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        Stream: _ClassVar[IndexKeyScanRequest.IndexKeyType]
        Subject: _ClassVar[IndexKeyScanRequest.IndexKeyType]
        EventType: _ClassVar[IndexKeyScanRequest.IndexKeyType]
    Stream: IndexKeyScanRequest.IndexKeyType
    Subject: IndexKeyScanRequest.IndexKeyType
    EventType: IndexKeyScanRequest.IndexKeyType
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    INDEX_KEY_TYPE_FIELD_NUMBER: _ClassVar[int]
    database_name: str
    revision: int
    index_key_type: IndexKeyScanRequest.IndexKeyType
    def __init__(self, database_name: _Optional[str] = ..., revision: _Optional[int] = ..., index_key_type: _Optional[_Union[IndexKeyScanRequest.IndexKeyType, str]] = ...) -> None: ...

class IndexKeyScanReply(_message.Message):
    __slots__ = ("index_key",)
    INDEX_KEY_FIELD_NUMBER: _ClassVar[int]
    index_key: str
    def __init__(self, index_key: _Optional[str] = ...) -> None: ...

class EventQueryRequest(_message.Message):
    __slots__ = ("database_name", "revision", "include_event_detail", "query")
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_EVENT_DETAIL_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    database_name: str
    revision: int
    include_event_detail: bool
    query: _domain_pb2.DatabaseQuery
    def __init__(self, database_name: _Optional[str] = ..., revision: _Optional[int] = ..., include_event_detail: bool = ..., query: _Optional[_Union[_domain_pb2.DatabaseQuery, _Mapping]] = ...) -> None: ...

class EventByIdRequest(_message.Message):
    __slots__ = ("database_name", "revision", "stream", "event_id")
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    STREAM_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    database_name: str
    revision: int
    stream: str
    event_id: str
    def __init__(self, database_name: _Optional[str] = ..., revision: _Optional[int] = ..., stream: _Optional[str] = ..., event_id: _Optional[str] = ...) -> None: ...

class EventQueryReply(_message.Message):
    __slots__ = ("revision", "detail")
    REVISION_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    revision: int
    detail: _cloudevents_pb2.CloudEvent
    def __init__(self, revision: _Optional[int] = ..., detail: _Optional[_Union[_cloudevents_pb2.CloudEvent, _Mapping]] = ...) -> None: ...

class EventsByRevisionsRequest(_message.Message):
    __slots__ = ("database_name", "event_revisions")
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    EVENT_REVISIONS_FIELD_NUMBER: _ClassVar[int]
    database_name: str
    event_revisions: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, database_name: _Optional[str] = ..., event_revisions: _Optional[_Iterable[int]] = ...) -> None: ...

class EventsReply(_message.Message):
    __slots__ = ("events",)
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[_cloudevents_pb2.CloudEvent]
    def __init__(self, events: _Optional[_Iterable[_Union[_cloudevents_pb2.CloudEvent, _Mapping]]] = ...) -> None: ...

class ListStateViewDefinitionsRequest(_message.Message):
    __slots__ = ("database_name", "status")
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    database_name: str
    status: _domain_pb2.StateViewStatus
    def __init__(self, database_name: _Optional[str] = ..., status: _Optional[_Union[_domain_pb2.StateViewStatus, str]] = ...) -> None: ...

class ListStateViewDefinitionsReply(_message.Message):
    __slots__ = ("state_view_name", "state_view_version")
    STATE_VIEW_NAME_FIELD_NUMBER: _ClassVar[int]
    STATE_VIEW_VERSION_FIELD_NUMBER: _ClassVar[int]
    state_view_name: str
    state_view_version: int
    def __init__(self, state_view_name: _Optional[str] = ..., state_view_version: _Optional[int] = ...) -> None: ...

class FetchStateViewRequest(_message.Message):
    __slots__ = ("state_view_identity", "database_revision", "parameters", "effective_time_end_at")
    STATE_VIEW_IDENTITY_FIELD_NUMBER: _ClassVar[int]
    DATABASE_REVISION_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_TIME_END_AT_FIELD_NUMBER: _ClassVar[int]
    state_view_identity: _domain_pb2.StateViewIdentity
    database_revision: int
    parameters: _domain_pb2.ParameterBindings
    effective_time_end_at: _timestamp_pb2.Timestamp
    def __init__(self, state_view_identity: _Optional[_Union[_domain_pb2.StateViewIdentity, _Mapping]] = ..., database_revision: _Optional[int] = ..., parameters: _Optional[_Union[_domain_pb2.ParameterBindings, _Mapping]] = ..., effective_time_end_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class StateViewSubscriptionRequest(_message.Message):
    __slots__ = ("state_view_identity", "parameters", "effective_time_end_at")
    STATE_VIEW_IDENTITY_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_TIME_END_AT_FIELD_NUMBER: _ClassVar[int]
    state_view_identity: _domain_pb2.StateViewIdentity
    parameters: _domain_pb2.ParameterBindings
    effective_time_end_at: _timestamp_pb2.Timestamp
    def __init__(self, state_view_identity: _Optional[_Union[_domain_pb2.StateViewIdentity, _Mapping]] = ..., parameters: _Optional[_Union[_domain_pb2.ParameterBindings, _Mapping]] = ..., effective_time_end_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class StateViewReply(_message.Message):
    __slots__ = ("state_view",)
    STATE_VIEW_FIELD_NUMBER: _ClassVar[int]
    state_view: _domain_pb2.StateView
    def __init__(self, state_view: _Optional[_Union[_domain_pb2.StateView, _Mapping]] = ...) -> None: ...

class ListStateChangesRequest(_message.Message):
    __slots__ = ("database_name",)
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    database_name: str
    def __init__(self, database_name: _Optional[str] = ...) -> None: ...

class ListStateChangesReply(_message.Message):
    __slots__ = ("name", "version")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    name: str
    version: int
    def __init__(self, name: _Optional[str] = ..., version: _Optional[int] = ...) -> None: ...

class ExecuteStateChangeRequest(_message.Message):
    __slots__ = ("database_name", "state_change_name", "version", "last_seen_revision", "request", "transaction_id", "principal_attributes", "commit_message", "correlation_id", "causation_id")
    class PrincipalAttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    STATE_CHANGE_NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    LAST_SEEN_REVISION_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_ID_FIELD_NUMBER: _ClassVar[int]
    PRINCIPAL_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    COMMIT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    CAUSATION_ID_FIELD_NUMBER: _ClassVar[int]
    database_name: str
    state_change_name: str
    version: int
    last_seen_revision: int
    request: CommandRequest
    transaction_id: str
    principal_attributes: _containers.ScalarMap[str, str]
    commit_message: str
    correlation_id: str
    causation_id: str
    def __init__(self, database_name: _Optional[str] = ..., state_change_name: _Optional[str] = ..., version: _Optional[int] = ..., last_seen_revision: _Optional[int] = ..., request: _Optional[_Union[CommandRequest, _Mapping]] = ..., transaction_id: _Optional[str] = ..., principal_attributes: _Optional[_Mapping[str, str]] = ..., commit_message: _Optional[str] = ..., correlation_id: _Optional[str] = ..., causation_id: _Optional[str] = ...) -> None: ...

class ExecuteStateChangeReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: _domain_pb2.TransactionResult
    def __init__(self, result: _Optional[_Union[_domain_pb2.TransactionResult, _Mapping]] = ...) -> None: ...

class CommandRequest(_message.Message):
    __slots__ = ("headers", "body", "content_type", "content_schema")
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    headers: _containers.RepeatedCompositeFieldContainer[Header]
    body: bytes
    content_type: str
    content_schema: str
    def __init__(self, headers: _Optional[_Iterable[_Union[Header, _Mapping]]] = ..., body: _Optional[bytes] = ..., content_type: _Optional[str] = ..., content_schema: _Optional[str] = ...) -> None: ...

class Header(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class AsyncCommandResponse(_message.Message):
    __slots__ = ("correlation_id",)
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    correlation_id: str
    def __init__(self, correlation_id: _Optional[str] = ...) -> None: ...
