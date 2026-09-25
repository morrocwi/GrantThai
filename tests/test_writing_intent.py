"""tests/test_writing_intent.py — the writing layer (v0.2, module A).

The file guidance/writing_intent.yaml is guidance, never a validator of
knowledge: every id it names exists in the registry, it passes its own
schema, no Thai string is filled without a cited source, every length
target cites a basis, `explain_field` is deterministic, length findings are
REVIEW-level only, and the checklist on the worked example matches a golden
file."""
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from grantthai.cli import cmd_explain_field  # noqa: E402
from grantthai.core import project as P  # noqa: E402
from grantthai.guidance import writing  # noqa: E402
from grantthai.validators.engine import Finding  # noqa: E402

INTENT_PATH = ROOT / "guidance/writing_intent.yaml"
EXAMPLE = ROOT / "examples/lecturer-no-ai/project.yaml"
GOLDEN = ROOT / "tests/golden/writing/checklist-lecturer-no-ai.json"
SOURCES = (ROOT / "docs/sources.md").read_text(encoding="utf-8")

THAI_RE = re.compile(r"[฀-๿]")
SEEN_IN_RE = re.compile(r"^(R[0-9]+ p[0-9]+|NEEDS_INPUT)$")


def _doc() -> dict:
    return yaml.safe_load(INTENT_PATH.read_text(encoding="utf-8"))


def _walk_strings(node, path=""):
    if isinstance(node, str):
        yield path, node
    elif isinstance(node, dict):
        for k, v in node.items():
            yield from _walk_strings(v, f"{path}/{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from _walk_strings(v, f"{path}/{i}")


# --------------------------------------------------------------------- data

def test_file_passes_its_schema():
    errs = P.schema_errors(_doc(), writing.WRITING_INTENT_SCHEMA_ID)
    assert errs == [], "\n".join(errs)


def test_every_field_id_exists_in_registry():
    reg = P.registry_by_id()
    doc = _doc()
    unknown = [f for f in doc["fields"] if f not in reg]
    assert unknown == [], unknown
    for item in doc["completeness_checklist"]:
        for fid in item["field_ids"]:
            assert fid in reg, f"{item['id']}: {fid}"


def test_acceptance_coverage_core_method_results_chain():
    """At least one intent for every CORE.*, METHOD.* and RESULTS.CHAIN.*
    registry field, and a checklist of at least 10 items."""
    reg = P.registry_by_id()
    doc = _doc()
    want = [f for f in reg if f.startswith(("CORE.", "METHOD.", "RESULTS.CHAIN."))]
    assert want, "registry has no target fields?"
    missing = [f for f in want if f not in doc["fields"]]
    assert missing == [], missing
    assert len(doc["completeness_checklist"]) >= 10


def test_no_thai_string_is_filled_without_a_source():
    """Every Thai-script string is exactly NEEDS_INPUT, or sits next to a
    cited source (a `source` key naming an SD-n from docs/sources.md).
    v0.2 fills none, so this reduces to: no Thai script anywhere but in
    a NEEDS_INPUT slot."""
    doc = _doc()
    for path, s in _walk_strings(doc):
        if THAI_RE.search(s):
            assert False, f"{path}: Thai text without a cited source: {s[:40]!r}"
    # and every bilingual `th` slot is the literal marker
    for fid, entry in doc["fields"].items():
        assert entry["purpose"]["th"] == "NEEDS_INPUT", fid
        assert entry["micro_template"]["th"] == "NEEDS_INPUT", fid
    for item in doc["completeness_checklist"]:
        assert item["check"]["th"] == "NEEDS_INPUT", item["id"]


def test_every_length_target_cites_a_basis():
    doc = _doc()
    for fid, entry in doc["fields"].items():
        basis = entry["length_target"]["basis"]
        assert basis.strip(), fid
        # a relayed handoff-package or public-document reading must say so
        if basis.startswith("core/0") or basis.startswith("SD-"):
            assert "NEEDS_VERIFICATION" in basis or "relayed" in basis, fid
        # SD-n ids must be documented in docs/sources.md
        for sd in re.findall(r"\bSD-[0-9]+\b", basis):
            assert f"| {sd} |" in SOURCES, f"{fid}: {sd} not in docs/sources.md"


def test_seen_in_is_page_ref_or_needs_input_never_quoted_text():
    doc = _doc()
    for fid, entry in doc["fields"].items():
        for trait in entry["quality_traits"]:
            assert SEEN_IN_RE.match(trait["seen_in"]), f"{fid}: {trait['seen_in']!r}"
            assert len(trait["trait"].split()) <= 25, f"{fid}: trait too long to be a trait"


def test_derived_from_hashes_are_documented():
    doc = _doc()
    tags = {doc["derived_from"]} | {e["derived_from"] for e in doc["fields"].values()}
    for tag in tags:
        if "@sha256:" in tag:
            assert tag.split("@sha256:")[1] in SOURCES, tag


def test_summary_cap_is_needs_verification():
    entry = _doc()["fields"]["CORE.NARRATIVE.SUMMARY"]
    assert entry["length_target"]["max"] == 3000
    assert "NEEDS_VERIFICATION" in entry["length_target"]["basis"]


def test_file_status_is_draft_and_marked():
    doc = _doc()
    assert doc["status"] == "DRAFT" and doc["status_marker"] == "NEEDS_VERIFICATION"


# ------------------------------------------------------------------ explain

def test_intent_returns_copy_or_none():
    assert writing.intent("CORE.RESEARCH.OBJECTIVES")["length_target"]["unit"] == "items"
    assert writing.intent("PROFILE.NO.SUCH.FIELD") is None
    a = writing.intent("CORE.RESEARCH.OBJECTIVES")
    a["purpose"] = "mutated"
    assert writing.intent("CORE.RESEARCH.OBJECTIVES")["purpose"] != "mutated"


def test_explain_field_is_deterministic_and_merges_registry():
    a = writing.explain_field("CORE.RESEARCH.OBJECTIVES")
    b = writing.explain_field("CORE.RESEARCH.OBJECTIVES")
    assert json.dumps(a, ensure_ascii=False, sort_keys=False) == json.dumps(b, ensure_ascii=False, sort_keys=False)
    assert a["label_en"] == "Research Objectives"
    assert a["label_th"] == "NEEDS_VERIFICATION"
    assert a["writing_intent"]["micro_template"]["en"].startswith("OBJ<n> answers RQ-<n>")
    assert a["writing_intent_status"] == {"status": "DRAFT", "status_marker": "NEEDS_VERIFICATION"}
    # a registry field with no intent still explains, with intent None
    c = writing.explain_field("FUND.CALL.FISCAL_YEAR")
    assert c["writing_intent"] is None and c["writing_intent_status"] is None


def test_explain_field_unknown_id_raises():
    try:
        writing.explain_field("CORE.NO.SUCH_FIELD")
    except KeyError:
        return
    assert False, "expected KeyError"


def test_explain_any_routes_field_ids_and_keeps_rule_ids():
    assert cmd_explain_field.explain_any("CORE.RESEARCH.GAP")["field_id"] == "CORE.RESEARCH.GAP"
    rule = cmd_explain_field.explain_any("S001")
    assert rule["id"] == "S001" and "severity" in rule


def test_cli_explain_field_subcommand(tmp_path):
    """The shipped subcommand works stand-alone through a throwaway parser."""
    import argparse
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    cmd_explain_field.register(sub)
    args = ap.parse_args(["explain-field", "METHOD.PLAN.DESIGN"])
    assert args.func(args) == 0


# ------------------------------------------------------------------ lengths

def test_measure_units():
    assert writing.measure("one two three", "words") == 3
    assert writing.measure({"b": "x y", "a": ["z"]}, "words") == 3
    assert writing.measure(["a", "b"], "items") == 2
    assert writing.measure("abc", "chars") == 3
    assert writing.measure("", "words") is None
    assert writing.measure("NEEDS_INPUT", "words") is None
    assert writing.measure([], "items") is None


def test_length_findings_are_review_only_and_report_only():
    doc = P.load(EXAMPLE)
    before = json.dumps(doc, ensure_ascii=False, sort_keys=True)
    findings = writing.length_findings(doc)
    assert json.dumps(doc, ensure_ascii=False, sort_keys=True) == before
    assert all(isinstance(f, Finding) for f in findings)
    assert all(f.severity in ("REVIEW", "INFO") for f in findings)
    assert all(f.rule_id in ("W101", "W102") for f in findings)
    assert not any(f.severity == "BLOCK" for f in findings)


def test_length_findings_over_max():
    """Negative case for W101: a summary above its target raises exactly one
    REVIEW finding for that field."""
    doc = P.load(EXAMPLE)
    P.set_field(doc, "CORE.NARRATIVE.SUMMARY", "word " * 3001)
    hits = [f for f in writing.length_findings(doc) if "CORE.NARRATIVE.SUMMARY" in f.field_ids]
    assert [f.rule_id for f in hits] == ["W101"]
    assert hits[0].severity == "REVIEW"
    assert "3001 words" in hits[0].message_en


def test_length_findings_under_min():
    """Negative case for W102."""
    doc = P.load(EXAMPLE)
    P.set_field(doc, "CORE.RESEARCH.OBJECTIVES", [])
    P.set_field(doc, "CORE.ALIGNMENT.STATEMENT", "too short")
    hits = {f.field_ids[0]: f for f in writing.length_findings(doc)}
    assert hits["CORE.ALIGNMENT.STATEMENT"].rule_id == "W102"
    # an empty value is NEEDS_INPUT territory (S001), not a length finding
    assert "CORE.RESEARCH.OBJECTIVES" not in hits


def test_thai_prose_never_raises_under_min():
    doc = P.load(EXAMPLE)
    P.set_field(doc, "CORE.RESEARCH.PROBLEM", "ปัญหาสมมติ")
    hits = [f for f in writing.length_findings(doc) if "CORE.RESEARCH.PROBLEM" in f.field_ids]
    assert hits == []


# ---------------------------------------------------------------- checklist

def test_checklist_matches_golden():
    doc = P.load(EXAMPLE)
    got = writing.checklist(doc)
    assert got == json.loads(GOLDEN.read_text(encoding="utf-8"))


def test_checklist_states_and_determinism():
    doc = P.load(EXAMPLE)
    a = writing.checklist(doc)
    b = writing.checklist(doc)
    assert a == b
    ids = [c["id"] for c in a]
    assert ids == sorted(ids) and len(ids) == len(set(ids))
    for c in a:
        assert c["state"] in ("PASS", "OPEN", "HUMAN_CHECK")
        assert (c["state"] == "HUMAN_CHECK") == (c["evaluable"] == "human")


def test_checklist_opens_when_a_field_is_cleared():
    doc = P.load(EXAMPLE)
    P.set_field(doc, "CORE.RESEARCH.GAP", "NEEDS_INPUT")
    states = {c["id"]: c["state"] for c in writing.checklist(doc)}
    assert states["WC01"] == "OPEN"
    doc = P.load(EXAMPLE)
    recs = P.records_by_id(doc)
    for it in recs["CORE.RESEARCH.OBJECTIVES"]["value"]:
        it["rq_ids"] = []
    states = {c["id"]: c["state"] for c in writing.checklist(doc)}
    assert states["WC02"] == "OPEN"


# ------------------------------------------------------------------ hygiene

IMPORT_RE = re.compile(r"^\s*(from|import)\s+(grantthai\.(assist|mcp|api)\b|openai|anthropic|google\.generativeai)", re.M)


def test_no_ai_import_in_guidance_package():
    paths = list((ROOT / "src/grantthai/guidance").glob("*.py")) + [ROOT / "src/grantthai/cli/cmd_explain_field.py"]
    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert not IMPORT_RE.search(text), f"{path.name} imports a forbidden package"


def test_new_files_pass_leak_pii_guard():
    r = subprocess.run([sys.executable, str(ROOT / "tools/ci/check_leak_pii.py"), "--root", str(ROOT)],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
