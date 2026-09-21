from genesis.core import PermissionPolicy
from genesis.evolution import AIBuilder


def test_ai_builder_creates_reviewable_proposal_only_when_enabled(tmp_path):
    policy = PermissionPolicy()
    builder = AIBuilder()
    try:
        builder.propose_model_project(policy, tmp_path / "candidate")
    except PermissionError:
        pass
    else:
        raise AssertionError("AI Builder must be disabled by default")

    policy.toggle_capability("ai_builder", True)
    policy.toggle_capability("transformers", True)
    proposal = builder.propose_model_project(policy, tmp_path / "candidate")

    assert proposal.status == "candidate"
    assert proposal.libraries == ("transformers",)
    assert (tmp_path / "candidate" / "proposal.json").exists()
