# ADR-004: Backend Package Layout and Port Style

**Status:** Proposed  
**Related:** ADR-001

## Context

ADR-001 defines the layers and leaves the package layout and port style to Design. The acceptance criteria are written as Gherkin in the requirements document, and acceptance tests must run them without keeping a second copy.

## Decision

**Layout** under `backend/src/backend/`:

- `domain/`: aggregates, value objects, and domain errors
- `application/`: application services, and `ports/` for the driving and driven ports
- `adapters/driving/` and `adapters/driven/`: one package per adapter

**Port style.** Ports are `typing.Protocol` classes owned by the application layer. A domain error is defined in `domain/`. An application error, such as one raised by a port, is defined in `application/`.

**Tests** live in `backend/tests/` under `unit/`, `integration/`, `system/`, and `acceptance/`. Acceptance tests read their scenarios from the fenced Gherkin blocks in `docs/requirements/functional-requirements.md`. No `.feature` files are committed.

## Consequences

- The dependency rule can be checked by import analysis on these packages.
- The mechanism for reading Gherkin from the Markdown is decided in Implementation.
