from genesis.core import PermissionPolicy
from genesis.ui import render_dashboard


def test_permissions_are_deny_by_default_and_explicitly_grantable(tmp_path):
    path = tmp_path / "permissions.json"
    policy = PermissionPolicy()
    assert policy.shell is False
    assert policy.external_actions is False
    policy.grant_project_filesystem()
    policy.save(path)
    restored = PermissionPolicy.load(path)
    assert restored.filesystem == "project_only"
    assert restored.user_confirmed is True


def test_dashboard_explains_permission_boundary():
    page = render_dashboard(None, PermissionPolicy())
    assert "Permission center" in page
    assert "Safe by default" in page
    assert "data-hint" in page
    assert "Transformers" in page
    assert "AI Builder" in page
    assert "type='submit'" in page
