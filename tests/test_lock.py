"""tests/test_lock.py — v0.2 module C: the object LOCK, plus AT-2 extended
(validate -> link -> review RG0..RG4 -> lock -> build shows every gate
current) and the object-hash golden vectors staying unchanged."""
import argparse
import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from grantthai import api_py as api  # noqa: E402
from grantthai.cli import cmd_review  # noqa: E402
from grantthai.core import project as P  # noqa: E402
from grantthai.core.object_hash import content_sha256, load_project_text, state_sha256  # noqa: E402
from grantthai.review import lock as L  # noqa: E402
from grantthai.review import records as R  # noqa: E402
from grantthai.validators import engine as E  # noqa: E402

EXAMPLE = ROOT / "examples/lecturer-no-ai/project.yaml"
GOLDEN = ROOT / "tests/golden/object-hash"
AS_OF = "2026-09-25"
DATE = "2026-09-25"
NAME = "FICTIONAL Reviewer A"


def reviewed_doc(independence="self"):
    """The example linked and reviewed at every gate (every linked field in RG0)."""
    doc = P.load(EXAMPLE)
    res = E.run(doc, EXAMPLE.parent, AS_OF)
    R.link_statuses(doc, res.findings)
    ids = [r["field_id"] for r, _ in P.iter_records(doc) if r["status"] == "LOGIC_LINKED"]
    scopes = {"RG0": ids, "RG1": "@chain:Problem", "RG2": "@chain:Method", "RG3": "@chain:Objective", "RG4": ids}
    for g in R.GATES:
        R.add_review(doc, gate_id=g, reviewer_name=NAME, reviewer_role="pi", scope=scopes[g],
                     independence=independence, date=DATE)
    return doc, res.report


def test_lock_requires_every_gate_current_and_reviewed():
    doc, rep = reviewed_doc()
    doc["review_records"] = [r for r in doc["review_records"] if r["gate_id"] != "RG4"]
    reasons = L.unmet(doc, validation=rep)
    assert reasons == ["RG4: no review record"]
    with pytest.raises(L.LockRefused) as exc:
        L.lock(doc, locked_by=NAME, date=DATE, validation=rep)
    assert "RG4: no review record" in str(exc.value)
    assert doc["lock"] == {"locked": False} and L.status(doc) == "unlocked"
    # A hand-written record without an outcome does not count as HUMAN_REVIEWED or better.
    doc, rep = reviewed_doc()
    doc["review_records"][2].pop("outcome")
    assert any(r.startswith("RG2: latest review record has no outcome") for r in L.unmet(doc, validation=rep))


def test_lock_keeps_content_sha256_and_records_it():
    doc, rep = reviewed_doc()
    before = content_sha256(doc)
    lk = L.lock(doc, locked_by=NAME, date=DATE, validation=rep)
    assert lk == {"locked": True, "locked_at": DATE, "locked_by": NAME, "locked_content_sha256": before}
    assert content_sha256(doc) == before
    assert L.is_locked(doc) and not L.is_broken(doc)
    assert R.stale(doc) == []
    assert P.schema_errors(doc, P.PROJECT_SCHEMA_ID) == []
    # Applying the lock changes no field status (status.yaml lock_vs_field_locked).
    assert all(r["status"] in ("HUMAN_REVIEWED", "NEEDS_INPUT") for r, _ in P.iter_records(doc))


def test_authored_edit_breaks_lock_and_stales_reviews():
    doc, rep = reviewed_doc()
    L.lock(doc, locked_by=NAME, date=DATE, validation=rep)
    edited = copy.deepcopy(doc)
    P.set_field(edited, "CORE.RESEARCH.PROBLEM", "an authored change")
    assert L.is_broken(edited) and not L.is_locked(edited) and L.status(edited) == "broken"
    assert R.stale(edited) == list(R.GATES)
    # A hand edit that leaves lock.locked true is broken too (hash mismatch).
    hand = copy.deepcopy(doc)
    P.records_by_id(hand)["CORE.RESEARCH.PROBLEM"]["value"] = "typed straight into project.yaml"
    assert hand["lock"]["locked"] is True and L.is_broken(hand)
    # A status change after the lock does not break it.
    later = copy.deepcopy(doc)
    R.add_review(later, gate_id="RG3", reviewer_name="FICTIONAL Reviewer B", reviewer_role="external",
                 scope=["CORE.RESEARCH.PROBLEM"], independence="independent", outcome="VERIFIED", date=DATE)
    assert L.is_locked(later) and R.stale(later) == []


def test_lock_requires_independent_review_when_fund_profile_says_so():
    doc, rep = reviewed_doc(independence="self")
    prof = {"independent_review_required": True}
    reasons = L.unmet(doc, validation=rep, fund_profile=prof)
    assert len(reasons) == 5 and all("requires an independent review" in r for r in reasons)
    with pytest.raises(L.LockRefused):
        L.lock(doc, locked_by=NAME, date=DATE, validation=rep, fund_profile=prof)
    assert L.status(doc) == "unlocked"
    doc, rep = reviewed_doc(independence="independent")
    assert L.unmet(doc, validation=rep, fund_profile=prof) == []
    L.lock(doc, locked_by=NAME, date=DATE, validation=rep, fund_profile=prof)
    assert L.is_locked(doc)
    # The bound FICTIONAL profile sets it false, so self reviews lock.
    doc, rep = reviewed_doc(independence="self")
    assert L.unmet(doc, validation=rep) == []


def test_lock_refuses_block_findings_unreviewed_required_fields_and_other_actors():
    doc, rep = reviewed_doc()
    bad = dict(rep, summary=dict(rep["summary"], block=1))
    assert L.unmet(doc, validation=bad) == ["validation report has BLOCK 1 (needs 0)"]
    doc2 = copy.deepcopy(doc)
    P.records_by_id(doc2)["CORE.RESEARCH.PROBLEM"]["status"] = "LOGIC_LINKED"
    assert L.unmet(doc2, validation=rep) == ["CORE.RESEARCH.PROBLEM: required field is LOGIC_LINKED, "
                                            "not HUMAN_REVIEWED or better"]
    for actor in ("human", "ai_assisted", "mcp", "rest", "core"):
        with pytest.raises(PermissionError):
            L.lock(doc, locked_by=NAME, date=DATE, validation=rep, actor=actor)
    with pytest.raises(ValueError):
        L.lock(doc, locked_by=" ", date=DATE, validation=rep)
    with pytest.raises(ValueError):
        L.lock(doc, locked_by=NAME, date="today", validation=rep)
    assert L.status(doc) == "unlocked"


# ------------------------------------------------------- AT-2 extended ---

def cli(argv):
    ap = argparse.ArgumentParser(prog="grantthai")
    sub = ap.add_subparsers(dest="cmd", required=True)
    cmd_review.register(sub)
    return cmd_review.run(ap.parse_args(argv))


def test_at2_extended_validate_link_review_lock_build(tmp_path, capsys):
    path = tmp_path / "project.yaml"
    P.save(P.load(EXAMPLE), path)
    before = content_sha256(P.load(path))

    rep = api.validate(path, as_of=AS_OF)                       # validate (report-only)
    assert rep["summary"]["block"] == 0
    assert cli(["link", str(path), "--as-of", AS_OF]) == 0       # persist STRUCTURE_CHECKED / LOGIC_LINKED
    ids = ",".join(r["field_id"] for r, _ in P.iter_records(P.load(path)) if r["status"] == "LOGIC_LINKED")
    scopes = {"RG0": ids, "RG1": "@chain:Problem", "RG2": "@chain:Method", "RG3": "@chain:Objective", "RG4": ids}
    for g in R.GATES:                                            # review RG0..RG4
        assert cli(["review", str(path), "--as", "pi", "--name", NAME, "--gate", g, "--scope", scopes[g],
                    "--independence", "self", "--date", DATE]) == 0
    assert cli(["lock", str(path), "--by", NAME, "--date", DATE, "--as-of", AS_OF]) == 0   # lock
    assert "locked by " + NAME in capsys.readouterr().out
    doc = P.load(path)
    assert content_sha256(doc) == before and L.is_locked(doc)

    out = api.build(path, as_of=AS_OF)                           # build
    text = out.read_text(encoding="utf-8")
    for g in R.GATES:
        assert f"- {g}: current (self review by role pi)" in text
    assert "project_locked: true" in text
    assert f"project_content_sha256: {before}" in text
    assert "AUTHOR_CHECKED" in text and "verified project object" not in text
    # Build is deterministic and does not touch the project file.
    assert state_sha256(P.load(path)) == state_sha256(doc)
    assert api.build(path, as_of=AS_OF).read_text(encoding="utf-8") == text

    # Refusing to lock twice is not required; an edit after the lock breaks it.
    api.set_field(path, "CORE.RESEARCH.PROBLEM", "edited after lock")
    assert L.is_broken(P.load(path))
    with pytest.raises(L.LockRefused):
        cli(["lock", str(path), "--by", NAME, "--date", DATE, "--as-of", AS_OF])


def test_object_hash_golden_vectors_unchanged():
    for vec in json.loads((GOLDEN / "expected.json").read_text(encoding="utf-8")):
        doc = load_project_text((GOLDEN / vec["input"]).read_text(encoding="utf-8"))
        assert content_sha256(doc) == vec["content_sha256"], vec["input"]
        assert state_sha256(doc) == vec["state_sha256"], vec["input"]
