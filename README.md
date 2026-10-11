# playground-notes-app

A notes application built to practise a specification-driven, test-first method: a mini V-cycle with BDD and TDD, DDD, and a hexagonal (ports and adapters) architecture.

## Principles

1. **One owner per fact.** Every statement lives in exactly one artifact. Others refer to it by ID and do not paraphrase it.
2. **References point upstream.** A downstream artifact names the upstream artifact it realizes. Upstream artifacts do not list their dependents.
3. **One language.** Terms follow the Ubiquitous Language (UL-NOTE-001).

## Naming

An artifact ID is `<TYPE>-<DOMAIN>-<NUMBER>`, or `<TYPE>-<SUBTYPE>-<DOMAIN>-<NUMBER>` for types with subtypes. Records that are not tied to a domain omit it (`ADR-001`).

| Artifact | Prefix | Example |
|---|---|---|
| Functional requirement | `REQ-FR` | `REQ-FR-NOTE-001` |
| Non-functional requirement | `REQ-NFR` | `REQ-NFR-NOTE-001` |
| Use case | `UC` | `UC-NOTE-001` |
| Analysis diagram | `ANA` | `ANA-NOTE-001` |
| Ubiquitous language | `UL` | `UL-NOTE-001` |
| Ontology concept | `ONT` | `ONT-NOTE-001` |
| Ontology relationship | `ONT-REL` | `ONT-REL-NOTE-001` |
| Ontology rule | `ONT-RULE` | `ONT-RULE-NOTE-001` |
| Domain invariant | `INV` | `INV-NOTE-001` |
| Architecture decision | `ADR` | `ADR-001` |
| Design specification | `DES` | `DES-NOTE-001` |
| Test case | `TC` | `TC-NOTE-001` |
| Test suite | `TS` | `TS-NOTE-001` |
| Defect | `BUG` | `BUG-NOTE-001` |

An ontology rule (`ONT-RULE`) is a structural truth about a concept. A domain invariant (`INV`) is a condition the aggregate must protect that the ontology cannot express, and it refers to the ontology rule it relates to and never restates it.

**Files.** A document that holds one artifact is named `<id>-<slug>`, in lowercase (`uc-note-001-create-note.md`). A document that holds many artifacts has a plain name (`functional-requirements.md`, `ont-note.ttl`).

## Who owns what

| Artifact | Owns | Path |
|---|---|---|
| Functional requirements | What the User needs, with Gherkin acceptance criteria | docs/requirements/functional-requirements.md |
| Non-functional requirements | Quality needs | docs/requirements/non-functional-requirements.md |
| Ontology | What exists and what is always true of it: concepts, relationships, rules, lifecycle | docs/ontology/ont-note.ttl |
| Use cases | Interaction: steps and failure flows | docs/use-cases/ |
| Analysis diagrams | A view of one use case | docs/architecture/ana-* |
| Ubiquitous language | How we talk | docs/architecture/ul-note-001-ubiquitous-language.md |
| Design specification | Aggregates, entities, value objects, and what enforces each ontology rule | docs/architecture/des-note-001-note-aggregate.* |
| Architecture decisions | Layers, ports, adapters, dependency rule, context map | docs/architecture/adr-* |
| Kanban | Where each use case stands | docs/kanban.md |

## Mini V-cycle

Each stage on the left has a matching check on the right.

| Stage | Produces | Verified by |
|---|---|---|
| Analysis | Requirements, ontology, use cases, language | Acceptance tests: the Gherkin criteria, run as BDD scenarios. System tests: one per use case flow, through a driving adapter. |
| Design | Domain model, ports, adapters | Integration tests: each adapter against its port |
| Implementation | Code, written test-first | Unit tests (TDD) of the domain and application layers |
| Verification | | Runs the checks above and closes the use case |

A use case moves across the Kanban stage by stage and is done when its acceptance criteria pass.
