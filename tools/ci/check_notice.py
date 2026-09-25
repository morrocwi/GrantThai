#!/usr/bin/env python3
"""tools/ci/check_notice.py

Guard: the one-line NOTICE constant (spec/output/notice_constant.txt) is
exactly one non-empty line, and it appears byte for byte in every file
that claims to reuse it: NOTICE, README.md, README.en.md, ai.json,
llms.txt, llms-full.txt and GRANTTHAI_STANDALONE.md. The primary render
template must place `{{ disclaimer }}` (the constant) as the first body
line.

Usage:
    python tools/ci/check_notice.py --root <path>
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REUSING_FILES = [
    "NOTICE",
    "README.md",
    "README.en.md",
    "ai.json",
    "llms.txt",
    "llms-full.txt",
    "GRANTTHAI_STANDALONE.md",
]
PRIMARY_TEMPLATE = "templates/nriis_submission.md.j2"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    violations = []

    const_path = root / "spec" / "output" / "notice_constant.txt"
    if not const_path.exists():
        print("notice guard: FAIL\n  - spec/output/notice_constant.txt is missing")
        return 1
    raw = const_path.read_text(encoding="utf-8")
    lines = raw.rstrip("\n").split("\n")
    if len(lines) != 1 or not lines[0].strip():
        violations.append("spec/output/notice_constant.txt must hold exactly one non-empty line")
    constant = lines[0]

    for rel in REUSING_FILES:
        path = root / rel
        if not path.exists():
            violations.append(f"{rel}: missing (it must carry the NOTICE constant)")
            continue
        if constant not in path.read_text(encoding="utf-8"):
            violations.append(f"{rel}: does not contain the NOTICE constant verbatim")

    tpl = root / PRIMARY_TEMPLATE
    if tpl.exists():
        text = tpl.read_text(encoding="utf-8")
        tlines = text.split("\n")
        fences = [i for i, line in enumerate(tlines) if line.strip() == "---"]
        body = tlines[fences[1] + 1:] if len(fences) >= 2 else []
        non_empty = [line.strip() for line in body if line.strip()]
        first_body_line = non_empty[0] if non_empty else ""
        if first_body_line != "{{ disclaimer }}":
            violations.append(f"{PRIMARY_TEMPLATE}: first body line must be '{{{{ disclaimer }}}}'")
    else:
        violations.append(f"{PRIMARY_TEMPLATE}: missing")

    if violations:
        print("notice guard: FAIL")
        for v in violations:
            print(f"  - {v}")
        return 1
    print("notice guard: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
