"""tests/test_rules_added.py — the rules added from the package audit
(S009-S011, R008, R009, W005, B007, E009, F005, C001-C003) and the
crosswalk of every package validation code."""
import json
import re
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


# ------------------------------------------------------------ v0.3 router
# Route data of WP-R3: the ART family, `routes:` on every rule, the
# crosswalk's route_scope mirror, and the academic-article route assets.

ROUTE_DIR = ROOT / "routes/academic-article"
ROUTE_IDS = {"nriis-proposal", "academic-article", "concept-note"}
ART_IDS = [f"ART{n:03d}" for n in range(1, 12)]
REPORT_CAVEAT = "funded final reports, not articles"


def _rules():
    return P.rules_catalog()["rules"]


def test_every_rule_declares_its_routes():
    for r in _rules():
        routes = r.get("routes")
        assert routes, f"{r['id']}: no routes"
        assert routes == ["all"] or (set(routes) <= ROUTE_IDS and "all" not in routes), (r["id"], routes)


def test_ART_family_ids_scope_and_severity():
    art = [r for r in _rules() if r["family"] == "ART"]
    assert [r["id"] for r in art] == ART_IDS
    for r in art:
        assert r["routes"] == ["academic-article"], r["id"]
        assert r["ships"] == "v0.3"
        assert r["negative_fixture"] == f"tests/fixtures/negative/{r['id']}/"
        if r["id"] == "ART007":
            assert r["severity"] == "BLOCK" and r["source"]["derived_from"] == "AGENTS.md"
            assert "non-negotiable 4" in r["source"]["locator"]
        else:
            assert r["severity"] == "REVIEW", r["id"]
    # no ART rule rests a BLOCK on a journal fact: every practice/policy source is REVIEW
    for r in art:
        if r["source"]["derived_from"] != "AGENTS.md":
            assert r["severity"] != "BLOCK", r["id"]
        if r["source"]["derived_from"] == "docs/practice/funded-work-patterns.md":
            assert REPORT_CAVEAT in r["source"]["locator"], r["id"]


def test_crosswalk_route_scope_agrees_with_rules():
    cw = yaml.safe_load((ROOT / "validators/crosswalk.yaml").read_text(encoding="utf-8"))
    rs = cw["route_scope"]
    assert set(rs["routes"]) == ROUTE_IDS
    by_family = {f["family"]: f for f in rs["families"]}
    for r in _rules():
        fam = by_family[r["family"]]
        want = fam["routes"]
        for ex in fam.get("exceptions") or []:
            if r["id"] in ex["rule_ids"]:
                want = ex["routes"]
        assert r["routes"] == want, (r["id"], r["routes"], want)
    for f in rs["families"]:
        assert f["routes"] == ["all"] or set(f["routes"]) <= ROUTE_IDS, f["family"]


def test_nriis_only_and_all_route_scope_per_spec():
    scope = {r["id"]: r["routes"] for r in _rules()}
    for rid in ("S009", "S010", "S012", "W001", "B001", "T001", "F003", "ELIG001", "U001", "P001", "G001", "C001", "FW002"):
        assert scope[rid] == ["nriis-proposal"], rid
    for rid in ("S001", "S002", "R001", "CH002", "X003", "AI001", "AI004", "FW001", "W101"):
        assert scope[rid] == ["all"], rid
    for rid in ("E001", "E009"):
        assert scope[rid] == ["nriis-proposal", "academic-article"], rid


def test_academic_article_route_assets_agree():
    route = yaml.safe_load((ROUTE_DIR / "route.yaml").read_text(encoding="utf-8"))
    assert route["id"] == "academic-article" and route["needs_fund_binding"] is False
    assert route["readiness"]["ready_flag"] == "manuscript_ready"
    assert route["output"]["filename"] == "ACADEMIC_ARTICLE.md"
    for rel in (route["output"]["template"], route["output"]["contract"], route["placement"]):
        assert (ROOT / rel).exists(), rel
    assert "ART" in route["rules"]["include_families"] and "FW002" in route["rules"]["exclude_ids"]
    assert route["required_fields"] == ["ARTICLE.META.KIND", "ARTICLE.FRONT.AUTHORS"]
    assert "not affiliated with any journal or publisher" in route["route_notice_en"]
    assert route["title_th"] == "NEEDS_INPUT"
    # the template is tagged for exactly this route and keeps the NOTICE as body line 1, the route notice as line 2
    tpl = (ROOT / route["output"]["template"]).read_text(encoding="utf-8")
    assert "output_kind: route_output" in tpl and "route: academic-article" in tpl
    assert "output_kind: primary_submission" not in tpl
    body = tpl.split("\n---\n", 2)[2].split("\n")
    assert body[0] == "{{ disclaimer }}" and body[1] == "{{ route_notice }}"
    for word in ("accepted", "publishable"):
        assert f"manuscript_ready: {word}" not in tpl
    # the contract cross-references the one-input-one-output contract
    contract = (ROOT / route["output"]["contract"]).read_text(encoding="utf-8")
    assert "spec/contracts/one-input-one-output.md" in contract
    assert "spec/output/nriis-submission.contract.md" in contract
    # sub-profiles: both shipped, both NEEDS_VERIFICATION, no venue named
    sp_dir = ROOT / route["sub_profiles"]["dir"]
    ids = {yaml.safe_load(p.read_text(encoding="utf-8"))["id"] for p in sp_dir.glob("*.yaml")}
    assert ids == {"thai-journal", "international-journal"} and route["sub_profiles"]["default"] in ids
    for p in sp_dir.glob("*.yaml"):
        sp = yaml.safe_load(p.read_text(encoding="utf-8"))
        assert sp["status"] == "NEEDS_VERIFICATION" and sp["route"] == "academic-article"
        assert sp["id"] == p.stem
        for req in sp["requirements"]:          # GrantThai defaults only: no researcher-supplied venue fact
            assert req["status"] == "NEEDS_VERIFICATION" and req["basis"] == "proposed_default", req
        assert not [r for r in sp["requirements"] if r["item"] in ("abstract_max_words", "body_max_words")]


def test_academic_article_placement_covers_every_article_field_once():
    placement = yaml.safe_load((ROUTE_DIR / "placement.yaml").read_text(encoding="utf-8"))
    assert placement["route"] == "academic-article"
    assert placement["not_placed_policy"] == "appendix"
    ids = [s["id"] for s in placement["sections"]]
    assert len(ids) == len(set(ids))
    placed = [f["field_id"] if isinstance(f, dict) else f for s in placement["sections"] for f in s["fields"]]
    assert len(placed) == len(set(placed))
    art_defs = json.loads((ROOT / "spec/registry/structured_fields.schema.json").read_text(encoding="utf-8"))["$defs"]
    art_structured = {k for k in art_defs if k.startswith("ARTICLE.")}
    assert art_structured <= set(placed), art_structured - set(placed)
    reg = P.registry_by_id()
    for fid in placed:
        if not fid.startswith("ARTICLE."):
            assert fid in reg and reg[fid]["field_id"] == fid, fid
    for s in placement["sections"]:
        assert s["title_th"] == "NEEDS_INPUT"
        for f in (x for x in s["fields"] if isinstance(x, dict)):
            for src in f.get("render_from") or []:
                assert src.startswith("chain:") or src in reg, (f["field_id"], src)
            if f.get("fallback_copy_from"):
                assert f["fallback_copy_from"] in reg
    for fid in placement["appendix_shared"]:
        assert fid in reg, fid
    # every rule input on an ARTICLE field is a placed field
    for r in _rules():
        for inp in r["inputs"]:
            if inp.startswith("ARTICLE."):
                assert inp in placed, (r["id"], inp)


def test_article_structured_defs_are_self_consistent():
    doc = json.loads((ROOT / "spec/registry/structured_fields.schema.json").read_text(encoding="utf-8"))
    defs, nonchain = doc["$defs"], set(doc["x-grantthai-nonchain-node-types"])
    want = {"ARTICLE.FRONT.ABSTRACT_TH", "ARTICLE.FRONT.ABSTRACT_EN", "ARTICLE.FRONT.AUTHORS", "ARTICLE.FRONT.CONTRIBUTIONS",
            "ARTICLE.BODY.SECTIONS", "ARTICLE.STATEMENT.AI_USE", "ARTICLE.BODY.FIGURES_TABLES", "ARTICLE.VENUE.TARGET"}
    assert want <= set(defs)
    for k in ("Author", "Contribution", "FigureTable", "ManuscriptSection"):
        assert k in nonchain
    assert re.match(defs["_node_id"]["pattern"], "ARTICLE.FRONT.AUTHORS") and re.match(defs["_node_id"]["pattern"], "AU1")
    for fid in ("ARTICLE.FRONT.AUTHORS", "ARTICLE.FRONT.CONTRIBUTIONS"):
        items = defs[fid]["items"]
        assert items["properties"]["member_id"]["x-grantthai-ref"]["targets"] == ["PROFILE.TEAM.MEMBERS"]
        assert "member_id" in items["required"]
    roles = defs["ARTICLE.FRONT.CONTRIBUTIONS"]["items"]["properties"]["roles"]["items"]["enum"]
    assert len(roles) == 14 and "NEEDS_VERIFICATION" in defs["ARTICLE.FRONT.CONTRIBUTIONS"]["items"]["properties"]["roles"]["description"]
    assert "source_ref" in defs["ARTICLE.VENUE.TARGET"]["properties"]["stated_requirements"]["items"]["properties"]
