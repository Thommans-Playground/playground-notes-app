# Notes App — Kanban

## Backlog
- UC-NOTE-002: Retrieve Note
- UC-NOTE-003: Rename Note
- UC-NOTE-004: Archive Note
- UC-NOTE-005: Restore Note
- UC-NOTE-006: Delete Note

## Analysis

## Design

## Implementation
- UC-NOTE-001: Create Note
  - [x] 1 Domain: NoteTitle keeps valid text (AC-001)
  - [x] 2 Domain: NoteTitle removes surrounding whitespace (AC-007)
  - [x] 3 Domain: NoteTitle keeps inner spaces (AC-007)
  - [x] 4 Domain: empty Title raises InvalidTitle (AC-005)
  - [x] 5 Domain: whitespace-only Title raises InvalidTitle (AC-005)
  - [ ] 5a Domain: NoteTitle cannot be built without validation (AC-005)
  - [ ] 6 Domain: NoteId.generate returns distinct ids (AC-003)
  - [ ] 7 Domain: Note.create keeps Title and Content (AC-001)
  - [ ] 8 Domain: Note.create works with no Content (AC-002)
  - [ ] 9 Domain: a new Note is Active (AC-004)
  - [ ] 10 Domain: a new Note has an id (AC-003)
  - [ ] 10a Domain: a created Note conforms to the ontology shapes
  - [ ] 11 Application: service stores the Note and returns its id (AC-001, AC-003)
  - [ ] 12 Application: invalid Title raises and the repository is not called (AC-005)
  - [ ] 13 Application: failing repository raises NoteNotKept, no id returned (AC-006)
  - [ ] 14 Integration: in-memory repository passes the contract tests (AC-001)
  - [ ] 15 System: HTTP create, 422 and 500 flows (AC-001, AC-003, AC-005, AC-006)
  - [ ] 16 Acceptance: Gherkin scenarios against the driving port (AC-001 to AC-007)

## Verification

## Done
