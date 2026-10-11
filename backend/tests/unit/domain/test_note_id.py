"""
Unit tests for the NoteId value object (DES-NOTE-001, section 3).

NoteId realizes the Note Identifier concept (ONT-NOTE-005) and supports
ONT-RULE-NOTE-001. These tests check it in isolation.
"""

import pytest

from backend.domain.note_id import NoteId


@pytest.mark.ac("REQ-FR-NOTE-001/AC-003")
def test_generated_ids_are_distinct():
    """
    Each generated identifier differs from every other one.

    Given two identifiers generated one after the other
    When they are compared
    Then they are not equal
    """
    first = NoteId.generate()
    second = NoteId.generate()

    assert first != second
