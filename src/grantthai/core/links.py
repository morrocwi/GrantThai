"""grantthai.core.links — reference implementation of
spec/common/links-and-sources.md: nodes, reference resolution, the derived
project chain graph (`project:chain_edges`) and offline source resolution.

Pure functions over already-loaded data (project dict, structured-field
schema dict, registry records, chain.yaml dict). No network access.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator
import re

SOURCE_ID_RE = re.compile(r"^SRC-[A-Z0-9][A-Z0-9-]{0,62}$")


@dataclass(frozen=True)
class Node:
    id: str
    type: str | None          # chain node, non-chain type, or None (fields record)
    field_id: str             # the record the node lives in (itself for a record)
    is_record: bool
    chain_key: str | None     # chain.<Node> key for records under `chain`


@dataclass
class Reference:
    source: str               # node id holding the reference
    key: str
    target: str               # the referenced id as written
    spec: dict                # x-grantthai-ref annotation


@dataclass
class LinkReport:
    nodes: dict = field(default_factory=dict)          # id -> Node
    duplicates: list = field(default_factory=list)     # ids seen twice (S007)
    references: list = field(default_factory=list)     # all References
    unresolved: list = field(default_factory=list)     # (Reference, reason) (S006)
    edges: set = field(default_factory=set)            # (from, to, kind)
    attribute_refs: list = field(default_factory=list) # resolved attribute References

    def causal_edges(self):
        return {(a, b) for a, b, k in self.edges if k == "causal"}


def _resolve_ref(schema_root: dict, sub: dict) -> dict:
    """Follow local $ref ("#/$defs/...") one level at a time."""
    seen = 0
    while isinstance(sub, dict) and "$ref" in sub and sub["$ref"].startswith("#/") and seen < 10:
        target = schema_root
        for part in sub["$ref"][2:].split("/"):
            target = target[part]
        merged = dict(target)
        merged.update({k: v for k, v in sub.items() if k != "$ref"})
        sub = merged
        seen += 1
    return sub


def _object_branches(schema_root: dict, sub: dict) -> list[dict]:
    sub = _resolve_ref(schema_root, sub)
    if not isinstance(sub, dict):
        return []
    if "oneOf" in sub or "anyOf" in sub:
        out = []
        for br in sub.get("oneOf", []) + sub.get("anyOf", []):
            out += _object_branches(schema_root, br)
        return out
    return [sub]


def walk_value(schema_root: dict, sub: dict, value: Any, holder: str, on_item, on_ref):
    """Walk `value` guided by schema `sub`. Calls on_item(item_dict, node_ann)
    for every x-grantthai-node item and on_ref(holder_id, key, target, ann)
    for every x-grantthai-ref property. `holder` is the node id that owns
    references found at this level."""
    for br in _object_branches(schema_root, sub):
        t = br.get("type")
        if t == "array" and isinstance(value, list):
            item_schema = _resolve_ref(schema_root, br.get("items", {}))
            ann = item_schema.get("x-grantthai-node") if isinstance(item_schema, dict) else None
            for it in value:
                if ann and isinstance(it, dict):
                    on_item(it, ann)
                    walk_value(schema_root, item_schema, it, it.get("id", holder), on_item, on_ref)
                else:
                    walk_value(schema_root, item_schema, it, holder, on_item, on_ref)
            return
        if t == "object" and isinstance(value, dict):
            props = br.get("properties", {})
            for key, v in value.items():
                ps = _resolve_ref(schema_root, props.get(key, {}))
                ref_ann = ps.get("x-grantthai-ref") if isinstance(ps, dict) else None
                if ref_ann is not None:
                    targets = v if isinstance(v, list) else [v]
                    for tgt in targets:
                        if isinstance(tgt, str):
                            on_ref(holder, key, tgt, ref_ann)
                elif key in props:
                    walk_value(schema_root, ps, v, holder, on_item, on_ref)
            return


def iter_records(project: dict) -> Iterator[tuple[dict, str | None]]:
    for rec in project.get("fields") or []:
        if isinstance(rec, dict):
            yield rec, None
    for key, recs in (project.get("chain") or {}).items():
        for rec in recs or []:
            if isinstance(rec, dict):
                yield rec, key


def derive(project: dict, structured: dict, chain: dict) -> LinkReport:
    rep = LinkReport()
    defs = structured.get("$defs", {})
    seen: dict[str, Node] = {}

    def add(node: Node):
        if node.id in seen:
            rep.duplicates.append(node.id)
        else:
            seen[node.id] = node

    pending_refs: list[Reference] = []
    for rec, chain_key in iter_records(project):
        fid = rec.get("field_id")
        if not isinstance(fid, str):
            continue
        add(Node(fid, chain_key, fid, True, chain_key))
        for key, tgts in (rec.get("links") or {}).items():
            ann = (defs.get("record_links", {}).get("properties", {}).get(key) or {}).get("x-grantthai-ref")
            for tgt in tgts or []:
                if ann is None:
                    rep.unresolved.append((Reference(fid, key, tgt, {}), "unknown links key"))
                else:
                    pending_refs.append(Reference(fid, key, tgt, ann))
        if "supports_claim_id" in rec:
            pending_refs.append(Reference(fid, "supports_claim_id", rec["supports_claim_id"],
                                          {"targets": ["chain:Claim"], "edge": "causal",
                                           "direction": "source_to_target"}))
        vschema = defs.get(fid)
        if vschema is not None and rec.get("value") is not None:
            def on_item(item, ann, _fid=fid):
                iid = item.get("id")
                if isinstance(iid, str):
                    add(Node(iid, ann.get("node_type"), _fid, False, None))

            def on_ref(holder, key, tgt, ann):
                pending_refs.append(Reference(holder, key, tgt, ann))

            walk_value(structured, vschema, rec["value"], fid, on_item, on_ref)

    rep.nodes = seen
    for ref in pending_refs:
        rep.references.append(ref)
        tgt = seen.get(ref.target)
        if tgt is None:
            rep.unresolved.append((ref, "no node has this id"))
            continue
        ok = False
        for t in ref.spec.get("targets", []):
            if t.startswith("chain:"):
                ok = ok or (tgt.is_record and tgt.chain_key == t[6:])
            else:
                ok = ok or tgt.field_id == t
        if not ok:
            rep.unresolved.append((ref, "node is not one of the key's targets"))
            continue
        st = ref.spec.get("source_types")
        if st is not None:
            src = seen.get(ref.source)
            if src is None or src.type not in st:
                rep.unresolved.append((ref, "links key not allowed on this record's chain node"))
                continue
        edge = ref.spec.get("edge")
        if edge in ("causal", "feedback"):
            if ref.spec.get("direction") == "source_to_target":
                rep.edges.add((ref.source, ref.target, edge))
            else:
                rep.edges.add((ref.target, ref.source, edge))
        else:
            rep.attribute_refs.append(ref)
    return rep


def find_cycle(edges) -> list | None:
    graph: dict[str, list[str]] = {}
    for a, b in edges:
        graph.setdefault(a, []).append(b)
    state: dict[str, int] = {}

    def visit(n, stack):
        state[n] = 1
        for m in graph.get(n, []):
            if state.get(m) == 1:
                return stack + [n, m]
            if state.get(m) is None:
                c = visit(m, stack + [n])
                if c:
                    return c
        state[n] = 2
        return None

    for n in sorted(graph):
        if state.get(n) is None:
            c = visit(n, [])
            if c:
                return c
    return None


def resolve_sources(project: dict, project_dir: Path | None) -> list[tuple[str, str, str]]:
    """Return (holder field_id, source_id, reason) for every source_ids
    entry that is NOT resolvable offline (S008), plus SOURCE-class records
    with no resolvable source."""
    problems = []
    entries: dict[str, list[dict]] = {}
    for s in project.get("sources") or []:
        if isinstance(s, dict):
            entries.setdefault(s.get("source_id"), []).append(s)
    for rec, _ in iter_records(project):
        fid = rec.get("field_id")
        good = 0
        for sid in rec.get("source_ids") or []:
            reason = None
            if not isinstance(sid, str) or not SOURCE_ID_RE.match(sid):
                reason = "bad source id form"
            elif len(entries.get(sid, [])) != 1:
                reason = "no single sources entry with this id"
            else:
                e = entries[sid][0]
                if not e.get("citation"):
                    reason = "sources entry has no citation"
                elif e.get("file"):
                    if project_dir is None:
                        reason = "file cannot be checked without the project directory"
                    else:
                        fp = project_dir / e["file"]
                        if not fp.is_file():
                            reason = "file does not exist"
                        elif e.get("sha256") and hashlib.sha256(fp.read_bytes()).hexdigest() != e["sha256"]:
                            reason = "file sha256 mismatch"
            if reason:
                problems.append((fid, sid, reason))
            else:
                good += 1
        if (rec.get("provenance") or {}).get("provenance_class") == "SOURCE" and good == 0:
            problems.append((fid, "", "provenance_class SOURCE with no resolvable source"))
    return problems
