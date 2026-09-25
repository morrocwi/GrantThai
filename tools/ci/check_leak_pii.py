#!/usr/bin/env python3
"""tools/ci/check_leak_pii.py

Guard: scan for personal data (PDPA) and workspace/session leaks.

Two independent scan modes, selectable via flags so this one script serves
both the plan's "leak/PII scan" guard and the harness's own leak-scan
requirement:

  --pii   (default on): Thai national ID numbers (checksum-validated),
           phone numbers, and email addresses.
  --leak  (default on): workstation/session artefacts that must never
           appear in a public repo. The committed source holds only
           GENERIC patterns (home and temp paths, private IP ranges,
           localhost, UUID-shaped session ids, scratchpad references).

Maintainer-specific terms (a local account name, private workspace or
repository names, internal host names) are NOT written in this file,
because a public denylist would itself leak them. They are loaded at run
time, one regular expression per line ("#" starts a comment), from:

  1. the untracked, gitignored file `.leakdeny.local` at the repository
     root (see .gitignore), and/or
  2. the environment variable GRANTTHAI_LEAKDENY (newline-separated), which
     CI can fill from a repository secret.

If neither is present the guard still runs the generic patterns and says
so. The founder's public name is not a leak and must never be listed.

Usage:
    python tools/ci/check_leak_pii.py --root <path>
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
LOCAL_DENYLIST_FILE = ".leakdeny.local"
LOCAL_DENYLIST_ENV = "GRANTTHAI_LEAKDENY"

TEXT_EXTS = {
    ".md", ".yaml", ".yml", ".json", ".py", ".jsonl", ".txt", ".html", ".j2",
    ".cff", ".toml", ".sh", ".bat", ".command",
}

SKIP_DIRS = {".git"}

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
# Thai mobile/landline-ish patterns: 0X-XXX-XXXX or 0XXXXXXXXX (10 digits
# starting with 0), optionally hyphenated.
PHONE_RE = re.compile(r"\b0\d{1,2}-?\d{3}-?\d{3,4}\b")
THAI_ID_RE = re.compile(r"\b\d{13}\b")

# Emails that are clearly placeholders/examples and must not be flagged.
EMAIL_ALLOWLIST_DOMAINS = {"example.invalid", "example.com", "example.org", "example.net"}

GENERIC_LEAK_PATTERNS = [
    ("home-path", re.compile(r"/home/[A-Za-z0-9_.\-]+")),
    ("macos-home-path", re.compile(r"/Users/[A-Za-z0-9_.\-]+/")),
    ("tmp-path", re.compile(r"/tmp/")),
    ("scratchpad", re.compile(r"\bscratchpad\b")),
    ("private-ip", re.compile(r"\b(192\.168|10\.\d{1,3}|172\.(1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b")),
    ("localhost", re.compile(r"\blocalhost\b")),
    ("session-id-uuid", re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b")),
]


def load_local_denylist():
    """Maintainer-specific patterns from .leakdeny.local and/or the env var."""
    lines = []
    local = REPO_ROOT / LOCAL_DENYLIST_FILE
    sources = []
    if local.exists():
        lines += local.read_text(encoding="utf-8").splitlines()
        sources.append(LOCAL_DENYLIST_FILE)
    env = os.environ.get(LOCAL_DENYLIST_ENV, "")
    if env.strip():
        lines += env.splitlines()
        sources.append(LOCAL_DENYLIST_ENV)
    patterns = []
    for n, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        patterns.append((f"local-denylist-{n}", re.compile(line)))
    return patterns, sources

FICTIONAL_EMAIL_DOMAIN_HINT = "@example."

# Dated filenames like "positions@2026-09.yaml" look like emails to a
# naive regex; exclude common non-email file extensions as the "TLD".
NON_EMAIL_FILE_EXTENSIONS = {
    "yaml", "yml", "json", "md", "py", "txt", "jsonl", "html", "j2",
    "cff", "toml", "sh", "bat", "command", "jpg", "pdf",
}


def thai_id_checksum_valid(digits: str) -> bool:
    if len(digits) != 13 or not digits.isdigit():
        return False
    d = [int(c) for c in digits]
    total = sum(d[i] * (13 - i) for i in range(12))
    check = (11 - (total % 11)) % 10
    return check == d[12]


def is_within_negative_fixtures(rel_parts) -> bool:
    """True if this relative path lies inside tests/fixtures/negative/."""
    parts = list(rel_parts)
    for i in range(len(parts) - 2):
        if parts[i:i+3] == ["tests", "fixtures", "negative"]:
            return True
    return False


def root_is_itself_a_negative_fixture(root) -> bool:
    return "negative" in root.parts and "fixtures" in root.parts and "tests" in root.parts


def iter_text_files(root: Path):
    skip_negative = not root_is_itself_a_negative_fixture(root)
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix not in TEXT_EXTS:
            continue
        rel = path.relative_to(root).as_posix()
        if skip_negative and is_within_negative_fixtures(path.relative_to(root).parts):
            continue
        if rel.startswith("tools/ci/") or rel.startswith(".github/workflows/"):
            # These paths legitimately contain the guard's own detection
            # patterns as literal strings; it is not leaked data.
            continue
        yield path


def scan_pii(root: Path):
    violations = []
    for path in iter_text_files(root):
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            for m in THAI_ID_RE.finditer(line):
                if thai_id_checksum_valid(m.group(0)):
                    violations.append(f"{rel}:{lineno}: checksum-valid Thai national ID found")
            for m in PHONE_RE.finditer(line):
                violations.append(f"{rel}:{lineno}: phone-number-shaped string found: {m.group(0)}")
            for m in EMAIL_RE.finditer(line):
                email = m.group(0)
                domain = email.split("@", 1)[1].lower()
                tld = domain.rsplit(".", 1)[-1]
                if domain in EMAIL_ALLOWLIST_DOMAINS or FICTIONAL_EMAIL_DOMAIN_HINT in email.lower():
                    continue
                if tld in NON_EMAIL_FILE_EXTENSIONS:
                    # e.g. "positions@2026-09.yaml" is a dated filename, not an email.
                    continue
                violations.append(f"{rel}:{lineno}: email address found: {email}")
    return violations


def scan_leaks(root: Path, patterns):
    violations = []
    for path in iter_text_files(root):
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            for name, pattern in patterns:
                if pattern.search(line):
                    violations.append(f"{rel}:{lineno}: leak pattern '{name}' matched")
    return violations


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--pii", action="store_true", default=True)
    parser.add_argument("--no-pii", dest="pii", action="store_false")
    parser.add_argument("--leak", action="store_true", default=True)
    parser.add_argument("--no-leak", dest="leak", action="store_false")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    all_violations = []
    if args.pii:
        all_violations += scan_pii(root)
    if args.leak:
        local_patterns, sources = load_local_denylist()
        if sources:
            print(f"leak/PII guard: loaded {len(local_patterns)} local denylist pattern(s) from {', '.join(sources)}")
        else:
            print(f"leak/PII guard: no local denylist ({LOCAL_DENYLIST_FILE} or ${LOCAL_DENYLIST_ENV}); generic patterns only")
        all_violations += scan_leaks(root, GENERIC_LEAK_PATTERNS + local_patterns)

    if all_violations:
        print("leak/PII guard: FAIL")
        for v in all_violations:
            print(f"  - {v}")
        return 1

    print("leak/PII guard: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
