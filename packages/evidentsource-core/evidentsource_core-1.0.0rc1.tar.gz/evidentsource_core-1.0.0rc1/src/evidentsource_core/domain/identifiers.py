"""Identifier types for database entities.

This module contains validated string wrapper types for various identifiers
used throughout the system: database names, stream names, event IDs, etc.
"""

from __future__ import annotations

import re
from typing import Self

import attrs

from evidentsource_core.domain.errors import (
    InvalidDatabaseName,
    InvalidEventId,
    InvalidEventSubject,
    InvalidEventType,
    InvalidStateChangeName,
    InvalidStateViewName,
    InvalidStreamName,
)

# =============================================================================
# Constants
# =============================================================================

SAFE_DELIMITER: str = "\u001f"
"""Unit separator character used as a safe delimiter in composite keys."""

SEQUENCE_KEY: str = "sequence"
"""Key name for sequence attribute in events."""

RECORDEDTIME_KEY: str = "recordedtime"
"""Key name for recorded time attribute in events."""

NAME_PATTERN_STR: str = r"^[a-zA-Z][a-zA-Z0-9\-_.]{1,127}$"
"""Pattern string for name validation (shared by multiple types)."""

NAME_PATTERN: re.Pattern[str] = re.compile(NAME_PATTERN_STR)
"""Compiled regex for name validation."""


def _is_valid_name(value: str) -> bool:
    """Check if value matches the name pattern."""
    return bool(NAME_PATTERN.match(value))


def _is_non_blank_lt_256_no_delimiter(value: str) -> bool:
    """Check if value is non-blank, under 256 chars, and has no safe delimiter."""
    return bool(value.strip()) and len(value) < 256 and SAFE_DELIMITER not in value


# =============================================================================
# DatabaseName
# =============================================================================


@attrs.frozen(order=True)
class DatabaseName:
    """A validated database name.

    Database names must:
    - Start with a letter (a-z, A-Z)
    - Contain only letters, digits, hyphens, underscores, or dots
    - Be 2-128 characters long
    """

    value: str = attrs.field()

    @value.validator
    def _validate_value(self, attribute: attrs.Attribute[str], value: str) -> None:
        if not _is_valid_name(value):
            raise InvalidDatabaseName(value)

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"DatabaseName({self.value!r})"


# =============================================================================
# StreamName
# =============================================================================


@attrs.frozen(order=True)
class StreamName:
    """A validated stream name.

    Stream names follow the same validation rules as database names.
    """

    value: str = attrs.field()

    @value.validator
    def _validate_value(self, attribute: attrs.Attribute[str], value: str) -> None:
        if not _is_valid_name(value):
            raise InvalidStreamName(value)

    @classmethod
    def from_source(cls, url: str) -> Self:
        """Extract stream name from a CloudEvents source URL.

        The stream name is extracted as the last path segment of the URL.

        Args:
            url: A CloudEvents source URL (e.g., "http://example.com/streams/my-stream")

        Returns:
            StreamName extracted from the URL

        Raises:
            InvalidStreamName: If the URL has no path segments or the stream name is invalid
        """
        parts = url.split("/")
        if not parts:
            raise InvalidStreamName(url)
        source = parts[-1]
        if not source:
            raise InvalidStreamName(url)
        return cls(source)

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        # Truncate long values like Rust does
        truncated = self.value[:8] + "..." if len(self.value) > 8 else self.value
        return f"StreamName({truncated!r})"


# =============================================================================
# EventId
# =============================================================================


@attrs.frozen(order=True)
class EventId:
    """A validated event ID.

    Event IDs must:
    - Be non-blank (after trimming whitespace)
    - Be less than 256 characters
    - Not contain the safe delimiter character (U+001F)
    """

    value: str = attrs.field()

    @value.validator
    def _validate_value(self, attribute: attrs.Attribute[str], value: str) -> None:
        if not _is_non_blank_lt_256_no_delimiter(value):
            raise InvalidEventId(value)

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        # Truncate long values like Rust does
        truncated = self.value[:8] + "..." if len(self.value) > 8 else self.value
        return f"EventId({truncated!r})"


# =============================================================================
# EventType
# =============================================================================


@attrs.frozen(order=True)
class EventType:
    """A validated event type.

    Event types follow the same validation rules as event IDs:
    - Non-blank (after trimming whitespace)
    - Less than 256 characters
    - No safe delimiter character
    """

    value: str = attrs.field()

    @value.validator
    def _validate_value(self, attribute: attrs.Attribute[str], value: str) -> None:
        if not _is_non_blank_lt_256_no_delimiter(value):
            raise InvalidEventType(value)

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        # Truncate long values like Rust does
        truncated = self.value[:16] + "..." if len(self.value) > 16 else self.value
        return f"EventType({truncated!r})"


# =============================================================================
# EventSubject
# =============================================================================


@attrs.frozen(order=True)
class EventSubject:
    """A validated event subject.

    Event subjects follow the same validation rules as event IDs:
    - Non-blank (after trimming whitespace)
    - Less than 256 characters
    - No safe delimiter character
    """

    value: str = attrs.field()

    @value.validator
    def _validate_value(self, attribute: attrs.Attribute[str], value: str) -> None:
        if not _is_non_blank_lt_256_no_delimiter(value):
            raise InvalidEventSubject(value)

    @classmethod
    def from_optional(cls, value: str | None) -> Self | None:
        """Create an optional EventSubject from an optional value.

        Args:
            value: Optional string value

        Returns:
            EventSubject if value is not None, else None

        Raises:
            InvalidEventSubject: If value is provided but invalid
        """
        if value is None:
            return None
        return cls(value)

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        # Truncate long values like Rust does
        truncated = self.value[:8] + "..." if len(self.value) > 8 else self.value
        return f"EventSubject({truncated!r})"


# =============================================================================
# StateViewName
# =============================================================================


@attrs.frozen(order=True)
class StateViewName:
    """A validated state view name.

    State view names follow the same validation rules as database names.
    """

    value: str = attrs.field()

    @value.validator
    def _validate_value(self, attribute: attrs.Attribute[str], value: str) -> None:
        if not _is_valid_name(value):
            raise InvalidStateViewName(value)

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        # Truncate long values like Rust does
        truncated = self.value[:16] + "..." if len(self.value) > 16 else self.value
        return f"StateViewName({truncated!r})"


# =============================================================================
# StateChangeName
# =============================================================================


@attrs.frozen(order=True)
class StateChangeName:
    """A validated state change name.

    State change names follow the same validation rules as database names.
    """

    value: str = attrs.field()

    @value.validator
    def _validate_value(self, attribute: attrs.Attribute[str], value: str) -> None:
        if not _is_valid_name(value):
            raise InvalidStateChangeName(value)

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        # Truncate long values like Rust does
        truncated = self.value[:16] + "..." if len(self.value) > 16 else self.value
        return f"StateChangeName({truncated!r})"
