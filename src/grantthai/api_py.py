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
    validate(project, *, as_of=None) -> dict          # validation report
    build(path, *, out_dir=None, as_of=None) -> Path  # build/NRIIS_SUBMISSION.md
    record_ai_tool(project, name, *, version=None, stage=None, save=True) -> bool
    data_warning() -> dict                             # {"en", "th"}: show before accepting data
    explain(rule_id) -> dict
    list_fields(*, tab=None, required_only=False) -> list[dict]   # whole registry; tab NOT_ON_TAB for non-NRIIS fields

`project` is either a path to project.yaml or an already-loaded dict.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from grantthai.core import project as _P
from grantthai.render import submission as _R
from grantthai.validators import engine as _E

NOT_ON_TAB = "NOT_ON_TAB"

__all__ = ["new_project", "set_field", "validate", "build", "explain", "list_fields", "load", "save"]


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


def validate(project: str | Path | dict, *, as_of: str | None = None) -> dict:
    """Validation report (spec/common/validation_report.schema.json).
    Report-only: never changes project.yaml."""
    if isinstance(project, dict):
        return _E.run(project, None, as_of).report
    p = Path(project).resolve()
    return _E.run(_P.load(p), p.parent, as_of).report


def build(path: str | Path, *, out_dir: str | Path | None = None, as_of: str | None = None) -> Path:
    """project.yaml -> exactly one build/NRIIS_SUBMISSION.md. Always renders;
    BLOCK findings are listed in the file's readiness summary."""
    return _R.build(path, out_dir, as_of)


def explain(rule_id: str) -> dict:
    return _E.explain(rule_id)


def list_fields(*, tab: str | None = None, required_only: bool = False) -> list[dict]:
    """Every registry field. Fields placed on an NRIIS tab (origin
    NRIIS_NATIVE) come first, in NRIIS entry order; every other field
    follows in registry order with tab "NOT_ON_TAB" (research core,
    methodology, fund-profile and derived fields: filled in project.yaml,
    never pasted as an NRIIS box). Thai labels are NEEDS_VERIFICATION."""
    reg = _P.registry_by_id()
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
