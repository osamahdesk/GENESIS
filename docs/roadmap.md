# GENESIS Roadmap

## Planning rule

Each working day has one scope file under `docs/daily/`. The file is the contract for that day. It is updated with implementation notes, tests, blockers, and the final status. A later feature is not started until the current file meets its acceptance criteria or the plan is intentionally revised.

## Phase 0 — Foundation

Days 01–05 establish the package, configuration, schemas, event model, and offline test path.

## Phase 1 — First complete experiment

Days 06–12 implement the provider abstraction, Researcher, Builder, restricted runner, evaluator, Critic, Coordinator, and persistent records.

## Phase 2 — Scientific integrity

Days 13–18 add benchmark splits, hidden evaluation, reproducibility identity, baseline comparisons, repeated trials, cost tracking, and failure preservation.

## Phase 3 — Usable v0.1 release

Days 19–24 add the CLI, configuration, error handling, safety tests, documentation, clean-install verification, and a public example. The release is made only when the acceptance criteria in `docs/v0.1-spec.md` pass.

## Phase 4 — Auditable adaptive core

The next milestone introduces the versioned experiment identity, benchmark split registry, skill contracts, dynamic planning, strategy memory, evidence assessment, risk policy decisions, an external kill switch, and multidimensional learning-curve metrics. Every adaptive change must remain comparable to a frozen baseline.

## Phase 5 — Strategy evolution

Introduce one mutation operator, frozen parents, candidate selection, regression gates, failure memory, repeated trials, and ablation reports. A strategy is promoted only when its quality-adjusted utility improves without adding safety violations.

## Phase 6 — Controlled external research

Only after the offline core is reliable: read-only search, page reading, source provenance, evidence objects, freshness, and conflict reporting. Browser actions and external writes remain separate milestones.

## Daily file convention

Every daily file contains:

- Objective.
- In scope.
- Out of scope.
- Files expected to change.
- Acceptance criteria.
- Tests to run.
- Implementation notes.
- Blockers.
- Final status.

The next day's file is not marked active until the current day's status is `COMPLETE` or the plan records an explicit revision.
