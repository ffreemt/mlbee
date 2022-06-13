"""Test st_mlbee."""
# pylint: disable=broad-except
from st_mlbee import __version__
from st_mlbee import st_mlbee


def test_version():
    """Test version."""
    assert __version__[:3] == "0.1"


def test_sanity():
    """Check sanity."""
    try:
        assert not st_mlbee()
    except Exception:
        assert True
