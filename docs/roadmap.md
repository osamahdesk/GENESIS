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

## Phase 4 — Strategy evolution

Days 25–35 introduce a versioned Strategy object, one mutation operator, frozen parents, candidate selection, regression gates, failure memory, and ablation reports.

## Phase 5 — Research extensions

After v0.1 is stable, investigate dynamic roles, tool experiments, capability-gap analysis, and knowledge graphs. These are separate research milestones, not prerequisites for the first release.

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
