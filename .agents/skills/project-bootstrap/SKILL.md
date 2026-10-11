---
name: project-bootstrap
description: Start a new project on this methodology (ontology, requirements, use cases, DDD, hexagonal architecture, BDD and TDD, mini V-cycles on a Kanban) by copying the method, naming the first bounded context, recording the architecture as ADRs, laying out the backend, and setting up the checks. Use when the user begins a new project or repository, wants to reuse this methodology elsewhere, or asks how to set up the playground-notes-app approach for another codebase.
---

# Project Bootstrap

Use this once per project, before the first use case. The methodology is proven only as far as the Notes app has taken it, so treat what you copy as a starting point and correct it from experience. Do this with the user, because the architecture and the first bounded context are their decisions.

## Steps

1. **Ask what is not obvious.** The domain and its first bounded context name, the language and framework, who or what will call the system (HTTP, MCP, CLI), and whether persistence has a durability requirement yet. Do not guess these.
2. **Copy the method, not the domain.** From playground-notes-app copy `README.md` (rewrite its title and examples), `.agents/skills/` (with `.claude/skills` as a symlink to it), `docs/kanban.md`, and `tools/`. Do not copy the Notes ontology, requirements, use cases, or design.
3. **Rename the context.** The tools and skills hard-code the Notes context: `ont-note.ttl`, the `NOTE` domain code, and `Note Management`. Replace them with the new context's names throughout, then run the tools to prove nothing was missed. If a name is left behind, treat it as a bug to fix once in the template.
4. **Seed the docs.** Create the empty owners from the README's ownership table: `docs/requirements/`, `docs/ontology/`, `docs/use-cases/`, `docs/architecture/` (with `adr/`), and a Kanban with the first use cases in Backlog.
5. **Record the architecture as ADRs** (use `adr-authoring`). At minimum: the style and dependency rule, the backend layout and port style, and the first persistence choice. Reuse the Notes ADRs as drafts only where the user agrees.
6. **Lay out the backend** as the layout ADR says, with empty `domain/`, `application/`, `adapters/`, and `tests/{unit,integration,system,acceptance}/`. Add the dev dependencies for tests, BDD, coverage, and the dependency rule.
7. **Enforce the dependency rule from the start.** Add the import-linter contracts as soon as the packages exist, so the first violation fails the build.
8. **Run the checks and commit.** Run the project's check command, fix what the renaming broke, and commit the skeleton before the first use case so its diff is readable.
9. **Start the first use case** with `use-case-analysis`.

## Lean first, add later

Do not copy every tool for its own sake. Start with what the first use case will use. Add the traceability tooling, diagram generation, and extra skills when there is something for them to check, not before.

## Do not

- Copy domain artifacts from another project. Their rules are not this project's rules.
- Skip recording the architecture. A layout that exists only in the code has no reason attached.
- Rename a context by search-and-replace without running the checks afterwards.
