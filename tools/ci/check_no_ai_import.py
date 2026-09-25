#!/usr/bin/env python3
"""tools/ci/check_no_ai_import.py

Guard: no AI-free core package (grantthai.core, .validators, .review,
.fund, .mapping, .render, .interview, .cli) may import grantthai.assist,
grantthai.mcp, grantthai.api, or a known LLM SDK.

Usage:
    python tools/ci/check_no_ai_import.py --root <path>

Exits 0 if clean, 1 and prints violations otherwise.
"""
from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

CORE_PACKAGES = {
    "core", "validators", "review", "fund", "mapping", "render",
    "interview", "cli",
}

BANNED_MODULE_PREFIXES = (
    "grantthai.assist",
    "grantthai.mcp",
    "grantthai.api",
    "openai",
    "anthropic",
    "google.generativeai",
    "genai",
    "mistralai",
    "cohere",
    "ollama",
    "langchain",
)


def iter_core_py_files(root: Path):
    src = root / "src" / "grantthai"
    if not src.exists():
        return
    for pkg in CORE_PACKAGES:
        pkg_dir = src / pkg
        if pkg_dir.exists():
            yield from pkg_dir.rglob("*.py")


def imported_modules(tree: ast.Module):
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                yield node.module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    violations = []
    for path in iter_core_py_files(root):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            violations.append(f"{path}: SyntaxError: {exc}")
            continue
        for mod in imported_modules(tree):
            if mod is None:
                continue
            if any(mod == p or mod.startswith(p + ".") for p in BANNED_MODULE_PREFIXES):
                violations.append(f"{path}: banned import '{mod}'")

    if violations:
        print("no-AI-import guard: FAIL")
        for v in violations:
            print(f"  - {v}")
        return 1

    print("no-AI-import guard: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
