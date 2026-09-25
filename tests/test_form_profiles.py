"""tests/test_form_profiles.py — v0.2 form profiles
(mappings/nriis/form_profiles/, spec/mappings/form_profile.schema.json,
grantthai.mapping.form_profile).

Every shipped profile passes its schema, references only registry fields,
carries NEEDS_VERIFICATION and a page; with no `form_profile` the example
build is byte-identical to the v0.1.0 golden output; ProfileView.required
changes exactly as each profile says; an unknown id is reported, never
silently ignored; and `form_profile` is project content (it moves
content_sha256)."""
import copy
import hashlib
import shutil
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from grantthai import api_py as api  # noqa: E402
from grantthai.core import project as P  # noqa: E402
from grantthai.core.object_hash import content_sha256  # noqa: E402
from grantthai.mapping import form_profile as FP  # noqa: E402
from grantthai.validators import engine as E  # noqa: E402

EXAMPLE = ROOT / "examples/lecturer-no-ai/project.yaml"
AS_OF = "2026-09-25"
PROFILE_DIR = ROOT / "mappings/nriis/form_profiles"
SOURCES = (ROOT / "docs/sources.md").read_text(encoding="utf-8")

# sha256 of build/NRIIS_SUBMISSION.md for examples/lecturer-no-ai at
# as_of 2026-09-25. v0.1.0 (main bbe3f8c) gave 2ca02132...a838 (102026 bytes);
# the v0.2 forms module reproduced it byte for byte with form_profile absent.
# The v0.2 integration then changed the template and contract on purpose
# (renderer 0.2.0: form_profile frontmatter key, review-gate hold reasons,
# W101/W102 findings, section 4.6 completeness checklist), so the golden was
# re-pinned in the same commit (CHANGELOG.md, v0.2). Regenerate it only for
# a deliberate template or contract change, and say so in CHANGELOG.md.
# Re-pinned for the v0.2.0 release: package version 0.2.0 in the
# frontmatter, the FICTIONAL-call banner and "n/a (fictional call)"
# submittable line, and the split section 1.5 advice.
# Re-pinned for renderer 0.3.0 (the AI-use ceiling): renderer_version, the
# frontmatter line authoring.ai_use_declaration: none, and section 4.7 (the
# AI Use Declaration appendix, "no AI use recorded" for this example). No
# other byte changed.
GOLDEN_V010_SHA256 = "060dd7d4d93dfd2da384d6e22779767f1dd3802175b4122987baace408f60b16"
GOLDEN_V010_BYTES = 110716

EXPECTED_IDS = {
    "research@sd1-2566", "innovation@sd1-2566", "personnel_development@sd1-2566",
    "system_standard@sd1-2566", "promotion_activity@sd1-2566",
    "pmu_template@sd2-2564", "pmu_template@sd3-2569",
    "ff_full_proposal@nriis-2570",
}


def _profiles():
    return {p.name[:-5]: yaml.safe_load(p.read_text(encoding="utf-8")) for p in sorted(PROFILE_DIR.glob("*.yaml"))}


def _rules(report, sev=None, rid=None):
    return [f for f in report["findings"]
            if (sev is None or f["severity"] == sev) and (rid is None or f["rule_id"] == rid)]


# --------------------------------------------------------------------------
# Data contract
# --------------------------------------------------------------------------

def test_eight_profiles_ship_and_ids_match_file_names():
    assert set(FP.profile_ids()) == EXPECTED_IDS
    for name, doc in _profiles().items():
        assert doc["id"] == name


def test_every_profile_passes_schema_and_field_check():
    for name, doc in _profiles().items():
        assert FP.check(doc) == [], name
        assert P.schema_errors(doc, FP.SCHEMA_ID) == [], name


def test_every_referenced_field_id_exists():
    known = set(P.registry_by_id())
    for name, doc in _profiles().items():
        refs = list(doc["require"]) + list(doc["hide"]) + list(doc["render_only"] or [])
        refs += list(doc.get("require_basis") or {})
        for item in doc["extra_items"]:
            refs += item.get("nearest_field_ids") or []
        for fid in refs:
            assert fid in known, (name, fid)


def test_every_profile_is_needs_verification_with_a_page():
    for name, doc in _profiles().items():
        assert doc["status_marker"] == "NEEDS_VERIFICATION", name
        assert isinstance(doc["source"]["page"], int) and doc["source"]["page"] >= 1, name
        assert doc["title_th"] == "NEEDS_VERIFICATION", name  # no Thai label without a cited transcription
        for item in doc["extra_items"]:
            assert item["status"] == "NEEDS_VERIFICATION" and item["page"] >= 1, name
        for rule in doc["budget_rules"]:
            assert rule["evaluable"] is False and rule["page"] >= 1, name
        for fid, basis in (doc.get("require_basis") or {}).items():
            assert basis["page"] >= 1 and fid in doc["require"], (name, fid)


def test_sources_are_registered_or_flagged_pending():
    """SD-1..4 are in docs/sources.md with their sha256. A candidate source
    (SD-5 / R0) must say so (`pending_registration: true`) and carry no
    sha256 it cannot cite."""
    for name, doc in _profiles().items():
        sd = doc["source"]["sd"]
        sha = doc["derived_from"].split("@sha256:")[1]
        if f"| {sd} |" in SOURCES:
            assert sha in SOURCES, (name, "sha256 not in docs/sources.md")
            assert not doc["source"].get("pending_registration"), name
        else:
            assert doc["source"].get("pending_registration") is True, (name, sd, "not in docs/sources.md")
            assert sha == "NEEDS_VERIFICATION", name


def test_no_profile_evaluates_a_budget_rule_or_names_a_fund_amount():
    for name, doc in _profiles().items():
        for rule in doc["budget_rules"]:
            assert rule["id"].endswith("-candidate"), name
        # no time-bound amount smuggled in: a number next to a currency word
        text = (PROFILE_DIR / f"{name}.yaml").read_text(encoding="utf-8")
        assert "บาท" not in text and "baht" not in text.lower(), name


# --------------------------------------------------------------------------
# ProfileView
# --------------------------------------------------------------------------

def test_default_view_equals_registry():
    v = FP.view(None)
    assert v.profile_id is None
    assert v.required == frozenset(r["field_id"] for r in P.registry() if r.get("required"))
    assert v.rendered == tuple(r["field_id"] for r in P.registry())
    assert v.tab_order == tuple(P.tab_mapping()["tab_order"])
    assert v.extra_items == () and v.budget_rules == ()
    assert v.profile_required == frozenset()


def test_required_changes_as_each_profile_says():
    base = FP.view(None).required
    for pid in FP.profile_ids():
        doc = FP.load(pid)
        v = FP.view(doc)
        assert v.profile_id == pid
        expected = (base | set(doc["require"])) - set(doc["hide"])
        assert v.required == frozenset(expected), pid
        assert v.profile_required == frozenset(set(doc["require"]) - base), pid
        assert v.tab_order == tuple(doc.get("tab_order") or P.tab_mapping()["tab_order"]), pid
        assert len(v.extra_items) == len(doc["extra_items"]) and len(v.budget_rules) == len(doc["budget_rules"])
    # the concrete claims of the shipped profiles
    # SD-5 p1: the "work being built on" block is conditional (focus area 6
    # only), so it is an extra item, never an unconditional requirement.
    ff = FP.view(FP.load("ff_full_proposal@nriis-2570"))
    assert ff.profile_required == frozenset()
    assert any("focus area 6" in x["ref"] for x in ff.extra_items)
    assert [r["id"] for r in ff.budget_rules] == ["B101-candidate", "B102-candidate", "B103-candidate"]
    assert "not a per-project check" in ff.budget_rules[0]["text"]
    for pid in ("pmu_template@sd2-2564", "pmu_template@sd3-2569"):
        assert FP.view(FP.load(pid)).profile_required == frozenset({"DOC.ATTACHMENTS.DOCUMENTS"})
    for pid in ("research@sd1-2566", "innovation@sd1-2566", "personnel_development@sd1-2566",
                "system_standard@sd1-2566", "promotion_activity@sd1-2566"):
        assert FP.view(FP.load(pid)).required == base, pid


def _inline(**over):
    p = {
        "schema": "grantthai.form_profile.v0", "version": "0.0.0-test", "id": "inline@test-0000",
        "title_en": "inline test profile", "status_marker": "NEEDS_VERIFICATION",
        "source": {"sd": "SD-1", "page": 47},
        "derived_from": "sourcedoc/SD-1@sha256:" + "0" * 64,
        "require": [], "render_only": None, "hide": [], "extra_items": [], "budget_rules": [],
    }
    p.update(over)
    return p


def test_render_only_hide_and_tab_order_override():
    v = FP.view(_inline(render_only=["CORE.GENERAL.TITLE_EN", "CORE.GENERAL.TITLE_TH"],
                        hide=["BUDGET.PLAN.ITEMS"],
                        tab_order=["PROJECT", "GENERAL", "WORKPLAN", "UTILIZATION", "ATTACHMENTS"]))
    assert v.rendered == ("CORE.GENERAL.TITLE_TH", "CORE.GENERAL.TITLE_EN")   # registry order kept
    assert "BUDGET.PLAN.ITEMS" in FP.view(None).required
    assert "BUDGET.PLAN.ITEMS" not in v.required                               # hidden => never required
    assert v.tab_order[0] == "PROJECT"
    w = FP.view(_inline(hide=["CORE.GENERAL.KEYWORDS_EN"]))
    assert w.rendered == tuple(f for f in FP.view(None).rendered if f != "CORE.GENERAL.KEYWORDS_EN")


def test_check_rejects_bad_profiles():
    assert FP.check(_inline(require=["CORE.NOPE.X"]))
    assert FP.check(_inline(require=["CORE.GENERAL.TITLE_TH"], hide=["CORE.GENERAL.TITLE_TH"]))
    assert FP.check(_inline(status_marker="PUBLIC_DOCUMENT"))
    assert FP.check(_inline(budget_rules=[{"id": "B101-candidate", "text": "x", "page": 1, "evaluable": True}]))
    assert FP.check(_inline(source={"sd": "SD-1"}))
    with pytest.raises(FP.FormProfileError):
        FP.view(_inline(require=["CORE.NOPE.X"]))
    with pytest.raises(FP.FormProfileNotFound):
        FP.load("does_not_exist@sd9-9999")
    with pytest.raises(FP.FormProfileNotFound):
        FP.load("../section_to_tab")


def test_load_returns_a_copy():
    a = FP.load("research@sd1-2566")
    a["require"].append("CORE.GENERAL.TITLE_TH")
    assert FP.load("research@sd1-2566")["require"] == []


def test_describe_is_deterministic():
    for pid in FP.profile_ids():
        assert FP.describe(pid) == FP.describe(pid)
        assert FP.describe(pid)["status_marker"] == "NEEDS_VERIFICATION"


# --------------------------------------------------------------------------
# Engine and build
# --------------------------------------------------------------------------

def test_example_build_without_profile_matches_golden(tmp_path):
    shutil.copy(EXAMPLE, tmp_path / "project.yaml")
    out = api.build(tmp_path / "project.yaml", as_of=AS_OF).read_bytes()
    assert len(out) == GOLDEN_V010_BYTES
    assert hashlib.sha256(out).hexdigest() == GOLDEN_V010_SHA256


def test_explicit_null_profile_renders_like_absent(tmp_path):
    doc = P.load(EXAMPLE)
    doc["form_profile"] = None
    assert E.run(doc, tmp_path, as_of=AS_OF).report["summary"]["block"] == 0
    from grantthai.render import submission as R
    a, _ = R.render(P.load(EXAMPLE), tmp_path, AS_OF)
    b, _ = R.render(doc, tmp_path, AS_OF)
    # The key's presence is authored content (spec/common/object-hash.md), so
    # only the two hash lines may differ.
    strip = lambda t: [ln for ln in t.splitlines() if not ln.startswith(("project_content_sha256:", "project_state_sha256:"))]
    assert strip(a) == strip(b)


def test_profile_items_render_in_readiness_summary(tmp_path):
    doc = P.load(EXAMPLE)
    doc["form_profile"] = "ff_full_proposal@nriis-2570"
    from grantthai.render import submission as R
    text, res = R.render(doc, tmp_path, AS_OF)
    assert res.report["summary"]["block"] == 0
    assert not [f for f in res.findings if f.rule_id == "SCHEMA"]
    assert "form_profile: ff_full_proposal@nriis-2570" in text
    assert "### 1.8 Form profile `ff_full_proposal@nriis-2570` (NEEDS_VERIFICATION)" in text
    assert "Unmapped profile items (NEEDS_VERIFICATION)" in text
    assert "B101-candidate (p9)" in text
    doc["form_profile"] = "pmu_template@sd2-2564"
    doc["fields"] = [r for r in doc["fields"] if r.get("field_id") != "DOC.ATTACHMENTS.DOCUMENTS"]
    text, res = R.render(doc, tmp_path, AS_OF)
    assert "REQUIRED: true (form profile pmu_template@sd2-2564, NEEDS_VERIFICATION)" in text
    assert "`DOC.ATTACHMENTS.DOCUMENTS`: NEEDS_INPUT" in text


def test_engine_reads_profile_required(tmp_path):
    doc = P.load(EXAMPLE)
    base = E.run(doc, tmp_path, as_of=AS_OF)
    assert base.form_profile.profile_id is None
    assert _rules(base.report, rid="S001") == []

    doc2 = copy.deepcopy(doc)
    doc2["fields"] = [r for r in doc2["fields"] if r.get("field_id") != "DOC.ATTACHMENTS.DOCUMENTS"]
    doc2["form_profile"] = "pmu_template@sd2-2564"
    res = E.run(doc2, tmp_path, as_of=AS_OF)
    assert res.form_profile.profile_id == "pmu_template@sd2-2564"
    s001 = _rules(res.report, rid="S001")
    missing = {f["field_ids"][0] for f in s001}
    present = {r.get("field_id") for r, _ in P.iter_records(doc2) if r.get("value") not in (None, "NEEDS_INPUT")}
    assert missing == res.form_profile.profile_required - present
    assert missing == {"DOC.ATTACHMENTS.DOCUMENTS"}
    for f in s001:
        assert "form profile pmu_template@sd2-2564" in f["message_en"]
        assert "NEEDS_VERIFICATION" in f["message_en"]
    # every S001 finding is BLOCK, as the catalog says
    assert all(f["severity"] == "BLOCK" for f in s001)


def test_unknown_profile_is_reported_not_ignored(tmp_path):
    doc = P.load(EXAMPLE)
    doc["form_profile"] = "nope@sd9-9999"
    res = E.run(doc, tmp_path, as_of=AS_OF)
    assert res.form_profile.profile_id is None                       # falls back to the observed form
    msgs = [f["message_en"] for f in _rules(res.report, "BLOCK", "SCHEMA")]
    assert any("not a shipped profile" in m for m in msgs)
    assert res.submittable is False


def test_form_profile_is_content_and_moves_content_sha256():
    doc = P.load(EXAMPLE)
    h0 = content_sha256(doc)
    doc["form_profile"] = "research@sd1-2566"
    assert content_sha256(doc) != h0
    doc["form_profile"] = None
    assert content_sha256(doc) != h0   # even an explicit null is content (spec/common/object-hash.md)


def test_profile_never_touches_status_or_hash():
    """Resolving a profile is read-only: the document object is unchanged."""
    doc = P.load(EXAMPLE)
    doc["form_profile"] = "ff_full_proposal@nriis-2570"
    before = copy.deepcopy(doc)
    FP.resolve(doc)
    assert doc == before
