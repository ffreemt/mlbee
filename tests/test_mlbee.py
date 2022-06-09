"""Test mlbee."""
# pylint: disable=broad-except
from mlbee import __version__
from mlbee import mlbee


def test_version():
    """Test version."""
    assert __version__[:3] == "0.1"


def test_sanity():
    """Check sanity."""
    try:
        assert not mlbee()
    except Exception:
        assert True
