"""Unit tests for the Note aggregate root (DES-NOTE-001, sections 1 and 2).

Note realizes the Note concept (ONT-NOTE-001). These tests check the factory
`Note.create` in isolation, with no application service or repository.
"""

import pytest

from backend.domain.note import Note


@pytest.mark.ac("REQ-FR-NOTE-001/AC-001")
def test_create_keeps_the_title_and_content():
    """
    A created Note holds the Title and the Content it was given.

    Given the Title "Shopping list" and the Content "Milk, eggs, bread"
    When a Note is created with Note.create
    Then the Note's Title is "Shopping list"
    And the Note's Content is "Milk, eggs, bread"
    """
    note = Note.create("Shopping list", "Milk, eggs, bread")

    assert note.title.value == "Shopping list"
    assert note.content == "Milk, eggs, bread"
