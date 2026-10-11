---
name: use-case-design
description: Run the Design stage for a use case in this project: map the ontology to the domain model, name the ports, record decisions, and decide which tests cover each acceptance criterion. Use after Analysis is complete for a use case, or when moving a Kanban card from Analysis to Design.
---

# Use Case Design

Start only when the use case has passed its Analysis exit check. The architecture is hexagonal (ports and adapters) with DDD, as recorded in `docs/architecture/adr/adr-001-hexagonal-architecture.md`. The ontology owns domain meaning. Cite it and never restate it.

## Steps

1. **Domain model.** In `docs/architecture/des-<context>-nnn-<slug>.md` (and its `.puml`):
   - Map each new concept to an entity or a value object, and cite its `ONT` ID.
   - Map each new relationship to a typed attribute, and cite its `ONT-REL` ID.
   - Add every new or changed `ONT-RULE` to the enforcement table, saying what enforces it.
   - Add a domain invariant (`INV`) only for a condition the ontology cannot express. It cites the ontology rule it relates to.
   - Keep the diagram consistent with the document. Use composition for value objects the aggregate owns.
2. **Ports and design diagrams.** Name the driving port the use case is offered through, and any driven ports it needs. Respect the dependency rule: the domain imports nothing from the application or adapters, and the application imports no adapter. Draw them next to the use case as `design-<use case id>-<slug>-sequence.puml` (adapter, port, service, domain, driven port) and `design-<use case id>-<slug>-class.puml` (application and adapters; domain classes by name only).
3. **Decisions.** Record any significant choice as an ADR (`docs/architecture/adr/adr-nnn-<slug>.md`) with Context, Decision, and Consequences.
4. **Test mapping.** For each acceptance criterion, decide which tests cover it:
   - acceptance: the Gherkin scenario
   - system: through a driving adapter, one per use case flow
   - integration: an adapter against its port
   - unit (TDD): the domain and application layers

   Record the mapping in the design specification's Verification Mapping section, one table per use case. Tests carry their IDs as tags or markers when written. Do not write a separate test plan document.

## Exit check

- Every ontology rule the use case touches appears in the enforcement table.
- The driving port and the driven ports are named, and the design diagrams are drawn.
- Each acceptance criterion has its tests identified.
- Update `docs/kanban.md`: move the card to Implementation.

## Do not

- Put domain rules in adapters. They translate and delegate.
- Restate attributes, definitions, or rule text from the ontology. Map and cite them.
- Let verification-only libraries (such as `rdflib` and `pyshacl`) be imported by the domain. They are development dependencies used by tests.
- Use inline Mermaid for anything but a passing illustration. Analysis diagrams are PlantUML files; Mermaid never replaces them (see the README, Diagrams).
