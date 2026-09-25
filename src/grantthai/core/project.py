"""grantthai.core.project — the project object model for v0.1.

Load and save the one input (``project.yaml``), validate documents against
the shipped JSON Schemas through a LOCAL registry (every
``spec/**/*.schema.json`` keyed by its ``$id``; nothing is ever fetched
from the network), and edit field records under the status hard ceiling
of ``spec/common/status_permissions.yaml``.

Hard ceiling, enforced here and nowhere else: an edit made through this
module can only leave a record at ``DRAFT`` (or ``NEEDS_INPUT`` when the
value is cleared). There is no function in the core that raises a status
above ``DRAFT`` in v0.1. An AI-drafted value can never carry the
provenance class ``SOURCE``: the researcher's own information is the
source; an AI draft is ``INFERENCE`` until a person confirms it.
"""
from __future__ import annotations

import copy
import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from grantthai.core.object_hash import load_project_text

# Repository data root (spec/, registry/, validators/, templates/, funds/,
# mappings/). GRANTTHAI_HOME overrides it; otherwise the source checkout
# this module lives in (src/grantthai/core/project.py -> repo root).
DATA_ROOT = Path(os.environ.get("GRANTTHAI_HOME") or Path(__file__).resolve().parents[3])

PROJECT_SCHEMA_ID = "https://github.com/morrocwi/GrantThai/spec/project/project.schema.json"
FUND_SCHEMA_ID = "https://github.com/morrocwi/GrantThai/spec/fund/fund-profile.schema.json"
STRUCTURED_SCHEMA_ID = "https://github.com/morrocwi/GrantThai/spec/registry/structured_fields.schema.json"
REPORT_SCHEMA_ID = "https://github.com/morrocwi/GrantThai/spec/common/validation_report.schema.json"

SCHEMA_VERSION = "0.2.0-draft"
DEFAULT_FUND_PROFILE = "example/FICTIONAL_CALL@0.1"

ACTORS = ("human", "ai_assisted")
AI_AUTHORED = ("ai_draft", "human_ai_assisted")


# --------------------------------------------------------------------------
# Shipped data (read once, from DATA_ROOT only)
# --------------------------------------------------------------------------

def _read_yaml(rel: str) -> Any:
    return yaml.safe_load((DATA_ROOT / rel).read_text(encoding="utf-8"))


def _read_jsonl(rel: str) -> list[dict]:
    text = (DATA_ROOT / rel).read_text(encoding="utf-8")
    return [json.loads(line) for line in text.splitlines() if line.strip()]


@lru_cache(maxsize=None)
def registry() -> tuple[dict, ...]:
    return tuple(_read_jsonl("registry/fields.jsonl"))


@lru_cache(maxsize=None)
def registry_by_id() -> dict:
    return {r["field_id"]: r for r in registry()}


@lru_cache(maxsize=None)
def nriis_fields() -> tuple[dict, ...]:
    return tuple(_read_jsonl("registry/nriis-fields.jsonl"))


@lru_cache(maxsize=None)
def rules_catalog() -> dict:
    return _read_yaml("validators/rules.yaml")


@lru_cache(maxsize=None)
def chain_config() -> dict:
    return _read_yaml("spec/common/chain.yaml")


@lru_cache(maxsize=None)
def tab_mapping() -> dict:
    return _read_yaml("mappings/nriis/section_to_tab.yaml")


@lru_cache(maxsize=None)
def notice_constant() -> str:
    raw = (DATA_ROOT / "spec/output/notice_constant.txt").read_text(encoding="utf-8")
    return raw.rstrip("\n")


@lru_cache(maxsize=None)
def _schemas() -> dict:
    out = {}
    for path in sorted((DATA_ROOT / "spec").rglob("*.schema.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        if "$id" in doc:
            out[doc["$id"]] = doc
    return out


def schema(schema_id: str) -> dict:
    return _schemas()[schema_id]


@lru_cache(maxsize=None)
def _registry():
    """A referencing.Registry holding every shipped schema by $id. It has no
    retrieve hook, so an unknown $ref raises instead of fetching a URL."""
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012

    resources = [(sid, Resource.from_contents(doc, default_specification=DRAFT202012))
                 for sid, doc in _schemas().items()]
    return Registry().with_resources(resources)


def schema_errors(instance: Any, schema_id: str, pointer: str | None = None) -> list[str]:
    """Validate `instance` against a shipped schema, or against the
    subschema at JSON pointer `pointer` inside it (e.g. "/$defs/X").
    Returns human-readable error strings, sorted."""
    import jsonschema

    target = schema(schema_id) if pointer is None else {"$ref": schema_id + "#" + pointer}
    validator = jsonschema.Draft202012Validator(target, registry=_registry())
    errs = []
    for e in validator.iter_errors(instance):
        where = "/".join(str(p) for p in e.absolute_path) or "(root)"
        errs.append(f"{where}: {e.message}")
    return sorted(errs)


# --------------------------------------------------------------------------
# Load / save
# --------------------------------------------------------------------------

def load(path: str | Path) -> dict:
    doc = load_project_text(Path(path).read_text(encoding="utf-8"))
    if not isinstance(doc, dict):
        raise ValueError(f"{path}: project.yaml must be a mapping at top level")
    return doc


def dump_text(doc: dict) -> str:
    return yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100)


def save(doc: dict, path: str | Path) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(dump_text(doc), encoding="utf-8", newline="\n")
    return p


def load_fund_profile(doc: dict) -> tuple[dict | None, str | None, list[str]]:
    """Resolve fund_binding.fund_profile_id to funds/<id>/fund-profile.yaml.
    Returns (profile, id, problems)."""
    fid = ((doc.get("fund_binding") or {}).get("fund_profile_id"))
    if not isinstance(fid, str) or not fid:
        return None, None, ["fund_binding.fund_profile_id is missing"]
    path = DATA_ROOT / "funds" / fid / "fund-profile.yaml"
    if ".." in Path(fid).parts or not path.is_file():
        return None, fid, [f"no fund profile at funds/{fid}/fund-profile.yaml"]
    prof = load_project_text(path.read_text(encoding="utf-8"))
    problems = [f"fund profile: {e}" for e in schema_errors(prof, FUND_SCHEMA_ID)]
    if isinstance(prof, dict) and prof.get("id") != fid:
        problems.append(f"fund profile id {prof.get('id')!r} does not equal the bound id {fid!r}")
    return prof, fid, problems


# --------------------------------------------------------------------------
# Records
# --------------------------------------------------------------------------

def iter_records(doc: dict):
    """(record, chain_key or None) for every field record, file order."""
    for rec in doc.get("fields") or []:
        if isinstance(rec, dict):
            yield rec, None
    for key, recs in (doc.get("chain") or {}).items():
        for rec in recs or []:
            if isinstance(rec, dict):
                yield rec, key


def records_by_id(doc: dict) -> dict:
    out = {}
    for rec, _ in iter_records(doc):
        fid = rec.get("field_id")
        if isinstance(fid, str) and fid not in out:
            out[fid] = rec
    return out


def normalized(doc: dict) -> dict:
    """A copy where the literal value "NEEDS_INPUT" reads as null +
    status NEEDS_INPUT and "NEEDS_VERIFICATION" as null + that marker
    (spec/common/field_record.schema.json)."""
    out = copy.deepcopy(doc)
    for rec, _ in iter_records(out):
        v = rec.get("value")
        if v == "NEEDS_INPUT":
            rec["value"] = None
            rec["status"] = "NEEDS_INPUT"
        elif v == "NEEDS_VERIFICATION":
            rec["value"] = None
            markers = list(rec.get("markers") or [])
            if "NEEDS_VERIFICATION" not in markers:
                markers.append("NEEDS_VERIFICATION")
            rec["markers"] = markers
    return out


def _default_provenance(actor: str) -> dict:
    if actor == "ai_assisted":
        return {"provenance_class": "INFERENCE", "source_type": "PROJECT_DOCUMENT",
                "evidence_role": "ORIENTING", "authored_by": "ai_draft"}
    return {"provenance_class": "DECISION", "source_type": "PROJECT_DOCUMENT",
            "evidence_role": "ORIENTING", "authored_by": "human"}


def new_project(project_id: str = "NEEDS_INPUT", fund_profile_id: str = DEFAULT_FUND_PROFILE,
                mode: str = "expert") -> dict:
    """A blank project.yaml object. Every required registry field is present
    as value null / status NEEDS_INPUT so the file doubles as a form."""
    doc: dict = {
        "schema_version": SCHEMA_VERSION,
        "project_id": project_id,
        "mode": mode,
        "authoring": {"mode": "human", "tools_disclosed": [], "self_declared": True},
        "fund_binding": {"fund_profile_id": fund_profile_id},
        "sources": [],
        "fields": [],
        "chain": {},
        "ecosystem_positions": [],
        "review_records": [],
        "mappings": [],
        "lock": {"locked": False},
    }
    for r in registry():
        if not r.get("required"):
            continue
        rec = {"field_id": r["field_id"], "value": None, "status": "NEEDS_INPUT",
               "provenance": _default_provenance("human")}
        node = r.get("chain_node")
        if node:
            doc["chain"].setdefault(node, []).append(rec)
        else:
            doc["fields"].append(rec)
    return doc


def set_field(doc: dict, field_id: str, value: Any, *, actor: str = "human",
              chain_node: str | None = None, provenance: dict | None = None,
              source_ids: list[str] | None = None, links: dict | None = None,
              tool: str | None = None) -> dict:
    """Write one field record (in place) and return it.

    The resulting status is always DRAFT, or NEEDS_INPUT when the value is
    cleared (None / "NEEDS_INPUT"). A value of "NEEDS_VERIFICATION" is stored
    as null plus that marker. `actor` is "human" or "ai_assisted"; an AI
    draft is recorded with authored_by ai_draft and may never claim the
    provenance class SOURCE (ValueError)."""
    if actor not in ACTORS:
        raise ValueError(f"actor must be one of {ACTORS}")
    if not isinstance(field_id, str) or not field_id:
        raise ValueError("field_id is required")
    reg = registry_by_id().get(field_id)
    node = chain_node if chain_node is not None else (reg or {}).get("chain_node")
    if reg is None and chain_node is None:
        raise ValueError(f"{field_id} is not in registry/fields.jsonl; pass chain_node "
                         "(e.g. PriorKnowledge, Evidence, Claim) for chain content")

    prov = dict(_default_provenance(actor))
    if provenance:
        prov.update(provenance)
    if actor == "ai_assisted":
        if prov.get("provenance_class") == "SOURCE":
            raise ValueError("an AI draft can never be provenance_class SOURCE; "
                             "the researcher's own cited information is the source")
        if prov.get("authored_by") not in AI_AUTHORED:
            prov["authored_by"] = "ai_draft"
    elif prov.get("authored_by") == "ai_draft":
        raise ValueError("authored_by ai_draft requires actor='ai_assisted'")

    markers: list[str] = []
    if value == "NEEDS_VERIFICATION":
        value, markers = None, ["NEEDS_VERIFICATION"]
    if value == "NEEDS_INPUT":
        value = None
    status = "NEEDS_INPUT" if value is None else "DRAFT"

    existing = None
    for rec, _ in iter_records(doc):
        if rec.get("field_id") == field_id:
            existing = rec
            break
    if existing is None:
        existing = {"field_id": field_id}
        if node:
            doc.setdefault("chain", {}).setdefault(node, []).append(existing)
        else:
            doc.setdefault("fields", []).append(existing)
    existing["value"] = value
    existing["status"] = status  # hard ceiling: never above DRAFT from here
    if markers:
        existing["markers"] = sorted(set(list(existing.get("markers") or []) + markers))
    if source_ids is not None:
        existing["source_ids"] = list(source_ids)
    if links is not None:
        existing["links"] = links
    if provenance is not None or actor == "ai_assisted" or "provenance" not in existing:
        existing["provenance"] = prov

    # An edit breaks an object LOCK (status_permissions.yaml regressions).
    lock = doc.get("lock")
    if isinstance(lock, dict) and lock.get("locked"):
        lock["locked"] = False
    if actor == "ai_assisted":
        auth = doc.setdefault("authoring", {"mode": "human", "tools_disclosed": [], "self_declared": True})
        auth["mode"] = "ai_assisted"
        auth.setdefault("self_declared", True)
        if tool:
            tools = list(auth.get("tools_disclosed") or [])
            if tool not in tools:
                tools.append(tool)
            auth["tools_disclosed"] = tools
    return existing
