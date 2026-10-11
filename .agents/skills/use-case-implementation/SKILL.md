---
name: use-case-implementation
description: Run the Implementation stage for a use case in this project: write the tests first (BDD acceptance, then TDD unit, integration and system), then the domain, application and adapter code, inside the hexagonal layout. Use after Design is complete for a use case, when moving a Kanban card from Implementation toward Verification, or whenever backend code or tests are written or changed. Use it even for a small change to backend code, because the order of work and the dependency rule apply to every change.
---

# Use Case Implementation

Start only when the use case has passed its Design exit check. The design specification (`docs/architecture/des-*`) and the design diagrams say what to build. The ontology owns domain meaning. Code realizes it and never redefines it. Layout and port style are in ADR-004. Layers and the dependency rule are in ADR-001.

Tests come first because they are the executable form of the acceptance criteria and the Verification Mapping. Code written before a failing test has nothing proving it is needed.

## Steps

1. **Set up once.** If `backend/tests/` and the acceptance-test mechanism do not exist yet, create them before any feature code, and record the choice as an ADR (`adr-nnn-acceptance-test-mechanism.md`, with Context, Decision, Consequences). Defaults to propose:
   - Extract the fenced Gherkin blocks from `docs/requirements/functional-requirements.md` at test time into a git-ignored temporary directory, and run them with `pytest-bdd`. ADR-004 forbids committed `.feature` files, so the Markdown stays the only copy.
   - Add the dependency rule as an import-linter contract (domain imports nothing inward-out, application imports no adapter) so it fails the build.
   - Add `pytest-bdd` and `import-linter` as dev dependencies only.
2. **Read the Verification Mapping** for the use case in the design specification. It lists, per acceptance criterion, which tests exist at which level. Build a checklist from it. Write nothing that is not on it, and if a needed test is missing from it, fix the mapping first (it is owned by Design).
3. **Acceptance tests (BDD, outside-in).** Write step definitions for the scenarios. They drive the application only through the driving port, with in-memory driven adapters (ADR-003). They fail first. They stay red until the use case works end to end.
4. **Inside-out, one red-green-refactor cycle at a time**, in this order:
   1. Domain (unit tests): value objects, then the aggregate. Each ontology rule is enforced where the enforcement table says. A test per rule, carrying the rule's AC ID.
   2. Application (unit tests): the service, with a fake or in-memory driven port. Include the failure path (a failing repository is reported, nothing is returned).
   3. Driven adapters (integration tests): each adapter against its port, using the shared contract tests so every adapter is held to the same behavior (ADR-003).
   4. Driving adapters (system tests): HTTP or MCP, one per use case flow including alternative flows.
5. **Tag every test with the ID it covers**: `@pytest.mark.ac("REQ-FR-NOTE-001/AC-003")` (one or more). The tag keeps each test tied to its criterion, and lets a later tool trace them.
6. **Refactor with the suite green.** Keep adapters thin: they translate and delegate. A domain rule found in an adapter or the service moves into the domain.
7. **Spec feedback.** If implementation shows the spec is wrong or incomplete, stop and fix the owner artifact first (ontology, requirement, use case, or design). Search for the ID (`grep -rn <ID> docs backend`) to find what else cites it, regenerate its checks, then continue. Do not patch around it in code or tests.

## Exit check

- Every test in the Verification Mapping for this use case exists, is tagged, and passes.
- Unit tests run with no web server and no database.
- The import-linter contracts pass (the dependency rule holds).
- No domain code imports `rdflib`, `pyshacl`, FastAPI or MCP.
- Update `docs/kanban.md`: move the card to Verification.

## Do not

- Write production code without a failing test that demands it.
- Restate ontology definitions or rule text in code comments or docstrings. Cite the ID.
- Put domain rules in adapters, or let the application import an adapter.
- Add behavior for another use case. It is designed and implemented with its own card.
- Commit `.feature` files or a second copy of the scenarios.
