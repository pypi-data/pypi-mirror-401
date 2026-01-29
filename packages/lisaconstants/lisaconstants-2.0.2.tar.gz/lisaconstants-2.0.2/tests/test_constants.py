"""Test the constants module."""

import typing as t

import pytest

import lisaconstants
import lisaconstants._constants
from lisaconstants import Alias, Constant, c, get_constant


def test_speed_of_light() -> None:
    """Test the value of `SPEED_OF_LIGHT`."""
    assert lisaconstants.SPEED_OF_LIGHT == 299792458


def test_c() -> None:
    """Test the value of the alias `c`."""
    assert c == 299792458


def test_constants_all_in_main_module() -> None:
    """Test that constants are correctly instantiated.

    This test checks that all constants returned by
    :func:`lisaconstants.get_all_constants` are correctly instantiated
    in ``lisaconstants.__init__.py``, i.e., that there is no mismatch
    between the variable name and :attr:`Constant.name`.

    This prevents typos such as

    .. code-block:: python

        SPED_F_LIGHT = Constant("SPEED_OF_LIGHT", ...)
    """
    for key, constant in lisaconstants.get_all_constants().items():
        assert hasattr(lisaconstants, key)
        assert getattr(lisaconstants, key) == constant.value


def test_aliases_all_in_main_module() -> None:
    """Test that aliases are correctly instantiated.

    This test checks that all aliases returned by
    :func:`lisaconstants.get_all_aliases` are correctly instantiated
    in ``lisaconstants.__init__.py``, i.e., that there is no mismatch
    between the variable name and :attr:`Alias.name`.

    This prevents typos such as (notice the mismatch between `v` and `c`)

    .. code-block:: python

        SPEED_OF_LIGHT = v = Constant("SPEED_OF_LIGHT", aliases=["c"], ...)
    """

    for key, alias in lisaconstants.get_all_aliases().items():
        assert hasattr(lisaconstants, key)
        assert getattr(lisaconstants, key) == alias.constant.value


def test_cannot_add_constant_twice() -> None:
    """Test checking that adding a name twice will raise an exception."""

    with pytest.raises(lisaconstants.ConstantNameAlreadyDefined):
        # Trying to add a constant whose name is that of an existing constant
        lisaconstants.Constant(
            "SUN_MASS", value=1.98848e30, unit="kg", description="Mass of the Sun"
        )

    with pytest.raises(lisaconstants.ConstantNameAlreadyDefined):
        # Trying to add a constant whose name is that of an existing alias
        lisaconstants.Constant("c", value=42, unit="Hz", description="Mass of the Sun")

    with pytest.raises(lisaconstants.ConstantNameAlreadyDefined):
        # Trying to add an alias whose name is that of an existing constant
        lisaconstants.get_all_constants()["SUN_MASS"].add_alias("SPEED_OF_LIGHT")

    with pytest.raises(lisaconstants.ConstantNameAlreadyDefined):
        # Trying to add an alias whose name is that of an existing alias
        lisaconstants.get_all_constants()["SUN_MASS"].add_alias("c")


@pytest.fixture(name="test_constant", params=[None, "Hz"])
def test_constant(request: t.Any) -> t.Generator[Constant, None, None]:
    """Return a test fixture constant."""

    # Define new constants that will be added in _all_constants dict
    cst = Constant(
        "test_constant",
        value=3.0,
        unit=request.param,
        description="Constant short-lived for tests",
    )

    # Return the alias
    yield cst

    # Perform some clean up after test function executes
    # pylint: disable=protected-access
    lisaconstants._constants._all_constants.pop("test_constant")


@pytest.fixture(name="pair")
def constat_alias_pair(
    test_constant: Constant,
) -> t.Generator[tuple[Constant, Alias], None, None]:
    """Return a pair of constant and alias for testing."""

    # Define new alias
    alias = test_constant.add_alias("test_alias")

    # Return the constant/alias pair
    yield test_constant, alias

    # Perform some cleanup
    # pylint: disable=protected-access
    lisaconstants._constants._all_aliases.pop("test_alias")


def test_constant_repr(pair: tuple[Constant, Alias]) -> None:
    """Test that constant and alias __repr__ work as intended."""

    cst, alias = pair

    # Test that constant and alias __repr__ work as intended
    if cst.unit is not None:
        assert str(cst) == "<test_constant (3.0 Hz)>"
        assert str(alias) == "<test_alias [test_constant] (3.0 Hz)>"
    else:
        assert str(cst) == "<test_constant (3.0)>"
        assert str(alias) == "<test_alias [test_constant] (3.0)>"


def test_constant_alias_cross_references(pair: tuple[Constant, Alias]) -> None:
    """Test that constant and alias cross-references are well defined."""
    cst, alias = pair

    # Check that new alias is properly recorded in constant aliases
    assert alias in cst.aliases

    # Check that all names are presents in the all_names property
    assert cst.name in cst.all_names
    assert alias.name in cst.all_names

    # Check that alias and constant inter-references are well defined
    assert alias in cst.aliases
    assert alias.constant is cst


def test_raised_exception_on_getting_undefined_constant() -> None:
    with pytest.raises(lisaconstants.ConstantNameUndefined):
        get_constant("UNDEFINED_CONSTANT")
