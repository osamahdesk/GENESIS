# Day 03 — Events and Lifecycle

**Status:** `COMPLETE`

## Objective

Make experiment progress explicit and auditable through a constrained state machine and append-only domain events.

## In scope

- Experiment lifecycle transitions.
- Domain event schema.
- Transition validation.
- Terminal-state completion timestamps.
- Event serialization.
- Tests for valid and invalid transitions.

## Out of scope

- Persistent event storage.
- Structured logging backend.
- Coordinator orchestration.
- Provider calls and agent execution.

## Acceptance criteria

- [x] Valid lifecycle transitions are accepted.
- [x] Invalid transitions are rejected.
- [x] Terminal states record completion time.
- [x] Every status change produces a serializable event.
- [x] Events contain actor, experiment, timestamp, payload, and schema version.

## Tests

```bash
python -m pytest
```

Result: `10 passed`.

## Implementation notes

The state machine is strict and is implemented independently from storage. Every accepted status change returns a `DomainEvent` that can later be persisted without changing the domain contract.

## Blockers

None.

## Final status

`COMPLETE`
