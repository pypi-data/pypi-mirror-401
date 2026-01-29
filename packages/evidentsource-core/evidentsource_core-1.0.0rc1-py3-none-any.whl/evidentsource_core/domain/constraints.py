"""Append conditions for transactional consistency (DCB specification).

This module provides types for expressing append conditions on transactions,
ensuring optimistic concurrency control following the Dynamic Consistency
Boundary (DCB) specification.

See: https://dcb.events/specification/
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from evidentsource_core.domain.errors import ConstraintConflict, IncompatibleSelectors
from evidentsource_core.domain.revision import Range, Revision

if TYPE_CHECKING:
    from evidentsource_core.domain.selectors import EventSelector

# =============================================================================
# AppendCondition Types (DCB spec: "Append Condition")
# =============================================================================


@attrs.frozen
class MinConstraint:
    """Events matching selector must have revision >= min."""

    selector: EventSelector
    revision: Revision

    def get_selector(self) -> EventSelector:
        """Get the selector for this constraint."""
        return self.selector

    def min_revision(self) -> int | None:
        """Get the minimum revision bound."""
        return self.revision

    def max_revision(self) -> int | None:
        """Get the maximum revision bound."""
        return None


@attrs.frozen
class MaxConstraint:
    """Events matching selector must have revision <= max."""

    selector: EventSelector
    revision: Revision

    def get_selector(self) -> EventSelector:
        """Get the selector for this constraint."""
        return self.selector

    def min_revision(self) -> int | None:
        """Get the minimum revision bound."""
        return None

    def max_revision(self) -> int | None:
        """Get the maximum revision bound."""
        return self.revision


@attrs.frozen
class RangeConstraint:
    """Events matching selector must have revision within range."""

    selector: EventSelector
    range: Range

    def get_selector(self) -> EventSelector:
        """Get the selector for this constraint."""
        return self.selector

    def min_revision(self) -> int | None:
        """Get the minimum revision bound."""
        return self.range.min

    def max_revision(self) -> int | None:
        """Get the maximum revision bound."""
        return self.range.max


AppendCondition = MinConstraint | MaxConstraint | RangeConstraint
"""An append condition for optimistic concurrency control (DCB spec)."""


# =============================================================================
# Constraint Factory
# =============================================================================


class Constraint:
    """Factory for creating batch constraints.

    Constraints ensure that events matching a selector have revision numbers
    within specified bounds at the time of transaction.

    Example:
        # Ensure no events exist with this subject
        constraint = Constraint.must_not_exist(Selector.subject("order-123"))

        # Ensure events exist
        constraint = Constraint.must_exist(Selector.stream("accounts"))

        # Optimistic concurrency control
        constraint = Constraint.unchanged_since(selector, last_seen_revision=42)
    """

    @staticmethod
    def min(selector: EventSelector, revision: int) -> MinConstraint:
        """Create a MIN constraint (events must have revision >= min).

        Use this when you want to ensure events exist (min=1) or have been
        updated to at least a certain revision.
        """
        return MinConstraint(selector, revision)

    @staticmethod
    def max(selector: EventSelector, revision: int) -> MaxConstraint:
        """Create a MAX constraint (events must have revision <= max).

        Use this when you want to ensure events don't exist yet (max=0) or
        haven't changed beyond a known revision (optimistic concurrency).
        """
        return MaxConstraint(selector, revision)

    @staticmethod
    def range(selector: EventSelector, range_val: Range) -> RangeConstraint:
        """Create a RANGE constraint (events must have revision within range)."""
        return RangeConstraint(selector, range_val)

    @staticmethod
    def must_not_exist(selector: EventSelector) -> MaxConstraint:
        """Require that no events matching the selector exist.

        This is a semantic alias for `max(selector, 0)`. Use this when creating
        new entities to ensure uniqueness.
        """
        return MaxConstraint(selector, 0)

    @staticmethod
    def must_exist(selector: EventSelector) -> MinConstraint:
        """Require that at least one event matching the selector exists.

        This is a semantic alias for `min(selector, 1)`. Use this when updating
        existing entities to ensure they exist.
        """
        return MinConstraint(selector, 1)

    @staticmethod
    def at_revision(selector: EventSelector, revision: int) -> RangeConstraint:
        """Require events matching the selector to be exactly at a specific revision.

        Use this for strict revision checks where you need to ensure the exact
        state hasn't changed.
        """
        return RangeConstraint(selector, Range.new(revision, revision))

    @staticmethod
    def unchanged_since(selector: EventSelector, last_seen_revision: int) -> MaxConstraint:
        """Require events matching the selector haven't changed since a known revision.

        This is a semantic alias for `max(selector, revision)`. Use this for
        optimistic concurrency control where you want to ensure no updates
        have occurred since you last read the data.
        """
        return MaxConstraint(selector, last_seen_revision)


# =============================================================================
# Constraint Combination
# =============================================================================


def combine_constraints(left: AppendCondition, right: AppendCondition) -> AppendCondition:
    """Combine two constraints into one.

    Both constraints must have the same selector. The resulting constraint
    is the union of the bounds (widest range that satisfies both).

    Args:
        left: First constraint
        right: Second constraint

    Returns:
        Combined constraint

    Raises:
        IncompatibleSelectors: If the constraints have different selectors
        ConstraintConflict: If the combined bounds are invalid (e.g., min > max)
    """
    left_selector = left.get_selector()
    right_selector = right.get_selector()

    if left_selector != right_selector:
        raise IncompatibleSelectors()

    selector = left_selector

    # Min + Min -> take the smaller min (widens the range)
    if isinstance(left, MinConstraint) and isinstance(right, MinConstraint):
        return MinConstraint(selector, min(left.revision, right.revision))

    # Max + Max -> take the larger max (widens the range)
    if isinstance(left, MaxConstraint) and isinstance(right, MaxConstraint):
        return MaxConstraint(selector, max(left.revision, right.revision))

    # Min + Max -> create range
    if isinstance(left, MinConstraint) and isinstance(right, MaxConstraint):
        min_val, max_val = left.revision, right.revision
        if min_val > max_val:
            raise ConstraintConflict(repr(left), repr(right))
        return RangeConstraint(selector, Range.new(min_val, max_val))

    if isinstance(left, MaxConstraint) and isinstance(right, MinConstraint):
        min_val, max_val = right.revision, left.revision
        if min_val > max_val:
            raise ConstraintConflict(repr(left), repr(right))
        return RangeConstraint(selector, Range.new(min_val, max_val))

    # Range + Min -> extend range min
    if isinstance(left, RangeConstraint) and isinstance(right, MinConstraint):
        new_min = min(left.range.min, right.revision)
        return RangeConstraint(selector, Range.new(new_min, left.range.max))

    if isinstance(left, MinConstraint) and isinstance(right, RangeConstraint):
        new_min = min(right.range.min, left.revision)
        return RangeConstraint(selector, Range.new(new_min, right.range.max))

    # Range + Max -> extend range max
    if isinstance(left, RangeConstraint) and isinstance(right, MaxConstraint):
        new_max = max(left.range.max, right.revision)
        return RangeConstraint(selector, Range.new(left.range.min, new_max))

    if isinstance(left, MaxConstraint) and isinstance(right, RangeConstraint):
        new_max = max(right.range.max, left.revision)
        return RangeConstraint(selector, Range.new(right.range.min, new_max))

    # Range + Range -> union of ranges
    if isinstance(left, RangeConstraint) and isinstance(right, RangeConstraint):
        new_min = min(left.range.min, right.range.min)
        new_max = max(left.range.max, right.range.max)
        return RangeConstraint(selector, Range.new(new_min, new_max))

    raise TypeError(f"Unknown constraint types: {type(left)}, {type(right)}")
