"""Protocol definitions for EvidentSource database operations.

This module defines the abstract interfaces (protocols) that database
implementations must provide. These are the Python equivalents of Rust traits.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from collections.abc import AsyncIterator
    from datetime import datetime

    from evidentsource_core.domain import (
        AppendCondition,
        DatabaseName,
        Event,
        EventAttribute,
        EventSelector,
        ProspectiveEvent,
        QueryOptions,
        Revision,
        StateChangeName,
        StateView,
        StateViewName,
        Transaction,
        TransactionSummary,
    )


# Type aliases
StateViewVersion = int
StateChangeVersion = int


# =============================================================================
# DatabaseIdentity
# =============================================================================


@runtime_checkable
class DatabaseIdentity(Protocol):
    """Basic database identity information."""

    @property
    @abstractmethod
    def name(self) -> DatabaseName:
        """Get the database name."""
        ...

    @property
    @abstractmethod
    def created_at(self) -> datetime:
        """Get the timestamp when this database was created."""
        ...


# =============================================================================
# DatabaseCatalog
# =============================================================================


@runtime_checkable
class DatabaseCatalog(Protocol):
    """Catalog of available databases."""

    @abstractmethod
    def list_databases(self) -> AsyncIterator[DatabaseName]:
        """List all databases in the catalog."""
        ...

    @abstractmethod
    async def create_database(self, name: DatabaseName) -> DatabaseIdentity:
        """Create a new database with the given name.

        Raises:
            DatabaseError: If creation fails (e.g., already exists)
        """
        ...

    @abstractmethod
    async def delete_database(self, name: DatabaseName) -> None:
        """Delete a database by name.

        Raises:
            DatabaseError: If deletion fails (e.g., not found)
        """
        ...


# =============================================================================
# DatabaseProvider
# =============================================================================


@runtime_checkable
class DatabaseProvider(DatabaseIdentity, Protocol):
    """Provides access to database views at various revisions."""

    @abstractmethod
    def local_database(self) -> DatabaseAtRevision:
        """Get the latest local database (may be stale)."""
        ...

    @abstractmethod
    async def latest_database(self) -> DatabaseAtRevision:
        """Get the latest revision on the server committed to storage.

        Raises:
            DatabaseError: If the operation fails
        """
        ...

    @abstractmethod
    async def database_at_revision(self, revision: Revision) -> DatabaseAtRevision:
        """Get the database at a specific revision, awaiting if necessary.

        Raises:
            DatabaseError: If the operation fails
        """
        ...

    @abstractmethod
    async def database_at_timestamp(self, revision_timestamp: datetime) -> DatabaseAtRevision:
        """Get the database at the revision effective at a specific timestamp.

        Raises:
            DatabaseError: If the operation fails
        """
        ...


# =============================================================================
# DatabaseConnection
# =============================================================================


@runtime_checkable
class DatabaseConnection(DatabaseProvider, Protocol):
    """A database connection capable of performing transactions."""

    @abstractmethod
    async def transact(
        self,
        events: list[ProspectiveEvent],
        constraints: list[AppendCondition] | None = None,
    ) -> DatabaseAtRevision:
        """Transact events with constraints.

        The transaction must contain at least one event. Constraints are checked
        against the current database state before committing.

        Args:
            events: Non-empty list of events to transact
            constraints: Optional list of constraints to check

        Returns:
            Database view at the new revision

        Raises:
            DatabaseError: If the transaction fails
        """
        ...

    @abstractmethod
    async def transact_with_id(
        self,
        transaction_id: str,
        events: list[ProspectiveEvent],
        constraints: list[AppendCondition] | None = None,
    ) -> DatabaseAtRevision:
        """Transact events with a custom transaction ID.

        This is useful for idempotency - if a transaction with the same ID has
        already been committed, the existing result is returned.

        Args:
            transaction_id: Unique identifier for the transaction
            events: Non-empty list of events to transact
            constraints: Optional list of constraints to check

        Returns:
            Database view at the new revision

        Raises:
            DatabaseError: If the transaction fails
        """
        ...

    @abstractmethod
    async def execute_state_change(
        self,
        name: StateChangeName,
        version: StateChangeVersion,
        request: object,  # CommandRequest
    ) -> DatabaseAtRevision:
        """Execute a state change.

        This invokes the named state change component with the given request
        and commits any resulting events.

        Raises:
            StateChangeError: If execution fails
        """
        ...

    @abstractmethod
    def log(self) -> AsyncIterator[TransactionSummary]:
        """Get the transaction log (summary only)."""
        ...

    @abstractmethod
    def log_detail(self) -> AsyncIterator[Transaction]:
        """Get the transaction log with full event details."""
        ...

    @abstractmethod
    def log_from(self, from_revision: Revision) -> AsyncIterator[TransactionSummary]:
        """Get the transaction log starting from a specific revision.

        This returns transaction summaries for all transactions committed at or
        after the specified revision.
        """
        ...

    @abstractmethod
    def log_detail_from(self, from_revision: Revision) -> AsyncIterator[Transaction]:
        """Get the transaction log with full event details, starting from a specific revision.

        This returns full transaction details (including events) for all transactions
        committed at or after the specified revision.
        """
        ...


# =============================================================================
# DatabaseAtRevision
# =============================================================================


@runtime_checkable
class DatabaseAtRevision(DatabaseIdentity, Protocol):
    """A database view at a specific revision."""

    @property
    @abstractmethod
    def revision(self) -> Revision:
        """Get this view's revision number."""
        ...

    @property
    @abstractmethod
    def revision_timestamp(self) -> datetime:
        """Get the timestamp when this revision was committed."""
        ...

    @abstractmethod
    def at_effective_timestamp(
        self, effective_timestamp: datetime
    ) -> DatabaseAtRevisionAndEffectiveTimestamp:
        """Get a view scoped to a specific effective timestamp (for bi-temporal queries)."""
        ...

    @abstractmethod
    async def at_revision(self, revision: Revision) -> DatabaseAtRevision:
        """Get a view at a different revision.

        This allows navigating to an earlier or later revision of the database.
        """
        ...

    @abstractmethod
    def speculate_with_transaction(self, events: list[ProspectiveEvent]) -> SpeculativeDatabase:
        """Create a speculative view with additional uncommitted events.

        Args:
            events: Non-empty list of events to speculate with
        """
        ...

    @abstractmethod
    def query_events(self, selector: EventSelector) -> AsyncIterator[Event]:
        """Query events matching a selector."""
        ...

    @abstractmethod
    def query_events_with_options(
        self, selector: EventSelector, options: QueryOptions
    ) -> AsyncIterator[Event]:
        """Query events matching a selector with options.

        This allows controlling the query direction and limiting results.
        """
        ...

    @abstractmethod
    async def view_state(self, name: StateViewName, version: StateViewVersion) -> StateView:
        """Fetch a state view.

        Raises:
            StateViewError: If the state view cannot be fetched
        """
        ...

    @abstractmethod
    async def view_state_with_params(
        self,
        name: StateViewName,
        version: StateViewVersion,
        params: list[tuple[str, EventAttribute]],
    ) -> StateView:
        """Fetch a state view with parameter bindings.

        Parameters are used to filter state views by specific attributes.
        Common parameter patterns (gRPC API - use just the parameter name):
        - ("account_id", SubjectAttribute(...)) - filter by subject
        - ("processing_day_stream", StreamAttribute(...)) - filter by stream

        Note: The HTTP REST API uses a different format with prefixes
        (e.g., ?subject.account_id=...)

        Raises:
            StateViewError: If the state view cannot be fetched
        """
        ...


# =============================================================================
# DatabaseAtRevisionAndEffectiveTimestamp
# =============================================================================


@runtime_checkable
class DatabaseAtRevisionAndEffectiveTimestamp(DatabaseAtRevision, Protocol):
    """A database view at both a revision and effective timestamp.

    This enables bi-temporal queries where you want to see the database
    state as it was understood at a particular point in effective time.
    """

    @property
    @abstractmethod
    def basis(self) -> DatabaseAtRevision:
        """Get the base database view (without effective timestamp scope)."""
        ...

    @property
    @abstractmethod
    def effective_timestamp(self) -> datetime:
        """Get the effective timestamp this view is scoped to."""
        ...

    @abstractmethod
    async def at_revision_with_effective_timestamp(
        self, revision: Revision
    ) -> DatabaseAtRevisionAndEffectiveTimestamp:
        """Get a view at a different revision while keeping the same effective timestamp.

        This is an async operation because fetching a different revision may require
        a remote call (e.g., gRPC) to retrieve the database state at that revision.

        Raises:
            DatabaseError: If the operation fails
        """
        ...


# =============================================================================
# SpeculativeDatabase
# =============================================================================


@runtime_checkable
class SpeculativeDatabase(DatabaseAtRevision, Protocol):
    """A speculative database view with uncommitted events.

    This allows querying the database as if certain events had been committed,
    useful for validation and preview scenarios.
    """

    @property
    @abstractmethod
    def basis(self) -> DatabaseAtRevision:
        """Get the committed view this speculation is based on."""
        ...

    @property
    @abstractmethod
    def speculated_transactions(self) -> list[list[ProspectiveEvent]]:
        """Get the transactions of speculated (uncommitted) events."""
        ...

    @property
    @abstractmethod
    def speculated_event_count(self) -> int:
        """Get the total count of speculated events."""
        ...
