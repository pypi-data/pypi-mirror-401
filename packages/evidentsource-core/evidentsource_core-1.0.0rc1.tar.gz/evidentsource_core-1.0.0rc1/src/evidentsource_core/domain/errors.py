"""Error types for the EvidentSource domain.

This module provides a hierarchical error structure that groups errors
by domain concept while enabling seamless error propagation.
"""

from __future__ import annotations

import attrs


class EvidentSourceError(Exception):
    """Base class for all EvidentSource errors."""

    pass


# =============================================================================
# Identifier Errors
# =============================================================================


class IdentifierError(EvidentSourceError):
    """Errors related to identifier validation (names, IDs, etc.)."""

    pass


class InvalidDatabaseName(IdentifierError):
    """Invalid database name."""

    def __init__(self, value: str) -> None:
        self.value = value
        super().__init__(f"invalid database name '{value}'")


class InvalidStreamName(IdentifierError):
    """Invalid stream name."""

    def __init__(self, value: str | None) -> None:
        self.value = value
        super().__init__(f"invalid stream name: {value!r}")


class InvalidEventId(IdentifierError):
    """Invalid event ID."""

    def __init__(self, value: str) -> None:
        self.value = value
        super().__init__(f"invalid event id: {value}")


class InvalidEventType(IdentifierError):
    """Invalid event type."""

    def __init__(self, value: str | None) -> None:
        self.value = value
        super().__init__(f"invalid event type: {value!r}")


class InvalidEventSubject(IdentifierError):
    """Invalid event subject."""

    def __init__(self, value: str) -> None:
        self.value = value
        super().__init__(f"invalid event subject: {value}")


class InvalidStateViewName(IdentifierError):
    """Invalid state view name."""

    def __init__(self, value: str) -> None:
        self.value = value
        super().__init__(f"invalid state view name '{value}'")


class InvalidStateChangeName(IdentifierError):
    """Invalid state change name."""

    def __init__(self, value: str) -> None:
        self.value = value
        super().__init__(f"invalid state change name '{value}'")


# =============================================================================
# Constraint Errors
# =============================================================================


class ConstraintError(EvidentSourceError):
    """Errors related to constraint operations."""

    pass


class BlankConstraint(ConstraintError):
    """Blank constraint error."""

    def __init__(self) -> None:
        super().__init__("blank constraint")


class InvalidRange(ConstraintError):
    """Invalid range where min > max."""

    def __init__(self, min_val: int, max_val: int) -> None:
        self.min = min_val
        self.max = max_val
        super().__init__(f"invalid range: min ({min_val}) must be <= max ({max_val})")


class ConstraintConflict(ConstraintError):
    """Constraint conflict error."""

    def __init__(self, left: str, right: str) -> None:
        self.left = left
        self.right = right
        super().__init__(f"constraint conflict: {left} vs {right}")


class IncompatibleSelectors(ConstraintError):
    """Cannot combine constraints with different selectors."""

    def __init__(self) -> None:
        super().__init__("cannot combine constraints with different selectors")


# =============================================================================
# Event Errors
# =============================================================================


class EventError(EvidentSourceError):
    """Errors related to event validation."""

    pass


class InvalidEventSource(EventError):
    """Invalid event source."""

    def __init__(self, value: str) -> None:
        self.value = value
        super().__init__(f"invalid event source: {value}")


class DuplicateEventId(EventError):
    """Duplicate event ID in stream."""

    def __init__(self, stream: str, event_id: str) -> None:
        self.stream = stream
        self.event_id = event_id
        super().__init__(f"duplicate event id: {stream}/{event_id}")


# =============================================================================
# Transaction Errors
# =============================================================================


class TransactionError(EvidentSourceError):
    """Errors related to transaction operations."""

    pass


class EmptyTransaction(TransactionError):
    """Transaction must contain at least one event."""

    def __init__(self) -> None:
        super().__init__("transaction must contain at least one event")


class InvalidTransactionId(TransactionError):
    """Invalid transaction ID."""

    def __init__(self, value: str) -> None:
        self.value = value
        super().__init__(f"invalid transaction ID: {value}")


class TransactionTooLarge(TransactionError):
    """Transaction too large."""

    def __init__(self, actual: int, max_size: int) -> None:
        self.actual = actual
        self.max = max_size
        super().__init__(f"transaction too large: {actual} events, max {max_size}")


class DuplicateTransactionId(TransactionError):
    """Duplicate transaction ID."""

    def __init__(self, value: str) -> None:
        self.value = value
        super().__init__(f"duplicate transaction id: {value}")


class InvalidEvents(TransactionError):
    """Transaction contains invalid events."""

    def __init__(self, errors: list[EventError]) -> None:
        self.errors = errors
        super().__init__(f"transaction contains {len(errors)} invalid events")


class InvalidConstraints(TransactionError):
    """Transaction has invalid constraints."""

    def __init__(self, errors: list[ConstraintError]) -> None:
        self.errors = errors
        super().__init__(f"transaction has {len(errors)} invalid constraints")


class ConstraintViolations(TransactionError):
    """Transaction has constraint violations."""

    def __init__(self, violations: list[str]) -> None:
        self.violations = violations
        super().__init__(f"transaction has {len(violations)} constraint violations")


# =============================================================================
# Operation Context
# =============================================================================


@attrs.frozen
class OperationContext:
    """Context for enriching errors with operation details.

    This provides additional context about what operation was being performed
    when an error occurred.
    """

    operation: str
    database: str
    details: str | None = None

    def with_details(self, details: str) -> OperationContext:
        """Add details to the context."""
        return attrs.evolve(self, details=details)

    def __str__(self) -> str:
        base = f"{self.operation}(db={self.database})"
        if self.details:
            base += f" [{self.details}]"
        return base


# =============================================================================
# Database Errors
# =============================================================================


class DatabaseError(EvidentSourceError):
    """Errors related to database operations."""

    pass


class DatabaseNotFound(DatabaseError):
    """Database not found."""

    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"database '{name}' not found")


class DatabaseAlreadyExists(DatabaseError):
    """Database already exists."""

    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"database '{name}' already exists")


class ConcurrentWriteCollision(DatabaseError):
    """Concurrent write collision."""

    def __init__(self) -> None:
        super().__init__("concurrent write collision")


class DatabaseTimeout(DatabaseError):
    """Operation timed out."""

    def __init__(self) -> None:
        super().__init__("operation timed out")


class DatabaseServerError(DatabaseError):
    """Server error."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(f"server error: {message}")


class DatabaseErrorWithContext(DatabaseError):
    """Database error with operation context."""

    def __init__(self, context: OperationContext, source: DatabaseError) -> None:
        self.context = context
        self.source = source
        super().__init__(f"{context}: {source}")

    def inner(self) -> DatabaseError:
        """Get the inner error, stripping any context wrappers."""
        if isinstance(self.source, DatabaseErrorWithContext):
            return self.source.inner()
        return self.source


# =============================================================================
# State View Errors
# =============================================================================


class StateViewError(EvidentSourceError):
    """Errors related to state view operations."""

    pass


class StateViewNotFound(StateViewError):
    """State view not found."""

    def __init__(self, name: str, version: int) -> None:
        self.name = name
        self.version = version
        super().__init__(f"state view {name}.v{version} not found")


class StateViewEvolveError(StateViewError):
    """Error evolving state view."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(f"error evolving state view: {message}")


class StateViewServerError(StateViewError):
    """Server error in state view operation."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(f"server error: {message}")


# =============================================================================
# State Change Errors
# =============================================================================


class StateChangeError(EvidentSourceError):
    """Errors related to state change operations."""

    pass


class StateChangeNotFound(StateChangeError):
    """State change not found."""

    def __init__(self, name: str, version: int) -> None:
        self.name = name
        self.version = version
        super().__init__(f"state change {name}.v{version} not found")


class StateChangeExecutionError(StateChangeError):
    """Execution error in state change."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(f"execution error: {message}")


class StateChangeServerError(StateChangeError):
    """Server error in state change operation."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(f"server error: {message}")


class StateChangeValidationError(StateChangeError):
    """Validation error in state change."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(f"validation error: {message}")
