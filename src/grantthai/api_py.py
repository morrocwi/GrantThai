"""grantthai.api_py — the small, stable Python API over the v0.1 engine.

This is the one surface the optional skill, MCP server and HTTP API wrap.
It is AI-free: nothing here calls a model. Any caller (a person's script
or an AI agent) gets the same hard ceiling, enforced in grantthai.core:
statuses never go above DRAFT, an AI-drafted value (actor="ai_assisted")
is stored as authored_by ai_draft and can never be provenance_class
SOURCE, and validation is report-only.

    new_project(project_id=..., fund_profile_id=..., mode=..., path=None) -> dict
    set_field(project, field_id, value, *, actor="human", chain_node=None,
              provenance=None, source_ids=None, links=None, tool=None,
              tool_version=None, stage=None, save=True) -> dict
    validate(project, *, as_of=None, route=None, sub_profile=None) -> dict   # validation report
    build(path=None, *, route=None, sub_profile=None, out_dir=None, as_of=None) -> Path
                                                       # exactly one build/<route output file>
    new_work(work_id=..., work_type=..., fund_profile_id=None, mode=..., path=None) -> dict   # work.yaml 0.3
    list_routes() -> list[dict]                        # every route; never picks one
    resolve_route(project, route=None) -> str          # ValueError (AmbiguousRoute, .candidates) if a person must choose
    check_route(work, route, *, sub_profile=None, as_of=None) -> dict   # route-scoped validation report
    migrate(path, *, rename=False, dry_run=False) -> dict               # 0.2 project.yaml -> work.yaml 0.3
    record_ai_tool(project, name, *, version=None, stage=None, save=True) -> bool
    data_warning() -> dict                             # {"en", "th"}: show before accepting data
    explain(rule_id) -> dict
    list_fields(*, tab=None, required_only=False, route=None) -> list[dict]
        # route None / nriis-proposal: whole registry, tab NOT_ON_TAB for non-NRIIS fields;
        # another route: its placement order, then NOT_PLACED

`project` is either a path (a work.yaml / project.yaml file, or a
directory holding exactly one of them) or an already-loaded dict. A route
is always the researcher's choice: with no route and no declared
default the call raises instead of picking one.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from grantthai import render as _RD
from grantthai.core import project as _P
from grantthai.routes import registry as _RT
from grantthai.routes import resolve as _RS
from grantthai.validators import engine as _E

NOT_ON_TAB = "NOT_ON_TAB"
NOT_PLACED = "NOT_PLACED"
AmbiguousRoute = _RS.AmbiguousRoute
TwoCanonicalInputs = _P.TwoCanonicalInputs

__all__ = ["new_project", "new_work", "set_field", "validate", "build", "explain", "list_fields", "load", "save",
           "list_routes", "resolve_route", "check_route", "migrate", "AmbiguousRoute", "TwoCanonicalInputs"]


def load(path: str | Path) -> dict:
    return _P.load(path)


def save(project: dict, path: str | Path) -> Path:
    return _P.save(project, path)


def new_project(project_id: str = "NEEDS_INPUT", fund_profile_id: str = _P.DEFAULT_FUND_PROFILE,
                mode: str = "expert", path: str | Path | None = None) -> dict:
    """A blank project object (required fields present as NEEDS_INPUT).
    Written to `path` when given; refuses to overwrite an existing file."""
    doc = _P.new_project(project_id, fund_profile_id, mode)
    if path is not None:
        p = Path(path)
        if p.exists():
            raise FileExistsError(f"{p} already exists; refusing to overwrite")
        _P.save(doc, p)
    return doc


def new_work(work_id: str = "NEEDS_INPUT", work_type: str = _P.LEGACY_WORK_TYPE,
             fund_profile_id: str | None = None, mode: str = "expert",
             path: str | Path | None = None) -> dict:
    """A blank work.yaml 0.3 object. `routing` is not written: the route is
    the researcher's own declaration. Fields present as NEEDS_INPUT are the
    required set of the one route that is the default for `work_type`
    (the registry's required flags for nriis-proposal), or the registry's
    required flags when no single route is the default. Written to `path`
    when given; refuses to overwrite an existing file."""
    wt_routes = [rid for rid in _RT.route_ids() if work_type in _RT.load(rid).default_for_work_types]
    required = None
    if len(wt_routes) == 1 and _RT.load(wt_routes[0]).required_fields != "registry":
        required = list(_RT.load(wt_routes[0]).required_fields)
    if len(wt_routes) == 1 and _RT.load(wt_routes[0]).needs_fund_binding and fund_profile_id is None:
        fund_profile_id = _P.DEFAULT_FUND_PROFILE
    doc = _P.new_work(work_id, work_type, fund_profile_id, mode, required_fields=required)
    errs = _P.schema_errors(doc, _P.WORK_SCHEMA_ID)
    if errs:
        raise ValueError("new work object fails spec/work/work.schema.json: " + "; ".join(errs))
    if path is not None:
        p = Path(path)
        if p.exists():
            raise FileExistsError(f"{p} already exists; refusing to overwrite")
        _P.save(doc, p)
    return doc


def set_field(project: str | Path | dict, field_id: str, value: Any, *, actor: str = "human",
              chain_node: str | None = None, provenance: dict | None = None,
              source_ids: list[str] | None = None, links: dict | None = None,
              tool: str | None = None, tool_version: str | None = None,
              stage: str | None = None, save: bool = True) -> dict:
    """Set one field. With a path, loads, edits and (save=True) writes the
    file back. Returns the written record."""
    if isinstance(project, dict):
        return _P.set_field(project, field_id, value, actor=actor, chain_node=chain_node,
                            provenance=provenance, source_ids=source_ids, links=links, tool=tool,
                            tool_version=tool_version, stage=stage)
    doc = _P.load(project)
    rec = _P.set_field(doc, field_id, value, actor=actor, chain_node=chain_node,
                       provenance=provenance, source_ids=source_ids, links=links, tool=tool,
                       tool_version=tool_version, stage=stage)
    if save:
        _P.save(doc, project)
    return rec


def record_ai_tool(project: str | Path | dict, name: str, *, version: str | None = None,
                   stage: str | None = None, save: bool = True) -> bool:
    """Record an AI tool in authoring.ai_use_declaration.tools (and
    tools_disclosed) without writing a field. Returns True when tools[]
    changed; the researcher's confirmation is then reset to false."""
    if isinstance(project, dict):
        return _P.record_ai_tool(project, name, version=version, stage=stage)
    doc = _P.load(project)
    changed = _P.record_ai_tool(doc, name, version=version, stage=stage)
    if save:
        _P.save(doc, project)
    return changed


def data_warning() -> dict:
    """The warning to show the researcher before accepting any research
    data (docs/policy/ai-use-ceiling.md section 5)."""
    from grantthai.core import pii
    return {"en": pii.DATA_WARNING_EN, "th": pii.DATA_WARNING_TH}


def _loaded(project: str | Path | dict) -> tuple[dict, Path | None]:
    if isinstance(project, dict):
        return project, None
    p = _P.discover(project).resolve()
    return _P.load(p), p.parent


def validate(project: str | Path | dict, *, as_of: str | None = None, route: str | None = None,
             sub_profile: str | None = None) -> dict:
    """Validation report (spec/common/validation_report.schema.json) for
    one route. With no route: routing.default_route, a legacy project.yaml
    -> nriis-proposal, the single default route for work_type, else
    AmbiguousRoute (a ValueError listing the candidates). Report-only:
    never changes the work file."""
    raw, folder = _loaded(project)
    rid = _RS.resolve_route(raw, route)
    return _E.run(raw, folder, as_of, route=rid, sub_profile=sub_profile).report


def check_route(work: str | Path | dict, route: str, *, sub_profile: str | None = None,
                as_of: str | None = None) -> dict:
    """grantthai route check: the validation report for an explicitly
    named route. Report-only."""
    if not route:
        raise ValueError("check_route needs a route; list them with list_routes()")
    return validate(work, as_of=as_of, route=route, sub_profile=sub_profile)


def resolve_route(project: str | Path | dict, route: str | None = None) -> str:
    """The route a build would use (resolution order in
    grantthai.routes.resolve). Raises AmbiguousRoute (ValueError, with
    .candidates) when the researcher has to choose."""
    raw, _ = _loaded(project)
    return _RS.resolve_route(raw, route)


def list_routes() -> list[dict]:
    """Every output route (routes/INDEX.yaml): id, title_en, status,
    output_filename, accepts_work_types, default_for_work_types,
    needs_fund_binding, ready_flag. Listing never chooses one."""
    return _RT.list_routes()


def build(path: str | Path | None = None, *, route: str | None = None, sub_profile: str | None = None,
          out_dir: str | Path | None = None, as_of: str | None = None) -> Path:
    """One work object -> exactly one build/<route output filename>
    (NRIIS_SUBMISSION.md for nriis-proposal, the legacy default). Always
    renders; BLOCK findings are listed in the file's readiness summary.
    Raises AmbiguousRoute (ValueError) when no route can be resolved and
    TwoCanonicalInputs when work.yaml and project.yaml sit side by side."""
    return _RD.build_route(path, route, sub_profile=sub_profile, out_dir=out_dir, as_of=as_of)


def migrate(path: str | Path, *, rename: bool = False, dry_run: bool = False) -> dict:
    """Rewrite a legacy 0.2 project.yaml as work.yaml 0.3 (work_type,
    routing; form_profile moved to routing.sub_profiles.nriis-proposal).
    Returns which review gates go stale; dry_run writes nothing."""
    return _P.migrate(path, rename=rename, dry_run=dry_run)


def explain(rule_id: str) -> dict:
    return _E.explain(rule_id)


def _placement_fields(route: "_RT.Route") -> list[tuple[str, str, int]]:
    """(field_id, section id, position) in the route's placement order."""
    doc = _P._read_yaml(route.placement) or {}
    secs = doc.get("sections") or []
    if isinstance(secs, dict):
        order = doc.get("section_order") or list(secs)
        secs = [dict(secs[k] or {}, id=k) for k in order if k in secs]
    out = []
    for sec in secs:
        sid = sec.get("id") or sec.get("section")
        for i, f in enumerate(sec.get("fields") or [], start=1):
            fid = f.get("field_id") if isinstance(f, dict) else f
            if isinstance(fid, str):
                out.append((fid, str(sid), i))
    return out


def list_fields(*, tab: str | None = None, required_only: bool = False, route: str | None = None) -> list[dict]:
    """Fields for one route. route None or nriis-proposal: the legacy
    listing below. Another route: the fields its placement file orders, in
    that order (tab = the placement section id), then every other registry
    field with tab "NOT_PLACED"; `required` is the route's required_fields.

    Every registry field. Fields placed on an NRIIS tab (origin
    NRIIS_NATIVE) come first, in NRIIS entry order; every other field
    follows in registry order with tab "NOT_ON_TAB" (research core,
    methodology, fund-profile and derived fields: filled in project.yaml,
    never pasted as an NRIIS box). Thai labels are NEEDS_VERIFICATION."""
    reg = _P.registry_by_id()
    if route and route != _P.LEGACY_ROUTE:
        rt = _RT.load(route)
        placed_rows = _placement_fields(rt)
        seen = {fid for fid, _, _ in placed_rows}
        rest_rows = [(r["field_id"], NOT_PLACED, i) for i, r in
                     enumerate((r for r in _P.registry() if r["field_id"] not in seen), start=1)]
        req_set = set(rt.required_fields) if rt.required_fields != "registry" else \
            {r["field_id"] for r in _P.registry() if r.get("required")}
        out = []
        for fid, t, pos in placed_rows + rest_rows:
            r = reg.get(fid, {})
            req = fid in req_set
            if (tab and t != tab) or (required_only and not req):
                continue
            out.append({
                "field_id": fid, "tab": t, "entry_order": pos,
                "label_en": r.get("label_en"), "label_th": r.get("label_th"), "type": r.get("type"),
                "cardinality": r.get("cardinality"), "required": req, "origin": r.get("origin"),
                "chain_node": r.get("chain_node"), "allowed_values": r.get("allowed_values"),
                "guidance_en": (r.get("guidance") or {}).get("en"),
            })
        return out
    order = _P.tab_mapping().get("tab_order") or []
    placed = sorted(_P.nriis_fields(), key=lambda n: (order.index(n["tab"]) if n["tab"] in order else 99,
                                                      n["entry_order"]))
    rows = [(n["core_field_id"], n["tab"], n["entry_order"], n) for n in placed]
    on_tab = {n["core_field_id"] for n in placed}
    rest = [r for r in _P.registry() if r["field_id"] not in on_tab]
    rows += [(r["field_id"], NOT_ON_TAB, i, None) for i, r in enumerate(rest, start=1)]
    out = []
    for fid, t, pos, n in rows:
        r = reg.get(fid, {})
        req = bool(n["required"] if n else r.get("required"))
        if tab and t != tab:
            continue
        if required_only and not req:
            continue
        out.append({
            "field_id": fid, "tab": t, "entry_order": pos,
            "label_en": r.get("label_en"), "label_th": r.get("label_th"), "type": r.get("type"),
            "cardinality": r.get("cardinality"), "required": req, "origin": r.get("origin"),
            "chain_node": r.get("chain_node"), "allowed_values": r.get("allowed_values"),
            "guidance_en": (r.get("guidance") or {}).get("en"),
        })
    return out
