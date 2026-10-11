# ADR-001: Hexagonal Architecture

**Status:** Accepted  
**Related Design:** DES-NOTE-001

## Context

The application has domain rules that must be testable without a web server or database, and it will be reached through more than one interface (HTTP and MCP). The domain is designed with DDD.

## Decision

Use the hexagonal architecture (ports and adapters), organized as onion layers. All dependencies point inward.

### Layers

From the inside out:

**Domain**
Aggregates, entities, value objects, and the rules they enforce (DES-NOTE-001). Depends on nothing.

**Application**
One application service per use case. It coordinates the domain and uses ports to reach the outside world. Depends on the domain only.

**Ports**
Interfaces owned by the application layer.
- Driving ports are how the outside asks the application to do something. Each use case is offered through one.
- Driven ports are what the application needs from the outside, such as keeping and finding Notes.

**Adapters**
Implementations that connect the outside world to the ports.
- Driving adapters turn an external request into a call on a driving port. Examples: HTTP (FastAPI), MCP.
- Driven adapters implement a driven port against a technology. Example: persistence.

### Dependency rule

- Domain code does not import application, port, or adapter code.
- Application code does not import adapter code.
- Adapters contain no domain rules. They translate and delegate.

## Consequences

- The domain and application layers can be exercised without a web server or a database.
- An adapter can be replaced without touching the domain or application.
- Libraries used only for verification, such as those that read the ontology, are development dependencies and are never imported by the domain.

## Decided Later

These are settled in the Design stage of each use case:

- The driving and driven ports for each use case
- The persistence technology
- The package layout in the backend
