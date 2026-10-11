# DES-NOTE-001: Note Domain Model

**Status:** Draft  
**Bounded Context:** Note Management  
**Ontology:** docs/ontology/ont-note.ttl  
**Use Case:** UC-NOTE-001  
**Language:** UL-NOTE-001

## 1. Aggregate

### Note Aggregate

**Aggregate Root:** Note (ONT-NOTE-001)

The Note aggregate represents a single Note and keeps itself consistent.

For now, the aggregate consists of one Entity and its Value Objects.

## 2. Entity

### Note

**Identity:** NoteId

**Attributes** (type mapping of the ontology relationships):

| Attribute | Type | Realizes |
|---|---|---|
| id | NoteId | ONT-REL-NOTE-001 |
| title | NoteTitle | ONT-REL-NOTE-002 |
| content | str \| None | ONT-REL-NOTE-003 |
| status | NoteStatus | ONT-REL-NOTE-004 |

**Behavior:**
- create(title, content): Note. A factory that returns a new Note.

## 3. Value Objects

### NoteId

Realizes ONT-NOTE-005. An immutable, UUID-backed identifier. Equality is based on its UUID value.

- generate(): NoteId. Returns a new random identifier.

### NoteTitle

Realizes ONT-NOTE-003. An immutable value that holds a Normalized Title.

- of(raw): NoteTitle. The only way to build one. Raises InvalidTitle.

### NoteStatus

Realizes ONT-NOTE-006. An enumeration of its members in the ontology.

## 4. Domain Errors

### InvalidTitle

Raised by NoteTitle.of when the raw Title cannot become a Normalized Title (ONT-RULE-NOTE-002).

## 5. Rule Enforcement

| Ontology rule | Enforced by |
|---|---|
| ONT-RULE-NOTE-001 | NoteId.generate; the aggregate exposes no way to change the id |
| ONT-RULE-NOTE-002 | NoteTitle.of |
| ONT-RULE-NOTE-003 | Note.create |
| ONT-RULE-NOTE-004 | NoteStatus enumeration |
| ONT-RULE-NOTE-005 | The behavior that changes status, designed with each use case |
| ONT-RULE-NOTE-006 | The content attribute is a single optional str |

## 6. Domain Invariants

None yet. An invariant (INV) is recorded here when the aggregate must protect a condition that the ontology cannot express.

## 7. Behavior

### create(title, content)

Realizes UC-NOTE-001. Builds the NoteTitle, generates the NoteId, and returns a Note with the initial status. The flow is defined in the use case and is not repeated here.

## 8. Aggregate Boundary

The Note aggregate is independently consistent.

Callers change its state only through its public behavior.

The Note aggregate does not keep itself. Keeping Notes is a driven port (ADR-001), designed per use case in `design-uc-*` diagrams.

## 9. Verification Mapping

Which tests cover each acceptance criterion. The tests carry their IDs as tags or markers when written. Acceptance tests run the Gherkin scenarios against the driving port. System tests go through the HTTP adapter.

### UC-NOTE-001

| Acceptance criterion | Acceptance | System | Integration | Unit |
|---|---|---|---|---|
| REQ-FR-NOTE-001/AC-001 | Scenario | Create succeeds (main flow) | Repository adapter keeps the Note | Note.create keeps the Content |
| REQ-FR-NOTE-001/AC-002 | Scenario | | | Note.create with no Content |
| REQ-FR-NOTE-001/AC-003 | Scenario | Response carries the Note Identifier | | NoteId.generate returns distinct values |
| REQ-FR-NOTE-001/AC-004 | Scenario | | | Note.create sets the initial status |
| REQ-FR-NOTE-001/AC-005 | Scenario | AF-001: invalid Title is refused | | NoteTitle.of with valid, blank, empty, padded, and inner-space Titles; the service does not call the repository |
| REQ-FR-NOTE-001/AC-006 | Scenario | AF-002: failure to keep is reported | | The service reports a failing repository and returns no identifier |

Ontology check, as a unit test: a created Note, converted to RDF, conforms to the shapes in ont-note.ttl (ONT-RULE-NOTE-001, 002, 004, 006).

## 10. Not Yet Designed

- Behavior other than create. It is designed with its own use case.
- Domain events.
