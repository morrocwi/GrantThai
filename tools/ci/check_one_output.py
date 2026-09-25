#!/usr/bin/env python3
"""tools/ci/check_one_output.py

Guard: the one-input, one-output contract, restated per route
(spec/contracts/one-input-one-output.md 0.3): one work object in,
`grantthai build --route X` out, exactly one file, build/<route filename>.
NRIIS is one route of the router; the route is always chosen by a person,
never by this tool.

Structural checks (no engine needed):
  1. routes/INDEX.yaml exists and every route it lists has a route.yaml
     whose `id` matches, whose `output.filename` equals the index entry,
     and whose `output.template` exists under templates/.
  2. Every route names exactly one template. That template carries an
     output_kind the guard accepts (`route_output`; the legacy aliases
     `primary_submission` for the NRIIS route and `secondary_optional`
     for the concept-note route are accepted so those templates stay
     byte-identical) and, when it carries a `route:` tag, that tag equals
     the route id. No template is claimed by two routes, and no template
     tagged `route_output` (or carrying a `route:` tag) is left without a
     route. At most one template is tagged `primary_submission`.
  3. Output filenames are unique across routes.
  4. Every route's contract file (`output.contract`) exists and names
     spec/contracts/one-input-one-output.md; the one-input-one-output
     contract names every route's contract path (the reverse).

Runtime check (in-process Python API, no network):
  5. For every shipped example under examples/ that holds a work.yaml or a
     project.yaml, building each route the example declares
     (`routing.declared_routes`, else `routing.default_route`, else the
     legacy nriis-proposal route) into an empty scratch directory produces
     exactly one new file per build with the declared name, and every file
     written by an earlier build in the same directory stays byte-identical.
     A route with no shipped example is reported as not runtime-checked.

Seeded bad fixtures (each must make this guard FAIL):
  tests/fixtures/negative/one_output_dup_filename/   two routes, one filename
  tests/fixtures/negative/one_output_two_templates/  one route claimed by two templates
  tests/fixtures/negative/one_output_orphan_template/ a route_output template with no route

Usage:
    python tools/ci/check_one_output.py --root <path>
"""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import sys
import tempfile
from pathlib import Path

import yaml

CONTRACT = "spec/contracts/one-input-one-output.md"
INDEX = "routes/INDEX.yaml"
ACCEPTED_KINDS = {"route_output", "primary_submission", "secondary_optional"}
LEGACY_ROUTE = "nriis-proposal"
AS_OF = "2026-09-25"

_KIND_RE = re.compile(r"^\s*output_kind:\s*([\w-]+)\s*$", re.M)
_ROUTE_RE = re.compile(r"^\s*route:\s*([\w-]+)\s*$", re.M)


def _header(text: str) -> str:
    """The leading Jinja comment block of a template ("" when absent)."""
    m = re.match(r"\s*\{#-?(.*?)-?#\}", text, re.S)
    return m.group(1) if m else ""


def _template_tags(path: Path) -> tuple[str | None, str | None]:
    head = _header(path.read_text(encoding="utf-8", errors="ignore"))
    kind = _KIND_RE.search(head)
    route = _ROUTE_RE.search(head)
    return (kind.group(1) if kind else None, route.group(1) if route else None)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _example_routes(doc: dict) -> list[str]:
    routing = doc.get("routing") or {}
    declared = routing.get("declared_routes") or []
    if declared:
        return list(declared)
    if routing.get("default_route"):
        return [routing["default_route"]]
    return [LEGACY_ROUTE]


def structural(root: Path, violations: list[str]) -> dict[str, dict]:
    """Return {route_id: {"filename", "template", "contract"}} for the
    routes the index lists; append every structural violation."""
    routes: dict[str, dict] = {}
    index_path = root / INDEX
    if not index_path.exists():
        violations.append(f"{INDEX} is missing")
        return routes
    try:
        index = yaml.safe_load(index_path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        violations.append(f"{INDEX}: not valid YAML ({exc})")
        return routes

    entries = index.get("routes") or []
    if not entries:
        violations.append(f"{INDEX} lists no routes")

    for entry in entries:
        rid = str(entry.get("id", ""))
        rel = entry.get("path")
        if not rid or not rel:
            violations.append(f"{INDEX}: a route entry lacks id or path: {entry!r}")
            continue
        if rid in routes:
            violations.append(f"{INDEX}: route id {rid!r} listed twice")
            continue
        rpath = root / rel
        if not rpath.exists():
            violations.append(f"route {rid}: {rel} is missing")
            continue
        try:
            route = yaml.safe_load(rpath.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            violations.append(f"route {rid}: {rel} is not valid YAML ({exc})")
            continue
        if route.get("id") != rid:
            violations.append(f"route {rid}: {rel} carries id {route.get('id')!r}")
        output = route.get("output") or {}
        filename = output.get("filename")
        template = output.get("template")
        contract = output.get("contract")
        if not filename:
            violations.append(f"route {rid}: output.filename is missing")
        elif entry.get("output_filename") not in (None, filename):
            violations.append(f"route {rid}: {INDEX} says {entry.get('output_filename')!r}, "
                               f"route.yaml says {filename!r}")
        if not template:
            violations.append(f"route {rid}: output.template is missing (a route names exactly one template)")
        elif isinstance(template, list):
            violations.append(f"route {rid}: output.template lists {len(template)} templates; exactly one is allowed")
            template = None
        elif not (root / template).exists():
            violations.append(f"route {rid}: template {template} does not exist")
            template = None
        if not contract:
            violations.append(f"route {rid}: output.contract is missing")
        routes[rid] = {"filename": filename, "template": template, "contract": contract}

    # 2. templates: one per route, tags agree, none shared, none orphaned
    claimed: dict[str, list[str]] = {}
    for rid, info in routes.items():
        tpl = info["template"]
        if not tpl:
            continue
        claimed.setdefault(tpl, []).append(rid)
        kind, tag = _template_tags(root / tpl)
        if kind not in ACCEPTED_KINDS:
            violations.append(f"route {rid}: {tpl} is tagged output_kind: {kind!r}; expected one of "
                               f"{sorted(ACCEPTED_KINDS)}")
        if tag is not None and tag != rid:
            violations.append(f"route {rid}: {tpl} carries route: {tag!r}")
    for tpl, rids in claimed.items():
        if len(rids) > 1:
            violations.append(f"template {tpl} is claimed by more than one route: {rids}")

    templates_dir = root / "templates"
    primary = []
    by_route_tag: dict[str, list[str]] = {}
    if templates_dir.exists():
        for path in sorted(templates_dir.glob("*.j2")):
            rel = path.relative_to(root).as_posix()
            kind, tag = _template_tags(path)
            if kind == "primary_submission":
                primary.append(rel)
            if tag is not None:
                by_route_tag.setdefault(tag, []).append(rel)
            if (kind == "route_output" or tag is not None) and rel not in claimed:
                violations.append(f"template {rel} is tagged for route output "
                                   f"(output_kind: {kind}, route: {tag}) but no route names it")
    else:
        violations.append("templates/ is missing")
    if len(primary) > 1:
        violations.append(f"more than one template tagged output_kind: primary_submission: {primary}")
    for tag, rels in by_route_tag.items():
        if len(rels) > 1:
            violations.append(f"route {tag} is claimed by more than one template: {rels}")

    # 3. filenames unique across routes
    names: dict[str, list[str]] = {}
    for rid, info in routes.items():
        if info["filename"]:
            names.setdefault(info["filename"], []).append(rid)
    for name, rids in names.items():
        if len(rids) > 1:
            violations.append(f"output filename {name!r} is used by more than one route: {rids}")

    # 4. contracts cross-reference
    contract_path = root / CONTRACT
    if not contract_path.exists():
        violations.append(f"{CONTRACT} is missing")
        contract_text = ""
    else:
        contract_text = contract_path.read_text(encoding="utf-8")
    for rid, info in routes.items():
        rc = info["contract"]
        if not rc:
            continue
        rc_path = root / rc
        if not rc_path.exists():
            violations.append(f"route {rid}: contract {rc} is missing")
            continue
        if CONTRACT not in rc_path.read_text(encoding="utf-8"):
            violations.append(f"route {rid}: {rc} does not reference {CONTRACT}")
        if contract_text and rc not in contract_text:
            violations.append(f"{CONTRACT} does not reference {rc} (route {rid})")
    return routes


def runtime(root: Path, routes: dict[str, dict], violations: list[str], notes: list[str]) -> None:
    examples_dir = root / "examples"
    if not examples_dir.is_dir():
        notes.append("examples/ is absent: the runtime check did not run")
        return
    inputs = []
    for d in sorted(p for p in examples_dir.iterdir() if p.is_dir()):
        work, project = d / "work.yaml", d / "project.yaml"
        if work.exists() and project.exists():
            violations.append(f"examples/{d.name}: holds both work.yaml and project.yaml (two canonical inputs)")
            continue
        if work.exists():
            inputs.append(work)
        elif project.exists():
            inputs.append(project)
    if not inputs:
        violations.append("examples/ holds no work.yaml or project.yaml; the runtime check cannot run")
        return

    sys.path.insert(0, str(root / "src"))
    from grantthai import api_py as api  # noqa: E402

    checked: set[str] = set()
    for src in inputs:
        label = f"examples/{src.parent.name}/{src.name}"
        try:
            doc = yaml.safe_load(src.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            violations.append(f"{label}: not valid YAML ({exc})")
            continue
        wanted = _example_routes(doc)
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            shutil.copy(src, tmp_path / src.name)
            build_dir = tmp_path / "build"
            seen: dict[str, str] = {}
            for rid in wanted:
                if rid not in routes:
                    violations.append(f"{label}: declares route {rid!r}, which {INDEX} does not list")
                    continue
                expected = routes[rid]["filename"]
                if not expected:
                    continue
                try:
                    out = api.build(tmp_path / src.name, route=rid, as_of=AS_OF)
                except Exception as exc:  # noqa: BLE001
                    violations.append(f"{label}: build --route {rid} raised {exc!r}")
                    continue
                names = sorted(p.name for p in build_dir.iterdir()) if build_dir.is_dir() else []
                if out != build_dir / expected:
                    violations.append(f"{label}: build --route {rid} returned {out}, expected {build_dir / expected}")
                if sorted(set(seen) | {expected}) != names:
                    violations.append(f"{label}: after build --route {rid} build/ holds {names!r}, expected "
                                       f"{sorted(set(seen) | {expected})!r}")
                for name, digest in seen.items():
                    if (build_dir / name).exists() and _sha(build_dir / name) != digest:
                        violations.append(f"{label}: build --route {rid} changed {name} (must stay byte-identical)")
                if (build_dir / expected).exists():
                    seen[expected] = _sha(build_dir / expected)
                checked.add(rid)
        notes.append(f"{label}: built {', '.join(wanted)}")
    for rid in routes:
        if rid not in checked:
            notes.append(f"route {rid}: no shipped example declares it; not runtime-checked")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    violations: list[str] = []
    notes: list[str] = []
    routes = structural(root, violations)
    if routes:
        runtime(root, routes, violations, notes)

    if violations:
        print("one-input-one-output guard: FAIL")
        for v in violations:
            print(f"  - {v}")
        return 1

    print("one-input-one-output guard: PASS (structural checks per route + renderer-output check on the shipped examples)")
    for n in notes:
        print(f"  . {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
