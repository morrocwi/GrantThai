"""tests/test_contradictions.py — the contradiction register is complete,
consistent with docs/contradictions.md, referenced from the registry, and
printed (every reading) in the output file."""
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from grantthai.core import project as P  # noqa: E402
from grantthai.render import submission as R  # noqa: E402

REG = yaml.safe_load((ROOT / "registry/contradictions.yaml").read_text(encoding="utf-8"))["contradictions"]
DOC = (ROOT / "docs/contradictions.md").read_text(encoding="utf-8")
FIELDS = {json.loads(x)["field_id"]: json.loads(x)
          for x in (ROOT / "registry/fields.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()}
EXAMPLE = ROOT / "examples/lecturer-no-ai/project.yaml"


def test_register_matches_docs_and_is_open():
    ids = [c["id"] for c in REG]
    assert len(ids) == len(set(ids))
    assert ids == sorted(re.findall(r"^\| (CX-\d\d) \|", DOC, flags=re.M))
    for c in REG:
        assert c["status"] == "OPEN"
        assert len(c["readings"]) >= 2 and all(r["source"] and r["says"] for r in c["readings"])
        assert c["current_handling"]


def test_register_covers_the_audit_list():
    text = " ".join(json.dumps(c, ensure_ascii=False) for c in REG)
    for needle in ("core/05", "core/06 §3", "core/06 §4", "core/02 §11", "Continuing", "SD-3", "UTILIZATION"):
        assert needle in text, needle


def test_references_resolve():
    ids = {c["id"] for c in REG}
    for fid, rec in FIELDS.items():
        for cx in rec.get("conflicts") or []:
            assert cx in ids, (fid, cx)
    for c in REG:
        aff = c.get("affects") or {}
        for f in aff.get("fields") or []:
            assert f in FIELDS, (c["id"], f)
            assert c["id"] in (FIELDS[f].get("conflicts") or []), (c["id"], f)
        for path in aff.get("files") or []:
            assert (ROOT / path).exists(), (c["id"], path)


def test_output_prints_every_reading_and_project_conflicts():
    doc = P.load(EXAMPLE)
    rec = P.records_by_id(doc)["CORE.GENERAL.TITLE_EN"]
    rec["conflicts"] = [{"conflict_id": "CF-1", "description": "Two drafts of the title disagree.",
                         "status": "DECIDED_BY_RESEARCHER", "decision_note": "Kept the shorter one.",
                         "readings": [{"says": "Title A"}, {"says": "Title B", "source_ids": ["SRC-1"]}]}]
    assert P.schema_errors(doc, P.PROJECT_SCHEMA_ID) == []
    text, _ = R.render(doc, EXAMPLE.parent, "2026-09-25")
    sec = text[text.index("### 4.4 Conflicts and open contradictions"):text.index("### 4.5 ")]
    for c in REG:
        assert f"**{c['id']}** (OPEN)" in sec
        for r in c["readings"]:
            assert f"Reading: {r['source']}: {r['says']}" in sec
    assert "**CF-1** on `CORE.GENERAL.TITLE_EN` (DECIDED_BY_RESEARCHER)" in sec
    assert "Reading: Title A" in sec and "Reading: Title B (sources: SRC-1)" in sec
    assert "- CONFLICTS: CX-10 (OPEN; see section 4.4)" in text
