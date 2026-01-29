# EvidentSource Core for Python

Core domain types for the EvidentSource event sourcing platform.

## Installation

```bash
pip install evidentsource-core
```

## Types

### Events

- **Event**: A stored event with full metadata (id, stream, type, subject, time, data, etc.)
- **ProspectiveEvent**: An event before storage (for state changes)
- **EventData**: Binary or string event data
- **BinaryEventData**: Binary event payload
- **StringEventData**: String event payload

### Selectors

- **Selector**: Complex event selectors (subject, type, stream combinations)
- **EventSelector**: Parameters for event queries

### Constraints

- **Constraint**: Individual constraint on event sequences
- **AppendCondition**: Constraint to apply when committing events

### Identifiers

- **DatabaseName**: Database name identifier
- **StreamName**: Stream name identifier
- **EventId**: Event ID identifier
- **EventType**: Event type identifier
- **EventSubject**: Event subject identifier
- **StateViewName**: State view name identifier
- **StateChangeName**: State change name identifier

### State Views

- **StateView**: Rendered state view result
- **StateViewCodec**: Protocol for state view serialization

### State Changes

- **Command**: Command received by a state change
- **CommandRequest**: Full command request with headers
- **StateChangeDefinitionSummary**: State change definition info

## License

MIT OR Apache-2.0
