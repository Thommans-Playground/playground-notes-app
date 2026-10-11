#!/usr/bin/env python3
"""Check the Note Management ontology.

Runs three groups of checks against docs/ontology/ont-note.ttl:

  lint          IDs are well formed and unique, rules have a rationale, links resolve
  constraints   the SHACL shapes accept valid Notes and reject invalid ones
  competency    the competency questions in the file header get their expected answers

Usage:
  uv run --with rdflib --with pyshacl tools/check_ontology.py

Exit status is the number of failed checks.
"""

import re
import sys
from pathlib import Path

from pyshacl import validate
from rdflib import OWL, RDF, RDFS, Graph, Namespace, URIRef

ROOT = Path(__file__).resolve().parent.parent
ONTOLOGY = ROOT / "docs" / "ontology" / "ont-note.ttl"

ID_PATTERN = re.compile(r"^ONT(-REL|-RULE)?-[A-Z]+-\d{3}$")

PREFIXES = (
    "@prefix : <http://example.org/notes#> .\n"
    "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n"
)

results: list[tuple[bool, str]] = []


def check(ok: bool, name: str, detail: str = "") -> None:
    results.append((ok, name))
    print(f"{'ok  ' if ok else 'FAIL'} {name}" + (f"  ({detail})" if detail and not ok else ""))


# --- lint -------------------------------------------------------------------

def lint(g: Graph, ns: Namespace) -> None:
    artifact_id, rationale, rule = ns["artifactId"], ns["rationale"], ns["rule"]

    ids = [(s, str(o)) for s, o in g.subject_objects(artifact_id)]
    values = [v for _, v in ids]
    check(all(ID_PATTERN.match(v) for v in values), "lint: every artifact ID is well formed",
          ", ".join(v for v in values if not ID_PATTERN.match(v)))
    duplicated = sorted({v for v in values if values.count(v) > 1})
    check(not duplicated, "lint: artifact IDs are unique", ", ".join(duplicated))

    rules = [s for s, v in ids if v.startswith("ONT-RULE-")]
    missing = [str(g.value(s, artifact_id)) for s in rules
               if g.value(s, rationale) is None or g.value(s, RDFS.comment) is None]
    check(not missing, "lint: every rule has a statement and a rationale", ", ".join(missing))

    bad_links = [str(o) for _, o in g.subject_objects(rule)
                 if not str(g.value(o, artifact_id) or "").startswith("ONT-RULE-")]
    check(not bad_links, "lint: every :rule link points to a rule", ", ".join(bad_links))

    unlabelled = [str(c) for c in g.subjects(RDF.type, OWL.Class)
                  if isinstance(c, URIRef) and (g.value(c, RDFS.label) is None
                                                 or g.value(c, RDFS.comment) is None)]
    check(not unlabelled, "lint: every concept has a label and a definition", ", ".join(unlabelled))

    incomplete = [str(p) for p in g.subjects(RDF.type, OWL.ObjectProperty)
                  if g.value(p, RDFS.domain) is None or g.value(p, RDFS.range) is None]
    check(not incomplete, "lint: every relationship has a domain and a range", ", ".join(incomplete))


# --- constraints ------------------------------------------------------------

def note(title: str, extra: str = "", status: str = ":Active") -> str:
    return (
        PREFIXES
        + f':t a :NormalizedTitle ; :text {title} . :i a :NoteIdentifier .\n'
        + f":n a :Note ; :hasIdentifier :i ; :hasTitle :t ; :hasStatus {status} {extra} ."
    )


CASES = [
    ("a Note with a valid Title conforms", note('"Shopping"'), True),
    ("a Title with inner spaces conforms", note('"a  b"'), True),
    ("a Note with one Content conforms", note('"x"', "; :hasContent :c") + " :c a :Content .", True),
    ("a blank Title is rejected", note('"   "'), False),
    ("an empty Title is rejected", note('""'), False),
    ("a Title with a leading space is rejected", note('" x"'), False),
    ("a Title with a trailing space is rejected", note('"x "'), False),
    ("an unknown status is rejected", note('"x"', status=":Foo"), False),
    ("a Note without a Title is rejected",
     PREFIXES + ":i a :NoteIdentifier . :n a :Note ; :hasIdentifier :i ; :hasStatus :Active .", False),
    ("a Note without an identifier is rejected",
     PREFIXES + ':t a :NormalizedTitle ; :text "x" . :n a :Note ; :hasTitle :t ; :hasStatus :Active .', False),
    ("a Note with two Contents is rejected",
     note('"x"', "; :hasContent :c1, :c2") + " :c1 a :Content . :c2 a :Content .", False),
]


def constraints(onto: Graph) -> None:
    for name, data, expected in CASES:
        conforms, _, _ = validate(
            Graph().parse(data=data, format="turtle"),
            shacl_graph=onto, data_graph_format="turtle", inference="none",
        )
        check(conforms == expected, f"constraints: {name}")


# --- competency questions ---------------------------------------------------

def names(onto: Graph, query: str) -> list[str]:
    rows = onto.query("PREFIX : <http://example.org/notes#> " + query)
    return sorted(str(r[0]).split("#")[1] for r in rows)


def competency(onto: Graph) -> None:
    check(names(onto, "SELECT ?s WHERE { ?s :isInitial true }") == ["Active"],
          "competency: CQ-1 a newly created Note is Active")
    check(names(onto, "SELECT ?s WHERE { :Archived :mayBecome ?s }") == ["Active", "Deleted"],
          "competency: CQ-2 an Archived Note may become Active or Deleted")
    check(names(onto, "SELECT ?s WHERE { :Deleted :mayBecome ?s }") == [],
          "competency: CQ-3 a Deleted Note may become nothing")
    # CQ-4 and CQ-5 (how many Titles and Contents) are answered by the constraints above.


def main() -> int:
    onto = Graph().parse(ONTOLOGY, format="turtle")
    ns = Namespace("http://example.org/notes#")
    lint(onto, ns)
    constraints(onto)
    competency(onto)
    failed = sum(1 for ok, _ in results if not ok)
    print(f"\n{len(results) - failed} passed, {failed} failed")
    return failed


if __name__ == "__main__":
    sys.exit(main())
