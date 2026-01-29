"""State change types.

State changes are commands that produce events. They encapsulate
business logic for validating and processing requests.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

import attrs

from evidentsource_core.domain.errors import EvidentSourceError

if TYPE_CHECKING:
    from evidentsource_core.domain.identifiers import StateChangeName

# Type alias for state change version
StateChangeVersion = int
"""State change version number."""


@attrs.frozen
class StateChangeDefinitionSummary:
    """A summary of a state change definition.

    This is returned when listing state changes registered with the database.
    """

    name: StateChangeName
    version: StateChangeVersion


class CommandParseError(EvidentSourceError):
    """Error when parsing a command body."""

    pass


class NoBody(CommandParseError):
    """Command body is required but was not provided."""

    def __init__(self) -> None:
        super().__init__("command body is required")


class DeserializationFailed(CommandParseError):
    """Failed to deserialize the command body."""

    def __init__(self, message: str) -> None:
        super().__init__(f"deserialization failed: {message}")
        self.message = message


class CommandRequestError(EvidentSourceError):
    """Error when creating a command request."""

    pass


@attrs.frozen
class TransactionOptions:
    """Optional parameters for transaction and state change operations.

    All fields are optional. Use these to add correlation metadata
    to transactions for distributed tracing and event flow tracking.

    Attributes:
        transaction_id: Unique identifier for idempotent transaction processing.
            If a transaction with this ID was already committed, the existing
            result is returned.
        correlation_id: Groups related events across a business flow.
            See: https://github.com/cloudevents/spec/blob/main/cloudevents/extensions/correlation.md
        causation_id: Tracks direct parent-child event relationships.
            See: https://github.com/cloudevents/spec/blob/main/cloudevents/extensions/correlation.md

    Example:
        # Transaction with correlation metadata
        options = TransactionOptions(
            transaction_id="txn-123",
            correlation_id="order-flow-456",
            causation_id="parent-event-789",
        )
        db = await conn.transact_with_options(events, constraints, options)
    """

    transaction_id: str | None = None
    correlation_id: str | None = None
    causation_id: str | None = None


class SerializationFailed(CommandRequestError):
    """Failed to serialize the request body."""

    def __init__(self, message: str) -> None:
        super().__init__(f"serialization failed: {message}")
        self.message = message


@attrs.define
class Command:
    """A command received by a state change.

    This mirrors the WIT Command type and can be used by domain code
    to implement parsing without depending on the SDK.

    The SDK is format-agnostic: users implement command parsing with their
    preferred deserializer (json, msgpack, etc.).

    Example:
        def parse_command(cmd: Command) -> MyDomainCommand:
            data = cmd.body
            if data is None:
                raise NoBody()
            import json
            try:
                parsed = json.loads(data)
                return MyDomainCommand(**parsed)
            except Exception as e:
                raise DeserializationFailed(str(e))

    Attributes:
        body: Optional request body as raw bytes.
        content_type: Content type of the body (e.g., "application/json").
        content_schema: Optional content schema URI.
    """

    body: bytes | None = None
    content_type: str = "application/json"
    content_schema: str | None = None

    @classmethod
    def new(
        cls,
        body: bytes | None,
        content_type: str = "application/json",
    ) -> Command:
        """Create a new command with the given body and content type."""
        return cls(body=body, content_type=content_type)

    @classmethod
    def json(cls, body: bytes) -> Command:
        """Create a command with a JSON body."""
        return cls(body=body, content_type="application/json")

    def with_schema(self, schema: str) -> Command:
        """Return a new command with the content schema set."""
        return Command(
            body=self.body,
            content_type=self.content_type,
            content_schema=schema,
        )

    def get_body(self) -> bytes | None:
        """Get a reference to the body bytes if present."""
        return self.body

    def get_content_type(self) -> str:
        """Get the content type."""
        return self.content_type

    def get_content_schema(self) -> str | None:
        """Get the content schema if present."""
        return self.content_schema

    def is_json(self) -> bool:
        """Check if the content type is JSON."""
        return self.content_type == "application/json" or self.content_type.endswith("+json")


@attrs.define
class CommandRequest:
    """A command request to execute a state change.

    Attributes:
        headers: HTTP-style headers for the request.
        body: Optional request body.
        content_type: Content type of the body (e.g., "application/json").
        content_schema: Optional content schema URL for validation.

    Example:
        # Simple request with JSON body
        request = CommandRequest.json({"account_id": "acc-123", "amount": 100})

        # Request with custom headers
        request = (
            CommandRequest.new()
            .with_body(b'{"data": "value"}')
            .with_content_type("application/json")
            .with_header("X-Request-Id", "req-456")
        )
    """

    headers: list[tuple[str, str]] = attrs.Factory(list)
    body: bytes | None = None
    content_type: str | None = None
    content_schema: str | None = None

    @classmethod
    def new(cls) -> CommandRequest:
        """Create a new empty command request."""
        return cls()

    @classmethod
    def with_body(cls, body: bytes) -> CommandRequest:
        """Create a command request with a body."""
        return cls(body=body)

    @classmethod
    def json(cls, value: object) -> CommandRequest:
        """Create a command request with a JSON-serialized body.

        This serializes the value to JSON and sets the appropriate Content-Type header.

        Args:
            value: The value to serialize to JSON.

        Returns:
            A CommandRequest with JSON body.

        Raises:
            SerializationFailed: If JSON serialization fails.

        Example:
            request = CommandRequest.json({
                "account_id": "acc-123",
                "initial_balance": 1000,
            })
            assert request.get_header("Content-Type") == "application/json"
        """
        import json

        try:
            body = json.dumps(value).encode()
        except (TypeError, ValueError) as e:
            raise SerializationFailed(str(e)) from e

        return cls(
            headers=[("Content-Type", "application/json")],
            body=body,
            content_type="application/json",
        )

    def with_header(self, name: str, value: str) -> Self:
        """Add a header to the request."""
        self.headers.append((name, value))
        return self

    def set_body(self, body: bytes) -> Self:
        """Set the request body."""
        self.body = body
        return self

    def with_content_type(self, content_type: str) -> Self:
        """Set the content type.

        Example:
            request = (
                CommandRequest.new()
                .set_body(b"<xml>data</xml>")
                .with_content_type("application/xml")
            )
        """
        self.content_type = content_type
        return self

    def with_content_schema(self, schema_url: str) -> Self:
        """Set the content schema URL.

        Example:
            request = (
                CommandRequest.new()
                .set_body(b"{}")
                .with_content_type("application/json")
                .with_content_schema("https://example.com/schemas/command.json")
            )
        """
        self.content_schema = schema_url
        return self

    def get_header(self, name: str) -> str | None:
        """Get a header value by name (case-insensitive)."""
        name_lower = name.lower()
        for key, value in self.headers:
            if key.lower() == name_lower:
                return value
        return None
