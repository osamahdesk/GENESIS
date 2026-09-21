# GENESIS

> A reproducible, local-first framework for measurable multi-agent AI experiments.

GENESIS is an open-source research project that studies whether structured collaboration between specialized AI agents can produce better problem-solving strategies under independent evaluation.

The project does not claim artificial general intelligence or unrestricted autonomous self-improvement. Its first objective is narrower and testable: run reproducible experiments in which agents research, build, execute, evaluate, critique, remember results, and compare strategies.

## The central rule

> A claimed improvement is accepted only when it is demonstrated by independent, repeatable evaluation.

An agent explanation is a hypothesis. An experiment result is evidence. A verified improvement must survive a frozen baseline, validation tasks, hidden tasks, resource limits, and regression checks.

## What we are building first

GENESIS v0.1 is a local command-line experiment runner for small Python problem-solving tasks. It contains a provider interface, structured experiment records, a restricted execution boundary, an independent evaluator, a baseline workflow, and reproducibility bundles.

The first release intentionally does **not** include autonomous browsing, external write actions, dynamic role creation, unrestricted shell access, distributed execution, or model training.

## Core workflow

```text
Task
  ↓
Hypothesis
  ↓
Strategy
  ↓
Implementation artifact
  ↓
Restricted execution
  ↓
Independent evaluation
  ↓
Critique and failure analysis
  ↓
Experiment record
  ↓
Evidence-based comparison
```

## Repository map

- `docs/vision.md` — project identity and research question.
- `docs/v0.1-spec.md` — the approved scope for the first release.
- `docs/architecture.md` — components, interfaces, and lifecycle.
- `docs/evaluation.md` — baselines, metrics, repetitions, and ablations.
- `docs/security.md` — execution boundaries and known limitations.
- `docs/roadmap.md` — phased roadmap and daily work sequence.
- `docs/work-tree.md` — work breakdown structure.
- `docs/daily/` — one file for each working day.
- `configs/` — versioned configuration examples.
- `benchmarks/` — benchmark definitions and task data.
- `genesis/` — Python package; implementation begins with the daily files.
- `tests/` — unit, integration, evaluation, and safety tests.

## Development rule

Work is completed one day at a time. Each daily file defines the scope, expected outputs, acceptance criteria, tests, and stop conditions. Do not silently implement a later day's feature. If architecture changes, record the reason in the relevant daily file and in the changelog.

## Quick start

The initial scaffold is intentionally small. Once the first implementation day is complete:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
python -m genesis
```

## Project status

The repository starts at **pre-development / v0.1 planning**. The approved implementation order is documented in `docs/roadmap.md`.

## License

MIT. See `LICENSE`.
