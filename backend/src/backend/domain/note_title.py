"""
The NoteTitle value object (DES-NOTE-001, section 3).

Realizes the Normalized Title concept (ONT-NOTE-003) and enforces
ONT-RULE-NOTE-002.
"""

from dataclasses import dataclass
from backend.domain.errors import InvalidTitle


@dataclass(frozen=True, init=False)
class NoteTitle:
    """
    An immutable Title that is already normalized.

    Build one with `NoteTitle.of`, which is the only intended way in.
    """

    value: str

    def __init__(self, *args, **kwargs)-> None:
        """ 
        Prevent direct instantiation of NoteTitle. Use NoteTitle.of instead.
        """
        raise TypeError("Use NoteTitle.of to build a NoteTitle")

    @classmethod
    def of(cls, raw: str) -> "NoteTitle":
        """
        Build a NoteTitle from raw text.

        Args:
            raw: The Title text as the User gave it.

        Returns:
            A NoteTitle holding the text.

        Raises:
            InvalidTitle: If nothing is left after removing surrounding whitespace.
        """

        normalized = raw.strip()
        if not normalized:
            raise InvalidTitle()
        # return cls(value=normalized)
        title = object.__new__(cls)
        object.__setattr__(title, "value", normalized)
        return title
