#!/usr/bin/env python3
"""Run every check for the project in one command.

This is the gate behind each Kanban exit check. A stage can move on when this passes.

  spec           ontology lint, SHACL constraints and competency questions
  diagrams       the generated ontology diagrams are current
  traceability   the matrix is current and cites no unknown ontology ID
  code           the pytest suites, if backend/tests exists
  architecture   the import-linter contracts, if any are configured

Usage
  uv run tools/check.py            Analysis and Design gate: spec, diagrams, traceability
  uv run tools/check.py --verify   Verification gate: also requires tests for every criterion
                                   and runs the code and architecture checks
"""

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "backend"


def uv(*args: str, withs: tuple[str, ...] = ()) -> list[str]:
    command = ["uv", "run"]
    for package in withs:
        command += ["--with", package]
    return command + list(args)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--verify", action="store_true",
                        help="Verification gate: require tests for every criterion; run code and architecture checks")
    args = parser.parse_args()

    traceability = [str(ROOT / "tools" / "traceability.py"), "--check"]
    if args.verify:
        traceability.append("--require-tests")

    checks = [
        ("spec", uv(str(ROOT / "tools" / "check_ontology.py"), withs=("rdflib", "pyshacl"))),
        ("diagrams", uv(str(ROOT / "tools" / "ontology_to_puml.py"), "--check", withs=("rdflib",))),
        ("traceability", uv(*traceability, withs=("rdflib",))),
    ]
    if args.verify:
        if (BACKEND / "tests").is_dir():
            checks.append(("code", uv("--project", str(BACKEND), "pytest", "--cov", str(BACKEND / "src"))))
        else:
            checks.append(("code", None))
        if "importlinter" in (BACKEND / "pyproject.toml").read_text():
            checks.append(("architecture", uv("--project", str(BACKEND), "lint-imports")))
        else:
            checks.append(("architecture", None))

    failed = []
    for name, command in checks:
        if command is None:
            print(f"FAIL {name}: nothing to run (no backend/tests, or no import-linter contract)")
            failed.append(name)
            continue
        print(f"--- {name}")
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        tail = (result.stdout + result.stderr).strip().splitlines()[-8:]
        if result.returncode == 0:
            print(f"ok   {name}")
        else:
            print("\n".join(tail))
            print(f"FAIL {name}")
            failed.append(name)

    print()
    print("all checks passed" if not failed else f"failed: {', '.join(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
