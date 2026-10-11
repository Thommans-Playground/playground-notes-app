---
name: ontology-authoring
description: Add or change concepts, relationships, rules, statuses, or lifecycle transitions in the Note Management ontology (docs/ontology/ont-note.ttl), then run its checks and regenerate its diagrams. Use whenever domain meaning changes, including during the ontology step of use case analysis.
---

# Ontology Authoring

The ontology (`docs/ontology/ont-note.ttl`) is the single source of truth for domain meaning: concepts, relationships, rules, and lifecycle. Other artifacts cite it by ID and never restate it. This skill is the procedure for changing it.

## Before you edit

1. Check whether the element already exists. List the IDs in use:
   `grep -o 'artifactId "[^"]*"' docs/ontology/ont-note.ttl | sort`
2. Use the ubiquitous language (`docs/architecture/ul-note-001-ubiquitous-language.md`) for labels. If the term is new, add it there as well.
3. IDs follow the README: `ONT-<DOMAIN>-nnn` for concepts, `ONT-REL-<DOMAIN>-nnn` for relationships, `ONT-RULE-<DOMAIN>-nnn` for rules. Take the next free number. Never reuse or renumber an ID.

## Adding an element

Keep the file's section order: concepts, relationships, statuses and lifecycle, rules, constraints.

**Concept** (`owl:Class`): give it `:artifactId`, `rdfs:label` (the ubiquitous language term), and `rdfs:comment` (a definition in domain terms). Use `rdfs:subClassOf` for specialization.

**Relationship** (`owl:ObjectProperty`): give it `:artifactId`, `rdfs:domain`, and `rdfs:range`. A relationship whose domain and range are the same class is drawn as a lifecycle in the state diagram.

**Attribute** (`owl:DatatypeProperty`): give it a domain and an XSD range. Prefer a concept with a relationship when the value has its own rules.

**Status or lifecycle change**: add the individual to the status enumeration, and add `:mayBecome` links. Mark the initial status with `:isInitial true`. Link the lifecycle rule with `:rule`.

**Rule** (an `owl:NamedIndividual`): give it `:artifactId`, `rdfs:comment` (the statement), and `:rationale` (why it exists). State a truth about a concept. Do not describe a procedure such as "trim the text"; describe the resulting state.

**Constraint**: when the rule is about the current shape of a Note, add a SHACL property shape, and link it to its rule with `:rule`. Rules about change over time cannot be expressed in SHACL. Link them with `:rule` from the element they govern, and verify them in the domain tests.

**Competency question**: when the change raises a question the ontology should answer, add it to the header comment and add a check for it in `tools/check_ontology.py`.

## Checks

Run all three, in this order:

```
uv run --with rdflib --with pyshacl tools/check_ontology.py
uv run --with rdflib tools/ontology_to_puml.py
uv run --with rdflib tools/ontology_to_puml.py --check
```

1. `check_ontology.py` lints the IDs and links, runs the SHACL constraint examples, and answers the competency questions. Add an example case for every new constraint, one that conforms and one that does not. Exit status is the number of failures; it must be 0.
2. `ontology_to_puml.py` regenerates `docs/ontology/ont-note-class.puml` and `ont-note-state.puml`.
3. `--check` confirms that the committed diagrams match the ontology.

## After the change

Search for the IDs you changed (`grep -rn "ONT-RULE-NOTE-002" docs`) and review every artifact that cites them: requirements, use cases, diagrams, and the design specification's enforcement table. A changed rule reopens the Kanban card of any use case that cites it.

## Do not

- Restate rule text, definitions, or the lifecycle in another artifact. Cite the ID.
- Put actions or procedures in the ontology. Those belong to use cases.
- Use programming types (`uuid`, `str | None`). Those belong to the design specification.
- Edit the generated diagrams by hand.
