# Minimal test to ensure package imports correctly
import pytest


def test_import():
    """Test that the package can be imported."""
    import stylometry
    assert hasattr(stylometry, "main")
    assert hasattr(stylometry, "__version__")


def test_version():
    """Test that version is a valid string."""
    from stylometry import __version__
    assert isinstance(__version__, str)
    assert len(__version__.split(".")) >= 2


def test_cli_help(capsys):
    """Test that CLI help works."""
    from stylometry import main
    import sys
    
    # Capture the help output
    with pytest.raises(SystemExit) as exc_info:
        main(["--help"])
    
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "stylometric" in captured.out.lower() or "corpus" in captured.out.lower()
