#!/usr/bin/env python3
"""tools/ci/check_no_hardcoded_rules.py

Guard: fund-call facts (agency acronyms, amounts next to a currency/time
unit) must not be hardcoded outside the allowlisted paths. Time-bound rules
live only in dated fund profiles (P6).

Allowlisted paths (docs/design/PLAN.md §E, "No-hardcoded-rules CI"):
  funds/, examples/, NOTICE, docs/sources.md, mappings/nriis/,
  and this script itself (it must be allowed to contain the pattern list).
  Also allowlisted: docs/design/PLAN.md, the published historical design
  plan. It describes the excluded source documents by agency and year; it
  is a record, not a rule source, and nothing reads rules from it.

Elsewhere, CI rejects:
  - known Thai research-funding agency acronyms, and
  - a number immediately next to one of: บาท, baht, ปีงบประมาณ, FY.
It does NOT reject a bare 25\\d\\d (e.g. a Buddhist-calendar year on its own).

Usage:
    python tools/ci/check_no_hardcoded_rules.py --root <path>
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ALLOWLIST_PREFIXES = (
    "funds/",
    "examples/",
    "NOTICE",
    "docs/sources.md",
    "mappings/nriis/",
    "tools/ci/check_no_hardcoded_rules.py",
    "docs/design/PLAN.md",
    "tests/fixtures/",  # fixtures deliberately contain seeded bad content
)

# Known Thai research-funding agency acronyms (kept short and generic on
# purpose; extend via PR review, not silently).
AGENCY_ACRONYMS = [
    r"\bวช\.", r"\bสกสว\.", r"\bบพข\.", r"\bบพค\.", r"\bบพท\.",
    r"\bNRCT\b", r"\bTSRI\b", r"\bPMU[A-Z]?\b",
]

UNIT_WORDS = ["บาท", "baht", "ปีงบประมาณ", "FY"]

NUMBER_NEAR_UNIT_RE = re.compile(
    r"(\d[\d,]*\s*(?:" + "|".join(re.escape(u) for u in UNIT_WORDS) + r")"
    r"|(?:" + "|".join(re.escape(u) for u in UNIT_WORDS) + r")\s*\d[\d,]*)",
    re.IGNORECASE,
)

AGENCY_RE = re.compile("|".join(AGENCY_ACRONYMS))

# The single canonical disclaimer (NOTICE) is deliberately reused verbatim
# in several files (README, ai.json, llms.txt, llms-full.txt, GOVERNANCE,
# CODE_OF_CONDUCT, PRIVACY, SECURITY, ...). A line that is clearly part of
# that non-affiliation disclaimer is exempt from the bare-acronym check —
# the guard is about smuggled-in *fund rule facts*, not the repeated
# unofficial-notice sentence itself.
DISCLAIMER_MARKERS = [
    "affiliat", "endorse", "sponsor", "official", "unofficial", "notice",
    "program management unit",
    "ผูกพัน", "สังกัด", "รับรอง", "อย่างเป็นทางการ", "เป็นอิสระ",
]

# Generic architecture vocabulary ("Fund/PMU" as an actor category, in a
# diagram or table) is not a specific agency rule and is always exempt,
# regardless of disclaimer markers.
GENERIC_TERM_PATTERNS = [
    re.compile(r"fund\s*/\s*pmu", re.IGNORECASE),
    re.compile(r"fund\s+pmu", re.IGNORECASE),
    re.compile(r"แหล่งทุน\s*/\s*(PMU|หน่วยบริหารจัดการทุน)"),
]

TEXT_EXTS = {".md", ".yaml", ".yml", ".json", ".py", ".jsonl", ".txt", ".html", ".j2"}


def is_allowlisted(rel_path: str) -> bool:
    return any(rel_path == p.rstrip("/") or rel_path.startswith(p) for p in ALLOWLIST_PREFIXES)


def is_disclaimer_line(line: str) -> bool:
    lower = line.lower()
    return any(marker.lower() in lower for marker in DISCLAIMER_MARKERS)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    violations = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts:
            continue
        if path.suffix not in TEXT_EXTS:
            continue
        rel = path.relative_to(root).as_posix()
        if is_allowlisted(rel):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            if any(p.search(line) for p in GENERIC_TERM_PATTERNS):
                continue
            if AGENCY_RE.search(line) and not is_disclaimer_line(line):
                violations.append(f"{rel}:{lineno}: contains a bare agency acronym outside the disclaimer (should live in a dated fund profile)")
            if NUMBER_NEAR_UNIT_RE.search(line):
                violations.append(f"{rel}:{lineno}: contains a number next to a currency/budget-year unit (should live in a dated fund profile)")

    if violations:
        print("no-hardcoded-rules guard: FAIL")
        for v in violations:
            print(f"  - {v}")
        return 1

    print("no-hardcoded-rules guard: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
