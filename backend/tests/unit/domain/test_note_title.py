"""Unit tests for the NoteTitle value object (DES-NOTE-001, section 3).

NoteTitle realizes the Normalized Title concept (ONT-NOTE-003) and enforces
ONT-RULE-NOTE-002. These tests check it in isolation, with no application
service, repository or framework involved.
"""

import pytest

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
