"""grantthai.review.diff — compare two project objects.

    diff(a, b) -> {
        "content_changed": bool,            # content_sha256(a) != content_sha256(b)
        "content_sha256": {"a": ..., "b": ...},
        "field_changes": [ {field_id, change: added|removed|changed, keys: [...]} ],
        "status_changes": [ {field_id, from, to} ],
        "stale_reviews": [gate_id ...],     # gates whose latest record in b is stale against b
        "review_records": {"a": n, "b": n},
        "mapping_changes": [ {id, from, to} ],
        "lock": {"a": unlocked|locked|broken, "b": ...},
    }

Deterministic: every list is sorted by field / gate / mapping id.
"""
from __future__ import annotations

from grantthai.core import project as P
from grantthai.core.object_hash import content_sha256
from grantthai.review import lock as L
from grantthai.review import records as R

CONTENT_KEYS = ("value", "markers", "hold_reason", "provenance", "links", "source_ids", "conflicts")


def _records(doc: dict) -> dict:
    return P.records_by_id(doc)


def diff(a: dict, b: dict) -> dict:
    ra, rb = _records(a), _records(b)
    field_changes = []
    status_changes = []
    for fid in sorted(set(ra) | set(rb)):
        if fid not in ra:
            field_changes.append({"field_id": fid, "change": "added", "keys": []})
            continue
        if fid not in rb:
            field_changes.append({"field_id": fid, "change": "removed", "keys": []})
            continue
        keys = [k for k in CONTENT_KEYS if ra[fid].get(k) != rb[fid].get(k)]
        if keys:
            field_changes.append({"field_id": fid, "change": "changed", "keys": keys})
        sa, sb = ra[fid].get("status"), rb[fid].get("status")
        if sa != sb:
            status_changes.append({"field_id": fid, "from": sa, "to": sb})

    ma = {m.get("id"): m for m in a.get("mappings") or [] if isinstance(m, dict)}
    mb = {m.get("id"): m for m in b.get("mappings") or [] if isinstance(m, dict)}
    mapping_changes = []
    for mid in sorted(set(ma) | set(mb)):
        sa = ma[mid].get("acceptance_state") if mid in ma else None
        sb = mb[mid].get("acceptance_state") if mid in mb else None
        if sa != sb:
            mapping_changes.append({"id": mid, "from": sa, "to": sb})

    ca, cb = content_sha256(a), content_sha256(b)
    return {
        "content_changed": ca != cb,
        "content_sha256": {"a": ca, "b": cb},
        "field_changes": field_changes,
        "status_changes": status_changes,
        "stale_reviews": R.stale(b),
        "review_records": {"a": len(a.get("review_records") or []),
                           "b": len(b.get("review_records") or [])},
        "mapping_changes": mapping_changes,
        "lock": {"a": L.status(a), "b": L.status(b)},
    }
