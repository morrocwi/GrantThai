"""tests/test_rules_added.py — the rules added from the package audit
(S009-S011, R008, R009, W005, B007, E009, F005, C001-C003) and the
crosswalk of every package validation code."""
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from grantthai import api_py as api  # noqa: E402
from grantthai.core import project as P  # noqa: E402

EXAMPLE = ROOT / "examples/lecturer-no-ai/project.yaml"
AS_OF = "2026-09-25"
H = {"provenance_class": "DECISION", "source_type": "PROJECT_DOCUMENT", "evidence_role": "ORIENTING",
     "authored_by": "human"}


def _report(tmp_path, mutate):
    doc = P.load(EXAMPLE)
    mutate(doc)
    path = tmp_path / "project.yaml"
    P.save(doc, path)
    return api.validate(path, as_of=AS_OF)


def _ids(rep, sev):
    return [f["rule_id"] for f in rep["findings"] if f["severity"] == sev]


def _rec(doc, fid):
    return P.records_by_id(doc)[fid]


def _add(doc, fid, value, chain=None):
    rec = {"field_id": fid, "value": value, "status": "DRAFT", "provenance": dict(H)}
    if chain:
        doc["chain"].setdefault(chain, []).append(rec)
    else:
        doc["fields"].append(rec)


def test_example_has_none_of_the_added_findings():
    rep = api.validate(EXAMPLE, as_of=AS_OF)
    added = {"S009", "S010", "S011", "S012", "R008", "R009", "W005", "B007", "E009", "F005"}
    assert not added & set(_ids(rep, "REVIEW") + _ids(rep, "BLOCK"))
    assert {"C001", "C002", "C003"} <= set(_ids(rep, "INFO"))


def test_S009_required_attachment_not_supplied(tmp_path):
    rep = _report(tmp_path, lambda d: _rec(d, "DOC.ATTACHMENTS.DOCUMENTS")["value"][0].update(required_status="REQUIRED"))
    assert "S009" in _ids(rep, "REVIEW")


def test_S010_activity_past_duration(tmp_path):
    def m(d):
        _rec(d, "CORE.GENERAL.DURATION_Y")["value"] = 0
        _rec(d, "CORE.GENERAL.DURATION_M")["value"] = 6
    assert "S010" in _ids(_report(tmp_path, m), "REVIEW")


def test_S011_candidate_values_review_never_block(tmp_path):
    rep = _report(tmp_path, lambda d: _add(d, "CORE.GENERAL.CHARACTERISTIC", "Continuing Project"))
    assert "S011" in _ids(rep, "REVIEW") and "S003" not in _ids(rep, "BLOCK")
    assert "S005" in _ids(rep, "BLOCK")          # a continuing project needs its past-performance table
    rep = _report(tmp_path, lambda d: _add(d, "CORE.GENERAL.CHARACTERISTIC", "Something else"))
    assert "S003" in _ids(rep, "BLOCK")
    rep = _report(tmp_path, lambda d: _rec(d, "CORE.GENERAL.OECD.SECONDARY").update(value="9.9 not listed"))
    assert "S011" in _ids(rep, "REVIEW") and "S003" not in _ids(rep, "BLOCK")
    rep = _report(tmp_path, lambda d: _rec(d, "CORE.GENERAL.OECD.SECONDARY").update(value="6.4 สังคมศาสตร์"))
    assert "S011" not in _ids(rep, "REVIEW")


def test_R008_instrument_without_construct(tmp_path):
    rep = _report(tmp_path, lambda d: _rec(d, "METHOD.PLAN.INSTRUMENTS")["value"][0].pop("construct_measured"))
    assert "R008" in _ids(rep, "REVIEW")


def test_R009_hypothesis_without_test(tmp_path):
    rep = _report(tmp_path, lambda d: _add(d, "CORE.RESEARCH.HYPOTHESES",
                                           [{"id": "HYP1", "statement": "FICTIONAL"}], chain="Hypothesis"))
    assert "R009" in _ids(rep, "REVIEW")


def test_W005_and_B007_partner_checks(tmp_path):
    rep = _report(tmp_path, lambda d: _add(d, "WORK.PARTNERS.ORGANIZATIONS", [
        {"id": "PTN1", "organization_name": "FICTIONAL partner", "in_cash": 0, "in_kind": 1000,
         "total_contribution": 1500}]))
    assert "W005" in _ids(rep, "REVIEW")
    msgs = [f["message_en"] for f in rep["findings"] if f["rule_id"] == "B007"]
    assert len(msgs) == 2                        # no valuation basis, and the total does not add up


def test_E009_ip_use_without_permission(tmp_path):
    rep = _report(tmp_path, lambda d: _rec(d, "CORE.NARRATIVE.IP_CHECK")["value"].update(
        check_status="CHECKED_RELATED_FOUND", related_ip=[{"id": "IPR1", "use_in_project": True}]))
    assert "E009" in _ids(rep, "REVIEW")


def test_F005_duplicate_funding_risk(tmp_path):
    def m(d):
        _rec(d, "CORE.GENERAL.OTHER_FUNDER")["value"] = True
        _add(d, "CORE.GENERAL.OTHER_FUNDER.AGENCY", "FICTIONAL other agency")
        _add(d, "CORE.GENERAL.OTHER_FUNDER.TITLE", "FICTIONAL other title")
        _add(d, "CORE.GENERAL.OTHER_FUNDER.DIFF", "FICTIONAL difference")
    rep = _report(tmp_path, m)
    assert "F005" in _ids(rep, "REVIEW") and "S005" not in _ids(rep, "BLOCK")


def test_crosswalk_covers_every_package_code_with_real_rule_ids():
    cw = yaml.safe_load((ROOT / "validators/crosswalk.yaml").read_text(encoding="utf-8"))
    rules = {r["id"] for r in P.rules_catalog()["rules"]}
    entries = cw["crosswalk"]
    for src, meta in cw["sources"].items():
        codes = [e["code"] for e in entries if e["source"] == src]
        assert len(codes) == meta["codes"] == len(set(codes)), src
    assert {s: m["codes"] for s, m in cw["sources"].items()} == {"core/02 §10": 37, "core/04 §30": 41, "core/05": 12}
    for e in entries:
        assert set(e["grantthai_rule_ids"]) <= rules, e
        assert e["coverage"] in ("full", "partial", "none")
        if e["coverage"] != "full":
            assert e.get("note"), e
        assert bool(e["grantthai_rule_ids"]) == (e["coverage"] != "none"), e
    # the audit's uncovered codes are now mapped
    got = {(e["source"], e["code"]): e["grantthai_rule_ids"] for e in entries}
    for key, rid in {("core/02 §10", "V-S06"): "S009", ("core/02 §10", "V-S07"): "S010",
                     ("core/02 §10", "V-R06"): "R008", ("core/02 §10", "V-R08"): "R009",
                     ("core/02 §10", "V-I07"): "W005", ("core/02 §10", "V-C01"): "C001",
                     ("core/04 §30", "V-I03"): "S010", ("core/04 §30", "V-B05"): "B007",
                     ("core/04 §30", "V-E03"): "E009", ("core/04 §30", "V-F03"): "F005",
                     ("core/05", "VAL.005"): "R008", ("core/05", "VAL.012"): "C001"}.items():
        assert rid in got[key], key


@pytest.mark.parametrize("rid", ["C001", "C002", "C003"])
def test_classification_rules_are_reported_as_not_evaluated(rid):
    assert api.explain(rid)["implemented_in_v0_1"] is False
