# Included Hugging Face Model

GENESIS includes the small `sshleifer/tiny-gpt2` checkpoint for local provider integration tests and demonstrations.

Source: https://huggingface.co/sshleifer/tiny-gpt2

The checkpoint is intentionally small and is not intended to be a high-quality production language model. Its purpose is to prove that GENESIS can load a local Hugging Face model through a provider boundary while keeping the default offline mock path available.

## Files

The directory contains the tokenizer files, configuration, and PyTorch checkpoint downloaded from the official Hugging Face repository. `SHA256SUMS` records the local file hashes committed with the project.

## Optional setup

```bash
pip install -e '.[hf]'
```

## Example

```python
from genesis.providers.huggingface_local import HuggingFaceLocalProvider

provider = HuggingFaceLocalProvider("models/sshleifer-tiny-gpt2")
response = provider.generate("GENESIS is")
print(response.text)
```

The default GENESIS test suite does not require this optional dependency. This keeps CI and the deterministic core lightweight.
