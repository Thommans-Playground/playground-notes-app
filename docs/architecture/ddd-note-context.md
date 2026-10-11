# DDD-NOTE-001: Note Domain Model

**Status:** Draft  
**Bounded Context:** Note Management  
**Related Ontology:** ONT-NOTE-001  
**Related Use Case:** UC-NOTE-001

## 1. Aggregate

### Note Aggregate

**Aggregate Root:** Note

The Note aggregate represents a single Note and maintains its internal consistency.

For the initial version, the aggregate consists of one Entity and its associated values.

## 2. Entity

### Note

**Identity:** NoteId

**Attributes:**
- id: NoteId
- title: NoteTitle
- content: str | None
- status: NoteStatus

**Behavior:**
- create(title, content)

## 3. Value Objects

### NoteId

An immutable, UUID-backed identifier.

Equality is based on its UUID value.

### NoteTitle

An immutable textual value.

Construction must reject empty or whitespace-only titles.

### NoteStatus

An enumeration:
- ACTIVE
- ARCHIVED
- DELETED

## 4. Aggregate Invariants

| Ontology Rule | Enforcement |
|---|---|
| INV-NOTE-001: Stable identity | NoteId creation and Note aggregate |
| INV-NOTE-002: Non-empty title | NoteTitle Value Object |
| INV-NOTE-003: Initial ACTIVE state | Note creation behavior |

## 5. Creation Behavior

**Operation:** CreateNote

Inputs:
- title: str
- content: str | None

Expected behavior:
1. Validate title using NoteTitle.
2. Generate a unique NoteId.
3. Create a Note with status ACTIVE.
4. Preserve the supplied content.
5. Return the new Note.

Persistence is not the responsibility of the Note entity.

## 6. Aggregate Boundary

The Note aggregate is independently consistent.

External application services must use the aggregate's public behavior to modify its state.

No relationships to User or Tag aggregates exist in this version.

## 7. Out of Scope

- Authentication and ownership
- Tagging
- Sharing
- Archiving behavior
- Deleting behavior
- Domain events
