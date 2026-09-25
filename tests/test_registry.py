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
    sources_md = (ROOT / "docs/sources.md").read_text(encoding="utf-8")
    for line in (ROOT / "registry/fields.jsonl").read_text(encoding="utf-8").splitlines():
        rec = json.loads(line)
        assert rec["label_en_basis"] == "descriptive"
        if rec["source_field_id"].startswith("NONE"):
            # added after Phase 0 from core/02 or a public source document
            assert rec["derived_from"].startswith(("core/02@sha256:", "sourcedoc/SD-")), rec["field_id"]
            if rec["source_status"] == "PUBLIC_DOCUMENT":
                doc = rec["source_document"]
                assert doc["status"] == "NEEDS_VERIFICATION"
                assert f"| {doc['doc_id']} |" in sources_md, doc["doc_id"]
            if rec["derived_from"].startswith("sourcedoc/"):
                sd, sha = rec["derived_from"][len("sourcedoc/"):].split("@sha256:")
                assert f"| {sd} |" in sources_md and sha in sources_md, rec["field_id"]
        else:
            assert rec["derived_from"].startswith("core/05@sha256:"), rec["field_id"]


ORIGINS = {"NRIIS_NATIVE", "FUND_PROFILE", "AUTHORING_CORE", "DERIVED", "RECOMMENDED_EXTENSION"}


def _jsonl(name):
    return [json.loads(x) for x in (ROOT / "registry" / name).read_text(encoding="utf-8").splitlines() if x.strip()]


def test_every_record_declares_an_origin_with_basis():
    for rec in _jsonl("fields.jsonl"):
        assert rec["origin"] in ORIGINS, rec["field_id"]
        assert rec["origin_basis"].strip(), rec["field_id"]


def test_only_nriis_native_fields_are_rendered_onto_tabs():
    """core/02 R4: authoring-core fields are never presented as NRIIS fields."""
    reg = {r["field_id"]: r for r in _jsonl("fields.jsonl")}
    nriis = _jsonl("nriis-fields.jsonl")
    assert nriis
    for n in nriis:
        assert n["origin"] == "NRIIS_NATIVE" == reg[n["core_field_id"]]["origin"]
    core = {n["core_field_id"] for n in nriis}
    assert not any(f.startswith(("METHOD.PLAN.", "CORE.RESEARCH.", "AUDIT.", "DOC.META.")) for f in core)
    # the methodology reaches NRIIS once, through the narrative box
    assert [f for f in core if "METHOD" in f] == ["CORE.NARRATIVE.METHOD"]


def test_narrative_fields_carry_render_from():
    for n in _jsonl("nriis-fields.jsonl"):
        if n["core_field_id"].startswith("CORE.NARRATIVE.") and n["core_field_id"] in (
                "CORE.NARRATIVE.SUMMARY", "CORE.NARRATIVE.RATIONALE", "CORE.NARRATIVE.OBJECTIVES",
                "CORE.NARRATIVE.FRAMEWORK", "CORE.NARRATIVE.THEORY", "CORE.NARRATIVE.METHOD"):
            assert n.get("render_from"), n["core_field_id"]


def test_policy_pathway_options_come_from_the_relayed_positions_file():
    import yaml
    pos = yaml.safe_load((ROOT / "ecosystem/positions@2026-09.yaml").read_text(encoding="utf-8"))
    assert pos["trust_level"] == "RELAYED" and "NEEDS_VERIFICATION" in pos["markers"]
    codes = [lens["code"] for lens in pos["lenses"]]
    reg = {r["field_id"]: r for r in _jsonl("fields.jsonl")}
    assert reg["CORE.ALIGNMENT.POLICY_PATHWAY"]["allowed_values"] == codes
    assert len(pos["positions"]) == 11 and all(p["trust_level"] == "RELAYED" for p in pos["positions"])
