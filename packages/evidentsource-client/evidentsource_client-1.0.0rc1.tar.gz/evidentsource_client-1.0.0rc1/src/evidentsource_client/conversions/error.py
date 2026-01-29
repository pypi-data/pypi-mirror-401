"""Conversion error types."""

from __future__ import annotations


class ConversionError(Exception):
    """Base class for conversion errors."""

    pass


class MissingField(ConversionError):
    """A required field was missing in the proto message."""

    def __init__(self, message_type: str, field: str) -> None:
        super().__init__(f"missing required field '{field}' in {message_type}")
        self.message_type = message_type
        self.field = field


class MissingOneof(ConversionError):
    """A oneof field had no variant set."""

    def __init__(self, message_type: str, oneof_name: str) -> None:
        super().__init__(f"missing oneof variant '{oneof_name}' in {message_type}")
        self.message_type = message_type
        self.oneof_name = oneof_name


class InvalidIdentifier(ConversionError):
    """An identifier failed validation."""

    def __init__(self, message: str) -> None:
        super().__init__(f"invalid identifier: {message}")


class InvalidConstraint(ConversionError):
    """A constraint was invalid."""

    def __init__(self, message: str) -> None:
        super().__init__(f"invalid constraint: {message}")


class NestedConversionError(ConversionError):
    """A nested conversion failed."""

    def __init__(self, context: str, source: Exception) -> None:
        super().__init__(f"nested conversion error in {context}: {source}")
        self.context = context
        self.source = source


class UnknownEnumVariant(ConversionError):
    """An enum variant was unrecognized."""

    def __init__(self, enum_name: str, value: int) -> None:
        super().__init__(f"unknown enum variant {value} for {enum_name}")
        self.enum_name = enum_name
        self.value = value


class InvalidRange(ConversionError):
    """Invalid range (min > max)."""

    def __init__(self, min_val: int, max_val: int) -> None:
        super().__init__(f"invalid range: min ({min_val}) > max ({max_val})")
        self.min_val = min_val
        self.max_val = max_val


class InvalidTimestamp(ConversionError):
    """Invalid timestamp."""

    def __init__(self) -> None:
        super().__init__("invalid timestamp")
