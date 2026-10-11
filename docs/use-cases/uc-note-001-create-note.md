# UC-NOTE-001: Create Note

**Status:** Draft  
**Bounded Context:** Note Management  
**Requirement:** REQ-FR-NOTE-001

## Goal

Create a new note with a valid title and optional content.

## Primary Actor

User

## Preconditions

None for this initial single-user version.

## Main Flow

1. User provides a title and optional content.
2. System removes leading and trailing whitespace from the title.
3. System validates that the normalized title is non-empty.
4. System assigns a unique Note identifier.
5. System creates the Note with status ACTIVE.
6. System persists the Note.
7. System returns the created Note identifier.

## Alternative Flows

**AF-001: Empty Title**

- The supplied title is empty or contains only whitespace.
- The system rejects the request.
- No Note is created.

**AF-002: Persistence Failure**

- The system cannot save the Note.
- The operation fails without reporting successful creation.

**AF-003: Invalid Title**

If the normalized title is empty:
- Reject the request.
- Do not create or persist a Note.
- Return a validation error.

## Postconditions

- A new Note exists with a unique identifier.
- The Note has an ACTIVE status.
- The Note retains its supplied title and content.

## Related Artifacts

- REQ-FR-NOTE-001
- ONT-NOTE-001
- INV-NOTE-001
- INV-NOTE-002
