"""grantthai.render.submission — renders the one output,
build/NRIIS_SUBMISSION.md, per spec/output/nriis-submission.contract.md.

Deterministic: no timestamps, no set/dict-order dependence, every list in
a declared order. Values are printed exactly as the researcher wrote them;
nothing here writes, rewrites or "improves" content. Missing values print
as NEEDS_INPUT, unconfirmed NRIIS facts as NEEDS_VERIFICATION, and markers
are never dropped.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from grantthai import __version__
from grantthai.core import project as P
from grantthai.core.object_hash import content_sha256, state_sha256
from grantthai.validators import engine as E

TEMPLATE = "nriis_submission.md.j2"
RENDERER_VERSION = "nriis_submission.md.j2@0.1.0"
STRUCTURED_TYPES = ("array<object>", "object", "rich_text|object")
AI_AUTHORED = ("ai_draft", "human_ai_assisted")


def _env():
    import jinja2

    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(P.DATA_ROOT / "templates")),
        autoescape=False, keep_trailing_newline=True, trim_blocks=True, lstrip_blocks=True,
        undefined=jinja2.StrictUndefined,
    )


# --------------------------------------------------------------------------
# value formatting
# --------------------------------------------------------------------------

def _scalar(v: Any) -> str:
    if v is None:
        return ""
    if v is True:
        return "true"
    if v is False:
        return "false"
    if isinstance(v, (int, float)):
        return repr(v)
    if isinstance(v, str):
        return v
    return json.dumps(v, ensure_ascii=False, separators=(", ", ": "))


def _fence(text: str) -> str:
    ticks = "```"
    while ticks in text:
        ticks += "`"
    return f"{ticks}text\n{text}\n{ticks}"


def _cell(v: Any, unresolved: set, key: str) -> str:
    if isinstance(v, list):
        if key.endswith("_ids"):
            parts = [f"{x} UNRESOLVED" if x in unresolved else str(x) for x in v]
        else:
            parts = [_scalar(x) for x in v]
        s = ", ".join(parts)
    else:
        s = _scalar(v)
        if key.endswith("_id") and isinstance(v, str) and v in unresolved:
            s += " UNRESOLVED"
    return s.replace("|", "\\|").replace("\n", " ")


def _props(fid: str) -> tuple[str, list[str]]:
    """('array'|'object', declared keys in schema order) for a structured field."""
    defs = P.schema(P.STRUCTURED_SCHEMA_ID).get("$defs", {})
    sub = defs.get(fid) or {}
    for br in [sub] + sub.get("oneOf", []) + sub.get("anyOf", []):
        if br.get("type") == "array":
            items = br.get("items") or {}
            return "array", list((items.get("properties") or {}).keys())
        if br.get("type") == "object":
            return "object", list((br.get("properties") or {}).keys())
    return "object", []


def _table(fid: str, value: Any, unresolved: set) -> str:
    kind, keys = _props(fid)
    if kind == "array" and isinstance(value, list):
        extra = []
        for it in value:
            if isinstance(it, dict):
                extra += [k for k in it if k not in keys and k not in extra]
        cols = keys + extra
        lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
        for it in value:
            it = it if isinstance(it, dict) else {}
            lines.append("| " + " | ".join(_cell(it.get(k), unresolved, k) for k in cols) + " |")
        return "\n".join(lines)
    if isinstance(value, dict):
        cols = keys + [k for k in value if k not in keys]
        lines = ["| key | value |", "|---|---|"]
        for k in cols:
            lines.append(f"| {k} | {_cell(value.get(k), unresolved, k)} |")
        return "\n".join(lines)
    return _fence(_scalar(value))


def _plain(value: Any) -> str:
    if isinstance(value, list) and all(not isinstance(x, (dict, list)) for x in value):
        return _fence("\n".join(_scalar(x) for x in value))
    return _fence(_scalar(value))


def _any(value: Any) -> str:
    if value is None:
        return _fence("NEEDS_INPUT")
    if isinstance(value, dict) or (isinstance(value, list) and any(isinstance(x, (dict, list)) for x in value)):
        return _fence(json.dumps(value, ensure_ascii=False, indent=1))
    return _plain(value)


# --------------------------------------------------------------------------
# arithmetic check lines
# --------------------------------------------------------------------------

def _arith(fid: str, recs: dict) -> str | None:
    def items(f):
        v = (recs.get(f) or {}).get("value")
        return [x for x in v if isinstance(x, dict)] if isinstance(v, list) else []

    def total(xs, key):
        nums = [E._num(x.get(key)) for x in xs]
        if not xs or any(n is None for n in nums):
            return None
        return sum(E.q(n) for n in nums)

    if fid == "WORK.PLAN.ACTIVITIES":
        t = total(items(fid), "weight_percent")
        if t is not None:
            return f"sum(weight_percent) = {t} (must be 100.00): {'OK' if t == E.q(100) else 'MISMATCH'}"
    if fid == "PROFILE.TEAM.MEMBERS":
        t = total(items(fid), "contribution_percent")
        if t is not None:
            return f"sum(contribution_percent) = {t} (must be 100.00): {'OK' if t == E.q(100) else 'MISMATCH'}"
    if fid == "BUDGET.PLAN.ITEMS":
        out = []
        for b in items(fid):
            f = [E._num(b.get(k)) for k in ("quantity", "persons_or_items", "times_or_months", "unit_price")]
            lt = E._num(b.get("line_total"))
            if any(x is None for x in f) or lt is None:
                out.append(f"{b.get('id')}: cannot check (a factor is missing)")
            else:
                prod = E.q(f[0] * f[1] * f[2] * f[3])
                out.append(f"{b.get('id')}: {f[0]} x {f[1]} x {f[2]} x {f[3]} = {prod}; line_total {E.q(lt)}: "
                           f"{'OK' if prod == E.q(lt) else 'MISMATCH'}")
        t = total(items(fid), "line_total")
        if t is not None:
            out.append(f"sum(line_total) = {t}")
        return "; ".join(out) if out else None
    if fid in ("BUDGET.PLAN.TOTAL", "CORE.GENERAL.REQUESTED_BUDGET", "CORE.GENERAL.TOTAL_BUDGET"):
        t = total(items("BUDGET.PLAN.ITEMS"), "line_total")
        v = E._num((recs.get(fid) or {}).get("value"))
        if t is not None and v is not None:
            return f"value {E.q(v)} vs sum of budget lines {t}: {'OK' if E.q(v) == t else 'MISMATCH'}"
    return None


# --------------------------------------------------------------------------
# context
# --------------------------------------------------------------------------

def build_context(raw: dict, result: E.Result) -> dict:
    doc = P.normalized(raw)
    recs = P.records_by_id(doc)
    reg = P.registry_by_id()
    unresolved = {ref.target for ref, _ in result.link_report.unresolved}
    by_field: dict[str, list[str]] = {}
    for f in result.findings:
        if f.severity in ("BLOCK", "REVIEW"):
            for fid in f.field_ids:
                by_field.setdefault(fid, []).append(f"{f.rule_id} {f.severity}")

    tab_order = P.tab_mapping().get("tab_order") or []
    nf = sorted(P.nriis_fields(), key=lambda n: (tab_order.index(n["tab"]) if n["tab"] in tab_order else 99,
                                                n["entry_order"]))
    tabs, meta, needs_input = [], [], []
    for n in nf:
        cfid = n["core_field_id"]
        r = reg.get(cfid) or {}
        rec = recs.get(cfid)
        value = None if rec is None else rec.get("value")
        prov = (rec or {}).get("provenance") or {}
        markers = sorted(set(list((rec or {}).get("markers") or [])))
        if value is None:
            status = "NEEDS_INPUT" if n["required"] else "EMPTY"
            basis = "no value in project.yaml" + ("" if n["required"] else " (optional)")
            if n["required"]:
                needs_input.append(cfid)
        else:
            status = rec.get("status") or "DRAFT"
            if status in ("DRAFT", "NEEDS_INPUT"):
                basis = "as authored; report-only validation, no review record"
            else:
                # v0.1 has no review or lock: a status above DRAFT can only
                # have been typed into project.yaml by hand. Show it, but say
                # that nothing backs it.
                basis = ("self-declared in project.yaml and NOT backed by any check: "
                         "GrantThai v0.1 sets no status above DRAFT")
        if value is None:
            rendered = _fence("NEEDS_INPUT" if n["required"] else "(optional, not supplied)")
        elif r.get("type") in STRUCTURED_TYPES and not isinstance(value, str):
            rendered = _table(cfid, value, unresolved)
        else:
            rendered = _plain(value)
        block = {
            "entry_order": n["entry_order"],
            "label_en": n["label_en"],
            "label_th": n["label_th"],
            "value": rendered,
            "field_id": cfid,
            "nriis_field_id": n["field_id"],
            "origin": n.get("origin") or r.get("origin") or "NEEDS_VERIFICATION",
            "provenance": (f"provenance_class={prov.get('provenance_class')}, source_type={prov.get('source_type')}, "
                           f"evidence_role={prov.get('evidence_role')}") if prov else "none (no record)",
            "render_from": ", ".join(n.get("render_from") or []),
            "conflicts": ", ".join(r.get("conflicts") or []),
            "status": status,
            "basis": basis,
            "markers": markers,
            "required": "true" if n["required"] else "false",
            "input_control": n["input_control"],
            "dependencies": ", ".join(r.get("dependencies") or n.get("dependencies") or []) or "none",
            "source_ids": ", ".join((rec or {}).get("source_ids") or []) or "none",
            "validation": ", ".join(dict.fromkeys(by_field.get(cfid, []))) or "no BLOCK/REVIEW finding",
            "authored_by": (f"{prov.get('authored_by')} (self-declared)" if prov else "none (no record)"),
            "arith": _arith(cfid, recs),
        }
        if not tabs or tabs[-1]["tab"] != n["tab"]:
            tabs.append({"tab": n["tab"], "fields": []})
        tabs[-1]["fields"].append(block)
        meta.append({
            "nriis_field_id": n["field_id"], "field_id": cfid, "origin": n.get("origin"), "tab": n["tab"],
            "entry_order": n["entry_order"],
            "required": n["required"], "status": status, "markers": markers,
            "source_ids": list((rec or {}).get("source_ids") or []),
            "authored_by": prov.get("authored_by"),
        })

    mapped = {n["core_field_id"] for n in nf}
    off_tab = {m.get("section"): m.get("reason") for m in P.tab_mapping().get("not_on_tab") or []}

    def _why_unmapped(fid):
        r = reg.get(fid)
        if r is None:
            return "chain content without a registry field (never an NRIIS field)"
        if r.get("section") in off_tab:
            return off_tab[r["section"]]
        return {"AUTHORING_CORE": "authoring core: its content reaches NRIIS only through a narrative field",
                "FUND_PROFILE": "a requirement of the bound call, not an NRIIS form field",
                "DERIVED": "calculated from other fields",
                "RECOMMENDED_EXTENSION": "structure not confirmed as an NRIIS field"}.get(r.get("origin"), "not mapped")

    feeds: dict[str, list[str]] = {}
    for n in nf:
        for src in n.get("render_from") or []:
            feeds.setdefault(src, []).append(n["core_field_id"])
    unmapped = [{"field_id": rec.get("field_id"), "chain": key or "fields", "status": rec.get("status"),
                 "origin": (reg.get(rec.get("field_id")) or {}).get("origin") or "none (not a registry field)",
                 "why": _why_unmapped(rec.get("field_id")),
                 "feeds": ", ".join(feeds.get(rec.get("field_id"), [])),
                 "value": _any(rec.get("value"))}
                for rec, key in P.iter_records(doc) if rec.get("field_id") not in mapped]

    # Conflicts and open contradictions: every package-level entry (all are
    # OPEN; none is resolved by GrantThai) with the project records it
    # touches, then every conflict the researcher recorded on a record.
    present = {rec.get("field_id") for rec, _ in P.iter_records(doc)}
    package_conflicts = []
    for cx in P.contradictions():
        aff = cx.get("affects") or {}
        touched = sorted(f for f in aff.get("fields") or [] if f in present)
        package_conflicts.append({
            "id": cx.get("id"), "title": cx.get("title"), "status": cx.get("status"),
            "readings": [f"{x.get('source')}: {x.get('says')}" for x in cx.get("readings") or []],
            "handling": cx.get("current_handling"),
            "touched": ", ".join(touched) or "no record of this project (affects "
                       + ", ".join((aff.get("files") or []) + (aff.get("fields") or [])) + ")",
        })
    project_conflicts = []
    for rec, _ in P.iter_records(doc):
        for c in rec.get("conflicts") or []:
            if isinstance(c, dict):
                project_conflicts.append({
                    "field_id": rec.get("field_id"), "id": c.get("conflict_id"), "status": c.get("status"),
                    "description": c.get("description"),
                    "readings": [(x.get("says") or "") + (f" (sources: {', '.join(x.get('source_ids') or [])})"
                                                           if x.get("source_ids") else "")
                                 for x in c.get("readings") or [] if isinstance(x, dict)],
                    "decision_note": c.get("decision_note") or "",
                })
    open_conflicts = sum(1 for c in package_conflicts if c["status"] == "OPEN") + \
        sum(1 for c in project_conflicts if c["status"] == "OPEN")

    # Readiness summary
    marked = [(rec.get("field_id"), m, rec.get("hold_reason"))
              for rec, _ in P.iter_records(doc) for m in sorted(set(rec.get("markers") or []))]
    ai_drafts = [rec.get("field_id") for rec, _ in P.iter_records(doc)
                 if ((rec.get("provenance") or {}).get("authored_by")) in AI_AUTHORED]
    record_needs_input = [rec.get("field_id") for rec, _ in P.iter_records(doc)
                          if rec.get("value") is None and rec.get("field_id") not in needs_input]
    mappings = [m for m in doc.get("mappings") or []
                if isinstance(m, dict) and m.get("acceptance_state") in ("PROPOSED", "ACCEPTED_BY_REQUESTER")]
    author_checked = [r for r in doc.get("review_records") or []
                      if isinstance(r, dict) and r.get("independence") == "self"]

    # Gates
    csha = content_sha256(raw)
    gates = {}
    records = [r for r in raw.get("review_records") or [] if isinstance(r, dict)]
    for g in ("RG0", "RG1", "RG2", "RG3", "RG4"):
        rs = [r for r in records if r.get("gate_id") == g]
        if not rs:
            gates[g] = {"state": "not_reviewed", "basis": "no review record"}
        else:
            last = rs[-1]
            cur = last.get("content_sha256") == csha
            gates[g] = {"state": ("current" if cur else "stale"),
                        "basis": f"{last.get('independence')} review by role {last.get('reviewer_role')}"}

    # Source manifest
    cited: dict[str, list[str]] = {}
    for rec, _ in P.iter_records(doc):
        for sid in rec.get("source_ids") or []:
            cited.setdefault(sid, []).append(rec.get("field_id"))
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

    lock = raw.get("lock") or {}
    locked = bool(lock.get("locked")) and lock.get("locked_content_sha256") == csha
    auth = raw.get("authoring") or {}
    summary = result.report["summary"]
    frontmatter = {
        "grantthai_version": __version__,
        "schema_version": str(raw.get("schema_version")),
        "renderer_version": RENDERER_VERSION,
        "project_id": str(raw.get("project_id")),
        "project_content_sha256": csha,
        "project_state_sha256": state_sha256(raw),
        "project_locked": locked,
        "fund_profile": result.fund_profile_id or "NEEDS_INPUT",
        "fund_profile_trust_level": result.trust_level,
        "nriis_mapping": str(P.tab_mapping().get("observed_form")),
        "authoring": {"mode": auth.get("mode", "human"),
                      "tools_disclosed": list(auth.get("tools_disclosed") or []),
                      "self_declared": True},
        "submission_mode": {"human_copy_paste": True, "ai_assisted_fill": False, "direct_submit": False},
        "human_final_approval_required": True,
        "review": gates,
        "submittable": result.submittable,
        "real_world_verified": result.real_world_verified,
        "hold_reasons": list(result.hold_reasons),
        "stale_rules": list(result.stale_rules),
        "accepted_by_requester_mappings": sorted(str(m.get("mapping_id") or m.get("id"))
                                                 for m in mappings if m.get("acceptance_state") == "ACCEPTED_BY_REQUESTER"),
        "validation_summary": dict(summary),
        "disclaimer": P.notice_constant(),
    }
    return {
        "frontmatter_yaml": yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True, width=10**6).rstrip("\n"),
        "disclaimer": P.notice_constant(),
        "project_id": str(raw.get("project_id")),
        "summary": summary,
        "submittable": result.submittable,
        "hold_reasons": result.hold_reasons,
        "blocks": [vars(f) for f in result.findings if f.severity == "BLOCK"],
        "reviews": [vars(f) for f in result.findings if f.severity == "REVIEW"],
        "infos": [vars(f) for f in result.findings if f.severity == "INFO"],
        "needs_input": needs_input,
        "record_needs_input": record_needs_input,
        "marked": marked,
        "ai_drafts": ai_drafts,
        "mappings": mappings,
        "author_checked": author_checked,
        "tab_order": tab_order,
        "tabs": tabs,
        "meta_yaml": yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, width=10**6).rstrip("\n"),
        "gates": gates,
        "sources": sources,
        "unresolved": unresolved_rows,
        "unmapped": unmapped,
        "package_conflicts": package_conflicts,
        "project_conflicts": project_conflicts,
        "open_conflicts": open_conflicts,
        "fund_profile": result.fund_profile_id or "NEEDS_INPUT",
        "trust_level": result.trust_level,
    }


def render(raw: dict, project_dir: Path | None = None, as_of: str | None = None) -> tuple[str, E.Result]:
    result = E.run(raw, project_dir, as_of)
    text = _env().get_template(TEMPLATE).render(**build_context(raw, result))
    return text, result


def build(project_path: str | Path, out_dir: str | Path | None = None, as_of: str | None = None) -> Path:
    """grantthai build: project.yaml -> <dir>/build/NRIIS_SUBMISSION.md.
    Always renders (BLOCK findings go into the readiness summary)."""
    project_path = Path(project_path).resolve()
    raw = P.load(project_path)
    text, _ = render(raw, project_path.parent, as_of)
    out = Path(out_dir) if out_dir else project_path.parent / "build"
    out.mkdir(parents=True, exist_ok=True)
    target = out / "NRIIS_SUBMISSION.md"
    target.write_text(text, encoding="utf-8", newline="\n")
    return target
