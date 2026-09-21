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
