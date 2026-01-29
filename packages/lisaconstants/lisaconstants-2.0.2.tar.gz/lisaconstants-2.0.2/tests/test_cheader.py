"""Test C/C++ header generation."""

import os
import tempfile
from typing import Generator

from pytest import fixture, raises

from lisaconstants import Constant, _constants
from lisaconstants.__main__ import generate_header
from lisaconstants.headers import CHeaderGenerator, CppHeaderGenerator


@fixture(name="constants")
def h2g2() -> Generator[dict[str, Constant], None, None]:
    """Return dictionary of H2G2 constants."""

    # Define new constants that will be added in _all_constants dict
    Constant(
        "LIFE_UNIVERSE",
        42,
        unit=None,
        description="Answer to life, the Universe and everything",
        aliases="l",
    )
    Constant("TEAPOT", "418", unit=None, description="I am a teapot")

    # Return the _all_constants dict
    # pylint: disable=protected-access
    yield _constants._all_constants

    # Below is some clean up after test function executes
    _constants._all_constants.pop("LIFE_UNIVERSE")
    _constants._all_constants.pop("TEAPOT")
    _constants._all_aliases.pop("l")


def word_in_file(word: str, filename: str) -> bool:
    """Check that a word can be found in file.

    Args:
        word: Word to find.
        filename: Path to file.
    """
    with open(filename, "r", encoding="utf-8") as file:
        return any(word in line for line in file)


def test_cpp(constants: dict[str, Constant]):
    """Test generation of C++ header."""

    with tempfile.TemporaryDirectory() as temp_dir:

        filename = os.path.join(temp_dir, "lisaconstants.hpp")
        CppHeaderGenerator(constants).write(filename)

        assert os.path.exists(filename)
        assert word_in_file("LIFE_UNIVERSE", filename)
        assert word_in_file("TEAPOT", filename)
        assert word_in_file("l", filename)


def test_c(constants: dict[str, Constant]) -> None:
    """Test generation of C header."""

    with tempfile.TemporaryDirectory() as temp_dir:

        filename = os.path.join(temp_dir, "lisaconstants.h")
        CHeaderGenerator(constants).write(filename)

        assert os.path.exists(filename)
        assert word_in_file("LISA_LIFE_UNIVERSE", filename)
        assert word_in_file("LISA_TEAPOT", filename)


def test_cli_c() -> None:
    """Test generation of C header through CLI."""
    with tempfile.TemporaryDirectory() as temp_dir:

        generate_header(["--dir", temp_dir, "c"])
        filename = os.path.join(temp_dir, "lisaconstants.h")
        assert os.path.exists(filename)
        assert word_in_file("LISA_SPEED_OF_LIGHT", filename)


def test_cli_cpp() -> None:
    """Test generation of C header through CLI."""
    with tempfile.TemporaryDirectory() as temp_dir:

        generate_header(["--dir", temp_dir, "cpp"])
        filename = os.path.join(temp_dir, "lisaconstants.hpp")
        assert os.path.exists(filename)
        assert word_in_file("SPEED_OF_LIGHT", filename)


def test_cli_wrong_format() -> None:
    """Test CLI raises exception if format is unknown."""

    with tempfile.TemporaryDirectory() as temp_dir:
        with raises(SystemExit):
            generate_header(["--dir", temp_dir, "txt"])
