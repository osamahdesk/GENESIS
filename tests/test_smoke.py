from genesis.cli import main


def test_cli_starts_without_credentials(capsys):
    assert main([]) == 0
    assert "foundation is ready" in capsys.readouterr().out
