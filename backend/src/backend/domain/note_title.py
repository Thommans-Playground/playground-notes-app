"""
The NoteTitle value object (DES-NOTE-001, section 3).

Realizes the Normalized Title concept (ONT-NOTE-003) and enforces
ONT-RULE-NOTE-002.
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class NoteTitle: 
    """
    An immutable Title that is already normalized.

    Build one with `NoteTitle.of`, which is the only intended way in.
    """

    value: str 

    @classmethod 
    def of(cls, raw: str)-> "NoteTitle":
        """
        Build a NoteTitle from raw text.

        Args:
            raw: The Title text as the User gave it.

        Returns:
            A NoteTitle holding the text.
        """
        return cls(value=raw)