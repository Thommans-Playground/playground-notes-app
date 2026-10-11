---
name: use-case-analysis
description: Run the Analysis stage for a use case in this project: requirement, ontology, ubiquitous language, use case, and analysis diagrams. Use when starting or changing a use case, or when moving a Kanban card out of Backlog into Analysis.
---

# Use Case Analysis

Follow these steps in order. The ontology (`docs/ontology/ont-<context>.ttl`) is the single source of truth for domain meaning. Cite it by ID and never restate it. ID and file naming conventions are in the README.

## Steps

1. **Requirement.** In `docs/requirements/functional-requirements.md`, write the need, the requirement, and the acceptance criteria as Gherkin scenarios. Tag each scenario with its AC ID (`@REQ-FR-<CTX>-nnn/AC-nnn`). Do not state domain rules here. Cite them by ID.
2. **Ontology first.** For every noun, relationship, rule, and status change the use case needs, check whether the ontology already has it. If not, add it with the `ontology-authoring` skill, which also runs the ontology checks and regenerates its diagrams. Nothing may cite an ID before it exists.
3. **Language.** In `docs/architecture/ul-<context>-nnn-ubiquitous-language.md`, add any new verb or term to the narrative, and update the words we do not use. Do not define terms there. The ontology owns definitions.
4. **Use case.** Create `docs/use-cases/uc-<context>-nnn-<slug>.md` with Goal, Primary Actor, Preconditions, Main Flow, Alternative Flows, and Postconditions.
   - Cite ontology rules in the steps by ID.
   - Each alternative flow states the step where it branches and cites the AC it satisfies.
   - Use the ubiquitous language.
5. **Analysis diagrams.** Next to the use case, name them `analysis-<use case id>-<slug>-<kind>.puml`.
   - `sequence`: system level, User and the system only, alternative flows as `alt` fragments, steps citing rule IDs. Required.
   - `class`: only the concepts the use case touches, with `ONT` and `ONT-REL` IDs. It is an excerpt of the generated `docs/ontology/ont-note-class.puml` and adds nothing to the ontology. Regenerate the ontology diagrams after any ontology change. Required.
   - `activity`: only when the flow has something the sequence diagram cannot show, such as loops, parallel branches, or many nested decisions. Do not draw it for a simple flow, because it would redraw the use case.
   - No boundary, control, or repository classes. Design decides those.
6. **Review.** Regenerate the traceability matrix (`uv run --with rdflib tools/traceability.py`) and read its Gaps section. Then check each of these:
   - Every new rule is cited by at least one acceptance criterion.
   - Every acceptance criterion is covered by a step or an alternative flow.
   - No rule text is restated in the requirement, use case, or diagrams.
   - Every cited ID exists in the ontology.
   - Terms follow the ubiquitous language.

## Exit check

- The ontology checks pass and its generated diagrams are current (see `ontology-authoring`).
- `tools/traceability.py --check` passes, and every gap in `docs/traceability.md` for this use case is closed or accepted.
- The requirement and the use case are reviewed.
- Update `docs/kanban.md`: move the card to Design.

## Do not

- Restate a rule, definition, or lifecycle that the ontology owns.
- Choose entities, value objects, ports, or adapters. That is the Design stage (`use-case-design`).
- Add back-links from upstream artifacts to their dependents.
- Use inline Mermaid for anything but a passing illustration. Analysis diagrams are PlantUML files; Mermaid never replaces them (see the README, Diagrams).
