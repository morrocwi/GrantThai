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
            if rec["origin"] == "VENUE_NATIVE":
                # v0.3: exists for one output route; traced to that route's definition
                assert rec["derived_from"] == "route/academic-article@0.1.0-draft", rec["field_id"]
                assert rec["source_status"] == "INFERRED_SCHEMA_EXTENSION"
                continue
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


ORIGINS = {"NRIIS_NATIVE", "FUND_PROFILE", "AUTHORING_CORE", "DERIVED", "RECOMMENDED_EXTENSION", "VENUE_NATIVE"}


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


# ---- v0.3 router: registry partition (scope / route_ids) ----

def test_partition_is_in_sync():
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools/registry/partition.py"), "--root", str(ROOT), "--check"],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr


def test_partition_counts_are_pinned():
    """122 pre-router fields + 24 ARTICLE.* = 146; shared core 39; NRIIS-only 83;
    article-only 24. Change these numbers only with a registry decision."""
    recs = _jsonl("fields.jsonl")
    assert len(recs) == 146
    article = [r for r in recs if r["field_id"].startswith("ARTICLE.")]
    assert len(article) == 24
    assert len(recs) - len(article) == 122
    by_scope = {}
    for r in recs:
        by_scope.setdefault(r["scope"], []).append(r)
    assert len(by_scope["shared"]) == 39
    nriis_only = [r for r in by_scope["route"] if r["route_ids"] == ["nriis-proposal"]]
    article_only = [r for r in by_scope["route"] if r["route_ids"] == ["academic-article"]]
    assert len(nriis_only) == 83 and len(article_only) == 24
    assert len(by_scope["route"]) == 83 + 24
    # shared <=> placed by more than one route
    for r in recs:
        assert (r["scope"] == "shared") == (len(r["route_ids"]) >= 2), r["field_id"]
        assert len(r["route_ids"]) == len(set(r["route_ids"]))
    # every shared field is placed by both the NRIIS and the article route
    for r in by_scope["shared"]:
        assert {"nriis-proposal", "academic-article"} <= set(r["route_ids"]), r["field_id"]


def test_article_fields_are_venue_native_route_scoped_and_never_required_globally():
    """ARTICLE.* fields exist for the academic-article route only. They are never
    NRIIS fields (R4), never required by the registry flag (the route's own
    required_fields drives S001 there, so the NRIIS route is untouched), and
    every venue-specific fact about them stays NEEDS_VERIFICATION."""
    recs = _jsonl("fields.jsonl")
    article = [r for r in recs if r["field_id"].startswith("ARTICLE.")]
    for r in article:
        assert r["origin"] == "VENUE_NATIVE" and r["section"] == "Article", r["field_id"]
        assert r["scope"] == "route" and r["route_ids"] == ["academic-article"], r["field_id"]
        assert r["required"] is False, r["field_id"]
        assert r["chain_node"] is None
        assert r["label_th"] == "NEEDS_VERIFICATION" and r["guidance"]["th"] == "NEEDS_INPUT"
        for src in r.get("render_from") or []:
            assert src in {x["field_id"] for x in recs} and not src.startswith("ARTICLE."), (r["field_id"], src)
    assert not any(r["origin"] == "VENUE_NATIVE" for r in recs if not r["field_id"].startswith("ARTICLE."))
    # the NRIIS render view is untouched by the article fields
    assert not any(n["core_field_id"].startswith("ARTICLE.") for n in _jsonl("nriis-fields.jsonl"))
    ids = {r["field_id"] for r in article}
    assert ids == {
        "ARTICLE.META.KIND", "ARTICLE.META.LANGUAGE", "ARTICLE.META.TITLE_TH", "ARTICLE.META.TITLE_EN",
        "ARTICLE.META.REFERENCE_STYLE",
        "ARTICLE.FRONT.ABSTRACT_TH", "ARTICLE.FRONT.ABSTRACT_EN", "ARTICLE.FRONT.AUTHORS", "ARTICLE.FRONT.CONTRIBUTIONS",
        "ARTICLE.SECTION.INTRODUCTION", "ARTICLE.SECTION.METHODS", "ARTICLE.SECTION.RESULTS",
        "ARTICLE.SECTION.DISCUSSION", "ARTICLE.SECTION.CONCLUSION", "ARTICLE.SECTION.LIMITATIONS",
        "ARTICLE.BODY.SECTIONS", "ARTICLE.BODY.FIGURES_TABLES",
        "ARTICLE.STATEMENT.ETHICS", "ARTICLE.STATEMENT.AI_USE", "ARTICLE.STATEMENT.DATA_AVAILABILITY",
        "ARTICLE.STATEMENT.CONFLICT_OF_INTEREST", "ARTICLE.STATEMENT.FUNDING",
        "ARTICLE.BACK.ACKNOWLEDGEMENTS", "ARTICLE.VENUE.TARGET",
    }


def test_pre_router_records_only_gained_scope_and_route_ids():
    """The 122 legacy records are byte-identical apart from the two new keys."""
    # Pinned to the last commit before the router work; a branch name would move.
    legacy = subprocess.run(["git", "show", "0d79ef1:registry/fields.jsonl"], cwd=ROOT,
                            capture_output=True, text=True)
    if legacy.returncode != 0:
        import pytest
        pytest.skip("pre-router baseline commit 0d79ef1 not available")
    old = [json.loads(x) for x in legacy.stdout.splitlines() if x.strip()]
    new = _jsonl("fields.jsonl")
    assert len(old) == 122
    for o, n in zip(old, new[:122]):
        n = dict(n)
        n.pop("scope"); n.pop("route_ids")
        assert o == n, o["field_id"]
