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
- create(title, content)

## 3. Value Objects

### NoteId

Realizes ONT-NOTE-005. An immutable, UUID-backed identifier. Equality is based on its UUID value.

### NoteTitle

Realizes ONT-NOTE-003. An immutable value that holds a Normalized Title.

### NoteStatus

Realizes ONT-NOTE-006. An enumeration of its members in the ontology.

## 4. Rule Enforcement

| Ontology rule | Enforced by |
|---|---|
| ONT-RULE-NOTE-001 | NoteId creation; the aggregate exposes no way to change it |
| ONT-RULE-NOTE-002 | NoteTitle construction |
| ONT-RULE-NOTE-003 | Note.create |
| ONT-RULE-NOTE-004 | NoteStatus enumeration |
| ONT-RULE-NOTE-005 | The behavior that changes status, designed with each use case |
| ONT-RULE-NOTE-006 | The content attribute allows no value |

## 5. Domain Invariants

None yet. An invariant (INV) is recorded here when the aggregate must protect a condition that the ontology cannot express.

## 6. Behavior

### create(title, content)

Realizes UC-NOTE-001. Returns a new Note. The flow is defined in the use case and is not repeated here.

## 7. Aggregate Boundary

The Note aggregate is independently consistent.

Callers change its state only through its public behavior.

The Note aggregate does not keep itself. Keeping and finding Notes is a driven port (ADR-001).

## 8. Not Yet Designed

- Behavior other than create. It is designed with its own use case.
- Domain events.
