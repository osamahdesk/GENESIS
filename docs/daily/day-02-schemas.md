# Day 02 — Typed Domain Schemas

**Status:** `COMPLETE`

## Objective

Define the minimum typed data model for tasks, strategies, budgets, artifacts, metrics, and experiments before implementing orchestration or persistence.

## In scope

- `Task` model.
- `Strategy` model.
- `Budget` model.
- `ArtifactRef` model.
- `Metric` model.
- `Experiment` model.
- Experiment terminal status values.
- JSON-friendly serialization.
- Validation tests.

## Out of scope

- Event bus and transition enforcement.
- SQLite persistence.
- Model providers.
- Agent implementations.
- Benchmark execution.
- Evolution operators.

## Expected files

- `genesis/core/models.py`.
- `genesis/core/__init__.py`.
- `tests/test_models.py`.

## Acceptance criteria

- [x] Invalid required fields fail with clear errors.
- [x] Tasks require at least one evaluation case.
- [x] Strategies require at least one step.
- [x] Budgets reject invalid limits.
- [x] Experiments can contain artifacts and metrics.
- [x] Duplicate artifact identifiers are rejected.
- [x] Terminal experiment status records completion time.
- [x] Nested data can be serialized without custom JSON encoders.

## Tests

```bash
python -m pytest
```

Result: `6 passed`.

## Implementation notes

The domain model uses standard-library dataclasses and enums. It remains provider-independent, serializable, and deterministic. Hugging Face is intentionally deferred to the provider and benchmark phases, where it can add value without coupling the core schemas to an external service.

## Blockers

None.

## Final status

`COMPLETE`
