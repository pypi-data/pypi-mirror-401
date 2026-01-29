"""Timestamp conversion utilities."""

from __future__ import annotations

from datetime import UTC, datetime

from google.protobuf.timestamp_pb2 import Timestamp

from evidentsource_client.conversions.error import InvalidTimestamp


def timestamp_to_datetime(ts: Timestamp) -> datetime:
    """Convert a protobuf Timestamp to a datetime.

    Args:
        ts: The protobuf Timestamp

    Returns:
        A timezone-aware datetime in UTC

    Raises:
        InvalidTimestamp: If the timestamp is invalid
    """
    try:
        return datetime.fromtimestamp(
            ts.seconds + ts.nanos / 1_000_000_000,
            tz=UTC,
        )
    except (ValueError, OSError) as e:
        raise InvalidTimestamp() from e


def datetime_to_timestamp(dt: datetime) -> Timestamp:
    """Convert a datetime to a protobuf Timestamp.

    Args:
        dt: The datetime to convert (will be converted to UTC if not already)

    Returns:
        A protobuf Timestamp
    """
    # Ensure we have a UTC timestamp
    dt = dt.replace(tzinfo=UTC) if dt.tzinfo is None else dt.astimezone(UTC)

    ts = Timestamp()
    ts.seconds = int(dt.timestamp())
    ts.nanos = dt.microsecond * 1000
    return ts
