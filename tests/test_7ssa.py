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


# ================================================================== S2 ====
# AT-7SSA-1: the fictional conceptual example builds exactly one
#   ACADEMIC_ARTICLE.md with all seven [S#] markers, NOTICE on line 1,
#   BLOCK 0, no 7SSA finding, byte-identical across two runs.
# AT-7SSA-2: the same object renders as thai-7 / thai-5 / thai-4 with the
#   source's headings, all seven markers, byte-identical reruns, the same
#   content_sha256 and the same multiset of researcher strings.
# AT-7SSA-3: --format tex writes exactly one .tex from the sha256-pinned
#   template (212 fill rows = 212 tokens); it compiles with latexmk when
#   latexmk is installed, else the test is skipped with that reason.

from grantthai.render import ssa as SSA  # noqa: E402
from grantthai.render import article_tex as TEX  # noqa: E402

MARKERS_EN = [f"###### [S{n}] " for n in range(1, 8)]


def _fm_body(text):
    fm, body = text[4:].split("\n---\n", 1)
    return yaml.safe_load(fm), body.split("\n")


def test_at_7ssa_1_example_builds_one_file_with_seven_sectors(tmp_path):
    shutil.copy(EXAMPLE, tmp_path / "work.yaml")
    out = api.build(tmp_path, as_of=AS_OF)
    assert out == tmp_path / "build" / "ACADEMIC_ARTICLE.md"
    assert sorted(p.name for p in (tmp_path / "build").iterdir()) == ["ACADEMIC_ARTICLE.md"]
    text = out.read_text(encoding="utf-8")
    fm, body = _fm_body(text)
    assert body[0] == P.notice_constant()
    assert fm["structure_profile"] == "7ssa-world" and fm["structure_profile_renderer"] == SSA.RENDERER_VERSION
    assert fm["validation_summary"]["block"] == 0 and fm["manuscript_ready"] is True
    for n in range(1, 8):
        assert text.count(f"###### [S{n}] ") == 1, n
    assert "##### 4. Conceptual Problem" in text                    # the conceptual overlay heading (§15.1)
    assert "### 9. 7SSA manuscript body: `7ssa-world`" in text
    assert "#### Article audit table (7SSA v1 §31)" in text and "no (NEEDS_INPUT)" not in text
    assert not [ln for ln in body if ln.startswith("- **7SSA-")]    # no 7SSA finding seeded
    again = api.build(EXAMPLE, out_dir=tmp_path / "again", as_of=AS_OF).read_bytes()
    assert again == out.read_bytes()


@pytest.mark.parametrize("pid", ["7ssa-thai-7", "7ssa-thai-5", "7ssa-thai-4"])
def test_at_7ssa_2_thai_layouts_are_deterministic_and_keep_every_sector(pid, tmp_path):
    a = api.build(EXAMPLE, out_dir=tmp_path / "a", as_of=AS_OF, structure_profile=pid).read_text(encoding="utf-8")
    b = api.build(EXAMPLE, out_dir=tmp_path / "b", as_of=AS_OF, structure_profile=pid).read_text(encoding="utf-8")
    assert a == b
    fm, _ = _fm_body(a)
    assert fm["structure_profile"] == pid
    assert fm["work_content_sha256"] == content_sha256(P.load(EXAMPLE))
    for i, h in enumerate(HEADINGS[pid], start=1):
        assert f"##### {i}. {h}\n" in a, h
    idx = ST.index(_route())
    for s in idx["sectors"]:
        assert a.count(f"###### [{s['id']}] {s['name_th']}\n") == 1, s["id"]


def test_at_7ssa_2_compression_preserves_the_multiset_of_researcher_strings():
    raw = P.load(EXAMPLE)
    recs = P.records_by_id(P.normalized(raw))
    rt = _route()

    def value(fid):
        return (recs.get(fid) or {}).get("value")

    items = value(ST.BODY_SECTIONS)
    blocks = SSA.sector_blocks(value, items, rt)
    want = SSA.researcher_strings(blocks)
    assert len(want) > 40
    for pid in PROFILES:
        prof = ST.load_profile(rt, pid)
        vis = SSA.compress(blocks, prof, ST.index(rt), article_type="conceptual")
        assert SSA.rendered_strings(vis, blocks["untagged"]) == want, pid
        assert [s["id"] for sec in vis for s in sec["sectors"]] == list(ST.SECTORS), pid
        assert vis == SSA.compress(blocks, prof, ST.index(rt), article_type="conceptual")   # pure, deterministic
    # and every string really is printed in each built file
    for pid in PROFILES:
        text, _ = api_render(raw, pid)
        for s in want:
            assert s in text, (pid, s[:40])


def api_render(raw, pid):
    from grantthai.render import render_route
    return render_route(raw, EXAMPLE.parent, route="academic-article", as_of=AS_OF, structure_profile=pid)


def test_property_compress_never_drops_or_duplicates_text():
    """Random sector contents (seeded, deterministic): for every profile the
    multiset of strings and the sector order are preserved; an empty sector
    is marked empty, never removed."""
    import random
    rng = random.Random(7)
    rt = _route()
    idx = ST.index(rt)
    words = ["alpha", "beta", "ข้อความ", "gamma | pipe", "", "delta\n\nparagraph", "S5 again"]
    for _ in range(60):
        blocks = {sid: [{"source": f"{ST.BODY_SECTIONS} MSC{rng.randint(1, 99)}", "label": rng.choice(words),
                         "slot": "", "text": rng.choice(words)} for _ in range(rng.randint(0, 3))]
                  for sid in ST.SECTORS}
        blocks["untagged"] = []
        want = SSA.researcher_strings(blocks)
        for pid in PROFILES:
            vis = SSA.compress(blocks, ST.load_profile(rt, pid), idx)
            assert SSA.rendered_strings(vis, []) == want
            for sec in vis:
                for s in sec["sectors"]:
                    assert s["empty"] == (not any(ST.filled(b["text"]) for b in blocks[s["id"]]))


def test_empty_sector_prints_needs_input_under_its_marker():
    raw = P.load(NEG / "7SSA-01/work.yaml")
    text, _ = api_render(raw, "7ssa-thai-4")
    sec = text.split("###### [S3] ", 1)[1].split("######", 1)[0]
    assert "NEEDS_INPUT (no researcher text for this sector yet)" in sec
    assert "| 2 | แนวคิดและกรอบการวิเคราะห์ | [S3] ฐานแนวคิดและองค์ความรู้เดิม | 0 |" in text


def test_plain_output_is_unchanged_without_a_profile(tmp_path):
    """No profile selected -> no 7SSA block, no frontmatter key; the 7SSA
    records section is hidden and a filled 7SSA record is listed, not dropped."""
    doc = P.load(EXAMPLE)
    doc["routing"].pop("structure_profiles")
    for r in doc["fields"]:
        if r["field_id"] == "ARTICLE.SSA.ARTICLE_TYPE":
            r["value"] = None
    text, _ = render_plain(doc)
    assert "7SSA manuscript body" not in text and "structure_profile" not in text.split("\n---\n", 1)[0]
    assert "### 4. 7SSA structure records" not in text
    assert "`ARTICLE.SSA.GAP` (ORIGIN: RECOMMENDED_EXTENSION" in text
    assert "section ssa_records is shown only when ARTICLE.SSA.ARTICLE_TYPE is set" in text


def render_plain(doc):
    from grantthai.render import render_route
    return render_route(doc, EXAMPLE.parent, route="academic-article", as_of=AS_OF)


def test_structure_profile_refused_on_a_route_without_profiles(tmp_path):
    with pytest.raises(ValueError, match="no structure profiles"):
        api.build(EXAMPLE, route="concept-note", out_dir=tmp_path, as_of=AS_OF, structure_profile="7ssa-world")
    assert not list(tmp_path.iterdir())


# ------------------------------------------------------------ tex export --

def _tex(tmp_path, **kw):
    out = api.build(EXAMPLE, out_dir=tmp_path, as_of=AS_OF, fmt="tex", **kw)
    assert sorted(p.name for p in tmp_path.iterdir()) == ["ACADEMIC_ARTICLE.tex"]
    return out, out.read_text(encoding="utf-8")


def test_at_7ssa_3_tex_export_writes_one_file_from_the_pinned_template(tmp_path):
    rt = _route()
    exp = rt.export("tex")
    text, fm = TEX.load_template(exp)
    src = yaml.safe_load((ROOT / exp["source"]).read_text(encoding="utf-8"))
    import hashlib
    assert hashlib.sha256((ROOT / exp["template"]).read_bytes()).hexdigest() == src["files"][0]["sha256"] \
        == fm["template_sha256"]
    assert len(fm["rows"]) == text.count("[FILL") == len(TEX.fill_tokens(text)) == fm["token_count"] == 212
    out, tex = _tex(tmp_path)
    assert out.name == "ACADEMIC_ARTICLE.tex"
    assert tex.startswith("% " + P.notice_constant().splitlines()[0])
    assert "[FILL" not in tex.replace(r"\newcommand{\Fill}{\texttt{[FILL]}}", "")
    assert "\\glosaauditfalse\n" in tex and "\\thaiarticlefalse\n" in tex
    # a visible draft/unofficial line right under the title (not only a comment)
    assert "\\maketitle\n" + TEX.DRAFT_MARKER_TEX + "\n" in tex and tex.count(TEX.DRAFT_MARKER) == 1
    assert "unofficial" in TEX.DRAFT_MARKER and "current instructions" in TEX.DRAFT_MARKER
    assert "\\section{Conceptual Problem}\n\\label{sec:s4}" in tex
    assert "pdfauthor={FICTIONAL Lecturer A}" in tex
    assert "CLASSIFICATION\\_GAP" in tex                               # escaped, literal
    assert "\\newcommand{\\PolicyCheckedDate}{[NEEDS\\_INPUT: Journal policy last checked" in tex
    policy = tex.split("\\label{app:policy-map}", 1)[1].split("\\bottomrule", 1)[0]
    assert " check " not in policy and "NEEDS\\_VERIFICATION" in policy
    for word in ("R1 & Leak", "R14 & Confidential"):
        row = next(ln for ln in tex.splitlines() if word in ln)
        assert "NEEDS\\_INPUT" in row, word                              # review state is never filled
    assert _tex(tmp_path / "again")[1] == tex                            # deterministic


def test_tex_export_keeps_audit_with_flag_and_marks_thai_layout(tmp_path):
    _, tex = _tex(tmp_path / "audit", glosa_audit=True)
    assert "\\glosaaudittrue\n" in tex
    _, tex = _tex(tmp_path / "thai", structure_profile="7ssa-thai-5")
    assert "Thai-journal layout 7ssa-thai-5 selected" in tex and "XeLaTeX" in tex
    # Thai script appears only in LaTeX comments (the template's own Thai-renderer notes and the NOTICE)
    assert all(ln.lstrip().startswith("%") for ln in tex.splitlines() if TEX.THAI_RE.search(ln))


def test_tex_export_prints_needs_input_for_thai_values(tmp_path):
    doc = P.load(EXAMPLE)
    for r in doc["fields"]:
        if r["field_id"] == "ARTICLE.META.TITLE_EN":
            r["value"] = "ชื่อเรื่องภาษาไทย"
    P.save(doc, tmp_path / "work.yaml")
    tex = api.build(tmp_path, as_of=AS_OF, fmt="tex").read_text(encoding="utf-8")
    title = tex.split("\\title{\\textbf{", 1)[1].split("}", 1)[0]
    assert title.startswith("[NEEDS\\_INPUT: Manuscript title; the value is Thai text")


def test_tex_export_needs_a_selected_profile_and_refuses_a_tampered_template(tmp_path, monkeypatch):
    doc = P.load(EXAMPLE)
    doc["routing"].pop("structure_profiles")
    P.save(doc, tmp_path / "w" / "work.yaml")
    with pytest.raises(ValueError, match="needs a 7ssa structure profile"):
        api.build(tmp_path / "w", as_of=AS_OF, fmt="tex")
    assert not (tmp_path / "w" / "build").exists()
    with pytest.raises(ValueError, match="no --format tex export"):
        api.build(EXAMPLE, route="concept-note", out_dir=tmp_path / "c", as_of=AS_OF, fmt="tex")
    bad = copy.deepcopy(_route().export("tex"))
    bad["source"] = "templates/tex/SOURCE.yaml"
    real = (ROOT / bad["template"]).read_bytes()
    monkeypatch.setattr(TEX.P, "DATA_ROOT", tmp_path / "root")
    for d in ("templates/tex", "registry", "spec"):
        (tmp_path / "root" / d).mkdir(parents=True)
    for rel in (bad["source"], bad["fillmap"]):
        shutil.copy(ROOT / rel, tmp_path / "root" / rel)
    (tmp_path / "root" / bad["template"]).write_bytes(real.replace(b"Introduction", b"Intro"))
    with pytest.raises(ValueError, match="does not match its pinned sha256"):
        TEX.load_template(bad)


@pytest.mark.skipif(shutil.which("latexmk") is None or shutil.which("pdflatex") is None,
                    reason="requires_tex: latexmk/pdflatex is not installed, so AT-7SSA-3 cannot compile the "
                           "export here (the one-file and fill checks above still ran)")
def test_at_7ssa_3_tex_export_compiles(tmp_path):
    out, _ = _tex(tmp_path)
    r = subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", out.name],
                       cwd=tmp_path, capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, r.stdout[-3000:]
    assert (tmp_path / "ACADEMIC_ARTICLE.pdf").stat().st_size > 10_000


def test_cli_build_format_tex_and_structure_profile(tmp_path):
    assert main(["build", str(EXAMPLE), "--format", "tex", "--out", str(tmp_path / "t"), "--as-of", AS_OF]) == 0
    assert sorted(p.name for p in (tmp_path / "t").iterdir()) == ["ACADEMIC_ARTICLE.tex"]
    assert main(["route", "build", "--route", "academic-article", str(EXAMPLE), "--structure-profile", "7ssa-thai-4",
                 "--out", str(tmp_path / "m"), "--as-of", AS_OF]) == 0
    text = (tmp_path / "m" / "ACADEMIC_ARTICLE.md").read_text(encoding="utf-8")
    assert "structure_profile: 7ssa-thai-4" in text
    assert main(["build", str(EXAMPLE), "--glosa-audit", "--out", str(tmp_path / "x"), "--as-of", AS_OF]) == 2


def test_skill_records_the_structure_profile_the_researcher_chose(tmp_path):
    sys.path.insert(0, str(ROOT / "skills/grantthai/scripts"))
    import grantthai_skill as gs
    shutil.copy(PLAIN_EXAMPLE, tmp_path / "work.yaml")
    answers = {"project": {"route": "academic-article", "structure_profile": "7ssa-thai-5"}, "answers": []}
    lines = gs.apply_answers(api, tmp_path / "work.yaml", answers)
    assert any("routing.structure_profiles.academic-article: 7ssa-thai-5" in ln for ln in lines)
    assert P.load(tmp_path / "work.yaml")["routing"]["structure_profiles"] == {"academic-article": "7ssa-thai-5"}
    with pytest.raises(ValueError, match="needs project.route"):
        gs.apply_answers(api, tmp_path / "work.yaml", {"project": {"structure_profile": "7ssa-world"}})
