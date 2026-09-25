"""7SSA structure profiles of the academic-article route (work packages S1+S2).

S1 (data, rules, selection):
- the four profiles and the index validate, headings are the source's text
  (7SSA master schema v1.0 §4, §5.1-§5.3), every profile covers S1-S7 once;
- the SSA rule family (7SSA-01..7SSA-10) is REVIEW/INFO only, the rule schema
  refuses a BLOCK from a 7SSA source, and each rule has a negative fixture on
  which it fires and no other 7SSA rule does;
- with no profile selected nothing changes; with an eligible article type
  the router LISTS candidates (INFO RT004) and never selects;
- routing.structure_profiles is outside content_sha256.
S2 (render, export) tests live further down (AT-7SSA-1..3).
"""
import copy
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from grantthai import api_py as api  # noqa: E402
from grantthai.cli import main  # noqa: E402
from grantthai.core import project as P  # noqa: E402
from grantthai.core.object_hash import content_sha256  # noqa: E402
from grantthai.routes import registry as RT  # noqa: E402
from grantthai.routes import structure as ST  # noqa: E402
from grantthai.validators import engine as E  # noqa: E402

AS_OF = "2026-09-25"
EXAMPLE = ROOT / "examples/article-7ssa-fictional/work.yaml"
PLAIN_EXAMPLE = ROOT / "examples/article-fictional/work.yaml"
NEG = ROOT / "tests/fixtures/negative"
SSA_IDS = [f"7SSA-{n:02d}" for n in range(1, 11)]
SSA_DIRS = sorted(d for d in NEG.glob("7SSA-*") if (d / "work.yaml").is_file())
PROFILES = ["7ssa-world", "7ssa-thai-7", "7ssa-thai-5", "7ssa-thai-4"]

# The visible headings, exactly as the founder's 7SSA master schema v1.0 writes them.
HEADINGS = {
    "7ssa-world": ["Introduction", "Approach and Scope", "Theoretical / Conceptual Foundations",
                   "The Unresolved Problem", "Theory / Framework / New Contribution",
                   "Critical Evaluation, Boundary Conditions, and Implications", "Conclusion"],
    "7ssa-thai-7": ["บทนำ", "แนวทางและขอบเขตการวิเคราะห์", "แนวคิด ทฤษฎี และองค์ความรู้ที่เกี่ยวข้อง",
                    "ปัญหา ข้อจำกัด หรือช่องว่างขององค์ความรู้เดิม", "การวิเคราะห์และข้อเสนอใหม่ของผู้เขียน",
                    "การอภิปราย ข้อโต้แย้ง ข้อจำกัด และนัยสำคัญ", "บทสรุป"],
    "7ssa-thai-5": ["บทนำ", "แนวคิดและกรอบการวิเคราะห์", "ปัญหาและข้อจำกัดขององค์ความรู้เดิม",
                    "การวิเคราะห์ ข้อเสนอ และการอภิปราย", "บทสรุป"],
    "7ssa-thai-4": ["บทนำ", "แนวคิดและกรอบการวิเคราะห์", "การวิเคราะห์และข้อเสนอ", "บทสรุป"],
}
MERGES = {"7ssa-world": [["S1"], ["S2"], ["S3"], ["S4"], ["S5"], ["S6"], ["S7"]],
          "7ssa-thai-7": [["S1"], ["S2"], ["S3"], ["S4"], ["S5"], ["S6"], ["S7"]],
          "7ssa-thai-5": [["S1"], ["S2", "S3"], ["S4"], ["S5", "S6"], ["S7"]],
          "7ssa-thai-4": [["S1"], ["S2", "S3"], ["S4", "S5", "S6"], ["S7"]]}
SOURCE_SHA = "1c8989c033254605e5df7c6e1a434cc3d640d061c6bcafe7408fc365d59df980"


def _route():
    return RT.load("academic-article")


# ------------------------------------------------------------------ data --

@pytest.mark.parametrize("pid", PROFILES)
def test_profile_validates_and_carries_the_source_headings(pid):
    prof = ST.load_profile(_route(), pid)
    assert P.schema_errors(prof, ST.SCHEMA_ID) == []
    assert [s["heading"] for s in prof["visible_sections"]] == HEADINGS[pid]
    assert [s["sectors"] for s in prof["visible_sections"]] == MERGES[pid]
    assert prof["source"]["sha256"] == SOURCE_SHA
    assert "NEEDS_VERIFICATION" in prof["status_note"]
    assert prof["excludes_article_kind"] == ["empirical_research"]


def test_index_sectors_slots_overlays_and_selection():
    idx = ST.index(_route())
    assert idx["source"]["sha256"] == SOURCE_SHA
    assert [s["id"] for s in idx["sectors"]] == list(ST.SECTORS)
    assert [s["name_th"] for s in idx["sectors"]][:2] == ["บทนำ", "แนวทาง ขอบเขต และฐานความรู้"]   # §1 master names
    assert idx["writing_order"] == ["S5", "S4", "S3", "S6", "S2", "S1", "S7"]                    # §22
    assert set(idx["article_kind_overlays"]) == set(idx["selection"]["article_types"]) == {
        "conceptual", "theory", "philosophical", "legal", "integrative_review", "formal_conceptual", "cs_sok", "policy"}
    assert idx["article_kind_overlays"]["philosophical"]["headings_en"]["S6"] == "Objections and Replies"
    assert idx["article_kind_overlays"]["legal"]["headings_en"]["S6"] == "Counterauthority / Consequences / Limits"
    assert idx["selection"]["candidates_by_sub_profile"] == {
        "thai-journal": ["7ssa-thai-7", "7ssa-thai-5", "7ssa-thai-4"], "international-journal": ["7ssa-world"]}
    reg = P.registry_by_id()
    for s in idx["sectors"]:
        for f in s["fields"]:
            assert f in reg, f
        for slot in s["slots"]:
            if slot.get("from_field"):
                fid, key = slot["from_field"].split("#")
                assert key in P.schema(P.STRUCTURED_SCHEMA_ID)["$defs"][fid]["properties"], slot


def test_schema_lint_flags_a_profile_that_drops_or_reorders_a_sector():
    sys.path.insert(0, str(ROOT / "tools/ci"))
    import check_schema_lint as L
    prof = copy.deepcopy(ST.load_profile(_route(), "7ssa-thai-5"))
    assert L.check_structure_profile(prof, "x") == []
    prof["visible_sections"][3]["sectors"] = ["S6", "S5"]
    assert L.check_structure_profile(prof, "x")
    prof["visible_sections"][3]["sectors"] = ["S5"]            # S6 dropped
    assert L.check_structure_profile(prof, "x")


# ----------------------------------------------------------------- rules --

def test_ssa_rules_are_review_or_info_and_7ssa_sourced():
    rules = [r for r in P.rules_catalog()["rules"] if r["family"] == "SSA"]
    assert [r["id"] for r in rules] == SSA_IDS
    for r in rules:
        assert r["severity"] in ("REVIEW", "INFO"), r["id"]
        assert r["routes"] == ["academic-article"] and r["ships"] == "v0.3"
        assert r["source"]["derived_from"] == f"7ssa/v1@sha256:{SOURCE_SHA}"
        assert r["source"]["locator"].startswith("7SSA schema v1 §"), r["id"]
        assert r["negative_fixture"] == f"tests/fixtures/negative/{r['id']}/"
        assert "route:structure_profile" in r["inputs"]
    assert {r["id"] for r in rules if r["severity"] == "INFO"} == {"7SSA-08", "7SSA-09"}


def test_rule_schema_refuses_a_block_from_a_7ssa_source():
    cat = copy.deepcopy(P.rules_catalog())
    rule = next(r for r in cat["rules"] if r["id"] == "7SSA-01")
    assert P.schema_errors(cat, "https://github.com/morrocwi/GrantThai/spec/validators/rule.schema.json") == []
    rule["severity"] = "BLOCK"
    assert P.schema_errors(cat, "https://github.com/morrocwi/GrantThai/spec/validators/rule.schema.json")


def test_every_ssa_rule_has_a_fixture():
    assert [d.name for d in SSA_DIRS] == SSA_IDS


@pytest.mark.parametrize("d", SSA_DIRS, ids=lambda d: d.name)
def test_ssa_negative_fixture_fires_alone(d):
    exp = json.loads((d / "expected.json").read_text(encoding="utf-8"))
    assert exp["rule_id"] == d.name
    rep = api.validate(d / "work.yaml", as_of=exp["as_of"], route=exp["route"])
    hits = [f for f in rep["findings"] if f["rule_id"] == d.name]
    assert hits and all(f["severity"] == exp["must_fire_severity"] for f in hits)
    assert {f["rule_id"] for f in rep["findings"] if f["rule_id"].startswith("7SSA")} == {d.name}
    assert rep["summary"]["block"] == 0


def test_ssa_rules_are_silent_without_a_profile_and_off_the_article_route():
    for d in SSA_DIRS:
        doc = P.load(d / "work.yaml")
        doc["routing"].pop("structure_profiles")
        rep = api.validate(doc, as_of=AS_OF, route="academic-article")
        assert not [f for f in rep["findings"] if f["rule_id"].startswith("7SSA")], d.name
    rep = api.validate(EXAMPLE, as_of=AS_OF, route="nriis-proposal")
    assert not [f for f in rep["findings"] if f["rule_id"].startswith("7SSA")]


def test_example_with_its_profile_has_block_zero_and_no_7ssa_finding():
    rep = api.validate(EXAMPLE, as_of=AS_OF)
    assert rep["summary"]["block"] == 0
    assert not [f for f in rep["findings"] if f["rule_id"].startswith("7SSA") or f["severity"] == "REVIEW"]


def test_unknown_profile_is_a_schema_block_and_a_profile_on_nriis_is_refused():
    rep = api.validate(EXAMPLE, as_of=AS_OF, structure_profile="7ssa-nine")
    assert any(f["rule_id"] == "SCHEMA" and f["severity"] == "BLOCK" and "7ssa-nine" in f["message_en"]
               for f in rep["findings"])
    with pytest.raises(ValueError, match="no structure profiles"):
        api.validate(EXAMPLE, as_of=AS_OF, route="nriis-proposal", structure_profile="7ssa-world")


# ------------------------------------------------------------- selection --

def test_router_lists_candidates_and_never_selects(tmp_path):
    doc = P.load(EXAMPLE)
    doc["routing"].pop("structure_profiles")
    before = copy.deepcopy(doc)
    rep = api.validate(doc, as_of=AS_OF)
    rt4 = [f for f in rep["findings"] if f["rule_id"] == "RT004"]
    assert len(rt4) == 1 and rt4[0]["severity"] == "INFO"
    assert "matching sub-profile international-journal: 7ssa-world" in rt4[0]["message_en"]
    assert "7ssa-thai-5" in rt4[0]["message_en"] and "never chooses" in rt4[0]["next_step_en"]
    assert doc == before                                          # nothing was written
    listing = api.list_structure_profiles("academic-article", doc)
    assert listing["selected"] is None and listing["candidates"]["matching"] == ["7ssa-world"]
    # not an eligible article type -> no candidates, no RT004
    doc2 = copy.deepcopy(doc)
    for r in doc2["fields"]:
        if r["field_id"] == "ARTICLE.SSA.ARTICLE_TYPE":
            r["value"] = "other"
    assert not [f for f in api.validate(doc2, as_of=AS_OF)["findings"] if f["rule_id"] == "RT004"]
    # a selected profile -> no RT004
    assert not [f for f in api.validate(EXAMPLE, as_of=AS_OF)["findings"] if f["rule_id"] == "RT004"]


def test_plain_article_example_is_untouched_by_7ssa():
    rep = api.validate(PLAIN_EXAMPLE, as_of=AS_OF)
    ids = {f["rule_id"] for f in rep["findings"]}
    assert not {i for i in ids if i.startswith("7SSA")} and "RT004" not in ids
    assert rep["summary"] == {"block": 0, "review": 3, "info": 15}


def test_structure_profile_choice_is_outside_content_sha256():
    raw = P.load(EXAMPLE)
    base = content_sha256(raw)
    for pid in PROFILES + [None]:
        edited = copy.deepcopy(raw)
        if pid:
            edited["routing"]["structure_profiles"]["academic-article"] = pid
        else:
            edited["routing"].pop("structure_profiles")
        assert content_sha256(edited) == base
        assert P.schema_errors(edited, P.WORK_SCHEMA_ID) == []


def test_cli_validate_and_route_profiles(tmp_path, capsys):
    assert main(["validate", str(EXAMPLE), "--structure-profile", "7ssa-thai-4", "--as-of", AS_OF, "--json"]) == 0
    rep = json.loads(capsys.readouterr().out)
    assert {f["rule_id"] for f in rep["findings"] if f["rule_id"].startswith("7SSA")} == {"7SSA-09"}
    assert main(["route", "profiles", str(EXAMPLE)]) == 0
    out = capsys.readouterr().out
    assert "7ssa-thai-4\tth\tthai-journal\t1=S1 | 2=S2+S3 | 3=S4+S5+S6 | 4=S7" in out
    assert "selected: 7ssa-world" in out


def test_every_ssa_rule_and_rt004_has_a_thai_explanation():
    sys.path.insert(0, str(ROOT / "skills/grantthai/scripts"))
    import grantthai_skill as gs
    th = gs.load_rules_th()
    for rid in SSA_IDS + ["RT004"]:
        assert th.get(rid, "").strip(), rid
