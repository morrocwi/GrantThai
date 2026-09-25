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
# this module lives in (src/grantthai/core/project.py -> repo root). This
# guess only holds for an editable install or a run from inside the repo
# checkout: `pip install .` (non-editable) copies src/grantthai/ into
# site-packages without its sibling data directories, so the guess is wrong
# there and GRANTTHAI_HOME must be set. `_require_data_root()` turns that
# into one clear message instead of a bare FileNotFoundError.
DATA_ROOT = Path(os.environ.get("GRANTTHAI_HOME") or Path(__file__).resolve().parents[3])


def _require_data_root() -> None:
    if (DATA_ROOT / "registry").is_dir() and (DATA_ROOT / "spec").is_dir():
        return
    raise RuntimeError(
        f"GrantThai cannot find its data directories (registry/, spec/, validators/, templates/, "
        f"funds/, mappings/) under {DATA_ROOT}. This usually means GrantThai was installed with "
        f"`pip install .` (a non-editable install), which does not carry those directories with "
        f"it. Set GRANTTHAI_HOME to your GrantThai repository checkout, e.g.:\n"
        f"    export GRANTTHAI_HOME=/path/to/GrantThai\n"
        f"or install editable from the checkout instead: `pip install -e .`."
    )


PROJECT_SCHEMA_ID = "https://github.com/morrocwi/GrantThai/spec/project/project.schema.json"
FUND_SCHEMA_ID = "https://github.com/morrocwi/GrantThai/spec/fund/fund-profile.schema.json"
STRUCTURED_SCHEMA_ID = "https://github.com/morrocwi/GrantThai/spec/registry/structured_fields.schema.json"
REPORT_SCHEMA_ID = "https://github.com/morrocwi/GrantThai/spec/common/validation_report.schema.json"

WORK_SCHEMA_ID = "https://github.com/morrocwi/GrantThai/spec/work/work.schema.json"

SCHEMA_VERSION = "0.2.0-draft"          # a legacy project.yaml (read unchanged, never rewritten)
WORK_SCHEMA_VERSION = "0.3.0-draft"     # work.yaml, a superset of project.yaml 0.2
WORK_FILE = "work.yaml"
PROJECT_FILE = "project.yaml"
LEGACY_ROUTE = "nriis-proposal"         # what a 0.2 project.yaml is read as
LEGACY_WORK_TYPE = "research_proposal"
DEFAULT_FUND_PROFILE = "example/FICTIONAL_CALL@0.1"

ACTORS = ("human", "ai_assisted")
AI_AUTHORED = ("ai_draft", "human_ai_assisted")
# Research stages of authoring.ai_use_declaration.tools[].stages
# (spec/project/project.schema.json#/$defs/ai_use_stage).
AI_USE_STAGES = ("idea", "proposal_writing", "literature", "data", "analysis", "writing",
                 "language_editing", "review", "publication")
DEFAULT_AI_STAGE = "proposal_writing"   # what an AI does through GrantThai's surfaces


# --------------------------------------------------------------------------
# Shipped data (read once, from DATA_ROOT only)
# --------------------------------------------------------------------------

def _read_yaml(rel: str) -> Any:
    _require_data_root()
    return yaml.safe_load((DATA_ROOT / rel).read_text(encoding="utf-8"))


def _read_jsonl(rel: str) -> list[dict]:
    _require_data_root()
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
def candidate_labels() -> dict:
    """mappings/nriis/labels@<edition>.yaml: CANDIDATE Thai labels and code
    lists from public documents, every one NEEDS_VERIFICATION (K14). With
    several editions the files are merged in sorted file-name order."""
    _require_data_root()
    out: dict = {}
    for path in sorted((DATA_ROOT / "mappings" / "nriis").glob("labels@*.yaml")):
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for k, v in doc.items():
            if isinstance(v, dict) and isinstance(out.get(k), dict):
                out[k] = {**out[k], **v}
            else:
                out[k] = v
    return out


def candidate_values(reg: dict) -> tuple[str, list[str]] | None:
    """A registry record's candidate option list (NEEDS_VERIFICATION):
    ("values", [...]) for literal values, ("codes", [...]) for a code list
    in a candidate labels file, or None."""
    cv = reg.get("candidate_values") if isinstance(reg, dict) else None
    if not isinstance(cv, dict):
        return None
    if isinstance(cv.get("values"), list):
        return "values", [str(v) for v in cv["values"]]
    ref = cv.get("ref") or ""
    if "#" in ref:
        key = ref.split("#", 1)[1]
        block = candidate_labels().get(key) or {}
        return "codes", [str(v.get("code")) for v in block.get("values") or [] if v.get("code") is not None]
    return None


def candidate_label_text(entry: dict | None) -> str:
    """'"<label>" (SD-1 p15, item 1.1)' for a field_labels/tab_labels entry."""
    if not isinstance(entry, dict) or not entry.get("label_th"):
        return ""
    src = entry.get("source") or {}
    where = f"{src.get('doc')} p{src.get('pages')}" + (f", item {src['item']}" if src.get("item") else "")
    return f'"{entry["label_th"]}" ({where})'


@lru_cache(maxsize=None)
def contradictions() -> tuple[dict, ...]:
    """registry/contradictions.yaml: package-level contradictions, all kept OPEN."""
    return tuple((_read_yaml("registry/contradictions.yaml") or {}).get("contradictions") or [])


@lru_cache(maxsize=None)
def notice_constant() -> str:
    _require_data_root()
    raw = (DATA_ROOT / "spec/output/notice_constant.txt").read_text(encoding="utf-8")
    return raw.rstrip("\n")


@lru_cache(maxsize=None)
def _schemas() -> dict:
    _require_data_root()
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
    _require_data_root()
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
              tool: str | None = None, tool_version: str | None = None,
              stage: str | None = None) -> dict:
    """Write one field record (in place) and return it.

    The resulting status is always DRAFT, or NEEDS_INPUT when the value is
    cleared (None / "NEEDS_INPUT"). A value of "NEEDS_VERIFICATION" is stored
    as null plus that marker. `actor` is "human" or "ai_assisted"; an AI
    draft is recorded with authored_by ai_draft and may never claim the
    provenance class SOURCE (ValueError). An AI-assisted write that names
    its `tool` also records it in authoring.ai_use_declaration.tools
    (record_ai_tool), with `tool_version` and `stage` when given."""
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
            record_ai_tool(doc, tool, version=tool_version, stage=stage or DEFAULT_AI_STAGE)
    return existing


def record_ai_tool(doc: dict, name: str, *, version: str | None = None,
                   stage: str | None = None) -> bool:
    """Record an AI tool the way an AI surface may: add its name to
    authoring.tools_disclosed and an entry to authoring.ai_use_declaration
    .tools (docs/policy/ai-use-ceiling.md). An existing entry of the same
    name gains the stage, and a version when it had none. purpose stays
    NEEDS_INPUT for the researcher. Returns True when tools[] changed; the
    researcher's confirmation (declaration_confirmed_by_human) is then reset
    to false, because the declaration no longer covers every use. Nothing
    else in the declaration is touched."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("tool name must be a non-empty string")
    if stage is not None and stage not in AI_USE_STAGES:
        raise ValueError(f"stage must be one of {AI_USE_STAGES}")
    auth = doc.setdefault("authoring", {"mode": "human", "tools_disclosed": [], "self_declared": True})
    auth["mode"] = "ai_assisted"
    auth.setdefault("self_declared", True)
    disclosed = list(auth.get("tools_disclosed") or [])
    if name not in disclosed:
        disclosed.append(name)
    auth["tools_disclosed"] = disclosed
    decl = auth.setdefault("ai_use_declaration", {})
    tools = decl.setdefault("tools", [])
    entry = next((t for t in tools if isinstance(t, dict) and t.get("name") == name), None)
    changed = False
    if entry is None:
        entry = {"name": name, "version": version or "NEEDS_INPUT", "stages": [], "purpose": "NEEDS_INPUT"}
        tools.append(entry)
        changed = True
    elif version and entry.get("version") in (None, "", "NEEDS_INPUT"):
        entry["version"] = version
        changed = True
    if stage and stage not in (entry.get("stages") or []):
        entry["stages"] = list(entry.get("stages") or []) + [stage]
        changed = True
    if changed or "declaration_confirmed_by_human" not in decl:
        decl["declaration_confirmed_by_human"] = False
    return changed


# --------------------------------------------------------------------------
# work.yaml 0.3: discovery, the legacy view, and the explicit migration
# --------------------------------------------------------------------------

class TwoCanonicalInputs(ValueError):
    """work.yaml and project.yaml sit in the same directory. The one-input
    rule is enforced, not assumed: the command stops (CLI exit 2)."""


def is_work(doc: dict) -> bool:
    """True for a work.yaml 0.3 object; False for a legacy 0.2 project.yaml
    (or anything else, which the 0.2 schema then reports)."""
    return isinstance(doc, dict) and doc.get("schema_version") == WORK_SCHEMA_VERSION


def object_schema_id(doc: dict) -> str:
    """The schema a loaded object validates against: work.schema.json for
    0.3, the frozen project.schema.json for everything else."""
    return WORK_SCHEMA_ID if is_work(doc) else PROJECT_SCHEMA_ID


def work_id(doc: dict) -> str:
    """The object's identifier: `project_id` when present (legacy files and
    0.3 files that keep it), else `work_id`. Printed exactly as written."""
    v = doc.get("project_id") if isinstance(doc, dict) else None
    if v is None and isinstance(doc, dict):
        v = doc.get("work_id")
    return str(v)


def work_view(doc: dict) -> dict:
    """The in-memory reading of the object for the router, never written
    back. A legacy 0.2 file reads as work_type research_proposal,
    default_route nriis-proposal and sub_profiles.nriis-proposal =
    form_profile; its bytes and content_sha256 do not change. For a 0.3
    file the legacy top-level form_profile is still read when routing does
    not name an nriis-proposal sub-profile."""
    legacy = not is_work(doc)
    routing = doc.get("routing") if isinstance(doc.get("routing"), dict) else {}
    subs = dict(routing.get("sub_profiles") or {}) if isinstance(routing.get("sub_profiles"), dict) else {}
    fp = doc.get("form_profile")
    if LEGACY_ROUTE not in subs and fp is not None:
        subs[LEGACY_ROUTE] = fp
    if legacy:
        return {"legacy": True, "work_id": work_id(doc), "work_type": LEGACY_WORK_TYPE,
                "declared_routes": [LEGACY_ROUTE], "default_route": LEGACY_ROUTE, "sub_profiles": subs}
    return {"legacy": False, "work_id": work_id(doc),
            "work_type": doc.get("work_type") or LEGACY_WORK_TYPE,
            "declared_routes": list(routing.get("declared_routes") or []),
            "default_route": routing.get("default_route"), "sub_profiles": subs}


def discover(path: str | Path | None = None) -> Path:
    """The one canonical input. `path` may be a file, a directory, or None
    (the current directory). In a directory, work.yaml is preferred, then
    project.yaml. If both exist in the input's directory the call raises
    TwoCanonicalInputs, whichever file was named."""
    p = Path(path) if path is not None else Path.cwd()
    folder = p if p.is_dir() else p.parent
    work, proj = folder / WORK_FILE, folder / PROJECT_FILE
    if work.is_file() and proj.is_file():
        raise TwoCanonicalInputs(f"two canonical inputs in {folder}: {WORK_FILE} and {PROJECT_FILE}; keep one "
                                 f"(`grantthai migrate --rename` turns a project.yaml into a work.yaml)")
    if p.is_dir():
        for cand in (work, proj):
            if cand.is_file():
                return cand
        raise FileNotFoundError(f"no {WORK_FILE} or {PROJECT_FILE} in {folder}")
    if not p.is_file():
        raise FileNotFoundError(f"{p} does not exist")
    return p


def new_work(work_id_: str = "NEEDS_INPUT", work_type: str = LEGACY_WORK_TYPE,
             fund_profile_id: str | None = None, mode: str = "expert",
             required_fields: list[str] | None = None) -> dict:
    """A blank work.yaml 0.3 object. `routing` is left out: the route is the
    researcher's declaration, never a default GrantThai writes. The fields
    in `required_fields` (default: the registry's required flags) are
    present as NEEDS_INPUT so the file doubles as a form."""
    doc: dict = {
        "schema_version": WORK_SCHEMA_VERSION,
        "work_id": work_id_,
        "work_type": work_type,
        "mode": mode,
        "authoring": {"mode": "human", "tools_disclosed": [], "self_declared": True},
    }
    if fund_profile_id:
        doc["fund_binding"] = {"fund_profile_id": fund_profile_id}
    doc.update({"sources": [], "fields": [], "chain": {}, "ecosystem_positions": [], "review_records": [],
                "mappings": [], "lock": {"locked": False}})
    reg = registry_by_id()
    wanted = ([r["field_id"] for r in registry() if r.get("required")] if required_fields is None
              else list(required_fields))
    for fid in wanted:
        rec = {"field_id": fid, "value": None, "status": "NEEDS_INPUT", "provenance": _default_provenance("human")}
        node = (reg.get(fid) or {}).get("chain_node")
        if node:
            doc["chain"].setdefault(node, []).append(rec)
        else:
            doc["fields"].append(rec)
    return doc


def migrated(doc: dict) -> dict:
    """The 0.3 form of a legacy 0.2 object (a new dict; `doc` is untouched):
    schema_version 0.3.0-draft, work_id (from project_id), work_type
    research_proposal, routing {declared_routes, default_route,
    sub_profiles} with form_profile moved under sub_profiles.nriis-proposal.
    Every other key keeps its value and order."""
    if is_work(doc):
        return copy.deepcopy(doc)
    view = work_view(doc)
    routing: dict = {"declared_routes": [LEGACY_ROUTE], "default_route": LEGACY_ROUTE}
    if view["sub_profiles"].get(LEGACY_ROUTE) is not None:
        routing["sub_profiles"] = {LEGACY_ROUTE: view["sub_profiles"][LEGACY_ROUTE]}
    head = {"schema_version": WORK_SCHEMA_VERSION,
            "work_id": copy.deepcopy(doc.get("project_id", "NEEDS_INPUT")),
            "work_type": LEGACY_WORK_TYPE}
    for k in ("mode", "authoring"):
        if k in doc:
            head[k] = copy.deepcopy(doc[k])
    head["routing"] = routing
    rest = {k: copy.deepcopy(v) for k, v in doc.items()
            if k not in head and k not in ("project_id", "form_profile")}
    out = {**head, **rest}
    return out


def migrate(path: str | Path, *, rename: bool = False, dry_run: bool = False) -> dict:
    """grantthai migrate: rewrite a legacy project.yaml as work.yaml 0.3.

    Reports which review gates go stale BEFORE anything is written:
    `work_type` and `work_id` are hashed content, `routing` is not
    (spec/common/object-hash.md), so a migration changes content_sha256 and
    every review gate that was current becomes stale. With dry_run nothing
    is written. With rename the file is written as work.yaml next to it and
    project.yaml is removed (refused if work.yaml already exists)."""
    from grantthai.core.object_hash import content_sha256
    from grantthai.review import records as RR

    src = Path(path)
    doc = load(src)
    if is_work(doc):
        return {"path": str(src), "changed": False, "written": None, "schema_version": WORK_SCHEMA_VERSION,
                "content_sha256_before": content_sha256(doc), "content_sha256_after": content_sha256(doc),
                "stale_gates": [], "note": "already work.yaml 0.3; nothing to do"}
    new = migrated(doc)
    before, after = content_sha256(doc), content_sha256(new)
    cur = [g for g, st in RR.gate_states(doc).items() if st["state"] == "current"]
    stale = [g for g in cur if RR.gate_states(new)[g]["state"] != "current"]
    target = src.with_name(WORK_FILE) if rename else src
    if rename and target.exists() and target.resolve() != src.resolve():
        raise FileExistsError(f"{target} already exists; refusing to overwrite")
    out = {"path": str(src), "changed": True, "written": None if dry_run else str(target),
           "schema_version_from": str(doc.get("schema_version")), "schema_version": WORK_SCHEMA_VERSION,
           "content_sha256_before": before, "content_sha256_after": after, "stale_gates": stale,
           "note": ("work_type and work_id are hashed content, routing is not; review gates current before the "
                    "migration become stale" if stale else "no review gate was current, so none goes stale")}
    if dry_run:
        return out
    save(new, target)
    if rename and target.resolve() != src.resolve():
        src.unlink()
    return out
