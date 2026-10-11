---
name: use-case-verification
description: Run the Verification stage for a use case in this project: run every check, confirm each acceptance criterion is covered by passing tests at the levels the design promised, close or accept traceability gaps, and close the Kanban card. Use after Implementation is complete, when moving a card from Verification to Done, or when asked whether a use case is finished, verified, or ready to close.
---

# Use Case Verification

Verification does not write features. It answers one question with evidence: does the finished use case satisfy what Analysis and Design promised? Each left-leg stage has a matching check on the right (see the README, Mini V-cycle), and this stage confirms every one ran and passed. Report results as they are. A failing or skipped check is stated, not worked around.

## Steps

1. **Run the suites, one level at a time**, so a failure points at a layer: unit, integration, system, acceptance. Then the whole suite with coverage.
2. **Run the spec and architecture checks**:
   - `uv run --with rdflib --with pyshacl tools/check_ontology.py`
   - `uv run --with rdflib tools/ontology_to_puml.py --check`
   - `uv run --with rdflib tools/traceability.py` then `--check`
   - the import-linter dependency-rule contracts
3. **Read the traceability Gaps section.** For this use case, "Acceptance criteria with no tests" must be empty. Every other gap is closed, or accepted with a one-line reason recorded in the use case's Kanban note or an ADR. Do not hide a gap by editing the generated file.
4. **Compare against the Verification Mapping.** For each acceptance criterion, confirm tests exist at every level the mapping names (not just one), and that the alternative flows in the use case each have a system test.
5. **Triage failures by where the fault is**, then fix at the owner, not at the symptom:
   - Code wrong: back to Implementation, add a regression test first. Record a defect `BUG-<DOMAIN>-nnn` only if the fault escaped a prior stage.
   - Design wrong (mapping, port, enforcement): fix the design specification.
   - Requirement, ontology or use case wrong: fix the Analysis artifact and re-run its exit check.
   Then re-run this stage from step 1. This is the dotted "checks" line of the V-cycle made concrete.
6. **Close out.** Set the use case's artifacts from Draft to the next status (`Accepted`) and any `Proposed` ADRs it relied on, only where the checks above passed.

## Exit check

- All suites pass, and all spec and architecture checks pass.
- Every acceptance criterion of the use case has passing tests at each mapped level.
- No unexplained traceability gap remains for this use case.
- Report to the user: what ran, counts passed and failed, coverage, any accepted gaps.
- Update `docs/kanban.md`: move the card to Done.

## Do not

- Close a card on a green build alone. Green with no test for a criterion proves nothing about it.
- Weaken, skip, or delete a test to make the suite pass.
- Edit generated files (`traceability.*`, `ont-note-*.puml`) by hand.
- Add features. New behavior is a new card.
