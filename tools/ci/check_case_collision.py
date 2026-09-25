#!/usr/bin/env python3
"""tools/ci/check_case_collision.py

Guard: no two paths in the tree differ only by letter case. On a
case-insensitive filesystem (the default on macOS and Windows) a clone
keeps only one of two such files, and the checkout shows as modified
straight after cloning.

Inside a git work tree the tracked paths (`git ls-files`) are checked;
anywhere else every file under --root is checked (the seeded bad fixture
is generated at run time by make_negative_fixtures.py, so no colliding
pair is ever committed).

Usage:
    python tools/ci/check_case_collision.py --root <path>
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "build", ".venv", "venv"}


def list_paths(root: Path) -> list[str]:
    if (root / ".git").exists():
        out = subprocess.run(["git", "-C", str(root), "ls-files", "-z"],
                             check=True, capture_output=True).stdout
        return [p for p in out.decode("utf-8").split("\0") if p]
    paths = []
    for p in root.rglob("*"):
        rel = p.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if p.is_file():
            paths.append(rel.as_posix())
    return paths


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    root = Path(parser.parse_args().root).resolve()
    seen: dict[str, list[str]] = {}
    for path in list_paths(root):
        # every directory prefix too, so a Docs/ vs docs/ split is caught
        parts = path.split("/")
        for i in range(1, len(parts) + 1):
            prefix = "/".join(parts[:i])
            bucket = seen.setdefault(prefix.casefold(), [])
            if prefix not in bucket:
                bucket.append(prefix)
    clashes = sorted(v for v in seen.values() if len(v) > 1)
    for group in clashes:
        print("CASE COLLISION: " + " vs ".join(sorted(group)), file=sys.stderr)
    if clashes:
        return 1
    print("check_case_collision: OK (no paths differ only by case)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
