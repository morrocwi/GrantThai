#!/usr/bin/env python3
"""tools/ci/check_schema_lint.py

Guard: the data contracts hold, not only parse.

  1. Every .json, .jsonl, .yaml and .yml file parses.
  2. Every path listed in spec/INDEX.yaml exists.
  3. Every spec/**/*.schema.json is itself a valid JSON Schema (2020-12).
  4. Instances are validated against their schemas:
       funds/**/fund-profile.yaml           -> spec/fund/fund-profile.schema.json
       examples/*/project.yaml,
       templates/project.blank.yaml,
       tests/fixtures/positive/*.yaml       -> spec/project/project.schema.json
       registry/fields.jsonl                -> spec/registry/field.schema.json
       registry/nriis-fields.jsonl          -> spec/nriis/field.schema.json
       validators/rules.yaml                -> spec/validators/rule.schema.json
       mappings/nriis/section_to_tab.yaml   -> spec/mappings/section_to_tab.schema.json
       mappings/modes/*.yaml                -> spec/mappings/mode_mapping.schema.json
       interview/*.yaml                     -> spec/interview/question_set.schema.json
  5. Cross-file checks: every chain.yaml edge endpoint is a declared node,
     no edge is listed twice, causal edges form a DAG; every fund profile id
     matches its path and its trust level is not above its rules'; every
     registry chain_node is a chain node and every registry dependency
     resolves; every rule input field id exists in the registry; every
     registry section has a tab in section_to_tab.yaml.

Schemas are read from <root>/spec when it exists, otherwise from this
repository's own spec/ (so a seeded bad fixture directory can be checked
against the real contracts). jsonschema and PyYAML are required; if either
is missing the guard FAILS rather than silently skipping.

Usage:
    python tools/ci/check_schema_lint.py --root <path>
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

try:
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
except ImportError:  # pragma: no cover
    Draft202012Validator = None

REPO_ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", ".pytest_cache"}
TRUST_ORDER = ["FICTIONAL", "COMMUNITY_EXTRACTED", "HUMAN_VERIFIED", "SECOND_CHECKED"]
FIELD_ID_PREFIXES = ("PROFILE.", "FUND.", "CORE.", "METHOD.", "WORK.", "GEO.", "BUDGET.",
                     "COMP.", "READY.", "RESULTS.", "DOC.", "AUDIT.", "BRIDGE.")


def is_within_negative_fixtures(rel_parts) -> bool:
    parts = list(rel_parts)
    for i in range(len(parts) - 2):
        if parts[i:i + 3] == ["tests", "fixtures", "negative"]:
            return True
    return False


def root_is_itself_a_negative_fixture(root: Path) -> bool:
    return "negative" in root.parts and "fixtures" in root.parts and "tests" in root.parts


def iter_files(root: Path, exts):
    skip_negative = not root_is_itself_a_negative_fixture(root)
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(p in SKIP_DIRS for p in path.parts):
            continue
        if path.suffix in exts:
            if skip_negative and is_within_negative_fixtures(path.relative_to(root).parts):
                continue
            yield path


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def build_registry(spec_dir: Path):
    resources = []
    schemas = {}
    for path in sorted(spec_dir.rglob("*.schema.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        schemas[path.relative_to(spec_dir).as_posix()] = schema
        resources.append((schema["$id"], Resource.from_contents(schema)))
    return Registry().with_resources(resources), schemas


def validate(violations, registry, schemas, schema_rel, instance, label):
    schema = schemas.get(schema_rel)
    if schema is None:
        violations.append(f"{label}: schema spec/{schema_rel} not found")
        return
    validator = Draft202012Validator(schema, registry=registry)
    for err in sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path)):
        where = "/".join(str(p) for p in err.absolute_path) or "(root)"
        violations.append(f"{label}: {where}: {err.message[:200]}")


def check_chain(chain: dict, label: str = "spec/common/chain.yaml"):
    """Return violations for chain.yaml structure. Importable for tests."""
    violations = []
    nodes = set()
    for group in (chain.get("nodes") or {}).values():
        for n in group or []:
            if n in nodes:
                violations.append(f"{label}: node declared twice: {n}")
            nodes.add(n)
    seen = set()
    causal = []
    for kind, edges in (chain.get("edges") or {}).items():
        for edge in edges or []:
            a, b = edge
            for end in (a, b):
                if end not in nodes:
                    violations.append(f"{label}: {kind} edge [{a}, {b}] uses undeclared node {end}")
            key = (kind, a, b)
            if key in seen:
                violations.append(f"{label}: duplicate {kind} edge [{a}, {b}]")
            seen.add(key)
            if kind == "causal":
                causal.append((a, b))
    # CH001 on the contract itself: causal edges must form a DAG.
    graph = {}
    for a, b in causal:
        graph.setdefault(a, []).append(b)
    state = {}

    def visit(n, stack):
        state[n] = 1
        for m in graph.get(n, []):
            if state.get(m) == 1:
                violations.append(f"{label}: causal cycle through {' -> '.join(stack + [n, m])}")
            elif state.get(m) is None:
                visit(m, stack + [n])
        state[n] = 2

    for n in list(graph):
        if state.get(n) is None:
            visit(n, [])
    for stage in chain.get("required_stages") or []:
        if stage not in nodes:
            violations.append(f"{label}: required stage {stage} is not a declared node")
    return violations


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    violations = []

    if yaml is None:
        print("schema-lint guard: FAIL\n  - PyYAML is not installed (pip install pyyaml)")
        return 1
    if Draft202012Validator is None:
        print("schema-lint guard: FAIL\n  - jsonschema is not installed (pip install jsonschema)")
        return 1

    # 1. Parsing
    parsed = {}
    for path in iter_files(root, {".json"}):
        rel = path.relative_to(root).as_posix()
        try:
            parsed[rel] = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            violations.append(f"{rel}: invalid JSON: {exc}")
    for path in iter_files(root, {".jsonl"}):
        rel = path.relative_to(root).as_posix()
        try:
            parsed[rel] = load_jsonl(path)
        except Exception as exc:
            violations.append(f"{rel}: invalid JSONL: {exc}")
    for path in iter_files(root, {".yaml", ".yml"}):
        rel = path.relative_to(root).as_posix()
        try:
            docs = list(yaml.safe_load_all(path.read_text(encoding="utf-8")))
            parsed[rel] = docs[0] if len(docs) == 1 else docs
        except Exception as exc:
            violations.append(f"{rel}: invalid YAML: {exc}")

    # 2. INDEX paths
    index = parsed.get("spec/INDEX.yaml")
    if isinstance(index, dict):
        for entry in index.get("contracts", []):
            p = entry.get("path")
            if p and not (root / p).exists():
                violations.append(f"spec/INDEX.yaml: listed contract path does not exist: {p}")

    # 3. Meta-validate schemas
    spec_dir = root / "spec" if (root / "spec").is_dir() else REPO_ROOT / "spec"
    try:
        registry, schemas = build_registry(spec_dir)
    except Exception as exc:
        print(f"schema-lint guard: FAIL\n  - cannot load schemas from {spec_dir.name}/: {exc}")
        return 1
    for rel, schema in schemas.items():
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:
            violations.append(f"spec/{rel}: not a valid JSON Schema: {str(exc)[:200]}")

    def get(rel):
        return parsed.get(rel)

    # 4. Instances
    fund_ids = {}
    for rel, doc in parsed.items():
        if rel.startswith("funds/") and rel.endswith("/fund-profile.yaml") and isinstance(doc, dict):
            validate(violations, registry, schemas, "fund/fund-profile.schema.json", doc, rel)
            if not rel.startswith("funds/_template/"):
                expected = rel[len("funds/"):-len("/fund-profile.yaml")]
                if doc.get("id") != expected:
                    violations.append(f"{rel}: id {doc.get('id')!r} must equal its path id {expected!r}")
            fund_ids[doc.get("id")] = rel
            levels = [r.get("trust_level") for r in doc.get("rules") or [] if r.get("trust_level") in TRUST_ORDER]
            if levels and doc.get("trust_level") in TRUST_ORDER:
                lowest = min(levels, key=TRUST_ORDER.index)
                if TRUST_ORDER.index(doc["trust_level"]) > TRUST_ORDER.index(lowest):
                    violations.append(f"{rel}: profile trust_level {doc['trust_level']} is above its lowest rule trust_level {lowest}")

    project_like = [
        rel for rel in parsed
        if (rel.startswith("examples/") and rel.endswith("/project.yaml"))
        or rel == "templates/project.blank.yaml"
        or (rel.startswith("tests/fixtures/positive/") and rel.endswith(".yaml"))
    ]
    for rel in project_like:
        validate(violations, registry, schemas, "project/project.schema.json", get(rel), rel)

    fields = get("registry/fields.jsonl")
    if isinstance(fields, list):
        for i, rec in enumerate(fields, start=1):
            validate(violations, registry, schemas, "registry/field.schema.json", rec, f"registry/fields.jsonl:{i}")
    nriis = get("registry/nriis-fields.jsonl")
    if isinstance(nriis, list):
        for i, rec in enumerate(nriis, start=1):
            validate(violations, registry, schemas, "nriis/field.schema.json", rec, f"registry/nriis-fields.jsonl:{i}")
    if get("validators/rules.yaml") is not None:
        validate(violations, registry, schemas, "validators/rule.schema.json", get("validators/rules.yaml"), "validators/rules.yaml")
    if get("mappings/nriis/section_to_tab.yaml") is not None:
        validate(violations, registry, schemas, "mappings/section_to_tab.schema.json", get("mappings/nriis/section_to_tab.yaml"), "mappings/nriis/section_to_tab.yaml")
    for rel in parsed:
        if rel.startswith("mappings/modes/") and rel.endswith(".yaml"):
            validate(violations, registry, schemas, "mappings/mode_mapping.schema.json", get(rel), rel)
        if rel.startswith("interview/") and rel.endswith(".yaml"):
            validate(violations, registry, schemas, "interview/question_set.schema.json", get(rel), rel)

    # 5. Cross-file checks
    chain = get("spec/common/chain.yaml")
    chain_nodes = set()
    if isinstance(chain, dict):
        violations += check_chain(chain)
        chain_nodes = set((chain.get("nodes") or {}).get("core") or []) | set((chain.get("nodes") or {}).get("bridge") or [])
    if isinstance(fields, list):
        ids = {r.get("field_id") for r in fields}
        if len(ids) != len(fields):
            violations.append("registry/fields.jsonl: duplicate field_id")
        for rec in fields:
            node = rec.get("chain_node")
            if node is not None and chain_nodes and node not in chain_nodes:
                violations.append(f"registry/fields.jsonl: {rec.get('field_id')}: chain_node {node} is not a chain.yaml core/bridge node")
            for dep in rec.get("dependencies") or []:
                if dep.split("=", 1)[0] not in ids:
                    violations.append(f"registry/fields.jsonl: {rec.get('field_id')}: dependency {dep} does not resolve")
        s2t = get("mappings/nriis/section_to_tab.yaml")
        if isinstance(s2t, dict):
            mapped = {m.get("section") for m in s2t.get("mappings") or []}
            for sec in sorted({r.get("section") for r in fields} - mapped):
                violations.append(f"mappings/nriis/section_to_tab.yaml: registry section {sec} has no tab")
        rules = get("validators/rules.yaml")
        if isinstance(rules, dict):
            for rule in rules.get("rules") or []:
                for inp in rule.get("inputs") or []:
                    if inp.startswith(FIELD_ID_PREFIXES) and inp not in ids:
                        violations.append(f"validators/rules.yaml: {rule.get('id')}: input {inp} is not a registry field")
                    if inp.startswith("chain:") and chain_nodes and inp[6:] not in chain_nodes:
                        violations.append(f"validators/rules.yaml: {rule.get('id')}: input {inp} is not a chain node")

    for rel in project_like:
        doc = get(rel)
        if isinstance(doc, dict) and fund_ids:
            fid = (doc.get("fund_binding") or {}).get("fund_profile_id")
            if fid not in fund_ids:
                violations.append(f"{rel}: fund_profile_id {fid!r} does not resolve to funds/{fid}/fund-profile.yaml")

    if violations:
        print("schema-lint guard: FAIL")
        for v in violations:
            print(f"  - {v}")
        return 1

    print("schema-lint guard: PASS (parse, INDEX paths, schema meta-validation, instance validation, cross-file checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
