from genesis.providers.model_onboarding import normalize_source, recommended_models, select_teacher


def test_model_source_normalization(tmp_path):
    assert normalize_source("sshleifer/tiny-gpt2") == ("huggingface", "sshleifer/tiny-gpt2")
    assert normalize_source("https://huggingface.co/HuggingFaceTB/SmolLM-135M") == ("huggingface", "HuggingFaceTB/SmolLM-135M")
    assert normalize_source(str(tmp_path)) == ("local", str(tmp_path.resolve()))


def test_teacher_selection_is_persisted(tmp_path):
    selected = select_teacher("sshleifer/tiny-gpt2", tmp_path)
    assert selected.resolved_id == "sshleifer/tiny-gpt2"
    assert (tmp_path / "teacher.json").exists()


def test_catalog_recommendations_respect_memory():
    assert [item.repo_id for item in recommended_models(1.0)] == ["sshleifer/tiny-gpt2"]
