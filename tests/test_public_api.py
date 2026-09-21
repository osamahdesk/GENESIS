from genesis import __version__
from genesis.core import PermissionPolicy
from genesis.providers import MockProvider, normalize_source, recommended_models


def test_public_mobile_api_exports_are_importable():
    assert __version__ == "0.1.3"
    assert MockProvider().generate("hello").provider == "mock"
    assert normalize_source("sshleifer/tiny-gpt2") == ("huggingface", "sshleifer/tiny-gpt2")
    assert recommended_models(1.0)[0].repo_id == "sshleifer/tiny-gpt2"
    assert PermissionPolicy().network == "none"
