"""tests/test_practice_patterns.py — practice shared by funded work
(docs/practice/funded-work-patterns.md).

The FW rules are REVIEW-only practice checks derived from CORE patterns of
the corpus of 100 funded final reports (docs/demo/corpus-100.csv). This
file checks: each FW rule fires on a negative case and stays quiet on the
worked example; no FW rule is BLOCK; every `practice:` entry in
guidance/writing_intent.yaml states the same count and tier as the script
tools/corpus/practice_stats.py computes from the public CSV; and only CORE
patterns carry a rule."""
import importlib.util
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from grantthai import api_py as api  # noqa: E402
from grantthai.core import project as P  # noqa: E402
from grantthai.validators.engine import item_numbers  # noqa: E402

EXAMPLE = ROOT / "examples/lecturer-no-ai/project.yaml"
DEMO = ROOT / "examples/demo-seedbank/project.yaml"
AS_OF = "2026-09-25"
PATTERNS_DOC = ROOT / "docs/practice/funded-work-patterns.md"
EVIDENCE_RE = re.compile(r"^([0-9]{1,3})/100 funded reports \(corpus-100\)$")


def _stats():
    spec = importlib.util.spec_from_file_location("practice_stats", ROOT / "tools/corpus/practice_stats.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    rows, _ = mod.compute(ROOT / "docs/demo/corpus-100.csv")
    return {r["pattern_id"]: r for r in rows}


def _report(tmp_path, mutate, base=EXAMPLE):
    doc = P.load(base)
    mutate(doc)
    path = tmp_path / "project.yaml"
    P.save(doc, path)
    return api.validate(path, as_of=AS_OF)


def _ids(rep, sev):
    return [f["rule_id"] for f in rep["findings"] if f["severity"] == sev]


def _rec(doc, fid):
    return P.records_by_id(doc)[fid]


# ----------------------------------------------------------------- the rules

def test_worked_example_has_no_FW_findings():
    rep = api.validate(EXAMPLE, as_of=AS_OF)
    assert not {"FW001", "FW002"} & set(_ids(rep, "REVIEW") + _ids(rep, "BLOCK") + _ids(rep, "INFO"))


def test_FW001_theory_without_references(tmp_path):
    def m(d):
        d["fields"] = [r for r in d["fields"] if r["field_id"] != "CORE.NARRATIVE.REFERENCES"]
    rep = _report(tmp_path, m)
    assert "FW001" in _ids(rep, "REVIEW") and "FW001" not in _ids(rep, "BLOCK")
    # an empty list counts as empty too
    rep = _report(tmp_path, lambda d: _rec(d, "CORE.NARRATIVE.REFERENCES").update(value=[]))
    assert "FW001" in _ids(rep, "REVIEW")


def test_FW001_quiet_when_no_theory_content(tmp_path):
    def m(d):
        d["fields"] = [r for r in d["fields"] if r["field_id"] != "CORE.NARRATIVE.REFERENCES"]
        for stage, recs in (d.get("chain") or {}).items():
            d["chain"][stage] = [r for r in recs if r.get("field_id") != "CORE.RESEARCH.THEORETICAL_FOUNDATIONS"]
        _rec(d, "CORE.NARRATIVE.THEORY")["value"] = "NEEDS_INPUT"
    assert "FW001" not in _ids(_report(tmp_path, m), "REVIEW")


def test_FW002_objectives_not_numbered(tmp_path):
    rep = _report(tmp_path, lambda d: _rec(d, "CORE.NARRATIVE.OBJECTIVES").update(
        value="FICTIONAL: describe current water use and co-design a shared schedule."))
    assert "FW002" in _ids(rep, "REVIEW") and "FW002" not in _ids(rep, "BLOCK")


def test_FW002_accepts_thai_and_bracketed_numbering(tmp_path):
    for text in ("FICTIONAL: ๑) สำรวจ ๒) ทดลอง", "FICTIONAL: (1) describe; (2) test", "ข้อ 1 สำรวจ ข้อ 2 ทดลอง"):
        rep = _report(tmp_path, lambda d, t=text: _rec(d, "CORE.NARRATIVE.OBJECTIVES").update(value=t))
        assert "FW002" not in _ids(rep, "REVIEW"), text


def test_item_numbers_ignores_decimals():
    assert item_numbers("rates of 2.5 and 3.5 per cent") == set()
    assert item_numbers("1) a 2) b 3) c") == {1, 2, 3}


def test_demo_shows_FW001_as_review_not_block():
    rep = api.validate(DEMO, as_of=AS_OF)
    assert "FW001" in _ids(rep, "REVIEW")
    assert rep["summary"]["block"] == len([f for f in rep["findings"] if f["severity"] == "BLOCK"])
    assert "FW001" not in _ids(rep, "BLOCK")


def test_FW_rules_are_never_block_and_cite_corpus():
    rules = [r for r in P.rules_catalog()["rules"] if r["family"] == "FW"]
    assert {r["id"] for r in rules} == {"FW001", "FW002"}
    stats = _stats()
    for r in rules:
        assert r["severity"] == "REVIEW", r["id"]
        assert r["source"]["derived_from"] == "docs/practice/funded-work-patterns.md"
        m = re.match(r"^corpus-100 pattern (FWP-[0-9]{2}) \(([0-9]+)/100; CORE\)$", r["source"]["locator"])
        assert m, r["id"]
        st = stats[m.group(1)]
        assert st["tier"] == "CORE" and st["kind"] == "proposal", r["id"]
        assert int(m.group(2)) == st["n"], r["id"]


# ------------------------------------------------------- guidance practice

def _practice_entries():
    doc = yaml.safe_load((ROOT / "guidance/writing_intent.yaml").read_text(encoding="utf-8"))
    for fid, entry in doc["fields"].items():
        for p in entry.get("practice") or []:
            yield fid, p


def test_practice_entries_match_the_csv():
    stats = _stats()
    seen = 0
    for fid, p in _practice_entries():
        seen += 1
        st = stats[p["pattern_id"]]
        m = EVIDENCE_RE.match(p["evidence"])
        assert m, (fid, p["evidence"])
        assert int(m.group(1)) == st["n"], (fid, p["pattern_id"])
        assert p["tier"] == st["tier"], (fid, p["pattern_id"], st["tier"])
        assert p["tier"] in ("CORE", "CONTEXTUAL", "EMERGING"), (fid, p["pattern_id"])
        assert fid in st["field_ids"], (fid, p["pattern_id"])
    assert seen >= 10


def test_practice_seen_in_cites_doc_and_page_only():
    ids = {ln.split(",", 1)[0] for ln in (ROOT / "docs/demo/corpus-100.csv").read_text(encoding="utf-8").splitlines()[1:]}
    for fid, p in _practice_entries():
        for ref in p.get("seen_in") or []:
            doc_id, page = ref.split(" p", 1)
            assert doc_id in ids and page.replace("-", "").isdigit(), (fid, ref)


def test_patterns_doc_lists_every_rule_and_core_pattern():
    text = PATTERNS_DOC.read_text(encoding="utf-8")
    for rid in ("FW001", "FW002"):
        assert rid in text
    for pid, st in _stats().items():
        assert f"| {pid} |" in text, pid
