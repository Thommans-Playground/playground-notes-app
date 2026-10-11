"""
Domain errors for Note Management (DES-NOTE-001, section 4).
"""


class InvalidTitle(Exception):
    """
    Raised when raw text cannot become a Normalized Title.

    Enforces ONT-RULE-NOTE-002. It carries no data: the driving adapter
    decides how to tell the User that the Title is not valid.
    """
