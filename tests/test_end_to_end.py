from genesis.core import Coordinator


def test_coordinator_runs_reproducible_baseline(tmp_path):
    result = Coordinator(tmp_path / ".genesis").run_once("EXP-TEST-001")

    assert result["evaluation"]["score"] == 1.0
    assert result["evaluation"]["passed"] == 7
    assert result["experiment"]["status"] == "verified"
    assert result["critique"]["failure_count"] == 0
