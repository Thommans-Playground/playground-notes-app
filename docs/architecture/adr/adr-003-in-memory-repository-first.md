# ADR-003: Start With an In-Memory Repository

**Status:** Proposed  
**Related:** ADR-001, UC-NOTE-001

## Context

UC-NOTE-001 needs a driven port to keep Notes. No non-functional requirement says how long Notes must last, so the persistence technology is open. Tests written first (TDD) benefit from fast, dependency-free adapters.

## Decision

The first driven adapter for `NoteRepository` keeps Notes in memory. A durable adapter is added when a durability requirement exists. Every adapter is checked by the same repository contract tests.

## Consequences

- Notes are lost when the process stops until a durable adapter exists.
- The domain and application layers do not change when the durable adapter is added.
- A durability requirement (REQ-NFR) must be written before a real database is chosen.
