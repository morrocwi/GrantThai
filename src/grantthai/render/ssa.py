"""grantthai.render.ssa — the 7SSA body of build/ACADEMIC_ARTICLE.md.

    sector_blocks(value, items, route) -> {S#: [block, ...]}
    compress(sector_blocks, profile, index, *, article_type=None) -> [visible section, ...]
    context(raw, recs, route, profile_id) -> dict        # what templates/article_7ssa.md.j2 renders

`compress` is a PURE, deterministic function (no I/O, no clock, no AI): it
places the researcher's own sector blocks into the visible sections of a
structure profile (7ssa-world, 7ssa-thai-7, 7ssa-thai-5, 7ssa-thai-4).
It concatenates sectors in sector order, gives every sector its own [S#]
marker (so Sector 5 always stays identifiable, 7SSA v1 §16 Rule A), prints
NEEDS_INPUT under the marker of an empty sector (§18: no sector disappears),
never reorders beyond the profile's map, never summarises, and never writes
bridging prose (Rules B-D are flags only). Every researcher string in the
input appears exactly once in the output, whatever the profile: the multiset
of strings is preserved (tests/test_7ssa.py property test).

This module MUST NEVER import grantthai.assist, grantthai.mcp,
grantthai.api, or any LLM SDK (tools/ci/check_no_ai_import.py).
"""
from __future__ import annotations

from typing import Any, Callable

from grantthai.routes import structure as ST

RENDERER_VERSION = "article_7ssa.md.j2@0.1.0"
NEEDS_INPUT = "NEEDS_INPUT"

# The ARTICLE.SSA.* fields whose keys are printed under a sector, in key
# order (the order of the structured contract). Values are printed as the
# researcher wrote them.
SECTOR_FIELDS = {
    "S4": ("ARTICLE.SSA.GAP", ("gap_type", "unresolved_problem", "why_existing_knowledge_fails",
                               "consequence_if_unresolved", "strongest_prior_attempt")),
    "S5": ("ARTICLE.SSA.CONTRIBUTION", ("one_sentence", "object_name", "contribution_type", "definition",
                                        "nearest_prior", "difference_from_prior")),
    "S7": ("ARTICLE.SSA.BEFORE_AFTER", ("before_state", "after_state", "non_claims")),
}


def _strings(v: Any) -> list[str]:
    if isinstance(v, str):
        return [v] if ST.filled(v) else []
    if isinstance(v, list):
        return [x for x in v if isinstance(x, str) and ST.filled(x)]
    return []


def sector_blocks(value: Callable[[str], Any], items: list[dict], route=None) -> dict:
    """{S1..S7: [block]}; a block is {source, label, slot, text}. Body items
    tagged with the sector come first (work-object order), then the sector's
    ARTICLE.SSA.* keys. Untagged items are returned under key "untagged"."""
    out: dict = {sid: [] for sid in ST.SECTORS}
    out["untagged"] = []
    for it in items:
        if not isinstance(it, dict):
            continue
        sid = it.get("ssa_sector")
        blk = {"source": f"{ST.BODY_SECTIONS} {it.get('id')}", "label": str(it.get("heading") or ""),
               "slot": it.get("ssa_slot") or "", "text": it.get("text") if isinstance(it.get("text"), str) else ""}
        out[sid if sid in ST.SECTORS else "untagged"].append(blk)
    for sid, (fid, keys) in SECTOR_FIELDS.items():
        v = value(fid)
        if not isinstance(v, dict):
            continue
        for k in keys:
            for s in _strings(v.get(k)):
                out[sid].append({"source": f"{fid}.{k}", "label": k, "slot": k, "text": s})
    return out


def _heading(section: dict, profile: dict, index: dict, article_type: str | None) -> tuple[str, bool]:
    """(visible heading, overlay_used). An article-type overlay replaces the
    heading of a one-sector section in a profile that uses overlays
    (contradiction CX-7SSA-02: overlay wins)."""
    ov = (index.get("article_kind_overlays") or {}).get(article_type or "")
    if profile.get("use_overlay_headings") and ov and len(section["sectors"]) == 1:
        return ov["headings_en"][section["sectors"][0]], True
    return section["heading"], False


def compress(blocks: dict, profile: dict, index: dict, *, article_type: str | None = None) -> list[dict]:
    """Pure: place sector blocks into the profile's visible sections."""
    names = {s["id"]: (s["name_th"] if profile.get("heading_lang") == "th" else s["name_en"])
             for s in index.get("sectors") or []}
    out = []
    for sec in profile.get("visible_sections") or []:
        heading, used = _heading(sec, profile, index, article_type)
        sectors = []
        for sid in sec["sectors"]:
            bl = [dict(b) for b in blocks.get(sid) or []]
            sectors.append({"id": sid, "marker": f"[{sid}] {names.get(sid, sid)}", "blocks": bl,
                            "empty": not any(ST.filled(b["text"]) for b in bl)})
        out.append({"n": sec["n"], "heading": heading, "overlay_heading": used, "sectors": sectors,
                    "compression": list(sec.get("compression") or [])})
    return out


def researcher_strings(blocks: dict) -> list[str]:
    """Every researcher string in sector blocks (texts and item headings),
    in a canonical order: for the multiset property test."""
    out = []
    for key in list(ST.SECTORS) + ["untagged"]:
        for b in blocks.get(key) or []:
            out += [x for x in (b["label"] if b["source"].startswith(ST.BODY_SECTIONS) else "", b["text"]) if x]
    return sorted(out)


def rendered_strings(visible: list[dict], untagged: list[dict]) -> list[str]:
    out = []
    for sec in visible:
        for s in sec["sectors"]:
            for b in s["blocks"]:
                out += [x for x in (b["label"] if b["source"].startswith(ST.BODY_SECTIONS) else "", b["text"]) if x]
    for b in untagged:
        out += [x for x in (b["label"], b["text"]) if x]
    return sorted(out)


def context(raw: dict, recs: dict, route, profile_id: str) -> dict:
    """Everything templates/article_7ssa.md.j2 needs, for one selected profile."""
    prof = ST.load_profile(route, profile_id)
    idx = ST.index(route)

    def value(fid):
        return (recs.get(fid) or {}).get("value")

    items = [x for x in (value(ST.BODY_SECTIONS) or []) if isinstance(x, dict)] \
        if isinstance(value(ST.BODY_SECTIONS), list) else []
    atype = value(ST.ARTICLE_TYPE)
    atype = atype if isinstance(atype, str) else None
    blocks = sector_blocks(value, items, route)
    visible = compress(blocks, prof, idx, article_type=atype)
    state = ST.sector_state(value, items, route, atype)
    where = {sid: sec["n"] for sec in visible for sid in [s["id"] for s in sec["sectors"]]}
    sector_map = []
    for sec in visible:
        for s in sec["sectors"]:
            st = state["sectors"][s["id"]]
            req = [x for x in st["slots"] if x["required"]]
            sector_map.append({
                "n": sec["n"], "heading": sec["heading"], "sector": s["id"], "marker": s["marker"],
                "filled": ", ".join(x["slot"] for x in req if x["filled"]) or "none",
                "needs_input": ", ".join(x["slot"] for x in req if not x["filled"]) or "none",
                "item_count": len(st["items"]),
                "compression": ", ".join(sec["compression"]) or "-",
            })
    audit = []
    for sec in idx.get("sectors") or []:
        st = state["sectors"][sec["id"]]
        answered = st["has_text"] or any(x["filled"] for x in st["slots"])
        audit.append({"question": sec["audit_question_en"], "sector": sec["id"],
                      "visible": where.get(sec["id"]),
                      "answered": "yes" if answered else "no (NEEDS_INPUT)"})
    rules = idx.get("compression_rules") or {}
    used_rules = sorted({r for sec in visible for r in sec["compression"]})
    return {
        "profile_id": profile_id,
        "title_en": prof.get("title_en"),
        "heading_lang": prof.get("heading_lang"),
        "status_note": prof.get("status_note"),
        "source_doc": prof["source"]["doc"],
        "source_sha256": prof["source"]["sha256"],
        "source_locator": prof["source"]["locator"],
        "article_type": atype or "NEEDS_INPUT",
        "overlay": atype if (ST.overlay(route, atype) and prof.get("use_overlay_headings")) else None,
        "visible": visible,
        "sector_map": sector_map,
        "audit": audit,
        "rules": [{"id": r, "text_en": rules[r]["text_en"], "locator": rules[r]["locator"]} for r in used_rules],
        "untagged": blocks["untagged"],
        "writing_order": " -> ".join(idx.get("writing_order") or []),
        "renderer_version": RENDERER_VERSION,
    }
