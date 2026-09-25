"""grantthai.render.article — renders build/ACADEMIC_ARTICLE.md, the one
output of the academic-article route, per spec/output/academic-article.contract.md.

    render(raw, project_dir, *, route, sub_profile, as_of) -> (text, engine.Result)

Called through grantthai.render.build_route / render_route (the dispatch),
which writes exactly one file. Deterministic: no timestamps, every list in
a declared order. Values print exactly as the researcher wrote them, with
the same value formatting as the NRIIS renderer, so a shared-core field
prints byte-identically in every route built from the same object. GrantThai
composes no section text, reformats no citation and names no venue; an empty
route title is filled by COPYING the shared title (never composing), and
the output says so.

The helpers below (placement reading, field blocks, the appendices) are also
used by grantthai.render.concept_note.

This module MUST NEVER import grantthai.assist, grantthai.mcp,
grantthai.api, or any LLM SDK (tools/ci/check_no_ai_import.py).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from grantthai import __version__
from grantthai.core import project as P
from grantthai.core.object_hash import content_sha256, state_sha256
from grantthai.render import submission as S
from grantthai.review import records as RR
from grantthai.validators import article as ART
from grantthai.validators import engine as E

AI_AUTHORED = ("ai_draft", "human_ai_assisted")
GATES = ("RG0", "RG1", "RG2", "RG3", "RG4")


# --------------------------------------------------------------------------
# placement (spec/routes/placement.schema.json; sections in file order)
# --------------------------------------------------------------------------

def read_placement(route) -> dict:
    """{sections: [{id, title_en, title_th, note, fields: [{field_id,
    shared, render_from, fallback_copy_from}]}], appendix_shared: [...]}.
    A bare field id reads as {field_id: id}."""
    rel = route.placement
    doc = (P._read_yaml(rel) or {}) if rel else {}
    secs = []
    for s in doc.get("sections") or []:
        fields = [{"field_id": f} if isinstance(f, str) else dict(f) for f in s.get("fields") or []]
        secs.append({"id": s["id"], "title_en": s.get("title_en") or "",
                     "title_th": s.get("title_th") or "NEEDS_INPUT", "note": s.get("note") or "",
                     "fields": fields, "when": s.get("when")})
    return {"sections": secs, "appendix_shared": list(doc.get("appendix_shared") or [])}


def section_shown(section: dict, recs: dict, structure_profile: str | None) -> bool:
    """A placement section's `when` condition (spec/routes/placement.schema.json):
    no condition -> shown; else shown when the field's value is in `in`, or
    (or_structure_profile_selected) when a structure profile is selected."""
    w = section.get("when")
    if not w:
        return True
    if w.get("or_structure_profile_selected") and structure_profile:
        return True
    return (recs.get(w.get("field_id")) or {}).get("value") in (w.get("in") or [])


def render_value(fid: str, value: Any, reg: dict, unresolved: set, required: bool) -> str:
    """The fenced value block, formatted exactly as the NRIIS renderer does."""
    if value is None:
        return S._fence("NEEDS_INPUT" if required else "(optional, not supplied)")
    if (reg.get(fid) or {}).get("type") in S.STRUCTURED_TYPES and not isinstance(value, str):
        return S._table(fid, value, unresolved)
    return S._plain(value)


def shared_formatter(reg: dict, unresolved: set):
    """fmt(fid, value, required) -> the value block. A shared-core field
    prints exactly as the NRIIS route prints it (a table or plain block when
    the NRIIS route places it on a tab, else the NRIIS appendix form), so
    its value is byte-identical in every route built from the same object.
    A route field prints as a table or plain block."""
    nriis_placed = {n["core_field_id"] for n in P.nriis_fields()}

    def fmt(fid: str, value: Any, required: bool) -> str:
        if (reg.get(fid) or {}).get("scope") == "shared" and fid not in nriis_placed:
            return S._any(value)
        return render_value(fid, value, reg, unresolved, required)
    return fmt


def _provenance(prov: dict) -> str:
    return (f"provenance_class={prov.get('provenance_class')}, source_type={prov.get('source_type')}, "
            f"evidence_role={prov.get('evidence_role')}") if prov else "none (no record)"


def _status_basis(rec: dict | None, value: Any, required: bool, review_basis: str | None) -> tuple[str, str]:
    if value is None:
        return ("NEEDS_INPUT" if required else "EMPTY"), \
            "no value in the work object" + ("" if required else " (optional)")
    status = rec.get("status") or "DRAFT"
    if status in ("DRAFT", "NEEDS_INPUT"):
        return status, "as authored; report-only validation, no review record"
    if status in ("STRUCTURE_CHECKED", "LOGIC_LINKED"):
        return status, "set by the deterministic validator (grantthai link); structure/links only, not a review"
    if status in ("HUMAN_REVIEWED", "VERIFIED", "LOCKED") and review_basis:
        return status, review_basis
    return status, "self-declared in the work object and NOT backed by any check"


def common_context(raw: dict, result: E.Result, route, *, placement: dict) -> dict:
    """Everything a non-NRIIS route template shares: readiness lists, the
    placed sections, metadata, gates, sources, unresolved references,
    conflicts, the records-not-placed and shared-records appendices, and the
    AI Use Declaration."""
    doc = P.normalized(raw)
    recs = P.records_by_id(doc)
    reg = P.registry_by_id()
    unresolved = {ref.target for ref, _ in result.link_report.unresolved}
    required_set = set(route.required_fields) if route.required_fields != "registry" else \
        {r["field_id"] for r in P.registry() if r.get("required")}
    gate_st = RR.gate_states(doc)
    cur = [f"{g} ({v['record'].get('independence')} review by role {v['record'].get('reviewer_role')}, "
           f"{v['record'].get('date')})" for g, v in gate_st.items() if v["state"] == "current"]
    review_basis = ("named review record(s), current: " + "; ".join(cur)) if cur else None
    by_field: dict[str, list[str]] = {}
    for f in result.findings:
        if f.severity in ("BLOCK", "REVIEW"):
            for fid in f.field_ids:
                by_field.setdefault(fid, []).append(f"{f.rule_id} {f.severity}")

    fmt = shared_formatter(reg, unresolved)
    sections, meta, needs_input, placed = [], [], [], set()
    hidden: dict[str, str] = {}
    for s in placement["sections"]:
        if not section_shown(s, recs, getattr(result, "structure_profile", None)):
            w = s.get("when") or {}
            for pf in s["fields"]:
                hidden[pf["field_id"]] = (f"section {s['id']} is shown only when {w.get('field_id')} is set"
                                          + (" or a structure profile is selected"
                                             if w.get("or_structure_profile_selected") else ""))
            continue
        blocks = []
        for pf in s["fields"]:
            fid = pf["field_id"]
            placed.add(fid)
            r = reg.get(fid) or {}
            rec = recs.get(fid)
            value = None if rec is None else rec.get("value")
            copied_from = None
            src_fid = pf.get("fallback_copy_from")
            if value is None and src_fid and (recs.get(src_fid) or {}).get("value") is not None:
                rec, value, copied_from = recs[src_fid], recs[src_fid].get("value"), src_fid
            if copied_from:
                placed.add(copied_from)
            if fid == ART.VENUE and isinstance(value, dict):
                value = venue_display(value)
            required = fid in required_set
            if value is None and required:
                needs_input.append(fid)
            prov = (rec or {}).get("provenance") or {}
            markers = sorted(set((rec or {}).get("markers") or []))
            status, basis = _status_basis(rec, value, required, review_basis)
            shared = bool(pf.get("shared")) or r.get("scope") == "shared"
            rf = pf.get("render_from") or []
            blocks.append({
                "label_en": r.get("label_en") or fid,
                "label_th": r.get("label_th") or "NEEDS_VERIFICATION",
                "value": fmt(copied_from or fid, value, required),
                "field_id": fid,
                "shared": shared,
                "origin": r.get("origin") or "none (not a registry field)",
                "provenance": _provenance(prov),
                "render_from": ", ".join(rf) if isinstance(rf, list) else str(rf),
                "copied_from": copied_from,
                "status": status,
                "basis": basis,
                "markers": markers,
                "required": "true" if required else "false",
                "source_ids": ", ".join((rec or {}).get("source_ids") or []) or "none",
                "validation": ", ".join(dict.fromkeys(by_field.get(fid, []))) or "no BLOCK/REVIEW finding",
                "authored_by": (f"{prov.get('authored_by')} (self-declared)" if prov else "none (no record)"),
            })
            meta.append({"field_id": fid, "section": s["id"], "origin": r.get("origin"),
                         "scope": r.get("scope"), "required": required, "status": status, "markers": markers,
                         "copied_from": copied_from,
                         "source_ids": list((rec or {}).get("source_ids") or []),
                         "authored_by": prov.get("authored_by")})
        sections.append({"id": s["id"], "title_en": s["title_en"], "title_th": s["title_th"],
                         "note": s["note"], "fields": blocks})

    appendix_shared = [f for f in placement["appendix_shared"] if f not in placed]

    read_from = {x for s in placement["sections"] if section_shown(s, recs, getattr(result, "structure_profile", None))
                 for pf in s["fields"]
                 for x in (pf.get("render_from") if isinstance(pf.get("render_from"), list) else [])}

    def _why(fid):
        if fid in hidden:
            return hidden[fid]
        r = reg.get(fid)
        if r is None:
            return "chain content without a registry field"
        rids = list(r.get("route_ids") or [])
        if r.get("scope") == "route" and route.id not in rids:
            return "a field of route " + ", ".join(rids) if rids else "a route field with no route"
        if fid in read_from:
            return f"a shared-core record route {route.id} names under RENDER_FROM but does not place"
        if r.get("scope") == "shared":
            return f"a shared-core field route {route.id} does not place"
        return f"not placed by route {route.id}"

    unmapped, shared_records = [], []
    for rec, key in P.iter_records(doc):
        fid = rec.get("field_id")
        if fid in placed:
            continue
        value = rec.get("value")
        if fid in appendix_shared:
            shared_records.append({"field_id": fid, "chain": key or "fields", "status": rec.get("status"),
                                   "value": fmt(fid, value, False)})
            continue
        r = reg.get(fid) or {}
        unmapped.append({"field_id": fid, "origin": r.get("origin") or "none (not a registry field)",
                         "scope": r.get("scope") or "none", "status": rec.get("status"), "why": _why(fid),
                         "value": fmt(fid, value, False) if r.get("scope") == "shared" else S._any(value)})

    marked = [(rec.get("field_id"), m, rec.get("hold_reason"))
              for rec, _ in P.iter_records(doc) for m in sorted(set(rec.get("markers") or []))]
    ai_drafts = [(rec.get("field_id"), (rec.get("provenance") or {}).get("authored_by"))
                 for rec, _ in P.iter_records(doc)
                 if (rec.get("provenance") or {}).get("authored_by") in AI_AUTHORED]
    record_needs_input = [rec.get("field_id") for rec, _ in P.iter_records(doc)
                          if rec.get("value") is None and rec.get("field_id") not in needs_input]

    csha = content_sha256(raw)
    gates = {}
    records = [r for r in raw.get("review_records") or [] if isinstance(r, dict)]
    for g in GATES:
        rs = [r for r in records if r.get("gate_id") == g]
        if not rs:
            gates[g] = {"state": "not_reviewed", "basis": "no review record"}
        else:
            last = rs[-1]
            gates[g] = {"state": "current" if last.get("content_sha256") == csha else "stale",
                        "basis": f"{last.get('independence')} review by role {last.get('reviewer_role')}"}

    cited: dict[str, list[str]] = {}
    for rec, _ in P.iter_records(doc):
        for sid in rec.get("source_ids") or []:
            cited.setdefault(sid, []).append(rec.get("field_id"))
    venue = (recs.get(ART.VENUE) or {}).get("value")
    if isinstance(venue, dict):
        for sid in list(venue.get("source_refs") or []) + [it.get("source_ref") for it in
                                                          venue.get("stated_requirements") or []
                                                          if isinstance(it, dict) and it.get("source_ref")]:
            if ART.VENUE not in cited.setdefault(sid, []):
                cited[sid].append(ART.VENUE)
    sources = []
    for s in sorted([s for s in doc.get("sources") or [] if isinstance(s, dict)],
                    key=lambda s: str(s.get("source_id"))):
        if s.get("contains_personal_data") is True:
            sources.append({"source_id": s.get("source_id"), "kind": s.get("kind"), "private": True})
        else:
            sources.append({"source_id": s.get("source_id"), "kind": s.get("kind"), "private": False,
                            "citation": s.get("citation") or "", "locator": s.get("locator") or "",
                            "url": s.get("url") or "", "sha256": s.get("sha256") or "",
                            "cited_by": ", ".join(cited.get(s.get("source_id"), [])) or "none"})
    unresolved_rows = [f"source {sid or '(none)'} on {holder}: {reason}"
                       for holder, sid, reason in result.source_problems]
    for ref, reason in result.link_report.unresolved:
        holder = result.link_report.nodes.get(ref.source)
        where = f"{ref.source}" + (f" in {holder.field_id}" if holder and holder.field_id != ref.source else "")
        unresolved_rows.append(f"reference {ref.key} -> {ref.target} UNRESOLVED on {where}: {reason}")

    project_conflicts = []
    for rec, _ in P.iter_records(doc):
        for cx in rec.get("conflicts") or []:
            if isinstance(cx, dict):
                project_conflicts.append({
                    "field_id": rec.get("field_id"), "id": cx.get("conflict_id"), "status": cx.get("status"),
                    "description": cx.get("description"),
                    "readings": [(x.get("says") or "") + (f" (sources: {', '.join(x.get('source_ids') or [])})"
                                                           if x.get("source_ids") else "")
                                 for x in cx.get("readings") or [] if isinstance(x, dict)],
                    "decision_note": cx.get("decision_note") or "",
                })

    lock = raw.get("lock") or {}
    auth = raw.get("authoring") or {}
    summary = result.report["summary"]
    view = P.work_view(raw)
    return {
        "doc": doc, "recs": recs, "csha": csha, "view": view, "summary": summary,
        "locked": bool(lock.get("locked")) and lock.get("locked_content_sha256") == csha,
        "authoring_fm": {"mode": auth.get("mode", "human"),
                         "tools_disclosed": list(auth.get("tools_disclosed") or []),
                         "self_declared": True,
                         "ai_use_declaration": ("none" if not isinstance(auth.get("ai_use_declaration"), dict)
                                                else "confirmed_by_researcher"
                                                if auth["ai_use_declaration"].get("declaration_confirmed_by_human")
                                                is True else "unconfirmed")},
        "hold_reasons": list(result.hold_reasons) + RR.gate_hold_reasons(raw),
        "blocks": [vars(f) for f in result.findings if f.severity == "BLOCK"],
        "reviews": [vars(f) for f in result.findings if f.severity == "REVIEW"],
        "infos": [vars(f) for f in result.findings if f.severity == "INFO"],
        "needs_input": needs_input, "record_needs_input": record_needs_input,
        "marked": marked, "ai_drafts": ai_drafts, "sections": sections,
        "meta_yaml": yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, width=10**6).rstrip("\n"),
        "gates": gates, "sources": sources, "unresolved": unresolved_rows,
        "project_conflicts": project_conflicts, "unmapped": unmapped, "shared_records": shared_records,
        "ai_decl": S.ai_declaration_context(raw, doc),
        "trust_level": result.trust_level,
        # The FICTIONAL banner prints only on the explicit marker
        # `fictional: true` in the work object (every shipped example sets
        # it), never on a substring of the researcher's own work_id.
        "fictional": raw.get("fictional") is True,
    }


def venue_display(value: dict) -> dict:
    """A display copy of ARTICLE.VENUE.TARGET: a stated requirement with no
    source_ref prints NEEDS_VERIFICATION in that column (rule ART010). The
    work object is not changed."""
    out = dict(value)
    reqs = []
    for it in value.get("stated_requirements") or []:
        if isinstance(it, dict) and not str(it.get("source_ref") or "").strip():
            it = {**it, "source_ref": "NEEDS_VERIFICATION (no source supplied)"}
        reqs.append(it)
    if "stated_requirements" in value:
        out["stated_requirements"] = reqs
    return out


def core_epistemic(raw: dict, recs: dict) -> dict:
    """The Core Epistemic Structure role block: experience-based expert(s)
    (the authors, by reference to the team record), the interactional
    expert (not recorded by GrantThai: NEEDS_INPUT), and each AI tool with
    its role, from authoring.ai_use_declaration (the only place a tool is
    named; never as an author)."""
    team = {m.get("id"): m for m in ((recs.get(ART.TEAM) or {}).get("value") or []) if isinstance(m, dict)}
    authors = [a for a in ((recs.get(ART.AUTHORS) or {}).get("value") or []) if isinstance(a, dict)]
    authors = sorted(authors, key=lambda a: (a.get("order") if isinstance(a.get("order"), int) else 10**6,
                                             str(a.get("id"))))
    names = [str((team.get(a.get("member_id")) or {}).get("full_name") or a.get("member_id")) for a in authors]
    auth = raw.get("authoring") if isinstance(raw.get("authoring"), dict) else {}
    decl = auth.get("ai_use_declaration") if isinstance(auth.get("ai_use_declaration"), dict) else {}
    tools = []
    for t in decl.get("tools") or []:
        if isinstance(t, dict) and t.get("name"):
            ver = f" {t.get('version')}" if t.get("version") else ""
            stages = ", ".join(t.get("stages") or []) or "stage NEEDS_INPUT"
            tools.append(f"{t.get('name')}{ver} ({stages}: {t.get('purpose') or 'purpose NEEDS_INPUT'})")
    if tools:
        ai = "; ".join(tools)
    elif E.ai_use_recorded(raw, P.normalized(raw)):
        ai = "NEEDS_INPUT (AI use is recorded but authoring.ai_use_declaration lists no tool)"
    else:
        ai = "None recorded"
    return {"experience_based_expert": (", ".join(names) + f" (the authors in {ART.AUTHORS})") if names
            else f"NEEDS_INPUT (no author in {ART.AUTHORS})",
            "interactional_expert": "NEEDS_INPUT (not recorded in the work object; write None if there is none)",
            "ai_models": ai}


def _env():
    return S._env()


def render(raw: dict, project_dir: Path | None = None, *, route, sub_profile=None, as_of=None):
    result = E.run(raw, project_dir, as_of, route=route.id, sub_profile=sub_profile)
    ctx = common_context(raw, result, route, placement=read_placement(route))
    recs = ctx["recs"]
    kind = (recs.get(ART.KIND) or {}).get("value")
    lang = (recs.get("ARTICLE.META.LANGUAGE") or {}).get("value")
    summary = ctx["summary"]
    manuscript_ready = summary["block"] == 0
    sp = result.sub_profile or "NEEDS_INPUT"
    frontmatter = {
        "grantthai_version": __version__,
        "schema_version": str(raw.get("schema_version")),
        "renderer_version": route.renderer_version,
        "route": route.id,
        "sub_profile": sp,
        "sub_profile_status": "NEEDS_VERIFICATION",
        "work_id": P.work_id(raw),
        "work_type": ctx["view"]["work_type"],
        "article_kind": kind if isinstance(kind, str) else "NEEDS_INPUT",
        "article_language": lang if isinstance(lang, str) else "NEEDS_INPUT",
        "work_content_sha256": ctx["csha"],
        "work_state_sha256": state_sha256(raw),
        "work_locked": ctx["locked"],
        "authoring": ctx["authoring_fm"],
        "submission_mode": {"human_copy_paste": True, "ai_assisted_fill": False, "direct_submit": False},
        "human_final_approval_required": True,
        "review": ctx["gates"],
        route.ready_flag: manuscript_ready,
        "hold_reasons": ctx["hold_reasons"],
        "validation_summary": dict(summary),
        "disclaimer": P.notice_constant(),
        "route_notice": route.route_notice_en or "",
    }
    context = {k: ctx[k] for k in ("summary", "hold_reasons", "blocks", "reviews", "infos", "needs_input",
                                   "record_needs_input", "marked", "ai_drafts", "sections", "meta_yaml", "gates",
                                   "sources", "unresolved", "project_conflicts", "unmapped", "shared_records",
                                   "ai_decl", "trust_level", "fictional")}
    context.update({
        "frontmatter_yaml": yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True,
                                           width=10**6).rstrip("\n"),
        "disclaimer": P.notice_constant(),
        "route_notice": route.route_notice_en or "",
        "work_id": P.work_id(raw),
        "route_id": route.id,
        "sub_profile": sp,
        "work_type": ctx["view"]["work_type"],
        "article_kind": frontmatter["article_kind"],
        "article_language": frontmatter["article_language"],
        "manuscript_ready": manuscript_ready,
        "core_epistemic": core_epistemic(raw, recs),
        # Route-adjacent advisories (spec §2.4) are not in this build: none of
        # their fields exists yet, so the section is absent.
        "advisories": [],
    })
    template = Path(route.template).name
    text = _env().get_template(template).render(**context)
    return text, result
