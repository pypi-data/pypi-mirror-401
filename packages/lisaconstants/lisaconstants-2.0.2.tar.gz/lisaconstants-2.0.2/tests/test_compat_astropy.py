"""Test the package consistency with astropy."""

import sys

import pytest

from lisaconstants import get_constant
from lisaconstants.compat.astropy import REFERENCE_VERSION, find_mismatched_constants
from lisaconstants.compat.astropy import get_mapping as get_astropy_mapping


@pytest.mark.skipif(sys.version_info < (3, 11), reason="requires python3.11 or higher")
def test_astropy_version_is_reference() -> None:
    """Check that test environment uses the reference astropy version."""
    import importlib.metadata

    from packaging.version import Version

    current_version = Version(importlib.metadata.version("astropy"))
    reference_version = Version(REFERENCE_VERSION)

    assert current_version == reference_version


def test_astropy_consistency() -> None:
    """Check that no constant report any mismatch with their astropy counterpart."""
    assert not find_mismatched_constants()


def test_get_astropy_counterpart() -> None:
    """Check that one can access an astropy counterpart"""
    SPEED_OF_LIGHT = get_constant("c")
    assert (
        map := get_astropy_mapping(SPEED_OF_LIGHT)
    ) is not None and map.astropy_name == "c"
    assert (
        map := get_astropy_mapping("SPEED_OF_LIGHT")
    ) is not None and map.astropy_name == "c"


def test_get_astropy_counterpart_when_undefined() -> None:
    """Check that get_mapping returns None when astropy counterpart undefined."""
    OBLIQUITY = get_constant("OBLIQUITY")
    assert get_astropy_mapping(OBLIQUITY) is None
    assert get_astropy_mapping("OBLIQUITY") is None
