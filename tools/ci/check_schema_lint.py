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
       mappings/nriis/form_profiles/*.yaml  -> spec/mappings/form_profile.schema.json (v0.2)
       guidance/writing_intent.yaml         -> spec/guidance/writing_intent.schema.json (v0.2)
       routes/*/route.yaml                  -> spec/routes/route.schema.json (v0.3)
       routes/**/placement.yaml             -> spec/routes/placement.schema.json (v0.3)
       routes/*/profiles/*.yaml             -> spec/routes/structure_profile.schema.json (7SSA;
                                               id = file name; S1-S7 covered in order;
                                               INDEX.yaml cross-checked)
       routes/*/sub_profiles/*.yaml         -> spec/routes/sub_profile.schema.json (v0.3;
                                               id must equal the file name, route the folder)
  5. Cross-file checks: every chain.yaml edge endpoint is a declared node,
     no edge is listed twice, causal edges form a DAG; every fund profile id
     matches its path and its trust level is not above its rules'; every
     registry chain_node is a chain node and every registry dependency
     resolves; every rule input field id exists in the registry; every
     registry section has a tab in section_to_tab.yaml.
  6. Structured-field contracts (spec/registry/structured_fields.schema.json):
     every registry field of type array<object>, object or rich_text|object
     has a value schema of the right shape (and no orphan schema exists);
     every item schema carries x-grantthai-node with a unique id prefix and a
     node type consistent with the registry chain_node; every *_id / *_ids
     property carries x-grantthai-ref with valid targets, and every causal or
     feedback annotation runs with spec/common/chain.yaml
     (spec/common/links-and-sources.md).
  7. Project instances (examples, template, positive fixtures): each record
     sits where its registry chain_node says, each registry field appears at
     most once, structured values validate, every link reference and every
     source reference resolves (offline), item ids are unique, causal edges
     are acyclic, and every review record is current (its content_sha256
     equals the project's content_sha256, spec/common/object-hash.md).

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
sys.path.insert(0, str(REPO_ROOT / "src"))
from grantthai.core import links as gt_links  # noqa: E402
from grantthai.core import object_hash as gt_hash  # noqa: E402

STRUCTURED_TYPES = {"array<object>", "object", "rich_text|object"}
STRUCTURED_REL = "registry/structured_fields.schema.json"
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", ".pytest_cache"}
TRUST_ORDER = ["FICTIONAL", "COMMUNITY_EXTRACTED", "HUMAN_VERIFIED", "SECOND_CHECKED"]
FIELD_ID_PREFIXES = ("PROFILE.", "FUND.", "CORE.", "METHOD.", "WORK.", "GEO.", "BUDGET.",
                     "COMP.", "READY.", "RESULTS.", "DOC.", "AUDIT.", "BRIDGE.", "ARTICLE.")


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


def _deref(root: dict, sub):
    return gt_links._resolve_ref(root, sub)


def _walk_schema(root: dict, sub, path: str, visit):
    """Visit every (path, property_name, property_schema, owner_item_schema) and
    every item schema. owner is the nearest enclosing x-grantthai-node schema."""
    sub = _deref(root, sub)
    if not isinstance(sub, dict):
        return
    for br in sub.get("oneOf", []) + sub.get("anyOf", []):
        _walk_schema(root, br, path, visit)
    if sub.get("type") == "array" and "items" in sub:
        visit("item", path + "[]", None, _deref(root, sub["items"]))
        _walk_schema(root, sub["items"], path + "[]", visit)
    for name, ps in (sub.get("properties") or {}).items():
        visit("prop", path + "." + name, name, _deref(root, ps))
        _walk_schema(root, ps, path + "." + name, visit)


def causal_reach(chain: dict) -> dict:
    graph = {}
    for a, b in (chain.get("edges") or {}).get("causal") or []:
        graph.setdefault(a, set()).add(b)
    reach = {}
    nodes = set(graph) | {b for bs in graph.values() for b in bs}
    for n in nodes:
        seen, stack = {n}, [n]
        while stack:
            for m in graph.get(stack.pop(), ()):
                if m not in seen:
                    seen.add(m)
                    stack.append(m)
        reach[n] = seen
    return reach


def check_structured(structured: dict, fields: list, chain: dict, label: str = "spec/" + STRUCTURED_REL):
    """Return violations for the structured-field contract. Importable for tests."""
    v = []
    defs = structured.get("$defs") or {}
    reg = {r.get("field_id"): r for r in fields}
    chain_nodes = set((chain.get("nodes") or {}).get("core") or []) | set((chain.get("nodes") or {}).get("bridge") or [])
    nonchain = set(structured.get("x-grantthai-nonchain-node-types") or [])
    feedback = {tuple(e) for e in (chain.get("edges") or {}).get("feedback") or []}
    reach = causal_reach(chain)

    def is_field_key(k):
        return not k.startswith("_") and k != "record_links"

    for fid, rec in reg.items():
        if rec.get("type") in STRUCTURED_TYPES and fid not in defs:
            v.append(f"{label}: registry field {fid} (type {rec.get('type')}) has no value schema in $defs")
    for k in defs:
        if is_field_key(k) and (k not in reg or reg[k].get("type") not in STRUCTURED_TYPES):
            v.append(f"{label}: $defs/{k} is not a structured registry field")

    # node types per field (record + nested items), and prefixes
    prefixes = {}
    field_types = {}
    for fid, sch in defs.items():
        if not is_field_key(fid) or fid not in reg:
            continue
        rec = reg[fid]
        cn = rec.get("chain_node")
        types = {cn} if cn else set()
        top = _deref(structured, sch)
        rt = rec.get("type")
        if rt == "array<object>":
            items = _deref(structured, top.get("items", {})) if top.get("type") == "array" else {}
            if top.get("type") != "array" or not isinstance(items, dict) or items.get("type") != "object":
                v.append(f"{label}: $defs/{fid}: array<object> field needs type array with object items")
            elif "x-grantthai-node" not in items:
                v.append(f"{label}: $defs/{fid}: array items need x-grantthai-node")
            want_min = rec.get("cardinality") == "1..N"
            if want_min != bool(top.get("minItems", 0) >= 1):
                v.append(f"{label}: $defs/{fid}: minItems does not match registry cardinality {rec.get('cardinality')}")
        elif rt == "object" and top.get("type") != "object":
            v.append(f"{label}: $defs/{fid}: object field needs type object")
        elif rt == "rich_text|object":
            kinds = {_deref(structured, b).get("type") for b in top.get("oneOf", [])}
            if kinds != {"string", "object"}:
                v.append(f"{label}: $defs/{fid}: rich_text|object needs oneOf [string, object]")

        def visit(kind, path, name, ps, _fid=fid, _cn=cn, _types=types):
            if kind == "item":
                ann = ps.get("x-grantthai-node") if isinstance(ps, dict) else None
                if ann is None:
                    return
                pfx, nt = ann.get("id_prefix"), ann.get("node_type")
                if pfx in prefixes:
                    v.append(f"{label}: {_fid}{path}: id prefix {pfx} already used by {prefixes[pfx]}")
                prefixes[pfx] = _fid + path
                idp = (ps.get("properties") or {}).get("id") or {}
                if idp.get("pattern") != f"^{pfx}[0-9]{{1,4}}$" or "id" not in (ps.get("required") or []):
                    v.append(f"{label}: {_fid}{path}: item must require id with pattern ^{pfx}[0-9]{{1,4}}$")
                if _cn and nt != _cn:
                    v.append(f"{label}: {_fid}{path}: node_type {nt} must equal registry chain_node {_cn}")
                if not _cn and nt not in nonchain:
                    v.append(f"{label}: {_fid}{path}: node_type {nt} must be a declared non-chain type")
                _types.add(nt)
        _walk_schema(structured, sch, "", visit)
        field_types[fid] = types

    def target_types(t):
        if t.startswith("chain:"):
            return {t[6:]} if t[6:] in chain_nodes else None
        if t not in reg:
            return None
        return field_types.get(t) or ({reg[t].get("chain_node")} if reg[t].get("chain_node") else {None})

    def check_ref(where, ann, source_types):
        if not isinstance(ann, dict):
            v.append(f"{label}: {where}: *_id/*_ids property needs x-grantthai-ref")
            return
        edge = ann.get("edge")
        if edge not in ("causal", "feedback", "attribute"):
            v.append(f"{label}: {where}: edge must be causal, feedback or attribute")
            return
        if edge != "attribute" and ann.get("direction") not in ("source_to_target", "target_to_source"):
            v.append(f"{label}: {where}: {edge} reference needs a direction")
            return
        for t in ann.get("targets") or []:
            tts = target_types(t)
            if tts is None:
                v.append(f"{label}: {where}: target {t} is neither a registry field nor a chain node")
                continue
            if edge == "attribute":
                continue
            for s in source_types:
                for tt in tts:
                    if s not in chain_nodes or tt not in chain_nodes:
                        v.append(f"{label}: {where}: {edge} edge between non-chain types {s} and {tt}; use attribute")
                        continue
                    up, down = (tt, s) if ann["direction"] == "target_to_source" else (s, tt)
                    if edge == "causal" and down not in reach.get(up, {up}):
                        v.append(f"{label}: {where}: causal edge {up} -> {down} runs against spec/common/chain.yaml")
                    if edge == "feedback" and (up, down) not in feedback:
                        v.append(f"{label}: {where}: feedback edge {up} -> {down} is not in chain.yaml edges.feedback")

    for fid, sch in defs.items():
        if not is_field_key(fid) or fid not in reg:
            continue
        rec_types = {reg[fid].get("chain_node")} if reg[fid].get("chain_node") else set()
        stack_owner = {"": rec_types or {None}}

        def visit(kind, path, name, ps, _fid=fid):
            if kind == "item":
                ann = ps.get("x-grantthai-node") if isinstance(ps, dict) else None
                if ann:
                    stack_owner[path] = {ann.get("node_type")}
                return
            if name != "id" and (name.endswith("_id") or name.endswith("_ids")):
                owner = max((p for p in stack_owner if path.startswith(p)), key=len)
                check_ref(f"{_fid}{path}", ps.get("x-grantthai-ref"), stack_owner[owner])
        _walk_schema(structured, sch, "", visit)
    for name, ps in ((defs.get("record_links") or {}).get("properties") or {}).items():
        ann = ps.get("x-grantthai-ref") if isinstance(ps, dict) else None
        st = (ann or {}).get("source_types")
        if not st or any(s not in chain_nodes for s in st):
            v.append(f"{label}: record_links/{name}: needs source_types naming chain nodes")
            continue
        check_ref(f"record_links/{name}", ann, set(st))
    return v


def check_project(doc: dict, rel: str, project_dir, registry, schemas, structured: dict, fields: list, chain: dict):
    """Return violations for one project.yaml instance beyond its JSON Schema. Importable for tests."""
    v = []
    reg = {r.get("field_id"): r for r in fields}
    defs = structured.get("$defs") or {}
    seen = set()
    for recs, key in [(doc.get("fields") or [], None)] + [(r or [], k) for k, r in (doc.get("chain") or {}).items()]:
        for rec in recs:
            if not isinstance(rec, dict):
                continue
            fid = rec.get("field_id")
            if fid in reg:
                want = reg[fid].get("chain_node")
                if want != key:
                    where = f"chain.{want}" if want else "fields"
                    v.append(f"{rel}: {fid} must be under {where}")
                if fid in seen:
                    v.append(f"{rel}: registry field {fid} appears more than once (S004)")
                seen.add(fid)
                if fid in defs and rec.get("value") is not None:
                    validator = Draft202012Validator({"$ref": f"{structured['$id']}#/$defs/{fid}"}, registry=registry)
                    for err in validator.iter_errors(rec["value"]):
                        where = "/".join(str(p) for p in err.absolute_path) or "(value)"
                        v.append(f"{rel}: {fid}: value/{where}: {err.message[:160]} (S002)")
            elif isinstance(fid, str):
                parts = fid.split(".")
                if not (key and parts[0] == "CORE" and len(parts) >= 3 and parts[1] == key.upper()):
                    v.append(f"{rel}: {fid} is not a registry field and not CORE.<NODE>.<NAME> under chain.<Node>")
    rep = gt_links.derive(doc, structured, chain)
    for d in sorted(set(rep.duplicates)):
        v.append(f"{rel}: node id {d} is used more than once (S007)")
    for ref, why in rep.unresolved:
        v.append(f"{rel}: {ref.source}.{ref.key} -> {ref.target}: {why} (S006)")
    cyc = gt_links.find_cycle(rep.causal_edges())
    if cyc:
        v.append(f"{rel}: causal cycle {' -> '.join(cyc)} (CH001)")
    for fid, sid, why in gt_links.resolve_sources(doc, project_dir):
        v.append(f"{rel}: {fid}: source {sid or '-'}: {why} (S008)")
    if doc.get("review_records"):
        current = gt_hash.content_sha256(doc)
        for i, rr in enumerate(doc["review_records"]):
            if isinstance(rr, dict) and rr.get("content_sha256") != current:
                v.append(f"{rel}: review_records/{i} is stale: content_sha256 {rr.get('content_sha256')} != current {current}")
    return v


SSA_SECTORS = [f"S{n}" for n in range(1, 8)]


def check_structure_profile(doc: dict, rel: str) -> list:
    """A 7SSA profile's visible sections list S1-S7 exactly once each, in
    order (a merge joins consecutive sectors; nothing is reordered or
    dropped), and are numbered 1..n."""
    v = []
    secs = doc.get("visible_sections") or []
    flat = [s for sec in secs if isinstance(sec, dict) for s in sec.get("sectors") or []]
    if flat != SSA_SECTORS:
        v.append(f"{rel}: visible_sections must cover S1-S7 exactly once, in order (got {flat})")
    if [sec.get("n") for sec in secs if isinstance(sec, dict)] != list(range(1, len(secs) + 1)):
        v.append(f"{rel}: visible_sections must be numbered 1..{len(secs)}")
    return v


def check_structure_index(doc: dict, rel: str, root: Path, fields) -> list:
    """The 7SSA profile index: profiles resolve, sectors are S1-S7 in order,
    candidates are shipped profile ids, overlay slots exist, from_field and
    sector fields are registry fields, the slot vocabulary equals
    ARTICLE.BODY.SECTIONS' ssa_slot vocabulary in the structured contract."""
    v = []
    ids = []
    for p in doc.get("profiles") or []:
        ids.append(p.get("id"))
        path = root / str(p.get("path"))
        if not path.is_file():
            v.append(f"{rel}: profile {p.get('id')} path {p.get('path')} does not exist")
        elif (load_yaml(path) or {}).get("id") != p.get("id"):
            v.append(f"{rel}: profile {p.get('id')} does not match the id inside {p.get('path')}")
    sectors = doc.get("sectors") or []
    if [s.get("id") for s in sectors] != SSA_SECTORS:
        v.append(f"{rel}: sectors must be S1-S7 in order")
    if sorted(doc.get("writing_order") or []) != SSA_SECTORS:
        v.append(f"{rel}: writing_order must list S1-S7 once each")
    sel = doc.get("selection") or {}
    for sp, cands in (sel.get("candidates_by_sub_profile") or {}).items():
        if not (root / "routes" / str(doc.get("route")) / "sub_profiles" / f"{sp}.yaml").is_file():
            v.append(f"{rel}: candidates_by_sub_profile names {sp}, which is not a shipped sub-profile")
        for c in cands:
            if c not in ids:
                v.append(f"{rel}: candidate {c} is not a listed profile")
    reg = {r.get("field_id") for r in fields} if isinstance(fields, list) else set()
    vocab = {}
    for s in sectors:
        names = [x.get("slot") for x in s.get("slots") or []]
        if len(names) != len(set(names)):
            v.append(f"{rel}: {s.get('id')} lists a slot twice")
        vocab[s.get("id")] = set(names)
        for f in list(s.get("fields") or []) + [x.get("from_field") for x in s.get("slots") or [] if x.get("from_field")]:
            if reg and f.split("#", 1)[0] not in reg:
                v.append(f"{rel}: {s.get('id')}: {f} is not a registry field")
    for kind, ov in (doc.get("article_kind_overlays") or {}).items():
        for sec, slots in (ov.get("extra_required_slots") or {}).items():
            for slot in slots:
                if slot not in vocab.get(sec, set()):
                    v.append(f"{rel}: overlay {kind}: {sec} slot {slot} is not a slot of {sec}")
    if set(doc.get("article_kind_overlays") or {}) != set(sel.get("article_types") or []):
        v.append(f"{rel}: article_kind_overlays must cover exactly selection.article_types")
    structured_path = REPO_ROOT / "spec" / STRUCTURED_REL
    if (root / "spec" / STRUCTURED_REL).is_file():
        structured_path = root / "spec" / STRUCTURED_REL
    try:
        items = json.loads(structured_path.read_text(encoding="utf-8"))["$defs"]["ARTICLE.BODY.SECTIONS"]["items"]
        spec_vocab = {b["if"]["properties"]["ssa_sector"]["const"]: set(b["then"]["properties"]["ssa_slot"]["enum"])
                      for b in items.get("allOf") or [] if "ssa_sector" in (b.get("if") or {}).get("properties", {})}
    except (KeyError, OSError, ValueError):
        spec_vocab = {}
    if spec_vocab != vocab:
        v.append(f"{rel}: slot vocabulary differs from ARTICLE.BODY.SECTIONS ssa_slot in spec/{STRUCTURED_REL}")
    return v


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
    # Registry, chain and structured contract fall back to this repository's
    # own copies when the checked root (a seeded bad fixture) has none.
    def own(rel, loader):
        if get(rel) is not None:
            return get(rel)
        path = REPO_ROOT / rel
        return loader(path) if path.exists() else None
    ref_fields = own("registry/fields.jsonl", load_jsonl) or []
    ref_chain = own("spec/common/chain.yaml", load_yaml) or {}
    ref_structured = schemas.get("registry/structured_fields.schema.json") or {}

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
        if rel.startswith("mappings/nriis/labels@") and rel.endswith(".yaml"):
            validate(violations, registry, schemas, "mappings/labels.schema.json", get(rel), rel)
            fids = {r.get("field_id") for r in get("registry/fields.jsonl") or []}
            for fid in ((get(rel) or {}).get("field_labels") or {}):
                if fids and fid not in fids:
                    violations.append(f"{rel}: field_labels key {fid} is not a registry field")
        if rel.startswith("mappings/modes/") and rel.endswith(".yaml"):
            validate(violations, registry, schemas, "mappings/mode_mapping.schema.json", get(rel), rel)
        if rel.startswith("interview/") and rel.endswith(".yaml"):
            validate(violations, registry, schemas, "interview/question_set.schema.json", get(rel), rel)
        if rel.startswith("mappings/nriis/form_profiles/") and rel.endswith(".yaml"):
            validate(violations, registry, schemas, "mappings/form_profile.schema.json", get(rel), rel)
        if rel == "guidance/writing_intent.yaml":
            validate(violations, registry, schemas, "guidance/writing_intent.schema.json", get(rel), rel)
        if rel.startswith("routes/"):
            parts = rel.split("/")
            if len(parts) == 3 and parts[2] == "route.yaml":
                validate(violations, registry, schemas, "routes/route.schema.json", get(rel), rel)
            elif parts[-1] == "placement.yaml":
                validate(violations, registry, schemas, "routes/placement.schema.json", get(rel), rel)
            elif len(parts) == 4 and parts[2] == "profiles" and rel.endswith(".yaml"):
                validate(violations, registry, schemas, "routes/structure_profile.schema.json", get(rel), rel)
                doc = get(rel)
                if isinstance(doc, dict) and parts[3] != "INDEX.yaml":
                    if doc.get("id") != parts[3][:-len(".yaml")]:
                        violations.append(f"{rel}: id {doc.get('id')!r} must equal its file name")
                    if doc.get("route") != parts[1]:
                        violations.append(f"{rel}: route {doc.get('route')!r} must equal its folder {parts[1]!r}")
                    violations += check_structure_profile(doc, rel)
                elif isinstance(doc, dict):
                    violations += check_structure_index(doc, rel, root, get("registry/fields.jsonl"))
            elif len(parts) == 4 and parts[2] == "sub_profiles" and rel.endswith(".yaml"):
                validate(violations, registry, schemas, "routes/sub_profile.schema.json", get(rel), rel)
                doc = get(rel)
                if isinstance(doc, dict):
                    if doc.get("id") != parts[3][:-len(".yaml")]:
                        violations.append(f"{rel}: id {doc.get('id')!r} must equal its file name")
                    if doc.get("route") != parts[1]:
                        violations.append(f"{rel}: route {doc.get('route')!r} must equal its folder {parts[1]!r}")

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
            off_tab = {m.get("section") for m in s2t.get("not_on_tab") or []}
            for sec in sorted(mapped & off_tab):
                violations.append(f"mappings/nriis/section_to_tab.yaml: section {sec} is both on a tab and not_on_tab")
            for sec in sorted({r.get("section") for r in fields} - mapped - off_tab):
                violations.append(f"mappings/nriis/section_to_tab.yaml: registry section {sec} has no tab and no not_on_tab reason")
        for rec in fields:
            for src in rec.get("render_from") or []:
                if src not in ids:
                    violations.append(f"registry/fields.jsonl: {rec.get('field_id')}: render_from {src} does not resolve")
        rules = get("validators/rules.yaml")
        if isinstance(rules, dict):
            for rule in rules.get("rules") or []:
                for inp in rule.get("inputs") or []:
                    if inp.startswith(FIELD_ID_PREFIXES) and inp not in ids:
                        violations.append(f"validators/rules.yaml: {rule.get('id')}: input {inp} is not a registry field")
                    if inp.startswith("chain:") and chain_nodes and inp[6:] not in chain_nodes:
                        violations.append(f"validators/rules.yaml: {rule.get('id')}: input {inp} is not a chain node")

    # 6. Structured-field contracts
    if ref_structured and ref_fields and ref_chain and (root / "spec").is_dir():
        violations += check_structured(ref_structured, ref_fields, ref_chain)

    # 7. Project instances beyond JSON Schema
    for rel in project_like:
        doc = get(rel)
        if isinstance(doc, dict) and ref_structured:
            violations += check_project(doc, rel, (root / rel).parent, registry, schemas,
                                        ref_structured, ref_fields, ref_chain)

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

    print("schema-lint guard: PASS (parse, INDEX paths, schema meta-validation, instance validation, cross-file checks, structured-field contracts, project links/sources/reviews)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
