"""Type conversions between proto and domain types.

This module provides bidirectional conversion between the gRPC proto types
generated from service.proto/domain.proto and the domain types from the
evidentsource-core package.

## Conversion Conventions

- **Domain -> Proto**: Functions named `*_to_proto` (infallible)
- **Proto -> Domain**: Functions named `proto_to_*` (may raise ConversionError)

The fallible direction handles cases where proto messages may have missing
required fields, invalid identifiers, or other validation failures.
"""

from evidentsource_client.conversions.constraints import (
    constraint_to_proto,
    proto_to_constraint,
)
from evidentsource_client.conversions.error import (
    ConversionError,
    InvalidConstraint,
    InvalidIdentifier,
    InvalidRange,
    InvalidTimestamp,
    MissingField,
    MissingOneof,
    NestedConversionError,
    UnknownEnumVariant,
)
from evidentsource_client.conversions.events import (
    event_to_proto,
    prospective_event_to_proto,
    proto_to_event,
    proto_to_transaction,
    proto_to_transaction_summary,
)
from evidentsource_client.conversions.selectors import (
    proto_to_selector,
    selector_to_proto,
)
from evidentsource_client.conversions.timestamps import (
    datetime_to_timestamp,
    timestamp_to_datetime,
)

__all__ = [
    # Errors
    "ConversionError",
    "MissingField",
    "MissingOneof",
    "InvalidIdentifier",
    "InvalidConstraint",
    "NestedConversionError",
    "UnknownEnumVariant",
    "InvalidRange",
    "InvalidTimestamp",
    # Timestamps
    "timestamp_to_datetime",
    "datetime_to_timestamp",
    # Events
    "event_to_proto",
    "prospective_event_to_proto",
    "proto_to_event",
    "proto_to_transaction",
    "proto_to_transaction_summary",
    # Selectors
    "selector_to_proto",
    "proto_to_selector",
    # Constraints
    "constraint_to_proto",
    "proto_to_constraint",
]
