# Day 13 — Hugging Face Local Provider

**Status:** `COMPLETE`

## Objective

Add a real small Hugging Face checkpoint and a lazy provider that can load it locally without coupling the default GENESIS installation to PyTorch.

## In scope

- `sshleifer/tiny-gpt2` checkpoint.
- Local model metadata and SHA-256 manifest.
- Optional `hf` dependency group.
- `HuggingFaceLocalProvider`.
- Provider tests that do not require heavyweight dependencies.

## Acceptance criteria

- [x] Model files are committed to GitHub.
- [x] The provider exposes model and provider metadata.
- [x] Optional dependencies are lazy and documented.
- [x] The default test suite passes without the `hf` extra.
- [x] A local-model smoke run is recorded when the optional dependencies are available.

## Verification

Default suite: `14 passed` without the Hugging Face extra.

Local model smoke run:

```text
PROVIDER=huggingface-local
MODEL=sshleifer-tiny-gpt2
TEXT=GENESIS is factors factors factors factors factors factors factors factors
INPUT_TOKENS=4
OUTPUT_TOKENS=8
```

The output is intentionally treated as an integration result, not a quality claim. The tiny checkpoint proves local loading and generation through the provider boundary.

## Final status

`COMPLETE`
