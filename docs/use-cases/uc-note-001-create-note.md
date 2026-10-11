# UC-NOTE-001: Create Note

**Status:** Draft  
**Bounded Context:** Note Management  
**Requirement:** REQ-FR-NOTE-001

## Goal

A User creates a Note.

## Primary Actor

User

## Preconditions

None.

## Main Flow

1. The User provides a Title and, optionally, Content.
2. The system normalizes and validates the Title (ONT-RULE-NOTE-002).
3. The system assigns the Note a Note Identifier (ONT-RULE-NOTE-001).
4. The system creates the Note as Active (ONT-RULE-NOTE-003).
5. The system keeps the Note.
6. The system returns the Note Identifier to the User.

## Alternative Flows

**AF-001: Invalid Title** (REQ-FR-NOTE-001/AC-005)

At step 2, the Title is not valid.

- No Note is created.
- The system tells the User the Title is not valid.

**AF-002: Note cannot be kept** (REQ-FR-NOTE-001/AC-006)

At step 5, the system cannot keep the Note.

- No Note is created.
- The system tells the User that creation failed.

## Postconditions

- On success, the Note exists with the Normalized Title and the Content provided.
- On any alternative flow, no Note exists.
