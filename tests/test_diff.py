"""tests/test_diff.py — v0.2 module C: `grantthai diff A B`."""
import argparse
import copy
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from grantthai.cli import cmd_review  # noqa: E402
from grantthai.core import project as P  # noqa: E402
from grantthai.review import diff as D  # noqa: E402
from grantthai.review import lock as L  # noqa: E402
from grantthai.review import mapping as M  # noqa: E402
from grantthai.review import records as R  # noqa: E402
from grantthai.validators import engine as E  # noqa: E402

EXAMPLE = ROOT / "examples/lecturer-no-ai/project.yaml"
FIXTURES = ROOT / "tests/fixtures/review"
AS_OF = "2026-09-25"
DATE = "2026-09-25"


def linked():
    doc = P.load(EXAMPLE)
    res = E.run(doc, EXAMPLE.parent, AS_OF)
    R.link_statuses(doc, res.findings)
    doc["mappings"] = yaml.safe_load((FIXTURES / "mappings.yaml").read_text(encoding="utf-8"))["mappings"]
    return doc, res.report


def test_diff_of_identical_objects_is_empty():
    a = P.load(EXAMPLE)
    d = D.diff(a, copy.deepcopy(a))
    assert d["content_changed"] is False
    assert d["field_changes"] == [] and d["status_changes"] == [] and d["mapping_changes"] == []
    assert d["stale_reviews"] == [] and d["lock"] == {"a": "unlocked", "b": "unlocked"}
    assert d["content_sha256"]["a"] == d["content_sha256"]["b"]


def test_diff_reports_content_status_mapping_and_staleness():
    a, rep = linked()
    ids = [r["field_id"] for r, _ in P.iter_records(a) if r["status"] == "LOGIC_LINKED"]
    for g in R.GATES:
        R.add_review(a, gate_id=g, reviewer_name="FICTIONAL Reviewer A", reviewer_role="pi", scope=ids,
                     independence="self", date=DATE)
    L.lock(a, locked_by="FICTIONAL Reviewer A", date=DATE, validation=rep)
    b = copy.deepcopy(a)
    P.set_field(b, "CORE.RESEARCH.PROBLEM", "changed")                     # authored edit
    P.records_by_id(b)["CORE.GENERAL.TITLE_EN"]["markers"] = ["NEEDS_VERIFICATION"]
    b["fields"].append({"field_id": "CORE.GENERAL.KEYWORDS_EXTRA", "value": "x", "status": "DRAFT",
                        "provenance": P._default_provenance("human")})
    b["chain"]["Objective"] = []                                           # removed records
    M.accept(b, "BRIDGE.MAPPING.SHARED_WATER_TURN", reviewer_name="FICTIONAL Proposer P", date=DATE)
    d = D.diff(a, b)
    assert d["content_changed"] is True
    changes = {c["field_id"]: c for c in d["field_changes"]}
    assert changes["CORE.RESEARCH.PROBLEM"] == {"field_id": "CORE.RESEARCH.PROBLEM", "change": "changed", "keys": ["value"]}
    assert changes["CORE.GENERAL.TITLE_EN"]["keys"] == ["markers"]
    assert changes["CORE.GENERAL.KEYWORDS_EXTRA"]["change"] == "added"
    assert all(c["change"] == "removed" for c in d["field_changes"] if c["field_id"].startswith("CORE.RESEARCH.OBJECTIVES"))
    assert {"field_id": "CORE.RESEARCH.PROBLEM", "from": "HUMAN_REVIEWED", "to": "DRAFT"} in d["status_changes"]
    assert d["stale_reviews"] == list(R.GATES)
    assert d["mapping_changes"] == [{"id": "BRIDGE.MAPPING.SHARED_WATER_TURN", "from": "PROPOSED", "to": "ACCEPTED_SELF"}]
    assert d["lock"] == {"a": "locked", "b": "broken"}
    assert d["review_records"] == {"a": 5, "b": 5}
    # Deterministic and JSON-serialisable; sorted by id.
    assert json.dumps(d, sort_keys=True) == json.dumps(D.diff(a, b), sort_keys=True)
    assert [c["field_id"] for c in d["field_changes"]] == sorted(c["field_id"] for c in d["field_changes"])


def test_diff_cli(tmp_path, capsys):
    a, _ = linked()
    b = copy.deepcopy(a)
    P.set_field(b, "CORE.GENERAL.TITLE_EN", "new")
    pa, pb = tmp_path / "a.yaml", tmp_path / "b.yaml"
    P.save(a, pa)
    P.save(b, pb)
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    cmd_review.register(sub)
    assert cmd_review.run(ap.parse_args(["diff", str(pa), str(pb)])) == 0
    out = capsys.readouterr().out
    assert "content changed: yes" in out and "changed CORE.GENERAL.TITLE_EN (value)" in out
    assert "status CORE.GENERAL.TITLE_EN: LOGIC_LINKED -> DRAFT" in out
    assert cmd_review.run(ap.parse_args(["diff", str(pa), str(pb), "--json"])) == 0
    assert json.loads(capsys.readouterr().out)["content_changed"] is True
