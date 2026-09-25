"""grantthai.review.records — status transitions and named review records.

Every status change made by this module goes through `transition()`,
which reads the transition table in spec/common/status_permissions.yaml
and refuses anything the table does not list for the acting actor. The
table is data; nothing here hard-codes a transition.

Actors (the same names as the table):
    named_human             - a person acting through a named review record
    deterministic_validator - the local validator run (`link_statuses`)
    core                    - automatic regressions

Neither MCP nor REST can reach this module: grantthai.api_py does not
import it, and the hard-ceiling tests assert that.
"""
from __future__ import annotations

import re
from functools import lru_cache
from typing import Any

from grantthai.core import project as P
from grantthai.core.object_hash import content_sha256

GATES = ("RG0", "RG1", "RG2", "RG3", "RG4")
INDEPENDENCE = ("self", "independent")
OUTCOMES = ("HUMAN_REVIEWED", "VERIFIED")
REVIEW_SCHEMA_ID = "https://github.com/morrocwi/GrantThai/spec/common/review.schema.json"
NAMED_HUMAN = "named_human"
DETERMINISTIC_VALIDATOR = "deterministic_validator"
DATE_RX = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Rule families that keep a record from LOGIC_LINKED
# (spec/common/status.yaml, logic_linked_criterion).
LOGIC_FAMILIES = ("R", "W", "B", "T", "CH")
STRUCTURE_STATUSES = ("STRUCTURE_CHECKED", "LOGIC_LINKED")
REVIEWED_STATUSES = ("HUMAN_REVIEWED", "VERIFIED", "LOCKED", "SUBMITTED")


@lru_cache(maxsize=None)
def _sequence() -> tuple[str, ...]:
    return tuple(P._read_yaml("spec/common/status.yaml").get("field_status_sequence") or [])


def _rank(status: str) -> int:
    seq = _sequence()
    return seq.index(status) if status in seq else -1


class TransitionRefused(ValueError):
    """The requested status change is not in the transition table."""


class CeilingViolation(PermissionError):
    """An actor other than a named human tried to act through a review."""


# --------------------------------------------------------------------------
# Transition table (data, read once)
# --------------------------------------------------------------------------

def _as_list(x: Any) -> list[str]:
    if x is None:
        return []
    return [str(v) for v in (x if isinstance(x, list) else [x])]


@lru_cache(maxsize=None)
def transition_table() -> tuple[dict, ...]:
    doc = P._read_yaml("spec/common/status_permissions.yaml") or {}
    out = []
    for t in doc.get("transitions") or []:
        out.append({
            "from": tuple(_as_list(t.get("from"))),
            "to": tuple(_as_list(t.get("to"))),
            "actors": tuple(_as_list(t.get("allowed_actors"))),
            "requires": t.get("requires"),
        })
    return tuple(out)


@lru_cache(maxsize=None)
def regression_table() -> tuple[dict, ...]:
    doc = P._read_yaml("spec/common/status_permissions.yaml") or {}
    out = []
    for r in doc.get("regressions") or []:
        if r.get("from") is None or r.get("to") is None:
            continue
        out.append({"from": tuple(_as_list(r.get("from"))), "to": tuple(_as_list(r.get("to"))),
                    "actors": (str(r.get("actor")),), "trigger": r.get("trigger")})
    return tuple(out)


def allowed(from_status: str, to_status: str, actor: str) -> bool:
    return any(from_status in t["from"] and to_status in t["to"] and actor in t["actors"]
               for t in transition_table())


def regression_allowed(from_status: str, to_status: str, actor: str) -> bool:
    return any(from_status in t["from"] and to_status in t["to"] and actor in t["actors"]
               for t in regression_table())


def regress(rec: dict, to_status: str, actor: str) -> dict:
    """Apply a regression listed under `regressions` in the table."""
    frm = rec.get("status") or "EMPTY"
    if not regression_allowed(frm, to_status, actor):
        raise TransitionRefused(
            f"{rec.get('field_id')}: regression {frm} -> {to_status} by {actor} is not in "
            "spec/common/status_permissions.yaml")
    rec["status"] = to_status
    return rec


def transition(rec: dict, to_status: str, actor: str) -> dict:
    """Move one field record to `to_status` as `actor`, in place. Refuses
    (TransitionRefused) any pair the table does not list for that actor."""
    frm = rec.get("status") or "EMPTY"
    if not allowed(frm, to_status, actor):
        raise TransitionRefused(
            f"{rec.get('field_id')}: {frm} -> {to_status} by {actor} is not in "
            "spec/common/status_permissions.yaml")
    rec["status"] = to_status
    return rec


# --------------------------------------------------------------------------
# Scope
# --------------------------------------------------------------------------

def resolve_scope(doc: dict, scope: str | list[str]) -> tuple[str, list[str]]:
    """Return (scope_text, field_ids). `scope` is a list of field ids, a
    comma-separated string of field ids, or "@chain:<Node>" meaning every
    record under chain.<Node>. Every id must exist in the project."""
    if isinstance(scope, list):
        text = ",".join(str(s) for s in scope)
        ids = [str(s) for s in scope]
    elif isinstance(scope, str) and scope.startswith("@chain:"):
        node = scope[len("@chain:"):]
        recs = (doc.get("chain") or {}).get(node)
        if not recs:
            raise ValueError(f"scope {scope}: chain node {node!r} has no records in this project")
        text = scope
        ids = [r.get("field_id") for r in recs if isinstance(r, dict) and r.get("field_id")]
    elif isinstance(scope, str) and scope.strip():
        text = scope
        ids = [s.strip() for s in scope.split(",") if s.strip()]
    else:
        raise ValueError("scope is required (field ids, or @chain:<Node>)")
    known = P.records_by_id(doc)
    missing = [i for i in ids if i not in known]
    if missing:
        raise ValueError(f"scope names fields that are not in this project: {', '.join(missing)}")
    return text, ids


# --------------------------------------------------------------------------
# Named review records
# --------------------------------------------------------------------------

def _check_actor(actor: str) -> None:
    if actor != NAMED_HUMAN:
        raise CeilingViolation(
            f"only a named human may write a review record (actor {actor!r}); MCP, REST and "
            "AI-assisted callers are capped at DRAFT (spec/common/status_permissions.yaml hard_ceiling)")


def _check_date(date: str) -> None:
    if not isinstance(date, str) or not DATE_RX.match(date):
        raise ValueError("date must be a YYYY-MM-DD string")


def add_review(doc: dict, *, gate_id: str, reviewer_name: str, reviewer_role: str,
               scope: str | list[str], independence: str, outcome: str | None = None,
               basis: str | None = None, date: str, actor: str = NAMED_HUMAN) -> dict:
    """Write one named review record for one gate (in place) and promote the
    fields in `scope` through the transition table.

    - `content_sha256` is the project content hash at the time of review.
    - Every field in scope must be LOGIC_LINKED (a first review), or
      HUMAN_REVIEWED when `outcome` is VERIFIED (a further review); the call
      is all-or-nothing and refuses otherwise.
    - `outcome` defaults to HUMAN_REVIEWED. A self review with outcome
      VERIFIED is stored as VERIFIED and rendered as AUTHOR_CHECKED
      (spec/common/status.yaml rendering_rules).
    - Refuses (CeilingViolation) unless `actor` is "named_human".
    """
    _check_actor(actor)
    if gate_id not in GATES:
        raise ValueError(f"gate_id must be one of {GATES}")
    if independence not in INDEPENDENCE:
        raise ValueError(f"independence must be one of {INDEPENDENCE}")
    outcome = outcome or "HUMAN_REVIEWED"
    if outcome not in OUTCOMES:
        raise ValueError(f"outcome must be one of {OUTCOMES}")
    if not isinstance(reviewer_name, str) or not reviewer_name.strip():
        raise ValueError("reviewer_name is required: a review record is a named human act")
    if not isinstance(reviewer_role, str) or not reviewer_role.strip():
        raise ValueError("reviewer_role is required")
    _check_date(date)

    scope_text, ids = resolve_scope(doc, scope)
    recs = P.records_by_id(doc)
    # Check every transition before applying any (all-or-nothing). A field
    # already at the outcome, or above it (a second gate covering the same
    # field), is left as it is: a review never lowers a status.
    to_move: list[str] = []
    for fid in ids:
        frm = recs[fid].get("status") or "EMPTY"
        if _rank(frm) >= _rank(outcome) and frm in REVIEWED_STATUSES:
            continue
        if not allowed(frm, outcome, actor):
            raise TransitionRefused(
                f"{fid}: {frm} -> {outcome} by {actor} is not in spec/common/status_permissions.yaml "
                "(a review promotes a LOGIC_LINKED field; run the local validator first)")
        to_move.append(fid)

    record = {
        "gate_id": gate_id,
        "reviewer_name": reviewer_name.strip(),
        "reviewer_role": reviewer_role.strip(),
        "scope": scope_text,
        "independence": independence,
        "outcome": outcome,
        "date": date,
        "content_sha256": content_sha256(doc),
    }
    if basis:
        record["basis"] = str(basis)
    errs = P.schema_errors(record, REVIEW_SCHEMA_ID)
    if errs:
        raise ValueError("review record does not validate: " + "; ".join(errs))

    for fid in to_move:
        transition(recs[fid], outcome, actor)
    doc.setdefault("review_records", []).append(record)
    return record


def records_for(doc: dict, gate_id: str) -> list[dict]:
    return [r for r in doc.get("review_records") or []
            if isinstance(r, dict) and r.get("gate_id") == gate_id]


def latest(doc: dict, gate_id: str) -> dict | None:
    rs = records_for(doc, gate_id)
    return rs[-1] if rs else None


def is_current(doc: dict, record: dict, csha: str | None = None) -> bool:
    return record.get("content_sha256") == (csha or content_sha256(doc))


def stale(doc: dict) -> list[str]:
    """Gate ids whose latest review record no longer matches the project's
    content_sha256 (an authored change happened after the review)."""
    csha = content_sha256(doc)
    return [g for g in GATES if latest(doc, g) is not None and not is_current(doc, latest(doc, g), csha)]


def gate_states(doc: dict) -> dict:
    """{gate_id: {"state": not_reviewed|current|stale, "record": dict|None}}."""
    csha = content_sha256(doc)
    out = {}
    for g in GATES:
        r = latest(doc, g)
        if r is None:
            out[g] = {"state": "not_reviewed", "record": None}
        else:
            out[g] = {"state": "current" if is_current(doc, r, csha) else "stale", "record": r}
    return out


def gate_hold_reasons(doc: dict) -> list[str]:
    """One hold reason per gate that is missing or stale. A missing gate
    never blocks `build` (spec/common/review_gates.yaml missing_gate_policy):
    these lines are meant for the rendered readiness summary."""
    out = []
    for g, st in gate_states(doc).items():
        if st["state"] == "not_reviewed":
            out.append(f"{g}: no review record (claim strength downgraded; build is not blocked)")
        elif st["state"] == "stale":
            out.append(f"{g}: review stale (content changed after the {st['record'].get('date')} review)")
    return out


# --------------------------------------------------------------------------
# Deterministic-validator promotion (local CLI only)
# --------------------------------------------------------------------------

def _family(rule_id: str) -> str:
    return re.match(r"^[A-Z]+", rule_id or "").group(0) if re.match(r"^[A-Z]+", rule_id or "") else ""


def link_statuses(doc: dict, findings: list, *, actor: str = DETERMINISTIC_VALIDATOR) -> dict:
    """Apply a local validator run to the field statuses, in place, per
    spec/common/status.yaml (structure_checked_criterion,
    logic_linked_criterion) and the regressions in status_permissions.yaml.

    `findings` is `grantthai.validators.engine.run(...).findings` (or the
    report's `findings` dicts). Returns {field_id: new_status} for every
    record whose status changed. Only the local CLI may call this: it is
    the one place a status rises above DRAFT without a named human.
    """
    if actor != DETERMINISTIC_VALIDATOR:
        raise CeilingViolation(f"only the deterministic validator may link statuses (actor {actor!r})")
    structure_block: set[str] = set()
    logic_block: set[str] = set()
    for f in findings:
        d = f if isinstance(f, dict) else f.as_dict()
        if d.get("severity") != "BLOCK":
            continue
        fam = _family(d.get("rule_id", ""))
        ids = d.get("field_ids") or []
        if fam in ("S", "SCHEMA", "X"):
            structure_block.update(ids)
        elif fam in LOGIC_FAMILIES:
            logic_block.update(ids)
    changed: dict[str, str] = {}
    for rec, _ in P.iter_records(doc):
        fid = rec.get("field_id")
        status = rec.get("status") or "EMPTY"
        if rec.get("value") is None:
            continue
        if status == "DRAFT":
            if fid in structure_block:
                continue
            transition(rec, "STRUCTURE_CHECKED", actor)
            if fid not in logic_block:
                transition(rec, "LOGIC_LINKED", actor)
            changed[fid] = rec["status"]
        elif status == "STRUCTURE_CHECKED":
            if fid in structure_block or fid in logic_block:
                regress(rec, "DRAFT", actor)
                changed[fid] = "DRAFT"
            else:
                transition(rec, "LOGIC_LINKED", actor)
                changed[fid] = "LOGIC_LINKED"
        elif status == "LOGIC_LINKED":
            if fid in structure_block or fid in logic_block:
                regress(rec, "DRAFT", actor)
                changed[fid] = "DRAFT"
    return changed
