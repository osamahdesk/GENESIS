from genesis import __version__
from genesis.core import PermissionPolicy
from genesis.providers import MockProvider, normalize_source, recommended_models


print(f"GENESIS {__version__} mobile-safe smoke test")
print(MockProvider().generate("hello").text)
print("Teacher source:", normalize_source("sshleifer/tiny-gpt2"))
print("Recommendations:", [model.repo_id for model in recommended_models(1.0)])
print("Default network permission:", PermissionPolicy().network)
print("PASS")
