#!/usr/bin/env python3
"""tools/ci/check_one_output.py

Guard: the one-input, one-output contract
(spec/contracts/one-input-one-output.md) holds structurally AND at runtime:
  1. Exactly one template under templates/ is tagged
     `output_kind: primary_submission`.
  2. spec/contracts/one-input-one-output.md and
     spec/output/nriis-submission.contract.md both exist and each names the
     other's path (cross-reference).
  3. Running `grantthai build` (via the Python API, in-process) against the
     shipped FICTIONAL worked example (examples/lecturer-no-ai/project.yaml)
     into a scratch directory produces exactly one file under build/, named
     NRIIS_SUBMISSION.md.

Usage:
    python tools/ci/check_one_output.py --root <path>
"""
from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
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

    example = root / "examples" / "lecturer-no-ai" / "project.yaml"
    if not example.exists():
        violations.append(f"{example.relative_to(root)} is missing; cannot run the renderer-output check")
    else:
        sys.path.insert(0, str(root / "src"))
        from grantthai import api_py as api  # noqa: E402

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            project = tmp_path / "project.yaml"
            shutil.copy(example, project)
            try:
                out = api.build(project, as_of="2026-09-25")
            except Exception as exc:  # noqa: BLE001
                violations.append(f"grantthai build raised on the FICTIONAL example: {exc!r}")
            else:
                build_dir = tmp_path / "build"
                names = sorted(p.name for p in build_dir.iterdir()) if build_dir.is_dir() else []
                if names != ["NRIIS_SUBMISSION.md"]:
                    violations.append(f"build/ under the scratch project holds {names!r}, expected exactly "
                                       "['NRIIS_SUBMISSION.md']")
                if out != build_dir / "NRIIS_SUBMISSION.md":
                    violations.append(f"grantthai build returned {out}, expected {build_dir / 'NRIIS_SUBMISSION.md'}")

    if violations:
        print("one-input-one-output guard: FAIL")
        for v in violations:
            print(f"  - {v}")
        return 1

    print("one-input-one-output guard: PASS (structural checks + renderer-output check on the FICTIONAL example)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
