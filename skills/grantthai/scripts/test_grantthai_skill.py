# SPDX-FileCopyrightText: 2026 Yaoharee Lahtee and ARAYA NIKAH SOCIAL ENTERPRISE CO.
# SPDX-License-Identifier: Apache-2.0
"""Tests for the GrantThai agent skill (skills/grantthai).

Run from the repository root with `pytest -q`. They check that the skill's
helper reproduces the FICTIONAL worked example through the public Python
API, keeps the AI-draft ceiling, explains every v0.1 rule in Thai, and
that SKILL.md is a loadable agent skill."""
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

SKILL = Path(__file__).resolve().parents[1]
ROOT = SKILL.parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(SKILL / "scripts"))

import grantthai_skill as gs  # noqa: E402
from grantthai import api_py as api  # noqa: E402

EXAMPLE = ROOT / "examples/lecturer-no-ai/project.yaml"
AS_OF = "2026-09-25"


def _answers_from_example() -> dict:
    doc = yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))
    answers = []
    recs = [(r, None) for r in doc["fields"]]
    recs += [(r, node) for node, rs in doc["chain"].items() for r in rs]
    for rec, node in recs:
        prov = rec["provenance"]
        a = {"field_id": rec["field_id"], "value": rec["value"], "by": "researcher",
             "provenance_class": prov["provenance_class"], "source_type": prov["source_type"],
             "evidence_role": prov["evidence_role"]}
        for k in ("source_ids", "links", "supports_claim_id", "claim_strength_cap"):
            if k in rec:
                a[k] = rec[k]
        if node:
            a["chain_node"] = node
        answers.append(a)
    return {"project": {"project_id": doc["project_id"],
                        "fund_profile_id": doc["fund_binding"]["fund_profile_id"]},
            "sources": doc["sources"], "answers": answers}


def test_skill_md_frontmatter():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert m, "SKILL.md must start with YAML frontmatter"
    fm = yaml.safe_load(m.group(1))
    assert fm["name"] == "grantthai"
    assert 50 < len(fm["description"]) <= 1024
    for ref in re.findall(r"`((?:reference|scripts)/[^` ]+)", text):
        assert (SKILL / ref).exists(), f"SKILL.md points to a missing file: {ref}"


def test_every_rule_has_a_thai_explanation():
    th = gs.load_rules_th()
    rules = yaml.safe_load((ROOT / "validators/rules.yaml").read_text(encoding="utf-8"))["rules"]
    v01 = {r["id"] for r in rules if r.get("ships") == "v0.1"}
    missing = sorted((v01 | {"SCHEMA"}) - set(th))
    assert not missing, f"no Thai explanation for {missing}"
    assert all(th[k].strip() for k in th)


def test_apply_reproduces_the_worked_example(tmp_path):
    answers = tmp_path / "answers.yaml"
    answers.write_text(yaml.safe_dump(_answers_from_example(), allow_unicode=True, sort_keys=False),
                       encoding="utf-8")
    project = tmp_path / "project.yaml"
    r = subprocess.run([sys.executable, str(SKILL / "scripts/grantthai_skill.py"), "apply",
                        str(answers), "--project", str(project), "--init"],
                       capture_output=True, text=True, cwd=tmp_path)
    assert r.returncode == 0, r.stderr
    rep = api.validate(project, as_of=AS_OF)
    assert rep["summary"]["block"] == 0, [f for f in rep["findings"] if f["severity"] == "BLOCK"]

    # Applying the same answers twice changes nothing (one record per field).
    before = project.read_bytes()
    gs.apply_answers(api, project, yaml.safe_load(answers.read_text(encoding="utf-8")))
    assert project.read_bytes() == before

    r = subprocess.run([sys.executable, str(SKILL / "scripts/grantthai_skill.py"), "report",
                        "--project", str(project), "--as-of", AS_OF],
                       capture_output=True, text=True, cwd=tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    outs = list((tmp_path / "build").iterdir())
    assert [p.name for p in outs] == ["NRIIS_SUBMISSION.md"]
    assert "NRIIS_SUBMISSION.md" in r.stdout


def test_ai_drafts_stay_drafts_and_never_source(tmp_path):
    project = tmp_path / "project.yaml"
    api.new_project(path=project)
    doc = {"tool": "EXAMPLE TOOL", "answers": [
        {"field_id": "CORE.GENERAL.TITLE_EN", "value": "An AI translation", "by": "ai"},
        {"field_id": "CORE.GENERAL.RESEARCH_ISSUE", "value": "NEEDS_VERIFICATION"},
    ]}
    gs.apply_answers(api, project, doc)
    p = api.load(project)
    recs = {r["field_id"]: r for r in p["fields"]}
    t = recs["CORE.GENERAL.TITLE_EN"]
    assert t["status"] == "DRAFT"
    assert t["provenance"]["authored_by"] == "ai_draft"
    assert t["provenance"]["provenance_class"] == "INFERENCE"
    assert p["authoring"]["mode"] == "ai_assisted"
    assert "EXAMPLE TOOL" in p["authoring"]["tools_disclosed"]
    ri = recs["CORE.GENERAL.RESEARCH_ISSUE"]
    assert ri["value"] is None and "NEEDS_VERIFICATION" in ri["markers"]

    with pytest.raises(ValueError, match="SOURCE"):
        gs.apply_answers(api, project, {"answers": [
            {"field_id": "CORE.RESEARCH.PROBLEM", "value": "x", "by": "ai", "provenance_class": "SOURCE"}]})
    with pytest.raises(ValueError, match="unknown keys"):
        gs.apply_answers(api, project, {"answers": [
            {"field_id": "CORE.GENERAL.TITLE_TH", "value": "x", "status": "VERIFIED"}]})
    with pytest.raises(ValueError, match="never a source"):
        gs.apply_answers(api, project, {"sources": [
            {"source_id": "SRC-1", "kind": "AI_TRANSLATION_PROPOSAL", "citation": "x"}]})

    r = gs.report(api, project, as_of=AS_OF)
    assert "CORE.GENERAL.TITLE_EN" in r["ai_drafts_to_confirm"]
    assert r["summary"]["block"] > 0
    assert all(f["explain_th"] for f in r["findings"])


def test_researcher_edited_ai_draft(tmp_path):
    project = tmp_path / "project.yaml"
    api.new_project(path=project)
    gs.apply_answers(api, project, {"tool": "EXAMPLE TOOL", "answers": [
        {"field_id": "CORE.GENERAL.TITLE_EN", "value": "Adopted wording", "by": "researcher_edited_ai_draft"}]})
    p = api.load(project)
    rec = next(r for r in p["fields"] if r["field_id"] == "CORE.GENERAL.TITLE_EN")
    assert rec["status"] == "DRAFT"
    assert rec["provenance"]["authored_by"] == "human_ai_assisted"
    assert p["authoring"]["mode"] == "ai_assisted"
    rep = api.validate(project, as_of=AS_OF)
    assert "SCHEMA" not in {f["rule_id"] for f in rep["findings"]}
