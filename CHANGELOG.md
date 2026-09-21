# Changelog

## Unreleased

- Approved the reduced v0.1 scope.
- Added the project vision, architecture, evaluation protocol, security model, roadmap, work tree, and daily work-file system.
- Added the initial Python package scaffold and offline smoke test.

## v0.1 development core

- Added the offline provider, benchmark evaluator, restricted runner, SQLite store, artifact hashing, agent roles, Coordinator, CLI commands, local dashboard, result documentation, and visual diagrams.
- Added the first end-to-end baseline result: `EXP-000001`, verified, 7/7 cases passed.

## Phase 2 — local model and guided UI

- Added the `sshleifer/tiny-gpt2` Hugging Face checkpoint with SHA-256 hashes.
- Added the optional `HuggingFaceLocalProvider` and local-model example.
- Added Arabic project documentation in `README.ar.md`.
- Added a guided dashboard with clickable teaching hints and a visible permission center.
- Added explicit deny-by-default permission policy and CLI inspection/grant commands.
- Verified the local model through the provider boundary and kept the default suite independent of heavyweight dependencies.

## Guided capabilities and AI Builder

- Added reversible dashboard toggles for Transformers, PyTorch, Hugging Face, AI Builder, and model training.
- Added a deny-by-default capability policy with explicit user confirmation state.
- Added a sandbox-only AI Builder that writes reviewable model-project proposals without executing generated code.
- Verified the UI toggle path through the local HTTP dashboard.

## Performance engineering

- Added accelerated batch evaluation with a separate worker and fresh namespace per case.
- Added in-memory and persistent hash-keyed evaluation caching.
- Added inference-mode and evaluation-mode optimizations for the local model provider.
- Added reproducible speed benchmarks and documented the measured batch and cache improvements.
- Kept isolated per-case execution available for untrusted artifacts.

## Teacher model onboarding

- Added memory-aware starter model recommendations.
- Added model selection by Hub ID, public URL, or local directory.
- Added persistent `teacher.json` selection records.
- Added explicit public Hugging Face Hub API search with read-only permission gating.
- Added dashboard `Use` actions for search results and teacher selection.

## PyPI packaging preparation

- Renamed the distribution to `genesis-agi` and set the first release version to `0.1.0`.
- Added PyPI metadata, project URLs, classifiers, keywords, and release tooling.
- Added the TestPyPI and production release guide.
- Built and validated the wheel and source distribution with `twine check`.

## 0.1.1 mobile compatibility fix

The evaluator now detects when accelerated batch execution produces no usable output, then retries the same cases through the portable isolated runner. This fixes Android/Termux environments where the batch worker can complete without returning captured stdout. The fallback is covered by a dedicated test.

## 0.1.2 cache invalidation fix

The evaluation cache schema version is now part of the cache key. Results created by older evaluator behavior cannot be reused after a compatibility fix, preventing stale mobile failures from being reported as fresh evaluations.

## 0.1.3 public API hardening

The package now exposes `normalize_source` from `genesis.providers`, adds a root `genesis.__version__`, and includes a mobile-safe library smoke example. Public import coverage now runs in CI so missing exports are caught before a PyPI release.

## 0.2.0 — Auditable adaptive core

Added versioned experiment identity, benchmark split protection, skill contracts, dynamic planning, strategy memory for successes and failures, evidence confidence and contradiction assessment, a centralized risk policy engine, an external kill switch, multidimensional learning-curve metrics, and a regression-gated improvement loop. The Coordinator now records its plan, identity fingerprint, and lessons alongside every experiment.
