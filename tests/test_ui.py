from genesis.ui import render_dashboard


def test_dashboard_contains_status_and_usage_hint():
    page = render_dashboard({"experiment": {"id": "EXP-1", "status": "verified"}, "evaluation": {"score": 1.0, "passed": 7, "total": 7}})

    assert "GENESIS Dashboard" in page
    assert "verified" in page
    assert "genesis run" in page
    assert "How GENESIS works" in page
