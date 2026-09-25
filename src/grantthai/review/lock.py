"""grantthai.review.lock — the object LOCK (spec/common/status.yaml
lock_vs_field_locked; spec/common/object-hash.md "Staleness and the LOCK").

`lock()` refuses unless every gate RG0..RG4 has a current review record
whose outcome is HUMAN_REVIEWED or VERIFIED, every required field that
carries a value is at HUMAN_REVIEWED or better, the validation report (when
given) has BLOCK == 0, and, when the bound fund profile sets
`independent_review_required: true`, every gate's latest record is an
independent review (spec/common/review_gates.yaml self_review). It then
writes `lock.locked_content_sha256`. Applying the lock changes no field
status and, because `lock` is excluded from content_sha256, makes no
review record stale.

A lock is broken when the project was locked at some point
(`locked_content_sha256` present) and either an edit cleared `locked`
(grantthai.core.project.set_field does this) or the current content hash
no longer equals the locked one (a hand edit to project.yaml).
"""
from __future__ import annotations

from grantthai.core import project as P
from grantthai.core.object_hash import content_sha256
from grantthai.review import records as R

REVIEWED_OR_BETTER = ("HUMAN_REVIEWED", "VERIFIED", "LOCKED")


class LockRefused(ValueError):
    """The LOCK gate is not met; the message lists every unmet condition."""


def unmet(doc: dict, *, validation: dict | None = None, fund_profile: dict | None = None) -> list[str]:
    """Every reason the object LOCK cannot be applied right now (empty when
    it can). `validation` is a validation report; `fund_profile` overrides
    the bound profile lookup (tests)."""
    reasons: list[str] = []
    states = R.gate_states(doc)
    for g, st in states.items():
        if st["state"] == "not_reviewed":
            reasons.append(f"{g}: no review record")
        elif st["state"] == "stale":
            reasons.append(f"{g}: review record is stale (content changed after review)")
        elif (st["record"].get("outcome") or "") not in ("HUMAN_REVIEWED", "VERIFIED"):
            reasons.append(f"{g}: latest review record has no outcome of HUMAN_REVIEWED or VERIFIED")

    if fund_profile is None:
        fund_profile, _, _ = P.load_fund_profile(doc)
    if isinstance(fund_profile, dict) and fund_profile.get("independent_review_required"):
        for g, st in states.items():
            rec = st["record"]
            if rec is not None and rec.get("independence") != "independent":
                reasons.append(f"{g}: the fund profile requires an independent review; "
                               f"the latest record is a self review")

    reg = P.registry_by_id()
    for rec, _ in P.iter_records(doc):
        fid = rec.get("field_id")
        if rec.get("value") is None or not (reg.get(fid) or {}).get("required"):
            continue
        if (rec.get("status") or "") not in REVIEWED_OR_BETTER:
            reasons.append(f"{fid}: required field is {rec.get('status') or 'EMPTY'}, "
                           "not HUMAN_REVIEWED or better")

    if validation is not None:
        block = int(((validation.get("summary") or {}).get("block")) or 0)
        if block:
            reasons.append(f"validation report has BLOCK {block} (needs 0)")
    return reasons


def lock(doc: dict, *, locked_by: str, date: str, actor: str = R.NAMED_HUMAN,
         validation: dict | None = None, fund_profile: dict | None = None) -> dict:
    """Apply the object LOCK, in place, as a named human. Returns doc["lock"]."""
    R._check_actor(actor)
    R._check_date(date)
    if not isinstance(locked_by, str) or not locked_by.strip():
        raise ValueError("locked_by is required: the LOCK is a named human act")
    reasons = unmet(doc, validation=validation, fund_profile=fund_profile)
    if reasons:
        raise LockRefused("LOCK refused:\n  - " + "\n  - ".join(reasons))
    doc["lock"] = {
        "locked": True,
        "locked_at": date,
        "locked_by": locked_by.strip(),
        "locked_content_sha256": content_sha256(doc),
    }
    return doc["lock"]


def status(doc: dict) -> str:
    """"unlocked" (never locked), "locked" (current), or "broken"."""
    lk = doc.get("lock") or {}
    if not isinstance(lk, dict) or not lk.get("locked_content_sha256"):
        return "unlocked"
    if lk.get("locked") and lk["locked_content_sha256"] == content_sha256(doc):
        return "locked"
    return "broken"


def is_locked(doc: dict) -> bool:
    return status(doc) == "locked"


def is_broken(doc: dict) -> bool:
    return status(doc) == "broken"
