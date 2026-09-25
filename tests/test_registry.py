"""tests/test_registry.py — the generated NRIIS registry is in sync, and the
derived registry keeps its NEEDS_VERIFICATION markers (founder ruling K14)."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_nriis_fields_in_sync():
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools/registry/build_nriis_fields.py"), "--root", str(ROOT), "--check"],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr


def test_no_thai_label_is_asserted():
    for name in ("fields.jsonl", "nriis-fields.jsonl"):
        for line in (ROOT / "registry" / name).read_text(encoding="utf-8").splitlines():
            rec = json.loads(line)
            assert rec["label_th"] == "NEEDS_VERIFICATION"
            assert "NEEDS_VERIFICATION" in rec["markers"]
            assert "NEEDS_VERIFICATION" in rec["observed_form"]


def test_registry_lineage():
    for line in (ROOT / "registry/fields.jsonl").read_text(encoding="utf-8").splitlines():
        rec = json.loads(line)
        assert rec["derived_from"].startswith("core/05@sha256:")
        assert rec["label_en_basis"] == "descriptive"
