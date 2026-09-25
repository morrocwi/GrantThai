"""tests/test_ai_use_ceiling.py — the AI-use ceiling (docs/policy/ai-use-ceiling.md).

Covers: rules AI001-AI004 (REVIEW only, each with a negative case and a
quiet case), the automatic tool record on every AI-assisted write (core,
CLI, MCP, HTTP), the rule that only the researcher confirms the
declaration, the data warning shown before accepting data, section 4.7 of
the output, the shared PII patterns, and the policy documents' crosswalk.
Personal-data-shaped strings are built at run time, never committed."""
import re
import shutil
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools" / "ci"))
sys.path.insert(0, str(ROOT / "skills" / "grantthai" / "scripts"))

import grantthai_skill as gs  # noqa: E402
import make_negative_fixtures as gen  # noqa: E402
from grantthai import api_py as api  # noqa: E402
from grantthai.core import pii  # noqa: E402
from grantthai.core import project as P  # noqa: E402
from grantthai.mcp import tools as T  # noqa: E402
from grantthai.validators import engine as E  # noqa: E402

EXAMPLE = ROOT / "examples/lecturer-no-ai/project.yaml"
DEMO = ROOT / "examples/demo-seedbank"
AS_OF = "2026-09-25"
AI_RULES = {"AI001", "AI002", "AI003", "AI004"}
POLICY_EN = ROOT / "docs/policy/ai-use-ceiling.md"
POLICY_TH = ROOT / "docs/policy/ai-use-ceiling.th.md"


def _ids(rep, sev):
    return [f["rule_id"] for f in rep["findings"] if f["severity"] == sev]


def _findings(rep, rid):
    return [f for f in rep["findings"] if f["rule_id"] == rid]


def _report(tmp_path, mutate, base=EXAMPLE):
    doc = P.load(base)
    mutate(doc)
    path = tmp_path / "project.yaml"
    P.save(doc, path)
    return api.validate(path, as_of=AS_OF)


def _full_declaration(confirmed=True):
    return {"tools": [{"name": "tool-x", "version": "1.0", "stages": ["proposal_writing"],
                       "purpose": "reworded the researcher's answers"}],
            "influence_on_conclusions": "none; the researcher decided every research choice",
            "human_verification": "the PI checked every AI-assisted value against the notes",
            "data_handling": "only the researcher's own non-personal answers were typed in",
            "declaration_confirmed_by_human": confirmed}


def _synthetic_pii() -> str:
    import random
    tid = gen.synthetic_thai_id(random.Random(7))
    return f"ติดต่อ {tid} หรือ " + "someone" + "@" + "univ.ac.th" + " โทร " + "08" + "1-234-5678"


# ------------------------------------------------------------ catalog

def test_AI_rules_are_review_only_and_cite_guideline_pages():
    rules = [r for r in P.rules_catalog()["rules"] if r["family"] == "AI"]
    assert {r["id"] for r in rules} == AI_RULES
    for r in rules:
        assert r["severity"] == "REVIEW", r["id"]
        assert r["source"]["derived_from"] == "docs/policy/ai-use-ceiling.md"
        assert "GenAI guideline 2569" in r["source"]["locator"] and re.search(r"p\.\d", r["source"]["locator"])
        assert r["id"] in E.EVALUATED_AFTER_V01
        assert r["negative_fixture"].startswith("test:tests/test_ai_use_ceiling.py::test_" + r["id"])


def test_every_AI_rule_has_a_thai_explanation():
    th = gs.load_rules_th()
    for rid in AI_RULES:
        assert th.get(rid, "").strip(), rid


def test_worked_example_has_no_AI_findings():
    rep = api.validate(EXAMPLE, as_of=AS_OF)
    assert not AI_RULES & {f["rule_id"] for f in rep["findings"]}


# ------------------------------------------------------------ AI001

def test_AI001_ai_use_without_confirmed_declaration(tmp_path):
    rep = _report(tmp_path, lambda d: P.set_field(d, "CORE.GENERAL.TITLE_EN", "A title", actor="ai_assisted",
                                                  tool="tool-x"))
    assert "AI001" in _ids(rep, "REVIEW") and "AI001" not in _ids(rep, "BLOCK")
    msgs = " ".join(f["message_en"] for f in _findings(rep, "AI001"))
    assert "not confirmed" in msgs and "version" in msgs and "purpose" in msgs

    def no_decl(d):
        d["authoring"]["mode"] = "ai_assisted"
    rep = _report(tmp_path, no_decl)
    assert any("missing" in f["message_en"] for f in _findings(rep, "AI001"))

    def full(d):
        P.set_field(d, "CORE.GENERAL.TITLE_EN", "A title", actor="ai_assisted", tool="tool-x",
                    tool_version="1.0")
        d["authoring"]["ai_use_declaration"] = _full_declaration(confirmed=True)
    assert "AI001" not in {f["rule_id"] for f in _report(tmp_path, full)["findings"]}


def test_AI001_confirmation_is_the_researchers(tmp_path):
    def unconfirmed(d):
        P.set_field(d, "CORE.GENERAL.TITLE_EN", "A title", actor="ai_assisted", tool="tool-x")
        d["authoring"]["ai_use_declaration"] = _full_declaration(confirmed=False)
    msgs = [f["message_en"] for f in _findings(_report(tmp_path, unconfirmed), "AI001")]
    assert msgs == [m for m in msgs if "not confirmed" in m] and msgs


# ------------------------------------------------------------ AI002

def test_AI002_ai_drafted_evidence(tmp_path):
    def ai_evidence(d):
        rec = d["chain"]["Evidence"][0]
        rec["provenance"].update({"authored_by": "ai_draft", "provenance_class": "INFERENCE"})
    rep = _report(tmp_path, ai_evidence)
    assert "AI002" in _ids(rep, "REVIEW") and "AI002" not in _ids(rep, "BLOCK")
    assert _findings(rep, "AI002")[0]["field_ids"] == ["CORE.EVIDENCE.E1"]
    # X003 still blocks the same record when it claims SOURCE
    def ai_evidence_source(d):
        d["chain"]["Evidence"][0]["provenance"]["authored_by"] = "ai_draft"
    rep = _report(tmp_path, ai_evidence_source)
    assert "X003" in _ids(rep, "BLOCK") and "AI002" in _ids(rep, "REVIEW")


def test_AI002_quiet_for_plans_and_human_evidence(tmp_path):
    def ai_plan(d):
        for rec in d["chain"]["Data"]:
            rec["provenance"].update({"authored_by": "ai_draft", "provenance_class": "INFERENCE"})
    assert "AI002" not in _ids(_report(tmp_path, ai_plan), "REVIEW")


# ------------------------------------------------------------ AI003

def test_AI003_pii_in_ai_assisted_value(tmp_path):
    text = _synthetic_pii()
    assert {k for k, _ in pii.find(text)} == {"thai_national_id", "email", "phone"}
    rep = _report(tmp_path, lambda d: P.set_field(d, "CORE.NARRATIVE.SUMMARY", text, actor="ai_assisted",
                                                  tool="tool-x"))
    f = _findings(rep, "AI003")
    assert f and f[0]["severity"] == "REVIEW" and f[0]["field_ids"] == ["CORE.NARRATIVE.SUMMARY"]
    # the finding names the kind of string, never the string itself
    for _, s in pii.find(text):
        assert s not in f[0]["message_en"]
    assert "p.14" in f[0]["message_en"]


def test_AI003_quiet_for_human_values_and_placeholders(tmp_path):
    text = _synthetic_pii()
    assert "AI003" not in _ids(_report(tmp_path, lambda d: P.set_field(d, "CORE.NARRATIVE.SUMMARY", text)),
                               "REVIEW")
    placeholder = "write to " + "someone" + "@" + "example.org"
    rep = _report(tmp_path, lambda d: P.set_field(d, "CORE.NARRATIVE.SUMMARY", placeholder,
                                                  actor="ai_assisted", tool="tool-x"))
    assert "AI003" not in _ids(rep, "REVIEW")


def test_leak_guard_and_engine_share_one_pattern_set():
    src = (ROOT / "tools/ci/check_leak_pii.py").read_text(encoding="utf-8")
    assert "from grantthai.core.pii import" in src
    assert "re.compile(r\"[A-Za-z0-9._%+" not in src   # no second copy of the e-mail pattern


# ------------------------------------------------------------ AI004

def test_AI004_high_self_assessed_risk(tmp_path):
    def high(d):
        P.set_field(d, "CORE.GENERAL.TITLE_EN", "A title", actor="ai_assisted", tool="tool-x")
        decl = _full_declaration()
        decl["risk_self_assessment"] = {"impact_on_conclusions": 1, "accuracy_hallucination": 2,
                                        "data_sensitivity": 3, "bias": 1, "reproducibility": 1}
        d["authoring"]["ai_use_declaration"] = decl
    f = _findings(_report(tmp_path, high), "AI004")
    assert f and f[0]["severity"] == "REVIEW"
    assert "GrantThai convention" in f[0]["message_en"] and "not the guideline's" in f[0]["message_en"]
    assert "data_sensitivity" in f[0]["message_en"] and "p.14-16" in f[0]["message_en"]


def test_AI004_quiet_below_three_and_convention_is_max():
    assert E.convention_risk_level({"impact_on_conclusions": 2, "bias": 1}) == 2
    assert E.convention_risk_level({}) is None
    assert E.convention_risk_level({"bias": True}) is None


# ------------------------------------------------------------ automatic tool record

def test_ai_write_records_tool_and_reset_of_confirmation():
    doc = P.load(EXAMPLE)
    P.set_field(doc, "CORE.GENERAL.TITLE_EN", "A title", actor="ai_assisted", tool="tool-x", tool_version="2.1")
    decl = doc["authoring"]["ai_use_declaration"]
    assert decl["tools"] == [{"name": "tool-x", "version": "2.1", "stages": ["proposal_writing"],
                              "purpose": "NEEDS_INPUT"}]
    assert decl["declaration_confirmed_by_human"] is False
    assert doc["authoring"]["tools_disclosed"] == ["tool-x"]
    decl["declaration_confirmed_by_human"] = True      # the researcher confirms
    P.set_field(doc, "CORE.GENERAL.TITLE_EN", "Another", actor="ai_assisted", tool="tool-x")
    assert decl["declaration_confirmed_by_human"] is True   # same tool, same stage: unchanged
    P.set_field(doc, "CORE.GENERAL.KEYWORDS_EN", ["a"], actor="ai_assisted", tool="tool-x", stage="language_editing")
    assert decl["tools"][0]["stages"] == ["proposal_writing", "language_editing"]
    assert decl["declaration_confirmed_by_human"] is False  # new use: re-confirm
    with pytest.raises(ValueError):
        P.set_field(doc, "CORE.GENERAL.TITLE_EN", "x", actor="ai_assisted", tool="tool-x", stage="peer_review")


def test_human_write_does_not_touch_the_declaration():
    doc = P.load(EXAMPLE)
    P.set_field(doc, "CORE.GENERAL.TITLE_EN", "A title")
    assert "ai_use_declaration" not in doc["authoring"]


def test_mcp_records_client_tool_and_version_and_warns(tmp_path):
    ctx = T.Context(root=tmp_path, client_name="test-client", client_version="9.9")
    r = T.call_tool(ctx, "grantthai_new_project", {"project_id": "PRJ-AI"})
    assert r["data_warning"]["en"] == pii.DATA_WARNING_EN and "p.14-16" in r["data_warning"]["en"]
    assert "หน้า 14–16" in r["data_warning"]["th"]
    assert "BEFORE you accept any research data" in T.INSTRUCTIONS
    T.call_tool(ctx, "grantthai_set_field", {"field_id": "CORE.GENERAL.TITLE_EN", "value": "t"})
    tools = P.load(tmp_path / "project.yaml")["authoring"]["ai_use_declaration"]["tools"]
    assert tools == [{"name": "test-client", "version": "9.9", "stages": ["proposal_writing"],
                      "purpose": "NEEDS_INPUT"}]
    T.call_tool(ctx, "grantthai_set_field", {"field_id": "CORE.GENERAL.TITLE_EN", "value": "t",
                                             "tool": "other-tool", "stage": "literature"})
    tools = P.load(tmp_path / "project.yaml")["authoring"]["ai_use_declaration"]["tools"]
    assert tools[1] == {"name": "other-tool", "version": "NEEDS_INPUT", "stages": ["literature"],
                        "purpose": "NEEDS_INPUT"}   # the client's version is not guessed for a named tool


def test_http_write_records_tool_and_create_warns(tmp_path):
    sys.path.insert(0, str(ROOT / "tests" / "api"))
    from test_http_api import Client  # noqa: E402
    from grantthai.api import make_app
    client = Client(make_app(tmp_path / "work"))
    s, _, j = client.post("/projects", {"project_id": "w"})
    assert s == 201 and j["data_warning"]["th"] == pii.DATA_WARNING_TH
    s, _, j = client.patch("/projects/w/fields", {"field_id": "CORE.GENERAL.TITLE_EN", "value": "t",
                                                  "tool": "web-assistant", "tool_version": "3", "stage": "writing"})
    assert s == 200
    tools = api.load(tmp_path / "work/w/project.yaml")["authoring"]["ai_use_declaration"]["tools"]
    assert tools == [{"name": "web-assistant", "version": "3", "stages": ["writing"], "purpose": "NEEDS_INPUT"}]
    s, _, j = client.patch("/projects/w/fields", {"field_id": "CORE.GENERAL.TITLE_EN", "value": "t",
                                                  "stage": "peer-review"})
    assert s == 400


def test_skill_refuses_confirmation_from_an_answers_file():
    doc = P.load(EXAMPLE)
    with pytest.raises(ValueError, match="only be set by the researcher"):
        gs.merge_declaration(doc, {"declaration_confirmed_by_human": True})
    with pytest.raises(ValueError, match="unknown keys"):
        gs.merge_declaration(doc, {"signature": "x"})
    lines = gs.merge_declaration(doc, {"tools": [{"name": "t", "purpose": "p", "stages": ["idea"]}],
                                       "human_verification": "checked"})
    decl = doc["authoring"]["ai_use_declaration"]
    assert decl["declaration_confirmed_by_human"] is False and "updated" in lines[0]
    assert decl["tools"][0]["stages"] == ["idea"] and decl["human_verification"] == "checked"


def test_skill_warning_command(capsys):
    assert gs.main(["warning"]) == 0
    out = capsys.readouterr().out
    assert pii.DATA_WARNING_TH in out and pii.DATA_WARNING_EN in out


# ------------------------------------------------------------ output section 4.7

def test_output_section_4_7_is_a_labelled_appendix():
    out = (DEMO / "NRIIS_SUBMISSION.md").read_text(encoding="utf-8")
    body, appendix = out.split("### 4.7 AI Use Declaration (GrantThai appendix, not an NRIIS field)", 1)
    assert "AI Use Declaration" not in body.split("## 3. Machine field metadata")[0].split("## 2.")[1]
    assert "NEEDS_VERIFICATION" in appendix.split("\n\n")[1]
    assert "GrantThai convention level: 2. This is GrantThai's own convention" in appendix
    assert "NOT CONFIRMED (NEEDS_INPUT)" in appendix
    fm = yaml.safe_load(out.split("---\n")[1])
    assert fm["authoring"]["ai_use_declaration"] == "unconfirmed"


def test_demo_shows_AI001_as_review_only():
    rep = api.validate(DEMO / "project.yaml", as_of=AS_OF)
    assert set(_ids(rep, "REVIEW")) == {"FW001", "AI001"}
    assert not AI_RULES & set(_ids(rep, "BLOCK"))


def test_confirmed_declaration_renders_confirmed(tmp_path):
    doc = P.load(EXAMPLE)
    P.set_field(doc, "CORE.GENERAL.TITLE_EN", "A title", actor="ai_assisted", tool="tool-x", tool_version="1.0")
    doc["authoring"]["ai_use_declaration"] = dict(_full_declaration(), confirmed_by="PI", confirmed_on="2026-09-25")
    P.save(doc, tmp_path / "project.yaml")
    out = api.build(tmp_path / "project.yaml", as_of=AS_OF).read_text(encoding="utf-8")
    assert "confirmed by the researcher (declaration_confirmed_by_human: true; by PI, on 2026-09-25)" in out
    assert "Still missing (rule AI001)" not in out


# ------------------------------------------------------------ policy documents

@pytest.mark.parametrize("doc", [POLICY_EN, POLICY_TH])
def test_policy_crosswalk_covers_every_guideline_row(doc):
    text = doc.read_text(encoding="utf-8")
    for n in range(1, 58):
        assert re.search(rf"^\| N{n:02d} \|", text, re.M), f"{doc.name}: N{n:02d}"
    for rid in sorted(AI_RULES):
        assert rid in text
    assert "OPEN" in text


def test_policy_quotes_are_short():
    """Third-party text is paraphrased; any Thai quotation is 15 words or fewer."""
    for doc in (POLICY_EN, POLICY_TH):
        for q in re.findall(r"“([^”]+)”", doc.read_text(encoding="utf-8")):
            if re.search(r"[฀-๿]", q):
                assert len(q.split()) <= 15 and len(q) <= 90, q
