#!/usr/bin/env python3
"""tools/ci/check_attribution.py

Guard: no AI/vendor name as author, co-author, or credit anywhere in the
repository's full git history, or in tracked files.

This intentionally checks for concrete ATTRIBUTION patterns (an actual
"Co-Authored-By: <vendor>" line, a "Claude-Session:" trailer, a "Generated
with <vendor>" footer, "written by <vendor>" credit line) rather than any
bare mention of a vendor/model word — GrantThai's own policy documents
(CONTRIBUTING.md, GOVERNANCE.md, README.md) legitimately *discuss* these
banned patterns by name, and that is not itself a violation.

Separately, CITATION.cff must never name any AI/vendor at all (it names
the founder only, per plan section H), so it gets a stricter, zero-mention
check.

Checks:
  1. Full commit message history (`git log --format=%B`).
  2. Every tracked text file, for the same concrete attribution patterns.
  3. CITATION.cff specifically, for any AI/vendor token at all.

Usage:
    python tools/ci/check_attribution.py --root <path>
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

VENDOR_ALT = r"(claude|anthropic|openai|gpt|codex|copilot|gemini|chatgpt)"

ATTRIBUTION_PATTERNS = [
    re.compile(r"co-authored-by:\s*[^\n]*" + VENDOR_ALT, re.IGNORECASE),
    re.compile(r"claude-session:\s*https?://", re.IGNORECASE),
    re.compile(r"generated with \[?" + VENDOR_ALT, re.IGNORECASE),
    re.compile(r"🤖\s*generated with", re.IGNORECASE),
    re.compile(r"\bwritten by\s+" + VENDOR_ALT, re.IGNORECASE),
    re.compile(r"\b" + VENDOR_ALT + r"\s+as\s+(a\s+)?(co-)?author", re.IGNORECASE),
]

# A pattern is exempt when the surrounding line is clearly *documenting the
# ban itself* (policy prose), e.g. "rejects Co-Authored-By lines naming an
# AI vendor" or "`Claude-Session:` trailers". This keeps the guard aimed at
# real attribution lines, not policy documentation.
POLICY_DISCUSSION_MARKERS = [
    "reject", "ban", "forbid", "must never", "never appear", "guard",
    "example", "e.g.", "such as", "pattern", "denylist", "disallow",
]

VENDOR_TOKEN_RE = re.compile(VENDOR_ALT, re.IGNORECASE)

TEXT_EXTS = {".md", ".yaml", ".yml", ".json", ".py", ".txt", ".cff"}


def is_within_negative_fixtures(rel_parts) -> bool:
    parts = list(rel_parts)
    for i in range(len(parts) - 2):
        if parts[i:i + 3] == ["tests", "fixtures", "negative"]:
            return True
    return False


def root_is_itself_a_negative_fixture(root: Path) -> bool:
    return "negative" in root.parts and "fixtures" in root.parts and "tests" in root.parts


def is_policy_discussion(line: str) -> bool:
    lower = line.lower()
    return any(marker in lower for marker in POLICY_DISCUSSION_MARKERS)


def check_git_history(root: Path):
    violations = []
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "log", "--format=%B"],
            capture_output=True, text=True, check=True,
        ).stdout
    except subprocess.CalledProcessError:
        return violations
    for pat in ATTRIBUTION_PATTERNS:
        if pat.search(out):
            violations.append(f"git history: matched pattern {pat.pattern!r}")
    return violations


def check_files(root: Path):
    violations = []
    skip_negative = not root_is_itself_a_negative_fixture(root)
    # tools/ci/ itself legitimately contains these regex patterns as code.
    skip_dirs_prefixes = ("tools/ci/", ".github/workflows/")
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix not in TEXT_EXTS:
            continue
        rel_parts = path.relative_to(root).parts
        rel = path.relative_to(root).as_posix()
        if skip_negative and is_within_negative_fixtures(rel_parts):
            continue
        if any(rel.startswith(p) for p in skip_dirs_prefixes):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        if rel == "CITATION.cff":
            for lineno, line in enumerate(text.splitlines(), start=1):
                if VENDOR_TOKEN_RE.search(line):
                    violations.append(f"{rel}:{lineno}: CITATION.cff must not name any AI/vendor")
            continue

        for lineno, line in enumerate(text.splitlines(), start=1):
            for pat in ATTRIBUTION_PATTERNS:
                if pat.search(line) and not is_policy_discussion(line):
                    violations.append(f"{rel}:{lineno}: attribution pattern matched: {pat.pattern!r}")
    return violations


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    violations = check_git_history(root) + check_files(root)

    if violations:
        print("attribution guard: FAIL")
        for v in violations:
            print(f"  - {v}")
        return 1

    print("attribution guard: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
