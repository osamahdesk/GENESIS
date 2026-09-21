# Day 01 — Foundation

**Status:** `IN_PROGRESS`

## Objective

Create a clean Python package, development configuration, repository structure, and a runnable offline entry point.

## In scope

- Package metadata.
- Basic module layout.
- CLI entry point.
- Development dependencies.
- Initial test command.
- No model calls and no generated code execution.

## Out of scope

- Agents.
- Persistent experiment storage.
- Network access.
- Sandbox implementation.
- Strategy evolution.

## Expected files

- `pyproject.toml`.
- `genesis/__main__.py`.
- `genesis/cli.py`.
- `tests/test_smoke.py`.

## Acceptance criteria

- [ ] `python -m genesis` runs without credentials.
- [ ] The package installs in editable mode.
- [ ] The smoke test passes.
- [ ] No secret is required for the first command.

## Tests

```bash
python -m genesis
python -m pytest
```

## Implementation notes

The daily file is updated as implementation progresses. Later-day features must not be added here.

## Blockers

None.

## Final status

`IN_PROGRESS`
