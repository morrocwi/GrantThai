"""tests/test_routes_schema.py — the router's contracts hold: routes/INDEX.yaml
is consistent, every shipped route.yaml / placement.yaml validates against
spec/routes/*.schema.json, ids and output filenames are unique, and the
work.yaml 0.3 schema is a superset of the frozen project.yaml 0.2 schema."""
import copy
import json
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "spec"


def _schemas():
    resources, schemas = [], {}
    for path in sorted(SPEC.rglob("*.schema.json")):
        sch = json.loads(path.read_text(encoding="utf-8"))
        schemas[path.relative_to(SPEC).as_posix()] = sch
        resources.append((sch["$id"], Resource.from_contents(sch)))
    return Registry().with_resources(resources), schemas


REGISTRY, SCHEMAS = _schemas()
INDEX = yaml.safe_load((ROOT / "routes/INDEX.yaml").read_text(encoding="utf-8"))
FIELD_IDS = {json.loads(x)["field_id"] for x in (ROOT / "registry/fields.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()}


def errors(schema_rel, instance):
    v = Draft202012Validator(SCHEMAS[schema_rel], registry=REGISTRY)
    return [f"{'/'.join(str(p) for p in e.absolute_path) or '(root)'}: {e.message[:160]}" for e in v.iter_errors(instance)]


def shipped_routes():
    for entry in INDEX["routes"]:
        path = ROOT / entry["path"]
        if entry["status"] == "planned":
            assert not path.exists(), f"{entry['id']} is planned but {entry['path']} exists: change its status"
            continue
        assert path.exists(), f"{entry['id']}: {entry['path']} missing"
        yield entry, yaml.safe_load(path.read_text(encoding="utf-8"))


def test_route_schemas_are_valid_json_schema():
    for rel in ("routes/route.schema.json", "routes/placement.schema.json", "routes/sub_profile.schema.json", "work/work.schema.json"):
        Draft202012Validator.check_schema(SCHEMAS[rel])


def test_index_ids_paths_and_filenames_are_unique():
    ids = [r["id"] for r in INDEX["routes"]]
    names = [r["output_filename"] for r in INDEX["routes"]]
    paths = [r["path"] for r in INDEX["routes"]]
    assert len(ids) == len(set(ids)) and len(names) == len(set(names)) and len(paths) == len(set(paths))
    assert set(ids) == {"nriis-proposal", "academic-article", "concept-note"}
    for r in INDEX["routes"]:
        assert r["path"] == f"routes/{r['id']}/route.yaml"
        assert r["status"] in ("draft", "planned", "stable", "deprecated")


def test_every_shipped_route_validates_and_matches_index():
    seen_templates, seen_files = {}, {}
    for entry, route in shipped_routes():
        assert errors("routes/route.schema.json", route) == [], entry["id"]
        assert route["id"] == entry["id"]
        assert route["version"] == entry["version"]
        assert route["output"]["filename"] == entry["output_filename"]
        assert (ROOT / route["output"]["template"]).exists(), route["output"]["template"]
        # one template per route, one route per template, one filename per route
        assert route["output"]["template"] not in seen_templates
        seen_templates[route["output"]["template"]] = entry["id"]
        assert route["output"]["filename"] not in seen_files
        seen_files[route["output"]["filename"]] = entry["id"]
        # the contract exists or is declared not-yet-created in spec/INDEX.yaml
        spec_index = yaml.safe_load((ROOT / "spec/INDEX.yaml").read_text(encoding="utf-8"))
        pending = {e["path"] for e in spec_index.get("not_yet_created") or []}
        assert (ROOT / route["output"]["contract"]).exists() or route["output"]["contract"] in pending
        if route["placement"]:
            assert (ROOT / route["placement"]).exists()
        if route["sub_profiles"]:
            assert (ROOT / route["sub_profiles"]["dir"]).is_dir()
        if isinstance(route["required_fields"], list):
            assert set(route["required_fields"]) <= FIELD_IDS
        # readiness never claims merit
        assert route["readiness"]["ready_flag"] in ("submittable", "manuscript_ready")


def test_nriis_route_wraps_existing_assets_unchanged():
    route = yaml.safe_load((ROOT / "routes/nriis-proposal/route.yaml").read_text(encoding="utf-8"))
    assert route["output"]["filename"] == "NRIIS_SUBMISSION.md"
    assert route["output"]["template"] == "templates/nriis_submission.md.j2"
    assert route["output"]["contract"] == "spec/output/nriis-submission.contract.md"
    assert route["placement"] == "mappings/nriis/section_to_tab.yaml"
    assert route["sub_profiles"] == {"dir": "mappings/nriis/form_profiles", "default": None}
    assert route["required_fields"] == "registry"
    assert route["needs_fund_binding"] is True
    assert route["readiness"]["ready_flag"] == "submittable"
    assert "output_kind: primary_submission" in (ROOT / route["output"]["template"]).read_text(encoding="utf-8")
    from grantthai.render import submission
    assert route["output"]["renderer_version"] == submission.RENDERER_VERSION


def test_concept_note_route_is_never_submittable_and_needs_no_fund():
    route = yaml.safe_load((ROOT / "routes/concept-note/route.yaml").read_text(encoding="utf-8"))
    assert route["needs_fund_binding"] is False
    assert route["readiness"]["always_hold"] is True
    assert not ({"B", "F", "ELIG", "T", "W"} & set(route["rules"]["include_families"]))
    assert "route_notice" in route["disclosure_blocks"] and route["route_notice_en"]


def test_concept_note_placement_validates_and_equals_its_body_selector():
    placement = yaml.safe_load((ROOT / "routes/concept-note/placement.yaml").read_text(encoding="utf-8"))
    assert errors("routes/placement.schema.json", placement) == []
    assert placement["route"] == "concept-note"
    placed = [f for s in placement["sections"] for f in s["fields"]]
    assert len(placed) == len(set(placed))
    assert set(placed) <= FIELD_IDS
    body = INDEX["partition"]["body"]["concept-note"]["field_ids"]
    assert set(placed) == set(body)
    assert set(placed) <= set(INDEX["partition"]["shared_core"])


def test_partition_declaration_is_well_formed():
    part = INDEX["partition"]
    shared = part["shared_core"]
    assert len(shared) == 39 and len(set(shared)) == 39
    assert set(shared) <= FIELD_IDS
    assert part["route_namespaces"] == {"ARTICLE": "academic-article"}
    assert set(part["body"]) == {r["id"] for r in INDEX["routes"]}


def test_route_schema_rejects_bad_routes():
    good = yaml.safe_load((ROOT / "routes/concept-note/route.yaml").read_text(encoding="utf-8"))
    bad = copy.deepcopy(good)
    bad["readiness"]["ready_flag"] = "accepted"              # readiness is structural, never a judgement
    assert errors("routes/route.schema.json", bad)
    bad = copy.deepcopy(good)
    bad["disclosure_blocks"] = ["notice", "route_notice"]
    del bad["route_notice_en"]                                # route_notice needs its text
    assert errors("routes/route.schema.json", bad)
    bad = copy.deepcopy(good)
    bad["output"]["filename"] = "out.txt"
    assert errors("routes/route.schema.json", bad)
    bad = copy.deepcopy(good)
    bad["accepts_work_types"] = ["blog_post"]
    assert errors("routes/route.schema.json", bad)


def test_sub_profile_schema_forces_needs_verification():
    sp = {"schema": "grantthai.sub_profile.v0", "id": "x", "route": "academic-article", "version": "0.1.0-draft",
          "status": "NEEDS_VERIFICATION", "title_en": "x", "title_th": "NEEDS_INPUT",
          "languages": {"title": ["en"], "abstract": ["en"], "keywords": ["en"]},
          "requirements": [{"item": "keyword_count_min", "value": 3, "status": "NEEDS_VERIFICATION", "basis": "proposed_default"}],
          "notes": ["no venue fact is GrantThai's own"]}
    assert errors("routes/sub_profile.schema.json", sp) == []
    bad = copy.deepcopy(sp)
    bad["status"] = "VERIFIED"
    assert errors("routes/sub_profile.schema.json", bad)
    bad = copy.deepcopy(sp)
    bad["requirements"][0]["basis"] = "researcher_supplied_source"     # then a source is required
    assert errors("routes/sub_profile.schema.json", bad)


# ---- work.yaml 0.3 is a superset of project.yaml 0.2 ----

def _legacy_examples():
    return sorted((ROOT / "examples").glob("*/project.yaml")) + sorted((ROOT / "tests/fixtures/positive").glob("*.yaml"))


@pytest.mark.parametrize("path", _legacy_examples(), ids=lambda p: p.parent.name + "/" + p.name)
def test_every_legacy_project_validates_as_work_after_only_the_version_bump(path):
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert errors("project/project.schema.json", doc) == []
    up = copy.deepcopy(doc)
    up["schema_version"] = "0.3.0-draft"
    assert errors("work/work.schema.json", up) == []


def test_work_schema_keeps_every_project_key_and_adds_the_router_keys():
    p = SCHEMAS["project/project.schema.json"]
    w = SCHEMAS["work/work.schema.json"]
    assert set(p["properties"]) <= set(w["properties"])
    assert set(w["properties"]) - set(p["properties"]) == {"work_id", "work_type", "routing"}
    assert "fund_binding" not in w["required"] and "fund_binding" in p["required"]
    assert w["properties"]["schema_version"]["const"] == "0.3.0-draft"
    assert w["$defs"]["ai_use_declaration"] == p["$defs"]["ai_use_declaration"]
    assert w["$defs"]["work_type"]["enum"] == SCHEMAS["routes/route.schema.json"]["$defs"]["work_type"]["enum"]


def test_work_schema_accepts_work_id_or_project_id_and_a_routing_block():
    base = {"schema_version": "0.3.0-draft", "mode": "expert", "fields": [], "chain": {}}
    assert errors("work/work.schema.json", base), "needs work_id or project_id"
    doc = dict(base, work_id="w1", work_type="academic_article",
               routing={"declared_routes": ["academic-article", "nriis-proposal"], "default_route": "academic-article",
                        "sub_profiles": {"academic-article": "thai-journal", "nriis-proposal": "research@sd1-2566"}})
    assert errors("work/work.schema.json", doc) == []
    assert errors("work/work.schema.json", dict(base, project_id="p1")) == []
    assert errors("work/work.schema.json", dict(base, work_id="w1", work_type="poem"))
    assert errors("work/work.schema.json", dict(base, work_id="w1", routing={"default_route": "Bad Route"}))
    assert errors("work/work.schema.json", dict(base, work_id="w1", routing={"chosen_by": "ai"}))
