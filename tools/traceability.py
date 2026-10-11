#!/usr/bin/env python3
"""Generate the traceability matrix from the IDs the documents cite.

Writes docs/traceability.md (a matrix) and docs/traceability.puml (a diagram of the same
connections). Both are views: the ontology, requirements,
use cases, design specification, and tests own the content, and this file only
shows how they connect and where the connections are missing.

What it reads
  docs/ontology/ont-note.ttl                       rules, and the elements each rule governs
  docs/requirements/functional-requirements.md     acceptance criteria and the rules each cites
  docs/use-cases/uc-*.md                           which use cases cite which rules and criteria
  docs/architecture/des-*.md                       the enforcement table and the verification mapping
  backend/tests/                                   tests that carry an acceptance criterion ID

Usage
  uv run --with rdflib tools/traceability.py            write the matrix
  uv run --with rdflib tools/traceability.py --check    fail if it is out of date,
                                                        or if a document cites an unknown ontology ID
  uv run --with rdflib tools/traceability.py --check --require-tests
                                                        also fail if an acceptance criterion has no tests
  uv run --with rdflib tools/traceability.py --impact ID
                                                        list every artifact that cites an ID
"""

import argparse
import re
import sys
import textwrap
from pathlib import Path

from rdflib import OWL, RDF, RDFS, Graph, Namespace, URIRef
from rdflib.namespace import SH

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
ONTOLOGY = DOCS / "ontology" / "ont-note.ttl"
OUTPUT = DOCS / "traceability.md"
DIAGRAM = DOCS / "traceability.puml"

ONT_ID = re.compile(r"\bONT(?:-REL|-RULE)?-[A-Z]+-\d{3}\b")
RULE_ID = re.compile(r"\bONT-RULE-[A-Z]+-\d{3}\b")
AC_ID = re.compile(r"\bREQ-[A-Z]+-[A-Z]+-\d{3}/AC-\d{3}\b")
UC_ID = re.compile(r"\bUC-[A-Z]+-\d{3}\b")
AC_TAG = re.compile(r"@(REQ-[A-Z]+-[A-Z]+-\d{3}/AC-\d{3})")


def read(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def cell(items) -> str:
    items = sorted(set(items))
    return "<br>".join(items) if items else "none"


# --- ontology ---------------------------------------------------------------

def ontology_rules():
    """Return ({rule id: statement}, {rule id: [elements it governs]}, {all ontology ids})."""
    g = Graph().parse(ONTOLOGY, format="turtle")
    ns = Namespace(str(dict(g.namespaces())[""]))
    aid, rule = ns["artifactId"], ns["rule"]

    def label(node):
        return str(g.value(node, RDFS.label) or str(node).removeprefix(str(ns)))

    ids = {str(o) for o in g.objects(None, aid)}
    statements = {
        str(g.value(r, aid)): str(g.value(r, RDFS.comment))
        for r in g.subjects(RDF.type, OWL.NamedIndividual)
        if str(g.value(r, aid) or "").startswith("ONT-RULE-")
    }

    governs: dict[str, list[str]] = {r: [] for r in statements}
    for shape in g.subjects(RDF.type, SH.NodeShape):
        target = g.value(shape, SH.targetClass)
        for constraint in g.objects(shape, SH.property):
            path = str(g.value(constraint, SH.path)).removeprefix(str(ns))
            for r in g.objects(constraint, rule):
                governs[str(g.value(r, aid))].append(f"{label(target)}.{path} (constraint)")
    for subject, r in g.subject_objects(rule):
        if isinstance(subject, URIRef):
            governs[str(g.value(r, aid))].append(f"{label(subject)} (lifecycle)")
    return statements, governs, ids


# --- documents --------------------------------------------------------------

def acceptance_criteria():
    """{ac id: set of rule ids cited in its scenario}"""
    text = read(DOCS / "requirements" / "functional-requirements.md")
    tags = list(AC_TAG.finditer(text))
    found = {}
    for i, tag in enumerate(tags):
        end = tags[i + 1].start() if i + 1 < len(tags) else len(text)
        found[tag.group(1)] = set(RULE_ID.findall(text[tag.end():end]))
    return found


def use_cases():
    """{use case id: file text}"""
    found = {}
    for path in sorted((DOCS / "use-cases").glob("uc-*.md")):
        text = path.read_text()
        match = UC_ID.search(text)
        if match:
            found[match.group(0)] = text
    return found


def design():
    """({rule id: enforcement}, set of ac ids with a verification mapping row)"""
    enforcement, mapped = {}, set()
    for path in sorted((DOCS / "architecture").glob("des-*.md")):
        for line in path.read_text().splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 2 and RULE_ID.fullmatch(cells[0]):
                enforcement[cells[0]] = cells[1]
            if line.startswith("|") and AC_ID.match(cells[0]):
                mapped.add(cells[0])
    return enforcement, mapped


def tests():
    """{ac id: [test files]}"""
    found: dict[str, list[str]] = {}
    for path in sorted((ROOT / "backend" / "tests").rglob("*.py")):
        for ac in set(AC_ID.findall(path.read_text())):
            found.setdefault(ac, []).append(str(path.relative_to(ROOT)))
    return found


def cited_ontology_ids() -> dict[str, set[str]]:
    """{ontology id: files citing it}, excluding the ontology folder and this output."""
    found: dict[str, set[str]] = {}
    for path in sorted(DOCS.rglob("*")):
        if not path.is_file() or path in {OUTPUT, DIAGRAM} or ONTOLOGY.parent in path.parents:
            continue
        if path.suffix not in {".md", ".puml"}:
            continue
        for ident in ONT_ID.findall(path.read_text()):
            found.setdefault(ident, set()).add(str(path.relative_to(ROOT)))
    return found


# --- output -----------------------------------------------------------------

def build() -> tuple[str, str, list[str]]:
    statements, governs, known_ids = ontology_rules()
    acs = acceptance_criteria()
    ucs = use_cases()
    enforcement, mapped = design()
    test_files = tests()
    cited = cited_ontology_ids()

    rule_cited_by_ac = {r: [ac for ac, rules in acs.items() if r in rules] for r in statements}
    rule_cited_by_uc = {r: [uc for uc, text in ucs.items() if r in text] for r in statements}
    ac_cited_by_uc = {ac: [uc for uc, text in ucs.items() if ac in text] for ac in acs}

    lines = [
        "# Traceability Matrix",
        "",
        "<!-- GENERATED by tools/traceability.py. Do not edit. -->",
        "",
        "A view of how the artifacts connect. Regenerate it with `uv run --with rdflib tools/traceability.py`.",
        "",
        "## Ontology rules",
        "",
        "| Rule | Statement | Governs | Cited by criteria | Cited by use cases | Enforced by (design) |",
        "|---|---|---|---|---|---|",
    ]
    for rule in sorted(statements):
        lines.append(
            f"| {rule} | {statements[rule]} | {cell(governs[rule])} | {cell(rule_cited_by_ac[rule])} "
            f"| {cell(rule_cited_by_uc[rule])} | {enforcement.get(rule, 'none')} |"
        )

    lines += [
        "",
        "## Acceptance criteria",
        "",
        "| Criterion | Rules cited | Use cases | In design mapping | Tests |",
        "|---|---|---|---|---|",
    ]
    for ac in sorted(acs):
        lines.append(
            f"| {ac} | {cell(acs[ac])} | {cell(ac_cited_by_uc[ac])} "
            f"| {'yes' if ac in mapped else 'no'} | {cell(test_files.get(ac, []))} |"
        )

    gaps = {
        "Rules cited by no acceptance criterion": [r for r in sorted(statements) if not rule_cited_by_ac[r]],
        "Rules with no enforcement in the design": [r for r in sorted(statements) if r not in enforcement],
        "Acceptance criteria cited by no use case": [a for a in sorted(acs) if not ac_cited_by_uc[a]],
        "Acceptance criteria missing from the design mapping": [a for a in sorted(acs) if a not in mapped],
        "Acceptance criteria with no tests": [a for a in sorted(acs) if a not in test_files],
    }
    lines += ["", "## Gaps", ""]
    for title, items in gaps.items():
        lines.append(f"- **{title}:** {', '.join(items) if items else 'none'}")

    unknown = sorted(i for i in cited if i not in known_ids)
    lines += ["", "## Unknown ontology IDs", ""]
    if unknown:
        lines += [f"- {i}, cited in {', '.join(sorted(cited[i]))}" for i in unknown]
    else:
        lines.append("None. Every ontology ID cited in the documents exists in the ontology.")
    lines.append("")

    # --- diagram ---
    def alias(prefix: str, ident: str) -> str:
        return prefix + re.sub(r"\W", "_", ident)

    gap = "#FFF1F2;line:E11D48"
    puml = [
        "@startuml traceability",
        "!include architecture/theme.puml",
        "title Traceability - Note Management",
        "",
        "' GENERATED by tools/traceability.py. Do not edit.",
        "",
        "left to right direction",
        "skinparam rectangle {",
        "  BackgroundColor #FFFFFF",
        "  BorderColor #475569",
        "  FontColor #0F172A",
        "}",
        "",
        'package "Ontology rules" <<Domain>> {',
    ]
    for rule in sorted(statements):
        puml.append(f'  rectangle "{rule}" as {alias("R_", rule)}' + ("" if rule_cited_by_ac[rule] else f" {gap}"))
    puml += ["}", "", 'package "Acceptance criteria" {']
    for ac in sorted(acs):
        no_tests = ac not in test_files
        puml.append(f'  rectangle "{ac}" as {alias("A_", ac)}' + (f" {gap}" if no_tests else ""))
    puml += ["}", "", 'package "Use cases" {']
    for uc in sorted(ucs):
        puml.append(f'  rectangle "{uc}" as {alias("U_", uc)}')
    puml += ["}", "", 'package "Design" <<Application>> {']
    for rule in sorted(enforcement):
        text = "\\n".join(textwrap.wrap(enforcement[rule], 30))
        puml.append(f'  rectangle "{text}" as {alias("D_", rule)}')
    puml += ["}", "", 'package "Tests" {']
    for name in sorted({t for files in test_files.values() for t in files}):
        puml.append(f'  rectangle "{name}" as {alias("T_", name)}')
    if not test_files:
        puml.append(f'  rectangle "no tests yet" as NoTests {gap}')
    puml += ["}", ""]
    for rule in sorted(statements):
        for ac in rule_cited_by_ac[rule]:
            puml.append(f'{alias("R_", rule)} --> {alias("A_", ac)}')
        if rule in enforcement:
            puml.append(f'{alias("R_", rule)} --> {alias("D_", rule)}')
    for ac in sorted(acs):
        for uc in ac_cited_by_uc[ac]:
            puml.append(f'{alias("A_", ac)} --> {alias("U_", uc)}')
        for name in test_files.get(ac, []):
            puml.append(f'{alias("A_", ac)} --> {alias("T_", name)}')
    # Keep the columns in order: tests sit to the right of the use cases.
    first_use_case = alias("U_", sorted(ucs)[0]) if ucs else None
    first_test = alias("T_", sorted({t for files in test_files.values() for t in files})[0]) if test_files else "NoTests"
    if first_use_case:
        puml.append(f"{first_use_case} -[hidden]-> {first_test}")
    puml += [
        "",
        "legend right",
        "  Arrows run from a source of truth to the artifacts that cite it or enforce it.",
        "  Red marks a gap: a rule no criterion cites, or a criterion with no tests.",
        "endlegend",
        "",
        "@enduml",
        "",
    ]
    return "\n".join(lines), "\n".join(puml), unknown


def impact(ident: str) -> int:
    """Print every file that cites an ID: the artifacts to revisit when its owner changes."""
    pattern = re.compile(re.escape(ident) + r"(?![\w-])")
    skip = {OUTPUT, DIAGRAM}
    roots = [DOCS, ROOT / "backend", ROOT / ".agents", ROOT / "README.md"]
    hits = []
    for root in roots:
        files = [root] if root.is_file() else sorted(root.rglob("*"))
        for path in files:
            if not path.is_file() or path in skip or ".venv" in path.parts or "__pycache__" in path.parts:
                continue
            try:
                lines = path.read_text().splitlines()
            except UnicodeDecodeError:
                continue
            numbers = [n for n, line in enumerate(lines, 1) if pattern.search(line)]
            if numbers:
                hits.append((str(path.relative_to(ROOT)), numbers))
    if not hits:
        print(f"{ident} is not cited anywhere")
        return 1
    for name, numbers in hits:
        print(f"{name}: lines {', '.join(map(str, numbers))}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true",
                        help="fail if the matrix is out of date or cites an unknown ontology ID")
    parser.add_argument("--require-tests", action="store_true",
                        help="with --check, also fail if an acceptance criterion has no tests")
    parser.add_argument("--impact", metavar="ID",
                        help="list every file that cites ID, to see what to revisit before changing its owner")
    args = parser.parse_args()

    if args.impact:
        return impact(args.impact)

    matrix, diagram, unknown = build()
    outputs = {OUTPUT: matrix, DIAGRAM: diagram}
    if not args.check:
        for path, content in outputs.items():
            path.write_text(content)
            print(f"wrote {path.relative_to(ROOT)}")
        return 0

    problems = [
        f"{path.relative_to(ROOT)} is out of date, regenerate with tools/traceability.py"
        for path, content in outputs.items()
        if not path.exists() or path.read_text() != content
    ]
    problems += [f"unknown ontology ID cited: {i}" for i in unknown]
    if args.require_tests:
        problems += [f"no tests for {ac}" for ac in sorted(acceptance_criteria()) if ac not in tests()]
    for problem in problems:
        print(problem)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
