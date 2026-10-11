"""
The NoteId value object (DES-NOTE-001, section 3).

Realizes the Note Identifier concept (ONT-NOTE-005) and enforces
ONT-RULE-NOTE-001: every Note has one identifier, unique and never changing.
"""

from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True)
class NoteId:
    value: UUID

    @classmethod
    def generate(cls) -> NoteId:
        """
        Generate a new NoteId with a unique UUID.

        Returns:
            A new NoteId instance with a unique UUID.
        """
        return cls(uuid4())
