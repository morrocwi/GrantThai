#!/usr/bin/env python3
"""tools/ci/check_notice.py

Guard: the one-line NOTICE constant (spec/output/notice_constant.txt) is
exactly one non-empty line, and it appears byte for byte in every file
that claims to reuse it: NOTICE, README.md, README.en.md, ai.json,
llms.txt, llms-full.txt and GRANTTHAI_STANDALONE.md.

Every output route's template (routes/INDEX.yaml -> route.yaml ->
output.template) must place `{{ disclaimer }}` (the constant) as the first
body line. A route that declares its own `route_notice_en` (for example the
academic-article route's "not affiliated with any journal or publisher"
line) must place `{{ route_notice }}` as the second body line, under the
NOTICE, never instead of it. The NOTICE constant itself is unchanged by the
router (decision K-R6 is open).

Usage:
    python tools/ci/check_notice.py --root <path>
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

REUSING_FILES = [
    "NOTICE",
    "README.md",
    "README.en.md",
    "ai.json",
    "llms.txt",
    "llms-full.txt",
    "GRANTTHAI_STANDALONE.md",
]
INDEX = "routes/INDEX.yaml"


def _body_lines(template_text: str) -> list[str]:
    tlines = template_text.split("\n")
    fences = [i for i, line in enumerate(tlines) if line.strip() == "---"]
    body = tlines[fences[1] + 1:] if len(fences) >= 2 else []
    return [line.strip() for line in body if line.strip()]


def _route_templates(root: Path, violations: list[str]) -> list[tuple[str, str, bool]]:
    """[(route_id, template relpath, has_route_notice)] from routes/INDEX.yaml."""
    index_path = root / INDEX
    if not index_path.exists():
        violations.append(f"{INDEX} is missing (every route template must carry the NOTICE)")
        return []
    try:
        index = yaml.safe_load(index_path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        violations.append(f"{INDEX}: not valid YAML ({exc})")
        return []
    out = []
    for entry in index.get("routes") or []:
        rid, rel = entry.get("id"), entry.get("path")
        if not rid or not rel or not (root / rel).exists():
            violations.append(f"route {rid!r}: {rel} is missing")
            continue
        try:
            route = yaml.safe_load((root / rel).read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            violations.append(f"route {rid}: {rel} is not valid YAML ({exc})")
            continue
        tpl = (route.get("output") or {}).get("template")
        if not tpl:
            violations.append(f"route {rid}: output.template is missing")
            continue
        out.append((rid, tpl, bool(route.get("route_notice_en"))))
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    violations: list[str] = []

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

    checked = 0
    for rid, tpl, has_route_notice in _route_templates(root, violations):
        path = root / tpl
        if not path.exists():
            violations.append(f"route {rid}: {tpl} is missing")
            continue
        body = _body_lines(path.read_text(encoding="utf-8"))
        first = body[0] if body else ""
        if first != "{{ disclaimer }}":
            violations.append(f"route {rid}: {tpl}: first body line must be '{{{{ disclaimer }}}}'")
        if has_route_notice:
            second = body[1] if len(body) > 1 else ""
            if second != "{{ route_notice }}":
                violations.append(f"route {rid}: {tpl}: second body line must be '{{{{ route_notice }}}}' "
                                   "(the route declares route_notice_en)")
        checked += 1

    if violations:
        print("notice guard: FAIL")
        for v in violations:
            print(f"  - {v}")
        return 1
    print(f"notice guard: PASS ({len(REUSING_FILES)} reusing files, {checked} route templates)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
