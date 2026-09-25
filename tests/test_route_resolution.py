"""v0.3 router: input discovery, the legacy view, route resolution (the
tool never picks between routes), migrate, and route-scoped validation."""
import copy
import shutil
from pathlib import Path

import pytest

from grantthai import api_py as api
from grantthai.cli import main
from grantthai.core import project as P
from grantthai.core.object_hash import content_sha256
from grantthai.routes import registry as R
from grantthai.routes import resolve as RS

ROOT = Path(__file__).resolve().parents[1]
LECTURER = ROOT / "examples/lecturer-no-ai/project.yaml"
DEMO = ROOT / "examples/demo-seedbank/project.yaml"
AS_OF = "2026-09-25"


# Routes whose files load in every wave. Resolution step 4 reads every
# route's default_for_work_types; tests that exercise it pin the route list
# so they do not depend on the article route's file (another work package).
TWO_ROUTES = ("nriis-proposal", "concept-note")


@pytest.fixture
def two_routes(monkeypatch):
    monkeypatch.setattr(R, "route_ids", lambda include_planned=False: TWO_ROUTES)


def _work(**over) -> dict:
    doc = P.migrated(P.load(LECTURER))
    doc.pop("routing")
    doc.update(over)
    return doc


# discovery ---------------------------------------------------------------

def test_both_canonical_inputs_in_one_directory_exit_2(tmp_path, capsys):
    shutil.copy(LECTURER, tmp_path / "project.yaml")
    P.save(_work(), tmp_path / "work.yaml")
    for argv in (["build", str(tmp_path)], ["build", str(tmp_path / "project.yaml")],
                 ["route", "build", "--route", "nriis-proposal", str(tmp_path)],
                 ["validate", str(tmp_path)]):
        assert main(argv + ["--as-of", AS_OF]) == 2, argv
        assert "two canonical inputs" in capsys.readouterr().err
    assert not (tmp_path / "build").exists()
    with pytest.raises(P.TwoCanonicalInputs):
        api.build(tmp_path, as_of=AS_OF)


def test_directory_discovery_prefers_work_yaml(tmp_path):
    shutil.copy(LECTURER, tmp_path / "project.yaml")
    assert P.discover(tmp_path) == tmp_path / "project.yaml"
    (tmp_path / "project.yaml").unlink()
    P.save(_work(), tmp_path / "work.yaml")
    assert P.discover(tmp_path) == tmp_path / "work.yaml"
    with pytest.raises(FileNotFoundError):
        P.discover(tmp_path / "missing")


# legacy view -------------------------------------------------------------

def test_legacy_view_reads_a_02_file_as_nriis_without_rewriting_it():
    before = LECTURER.read_bytes()
    doc = P.load(DEMO)
    v = P.work_view(doc)
    assert v["legacy"] and v["work_type"] == "research_proposal" and v["default_route"] == "nriis-proposal"
    assert v["sub_profiles"] == {"nriis-proposal": doc["form_profile"]}
    assert RS.resolve_route(doc) == "nriis-proposal"
    assert RS.resolve_sub_profile(doc, "nriis-proposal") == doc["form_profile"]
    assert P.work_view(P.load(LECTURER))["sub_profiles"] == {}
    assert LECTURER.read_bytes() == before


# resolution --------------------------------------------------------------

def test_resolution_order_explicit_then_default_route_then_work_type(two_routes):
    doc = _work(work_type="concept_note")
    assert RS.resolve_route(doc) == "concept-note"                       # step 4: single default
    doc["routing"] = {"default_route": "nriis-proposal"}
    assert RS.resolve_route(doc) == "nriis-proposal"                     # step 2
    assert RS.resolve_route(doc, "concept-note") == "concept-note"       # step 1
    with pytest.raises(R.RouteNotFound):
        RS.resolve_route(doc, "no-such-route")


def test_ambiguity_raises_with_candidates_and_cli_exits_2(tmp_path, capsys, two_routes):
    # final_report is the default route of neither, so a person has to choose.
    doc = _work(work_type="final_report")
    with pytest.raises(RS.AmbiguousRoute) as ei:
        RS.resolve_route(doc)
    assert ei.value.candidates == ["nriis-proposal", "concept-note"]
    assert "never picks a route" in str(ei.value)
    P.save(doc, tmp_path / "work.yaml")
    assert main(["build", str(tmp_path), "--as-of", AS_OF]) == 2
    assert "choose one with --route" in capsys.readouterr().err
    assert not (tmp_path / "build").exists()
    with pytest.raises(ValueError):
        api.build(tmp_path, as_of=AS_OF)
    with pytest.raises(ValueError):
        api.validate(tmp_path, as_of=AS_OF)
    # an explicit route still builds
    assert main(["build", str(tmp_path), "--route", "nriis-proposal", "--as-of", AS_OF]) == 0
    assert [p.name for p in (tmp_path / "build").iterdir()] == ["NRIIS_SUBMISSION.md"]


def test_declared_routes_are_honoured_before_the_work_type_default(tmp_path, capsys, two_routes):
    # research_proposal defaults to nriis-proposal, but the person declared only concept-note.
    doc = _work(work_type="research_proposal", routing={"declared_routes": ["concept-note"]})
    assert RS.resolve_route(doc) == "concept-note"
    P.save(doc, tmp_path / "work.yaml")
    assert main(["build", str(tmp_path), "--as-of", AS_OF]) == 0
    assert [p.name for p in (tmp_path / "build").iterdir()] == ["RESEARCH_CONCEPT_NOTE.md"]


def test_several_declared_routes_without_default_raise_with_the_declared_list(tmp_path, capsys, two_routes):
    doc = _work(work_type="research_proposal",
                routing={"declared_routes": ["nriis-proposal", "concept-note"]})
    with pytest.raises(RS.AmbiguousRoute) as ei:
        RS.resolve_route(doc)
    assert ei.value.candidates == ["nriis-proposal", "concept-note"]
    assert "never picks a route" in str(ei.value)
    P.save(doc, tmp_path / "work.yaml")
    assert main(["build", str(tmp_path), "--as-of", AS_OF]) == 2
    assert "choose one with --route" in capsys.readouterr().err
    assert not (tmp_path / "build").exists()
    # default_route and an explicit --route still decide
    doc["routing"]["default_route"] = "concept-note"
    assert RS.resolve_route(doc) == "concept-note"
    assert RS.resolve_route(doc, "nriis-proposal") == "nriis-proposal"


def test_explicit_route_outside_declared_routes_is_an_info_finding(two_routes):
    doc = _work(work_type="research_proposal", routing={"declared_routes": ["concept-note"]})
    from grantthai.validators import engine as E
    out = E.run(doc, None, AS_OF, route="nriis-proposal")
    rt3 = [f for f in out.findings if f.rule_id == "RT003"]
    assert len(rt3) == 1 and rt3[0].severity == "INFO"
    out = E.run(doc, None, AS_OF, route="concept-note")
    assert not [f for f in out.findings if f.rule_id == "RT003"]


def test_unknown_route_exits_2(capsys):
    assert main(["route", "build", "--route", "no-such-route", str(LECTURER), "--as-of", AS_OF]) == 2
    assert "unknown route" in capsys.readouterr().err


def test_route_without_renderer_writes_nothing(tmp_path, capsys, monkeypatch):
    from grantthai import render
    monkeypatch.setitem(render.RENDERERS, "concept-note", "grantthai.render._no_such_renderer")
    shutil.copy(LECTURER, tmp_path / "project.yaml")
    assert main(["build", str(tmp_path), "--route", "concept-note", "--as-of", AS_OF]) == 2
    assert "nothing was written" in capsys.readouterr().err
    assert not (tmp_path / "build").exists()


# hash, migrate ------------------------------------------------------------

def test_routing_is_outside_content_sha256_and_work_type_inside():
    doc = _work()
    base = content_sha256(doc)
    doc["routing"] = {"declared_routes": ["nriis-proposal", "concept-note"], "default_route": "concept-note",
                      "sub_profiles": {"nriis-proposal": "research@sd1-2566"}}
    assert content_sha256(doc) == base
    doc["work_type"] = "concept_note"
    assert content_sha256(doc) != base
    assert content_sha256(P.load(LECTURER)) == content_sha256(copy.deepcopy(P.load(LECTURER)))


def test_migrate_dry_run_writes_nothing_and_reports_stale_gates(tmp_path):
    shutil.copy(DEMO, tmp_path / "project.yaml")
    before = (tmp_path / "project.yaml").read_bytes()
    res = api.migrate(tmp_path / "project.yaml", rename=True, dry_run=True)
    assert res["written"] is None and res["changed"] and isinstance(res["stale_gates"], list)
    assert res["content_sha256_before"] != res["content_sha256_after"]
    assert (tmp_path / "project.yaml").read_bytes() == before and not (tmp_path / "work.yaml").exists()
    res = api.migrate(tmp_path / "project.yaml")
    new = P.load(tmp_path / "project.yaml")
    assert new["schema_version"] == P.WORK_SCHEMA_VERSION and "form_profile" not in new
    assert new["routing"]["sub_profiles"] == {"nriis-proposal": "ff_full_proposal@nriis-2570"}
    assert new["work_id"] == P.load(DEMO)["project_id"] and new["work_type"] == "research_proposal"
    assert P.schema_errors(new, P.WORK_SCHEMA_ID) == []
    assert api.migrate(tmp_path / "project.yaml")["changed"] is False


def test_migrate_reports_a_current_gate_going_stale(tmp_path):
    from grantthai.review import records as RR
    doc = P.load(LECTURER)
    gate = RR.GATES[0]
    doc["review_records"] = [{"gate_id": gate, "reviewer_name": "FICTIONAL Reviewer", "reviewer_role": "lecturer",
                              "independence": "self", "date": "2026-09-25", "content_sha256": content_sha256(doc)}]
    assert RR.gate_states(doc)[gate]["state"] == "current"
    P.save(doc, tmp_path / "project.yaml")
    res = api.migrate(tmp_path / "project.yaml", dry_run=True)
    assert res["stale_gates"] == [gate]


def test_init_writes_a_valid_work_yaml(tmp_path, two_routes):
    assert main(["init", str(tmp_path / "work.yaml"), "--work-type", "concept_note"]) == 0
    doc = P.load(tmp_path / "work.yaml")
    assert doc["schema_version"] == "0.3.0-draft" and doc["work_type"] == "concept_note"
    assert "routing" not in doc and "fund_binding" not in doc
    assert P.schema_errors(doc, P.WORK_SCHEMA_ID) == []
    seeded = {r["field_id"] for r, _ in P.iter_records(doc)}
    assert seeded == set(R.load("concept-note").required_fields)
    assert RS.resolve_route(doc) == "concept-note"
    assert main(["init", str(tmp_path / "work.yaml")]) == 2          # refuses to overwrite
    legacy = api.new_project("T-1")
    assert legacy["schema_version"] == "0.2.0-draft"                  # the 0.2 API is unchanged


# route-scoped validation -------------------------------------------------

def test_concept_note_route_runs_no_fund_budget_or_workplan_rules():
    rep = api.check_route(LECTURER, "concept-note", as_of=AS_OF)
    ids = [f["rule_id"] for f in rep["findings"]]
    assert not [i for i in ids if i.startswith(("F", "B", "W", "T", "ELIG", "ART"))], ids
    rt2 = [f for f in rep["findings"] if f["rule_id"] == "RT002"]
    assert len(rt2) == 1 and rt2[0]["severity"] == "INFO" and "W101" in rt2[0]["message_en"]
    assert rep["fund_profile"] == ""
    from grantthai.validators import engine as E
    res = E.run(P.load(LECTURER), LECTURER.parent, AS_OF, route="concept-note")
    assert res.route == "concept-note" and res.submittable is False
    assert any("never submittable" in h for h in res.hold_reasons)
    assert P.schema_errors(rep, P.REPORT_SCHEMA_ID) == []


def test_rt001_when_the_route_was_not_made_for_the_work_type():
    doc = _work(work_type="final_report")
    rep = api.validate(doc, route="nriis-proposal", as_of=AS_OF)
    rt1 = [f for f in rep["findings"] if f["rule_id"] == "RT001"]
    assert len(rt1) == 1 and rt1[0]["severity"] == "INFO"
    assert not [f for f in api.validate(LECTURER, as_of=AS_OF)["findings"] if f["rule_id"] == "RT001"]


def test_work_yaml_validates_against_the_work_schema():
    doc = _work()
    rep = api.validate(doc, route="nriis-proposal", as_of=AS_OF)
    assert not [f for f in rep["findings"] if f["rule_id"] == "SCHEMA"]
    assert rep["project_id"] == doc["work_id"]
    bad = _work(work_type="poem")
    rep = api.validate(bad, route="nriis-proposal", as_of=AS_OF)
    assert any(f["rule_id"] == "SCHEMA" and f["message_en"].startswith("work.yaml") for f in rep["findings"])


def test_route_list_and_explain_router_findings(capsys):
    rows = api.list_routes()
    assert [r["id"] for r in rows] == ["nriis-proposal", "academic-article", "concept-note"]
    nriis = rows[0]
    assert nriis["output_filename"] == "NRIIS_SUBMISSION.md" and nriis["ready_flag"] == "submittable"
    assert main(["route", "list"]) == 0
    assert "nriis-proposal" in capsys.readouterr().out
    assert api.explain("RT002")["severity"] == "INFO"


def test_fields_by_route_placement_then_not_placed():
    rows = api.list_fields(route="concept-note")
    placed = [r["field_id"] for r in rows if r["tab"] != api.NOT_PLACED]
    assert placed[:2] == ["CORE.GENERAL.TITLE_TH", "CORE.GENERAL.TITLE_EN"]
    assert len(placed) == 19 and len(rows) == len(P.registry())
    assert api.list_fields() == api.list_fields(route="nriis-proposal")
