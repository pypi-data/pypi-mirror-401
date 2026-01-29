"""Test the indexing module."""

from lisaconstants.indexing import adjacent_mosa, distant_mosa, link2sc, mosa2sc


def test_link2sc() -> None:
    """Test the conversion of a link to emitter and receiver spacecraft indices."""

    assert link2sc(32) == (2, 3)
    assert link2sc(13) == (3, 1)
    assert link2sc(21) == (1, 2)


def test_mosa2sc() -> None:
    """Test the conversion of a MOSA to emitter and receiver spacecraft indices."""

    assert mosa2sc(32) == (3, 2)
    assert mosa2sc(13) == (1, 3)
    assert mosa2sc(21) == (2, 1)


def test_distant_mosa() -> None:
    """Test the extraction of the distant MOSA from a given MOSA."""

    assert distant_mosa(32) == 23
    assert distant_mosa(13) == 31
    assert distant_mosa(21) == 12
    assert distant_mosa(12) == 21
    assert distant_mosa(23) == 32
    assert distant_mosa(31) == 13


def test_adjacent_mosa() -> None:
    """Test the extraction of the adjacent MOSA from a given MOSA."""

    assert adjacent_mosa(32) == 31
    assert adjacent_mosa(13) == 12
    assert adjacent_mosa(21) == 23
    assert adjacent_mosa(12) == 13
    assert adjacent_mosa(23) == 21
    assert adjacent_mosa(31) == 32
