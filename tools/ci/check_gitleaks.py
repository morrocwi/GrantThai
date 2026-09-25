#!/usr/bin/env python3
"""tools/ci/check_gitleaks.py

Guard: run gitleaks over the repository if the binary is available. If it
is not installed in this environment, fall back to a minimal built-in
secret-shape scan (API-key-shaped strings, private-key headers) so the
guard is never silently skipped — it degrades, and says so loudly.

When scanning the real repository tree (--root is the repo root, not a
fixture directory), tests/fixtures/negative/ is excluded — those files are
seeded bad content on purpose and are scanned directly, and only directly,
by tools/ci/run_all_guards.sh.

Usage:
    python tools/ci/check_gitleaks.py --root <path>
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FALLBACK_PATTERNS = [
    ("AWS Access Key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("Generic API key assignment", re.compile(r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]")),
    ("PEM private key header", re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}")),
]

SKIP_DIRS = {".git"}


def root_is_itself_a_negative_fixture(root: Path) -> bool:
    return "negative" in root.parts and "fixtures" in root.parts and "tests" in root.parts


def scan_root(root: Path) -> Path:
    """Return a directory to scan: root itself, or a filtered temp copy with
    tests/fixtures/negative/ removed, when root is the full repository."""
    if root_is_itself_a_negative_fixture(root):
        return root
    negative_dir = root / "tests" / "fixtures" / "negative"
    if not negative_dir.exists():
        return root
    tmp = Path(tempfile.mkdtemp(prefix="grantthai_gitleaks_"))
    dest = tmp / "repo"
    shutil.copytree(
        root, dest,
        ignore=shutil.ignore_patterns(".git"),
    )
    filtered_negative = dest / "tests" / "fixtures" / "negative"
    if filtered_negative.exists():
        shutil.rmtree(filtered_negative)
    return dest


def run_gitleaks(root: Path) -> int | None:
    binary = shutil.which("gitleaks")
    if not binary:
        return None
    target = scan_root(root)
    result = subprocess.run(
        [binary, "detect", "--source", str(target), "--no-git", "-v"],
        capture_output=True, text=True,
    )
    print(result.stdout)
    print(result.stderr, file=sys.stderr)
    return result.returncode


def fallback_scan(root: Path) -> int:
    target = scan_root(root)
    violations = []
    for path in target.rglob("*"):
        if not path.is_file() or any(p in SKIP_DIRS for p in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        rel = path.relative_to(target).as_posix()
        for name, pat in FALLBACK_PATTERNS:
            for lineno, line in enumerate(text.splitlines(), start=1):
                if pat.search(line):
                    violations.append(f"{rel}:{lineno}: possible secret ({name})")
    if violations:
        print("gitleaks guard (fallback scan): FAIL")
        for v in violations:
            print(f"  - {v}")
        return 1
    print("gitleaks guard (fallback scan — gitleaks binary not found, degraded mode): PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    rc = run_gitleaks(root)
    if rc is not None:
        print("gitleaks guard: PASS" if rc == 0 else "gitleaks guard: FAIL")
        return rc
    return fallback_scan(root)


if __name__ == "__main__":
    sys.exit(main())
