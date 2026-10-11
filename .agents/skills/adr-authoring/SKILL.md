---
name: adr-authoring
description: Write or change an architecture decision record (ADR) in docs/architecture/adr/: decide whether a decision deserves one, number it, fill Context, Decision and Consequences, set its status, and link it from the design that relies on it. Use whenever a structural or technology choice is made or reversed (layers, ports, persistence, layout, libraries, bounded contexts), when a decision is found written only in a diagram or comment, or when asked to record, supersede, accept, or review an ADR.
---

# ADR Authoring

An ADR records one decision and the reason for it, so the reason survives after the people who made it have forgotten. It owns that decision. Other artifacts cite it by ID and never restate it.

## When to write one

Write an ADR when the choice is structural, hard to reverse, or likely to be questioned later: layers, port style, persistence technology, package layout, a library the domain depends on, splitting or merging bounded contexts. Do not write one for a choice a design diagram or the code already makes obvious and cheap to change.

A decision found only in a diagram note, a comment, or a conversation is an undocumented decision. Move it into an ADR and have the diagram cite the ID.

## Steps

1. **Check for an existing ADR** on the same topic in `docs/architecture/adr/`. Change that one, or supersede it, rather than adding a second.
2. **Take the next number** after the highest in use. Never reuse or renumber an ID, including a gap left by a retired one. File name: `adr-nnn-<slug>.md`.
3. **Write it** with these sections and nothing else:
   - Header: `Status` and `Related` (the IDs this decision responds to or depends on: ADRs, designs, use cases).
   - **Context**: the forces and constraints, in a few sentences. State what is not yet known.
   - **Decision**: what we do, in the present tense. One decision per ADR.
   - **Consequences**: what becomes easier, what becomes harder, and what must now be done (a requirement to write, a contract test to add).
4. **Set the status.** `Proposed` while it is open for challenge. `Accepted` once the work that relies on it has been implemented and verified. `Superseded by ADR-nnn` when replaced. Do not delete a superseded ADR.
5. **Link from the user, not into it.** The design or diagram that relies on the decision cites the ADR ID. The ADR does not list its dependents. Related IDs in the header point upstream or to peer decisions only.
6. **Keep it short.** If the Context needs more than a page, the decision is probably several decisions.

## Reviewing an ADR

- Does the Decision state one thing?
- Is the reason in Context, and is anything unknown said to be unknown?
- Do Consequences include the costs, not only the benefits?
- Is the status honest? An ADR relied on by shipped code that is still `Proposed` should be `Accepted`.

## Do not

- Write an ADR after the fact to justify code without a real reason. Record the actual reason or say there was none.
- Restate an ontology rule, a requirement, or a use case flow. Cite it.
- Edit an Accepted ADR to change its meaning. Supersede it.
