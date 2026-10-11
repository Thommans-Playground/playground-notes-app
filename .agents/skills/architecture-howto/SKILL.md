---
name: architecture-howto
description: Recipes for applying this project's architecture (DDD, hexagonal/onion with ports and adapters) when writing or changing backend code: add a driving or driven port, add an adapter, map errors across layers, fake a port in tests, write a repository contract test, and review a change for dependency-rule violations. Use whenever code is placed in domain/, application/ or adapters/, a port or adapter is added, or someone asks where something belongs. The decisions live in ADR-001 and ADR-004. This skill only says how to apply them.
---

# Architecture How-To

The architecture is decided in `docs/architecture/adr/adr-001-hexagonal-architecture.md` (layers, dependency rule) and `adr-004-backend-layout-and-ports.md` (layout, port style). Read them first. This skill gives recipes that follow from them and never restates them, so when an ADR changes, this skill still points at the truth.

These recipes were written before the first implementation. After UC-NOTE-001, correct anything that did not survive contact with the code.

## Where does it go?

Ask what the code is, in this order:

1. A rule about what a Note is or may do (an ontology rule or an invariant) → `domain/`, in the aggregate or a value object that the design specification names.
2. The steps of one use case, in order → an application service in `application/`.
3. Something the application needs from outside (keep, find, send) → a driven port in `application/ports/`.
4. A way for the outside to call the application → a driving port in `application/ports/`.
5. Translation to or from a technology (HTTP, MCP, a database) → an adapter in `adapters/driving/` or `adapters/driven/`.

If a piece of code seems to belong in two layers, it is doing two jobs. Split it.

## Recipes

**Add a driving port and service.** Define the port as a `Protocol` with one method per use case. Define the command as a plain dataclass. The service implements the port, takes its driven ports in its constructor, and has no framework imports.

**Add a driven port.** Define a `Protocol` in `application/ports/`, named for what the application needs (`NoteRepository`), not for a technology. Define the error a port may raise in `application/` (for example `NoteNotKept`), so adapters translate their own failures into it.

**Add a driven adapter.** Implement the port in `adapters/driven/<name>/`. Translate technology failures into the port's error. Put no domain rule in it. Start with the in-memory adapter (ADR-003).

**Add a driving adapter.** Build the command from the request, call the driving port, and map results and errors to the protocol's response. The mapping of each error to a status or message is the adapter's job, and is recorded in the design diagrams.

**Wire it up.** Construct adapters and services in one composition point at the edge (for example the FastAPI app factory). The domain and application layers never construct adapters.

**Fake a port in a test.** For unit tests of a service, pass a small fake or the in-memory adapter. For the failure path, pass a fake whose method raises the port's error. Never patch imports.

**Write a repository contract test.** One test class parameterized over every adapter of the port. Each adapter must pass the same tests, so a new adapter is accepted by running the existing contract against it.

**Cross a boundary with an error.** Domain errors (such as `InvalidTitle`) pass through the application layer unchanged and are mapped by the driving adapter. Application errors are raised by ports. Neither layer returns error strings.

## Review checklist for a change

- Does any module in `domain/` import from `application/` or `adapters/`? It must not.
- Does any module in `application/` import from `adapters/`? It must not.
- Does the domain import FastAPI, MCP, `rdflib`, or `pyshacl`? It must not.
- Does an adapter contain an `if` that decides a business outcome? Move it into the domain.
- Does a new port name a technology? Rename it for the need.
- Is the dependency rule enforced by an import-linter contract, and does it pass?

## Do not

- Restate the layers, the dependency rule, or the layout. Cite the ADR.
- Add an architecture decision here. Record it as an ADR (`adr-authoring`).
