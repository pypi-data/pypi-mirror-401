"""AppendCondition type conversions."""

from __future__ import annotations

from evidentsource_core import (
    AppendCondition,
    MaxConstraint,
    MinConstraint,
    Range,
    RangeConstraint,
)

from evidentsource_client.proto import domain_pb2 as proto

from .error import InvalidRange, MissingField, MissingOneof, NestedConversionError
from .selectors import proto_to_selector, selector_to_proto

# =============================================================================
# Domain -> Proto
# =============================================================================


def constraint_to_proto(constraint: AppendCondition) -> proto.AppendCondition:
    """Convert an AppendCondition to a proto AppendCondition."""
    if isinstance(constraint, MinConstraint):
        return proto.AppendCondition(
            min=proto.AppendCondition.Min(
                selector=selector_to_proto(constraint.selector),
                revision=constraint.revision,
            )
        )
    elif isinstance(constraint, MaxConstraint):
        return proto.AppendCondition(
            max=proto.AppendCondition.Max(
                selector=selector_to_proto(constraint.selector),
                revision=constraint.revision,
            )
        )
    elif isinstance(constraint, RangeConstraint):
        return proto.AppendCondition(
            range=proto.AppendCondition.Range(
                selector=selector_to_proto(constraint.selector),
                min=constraint.range.min,
                max=constraint.range.max,
            )
        )
    raise TypeError(f"Unknown constraint type: {type(constraint)}")


# =============================================================================
# Proto -> Domain
# =============================================================================


def proto_to_constraint(proto_constraint: proto.AppendCondition) -> AppendCondition:
    """Convert a proto AppendCondition to an AppendCondition."""
    # Check which field is set by examining the fields directly
    if proto_constraint.HasField("min"):
        min_constraint = proto_constraint.min
        if not min_constraint.HasField("selector"):
            raise MissingField("AppendCondition.Min", "selector")

        try:
            selector = proto_to_selector(min_constraint.selector)
        except Exception as e:
            raise NestedConversionError("AppendCondition.Min.selector", e) from e

        return MinConstraint(selector, min_constraint.revision)

    elif proto_constraint.HasField("max"):
        max_constraint = proto_constraint.max
        if not max_constraint.HasField("selector"):
            raise MissingField("AppendCondition.Max", "selector")

        try:
            selector = proto_to_selector(max_constraint.selector)
        except Exception as e:
            raise NestedConversionError("AppendCondition.Max.selector", e) from e

        return MaxConstraint(selector, max_constraint.revision)

    elif proto_constraint.HasField("range"):
        range_constraint = proto_constraint.range
        if not range_constraint.HasField("selector"):
            raise MissingField("AppendCondition.Range", "selector")

        try:
            selector = proto_to_selector(range_constraint.selector)
        except Exception as e:
            raise NestedConversionError("AppendCondition.Range.selector", e) from e

        try:
            domain_range = Range.new(range_constraint.min, range_constraint.max)
        except Exception as e:
            raise InvalidRange(range_constraint.min, range_constraint.max) from e

        return RangeConstraint(selector, domain_range)

    raise MissingOneof("AppendCondition", "condition")
