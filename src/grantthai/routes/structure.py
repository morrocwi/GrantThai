"""grantthai.routes.structure — structure profiles of a route (7SSA).

A structure profile says how a route's output body is ARRANGED into visible
sections: a third axis next to the sub-profile (venue type) of a route. The
only family is 7SSA (Seven-Section Scholarly Architecture), from the
founder-authored 7SSA master schema v1.0, shipped as data under
routes/academic-article/profiles/ (spec/routes/structure_profile.schema.json).

A profile is chosen by a person only: --structure-profile, or
routing.structure_profiles[<route>] in work.yaml (outside content_sha256).
This module resolves what a person chose, lists candidates when asked, and
reads the sector/slot data; it never selects a profile.

    has_profiles(route) -> bool
    profile_ids(route) -> list[str]
    load_profile(route, profile_id) -> dict          # StructureProfileNotFound
    resolve_structure_profile(doc, route, explicit=None) -> str | None
    candidates(doc, route, sub_profile, article_type) -> dict | None
    sectors(route) -> list[dict]; overlay(route, article_type) -> dict | None
    sector_state(value, items, route, article_type) -> dict   # pure; no I/O beyond the cached data

This package MUST NEVER import grantthai.assist, grantthai.mcp,
grantthai.api, or any LLM SDK. Enforced by tools/ci/check_no_ai_import.py.
"""
from __future__ import annotations

from functools import lru_cache
from typing import Any, Callable

from grantthai.core import project as P

SCHEMA_ID = "https://github.com/morrocwi/GrantThai/spec/routes/structure_profile.schema.json"
SECTORS = ("S1", "S2", "S3", "S4", "S5", "S6", "S7")
BODY_SECTIONS = "ARTICLE.BODY.SECTIONS"
ARTICLE_TYPE = "ARTICLE.SSA.ARTICLE_TYPE"


class StructureProfileError(ValueError):
    """A structure-profile file is missing or fails its contract."""


class StructureProfileNotFound(StructureProfileError):
    """The route ships no structure profile with this id."""


def _cfg(route) -> dict | None:
    sp = route.raw.get("structure_profiles") if hasattr(route, "raw") else None
    return sp if isinstance(sp, dict) else None


def has_profiles(route) -> bool:
    return _cfg(route) is not None


@lru_cache(maxsize=None)
def _read(rel: str) -> dict:
    if ".." in rel.split("/"):
        raise StructureProfileError(f"{rel}: not a path under the data root")
    path = P.DATA_ROOT / rel
    if not path.is_file():
        raise StructureProfileError(f"{rel}: no such file")
    doc = P._read_yaml(rel)
    errs = P.schema_errors(doc, SCHEMA_ID)
    if errs:
        raise StructureProfileError(f"{rel}: " + "; ".join(errs))
    return doc


def index(route) -> dict:
    cfg = _cfg(route)
    if cfg is None:
        raise StructureProfileError(f"route {route.id} has no structure profiles")
    return _read(cfg["index"])


def profile_ids(route) -> list[str]:
    if not has_profiles(route):
        return []
    return [p["id"] for p in index(route).get("profiles") or []]


def load_profile(route, profile_id: str) -> dict:
    if not has_profiles(route):
        raise StructureProfileNotFound(f"route {route.id} has no structure profiles (asked for {profile_id!r})")
    entry = next((p for p in index(route).get("profiles") or [] if p.get("id") == profile_id), None)
    if entry is None:
        raise StructureProfileNotFound(f"{profile_id!r} is not a shipped structure profile of route {route.id} "
                                       f"(known: {', '.join(profile_ids(route)) or 'none'})")
    doc = _read(entry["path"])
    if doc.get("id") != profile_id:
        raise StructureProfileError(f"{entry['path']}: id {doc.get('id')!r} does not equal {profile_id!r}")
    return doc


def resolve_structure_profile(doc: dict, route, explicit: str | None = None) -> str | None:
    """--structure-profile, else routing.structure_profiles[route], else
    None (the plain output). Never a default: only a person selects."""
    if explicit:
        return explicit
    routing = doc.get("routing") if isinstance(doc.get("routing"), dict) else {}
    chosen = routing.get("structure_profiles") if isinstance(routing.get("structure_profiles"), dict) else {}
    val = chosen.get(route.id)
    return val if isinstance(val, str) and val.strip() else None


def sectors(route) -> list[dict]:
    return list(index(route).get("sectors") or [])


def overlay(route, article_type: str | None) -> dict | None:
    if not article_type:
        return None
    return (index(route).get("article_kind_overlays") or {}).get(article_type)


def candidates(doc: dict, route, sub_profile: str | None, article_type: Any) -> dict | None:
    """{matching: [...], others: [...]} when the router should PROPOSE 7SSA
    profiles (selection data in INDEX.yaml: work_type, article type), else
    None. Pure listing: nothing is written, nothing is chosen."""
    if not has_profiles(route):
        return None
    sel = index(route).get("selection") or {}
    if P.work_view(doc)["work_type"] not in (sel.get("work_types") or []):
        return None
    if not isinstance(article_type, str) or article_type not in (sel.get("article_types") or []):
        return None
    ids = profile_ids(route)
    matching = [p for p in (sel.get("candidates_by_sub_profile") or {}).get(sub_profile or "", []) if p in ids]
    return {"matching": matching, "others": [p for p in ids if p not in matching]}


# --------------------------------------------------------------------------
# sector state (shared by the SSA validator family and the renderer)
# --------------------------------------------------------------------------

def filled(v: Any) -> bool:
    if v is None:
        return False
    if isinstance(v, str):
        return v.strip() not in ("", "NEEDS_INPUT", "NEEDS_VERIFICATION")
    if isinstance(v, (list, dict)):
        return any(filled(x) for x in (v.values() if isinstance(v, dict) else v))
    return True


def _from_field(value: Callable[[str], Any], ref: str) -> Any:
    fid, _, key = ref.partition("#")
    v = value(fid)
    if key:
        return v.get(key) if isinstance(v, dict) else None
    return v


def sector_state(value: Callable[[str], Any], items: list[dict], route, article_type: Any) -> dict:
    """Per sector: the body items tagged with it (in work-object order), the
    required slots (base + article-type overlay), which slots are filled
    (by a tagged item with text, or by the ARTICLE.SSA.* key the slot reads),
    and the untagged items. `value(fid)` returns a field's value."""
    ov = overlay(route, article_type if isinstance(article_type, str) else None) or {}
    extra = ov.get("extra_required_slots") or {}
    out: dict = {"sectors": {}, "untagged": [it for it in items if not it.get("ssa_sector")]}
    for sec in sectors(route):
        sid = sec["id"]
        tagged = [it for it in items if it.get("ssa_sector") == sid]
        slots = []
        for s in sec.get("slots") or []:
            by_item = any(it.get("ssa_slot") == s["slot"] and filled(it.get("text")) for it in tagged)
            by_field = bool(s.get("from_field")) and filled(_from_field(value, s["from_field"]))
            slots.append({"slot": s["slot"], "required": bool(s.get("required")) or s["slot"] in (extra.get(sid) or []),
                          "filled": by_item or by_field,
                          "via": "item" if by_item else ("field " + s["from_field"]) if by_field else None,
                          "from_field": s.get("from_field")})
        out["sectors"][sid] = {
            "id": sid, "name_en": sec["name_en"], "name_th": sec["name_th"], "chain": sec["chain"],
            "audit_question_en": sec["audit_question_en"],
            "items": tagged,
            "slots": slots,
            "has_text": any(filled(it.get("text")) for it in tagged),
            "any_required_filled": any(s["filled"] for s in slots if s["required"]),
        }
    return out
