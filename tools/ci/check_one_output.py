#!/usr/bin/env python3
"""tools/ci/check_one_output.py

Guard: the one-input, one-output contract
(spec/contracts/one-input-one-output.md) holds structurally.

Phase 0 checks (no renderer exists yet, so this is necessarily partial):
  1. Exactly one template under templates/ is tagged
     `output_kind: primary_submission`.
  2. spec/contracts/one-input-one-output.md and
     spec/output/nriis-submission.contract.md both exist and each names the
     other's path (cross-reference).

Once the renderer ships (v0.1+), a third check is added here: running
`grantthai build` against a fixture project produces exactly one file
under build/ named NRIIS_SUBMISSION.md (plus, only with --concept-note,
RESEARCH_CONCEPT_NOTE.md).

Usage:
    python tools/ci/check_one_output.py --root <path>
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    violations = []

    templates_dir = root / "templates"
    primary = []
    if templates_dir.exists():
        for path in templates_dir.glob("*.j2"):
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "output_kind: primary_submission" in text:
                primary.append(path.relative_to(root).as_posix())

    if len(primary) == 0:
        violations.append("no template tagged output_kind: primary_submission found under templates/")
    elif len(primary) > 1:
        violations.append(f"more than one template tagged output_kind: primary_submission: {primary}")

    contract = root / "spec" / "contracts" / "one-input-one-output.md"
    if not contract.exists():
        violations.append("spec/contracts/one-input-one-output.md is missing")

    output_contract = root / "spec" / "output" / "nriis-submission.contract.md"
    if not output_contract.exists():
        violations.append("spec/output/nriis-submission.contract.md is missing")

    if contract.exists() and output_contract.exists():
        if "spec/output/nriis-submission.contract.md" not in contract.read_text(encoding="utf-8"):
            violations.append("spec/contracts/one-input-one-output.md does not reference spec/output/nriis-submission.contract.md")
        if "spec/contracts/one-input-one-output.md" not in output_contract.read_text(encoding="utf-8"):
            violations.append("spec/output/nriis-submission.contract.md does not reference spec/contracts/one-input-one-output.md")

    if violations:
        print("one-input-one-output guard: FAIL")
        for v in violations:
            print(f"  - {v}")
        return 1

    print("one-input-one-output guard: PASS (Phase 0 structural checks only; renderer output check ships v0.1)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
