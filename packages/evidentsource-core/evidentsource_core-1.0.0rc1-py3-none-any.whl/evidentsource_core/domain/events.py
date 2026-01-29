"""Event types for the event log.

This module defines the core event types used in the database.

EvidentSource uses CloudEvents as its event format, but with specialized semantics:
- `ProspectiveEvent`: Events before storage, where `stream` is the simple stream name
- `Event`: Events after storage, where `source` is a full URI containing the stream path
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

if TYPE_CHECKING:
    from datetime import datetime

# =============================================================================
# EventData
# =============================================================================


@attrs.frozen
class BinaryEventData:
    """Binary data payload."""

    data: bytes

    def as_bytes(self) -> bytes:
        """Get the data as bytes."""
        return self.data


@attrs.frozen
class StringEventData:
    """String data payload (typically JSON)."""

    data: str

    def as_bytes(self) -> bytes:
        """Get the data as bytes (UTF-8 encoded)."""
        return self.data.encode("utf-8")


EventData = BinaryEventData | StringEventData
"""Event data payload - either binary or string."""


def event_data_as_bytes(data: EventData) -> bytes:
    """Get event data as bytes."""
    return data.as_bytes()


# =============================================================================
# ExtensionValue
# =============================================================================


@attrs.frozen
class BooleanExtension:
    """Boolean extension value."""

    value: bool


@attrs.frozen
class IntegerExtension:
    """Integer extension value (CloudEvents spec: -2,147,483,648 to +2,147,483,647)."""

    value: int


@attrs.frozen
class StringExtension:
    """String extension value."""

    value: str


ExtensionValue = BooleanExtension | IntegerExtension | StringExtension
"""Extension attribute value types supported by CloudEvents."""


# =============================================================================
# ProspectiveEvent
# =============================================================================


@attrs.define
class ProspectiveEvent:
    """A prospective event before storage.

    In EvidentSource, prospective events use the stream name directly as the source.
    When stored, the server transforms this into a full URI in the `Event` type.
    """

    id: str
    """Unique identifier for this event (typically UUID)."""

    stream: str
    """The stream this event belongs to. Maps to CloudEvents `source`."""

    event_type: str
    """The event type (e.g., "com.example.account.opened")."""

    subject: str | None = None
    """Optional subject identifying the entity this event is about."""

    data: EventData | None = None
    """Optional event data payload."""

    time: datetime | None = None
    """Optional timestamp when the event occurred."""

    datacontenttype: str | None = None
    """Optional content type of the data (e.g., "application/json")."""

    dataschema: str | None = None
    """Optional schema URI for the data."""

    extensions: dict[str, ExtensionValue] = attrs.field(factory=dict)
    """Extension attributes."""

    def get_stream(self) -> str:
        """Get the stream name."""
        return self.stream

    def get_event_type(self) -> str:
        """Get the event type."""
        return self.event_type

    def get_subject(self) -> str | None:
        """Get the subject, if present."""
        return self.subject

    def get_data(self) -> EventData | None:
        """Get the data payload, if present."""
        return self.data

    def get_time(self) -> datetime | None:
        """Get the timestamp, if present."""
        return self.time

    def extension(self, key: str) -> ExtensionValue | None:
        """Get an extension value by key."""
        return self.extensions.get(key)


# =============================================================================
# Event
# =============================================================================


@attrs.define
class Event:
    """A stored event with a full source URI.

    After storage, the EvidentSource server transforms the stream name into a full URI
    like `https://host/db/database-name/streams/stream-name`.
    """

    id: str
    """Unique identifier for this event."""

    source: str
    """Full source URI (e.g., "https://host/db/name/streams/stream")."""

    event_type: str
    """The event type (e.g., "com.example.account.opened")."""

    subject: str | None = None
    """Optional subject identifying the entity this event is about."""

    data: EventData | None = None
    """Optional event data payload."""

    time: datetime | None = None
    """Optional timestamp when the event occurred."""

    datacontenttype: str | None = None
    """Optional content type of the data."""

    dataschema: str | None = None
    """Optional schema URI for the data."""

    extensions: dict[str, ExtensionValue] = attrs.field(factory=dict)
    """Extension attributes."""

    def get_source(self) -> str:
        """Get the full source URI."""
        return self.source

    def stream(self) -> str | None:
        """Extract the stream name from the source URI.

        Parses URIs like `https://host/db/name/streams/my-stream` to extract `my-stream`.
        Returns None if the URI doesn't match the expected pattern.
        """
        marker = "/streams/"
        idx = self.source.find(marker)
        if idx == -1:
            return None
        return self.source[idx + len(marker) :]

    def get_event_type(self) -> str:
        """Get the event type."""
        return self.event_type

    def get_subject(self) -> str | None:
        """Get the subject, if present."""
        return self.subject

    def get_data(self) -> EventData | None:
        """Get the data payload, if present."""
        return self.data

    def get_time(self) -> datetime | None:
        """Get the timestamp, if present."""
        return self.time

    def extension(self, key: str) -> ExtensionValue | None:
        """Get an extension value by key."""
        return self.extensions.get(key)


# =============================================================================
# Transaction
# =============================================================================


@attrs.frozen
class TransactionSummary:
    """Summary information about a transaction."""

    revision: int
    """The revision at which this transaction was committed."""

    event_count: int
    """Number of events in the transaction."""

    transaction_id: str | None = None
    """Optional transaction identifier."""


@attrs.frozen
class Transaction:
    """A transaction of events that were transacted together."""

    events: list[Event]
    """The events in this transaction."""

    summary: TransactionSummary
    """Summary information about the transaction."""
