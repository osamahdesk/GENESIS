# Phase 2 — Model-backed Experiments and Scientific Integrity

## Goal

Phase 2 introduces a real small local language model without weakening GENESIS's reproducibility or offline fallback. It also turns the baseline into a proper comparison target.

## Milestones

1. Include and verify a small Hugging Face checkpoint.
2. Add a lazy local provider so the core does not require heavyweight dependencies.
3. Record model identity and model-path metadata in experiments.
4. Compare mock, local-model, and future API-backed workflows under explicit budgets.
5. Add repeated trials, validation/hidden split reporting, cost and latency metrics, and failure preservation.
6. Add a frozen baseline and regression gate before strategy evolution.

## Model choice

The first included checkpoint is `sshleifer/tiny-gpt2`. It is small enough to commit to GitHub and useful for integration tests. It is not treated as a high-quality assistant; its purpose is to verify local model loading and provider isolation.

## Why the model is optional

The deterministic mock path remains the default because it is stable, fast, and usable in clean environments. Users who want the local model install the `hf` extra. This prevents a large PyTorch dependency from becoming a requirement for documentation, schema, and evaluator tests.

## Acceptance criteria

Phase 2 is complete only when the local model can be loaded from the committed files, a generation call returns provider metadata, and the same repository still passes its default offline test suite without the optional dependency.
