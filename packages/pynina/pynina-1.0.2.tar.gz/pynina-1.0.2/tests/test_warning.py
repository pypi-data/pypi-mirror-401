from copy import deepcopy
from datetime import datetime, timedelta

from pynina import Warning

dummy_warning = Warning(
    "id",
    "headline",
    "severity",
    "description",
    "sender",
    [],
    [],
    "web",
    datetime.now().isoformat(),
    None,
    None,
)


def test_warning_valid_no_start_no_exp():
    """Test if a warning is valid when it has no start and no expiration time."""
    warning = deepcopy(dummy_warning)

    assert warning.is_valid


def test_warning_valid_no_exp():
    """Test if a warning is valid when it has a start but no expiration time."""
    warning = deepcopy(dummy_warning)
    warning.start = (datetime.now() - timedelta(hours=2)).isoformat()

    assert warning.is_valid


def test_warning_valid_no_start_exp_future():
    """Test if a warning is valid when it has an expiration time in the future but start time."""
    warning = deepcopy(dummy_warning)
    warning.expires = (datetime.now() + timedelta(hours=2)).isoformat()

    assert warning.is_valid


def test_warning_valid_no_start_exp_past():
    """Test if a warning is valid when it has an expiration time in the past but start time."""
    warning = deepcopy(dummy_warning)
    warning.expires = (datetime.now() - timedelta(hours=2)).isoformat()

    assert not warning.is_valid


def test_warning_valid_no_start_exp_now():
    """Test if a warning is valid when it has an expiration time is now but start time."""
    warning = deepcopy(dummy_warning)
    warning.expires = datetime.now().isoformat()

    assert not warning.is_valid
