"""The v0.2 demo (examples/demo-seedbank): FICTIONAL banner, AI ceiling,
determinism, no leaks, and page-cited comparison sources."""
import re
import shutil
from pathlib import Path

import yaml

from grantthai import api_py as api
from grantthai.core import project as P

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "examples/demo-seedbank"
TRANSCRIPT = ROOT / "docs/demo/transcript-seedbank.md"
COMPARISON = ROOT / "docs/demo/comparison.md"
AS_OF = "2026-09-25"
ABOVE_DRAFT = {"STRUCTURE_CHECKED", "LOGIC_LINKED", "HUMAN_REVIEWED", "VERIFIED", "LOCKED"}
READING = [ROOT / "docs/demo/scored-reading-draft.md", ROOT / "docs/demo/scored-reading-draft.th.md"]
FILES = [TRANSCRIPT, COMPARISON, *READING, DEMO / "README.md", DEMO / "answers.yaml", DEMO / "project.yaml",
         DEMO / "NRIIS_SUBMISSION.md"]


def test_fictional_banner_on_line_1_and_after_the_notice():
    for f in (TRANSCRIPT, DEMO / "README.md"):
        lines = f.read_text(encoding="utf-8").splitlines()
        assert "FICTIONAL" in lines[0], f
        notice = next(i for i, ln in enumerate(lines) if "NOTICE" in ln)
        assert any("FICTIONAL" in ln for ln in lines[notice + 1:notice + 4]), f
    assert COMPARISON.read_text(encoding="utf-8").splitlines()[2].startswith("> **The demo is FICTIONAL.**")
    assert "FICTIONAL" in yaml.safe_load((DEMO / "project.yaml").read_text(encoding="utf-8"))["project_id"]


def test_output_carries_a_fictional_banner_right_after_the_notice():
    body = (DEMO / "NRIIS_SUBMISSION.md").read_text(encoding="utf-8").split("\n---\n", 1)[1]
    lines = [ln for ln in body.splitlines() if ln.strip()]
    assert lines[1].startswith("> **FICTIONAL / สมมติ")
    assert "Submittable to a real call: n/a (fictional call)" in body


def test_nothing_above_draft_and_no_source():
    doc = P.load(DEMO / "project.yaml")
    assert doc["authoring"]["mode"] == "ai_assisted" and doc["authoring"]["tools_disclosed"]
    assert not doc.get("review_records") and not (doc.get("lock") or {}).get("locked")
    for rec, _ in P.iter_records(doc):
        assert rec.get("status") not in ABOVE_DRAFT, rec["field_id"]
        assert (rec.get("provenance") or {}).get("provenance_class") != "SOURCE", rec["field_id"]


def test_every_value_cites_a_transcript_turn():
    doc = P.load(DEMO / "project.yaml")
    turns = {s["source_id"]: s.get("locator") for s in doc["sources"] if s["source_id"].startswith("SRC-T")}
    text = TRANSCRIPT.read_text(encoding="utf-8")
    for sid, loc in turns.items():
        assert f"### {loc} " in text, sid
    for rec, _ in P.iter_records(doc):
        if rec.get("value") is not None:
            assert any(s in turns for s in rec.get("source_ids") or []), rec["field_id"]


def test_validate_block_zero_and_build_is_deterministic(tmp_path):
    rep = api.validate(DEMO / "project.yaml", as_of=AS_OF)
    assert [f for f in rep["findings"] if f["severity"] == "BLOCK" and not f["rule_id"].startswith("ELIG")] == []
    shutil.copy(DEMO / "project.yaml", tmp_path / "project.yaml")
    out = api.build(tmp_path / "project.yaml", as_of=AS_OF).read_bytes()
    assert out == (DEMO / "NRIIS_SUBMISSION.md").read_bytes()
    assert out == api.build(tmp_path / "project.yaml", as_of=AS_OF).read_bytes()


def test_no_local_paths_or_ids():
    tmp = "/" + "tmp" + "/"   # built in pieces so this file does not trip the leak guard itself
    # vendor and AI-credit names are covered for every tracked file by
    # tools/ci/check_attribution.py; this test covers local paths and ids.
    bad = re.compile(r"/home/|" + tmp + r"|/Users/|\b192\.168\.|\b10\.\d+\.\d+\.\d+|session_[0-9A-Za-z]{8,}", re.I)
    for f in FILES:
        m = bad.search(f.read_text(encoding="utf-8"))
        assert m is None, f"{f.name}: {m.group(0) if m else ''}"


def test_private_source_prints_private_only():
    out = (DEMO / "NRIIS_SUBMISSION.md").read_text(encoding="utf-8")
    assert "`SRC-FN1` (PRIMARY_DATA): [private]" in out


def test_every_real_source_citation_has_a_page_or_is_marked_relayed():
    text = COMPARISON.read_text(encoding="utf-8")
    assert re.search(r"^\| R1 \|", text, re.M) and re.search(r"^\| G1 \|", text, re.M)
    # every cell of the structural matrix that names a real document part
    # carries a page, a TOC reference, N/A-report, or says relayed
    matrix = text.split("## 2. Structural matrix")[1].split("### Demo value status")[0]
    for ln in matrix.splitlines():
        if ln.startswith("| ") and not ln.startswith("| Part") and not ln.startswith("|---"):
            cells = [c.strip() for c in ln.strip("|").split("|")][1:5]
            for c in cells:
                assert re.search(r"\bp\d+|TOC|N/A-report|relayed|OPEN|not applicable|keyword", c), (ln, c)
    # no quoted fragment from a real work longer than 15 words
    for q in re.findall(r"“([^”]+)”|\"([^\"]+)\"", text):
        frag = q[0] or q[1]
        assert len(frag.split()) <= 15, frag
