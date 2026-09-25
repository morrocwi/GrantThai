"""tests/test_engine.py — v0.1 engine: project.yaml -> exactly one
build/NRIIS_SUBMISSION.md. End-to-end on the FICTIONAL worked example,
determinism, negative cases, and the hard ceiling on AI drafts."""
import copy
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from grantthai import api_py as api  # noqa: E402
from grantthai.core import project as P  # noqa: E402
from grantthai.validators import engine as E  # noqa: E402

EXAMPLE = ROOT / "examples/lecturer-no-ai/project.yaml"
AS_OF = "2026-09-25"
NOTICE = (ROOT / "spec/output/notice_constant.txt").read_text(encoding="utf-8").rstrip("\n")


def _copy_example(tmp_path, mutate=None):
    doc = P.load(EXAMPLE)
    if mutate:
        mutate(doc)
    path = tmp_path / "project.yaml"
    P.save(doc, path)
    return path


def _rules(report, sev=None):
    return [f["rule_id"] for f in report["findings"] if sev is None or f["severity"] == sev]


def _body(text):
    return text.split("\n---\n", 1)[1]


# ---------------------------------------------------------------- e2e ----

def test_e2e_example_builds_exactly_one_file_block_zero(tmp_path):
    shutil.copy(EXAMPLE, tmp_path / "project.yaml")
    out = api.build(tmp_path / "project.yaml", as_of=AS_OF)
    assert out == tmp_path / "build" / "NRIIS_SUBMISSION.md"
    assert sorted(p.name for p in (tmp_path / "build").iterdir()) == ["NRIIS_SUBMISSION.md"]
    text = out.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    assert _body(text).lstrip("\n").split("\n", 1)[0] == NOTICE          # NOTICE is body line 1
    assert "validation_summary:\n  block: 0\n" in text
    assert "submittable: true" in text and "real_world_verified: false" in text
    body = _body(text)
    assert body.index("## 1. Readiness summary") < body.index("## 2. Copy/paste fields by NRIIS tab") \
        < body.index("## 3. Machine field metadata") < body.index("## 4. Validation and provenance appendix")
    # tabs in the observed order, every registry NRIIS field rendered once
    tabs = [ln for ln in body.splitlines() if ln.startswith("### Tab ")]
    assert [t.split(": ")[1].split(" ")[0] for t in tabs] == P.tab_mapping()["tab_order"]
    for n in P.nriis_fields():
        assert body.count(f"(NRIIS map: `{n['field_id']}`)") == 1
    assert "LABEL_TH: NEEDS_VERIFICATION" in body
    # ORIGIN is the registry origin (core/02 §2), never a provenance class
    assert "- ORIGIN: NRIIS_NATIVE\n" in body and "- ORIGIN: provenance_class" not in body
    assert "- RENDER_FROM: METHOD.PLAN.DESIGN" in body
    # the methodology is one NRIIS box; its structured records sit in the appendix
    sec2 = body[body.index("## 2. Copy/paste"):body.index("## 3. Machine field metadata")]
    assert "`METHOD.PLAN." not in sec2 and sec2.count("FIELD_ID: `CORE.NARRATIVE.METHOD`") == 1
    appendix = body[body.index("### 4.5 Project records not placed on any NRIIS tab"):]
    assert "`METHOD.PLAN.DESIGN` (ORIGIN: AUTHORING_CORE" in appendix
    assert "ARITHMETIC CHECK: sum(weight_percent) = 100.00 (must be 100.00): OK" in body


def test_report_matches_schema_and_accounts_for_every_rule():
    rep = api.validate(EXAMPLE, as_of=AS_OF)
    assert P.schema_errors(rep, P.REPORT_SCHEMA_ID) == []
    assert rep["summary"]["block"] == 0
    # v0.2: the only REVIEW findings on the (deliberately terse) example are
    # writing-length guidance (W101/W102), never a structural or logic finding.
    assert {f["rule_id"] for f in rep["findings"] if f["severity"] == "REVIEW"} <= {"W101", "W102"}
    catalog = [r["id"] for r in P.rules_catalog()["rules"]]
    not_eval = set(_rules(rep, "INFO"))
    for rid in catalog:
        rule = P.rules_catalog()["rules"][catalog.index(rid)]
        evaluated = ((rule["ships"] == "v0.1" and rid not in E.V01_NOT_EVALUATED)
                     or rid in E.EVALUATED_AFTER_V01)
        assert evaluated != (rid in not_eval), rid       # evaluated XOR reported as not evaluated


def test_determinism_byte_identical(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    for d in (a, b):
        d.mkdir()
        shutil.copy(EXAMPLE, d / "project.yaml")
    out_a = api.build(a / "project.yaml", as_of=AS_OF).read_bytes()
    out_b = api.build(b / "project.yaml", as_of=AS_OF).read_bytes()
    assert out_a == out_b
    assert api.build(a / "project.yaml", as_of=AS_OF).read_bytes() == out_a


def test_cli_build_and_validate(tmp_path):
    shutil.copy(EXAMPLE, tmp_path / "project.yaml")
    env = dict(os.environ, PYTHONPATH=str(ROOT / "src"))
    r = subprocess.run([sys.executable, "-m", "grantthai", "validate", str(tmp_path / "project.yaml"),
                        "--as-of", AS_OF], capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stderr
    assert "BLOCK 0" in r.stdout
    r = subprocess.run([sys.executable, "-m", "grantthai", "build", str(tmp_path / "project.yaml"),
                        "--as-of", AS_OF], capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stderr
    assert [p.name for p in (tmp_path / "build").iterdir()] == ["NRIIS_SUBMISSION.md"]
    r = subprocess.run([sys.executable, "-m", "grantthai", "explain", "B002"], capture_output=True, text=True, env=env)
    assert r.returncode == 0 and '"implemented_in_v0_1": true' in r.stdout


def test_new_project_set_field_roundtrip(tmp_path):
    path = tmp_path / "project.yaml"
    api.new_project("T-0001", path=path)
    with pytest.raises(FileExistsError):
        api.new_project("T-0001", path=path)
    assert P.schema_errors(P.load(path), P.PROJECT_SCHEMA_ID) == []
    rec = api.set_field(path, "CORE.GENERAL.TITLE_EN", "My own title")
    assert rec["status"] == "DRAFT" and rec["provenance"]["authored_by"] == "human"
    rep = api.validate(path, as_of=AS_OF)
    assert "CORE.GENERAL.TITLE_EN" not in {fid for f in rep["findings"] if f["rule_id"] == "S001"
                                           for fid in f.get("field_ids", [])}
    assert "S001" in _rules(rep, "BLOCK")                  # the rest is still NEEDS_INPUT
    out = api.build(path, as_of=AS_OF)                     # a BLOCK never stops build
    assert "NEEDS_INPUT" in out.read_text(encoding="utf-8")
    assert [f["field_id"] for f in api.list_fields(tab="ATTACHMENTS")]


# ---------------------------------------------------------- negatives ----

def test_negative_budget_arithmetic_B002(tmp_path):
    def mutate(doc):
        P.records_by_id(doc)["BUDGET.PLAN.ITEMS"]["value"][0]["line_total"] = 36001
    path = _copy_example(tmp_path, mutate)
    rep = api.validate(path, as_of=AS_OF)
    assert "B002" in _rules(rep, "BLOCK")
    text = api.build(path, as_of=AS_OF).read_text(encoding="utf-8")
    assert "submittable: false" in text and "MISMATCH" in text and "**B002**" in text


def test_negative_missing_required_S001(tmp_path):
    def mutate(doc):
        doc["fields"] = [r for r in doc["fields"] if r["field_id"] != "CORE.GENERAL.TITLE_EN"]
    path = _copy_example(tmp_path, mutate)
    rep = api.validate(path, as_of=AS_OF)
    assert any(f["rule_id"] == "S001" and f["field_ids"] == ["CORE.GENERAL.TITLE_EN"] for f in rep["findings"])
    text = api.build(path, as_of=AS_OF).read_text(encoding="utf-8")
    assert "- `CORE.GENERAL.TITLE_EN`: NEEDS_INPUT." in text


def test_negative_cycle_and_unresolved_reference_CH001_S006(tmp_path):
    def mutate(doc):
        acts = P.records_by_id(doc)["WORK.PLAN.ACTIVITIES"]["value"]
        acts[0]["depends_on_activity_ids"] = ["ACT3"]
        acts[1]["objective_ids"].append("OBJ9")
    path = _copy_example(tmp_path, mutate)
    rep = api.validate(path, as_of=AS_OF)
    assert {"CH001", "S006"} <= set(_rules(rep, "BLOCK"))
    text = api.build(path, as_of=AS_OF).read_text(encoding="utf-8")
    assert "OBJ9 UNRESOLVED" in text


def test_negative_schema_violation(tmp_path):
    path = _copy_example(tmp_path, lambda d: d.update(mode="robot"))
    assert "SCHEMA" in _rules(api.validate(path, as_of=AS_OF), "BLOCK")


def test_stale_fund_rules_by_as_of():
    rep = api.validate(EXAMPLE, as_of="2100-01-01")
    assert "F002" in _rules(rep, "REVIEW")


# -------------------------------------------------------- hard ceiling ---

def test_ai_draft_is_never_source_and_never_above_draft():
    doc = P.load(EXAMPLE)
    with pytest.raises(ValueError):
        P.set_field(doc, "CORE.RESEARCH.PROBLEM", "AI text", actor="ai_assisted",
                    provenance={"provenance_class": "SOURCE"})
    rec = P.set_field(copy.deepcopy(doc), "CORE.GENERAL.TITLE_EN", "AI text", actor="ai_assisted", tool="some-tool")
    assert rec["status"] == "DRAFT"
    assert rec["provenance"]["authored_by"] == "ai_draft"
    assert rec["provenance"]["provenance_class"] == "INFERENCE"
    doc2 = copy.deepcopy(doc)
    P.set_field(doc2, "CORE.GENERAL.TITLE_EN", "AI text", actor="ai_assisted", tool="some-tool")
    assert doc2["authoring"]["mode"] == "ai_assisted" and doc2["authoring"]["tools_disclosed"] == ["some-tool"]
    with pytest.raises(ValueError):
        P.set_field(doc2, "CORE.GENERAL.TITLE_EN", "x", provenance={"authored_by": "ai_draft"})
    text, _ = __import__("grantthai.render.submission", fromlist=["render"]).render(doc2, EXAMPLE.parent, AS_OF)
    assert "- `CORE.GENERAL.TITLE_EN`: authored_by is `ai_draft`" in text
    assert "ai_assisted" in text


def test_needs_verification_value_becomes_marker():
    doc = P.load(EXAMPLE)
    rec = P.set_field(doc, "CORE.GENERAL.TITLE_EN", "NEEDS_VERIFICATION")
    assert rec["value"] is None and rec["status"] == "NEEDS_INPUT" and "NEEDS_VERIFICATION" in rec["markers"]


def test_hand_written_ai_draft_as_source_is_blocked_X003(tmp_path):
    """A project.yaml written by hand or by a chat AI skips set_field, so the
    validator itself must catch an AI draft marked SOURCE."""
    def mutate(doc):
        rec = doc["fields"][0]
        rec["provenance"] = dict(rec["provenance"], provenance_class="SOURCE", authored_by="ai_draft")
    path = _copy_example(tmp_path, mutate)
    assert "X003" in _rules(api.validate(path, as_of=AS_OF), "BLOCK")
    assert "X003" not in _rules(api.validate(EXAMPLE, as_of=AS_OF))


def test_hand_written_status_above_draft_is_flagged_in_output(tmp_path):
    def mutate(doc):
        doc["fields"][0]["status"] = "VERIFIED"
    path = _copy_example(tmp_path, mutate)
    text = api.build(path, as_of=AS_OF).read_text(encoding="utf-8")
    assert "STATUS: VERIFIED (basis: self-declared in project.yaml and NOT backed by any check" in text


def test_worksheet_never_advises_relabelling_adopted_ai_text_as_human():
    """Section 1.5: an unadopted ai_draft may be rewritten and set to human;
    an adopted human_ai_assisted value is only confirmed, never relabelled."""
    doc = P.load(EXAMPLE)
    P.set_field(doc, "CORE.GENERAL.TITLE_EN", "AI text", actor="ai_assisted", tool="some-tool")
    for rec, _ in P.iter_records(doc):
        if rec.get("field_id") == "CORE.GENERAL.TITLE_EN":
            rec["provenance"]["authored_by"] = "human_ai_assisted"
    text, _ = __import__("grantthai.render.submission", fromlist=["render"]).render(doc, EXAMPLE.parent, AS_OF)
    line = next(ln for ln in text.splitlines() if ln.startswith("- `CORE.GENERAL.TITLE_EN`: authored_by"))
    assert "`human_ai_assisted`" in line
    assert "set authored_by to human" not in line
    assert "keep authored_by as human_ai_assisted" in line
