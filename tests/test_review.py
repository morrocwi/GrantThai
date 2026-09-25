"""tests/test_review.py — v0.2 module C: named review records, the status
transition table, staleness, mapping acceptance, and the hard ceiling
(MCP and REST cannot reach any of it)."""
import argparse
import copy
import re
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from grantthai import api_py as api  # noqa: E402
from grantthai.cli import cmd_review  # noqa: E402
from grantthai.core import project as P  # noqa: E402
from grantthai.core.object_hash import content_sha256, state_sha256  # noqa: E402
from grantthai.render import submission as S  # noqa: E402
from grantthai.review import mapping as M  # noqa: E402
from grantthai.review import records as R  # noqa: E402
from grantthai.validators import engine as E  # noqa: E402

EXAMPLE = ROOT / "examples/lecturer-no-ai/project.yaml"
FIXTURES = ROOT / "tests/fixtures/review"
AS_OF = "2026-09-25"
DATE = "2026-09-25"
STATUSES = tuple(yaml.safe_load((ROOT / "spec/common/status.yaml").read_text(encoding="utf-8"))["field_status_sequence"])
ACTORS = ("human", "ai_assisted", "deterministic_validator", "named_human", "core")


def linked_doc():
    """The example after a local validator run persisted its statuses."""
    doc = P.load(EXAMPLE)
    res = E.run(doc, EXAMPLE.parent, AS_OF)
    R.link_statuses(doc, res.findings)
    return doc, res


def linked_ids(doc):
    return [r["field_id"] for r, _ in P.iter_records(doc) if r.get("status") == "LOGIC_LINKED"]


def review(doc, gate="RG0", scope=None, independence="self", outcome=None, name="FICTIONAL Reviewer A"):
    return R.add_review(doc, gate_id=gate, reviewer_name=name, reviewer_role="pi",
                        scope=scope if scope is not None else linked_ids(doc),
                        independence=independence, outcome=outcome, date=DATE)


# ------------------------------------------------------ transition table ---

def test_every_transition_not_in_table_is_refused():
    table = yaml.safe_load((ROOT / "spec/common/status_permissions.yaml").read_text(encoding="utf-8"))
    listed = set()
    for t in table["transitions"]:
        for f in (t["from"] if isinstance(t["from"], list) else [t["from"]]):
            for to in (t["to"] if isinstance(t["to"], list) else [t["to"]]):
                for a in t["allowed_actors"]:
                    listed.add((f, to, a))
    checked = 0
    for f in STATUSES:
        for to in STATUSES:
            for a in ACTORS:
                rec = {"field_id": "X", "status": f}
                if (f, to, a) in listed:
                    assert R.transition(rec, to, a)["status"] == to
                else:
                    with pytest.raises(R.TransitionRefused):
                        R.transition(rec, to, a)
                checked += 1
    assert checked == len(STATUSES) ** 2 * len(ACTORS)
    assert listed  # the table is not empty


def test_link_statuses_promotes_only_valid_records_and_regresses_on_block():
    doc, res = linked_doc()
    assert res.report["summary"]["block"] == 0
    assert all(r["status"] == "LOGIC_LINKED" for r, _ in P.iter_records(doc) if r.get("value") is not None)
    assert all(r["status"] == "NEEDS_INPUT" for r, _ in P.iter_records(doc) if r.get("value") is None)
    # A BLOCK finding of a link family on a linked field regresses it to DRAFT.
    fid = linked_ids(doc)[0]
    changed = R.link_statuses(doc, [{"rule_id": "R001", "severity": "BLOCK", "field_ids": [fid]}])
    assert changed == {fid: "DRAFT"}
    # A structure BLOCK keeps a DRAFT record at DRAFT; a link BLOCK stops at STRUCTURE_CHECKED.
    other = linked_ids(doc)[0]
    P.records_by_id(doc)[other]["status"] = "DRAFT"
    changed = R.link_statuses(doc, [{"rule_id": "S002", "severity": "BLOCK", "field_ids": [fid]},
                                    {"rule_id": "CH001", "severity": "BLOCK", "field_ids": [other]}])
    assert fid not in changed and changed[other] == "STRUCTURE_CHECKED"
    with pytest.raises(R.CeilingViolation):
        R.link_statuses(doc, [], actor="ai_assisted")


# --------------------------------------------------------- review records ---

def test_review_keeps_content_sha256_and_promotes_scope():
    doc, _ = linked_doc()
    before = content_sha256(doc)
    rec = review(doc, scope=["CORE.GENERAL.TITLE_EN", "CORE.RESEARCH.PROBLEM"])
    assert rec["content_sha256"] == before == content_sha256(doc)
    assert state_sha256(doc) != before
    recs = P.records_by_id(doc)
    assert recs["CORE.GENERAL.TITLE_EN"]["status"] == "HUMAN_REVIEWED"
    assert recs["CORE.RESEARCH.PROBLEM"]["status"] == "HUMAN_REVIEWED"
    assert recs["CORE.GENERAL.TITLE_TH"]["status"] == "LOGIC_LINKED"
    assert P.schema_errors(doc, P.PROJECT_SCHEMA_ID) == []
    assert rec["outcome"] == "HUMAN_REVIEWED" and rec["scope"] == "CORE.GENERAL.TITLE_EN,CORE.RESEARCH.PROBLEM"
    assert R.stale(doc) == []


def test_review_refuses_field_not_logic_linked():
    doc = P.load(EXAMPLE)  # every status DRAFT
    with pytest.raises(R.TransitionRefused):
        review(doc, scope=["CORE.GENERAL.TITLE_EN"])
    assert doc["review_records"] == [] and P.records_by_id(doc)["CORE.GENERAL.TITLE_EN"]["status"] == "DRAFT"
    # All-or-nothing: one DRAFT field in the scope refuses the whole record.
    doc, _ = linked_doc()
    P.records_by_id(doc)["CORE.GENERAL.TITLE_TH"]["status"] = "DRAFT"
    with pytest.raises(R.TransitionRefused):
        review(doc, scope=["CORE.GENERAL.TITLE_EN", "CORE.GENERAL.TITLE_TH"])
    assert P.records_by_id(doc)["CORE.GENERAL.TITLE_EN"]["status"] == "LOGIC_LINKED"


def test_review_refuses_every_actor_but_named_human():
    doc, _ = linked_doc()
    for actor in ("human", "ai_assisted", "mcp", "rest", "assist", "deterministic_validator", "core", ""):
        with pytest.raises(R.CeilingViolation):
            R.add_review(doc, gate_id="RG0", reviewer_name="X", reviewer_role="pi", scope=linked_ids(doc)[:1],
                         independence="self", date=DATE, actor=actor)
    assert doc["review_records"] == []


def test_review_rejects_bad_inputs():
    doc, _ = linked_doc()
    with pytest.raises(ValueError):
        review(doc, gate="RG9")
    with pytest.raises(ValueError):
        review(doc, independence="peer")
    with pytest.raises(ValueError):
        review(doc, outcome="LOCKED")
    with pytest.raises(ValueError):
        review(doc, name="   ")
    with pytest.raises(ValueError):
        R.add_review(doc, gate_id="RG0", reviewer_name="A", reviewer_role="pi", scope=linked_ids(doc)[:1],
                     independence="self", date="25/09/2026")
    with pytest.raises(ValueError):
        review(doc, scope=["NOT.A.FIELD"])
    with pytest.raises(ValueError):
        review(doc, scope="@chain:NoSuchNode")
    assert doc["review_records"] == []


def test_scope_chain_node_covers_every_record_under_it():
    doc, _ = linked_doc()
    rec = review(doc, gate="RG2", scope="@chain:Method")
    assert rec["scope"] == "@chain:Method"
    for r in doc["chain"]["Method"]:
        assert r["status"] == "HUMAN_REVIEWED"
    assert P.records_by_id(doc)["CORE.GENERAL.TITLE_EN"]["status"] == "LOGIC_LINKED"


def test_authored_edit_makes_review_stale_but_status_change_does_not():
    doc, _ = linked_doc()
    review(doc)
    assert R.stale(doc) == []
    # A further review (a status change) keeps the first record current.
    review(doc, gate="RG1", scope=["CORE.GENERAL.TITLE_EN"], outcome="VERIFIED")
    assert R.stale(doc) == []
    P.set_field(doc, "CORE.GENERAL.TITLE_EN", "an authored change")
    assert R.stale(doc) == ["RG0", "RG1"]
    assert P.records_by_id(doc)["CORE.GENERAL.TITLE_EN"]["status"] == "DRAFT"
    assert R.gate_states(doc)["RG0"]["state"] == "stale"
    # Editing a marker is also an authored change (object-hash.md).
    doc2, _ = linked_doc()
    review(doc2)
    P.records_by_id(doc2)["CORE.GENERAL.TITLE_TH"]["markers"] = ["NEEDS_VERIFICATION"]
    assert R.stale(doc2) == ["RG0"]


def test_further_review_promotes_to_verified_and_never_lowers():
    doc, _ = linked_doc()
    review(doc, scope=["CORE.GENERAL.TITLE_EN"])
    review(doc, gate="RG3", scope=["CORE.GENERAL.TITLE_EN"], outcome="VERIFIED", independence="independent",
           name="FICTIONAL Reviewer B")
    assert P.records_by_id(doc)["CORE.GENERAL.TITLE_EN"]["status"] == "VERIFIED"
    # A later HUMAN_REVIEWED-outcome record over a VERIFIED field leaves it VERIFIED.
    review(doc, gate="RG4", scope=["CORE.GENERAL.TITLE_EN"])
    assert P.records_by_id(doc)["CORE.GENERAL.TITLE_EN"]["status"] == "VERIFIED"
    assert len(doc["review_records"]) == 3


def test_self_review_renders_as_author_checked():
    doc, _ = linked_doc()
    review(doc, gate="RG0", scope=["CORE.GENERAL.TITLE_EN"], outcome="VERIFIED", independence="self")
    assert P.records_by_id(doc)["CORE.GENERAL.TITLE_EN"]["status"] == "VERIFIED"
    text, _ = S.render(doc, EXAMPLE.parent, AS_OF)
    assert "- RG0: AUTHOR_CHECKED (self review)." in text
    assert "- RG0: current (self review by role pi)" in text
    assert "verified project object" not in text


def test_missing_gate_never_blocks_build_and_adds_hold_reason(tmp_path):
    doc, _ = linked_doc()
    assert doc["review_records"] == []
    assert len(R.gate_hold_reasons(doc)) == 5
    assert all("build is not blocked" in h for h in R.gate_hold_reasons(doc))
    path = tmp_path / "project.yaml"
    P.save(doc, path)
    out = api.build(path, as_of=AS_OF)
    text = out.read_text(encoding="utf-8")
    assert "- RG0: not_reviewed (no review record)" in text
    review(doc)
    P.set_field(doc, "CORE.GENERAL.TITLE_EN", "changed")
    assert any(h.startswith("RG0: review stale") for h in R.gate_hold_reasons(doc))


# --------------------------------------------------------------- mappings ---

def with_mappings():
    doc, _ = linked_doc()
    doc["mappings"] = yaml.safe_load((FIXTURES / "mappings.yaml").read_text(encoding="utf-8"))["mappings"]
    assert P.schema_errors(doc, P.PROJECT_SCHEMA_ID) == []
    return doc


def test_mapping_accept_and_reject_touch_only_state():
    doc = with_mappings()
    before = content_sha256(doc)
    m = M.accept(doc, "BRIDGE.MAPPING.SHARED_WATER_TURN", reviewer_name="FICTIONAL Proposer P", date=DATE)
    assert m["acceptance_state"] == "ACCEPTED_SELF" and m["review"]["independence"] == "self"
    m = M.accept(doc, "BRIDGE.MAPPING.RESERVOIR_KEEPER", reviewer_name="FICTIONAL Requester Q", date=DATE)
    assert m["acceptance_state"] == "ACCEPTED_BY_REQUESTER"
    m = M.accept(doc, "BRIDGE.MAPPING.RESERVOIR_KEEPER", reviewer_name="FICTIONAL Reviewer B", date=DATE)
    assert m["acceptance_state"] == "ACCEPTED_REVIEWED" and m["review"]["independence"] == "independent"
    m = M.accept(doc, "BRIDGE.MAPPING.SHARED_WATER_TURN", reviewer_name="FICTIONAL Reviewer B", date=DATE)
    assert m["acceptance_state"] == "ACCEPTED_REVIEWED"
    m = M.reject(doc, "BRIDGE.MAPPING.SHARED_WATER_TURN", reviewer_name="FICTIONAL Reviewer B", date=DATE,
                 basis="term is broader than the concept")
    assert m["acceptance_state"] == "PROPOSED" and m["review"]["basis"].startswith("REJECTED: ")
    assert "outcome" not in m["review"]
    assert content_sha256(doc) == before
    assert P.schema_errors(doc, P.PROJECT_SCHEMA_ID) == []
    assert doc["review_records"] == []  # a mapping review lives on the mapping only
    with pytest.raises(ValueError):
        M.accept(doc, "BRIDGE.MAPPING.NOPE", reviewer_name="A", date=DATE)
    with pytest.raises(R.CeilingViolation):
        M.accept(doc, "BRIDGE.MAPPING.SHARED_WATER_TURN", reviewer_name="A", date=DATE, actor="ai_assisted")
    with pytest.raises(R.CeilingViolation):
        M.reject(doc, "BRIDGE.MAPPING.SHARED_WATER_TURN", reviewer_name="A", date=DATE, actor="mcp")


# ------------------------------------------------------------ hard ceiling ---

def test_hard_ceiling_mcp_and_rest_cannot_reach_review_or_link():
    """Static: neither wrapper, nor the api_py surface they wrap, imports
    the review package or the review CLI module. Functional: every
    promoting function refuses any actor but named_human / the validator."""
    files = list((ROOT / "src/grantthai/mcp").rglob("*.py")) + list((ROOT / "src/grantthai/api").rglob("*.py")) \
        + [ROOT / "src/grantthai/api_py.py"]
    rx = re.compile(r"grantthai\.review|cmd_review|grantthai\.cli\b")
    for f in files:
        assert not rx.search(f.read_text(encoding="utf-8")), f"{f} reaches the review layer"
    assert not any(n in ("add_review", "lock", "link_statuses", "accept") for n in api.__all__)
    assert not hasattr(api, "add_review") and not hasattr(api, "lock")
    doc, _ = linked_doc()
    for actor in ("mcp", "rest", "ai_assisted", "human"):
        with pytest.raises(PermissionError):
            R.add_review(doc, gate_id="RG0", reviewer_name="A", reviewer_role="pi",
                         scope=linked_ids(doc)[:1], independence="self", date=DATE, actor=actor)
        with pytest.raises(PermissionError):
            R.link_statuses(doc, [], actor=actor)
    assert all(r["status"] in ("LOGIC_LINKED", "NEEDS_INPUT") for r, _ in P.iter_records(doc))
    # The MCP validate tool is report-only: the project file keeps every DRAFT.
    assert state_sha256(P.load(EXAMPLE)) == state_sha256(P.load(EXAMPLE))


# -------------------------------------------------------------------- CLI ---

def cli(argv):
    ap = argparse.ArgumentParser(prog="grantthai")
    sub = ap.add_subparsers(dest="cmd", required=True)
    cmd_review.register(sub)
    return cmd_review.run(ap.parse_args(argv))


def test_cli_review_and_mapping_commands(tmp_path, capsys):
    path = tmp_path / "project.yaml"
    P.save(with_mappings(), path)
    assert cli(["review", str(path), "--as", "pi", "--name", "FICTIONAL Reviewer A", "--gate", "RG0",
                "--scope", "CORE.GENERAL.TITLE_EN,CORE.RESEARCH.PROBLEM", "--independence", "self",
                "--outcome", "VERIFIED", "--basis", "read against the cited sources", "--date", DATE]) == 0
    assert "RG0: AUTHOR_CHECKED" in capsys.readouterr().out
    doc = P.load(path)
    assert doc["review_records"][0]["basis"] == "read against the cited sources"
    assert P.records_by_id(doc)["CORE.GENERAL.TITLE_EN"]["status"] == "VERIFIED"
    assert cli(["accept-mapping", str(path), "BRIDGE.MAPPING.RESERVOIR_KEEPER", "--name", "FICTIONAL Requester Q",
                "--date", DATE]) == 0
    assert "ACCEPTED_BY_REQUESTER" in capsys.readouterr().out
    assert cli(["reject-mapping", str(path), "BRIDGE.MAPPING.RESERVOIR_KEEPER", "--name", "FICTIONAL Reviewer B",
                "--date", DATE, "--basis", "no"]) == 0
    assert P.load(path)["mappings"][1]["acceptance_state"] == "PROPOSED"
    # A DRAFT field (an authored edit after linking) is refused by the CLI too.
    api.set_field(path, "CORE.GENERAL.TITLE_TH", "FICTIONAL new Thai title")
    with pytest.raises(R.TransitionRefused):
        cli(["review", str(path), "--as", "pi", "--name", "A", "--gate", "RG1", "--scope", "CORE.GENERAL.TITLE_TH",
             "--independence", "self", "--date", DATE])
    assert len(P.load(path)["review_records"]) == 1
    # An unknown command is not ours.
    ns = argparse.Namespace(cmd="build")
    assert cmd_review.run(ns) is None


def test_cli_link_persists_validator_statuses(tmp_path, capsys):
    path = tmp_path / "project.yaml"
    P.save(P.load(EXAMPLE), path)
    before = content_sha256(P.load(path))
    assert cli(["link", str(path), "--as-of", AS_OF]) == 0
    out = capsys.readouterr().out
    assert "59 status change(s); BLOCK 0" in out
    doc = P.load(path)
    assert content_sha256(doc) == before
    assert copy.deepcopy(linked_ids(doc)) and all(
        r["status"] == "LOGIC_LINKED" for r, _ in P.iter_records(doc) if r.get("value") is not None)
