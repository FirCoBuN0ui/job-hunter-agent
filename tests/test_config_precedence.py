from main import get_explicit_cli_flags


def test_get_explicit_cli_flags_basic():
    argv = ["main.py", "--config", "config.yaml", "--top=2", "--keywords", "python,etl"]
    flags = get_explicit_cli_flags(argv)
    assert "config" in flags
    assert "top" in flags
    assert "keywords" in flags