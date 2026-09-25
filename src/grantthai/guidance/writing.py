"""grantthai.guidance.writing — reference implementation of the writing layer.

    intent(field_id)        -> the writing intent for one field, or None
    explain_field(field_id) -> registry record merged with its intent
    length_findings(doc)    -> REVIEW-level Finding objects (W101 over max,
                               W102 under min); never BLOCK, never a status
    checklist(doc)          -> completeness checklist states
                               (PASS | OPEN | HUMAN_CHECK)

Everything is deterministic and reads only `guidance/writing_intent.yaml`
and the registry. A length target is a target, not a rule of the fund:
the basis string on each target says where it comes from, and a target
whose source could not be read here is NEEDS_VERIFICATION.

Word counting: whitespace-separated tokens over every string leaf of the
value. Thai prose is often written without spaces, so for a value that
contains Thai script the under-minimum finding (W102) is not raised and
the over-maximum finding says the count is a token count.
"""
from __future__ import annotations

import re
from functools import lru_cache
from typing import Any

from grantthai.core import project as P
from grantthai.validators.engine import Finding

WRITING_INTENT_REL = "guidance/writing_intent.yaml"
WRITING_INTENT_SCHEMA_ID = "https://github.com/morrocwi/GrantThai/spec/guidance/writing_intent.schema.json"

FIELD_ID_RE = re.compile(r"^(PROFILE|FUND|CORE|METHOD|WORK|GEO|BUDGET|COMP|READY|RESULTS|DOC|AUDIT|BRIDGE)(\.[A-Z0-9_]+){2,}$")
THAI_RE = re.compile(r"[฀-๿]")

RULE_OVER_MAX = "W101"
RULE_UNDER_MIN = "W102"
DEFAULT_SEVERITY = "REVIEW"

STATE_PASS = "PASS"
STATE_OPEN = "OPEN"
STATE_HUMAN = "HUMAN_CHECK"


# --------------------------------------------------------------------------
# Data
# --------------------------------------------------------------------------

@lru_cache(maxsize=None)
def load() -> dict:
    """The parsed writing-intent file (read once from the data root)."""
    return P._read_yaml(WRITING_INTENT_REL)


def intent(field_id: str) -> dict | None:
    """The intent for `field_id`, or None when the file has no entry."""
    entry = (load().get("fields") or {}).get(field_id)
    return dict(entry) if isinstance(entry, dict) else None


def explain_field(field_id: str) -> dict:
    """The registry record for `field_id` merged with its writing intent.

    Raises KeyError for an id the registry does not know. The result is a
    plain dict of plain values, in a fixed key order, so two calls give
    the same JSON."""
    reg = P.registry_by_id()
    if field_id not in reg:
        raise KeyError(f"unknown field id {field_id!r}")
    rec = reg[field_id]
    out = {
        "field_id": field_id,
        "label_en": rec.get("label_en"),
        "label_th": rec.get("label_th"),
        "type": rec.get("type"),
        "cardinality": rec.get("cardinality"),
        "required": rec.get("required"),
        "input_control": rec.get("input_control"),
        "origin": rec.get("origin"),
        "chain_node": rec.get("chain_node"),
        "section": rec.get("section"),
        "dependencies": list(rec.get("dependencies") or []),
        "guidance": dict(rec.get("guidance") or {}),
        "conflicts": list(rec.get("conflicts") or []),
        "markers": list(rec.get("markers") or []),
        "registry_derived_from": rec.get("derived_from"),
        "writing_intent": intent(field_id),
        "writing_intent_status": None,
    }
    if out["writing_intent"] is not None:
        doc = load()
        out["writing_intent_status"] = {"status": doc.get("status"), "status_marker": doc.get("status_marker")}
    return out


# --------------------------------------------------------------------------
# Measuring a value
# --------------------------------------------------------------------------

def _string_leaves(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        out: list[str] = []
        for k in sorted(value):
            out.extend(_string_leaves(value[k]))
        return out
    if isinstance(value, list):
        out = []
        for v in value:
            out.extend(_string_leaves(v))
        return out
    if value is None or isinstance(value, bool):
        return []
    return [str(value)]


def is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == "" or value in ("NEEDS_INPUT", "NEEDS_VERIFICATION")
    if isinstance(value, (list, dict)):
        return len(value) == 0
    return False


def measure(value: Any, unit: str) -> int | None:
    """Length of `value` in `unit` (words, items, chars); None when empty."""
    if is_empty(value):
        return None
    if unit == "items":
        if isinstance(value, list):
            return len(value)
        return 1
    text = " ".join(_string_leaves(value))
    if unit == "chars":
        return len(text)
    if unit == "words":
        return len(text.split())
    raise ValueError(f"unknown length unit {unit!r}")


def has_thai(value: Any) -> bool:
    return any(THAI_RE.search(s) for s in _string_leaves(value))


# --------------------------------------------------------------------------
# Length findings (REVIEW only)
# --------------------------------------------------------------------------

def _severity(rule_id: str) -> str:
    """REVIEW, or whatever the rule catalog says once the integrator has
    registered W101/W102 there. Never escalates above REVIEW: a length
    target is guidance, not a fund rule."""
    try:
        rules = {r["id"]: r for r in P.rules_catalog().get("rules") or []}
    except Exception:  # pragma: no cover - data root missing is reported elsewhere
        rules = {}
    sev = (rules.get(rule_id) or {}).get("severity", DEFAULT_SEVERITY)
    return "INFO" if sev == "INFO" else DEFAULT_SEVERITY


def length_findings(doc: dict, field_ids: list[str] | None = None) -> list[Finding]:
    """One Finding per field whose non-empty value is outside its length
    target. `field_ids` restricts the check to those fields. Report-only."""
    recs = P.records_by_id(P.normalized(doc))
    targets = load().get("fields") or {}
    out: list[Finding] = []
    for fid in sorted(targets):
        if field_ids is not None and fid not in field_ids:
            continue
        rec = recs.get(fid)
        if rec is None:
            continue
        value = rec.get("value")
        tgt = targets[fid].get("length_target") or {}
        unit = tgt.get("unit")
        if not unit:
            continue        # no target shipped for this field (null length_target)
        n = measure(value, unit)
        if n is None:
            continue
        basis = tgt.get("basis", "")
        thai = unit == "words" and has_thai(value)
        note = " (whitespace-token count; Thai prose without spaces counts low)" if thai else ""
        if n > int(tgt["max"]):
            out.append(Finding(
                RULE_OVER_MAX, _severity(RULE_OVER_MAX),
                f"{fid}: {n} {unit} is above the writing target of {tgt['max']} {unit}{note}. Basis: {basis}.",
                [fid],
                "Shorten, or keep it and note why; a length target is guidance, not a fund rule.",
            ))
        elif n < int(tgt["min"]) and not thai:
            out.append(Finding(
                RULE_UNDER_MIN, _severity(RULE_UNDER_MIN),
                f"{fid}: {n} {unit} is below the writing target of {tgt['min']} {unit}. Basis: {basis}.",
                [fid],
                "Check the micro-template (grantthai explain FIELD_ID) for the parts a reader expects.",
            ))
    return out


# --------------------------------------------------------------------------
# Completeness checklist
# --------------------------------------------------------------------------

def _filled(recs: dict, fid: str) -> bool:
    rec = recs.get(fid)
    return rec is not None and not is_empty(rec.get("value"))


def _items_have_key(recs: dict, fid: str, key: str) -> bool | None:
    rec = recs.get(fid)
    if rec is None or is_empty(rec.get("value")):
        return None
    value = rec.get("value")
    if not isinstance(value, list):
        return False
    return all(isinstance(it, dict) and not is_empty(it.get(key)) for it in value)


def checklist(doc: dict) -> list[dict]:
    """The completeness checklist evaluated on `doc`. Each item:
    {id, state, field_ids, check_en, evaluable, kind}. A human item is
    always HUMAN_CHECK; a deterministic item is PASS or OPEN."""
    recs = P.records_by_id(P.normalized(doc))
    out = []
    for item in load().get("completeness_checklist") or []:
        fids = list(item.get("field_ids") or [])
        entry = {
            "id": item["id"],
            "state": STATE_HUMAN,
            "field_ids": fids,
            "check_en": (item.get("check") or {}).get("en", ""),
            "evaluable": item.get("evaluable"),
            "kind": item.get("kind"),
        }
        if item.get("evaluable") == "deterministic":
            kind = item.get("kind")
            if kind == "fields_filled":
                ok = all(_filled(recs, f) for f in fids)
            elif kind == "items_have_key":
                key = (item.get("params") or {}).get("key", "")
                results = [_items_have_key(recs, f, key) for f in fids]
                ok = all(r is True for r in results)
            elif kind == "length_within":
                ok = not length_findings(doc, fids)
            else:
                raise ValueError(f"{item['id']}: unknown checklist kind {kind!r}")
            entry["state"] = STATE_PASS if ok else STATE_OPEN
        out.append(entry)
    return out
