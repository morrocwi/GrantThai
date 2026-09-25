#!/usr/bin/env python3
"""tools/ci/check_reuse.py

Guard: REUSE (https://reuse.software/) license coverage lint. Runs the
`reuse` CLI (`reuse lint`) when it is installed.

Without the CLI it falls back to a minimal check (REUSE.toml, LICENSE and
the LICENSES/ texts exist). That fallback is only a local convenience: when
the CI environment variable is set (as on GitHub Actions), a missing `reuse`
CLI is a FAILURE, so CI can never go green on the degraded check.

Usage:
    python tools/ci/check_reuse.py --root <path>
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def run_reuse_cli(root: Path) -> int | None:
    binary = shutil.which("reuse")
    if not binary:
        return None
    result = subprocess.run([binary, "--root", str(root), "lint"], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr, file=sys.stderr)
    return result.returncode


def fallback_check(root: Path) -> int:
    problems = []
    reuse_toml = root / "REUSE.toml"
    if not reuse_toml.exists():
        problems.append("REUSE.toml is missing")
    licenses_dir = root / "LICENSES"
    if not licenses_dir.exists():
        problems.append("LICENSES/ directory is missing")
    else:
        required = ["Apache-2.0.txt", "CC-BY-4.0.txt"]
        for r in required:
            if not (licenses_dir / r).exists():
                problems.append(f"LICENSES/{r} is missing")
    if not (root / "LICENSE").exists():
        problems.append("LICENSE is missing")

    if problems:
        print("reuse guard (fallback check — 'reuse' CLI not found, degraded mode): FAIL")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("reuse guard (fallback check — 'reuse' CLI not found, degraded mode): PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    rc = run_reuse_cli(root)
    if rc is not None:
        print("reuse guard: PASS" if rc == 0 else "reuse guard: FAIL")
        return rc
    if os.environ.get("CI"):
        print("reuse guard: FAIL — the 'reuse' CLI is not installed in CI (pip install reuse)")
        return 1
    return fallback_check(root)


if __name__ == "__main__":
    sys.exit(main())
