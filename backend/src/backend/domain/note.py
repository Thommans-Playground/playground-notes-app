"""
The Note Aggregate Root (DES-NOTE-001, sections 1 and 2).
"""

from dataclasses import dataclass

from backend.domain.note_title import NoteTitle


@dataclass
class Note:
    """
    A written information that a user keeps.

    It is the aggregate root, so callers change its state only through
    its public behavior.
    """

    title: NoteTitle
    content: str | None

    @classmethod
    def create(cls, title: str, content: str | None = None) -> Note:
        """
        Create a new Note.

        Args:
            title: The raw Title as the User gave it.
            content: The Content, or None if the User gave none.

        Returns:
            A new Note.

        Raises:
            InvalidTitle: If the Title cannot be normalized (ONT-RULE-NOTE-002).
        """
        return cls(title=NoteTitle.of(title), content=content)
