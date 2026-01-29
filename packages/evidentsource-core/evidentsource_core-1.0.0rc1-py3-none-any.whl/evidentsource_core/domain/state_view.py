"""State view types.

State views are materialized views computed from events. They provide
queryable state derived from the event log.

StateViewCodec:
    The StateViewCodec protocol allows state view types to define their own
    serialization format. The SDK calls from_bytes() once at the start to
    deserialize the previous state, runs evolve() for each event, then calls
    to_bytes() once at the end.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol, Self

import attrs

if TYPE_CHECKING:
    from datetime import datetime

    from evidentsource_core.domain.identifiers import DatabaseName, StateViewName
    from evidentsource_core.domain.revision import Revision
    from evidentsource_core.domain.selectors import EventSelector

# Type alias for state view version
StateViewVersion = int
"""State view version number."""


@attrs.define
class StateView:
    """A materialized state view.

    Attributes:
        database: The database this state view belongs to.
        name: The name of this state view.
        version: The version of this state view definition.
        event_selector: The event selector that determines which events affect this view.
        last_modified_revision: The revision at which this view was last modified, if any.
        last_modified_timestamp: The timestamp when this view was last modified, if any.
        content_type: The content type of the serialized state (e.g., "application/json").
        content_schema_url: Optional URL to the schema for the content.
        content: The serialized state content, if any.
    """

    database: DatabaseName
    name: StateViewName
    version: StateViewVersion
    event_selector: EventSelector
    last_modified_revision: Revision | None = None
    last_modified_timestamp: datetime | None = None
    content_type: str = "application/json"
    content_schema_url: str | None = None
    content: bytes | None = None

    def has_content(self) -> bool:
        """Check if this state view has content."""
        return self.content is not None

    def content_bytes(self) -> bytes | None:
        """Get the content as bytes, if present."""
        return self.content


class StateViewCodec(Protocol):
    """Protocol for state view types that can serialize/deserialize to bytes.

    The SDK calls from_bytes() once at the start to deserialize the previous state,
    runs evolve() for each event, then calls to_bytes() once at the end.

    Example:
        class AccountSummary:
            balance: int = 0
            transaction_count: int = 0

            @classmethod
            def from_bytes(
                cls,
                data: bytes | None,
                content_type: str | None,
                content_schema: str | None,
            ) -> Self:
                if data is None or len(data) == 0:
                    return cls()
                import json
                parsed = json.loads(data)
                return cls(
                    balance=parsed.get("balance", 0),
                    transaction_count=parsed.get("transaction_count", 0),
                )

            def to_bytes(
                self,
                content_type: str | None,
                content_schema: str | None,
            ) -> bytes | None:
                import json
                return json.dumps({
                    "balance": self.balance,
                    "transaction_count": self.transaction_count,
                }).encode()
    """

    @classmethod
    @abstractmethod
    def from_bytes(
        cls,
        data: bytes | None,
        content_type: str | None,
        content_schema: str | None,
    ) -> Self:
        """Deserialize state from bytes.

        Called once per state view invocation with the previous state.
        Returns Default state if data is None or empty.

        Args:
            data: The serialized state bytes, if any
            content_type: The content type (e.g., "application/json")
            content_schema: Optional schema URL for the content
        """
        ...

    @abstractmethod
    def to_bytes(
        self,
        content_type: str | None,
        content_schema: str | None,
    ) -> bytes | None:
        """Serialize state to bytes.

        Called once after all events have been processed.
        Returns None if state should not be persisted.

        Args:
            content_type: The content type (e.g., "application/json")
            content_schema: Optional schema URL for the content
        """
        ...
