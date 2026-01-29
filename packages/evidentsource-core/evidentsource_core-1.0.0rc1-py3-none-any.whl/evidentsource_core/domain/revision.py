"""Revision types for database versioning.

This module defines the Revision type alias and the Range type for
constraining revisions in batch operations.
"""

from __future__ import annotations

import attrs

from evidentsource_core.domain.errors import InvalidRange

# Type alias for revision numbers
Revision = int
"""A database revision number."""


@attrs.frozen
class Range:
    """A range of revisions (inclusive on both ends)."""

    _min: int = attrs.field(alias="min")
    _max: int = attrs.field(alias="max")

    def __attrs_post_init__(self) -> None:
        """Validate that min <= max."""
        if self._min > self._max:
            raise InvalidRange(self._min, self._max)

    @classmethod
    def new(cls, min_val: int, max_val: int) -> Range:
        """Create a new Range if min <= max.

        Args:
            min_val: Minimum revision (inclusive)
            max_val: Maximum revision (inclusive)

        Returns:
            A new Range

        Raises:
            InvalidRange: If min > max
        """
        return cls(min=min_val, max=max_val)

    def contains(self, r: int) -> bool:
        """Check if a revision is contained within this range."""
        return self._min <= r <= self._max

    @property
    def min(self) -> int:
        """Get the minimum revision."""
        return self._min

    @property
    def max(self) -> int:
        """Get the maximum revision."""
        return self._max
