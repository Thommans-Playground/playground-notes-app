"""Unit tests for the NoteTitle value object (DES-NOTE-001, section 3).

NoteTitle realizes the Normalized Title concept (ONT-NOTE-003) and enforces
ONT-RULE-NOTE-002. These tests check it in isolation, with no application
service, repository or framework involved.
"""

import pytest

from backend.domain.errors import InvalidTitle
from backend.domain.note_title import NoteTitle


@pytest.mark.ac("REQ-FR-NOTE-001/AC-001")
def test_a_valid_title_keeps_its_text():
    """A Title with visible characters and no surrounding whitespace is kept as given.

    Given the raw text "Shopping list"
    When a NoteTitle is built from it with NoteTitle.of
    Then the NoteTitle's value is "Shopping list"
    """
    title = NoteTitle.of("Shopping list")

    assert title.value == "Shopping list"


@pytest.mark.ac("REQ-FR-NOTE-001/AC-007")
def test_whitespace_around_a_title_is_removed():
    """Leading and trailing whitespace is removed when a NoteTitle is built.

    Given the raw text "  Shopping list  "
    When a NoteTitle is built from it with NoteTitle.of
    Then the NoteTitle's value is "Shopping list"
    """
    title = NoteTitle.of("  Shopping list  ")

    assert title.value == "Shopping list"


@pytest.mark.ac("REQ-FR-NOTE-001/AC-007")
def test_spaces_inside_a_title_are_kept():
    """Only surrounding whitespace is removed; spaces between words are left alone.

    Given the raw text "  Shopping   list  " with several spaces between the words
    When a NoteTitle is built from it with NoteTitle.of
    Then the NoteTitle's value is "Shopping   list", with the inner spaces unchanged
    """
    title = NoteTitle.of("  Shopping   list  ")

    assert title.value == "Shopping   list"


@pytest.mark.ac("REQ-FR-NOTE-001/AC-005")
def test_an_empty_title_is_rejected():
    """A Title with no characters at all cannot become a Normalized Title.

    Given the raw text "" (nothing)
    When a NoteTitle is built from it with NoteTitle.of
    Then InvalidTitle is raised and no NoteTitle exists
    """
    with pytest.raises(InvalidTitle):
        NoteTitle.of("")


@pytest.mark.ac("REQ-FR-NOTE-001/AC-005")
def test_a_whitespace_only_title_is_rejected():
    """A Title with only whitespace has nothing left once normalized, so it is invalid.

    Given the raw text "   " (spaces only)
    When a NoteTitle is built from it with NoteTitle.of
    Then InvalidTitle is raised and no NoteTitle exists
    """
    with pytest.raises(InvalidTitle):
        NoteTitle.of("   ")


@pytest.mark.ac("REQ-FR-NOTE-001/AC-005")
def test_a_title_cannot_be_built_without_validation():
    """The constructor is private, so ONT-RULE-NOTE-002 cannot be skipped.

    Given the raw text "   " that NoteTitle.of would reject
    When a NoteTitle is built by calling the class directly
    Then TypeError is raised, so the only way in is NoteTitle.of
    """
    with pytest.raises(TypeError):
        NoteTitle("   ")
