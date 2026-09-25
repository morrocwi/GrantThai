"""tests/test_labels.py — candidate Thai labels come only from cited public
documents, stay NEEDS_VERIFICATION, never touch the registry's label_th,
and are shown in the output tagged as candidates (founder ruling K14)."""
import json
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from grantthai import api_py as api  # noqa: E402

LABELS = sorted((ROOT / "mappings/nriis").glob("labels@*.yaml"))
SOURCES = (ROOT / "docs/sources.md").read_text(encoding="utf-8")


def test_labels_are_candidates_from_cited_public_documents():
    assert LABELS
    for path in LABELS:
        text = path.read_text(encoding="utf-8")
        doc = yaml.safe_load(text)
        assert doc["status"] == "CANDIDATE" and doc["status_marker"] == "NEEDS_VERIFICATION"
        for sd, meta in doc["sources"].items():
            assert f"| {sd} |" in SOURCES
            assert meta["derived_from"].split("@sha256:")[1] in SOURCES
        # never the screenshot-derived readout (K14)
        assert "screenshot" not in json.dumps(doc["field_labels"], ensure_ascii=False).lower()
        for fid, entry in doc["field_labels"].items():
            assert entry["source"]["doc"] in doc["sources"], fid


def test_registry_label_th_is_untouched():
    for line in (ROOT / "registry/fields.jsonl").read_text(encoding="utf-8").splitlines():
        assert json.loads(line)["label_th"] == "NEEDS_VERIFICATION"


def test_output_shows_candidates_tagged(tmp_path):
    shutil.copy(ROOT / "examples/lecturer-no-ai/project.yaml", tmp_path / "project.yaml")
    text = api.build(tmp_path / "project.yaml", as_of="2026-09-25").read_text(encoding="utf-8")
    assert 'LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "ชื่อโครงการ" (SD-1 p15, item 1.1))' in text
    assert '### Tab 1: GENERAL (NEEDS_VERIFICATION); candidate part label (candidate, NEEDS_VERIFICATION): ' in text
    for line in text.splitlines():
        if line.startswith("LABEL_TH:") and "candidate" in line:
            assert line.startswith("LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: ")
