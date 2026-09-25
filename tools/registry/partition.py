#!/usr/bin/env python3
"""tools/registry/partition.py

Write `scope` and `route_ids` onto every record of registry/fields.jsonl
from the single partition declaration in routes/INDEX.yaml:

  scope: shared   the field is in partition.shared_core (authored once,
                  placed by more than one route);
  scope: route    the field exists for one route's output only;
  route_ids       every route whose partition.body.<route> selector
                  includes the field (shared_core: true, namespaces: [...],
                  field_ids: [...]); a field in a partition.route_namespaces
                  namespace is placed by that route alone.

Nothing else in the record is touched, and the line order is kept, so a
re-run on a partitioned file is a no-op. `--check` exits non-zero when the
committed file differs from what the declaration gives (used by
tests/test_registry.py). The tool never decides a route for a work object;
it only labels the registry.

Usage:
    python tools/registry/partition.py [--root .] [--check]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml


def _ns(field_id: str) -> str:
    return field_id.split(".", 1)[0]


def partition(fields: list[dict], index: dict) -> tuple[list[dict], list[str]]:
    """Return (records with scope/route_ids set, violations)."""
    part = index.get("partition") or {}
    shared = list(part.get("shared_core") or [])
    route_ns = dict(part.get("route_namespaces") or {})
    body = dict(part.get("body") or {})
    route_ids = [r["id"] for r in index.get("routes") or []]
    v = []
    ids = {r["field_id"] for r in fields}
    for fid in shared:
        if fid not in ids:
            v.append(f"shared_core lists {fid}, which is not a registry field")
    if len(shared) != len(set(shared)):
        v.append("shared_core lists a field twice")
    for rid in body:
        if rid not in route_ids:
            v.append(f"partition.body names {rid}, which is not a route in routes/INDEX.yaml")
    for ns, rid in route_ns.items():
        if rid not in route_ids:
            v.append(f"route_namespaces maps {ns} to {rid}, which is not a route")
    shared_set = set(shared)
    out = []
    for rec in fields:
        rec = dict(rec)
        fid = rec["field_id"]
        ns = _ns(fid)
        placed = []
        if ns in route_ns:
            placed = [route_ns[ns]]
        else:
            for rid in route_ids:
                sel = body.get(rid) or {}
                hit = (sel.get("shared_core") and fid in shared_set) \
                    or ns in (sel.get("namespaces") or []) \
                    or fid in (sel.get("field_ids") or [])
                if hit:
                    placed.append(rid)
        scope = "shared" if fid in shared_set else "route"
        if scope == "shared" and len(placed) < 2:
            v.append(f"{fid}: shared_core but placed by {placed}")
        if scope == "route" and len(placed) != 1:
            v.append(f"{fid}: scope route but placed by {placed}")
        # rebuild with scope/route_ids at the end of the record, once
        rec.pop("scope", None)
        rec.pop("route_ids", None)
        rec["scope"] = scope
        rec["route_ids"] = placed
        out.append(rec)
    return out, v


def render(records: list[dict]) -> str:
    return "\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    target = root / "registry" / "fields.jsonl"
    fields = [json.loads(x) for x in target.read_text(encoding="utf-8").splitlines() if x.strip()]
    index = yaml.safe_load((root / "routes" / "INDEX.yaml").read_text(encoding="utf-8"))
    records, violations = partition(fields, index)
    if violations:
        print("registry partition: FAIL")
        for x in violations:
            print(f"  - {x}")
        return 1
    text = render(records)
    if args.check:
        if target.read_text(encoding="utf-8") != text:
            print("registry partition: registry/fields.jsonl is out of date; run tools/registry/partition.py")
            return 1
        n_shared = sum(1 for r in records if r["scope"] == "shared")
        print(f"registry partition: OK ({len(records)} records, {n_shared} shared, {len(records) - n_shared} route)")
        return 0
    target.write_text(text, encoding="utf-8")
    print(f"wrote {target.relative_to(root)} ({len(records)} records)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
