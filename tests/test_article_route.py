"""v0.3 router, work package R4: the academic-article and concept-note routes.

AT-R2  examples/article-fictional builds exactly one build/ACADEMIC_ARTICLE.md
       with the NOTICE constant on body line 1 (and the route notice on line
       2), BLOCK = 0, exactly the seeded ART findings, deterministic across
       two runs.
AT-R3  one work object (examples/both-routes-fictional) builds
       NRIIS_SUBMISSION.md and ACADEMIC_ARTICLE.md in two invocations; each
       invocation creates one file and leaves the other byte-identical;
       shared-core values print identically in both; editing `routing` does
       not change content_sha256.
Plus one negative fixture per ART rule (tests/fixtures/negative/ART0nn/,
work.yaml + expected.json): the rule fires on the academic-article route,
with its catalog severity, and no other ART rule fires.
"""
import copy
import json
import re
import shutil
from pathlib import Path

import pytest
import yaml

from grantthai import api_py as api
from grantthai.cli import main
from grantthai.core import project as P
from grantthai.core.object_hash import content_sha256
from grantthai.render import article as A
from grantthai.render import submission as S
from grantthai.validators import engine as E

ROOT = Path(__file__).resolve().parents[1]
AS_OF = "2026-09-25"
ARTICLE_EX = ROOT / "examples/article-fictional/work.yaml"
BOTH_EX = ROOT / "examples/both-routes-fictional/work.yaml"
NEG = ROOT / "tests/fixtures/negative"
SEEDED = {"ART002", "ART006", "ART010"}
ART_DIRS = sorted(d for d in NEG.glob("ART0*") if (d / "work.yaml").is_file())


def _frontmatter_and_body(text: str):
    assert text.startswith("---\n")
    fm, body = text[4:].split("\n---\n", 1)
    return yaml.safe_load(fm), body.split("\n")


# ------------------------------------------------------------------ AT-R2 --

def test_at_r2_article_example_builds_one_file_notice_first_block_zero(tmp_path):
    shutil.copy(ARTICLE_EX, tmp_path / "work.yaml")
    out = api.build(tmp_path, as_of=AS_OF)                     # default_route: academic-article
    assert out == tmp_path / "build" / "ACADEMIC_ARTICLE.md"
    assert sorted(p.name for p in (tmp_path / "build").iterdir()) == ["ACADEMIC_ARTICLE.md"]
    text = out.read_text(encoding="utf-8")
    fm, body = _frontmatter_and_body(text)
    assert body[0] == P.notice_constant()
    route_notice = yaml.safe_load((ROOT / "routes/academic-article/route.yaml").read_text())["route_notice_en"]
    assert body[1] == route_notice and "not affiliated with any journal" in body[1]
    assert fm["route"] == "academic-article" and fm["manuscript_ready"] is True
    assert fm["validation_summary"]["block"] == 0
    assert fm["disclaimer"] == P.notice_constant()
    assert "submittable" not in fm and "fund_profile" not in fm
    rep = api.validate(tmp_path / "work.yaml", as_of=AS_OF, route="academic-article")
    art = {f["rule_id"] for f in rep["findings"] if f["rule_id"].startswith("ART")}
    assert art == SEEDED
    assert all(f["severity"] == "REVIEW" for f in rep["findings"] if f["rule_id"] in SEEDED)
    for rid in SEEDED:
        assert f"**{rid}**" in text


def test_at_r2_deterministic_across_two_runs_and_surfaces(tmp_path):
    a = api.build(ARTICLE_EX, route="academic-article", out_dir=tmp_path / "a", as_of=AS_OF).read_bytes()
    b = api.build(ARTICLE_EX, route="academic-article", out_dir=tmp_path / "b", as_of=AS_OF).read_bytes()
    assert a == b
    for name, argv in {"build": ["build", str(ARTICLE_EX)],
                       "route-build": ["route", "build", "--route", "academic-article", str(ARTICLE_EX)]}.items():
        out = tmp_path / name
        assert main(argv + ["--out", str(out), "--as-of", AS_OF]) == 0
        assert sorted(p.name for p in out.iterdir()) == ["ACADEMIC_ARTICLE.md"]
        assert (out / "ACADEMIC_ARTICLE.md").read_bytes() == a
    assert not re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}", a.decode("utf-8"))   # no timestamps


def test_article_output_copies_titles_and_marks_unsourced_venue_items(tmp_path):
    text = api.build(ARTICLE_EX, out_dir=tmp_path, as_of=AS_OF).read_text(encoding="utf-8")
    assert "COPIED_FROM: `CORE.GENERAL.TITLE_EN`" in text and "COPIED_FROM: `CORE.GENERAL.TITLE_TH`" in text
    assert "NEEDS_VERIFICATION (no source supplied)" in text
    assert "## 5. Advisories" not in text                        # no advisory fields filled
    assert "### 4.8 Core Epistemic Structure" in text
    # an AI tool is named only in the declaration and the role block, never as an author
    authors = text.split("#### 5. Authors", 1)[1].split("####", 1)[0]
    assert "text-editing assistant" not in authors


def test_article_sub_profile_changes_the_checked_languages():
    raw = P.load(ARTICLE_EX)
    intl = E.run(raw, None, AS_OF, route="academic-article")
    thai = E.run(raw, None, AS_OF, route="academic-article", sub_profile="thai-journal")
    assert intl.sub_profile == "international-journal" and thai.sub_profile == "thai-journal"
    assert "ART001" not in {f.rule_id for f in intl.findings}
    assert {f.field_ids[0] for f in thai.findings if f.rule_id == "ART001"} == {"ARTICLE.FRONT.ABSTRACT_TH"}
    unknown = E.run(raw, None, AS_OF, route="academic-article", sub_profile="no-such-profile")
    assert any(f.rule_id == "SCHEMA" and f.severity == "BLOCK" and "no-such-profile" in f.message_en
               for f in unknown.findings)


# ------------------------------------------------------------------ AT-R3 --

def test_at_r3_two_routes_one_object_each_build_touches_one_file(tmp_path):
    shutil.copy(BOTH_EX, tmp_path / "work.yaml")
    build = tmp_path / "build"
    n1 = api.build(tmp_path, as_of=AS_OF)                                   # default_route nriis-proposal
    assert n1.name == "NRIIS_SUBMISSION.md"
    assert sorted(p.name for p in build.iterdir()) == ["NRIIS_SUBMISSION.md"]
    nriis_bytes = n1.read_bytes()
    a1 = api.build(tmp_path, route="academic-article", as_of=AS_OF)
    assert sorted(p.name for p in build.iterdir()) == ["ACADEMIC_ARTICLE.md", "NRIIS_SUBMISSION.md"]
    assert n1.read_bytes() == nriis_bytes                                   # untouched by the article build
    art_bytes = a1.read_bytes()
    n2 = api.build(tmp_path, route="nriis-proposal", as_of=AS_OF)
    assert n2.read_bytes() == nriis_bytes and a1.read_bytes() == art_bytes
    assert sorted(p.name for p in build.iterdir()) == ["ACADEMIC_ARTICLE.md", "NRIIS_SUBMISSION.md"]


def test_at_r3_shared_core_values_identical_in_both_outputs(tmp_path):
    raw = P.load(BOTH_EX)
    nriis = api.build(BOTH_EX, route="nriis-proposal", out_dir=tmp_path, as_of=AS_OF).read_text(encoding="utf-8")
    art = api.build(BOTH_EX, route="academic-article", out_dir=tmp_path, as_of=AS_OF).read_text(encoding="utf-8")
    reg = P.registry_by_id()
    res = E.run(raw, None, AS_OF)
    unresolved = {ref.target for ref, _ in res.link_report.unresolved}
    fmt = A.shared_formatter(reg, unresolved)
    shared = [(rec["field_id"], rec.get("value")) for rec, _ in P.iter_records(P.normalized(raw))
              if (reg.get(rec.get("field_id")) or {}).get("scope") == "shared" and rec.get("value") is not None]
    assert len(shared) >= 20
    for fid, value in shared:
        block = fmt(fid, value, False)
        assert block in nriis, fid
        assert block in art, fid
    # the NRIIS renderer's own blocks for its placed shared fields are the same strings
    ctx = S.build_context(raw, res)
    nriis_blocks = {f["field_id"]: f["value"] for t in ctx["tabs"] for f in t["fields"]}
    for fid, value in shared:
        if fid in nriis_blocks:
            assert nriis_blocks[fid] == fmt(fid, value, False), fid


def test_at_r3_routing_edits_do_not_change_content_sha256(tmp_path):
    raw = P.load(BOTH_EX)
    before = content_sha256(raw)
    edited = copy.deepcopy(raw)
    edited["routing"] = {"declared_routes": ["academic-article"], "default_route": "academic-article",
                         "sub_profiles": {"academic-article": "international-journal"}}
    assert content_sha256(edited) == before
    del edited["routing"]
    assert content_sha256(edited) == before
    edited["work_type"] = "academic_article"                   # work_type is authored content
    assert content_sha256(edited) != before
    # and the article output's work_content_sha256 is the same whatever the routing says
    P.save(raw, tmp_path / "a" / "work.yaml")
    r2 = copy.deepcopy(raw)
    r2["routing"]["default_route"] = "academic-article"
    P.save(r2, tmp_path / "b" / "work.yaml")
    fa = _frontmatter_and_body(api.build(tmp_path / "a", route="academic-article", as_of=AS_OF)
                               .read_text(encoding="utf-8"))[0]
    fb = _frontmatter_and_body(api.build(tmp_path / "b", as_of=AS_OF).read_text(encoding="utf-8"))[0]
    assert fa["work_content_sha256"] == fb["work_content_sha256"] == before


# ----------------------------------------------------------- concept note --

def test_concept_note_required_fields_are_checked_by_S001():
    doc = P.load(BOTH_EX)

    def drop(node):
        if isinstance(node, dict):
            for v in node.values():
                drop(v)
        elif isinstance(node, list):
            node[:] = [x for x in node if not (isinstance(x, dict) and x.get("field_id") == "CORE.RESEARCH.PROBLEM"
                                               and "value" in x)]
            for x in node:
                drop(x)
    drop(doc)
    rep = api.validate(doc, as_of=AS_OF, route="concept-note")
    s001 = [f for f in rep["findings"] if f["rule_id"] == "S001"]
    assert s001 and "CORE.RESEARCH.PROBLEM" in " ".join(" ".join(f.get("field_ids") or []) + f["message_en"]
                                                      for f in s001)


def test_concept_note_route_builds_one_file_and_always_holds(tmp_path):
    out = api.build(BOTH_EX, route="concept-note", out_dir=tmp_path, as_of=AS_OF)
    assert sorted(p.name for p in tmp_path.iterdir()) == ["RESEARCH_CONCEPT_NOTE.md"]
    fm, body = _frontmatter_and_body(out.read_text(encoding="utf-8"))
    assert body[0] == P.notice_constant()
    assert fm["submittable"] is False and fm["route"] == "concept-note"
    assert any("never submittable" in h for h in fm["hold_reasons"])
    rep = api.validate(BOTH_EX, as_of=AS_OF, route="concept-note")
    fams = {re.sub(r"[0-9]+$", "", f["rule_id"]) for f in rep["findings"]}
    assert not fams & {"B", "F", "ELIG", "W", "T", "ART"}


# ------------------------------------------------------ negative fixtures --

def test_every_art_rule_has_a_fixture():
    catalog = {r["id"]: r for r in P.rules_catalog()["rules"] if r.get("family") == "ART"}
    assert {d.name for d in ART_DIRS} == set(catalog)
    for rid, rule in catalog.items():
        assert rule["negative_fixture"] == f"tests/fixtures/negative/{rid}/"


@pytest.mark.parametrize("d", ART_DIRS, ids=lambda d: d.name)
def test_art_negative_fixture_fires(d):
    exp = json.loads((d / "expected.json").read_text(encoding="utf-8"))
    assert exp["rule_id"] == d.name
    rep = api.validate(d / "work.yaml", as_of=exp["as_of"], route=exp["route"])
    hits = [f for f in rep["findings"] if f["rule_id"] == d.name]
    assert hits, f"{d.name} did not fire"
    assert all(f["severity"] == exp["must_fire_severity"] for f in hits)
    others = {f["rule_id"] for f in rep["findings"] if f["rule_id"].startswith("ART")} - {d.name}
    assert not others, others
    assert rep["summary"]["block"] == (len(hits) if exp["must_fire_severity"] == "BLOCK" else 0)


ART_VARIANT_DIRS = sorted(d for d in NEG.glob("ART0*/*") if (d / "work.yaml").is_file())


@pytest.mark.parametrize("d", ART_VARIANT_DIRS, ids=lambda d: f"{d.parent.name}/{d.name}")
def test_art_negative_fixture_variants_fire(d):
    """Extra cases of one rule (e.g. ART007 partial_name, undisclosed)."""
    exp = json.loads((d / "expected.json").read_text(encoding="utf-8"))
    assert exp["rule_id"] == d.parent.name
    rep = api.validate(d / "work.yaml", as_of=exp["as_of"], route=exp["route"])
    hits = [f for f in rep["findings"] if f["rule_id"] == exp["rule_id"]]
    assert hits and all(f["severity"] == exp["must_fire_severity"] for f in hits), d
    others = {f["rule_id"] for f in rep["findings"] if f["rule_id"].startswith("ART")} - {exp["rule_id"]}
    assert not others, others


def test_art007_variants_exist():
    assert {d.name for d in ART_VARIANT_DIRS if d.parent.name == "ART007"} >= {"partial_name", "undisclosed"}


def test_art007_generic_pattern_spares_person_names_and_organizations():
    from grantthai.validators import article as ART
    for name in ("Ai Nakamura", "FICTIONAL Lecturer A", "Kaiwan Srisai", "Aiyana Brown"):
        assert not ART._generic_ai_name(name), name
    for name in ("FICTIONAL ChatBot", "FICTIONAL-GPT", "FICTIONAL AI assistant", "a large language model", "ปัญญาประดิษฐ์"):
        assert ART._generic_ai_name(name), name
    assert ART._names_tool("Tool X", "Tool X (model Y)") and ART._names_tool("Tool X (v2)", "Tool X")
    assert not ART._names_tool("FICTIONAL Lecturer A", "FICTIONAL text-editing assistant")


def test_art_rules_do_not_run_on_the_nriis_route():
    rep = api.validate(ART_DIRS[0] / "work.yaml", as_of=AS_OF, route="nriis-proposal")
    assert not [f for f in rep["findings"] if f["rule_id"].startswith("ART")]
