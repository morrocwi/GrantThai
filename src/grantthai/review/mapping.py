"""grantthai.review.mapping — accept or reject a LocalTerm -> AcademicConcept
mapping proposal (spec/common/mapping_proposal.schema.json).

Accepting or rejecting is a review act: it touches only the mapping's
`acceptance_state` and `review` keys, both of which content_sha256
excludes (spec/common/object-hash.md), so the project's content hash is
unchanged and no review record goes stale.

Resulting states (all decided by the schema's allowed sets):
    proposed by a human, accepted by that same person   -> ACCEPTED_SELF
    proposed by a human, accepted by someone else       -> ACCEPTED_REVIEWED
    proposed by an AI, accepted by its requester        -> ACCEPTED_BY_REQUESTER
    proposed by an AI, accepted by someone else         -> ACCEPTED_REVIEWED
    rejected (either kind)                              -> PROPOSED
"""
from __future__ import annotations

from grantthai.core import project as P
from grantthai.core.object_hash import content_sha256
from grantthai.review import records as R

MAPPING_SCHEMA_ID = "https://github.com/morrocwi/GrantThai/spec/common/mapping_proposal.schema.json"
MAPPING_GATE = "RG1"   # concept gate (spec/common/review_gates.yaml)


def find(doc: dict, mapping_id: str) -> dict:
    for m in doc.get("mappings") or []:
        if isinstance(m, dict) and m.get("id") == mapping_id:
            return m
    raise ValueError(f"no mapping {mapping_id!r} in this project")


def _review_record(doc: dict, mapping_id: str, *, reviewer_name: str, reviewer_role: str,
                   independence: str, date: str, basis: str | None, outcome: str | None) -> dict:
    rec = {
        "gate_id": MAPPING_GATE,
        "reviewer_name": reviewer_name.strip(),
        "reviewer_role": reviewer_role.strip(),
        "scope": mapping_id,
        "independence": independence,
        "date": date,
        "content_sha256": content_sha256(doc),
    }
    if outcome:
        rec["outcome"] = outcome
    if basis:
        rec["basis"] = str(basis)
    errs = P.schema_errors(rec, R.REVIEW_SCHEMA_ID)
    if errs:
        raise ValueError("mapping review record does not validate: " + "; ".join(errs))
    return rec


def _check(doc: dict, m: dict) -> None:
    errs = P.schema_errors(m, MAPPING_SCHEMA_ID)
    if errs:
        raise ValueError(f"mapping {m.get('id')} would not validate: " + "; ".join(errs))


def accept(doc: dict, mapping_id: str, *, reviewer_name: str, date: str,
           reviewer_role: str = "reviewer", basis: str | None = None,
           actor: str = R.NAMED_HUMAN) -> dict:
    """Accept one mapping as a named human. Returns the mapping (in place)."""
    R._check_actor(actor)
    R._check_date(date)
    if not isinstance(reviewer_name, str) or not reviewer_name.strip():
        raise ValueError("reviewer_name is required")
    m = find(doc, mapping_id)
    kind = (m.get("proposed_by") or {}).get("kind")
    proposer = (m.get("proposed_by") or {}).get("name")
    name = reviewer_name.strip()
    if kind == "human":
        if proposer == name:
            state, independence = "ACCEPTED_SELF", "self"
        else:
            state, independence = "ACCEPTED_REVIEWED", "independent"
    elif kind == "ai":
        if m.get("requested_by") == name:
            state, independence = "ACCEPTED_BY_REQUESTER", "self"
        else:
            state, independence = "ACCEPTED_REVIEWED", "independent"
    else:
        raise ValueError(f"mapping {mapping_id}: proposed_by.kind must be human or ai")
    before = content_sha256(doc)
    m["acceptance_state"] = state
    m["review"] = _review_record(doc, mapping_id, reviewer_name=name, reviewer_role=reviewer_role,
                                 independence=independence, date=date, basis=basis,
                                 outcome="HUMAN_REVIEWED")
    _check(doc, m)
    assert content_sha256(doc) == before  # acceptance is state, never content
    return m


def reject(doc: dict, mapping_id: str, *, reviewer_name: str, date: str,
           reviewer_role: str = "reviewer", basis: str | None = None,
           actor: str = R.NAMED_HUMAN) -> dict:
    """Reject one mapping: it returns to PROPOSED, with the named rejection
    kept in `review` (no outcome, basis prefixed REJECTED)."""
    R._check_actor(actor)
    R._check_date(date)
    if not isinstance(reviewer_name, str) or not reviewer_name.strip():
        raise ValueError("reviewer_name is required")
    m = find(doc, mapping_id)
    name = reviewer_name.strip()
    proposer = (m.get("proposed_by") or {}).get("name")
    independence = "self" if name in (proposer, m.get("requested_by")) else "independent"
    before = content_sha256(doc)
    m["acceptance_state"] = "PROPOSED"
    m["review"] = _review_record(doc, mapping_id, reviewer_name=name, reviewer_role=reviewer_role,
                                 independence=independence, date=date,
                                 basis="REJECTED" + (f": {basis}" if basis else ""), outcome=None)
    _check(doc, m)
    assert content_sha256(doc) == before
    return m
