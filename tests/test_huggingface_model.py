from pathlib import Path

from genesis.providers.huggingface_local import HuggingFaceLocalProvider


MODEL_DIR = Path(__file__).parents[1] / "models" / "sshleifer-tiny-gpt2"


def test_included_huggingface_checkpoint_has_required_files():
    required = {"config.json", "vocab.json", "merges.txt", "pytorch_model.bin", "SHA256SUMS"}
    assert required.issubset({path.name for path in MODEL_DIR.iterdir()})


def test_huggingface_provider_is_lazy_and_provider_agnostic():
    provider = HuggingFaceLocalProvider(MODEL_DIR)
    assert provider.provider_name == "huggingface-local"
    assert provider.model_name == "sshleifer-tiny-gpt2"
