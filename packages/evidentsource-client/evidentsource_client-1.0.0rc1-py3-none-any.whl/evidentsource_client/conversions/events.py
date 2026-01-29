"""Event and Transaction type conversions."""

from __future__ import annotations

from datetime import datetime

from evidentsource_core import (
    BinaryEventData,
    BooleanExtension,
    Event,
    ExtensionValue,
    IntegerExtension,
    ProspectiveEvent,
    StringEventData,
    StringExtension,
    Transaction,
    TransactionSummary,
)

from evidentsource_client.proto import cloudevents_pb2 as proto_ce
from evidentsource_client.proto import domain_pb2 as proto

from .timestamps import datetime_to_timestamp, timestamp_to_datetime

# =============================================================================
# Event: Domain -> Proto
# =============================================================================


def event_to_proto(event: Event) -> proto_ce.CloudEvent:
    """Convert an Event to a CloudEvent proto."""
    attributes: dict[str, proto_ce.CloudEvent.CloudEventAttributeValue] = {}

    # Add optional attributes
    if event.subject is not None:
        attributes["subject"] = proto_ce.CloudEvent.CloudEventAttributeValue(
            ce_string=event.subject
        )

    if event.time is not None:
        attributes["time"] = proto_ce.CloudEvent.CloudEventAttributeValue(
            ce_timestamp=datetime_to_timestamp(event.time)
        )

    if event.datacontenttype is not None:
        attributes["datacontenttype"] = proto_ce.CloudEvent.CloudEventAttributeValue(
            ce_string=event.datacontenttype
        )

    if event.dataschema is not None:
        attributes["dataschema"] = proto_ce.CloudEvent.CloudEventAttributeValue(
            ce_uri=event.dataschema
        )

    # Add extension attributes
    for key, value in event.extensions.items():
        attr_value = _extension_to_attr(value)
        if attr_value is not None:
            attributes[key] = attr_value

    # Build CloudEvent
    ce = proto_ce.CloudEvent(
        spec_version="1.0",
        id=event.id,
        source=event.source,
        type=event.event_type,
        attributes=attributes,
    )

    # Handle data
    if event.data is not None:
        if isinstance(event.data, BinaryEventData):
            ce.binary_data = event.data.data
        elif isinstance(event.data, StringEventData):
            ce.text_data = event.data.data

    return ce


def prospective_event_to_proto(event: ProspectiveEvent) -> proto_ce.CloudEvent:
    """Convert a ProspectiveEvent to a CloudEvent proto."""
    attributes: dict[str, proto_ce.CloudEvent.CloudEventAttributeValue] = {}

    # Add optional attributes
    if event.subject is not None:
        attributes["subject"] = proto_ce.CloudEvent.CloudEventAttributeValue(
            ce_string=event.subject
        )

    if event.time is not None:
        attributes["time"] = proto_ce.CloudEvent.CloudEventAttributeValue(
            ce_timestamp=datetime_to_timestamp(event.time)
        )

    if event.datacontenttype is not None:
        attributes["datacontenttype"] = proto_ce.CloudEvent.CloudEventAttributeValue(
            ce_string=event.datacontenttype
        )

    if event.dataschema is not None:
        attributes["dataschema"] = proto_ce.CloudEvent.CloudEventAttributeValue(
            ce_uri=event.dataschema
        )

    # Add extension attributes
    for key, value in event.extensions.items():
        attr_value = _extension_to_attr(value)
        if attr_value is not None:
            attributes[key] = attr_value

    # Build CloudEvent - ProspectiveEvent uses stream as source
    ce = proto_ce.CloudEvent(
        spec_version="1.0",
        id=event.id,
        source=event.stream,
        type=event.event_type,
        attributes=attributes,
    )

    # Handle data
    if event.data is not None:
        if isinstance(event.data, BinaryEventData):
            ce.binary_data = event.data.data
        elif isinstance(event.data, StringEventData):
            ce.text_data = event.data.data

    return ce


def _extension_to_attr(
    value: ExtensionValue,
) -> proto_ce.CloudEvent.CloudEventAttributeValue | None:
    """Convert an ExtensionValue to a CloudEventAttributeValue."""
    if isinstance(value, StringExtension):
        return proto_ce.CloudEvent.CloudEventAttributeValue(ce_string=value.value)
    elif isinstance(value, BooleanExtension):
        return proto_ce.CloudEvent.CloudEventAttributeValue(ce_boolean=value.value)
    elif isinstance(value, IntegerExtension):
        return proto_ce.CloudEvent.CloudEventAttributeValue(ce_integer=value.value)
    return None


# =============================================================================
# Event: Proto -> Domain
# =============================================================================


def proto_to_event(proto_event: proto_ce.CloudEvent) -> Event:
    """Convert a CloudEvent proto to an Event."""
    subject: str | None = None
    time: datetime | None = None
    datacontenttype: str | None = None
    dataschema: str | None = None
    extensions: dict[str, ExtensionValue] = {}

    # Process attributes
    for key, value in proto_event.attributes.items():
        which = value.WhichOneof("attr")
        if which is None:
            continue

        if key == "subject" and which == "ce_string":
            subject = value.ce_string
        elif key == "time" and which == "ce_timestamp":
            time = timestamp_to_datetime(value.ce_timestamp)
        elif key == "datacontenttype" and which == "ce_string":
            datacontenttype = value.ce_string
        elif key == "dataschema" and which == "ce_uri":
            dataschema = value.ce_uri
        elif which == "ce_string":
            extensions[key] = StringExtension(value.ce_string)
        elif which == "ce_boolean":
            extensions[key] = BooleanExtension(value.ce_boolean)
        elif which == "ce_integer":
            extensions[key] = IntegerExtension(value.ce_integer)

    # Handle data
    data: BinaryEventData | StringEventData | None = None
    data_which = proto_event.WhichOneof("data")
    if data_which == "binary_data":
        data = BinaryEventData(proto_event.binary_data)
    elif data_which == "text_data":
        data = StringEventData(proto_event.text_data)

    return Event(
        id=proto_event.id,
        source=proto_event.source,
        event_type=proto_event.type,
        subject=subject,
        data=data,
        time=time,
        datacontenttype=datacontenttype,
        dataschema=dataschema,
        extensions=extensions,
    )


# =============================================================================
# Transaction and TransactionSummary: Proto -> Domain
# =============================================================================


def proto_to_transaction(proto_transaction: proto.Transaction) -> Transaction:
    """Convert a Transaction proto to a domain Transaction."""
    events = [proto_to_event(e) for e in proto_transaction.events]

    return Transaction(
        events=events,
        summary=TransactionSummary(
            revision=proto_transaction.basis + len(events),
            event_count=len(events),
            transaction_id=proto_transaction.id if proto_transaction.id else None,
        ),
    )


def proto_to_transaction_summary(proto_summary: proto.TransactionSummary) -> TransactionSummary:
    """Convert a TransactionSummary proto to a domain TransactionSummary."""
    return TransactionSummary(
        revision=proto_summary.revision,
        event_count=int(proto_summary.revision - proto_summary.basis),
        transaction_id=proto_summary.id if proto_summary.id else None,
    )
