"""EventSelector type conversions."""

from __future__ import annotations

from evidentsource_core import (
    AndSelector,
    EqualsSelector,
    EventAttribute,
    EventAttributePrefix,
    EventSelector,
    EventSubject,
    EventType,
    EventTypeAttribute,
    EventTypePrefix,
    OrSelector,
    StartsWithSelector,
    StreamAttribute,
    StreamName,
    StreamPrefix,
    SubjectAttribute,
    SubjectPrefix,
)

from evidentsource_client.proto import domain_pb2 as proto

from .error import ConversionError, MissingField, MissingOneof, NestedConversionError

# =============================================================================
# Domain -> Proto
# =============================================================================


def selector_to_proto(selector: EventSelector) -> proto.EventSelector:
    """Convert an EventSelector to a proto EventSelector."""
    if isinstance(selector, EqualsSelector):
        return proto.EventSelector(equals=_attribute_to_proto(selector.attribute))
    elif isinstance(selector, StartsWithSelector):
        return proto.EventSelector(starts_with=_prefix_to_proto(selector.prefix))
    elif isinstance(selector, AndSelector):
        return proto.EventSelector(
            and_=proto.EventSelector.LogicalAnd(
                left=selector_to_proto(selector.left),
                right=selector_to_proto(selector.right),
            )
        )
    elif isinstance(selector, OrSelector):
        return proto.EventSelector(
            or_=proto.EventSelector.LogicalOr(
                left=selector_to_proto(selector.left),
                right=selector_to_proto(selector.right),
            )
        )
    raise TypeError(f"Unknown selector type: {type(selector)}")


def _attribute_to_proto(attr: EventAttribute) -> proto.EventAttribute:
    """Convert an EventAttribute to a proto EventAttribute."""
    if isinstance(attr, StreamAttribute):
        return proto.EventAttribute(stream=str(attr.stream))
    elif isinstance(attr, SubjectAttribute):
        if attr.subject is None:
            return proto.EventAttribute(
                subject=proto.EventAttribute.SubjectValue(has_value=False, value="")
            )
        return proto.EventAttribute(
            subject=proto.EventAttribute.SubjectValue(has_value=True, value=str(attr.subject))
        )
    elif isinstance(attr, EventTypeAttribute):
        return proto.EventAttribute(event_type=str(attr.event_type))
    raise TypeError(f"Unknown attribute type: {type(attr)}")


def _prefix_to_proto(prefix: EventAttributePrefix) -> proto.EventSelector.StartsWith:
    """Convert an EventAttributePrefix to a proto StartsWith."""
    if isinstance(prefix, StreamPrefix):
        return proto.EventSelector.StartsWith(stream=str(prefix.stream))
    elif isinstance(prefix, SubjectPrefix):
        return proto.EventSelector.StartsWith(subject=str(prefix.subject))
    elif isinstance(prefix, EventTypePrefix):
        return proto.EventSelector.StartsWith(event_type=str(prefix.event_type))
    raise TypeError(f"Unknown prefix type: {type(prefix)}")


# =============================================================================
# Proto -> Domain
# =============================================================================


def proto_to_selector(proto_selector: proto.EventSelector) -> EventSelector:
    """Convert a proto EventSelector to an EventSelector."""
    which = proto_selector.WhichOneof("selector")

    if which is None:
        raise MissingOneof("EventSelector", "selector")

    if which == "equals":
        attr = _proto_to_attribute(proto_selector.equals)
        return EqualsSelector(attr)
    elif which == "starts_with":
        prefix = _proto_to_prefix(proto_selector.starts_with)
        return StartsWithSelector(prefix)
    elif which == "and_":
        logical_and = proto_selector.and_
        if not logical_and.HasField("left"):
            raise MissingField("EventSelector.LogicalAnd", "left")
        if not logical_and.HasField("right"):
            raise MissingField("EventSelector.LogicalAnd", "right")

        try:
            left = proto_to_selector(logical_and.left)
        except ConversionError as e:
            raise NestedConversionError("And.left", e) from e

        try:
            right = proto_to_selector(logical_and.right)
        except ConversionError as e:
            raise NestedConversionError("And.right", e) from e

        return AndSelector(left=left, right=right)
    elif which == "or_":
        logical_or = proto_selector.or_
        if not logical_or.HasField("left"):
            raise MissingField("EventSelector.LogicalOr", "left")
        if not logical_or.HasField("right"):
            raise MissingField("EventSelector.LogicalOr", "right")

        try:
            left = proto_to_selector(logical_or.left)
        except ConversionError as e:
            raise NestedConversionError("Or.left", e) from e

        try:
            right = proto_to_selector(logical_or.right)
        except ConversionError as e:
            raise NestedConversionError("Or.right", e) from e

        return OrSelector(left=left, right=right)

    raise MissingOneof("EventSelector", "selector")


def _proto_to_attribute(proto_attr: proto.EventAttribute) -> EventAttribute:
    """Convert a proto EventAttribute to an EventAttribute."""
    which = proto_attr.WhichOneof("attribute")

    if which is None:
        raise MissingOneof("EventAttribute", "attribute")

    if which == "stream":
        return StreamAttribute(StreamName(proto_attr.stream))
    elif which == "subject":
        subj = proto_attr.subject
        if subj.has_value:
            return SubjectAttribute(EventSubject(subj.value))
        return SubjectAttribute(None)
    elif which == "event_type":
        return EventTypeAttribute(EventType(proto_attr.event_type))

    raise MissingOneof("EventAttribute", "attribute")


def _proto_to_prefix(
    proto_starts_with: proto.EventSelector.StartsWith,
) -> EventAttributePrefix:
    """Convert a proto StartsWith to an EventAttributePrefix."""
    which = proto_starts_with.WhichOneof("attribute")

    if which is None:
        raise MissingOneof("StartsWith", "attribute")

    if which == "stream":
        return StreamPrefix(StreamName(proto_starts_with.stream))
    elif which == "subject":
        return SubjectPrefix(EventSubject(proto_starts_with.subject))
    elif which == "event_type":
        return EventTypePrefix(EventType(proto_starts_with.event_type))

    raise MissingOneof("StartsWith", "attribute")
