import datetime

import cloudevents_pb2 as _cloudevents_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QueryTemporality(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REVISION_ORDER: _ClassVar[QueryTemporality]
    EFFECTIVE_TIME_ORDER: _ClassVar[QueryTemporality]

class QueryDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FORWARD: _ClassVar[QueryDirection]
    REVERSE: _ClassVar[QueryDirection]

class StateViewStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INACTIVE: _ClassVar[StateViewStatus]
    ACTIVE: _ClassVar[StateViewStatus]

class StateChangeStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STATE_CHANGE_INACTIVE: _ClassVar[StateChangeStatus]
    STATE_CHANGE_ACTIVE: _ClassVar[StateChangeStatus]
REVISION_ORDER: QueryTemporality
EFFECTIVE_TIME_ORDER: QueryTemporality
FORWARD: QueryDirection
REVERSE: QueryDirection
INACTIVE: StateViewStatus
ACTIVE: StateViewStatus
STATE_CHANGE_INACTIVE: StateChangeStatus
STATE_CHANGE_ACTIVE: StateChangeStatus

class Database(_message.Message):
    __slots__ = ("name", "created_at", "basis", "revision", "revision_timestamp")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    BASIS_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    REVISION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    name: str
    created_at: _timestamp_pb2.Timestamp
    basis: int
    revision: int
    revision_timestamp: _timestamp_pb2.Timestamp
    def __init__(self, name: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., basis: _Optional[int] = ..., revision: _Optional[int] = ..., revision_timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class EventAttribute(_message.Message):
    __slots__ = ("stream", "subject", "event_type")
    class SubjectValue(_message.Message):
        __slots__ = ("has_value", "value")
        HAS_VALUE_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        has_value: bool
        value: str
        def __init__(self, has_value: bool = ..., value: _Optional[str] = ...) -> None: ...
    STREAM_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    stream: str
    subject: EventAttribute.SubjectValue
    event_type: str
    def __init__(self, stream: _Optional[str] = ..., subject: _Optional[_Union[EventAttribute.SubjectValue, _Mapping]] = ..., event_type: _Optional[str] = ...) -> None: ...

class EventSelector(_message.Message):
    __slots__ = ("equals", "starts_with")
    class LogicalAnd(_message.Message):
        __slots__ = ("left", "right")
        LEFT_FIELD_NUMBER: _ClassVar[int]
        RIGHT_FIELD_NUMBER: _ClassVar[int]
        left: EventSelector
        right: EventSelector
        def __init__(self, left: _Optional[_Union[EventSelector, _Mapping]] = ..., right: _Optional[_Union[EventSelector, _Mapping]] = ...) -> None: ...
    class LogicalOr(_message.Message):
        __slots__ = ("left", "right")
        LEFT_FIELD_NUMBER: _ClassVar[int]
        RIGHT_FIELD_NUMBER: _ClassVar[int]
        left: EventSelector
        right: EventSelector
        def __init__(self, left: _Optional[_Union[EventSelector, _Mapping]] = ..., right: _Optional[_Union[EventSelector, _Mapping]] = ...) -> None: ...
    class StartsWith(_message.Message):
        __slots__ = ("stream", "subject", "event_type")
        STREAM_FIELD_NUMBER: _ClassVar[int]
        SUBJECT_FIELD_NUMBER: _ClassVar[int]
        EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
        stream: str
        subject: str
        event_type: str
        def __init__(self, stream: _Optional[str] = ..., subject: _Optional[str] = ..., event_type: _Optional[str] = ...) -> None: ...
    EQUALS_FIELD_NUMBER: _ClassVar[int]
    STARTS_WITH_FIELD_NUMBER: _ClassVar[int]
    AND_FIELD_NUMBER: _ClassVar[int]
    OR_FIELD_NUMBER: _ClassVar[int]
    equals: EventAttribute
    starts_with: EventSelector.StartsWith
    def __init__(self, equals: _Optional[_Union[EventAttribute, _Mapping]] = ..., starts_with: _Optional[_Union[EventSelector.StartsWith, _Mapping]] = ..., **kwargs) -> None: ...

class UnboundEventAttribute(_message.Message):
    __slots__ = ("stream", "subject", "event_type")
    class StreamValue(_message.Message):
        __slots__ = ("parameter", "stream")
        PARAMETER_FIELD_NUMBER: _ClassVar[int]
        STREAM_FIELD_NUMBER: _ClassVar[int]
        parameter: str
        stream: str
        def __init__(self, parameter: _Optional[str] = ..., stream: _Optional[str] = ...) -> None: ...
    class SubjectValue(_message.Message):
        __slots__ = ("parameter", "subject")
        PARAMETER_FIELD_NUMBER: _ClassVar[int]
        SUBJECT_FIELD_NUMBER: _ClassVar[int]
        parameter: str
        subject: UnboundEventAttribute.SubjectData
        def __init__(self, parameter: _Optional[str] = ..., subject: _Optional[_Union[UnboundEventAttribute.SubjectData, _Mapping]] = ...) -> None: ...
    class SubjectData(_message.Message):
        __slots__ = ("has_value", "value")
        HAS_VALUE_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        has_value: bool
        value: str
        def __init__(self, has_value: bool = ..., value: _Optional[str] = ...) -> None: ...
    class EventTypeValue(_message.Message):
        __slots__ = ("parameter", "event_type")
        PARAMETER_FIELD_NUMBER: _ClassVar[int]
        EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
        parameter: str
        event_type: str
        def __init__(self, parameter: _Optional[str] = ..., event_type: _Optional[str] = ...) -> None: ...
    STREAM_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    stream: UnboundEventAttribute.StreamValue
    subject: UnboundEventAttribute.SubjectValue
    event_type: UnboundEventAttribute.EventTypeValue
    def __init__(self, stream: _Optional[_Union[UnboundEventAttribute.StreamValue, _Mapping]] = ..., subject: _Optional[_Union[UnboundEventAttribute.SubjectValue, _Mapping]] = ..., event_type: _Optional[_Union[UnboundEventAttribute.EventTypeValue, _Mapping]] = ...) -> None: ...

class UnboundEventSelector(_message.Message):
    __slots__ = ("equals", "starts_with")
    class LogicalAnd(_message.Message):
        __slots__ = ("left", "right")
        LEFT_FIELD_NUMBER: _ClassVar[int]
        RIGHT_FIELD_NUMBER: _ClassVar[int]
        left: UnboundEventSelector
        right: UnboundEventSelector
        def __init__(self, left: _Optional[_Union[UnboundEventSelector, _Mapping]] = ..., right: _Optional[_Union[UnboundEventSelector, _Mapping]] = ...) -> None: ...
    class LogicalOr(_message.Message):
        __slots__ = ("left", "right")
        LEFT_FIELD_NUMBER: _ClassVar[int]
        RIGHT_FIELD_NUMBER: _ClassVar[int]
        left: UnboundEventSelector
        right: UnboundEventSelector
        def __init__(self, left: _Optional[_Union[UnboundEventSelector, _Mapping]] = ..., right: _Optional[_Union[UnboundEventSelector, _Mapping]] = ...) -> None: ...
    EQUALS_FIELD_NUMBER: _ClassVar[int]
    STARTS_WITH_FIELD_NUMBER: _ClassVar[int]
    AND_FIELD_NUMBER: _ClassVar[int]
    OR_FIELD_NUMBER: _ClassVar[int]
    equals: UnboundEventAttribute
    starts_with: UnboundEventAttribute
    def __init__(self, equals: _Optional[_Union[UnboundEventAttribute, _Mapping]] = ..., starts_with: _Optional[_Union[UnboundEventAttribute, _Mapping]] = ..., **kwargs) -> None: ...

class ParameterBindings(_message.Message):
    __slots__ = ("bindings",)
    class BindingsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: EventAttribute
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[EventAttribute, _Mapping]] = ...) -> None: ...
    BINDINGS_FIELD_NUMBER: _ClassVar[int]
    bindings: _containers.MessageMap[str, EventAttribute]
    def __init__(self, bindings: _Optional[_Mapping[str, EventAttribute]] = ...) -> None: ...

class RangeCursor(_message.Message):
    __slots__ = ("timestamp", "revision")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    revision: int
    def __init__(self, timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., revision: _Optional[int] = ...) -> None: ...

class QueryRange(_message.Message):
    __slots__ = ("revision", "effective_time")
    class RevisionRange(_message.Message):
        __slots__ = ("start_at",)
        START_AT_FIELD_NUMBER: _ClassVar[int]
        start_at: int
        def __init__(self, start_at: _Optional[int] = ...) -> None: ...
    class EffectiveTimeRange(_message.Message):
        __slots__ = ("start_at", "end_at")
        START_AT_FIELD_NUMBER: _ClassVar[int]
        END_AT_FIELD_NUMBER: _ClassVar[int]
        start_at: RangeCursor
        end_at: _timestamp_pb2.Timestamp
        def __init__(self, start_at: _Optional[_Union[RangeCursor, _Mapping]] = ..., end_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
    REVISION_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_TIME_FIELD_NUMBER: _ClassVar[int]
    revision: QueryRange.RevisionRange
    effective_time: QueryRange.EffectiveTimeRange
    def __init__(self, revision: _Optional[_Union[QueryRange.RevisionRange, _Mapping]] = ..., effective_time: _Optional[_Union[QueryRange.EffectiveTimeRange, _Mapping]] = ...) -> None: ...

class DatabaseQuery(_message.Message):
    __slots__ = ("selector", "range", "direction", "limit")
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    selector: EventSelector
    range: QueryRange
    direction: QueryDirection
    limit: int
    def __init__(self, selector: _Optional[_Union[EventSelector, _Mapping]] = ..., range: _Optional[_Union[QueryRange, _Mapping]] = ..., direction: _Optional[_Union[QueryDirection, str]] = ..., limit: _Optional[int] = ...) -> None: ...

class AppendCondition(_message.Message):
    __slots__ = ("min", "max", "range")
    class Min(_message.Message):
        __slots__ = ("selector", "revision")
        SELECTOR_FIELD_NUMBER: _ClassVar[int]
        REVISION_FIELD_NUMBER: _ClassVar[int]
        selector: EventSelector
        revision: int
        def __init__(self, selector: _Optional[_Union[EventSelector, _Mapping]] = ..., revision: _Optional[int] = ...) -> None: ...
    class Max(_message.Message):
        __slots__ = ("selector", "revision")
        SELECTOR_FIELD_NUMBER: _ClassVar[int]
        REVISION_FIELD_NUMBER: _ClassVar[int]
        selector: EventSelector
        revision: int
        def __init__(self, selector: _Optional[_Union[EventSelector, _Mapping]] = ..., revision: _Optional[int] = ...) -> None: ...
    class Range(_message.Message):
        __slots__ = ("selector", "min", "max")
        SELECTOR_FIELD_NUMBER: _ClassVar[int]
        MIN_FIELD_NUMBER: _ClassVar[int]
        MAX_FIELD_NUMBER: _ClassVar[int]
        selector: EventSelector
        min: int
        max: int
        def __init__(self, selector: _Optional[_Union[EventSelector, _Mapping]] = ..., min: _Optional[int] = ..., max: _Optional[int] = ...) -> None: ...
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    min: AppendCondition.Min
    max: AppendCondition.Max
    range: AppendCondition.Range
    def __init__(self, min: _Optional[_Union[AppendCondition.Min, _Mapping]] = ..., max: _Optional[_Union[AppendCondition.Max, _Mapping]] = ..., range: _Optional[_Union[AppendCondition.Range, _Mapping]] = ...) -> None: ...

class KafkaOriginMetadata(_message.Message):
    __slots__ = ("topic", "partition", "offset", "correlation_id")
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    PARTITION_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    topic: str
    partition: int
    offset: int
    correlation_id: str
    def __init__(self, topic: _Optional[str] = ..., partition: _Optional[int] = ..., offset: _Optional[int] = ..., correlation_id: _Optional[str] = ...) -> None: ...

class TransactionOrigin(_message.Message):
    __slots__ = ("http_transaction", "http_state_change", "grpc_transaction", "grpc_state_change", "kafka_transaction", "kafka_state_change")
    class HttpTransaction(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class HttpStateChange(_message.Message):
        __slots__ = ("name", "version")
        NAME_FIELD_NUMBER: _ClassVar[int]
        VERSION_FIELD_NUMBER: _ClassVar[int]
        name: str
        version: int
        def __init__(self, name: _Optional[str] = ..., version: _Optional[int] = ...) -> None: ...
    class GrpcTransaction(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class GrpcStateChange(_message.Message):
        __slots__ = ("name", "version")
        NAME_FIELD_NUMBER: _ClassVar[int]
        VERSION_FIELD_NUMBER: _ClassVar[int]
        name: str
        version: int
        def __init__(self, name: _Optional[str] = ..., version: _Optional[int] = ...) -> None: ...
    class KafkaTransaction(_message.Message):
        __slots__ = ("kafka",)
        KAFKA_FIELD_NUMBER: _ClassVar[int]
        kafka: KafkaOriginMetadata
        def __init__(self, kafka: _Optional[_Union[KafkaOriginMetadata, _Mapping]] = ...) -> None: ...
    class KafkaStateChange(_message.Message):
        __slots__ = ("name", "version", "kafka")
        NAME_FIELD_NUMBER: _ClassVar[int]
        VERSION_FIELD_NUMBER: _ClassVar[int]
        KAFKA_FIELD_NUMBER: _ClassVar[int]
        name: str
        version: int
        kafka: KafkaOriginMetadata
        def __init__(self, name: _Optional[str] = ..., version: _Optional[int] = ..., kafka: _Optional[_Union[KafkaOriginMetadata, _Mapping]] = ...) -> None: ...
    HTTP_TRANSACTION_FIELD_NUMBER: _ClassVar[int]
    HTTP_STATE_CHANGE_FIELD_NUMBER: _ClassVar[int]
    GRPC_TRANSACTION_FIELD_NUMBER: _ClassVar[int]
    GRPC_STATE_CHANGE_FIELD_NUMBER: _ClassVar[int]
    KAFKA_TRANSACTION_FIELD_NUMBER: _ClassVar[int]
    KAFKA_STATE_CHANGE_FIELD_NUMBER: _ClassVar[int]
    http_transaction: TransactionOrigin.HttpTransaction
    http_state_change: TransactionOrigin.HttpStateChange
    grpc_transaction: TransactionOrigin.GrpcTransaction
    grpc_state_change: TransactionOrigin.GrpcStateChange
    kafka_transaction: TransactionOrigin.KafkaTransaction
    kafka_state_change: TransactionOrigin.KafkaStateChange
    def __init__(self, http_transaction: _Optional[_Union[TransactionOrigin.HttpTransaction, _Mapping]] = ..., http_state_change: _Optional[_Union[TransactionOrigin.HttpStateChange, _Mapping]] = ..., grpc_transaction: _Optional[_Union[TransactionOrigin.GrpcTransaction, _Mapping]] = ..., grpc_state_change: _Optional[_Union[TransactionOrigin.GrpcStateChange, _Mapping]] = ..., kafka_transaction: _Optional[_Union[TransactionOrigin.KafkaTransaction, _Mapping]] = ..., kafka_state_change: _Optional[_Union[TransactionOrigin.KafkaStateChange, _Mapping]] = ...) -> None: ...

class TransactionMetadata(_message.Message):
    __slots__ = ("origin", "last_read_revision", "principal_attributes", "commit_message", "correlation_id", "causation_id")
    class PrincipalAttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    LAST_READ_REVISION_FIELD_NUMBER: _ClassVar[int]
    PRINCIPAL_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    COMMIT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    CAUSATION_ID_FIELD_NUMBER: _ClassVar[int]
    origin: TransactionOrigin
    last_read_revision: int
    principal_attributes: _containers.ScalarMap[str, str]
    commit_message: str
    correlation_id: str
    causation_id: str
    def __init__(self, origin: _Optional[_Union[TransactionOrigin, _Mapping]] = ..., last_read_revision: _Optional[int] = ..., principal_attributes: _Optional[_Mapping[str, str]] = ..., commit_message: _Optional[str] = ..., correlation_id: _Optional[str] = ..., causation_id: _Optional[str] = ...) -> None: ...

class TransactionSummary(_message.Message):
    __slots__ = ("id", "database", "basis", "revision", "timestamp", "metadata")
    ID_FIELD_NUMBER: _ClassVar[int]
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    BASIS_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    database: str
    basis: int
    revision: int
    timestamp: _timestamp_pb2.Timestamp
    metadata: TransactionMetadata
    def __init__(self, id: _Optional[str] = ..., database: _Optional[str] = ..., basis: _Optional[int] = ..., revision: _Optional[int] = ..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., metadata: _Optional[_Union[TransactionMetadata, _Mapping]] = ...) -> None: ...

class TransactionResult(_message.Message):
    __slots__ = ("transaction_summary", "event_id_mappings")
    class EventIdMappingsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    TRANSACTION_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    transaction_summary: TransactionSummary
    event_id_mappings: _containers.ScalarMap[str, str]
    def __init__(self, transaction_summary: _Optional[_Union[TransactionSummary, _Mapping]] = ..., event_id_mappings: _Optional[_Mapping[str, str]] = ...) -> None: ...

class Transaction(_message.Message):
    __slots__ = ("id", "database", "basis", "events", "timestamp", "metadata")
    ID_FIELD_NUMBER: _ClassVar[int]
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    BASIS_FIELD_NUMBER: _ClassVar[int]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    database: str
    basis: int
    events: _containers.RepeatedCompositeFieldContainer[_cloudevents_pb2.CloudEvent]
    timestamp: _timestamp_pb2.Timestamp
    metadata: TransactionMetadata
    def __init__(self, id: _Optional[str] = ..., database: _Optional[str] = ..., basis: _Optional[int] = ..., events: _Optional[_Iterable[_Union[_cloudevents_pb2.CloudEvent, _Mapping]]] = ..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., metadata: _Optional[_Union[TransactionMetadata, _Mapping]] = ...) -> None: ...

class StateViewMaintenanceMode(_message.Message):
    __slots__ = ("lazy", "eager")
    class Lazy(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class Eager(_message.Message):
        __slots__ = ("priority",)
        PRIORITY_FIELD_NUMBER: _ClassVar[int]
        priority: int
        def __init__(self, priority: _Optional[int] = ...) -> None: ...
    LAZY_FIELD_NUMBER: _ClassVar[int]
    EAGER_FIELD_NUMBER: _ClassVar[int]
    lazy: StateViewMaintenanceMode.Lazy
    eager: StateViewMaintenanceMode.Eager
    def __init__(self, lazy: _Optional[_Union[StateViewMaintenanceMode.Lazy, _Mapping]] = ..., eager: _Optional[_Union[StateViewMaintenanceMode.Eager, _Mapping]] = ...) -> None: ...

class StateViewIdentity(_message.Message):
    __slots__ = ("database_name", "state_view_name", "state_view_version")
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    STATE_VIEW_NAME_FIELD_NUMBER: _ClassVar[int]
    STATE_VIEW_VERSION_FIELD_NUMBER: _ClassVar[int]
    database_name: str
    state_view_name: str
    state_view_version: int
    def __init__(self, database_name: _Optional[str] = ..., state_view_name: _Optional[str] = ..., state_view_version: _Optional[int] = ...) -> None: ...

class StateViewDefinition(_message.Message):
    __slots__ = ("identity", "description", "selector", "query_temporality", "content_type", "content_schema_url", "maintenance_mode", "source_code_uri", "status")
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    QUERY_TEMPORALITY_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_SCHEMA_URL_FIELD_NUMBER: _ClassVar[int]
    MAINTENANCE_MODE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_CODE_URI_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    identity: StateViewIdentity
    description: str
    selector: UnboundEventSelector
    query_temporality: QueryTemporality
    content_type: str
    content_schema_url: str
    maintenance_mode: StateViewMaintenanceMode
    source_code_uri: str
    status: StateViewStatus
    def __init__(self, identity: _Optional[_Union[StateViewIdentity, _Mapping]] = ..., description: _Optional[str] = ..., selector: _Optional[_Union[UnboundEventSelector, _Mapping]] = ..., query_temporality: _Optional[_Union[QueryTemporality, str]] = ..., content_type: _Optional[str] = ..., content_schema_url: _Optional[str] = ..., maintenance_mode: _Optional[_Union[StateViewMaintenanceMode, _Mapping]] = ..., source_code_uri: _Optional[str] = ..., status: _Optional[_Union[StateViewStatus, str]] = ...) -> None: ...

class StateView(_message.Message):
    __slots__ = ("identity", "event_selector", "last_modified", "last_modified_revision", "content_type", "content_schema_url", "data", "url")
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    EVENT_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    LAST_MODIFIED_FIELD_NUMBER: _ClassVar[int]
    LAST_MODIFIED_REVISION_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_SCHEMA_URL_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    identity: StateViewIdentity
    event_selector: EventSelector
    last_modified: _timestamp_pb2.Timestamp
    last_modified_revision: int
    content_type: str
    content_schema_url: str
    data: bytes
    url: str
    def __init__(self, identity: _Optional[_Union[StateViewIdentity, _Mapping]] = ..., event_selector: _Optional[_Union[EventSelector, _Mapping]] = ..., last_modified: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., last_modified_revision: _Optional[int] = ..., content_type: _Optional[str] = ..., content_schema_url: _Optional[str] = ..., data: _Optional[bytes] = ..., url: _Optional[str] = ...) -> None: ...

class InvalidEvent(_message.Message):
    __slots__ = ("event", "errors")
    EVENT_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    event: _cloudevents_pb2.CloudEvent
    errors: _containers.RepeatedCompositeFieldContainer[EventInvalidation]
    def __init__(self, event: _Optional[_Union[_cloudevents_pb2.CloudEvent, _Mapping]] = ..., errors: _Optional[_Iterable[_Union[EventInvalidation, _Mapping]]] = ...) -> None: ...

class EventInvalidation(_message.Message):
    __slots__ = ("invalid_event_source", "invalid_stream_name", "invalid_event_id", "duplicate_event_id", "invalid_event_subject", "invalid_event_type")
    INVALID_EVENT_SOURCE_FIELD_NUMBER: _ClassVar[int]
    INVALID_STREAM_NAME_FIELD_NUMBER: _ClassVar[int]
    INVALID_EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    DUPLICATE_EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    INVALID_EVENT_SUBJECT_FIELD_NUMBER: _ClassVar[int]
    INVALID_EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    invalid_event_source: InvalidEventSource
    invalid_stream_name: InvalidStreamName
    invalid_event_id: InvalidEventId
    duplicate_event_id: DuplicateEventId
    invalid_event_subject: InvalidEventSubject
    invalid_event_type: InvalidEventType
    def __init__(self, invalid_event_source: _Optional[_Union[InvalidEventSource, _Mapping]] = ..., invalid_stream_name: _Optional[_Union[InvalidStreamName, _Mapping]] = ..., invalid_event_id: _Optional[_Union[InvalidEventId, _Mapping]] = ..., duplicate_event_id: _Optional[_Union[DuplicateEventId, _Mapping]] = ..., invalid_event_subject: _Optional[_Union[InvalidEventSubject, _Mapping]] = ..., invalid_event_type: _Optional[_Union[InvalidEventType, _Mapping]] = ...) -> None: ...

class InvalidAppendCondition(_message.Message):
    __slots__ = ("index", "errors")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    index: int
    errors: _containers.RepeatedCompositeFieldContainer[AppendConditionInvalidation]
    def __init__(self, index: _Optional[int] = ..., errors: _Optional[_Iterable[_Union[AppendConditionInvalidation, _Mapping]]] = ...) -> None: ...

class AppendConditionInvalidation(_message.Message):
    __slots__ = ("invalid_event_subject", "invalid_stream_name", "invalid_append_condition_range", "append_condition_conflict")
    INVALID_EVENT_SUBJECT_FIELD_NUMBER: _ClassVar[int]
    INVALID_STREAM_NAME_FIELD_NUMBER: _ClassVar[int]
    INVALID_APPEND_CONDITION_RANGE_FIELD_NUMBER: _ClassVar[int]
    APPEND_CONDITION_CONFLICT_FIELD_NUMBER: _ClassVar[int]
    invalid_event_subject: InvalidEventSubject
    invalid_stream_name: InvalidStreamName
    invalid_append_condition_range: InvalidAppendConditionRange
    append_condition_conflict: AppendConditionConflict
    def __init__(self, invalid_event_subject: _Optional[_Union[InvalidEventSubject, _Mapping]] = ..., invalid_stream_name: _Optional[_Union[InvalidStreamName, _Mapping]] = ..., invalid_append_condition_range: _Optional[_Union[InvalidAppendConditionRange, _Mapping]] = ..., append_condition_conflict: _Optional[_Union[AppendConditionConflict, _Mapping]] = ...) -> None: ...

class InvalidAppendConditionRange(_message.Message):
    __slots__ = ("min", "max")
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    min: int
    max: int
    def __init__(self, min: _Optional[int] = ..., max: _Optional[int] = ...) -> None: ...

class AppendConditionConflict(_message.Message):
    __slots__ = ("lhs", "rhs")
    LHS_FIELD_NUMBER: _ClassVar[int]
    RHS_FIELD_NUMBER: _ClassVar[int]
    lhs: AppendCondition
    rhs: AppendCondition
    def __init__(self, lhs: _Optional[_Union[AppendCondition, _Mapping]] = ..., rhs: _Optional[_Union[AppendCondition, _Mapping]] = ...) -> None: ...

class EmptyAppendCondition(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class InvalidEventSource(_message.Message):
    __slots__ = ("event_source",)
    EVENT_SOURCE_FIELD_NUMBER: _ClassVar[int]
    event_source: str
    def __init__(self, event_source: _Optional[str] = ...) -> None: ...

class InvalidStreamName(_message.Message):
    __slots__ = ("stream_name",)
    STREAM_NAME_FIELD_NUMBER: _ClassVar[int]
    stream_name: str
    def __init__(self, stream_name: _Optional[str] = ...) -> None: ...

class InvalidEventId(_message.Message):
    __slots__ = ("stream", "event_id")
    STREAM_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    stream: str
    event_id: str
    def __init__(self, stream: _Optional[str] = ..., event_id: _Optional[str] = ...) -> None: ...

class DuplicateEventId(_message.Message):
    __slots__ = ("stream", "event_id")
    STREAM_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    stream: str
    event_id: str
    def __init__(self, stream: _Optional[str] = ..., event_id: _Optional[str] = ...) -> None: ...

class InvalidEventSubject(_message.Message):
    __slots__ = ("event_subject",)
    EVENT_SUBJECT_FIELD_NUMBER: _ClassVar[int]
    event_subject: str
    def __init__(self, event_subject: _Optional[str] = ...) -> None: ...

class InvalidEventType(_message.Message):
    __slots__ = ("event_type",)
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    event_type: str
    def __init__(self, event_type: _Optional[str] = ...) -> None: ...

class StateChangeIdentity(_message.Message):
    __slots__ = ("database_name", "state_change_name", "state_change_version")
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    STATE_CHANGE_NAME_FIELD_NUMBER: _ClassVar[int]
    STATE_CHANGE_VERSION_FIELD_NUMBER: _ClassVar[int]
    database_name: str
    state_change_name: str
    state_change_version: int
    def __init__(self, database_name: _Optional[str] = ..., state_change_name: _Optional[str] = ..., state_change_version: _Optional[int] = ...) -> None: ...

class StateChangeDefinition(_message.Message):
    __slots__ = ("identity", "description", "source_code_uri", "status")
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SOURCE_CODE_URI_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    identity: StateChangeIdentity
    description: str
    source_code_uri: str
    status: StateChangeStatus
    def __init__(self, identity: _Optional[_Union[StateChangeIdentity, _Mapping]] = ..., description: _Optional[str] = ..., source_code_uri: _Optional[str] = ..., status: _Optional[_Union[StateChangeStatus, str]] = ...) -> None: ...

class AsyncTransactionResponse(_message.Message):
    __slots__ = ("success", "error")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: TransactionResult
    error: AsyncTransactionError
    def __init__(self, success: _Optional[_Union[TransactionResult, _Mapping]] = ..., error: _Optional[_Union[AsyncTransactionError, _Mapping]] = ...) -> None: ...

class AsyncTransactionError(_message.Message):
    __slots__ = ("error_code", "message", "details")
    class DetailsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    error_code: str
    message: str
    details: _containers.ScalarMap[str, str]
    def __init__(self, error_code: _Optional[str] = ..., message: _Optional[str] = ..., details: _Optional[_Mapping[str, str]] = ...) -> None: ...
