"""grantthai.mcp.tools — the MCP tool and resource surface, transport-free.

Every tool is a thin wrapper over grantthai.api_py (the same functions the
CLI calls). Nothing here talks to a model or to the network, and nothing
here can submit anything anywhere.

Hard rules kept by this module (spec/mcp/tools.schema.json):
  * no tool raises a field status above DRAFT (the engine's set_field only
    writes DRAFT or NEEDS_INPUT; this module never writes a status itself);
  * every value written over MCP is recorded as AI-assisted
    (actor="ai_assisted"): an AI's own wording is authored_by ai_draft and
    INFERENCE, and a value the researcher dictated word for word is
    authored_by human_ai_assisted and DECISION. SOURCE is never offered;
  * grantthai_validate is report-only; grantthai_build writes exactly one
    file, build/NRIIS_SUBMISSION.md, next to project.yaml (or in out_dir);
  * file paths are resolved inside one root folder (default: the server's
    working directory) and may not escape it.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from grantthai import __version__
from grantthai import api_py as api
from grantthai.core import pii as _PII
from grantthai.core import project as _P

SERVER_NAME = "grantthai"
DEFAULT_TOOL_NAME = "mcp-client"

NOTICE_URI = "grantthai://notice"
FIELDS_URI = "grantthai://fields"

INSTRUCTIONS = (
    "GrantThai turns one project.yaml into one overview file, build/NRIIS_SUBMISSION.md. "
    "The researcher's own information is the source. You (the AI) draft; the researcher "
    "confirms. Values you write are stored as AI drafts at status DRAFT and listed in the "
    "output for the researcher to confirm. Never invent Thai fund, NRIIS or institutional "
    "facts: write the literal value NEEDS_VERIFICATION instead. Validation findings are a "
    "report, not a verdict on the research. Nothing here submits anything to NRIIS or any fund. "
    "BEFORE you accept any research data from the researcher, show them this warning (data_warning in "
    "the grantthai_new_project result): " + _PII.DATA_WARNING_EN + " "
    "Every grantthai_set_field call records your tool name and version in "
    "authoring.ai_use_declaration.tools; only the researcher fills in the rest and confirms it. "
    "Typical flow: grantthai_new_project -> grantthai_list_fields -> grantthai_set_field (repeat) "
    "-> grantthai_validate -> grantthai_build."
)


class ToolError(Exception):
    """A tool-level failure, reported to the client as isError."""


@dataclass
class Context:
    """Per-server state: the folder all paths live in, and the client name
    and version (from MCP initialize) used as the disclosed tool when none
    is given."""
    root: Path = field(default_factory=Path.cwd)
    client_name: str | None = None
    client_version: str | None = None

    def path(self, rel: str | None, default: str | None = None) -> Path:
        raw = rel if rel not in (None, "") else default
        if raw is None:
            raise ToolError("a path is required")
        root = self.root.resolve()
        p = Path(raw)
        p = (p if p.is_absolute() else root / p).resolve()
        if p != root and root not in p.parents:
            raise ToolError(f"path {raw!r} is outside the GrantThai root folder {root}")
        return p

    def rel(self, p: Path) -> str:
        try:
            return p.resolve().relative_to(self.root.resolve()).as_posix()
        except ValueError:
            return str(p)


# ---------------------------------------------------------------------------
# JSON Schemas for tool inputs
# ---------------------------------------------------------------------------

_PROJECT_PATH = {
    "type": "string",
    "description": "Path to project.yaml, relative to the GrantThai root folder. Default: project.yaml.",
    "default": "project.yaml",
}
_AS_OF = {
    "type": "string",
    "pattern": r"^\d{4}-\d{2}-\d{2}$",
    "description": "Date (YYYY-MM-DD) used for fund-rule staleness checks. Default: today. "
                   "Two builds of the same input with the same as_of are byte-identical.",
}

TOOL_SPECS: list[dict] = [
    {
        "name": "grantthai_new_project",
        "wraps_cli_command": "grantthai init",
        "status_effect": "draft_only",
        "annotations": {"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False,
                        "openWorldHint": False},
        "description": (
            "Create a blank project.yaml. Every required field is present with status NEEDS_INPUT. "
            "Refuses to overwrite an existing file."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_path": _PROJECT_PATH,
                "project_id": {"type": "string", "default": "NEEDS_INPUT",
                               "description": "Researcher's own project id; leave NEEDS_INPUT if unknown."},
                "fund_profile_id": {"type": "string", "default": _P.DEFAULT_FUND_PROFILE,
                                    "description": "Fund profile id. Only the FICTIONAL example profile ships in v0.1."},
                "mode": {"type": "string", "enum": ["expert", "human_direct"], "default": "expert"},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "grantthai_list_fields",
        "wraps_cli_command": "grantthai fields",
        "status_effect": "none",
        "annotations": {"readOnlyHint": True, "openWorldHint": False},
        "description": (
            "List every field: first the NRIIS boxes in entry order, then fields that are not NRIIS boxes "
            "(tab NOT_ON_TAB: research core, methodology, fund-profile and derived fields, still filled in "
            "project.yaml). Gives field_id, tab, origin, type, whether required, English label, guidance. "
            "Thai labels and NRIIS tab names are NEEDS_VERIFICATION; do not guess them."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "tab": {"type": "string", "description": "Only this tab."},
                "required_only": {"type": "boolean", "default": False},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "grantthai_set_field",
        "wraps_cli_command": "grantthai set",
        "status_effect": "draft_only",
        "annotations": {"readOnlyHint": False, "destructiveHint": False, "idempotentHint": True,
                        "openWorldHint": False},
        "description": (
            "Write one field into project.yaml. The record is always status DRAFT (or NEEDS_INPUT when the "
            "value is null / \"NEEDS_INPUT\") and is recorded as AI-assisted, so the output lists it for the "
            "researcher to confirm. Set researcher_verbatim=true only when the value is exactly what the "
            "researcher told you; otherwise it is stored as your draft (ai_draft, INFERENCE). A value can "
            "never be marked SOURCE from here. If a Thai fund, NRIIS or institutional fact is not in the "
            "researcher's own material, write the literal value \"NEEDS_VERIFICATION\"."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_path": _PROJECT_PATH,
                "field_id": {"type": "string", "minLength": 1,
                             "description": "A field_id from grantthai_list_fields, or a chain record id with chain_node."},
                "value": {"description": "The value (string, number, boolean, list or object as the field type needs). "
                                         "null or \"NEEDS_INPUT\" clears it; \"NEEDS_VERIFICATION\" marks it unconfirmed."},
                "researcher_verbatim": {"type": "boolean", "default": False,
                                        "description": "True only if the value is the researcher's own words, unchanged."},
                "chain_node": {"type": "string",
                               "description": "For chain content not in the registry (e.g. PriorKnowledge, Evidence, Claim)."},
                "source_ids": {"type": "array", "items": {"type": "string"},
                               "description": "Ids of the researcher's sources (SRC-...) this value rests on."},
                "links": {"type": "object", "description": "Chain links for this record, as the engine expects."},
                "tool": {"type": "string",
                         "description": "Name of the AI tool drafting (disclosed in the output and recorded in "
                                        "authoring.ai_use_declaration.tools). Default: the MCP client's name."},
                "tool_version": {"type": "string",
                                 "description": "The tool's version. Default: the MCP client's version, if it sent one."},
                "stage": {"type": "string", "enum": list(_P.AI_USE_STAGES),
                          "description": f"Research stage of this AI use. Default: {_P.DEFAULT_AI_STAGE}."},
            },
            "required": ["field_id", "value"],
            "additionalProperties": False,
        },
    },
    {
        "name": "grantthai_validate",
        "wraps_cli_command": "grantthai validate",
        "status_effect": "none",
        "annotations": {"readOnlyHint": True, "openWorldHint": False},
        "description": (
            "Check project.yaml and return the validation report (BLOCK / REVIEW / INFO findings). "
            "Report-only: never changes project.yaml and never judges the research itself."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {"project_path": _PROJECT_PATH, "as_of": _AS_OF},
            "additionalProperties": False,
        },
    },
    {
        "name": "grantthai_explain",
        "wraps_cli_command": "grantthai explain",
        "status_effect": "none",
        "annotations": {"readOnlyHint": True, "openWorldHint": False},
        "description": "Explain one validation rule id (e.g. S001, B002, SCHEMA).",
        "inputSchema": {
            "type": "object",
            "properties": {"rule_id": {"type": "string", "minLength": 1}},
            "required": ["rule_id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "grantthai_build",
        "wraps_cli_command": "grantthai build",
        "status_effect": "none",
        "annotations": {"readOnlyHint": False, "destructiveHint": False, "idempotentHint": True,
                        "openWorldHint": False},
        "description": (
            "Render exactly one file, build/NRIIS_SUBMISSION.md, from project.yaml and return its path and "
            "Markdown content. Always renders, even with BLOCK findings (they are listed in the file). "
            "This is an overview for the researcher to check; it submits nothing."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_path": _PROJECT_PATH,
                "out_dir": {"type": "string",
                            "description": "Folder to write NRIIS_SUBMISSION.md into. Default: build/ next to project.yaml."},
                "as_of": _AS_OF,
            },
            "additionalProperties": False,
        },
    },
]

TOOLS_BY_NAME = {t["name"]: t for t in TOOL_SPECS}

RESOURCE_SPECS: list[dict] = [
    {"uri": NOTICE_URI, "name": "notice", "mimeType": "text/plain",
     "description": "The independence notice printed on line 1 of every NRIIS_SUBMISSION.md body."},
    {"uri": FIELDS_URI, "name": "fields", "mimeType": "application/json",
     "description": "The whole field registry, NRIIS boxes first in entry order (same data as grantthai_list_fields)."},
]


def list_tools() -> list[dict]:
    """Tool definitions in MCP tools/list shape."""
    return [{"name": t["name"], "description": t["description"], "inputSchema": t["inputSchema"],
             "annotations": t["annotations"]} for t in TOOL_SPECS]


def list_resources() -> list[dict]:
    return [dict(r) for r in RESOURCE_SPECS]


def read_resource(uri: str) -> tuple[str, str]:
    """Return (text, mime_type) for a resource uri."""
    uri = str(uri)
    if uri == NOTICE_URI:
        return _P.notice_constant(), "text/plain"
    if uri == FIELDS_URI:
        return json.dumps(api.list_fields(), ensure_ascii=False, indent=2), "application/json"
    raise ToolError(f"unknown resource {uri!r}")


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------

def _new_project(ctx: Context, a: dict) -> dict:
    p = ctx.path(a.get("project_path"), "project.yaml")
    doc = api.new_project(a.get("project_id") or "NEEDS_INPUT",
                          a.get("fund_profile_id") or _P.DEFAULT_FUND_PROFILE,
                          a.get("mode") or "expert", path=p)
    needs = [r["field_id"] for r, _ in _P.iter_records(doc) if r.get("status") == "NEEDS_INPUT"]
    return {"project_path": ctx.rel(p), "needs_input": needs,
            "data_warning": {"en": _PII.DATA_WARNING_EN, "th": _PII.DATA_WARNING_TH},
            "next": "Show the researcher data_warning first. Then ask for each NEEDS_INPUT field and call "
                    "grantthai_set_field."}


def _list_fields(ctx: Context, a: dict) -> dict:
    fields = api.list_fields(tab=a.get("tab"), required_only=bool(a.get("required_only")))
    return {"count": len(fields), "fields": fields}


def _set_field(ctx: Context, a: dict) -> dict:
    p = ctx.path(a.get("project_path"), "project.yaml")
    if not p.exists():
        raise ToolError(f"{ctx.rel(p)} does not exist; call grantthai_new_project first")
    if "value" not in a:
        raise ToolError("value is required (use null to clear)")
    verbatim = bool(a.get("researcher_verbatim"))
    prov = ({"provenance_class": "DECISION", "authored_by": "human_ai_assisted"} if verbatim
            else {"provenance_class": "INFERENCE", "authored_by": "ai_draft"})
    tool = a.get("tool") or ctx.client_name or DEFAULT_TOOL_NAME
    version = a.get("tool_version") or (ctx.client_version if not a.get("tool") else None)
    rec = api.set_field(p, a["field_id"], a["value"], actor="ai_assisted",
                        chain_node=a.get("chain_node"), provenance=prov,
                        source_ids=a.get("source_ids"), links=a.get("links"), tool=tool,
                        tool_version=version, stage=a.get("stage"))
    return {"project_path": ctx.rel(p), "record": rec,
            "note": "Stored as an AI-assisted DRAFT. The researcher must confirm it; "
                    "the output lists it under AI-drafted values."}


def _validate(ctx: Context, a: dict) -> dict:
    p = ctx.path(a.get("project_path"), "project.yaml")
    if not p.exists():
        raise ToolError(f"{ctx.rel(p)} does not exist")
    return api.validate(p, as_of=a.get("as_of"))


def _explain(ctx: Context, a: dict) -> dict:
    return api.explain(a["rule_id"])


def _build(ctx: Context, a: dict) -> dict:
    p = ctx.path(a.get("project_path"), "project.yaml")
    if not p.exists():
        raise ToolError(f"{ctx.rel(p)} does not exist")
    out_dir = ctx.path(a["out_dir"]) if a.get("out_dir") else None
    out = api.build(p, out_dir=out_dir, as_of=a.get("as_of"))
    report = api.validate(p, as_of=a.get("as_of"))
    return {"path": ctx.rel(out), "summary": report.get("summary"),
            "markdown": Path(out).read_text(encoding="utf-8"),
            "note": "Overview for the researcher to check. Nothing was submitted anywhere."}


HANDLERS: dict[str, Callable[[Context, dict], dict]] = {
    "grantthai_new_project": _new_project,
    "grantthai_list_fields": _list_fields,
    "grantthai_set_field": _set_field,
    "grantthai_validate": _validate,
    "grantthai_explain": _explain,
    "grantthai_build": _build,
}


def call_tool(ctx: Context, name: str, arguments: dict | None) -> dict:
    """Run one tool. Returns the structured result; raises ToolError for any
    failure the client should see as isError."""
    handler = HANDLERS.get(name)
    if handler is None:
        raise ToolError(f"unknown tool {name!r}")
    args = dict(arguments or {})
    try:
        import jsonschema
        jsonschema.validate(args, TOOLS_BY_NAME[name]["inputSchema"])
    except jsonschema.ValidationError as exc:
        raise ToolError(f"invalid arguments for {name}: {exc.message}") from None
    try:
        return handler(ctx, args)
    except ToolError:
        raise
    except (ValueError, KeyError, FileExistsError, FileNotFoundError, OSError) as exc:
        raise ToolError(str(exc).strip("'\"")) from None


def server_info() -> dict:
    return {"name": SERVER_NAME, "version": __version__}


def dumps(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2, default=str)
