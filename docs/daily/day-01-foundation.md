# Day 01 — Foundation

**Status:** `COMPLETE`

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

- [x] `python -m genesis` runs without credentials.
- [x] The package installs in editable mode.
- [x] The smoke test passes.
- [x] No secret is required for the first command.

## Tests

```bash
python -m genesis
python -m pytest
```

Result: `1 passed`.

## Implementation notes

The repository was initialized with a public-facing README, approved v0.1 specification, architecture, evaluation protocol, security model, roadmap, work tree, and daily-file system. The first CLI command is offline and does not require a provider credential.

## Blockers

None.

## Final status

`COMPLETE`
