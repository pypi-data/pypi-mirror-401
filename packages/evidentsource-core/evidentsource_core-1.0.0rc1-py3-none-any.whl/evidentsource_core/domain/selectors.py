"""Event selectors for querying events.

This module provides types for building event queries based on
event attributes like stream, subject, and event type.

Selectors support operator overloading for composition:
    selector = EventSelector.stream("orders") & EventSelector.event_type("OrderPlaced")
    selector = EventSelector.subject("user-1") | EventSelector.subject("user-2")
"""

from __future__ import annotations

from enum import Enum, auto
from typing import TYPE_CHECKING, Self

import attrs

from evidentsource_core.domain.identifiers import (
    EventSubject,
    EventType,
    StreamName,
)

if TYPE_CHECKING:
    from evidentsource_core.domain.events import Event, ProspectiveEvent


# =============================================================================
# EventAttribute
# =============================================================================


@attrs.frozen
class StreamAttribute:
    """Match events in a specific stream."""

    stream: StreamName


@attrs.frozen
class SubjectAttribute:
    """Match events with a specific subject (or no subject if None)."""

    subject: EventSubject | None


@attrs.frozen
class EventTypeAttribute:
    """Match events of a specific type."""

    event_type: EventType


EventAttribute = StreamAttribute | SubjectAttribute | EventTypeAttribute
"""An event attribute for exact matching."""


# =============================================================================
# EventAttributePrefix
# =============================================================================


@attrs.frozen
class StreamPrefix:
    """Match streams starting with prefix."""

    stream: StreamName


@attrs.frozen
class SubjectPrefix:
    """Match subjects starting with prefix."""

    subject: EventSubject


@attrs.frozen
class EventTypePrefix:
    """Match event types starting with prefix."""

    event_type: EventType


EventAttributePrefix = StreamPrefix | SubjectPrefix | EventTypePrefix
"""An event attribute prefix for starts-with matching."""


# =============================================================================
# EventSelector
# =============================================================================


@attrs.frozen
class EqualsSelector:
    """Match events where an attribute equals a value."""

    attribute: EventAttribute

    def __and__(self, other: EventSelector) -> AndSelector:
        return AndSelector(left=self, right=other)

    def __or__(self, other: EventSelector) -> OrSelector:
        return OrSelector(left=self, right=other)

    def matches_prospective(self, event: ProspectiveEvent) -> bool:
        """Check if a prospective event matches this selector."""
        attr = self.attribute
        if isinstance(attr, StreamAttribute):
            return event.stream == str(attr.stream)
        elif isinstance(attr, SubjectAttribute):
            if attr.subject is None:
                return event.subject is None
            return event.subject == str(attr.subject)
        elif isinstance(attr, EventTypeAttribute):
            return event.event_type == str(attr.event_type)
        return False

    def matches(self, event: Event) -> bool:
        """Check if a stored event matches this selector."""
        attr = self.attribute
        if isinstance(attr, StreamAttribute):
            stream = event.stream()
            return stream is not None and stream == str(attr.stream)
        elif isinstance(attr, SubjectAttribute):
            if attr.subject is None:
                return event.subject is None
            return event.subject == str(attr.subject)
        elif isinstance(attr, EventTypeAttribute):
            return event.event_type == str(attr.event_type)
        return False

    def flatten(self) -> list[FlatSelectorNode]:
        """Flatten this selector into an index-based representation."""
        return [FlatEqualsNode(self.attribute)]


@attrs.frozen
class StartsWithSelector:
    """Match events where an attribute starts with a prefix."""

    prefix: EventAttributePrefix

    def __and__(self, other: EventSelector) -> AndSelector:
        return AndSelector(left=self, right=other)

    def __or__(self, other: EventSelector) -> OrSelector:
        return OrSelector(left=self, right=other)

    def matches_prospective(self, event: ProspectiveEvent) -> bool:
        """Check if a prospective event matches this selector."""
        prefix = self.prefix
        if isinstance(prefix, StreamPrefix):
            return event.stream.startswith(str(prefix.stream))
        elif isinstance(prefix, SubjectPrefix):
            if event.subject is None:
                return False
            return event.subject.startswith(str(prefix.subject))
        elif isinstance(prefix, EventTypePrefix):
            return event.event_type.startswith(str(prefix.event_type))
        return False

    def matches(self, event: Event) -> bool:
        """Check if a stored event matches this selector."""
        prefix = self.prefix
        if isinstance(prefix, StreamPrefix):
            stream = event.stream()
            return stream is not None and stream.startswith(str(prefix.stream))
        elif isinstance(prefix, SubjectPrefix):
            if event.subject is None:
                return False
            return event.subject.startswith(str(prefix.subject))
        elif isinstance(prefix, EventTypePrefix):
            return event.event_type.startswith(str(prefix.event_type))
        return False

    def flatten(self) -> list[FlatSelectorNode]:
        """Flatten this selector into an index-based representation."""
        return [FlatStartsWithNode(self.prefix)]


@attrs.frozen
class AndSelector:
    """Match events matching both selectors."""

    left: EventSelector
    right: EventSelector

    def __and__(self, other: EventSelector) -> AndSelector:
        return AndSelector(left=self, right=other)

    def __or__(self, other: EventSelector) -> OrSelector:
        return OrSelector(left=self, right=other)

    def matches_prospective(self, event: ProspectiveEvent) -> bool:
        """Check if a prospective event matches this selector."""
        return self.left.matches_prospective(event) and self.right.matches_prospective(event)

    def matches(self, event: Event) -> bool:
        """Check if a stored event matches this selector."""
        return self.left.matches(event) and self.right.matches(event)

    def flatten(self) -> list[FlatSelectorNode]:
        """Flatten this selector into an index-based representation."""
        nodes: list[FlatSelectorNode] = []
        left_idx = _flatten_into(self.left, nodes)
        right_idx = _flatten_into(self.right, nodes)
        nodes.append(FlatAndNode(left_idx, right_idx))
        return nodes


@attrs.frozen
class OrSelector:
    """Match events matching either selector."""

    left: EventSelector
    right: EventSelector

    def __and__(self, other: EventSelector) -> AndSelector:
        return AndSelector(left=self, right=other)

    def __or__(self, other: EventSelector) -> OrSelector:
        return OrSelector(left=self, right=other)

    def matches_prospective(self, event: ProspectiveEvent) -> bool:
        """Check if a prospective event matches this selector."""
        return self.left.matches_prospective(event) or self.right.matches_prospective(event)

    def matches(self, event: Event) -> bool:
        """Check if a stored event matches this selector."""
        return self.left.matches(event) or self.right.matches(event)

    def flatten(self) -> list[FlatSelectorNode]:
        """Flatten this selector into an index-based representation."""
        nodes: list[FlatSelectorNode] = []
        left_idx = _flatten_into(self.left, nodes)
        right_idx = _flatten_into(self.right, nodes)
        nodes.append(FlatOrNode(left_idx, right_idx))
        return nodes


EventSelector = EqualsSelector | StartsWithSelector | AndSelector | OrSelector
"""A selector for matching events."""


def _flatten_into(selector: EventSelector, nodes: list[FlatSelectorNode]) -> int:
    """Flatten a selector into the nodes list and return its index."""
    if isinstance(selector, EqualsSelector):
        idx = len(nodes)
        nodes.append(FlatEqualsNode(selector.attribute))
        return idx
    elif isinstance(selector, StartsWithSelector):
        idx = len(nodes)
        nodes.append(FlatStartsWithNode(selector.prefix))
        return idx
    elif isinstance(selector, AndSelector):
        left_idx = _flatten_into(selector.left, nodes)
        right_idx = _flatten_into(selector.right, nodes)
        idx = len(nodes)
        nodes.append(FlatAndNode(left_idx, right_idx))
        return idx
    elif isinstance(selector, OrSelector):
        left_idx = _flatten_into(selector.left, nodes)
        right_idx = _flatten_into(selector.right, nodes)
        idx = len(nodes)
        nodes.append(FlatOrNode(left_idx, right_idx))
        return idx
    raise TypeError(f"Unknown selector type: {type(selector)}")


# =============================================================================
# FlatSelectorNode (for WIT transfer)
# =============================================================================


@attrs.frozen
class FlatEqualsNode:
    """Match events where an attribute equals a value."""

    attribute: EventAttribute


@attrs.frozen
class FlatStartsWithNode:
    """Match events where an attribute starts with a prefix."""

    prefix: EventAttributePrefix


@attrs.frozen
class FlatAndNode:
    """Match events matching both selectors (indices into the node list)."""

    left: int
    right: int


@attrs.frozen
class FlatOrNode:
    """Match events matching either selector (indices into the node list)."""

    left: int
    right: int


FlatSelectorNode = FlatEqualsNode | FlatStartsWithNode | FlatAndNode | FlatOrNode
"""Flattened selector node for WIT transfer."""


# =============================================================================
# QueryDirection and QueryOptions
# =============================================================================


class QueryDirection(Enum):
    """Direction for iterating through query results."""

    FORWARD = auto()
    """Iterate from oldest to newest (by revision)."""

    REVERSE = auto()
    """Iterate from newest to oldest (by revision)."""


@attrs.define
class QueryOptions:
    """Options for configuring event queries.

    Use the builder-style methods to configure direction and limits.

    Example:
        # Default options (forward, no limit)
        opts = QueryOptions()

        # Get first 100 events in reverse order
        opts = QueryOptions().reverse().limit(100)
    """

    direction: QueryDirection = QueryDirection.FORWARD
    """Direction for iterating through results."""

    _limit: int | None = attrs.field(default=None, alias="_limit")
    """Maximum number of results to return."""

    def forward(self) -> Self:
        """Set the direction to forward (oldest to newest)."""
        self.direction = QueryDirection.FORWARD
        return self

    def reverse(self) -> Self:
        """Set the direction to reverse (newest to oldest)."""
        self.direction = QueryDirection.REVERSE
        return self

    def limit(self, value: int) -> Self:
        """Set the maximum number of results to return."""
        self._limit = value
        return self

    def get_direction(self) -> QueryDirection:
        """Get the configured direction."""
        return self.direction

    def get_limit(self) -> int | None:
        """Get the configured limit, if any."""
        return self._limit


# =============================================================================
# Factory Functions (for convenient selector construction)
# =============================================================================


class Selector:
    """Factory for creating event selectors.

    Example:
        selector = Selector.stream("orders") & Selector.event_type("OrderPlaced")
        selector = Selector.subject("user-1") | Selector.subject("user-2")
    """

    @staticmethod
    def stream(name: str) -> EqualsSelector:
        """Create a selector matching events in a specific stream."""
        return EqualsSelector(StreamAttribute(StreamName(name)))

    @staticmethod
    def subject(value: str) -> EqualsSelector:
        """Create a selector matching events with a specific subject."""
        return EqualsSelector(SubjectAttribute(EventSubject(value)))

    @staticmethod
    def no_subject() -> EqualsSelector:
        """Create a selector matching events with no subject."""
        return EqualsSelector(SubjectAttribute(None))

    @staticmethod
    def event_type(value: str) -> EqualsSelector:
        """Create a selector matching events of a specific type."""
        return EqualsSelector(EventTypeAttribute(EventType(value)))

    @staticmethod
    def stream_starts_with(prefix: str) -> StartsWithSelector:
        """Create a selector matching streams starting with a prefix."""
        return StartsWithSelector(StreamPrefix(StreamName(prefix)))

    @staticmethod
    def subject_starts_with(prefix: str) -> StartsWithSelector:
        """Create a selector matching subjects starting with a prefix."""
        return StartsWithSelector(SubjectPrefix(EventSubject(prefix)))

    @staticmethod
    def event_type_starts_with(prefix: str) -> StartsWithSelector:
        """Create a selector matching event types starting with a prefix."""
        return StartsWithSelector(EventTypePrefix(EventType(prefix)))


# Alias for more Pythonic API
EventSelector_factory = Selector
