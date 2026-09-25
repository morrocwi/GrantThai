"""tests/test_schema_lint.py — schema-lint validates instances and the chain
contract, not only parsing."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "ci"))

import check_schema_lint as lint  # noqa: E402

GUARD = str(ROOT / "tools/ci/check_schema_lint.py")


def run(root):
    return subprocess.run([sys.executable, GUARD, "--root", str(root)], capture_output=True, text=True)


def test_schema_lint_passes_on_repo():
    r = run(ROOT)
    assert r.returncode == 0, r.stdout + r.stderr


def test_schema_lint_fails_on_parse_errors():
    assert run(ROOT / "tests/fixtures/negative/schema_lint").returncode != 0


def test_schema_lint_fails_on_invalid_instances():
    r = run(ROOT / "tests/fixtures/negative/schema_instance")
    assert r.returncode != 0
    assert "must equal its path id" in r.stdout
    assert "fund_binding/fund_profile_id" in r.stdout
    # route data files are instances too (placement, sub-profile)
    assert "routes/bad-route/placement.yaml" in r.stdout and "not_placed_policy" in r.stdout
    assert "routes/bad-route/sub_profiles/bad-sub.yaml" in r.stdout
    assert "must equal its file name" in r.stdout


def test_chain_check_catches_undeclared_duplicate_and_cycle():
    bad = {
        "nodes": {"core": ["A", "B"]},
        "edges": {"causal": [["A", "B"], ["A", "B"], ["B", "A"], ["A", "Ghost"]]},
        "required_stages": ["A"],
    }
    msgs = "\n".join(lint.check_chain(bad))
    assert "undeclared node Ghost" in msgs
    assert "duplicate causal edge" in msgs
    assert "causal cycle" in msgs


def test_real_chain_is_clean():
    import yaml
    chain = yaml.safe_load((ROOT / "spec/common/chain.yaml").read_text(encoding="utf-8"))
    assert lint.check_chain(chain) == []


def _contracts():
    import json
    import yaml
    structured = json.loads((ROOT / "spec/registry/structured_fields.schema.json").read_text(encoding="utf-8"))
    fields = [json.loads(x) for x in (ROOT / "registry/fields.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    chain = yaml.safe_load((ROOT / "spec/common/chain.yaml").read_text(encoding="utf-8"))
    return structured, fields, chain


def test_every_structured_field_has_a_contract():
    structured, fields, chain = _contracts()
    assert lint.check_structured(structured, fields, chain) == []
    structured_ids = {r["field_id"] for r in fields if r["type"] in lint.STRUCTURED_TYPES}
    assert structured_ids and structured_ids <= set(structured["$defs"])


def test_structured_contract_check_catches_gaps():
    import copy
    structured, fields, chain = _contracts()
    bad = copy.deepcopy(structured)
    del bad["$defs"]["BUDGET.PLAN.ITEMS"]                                       # missing contract
    acts = bad["$defs"]["WORK.PLAN.ACTIVITIES"]["items"]["properties"]
    del acts["objective_ids"]["x-grantthai-ref"]                                # unannotated reference
    acts["output_ids"]["x-grantthai-ref"]["direction"] = "target_to_source"     # Output -> Activity: against the chain
    bad["$defs"]["RESULTS.CHAIN.OUTPUTS"]["items"]["x-grantthai-node"]["id_prefix"] = "ACT"  # prefix clash
    msgs = "\n".join(lint.check_structured(bad, fields, chain))
    assert "BUDGET.PLAN.ITEMS (type array<object>) has no value schema" in msgs
    assert "objective_ids: *_id/*_ids property needs x-grantthai-ref" in msgs
    assert "causal edge Output -> Activity runs against" in msgs
    assert "id prefix ACT already used" in msgs


def test_schema_lint_catches_broken_links_sources_and_stale_review():
    out = run(ROOT / "tests/fixtures/negative/schema_instance").stdout
    for needle in ("must be under chain.Gap", "(S002)", "node id ACT2 is used more than once (S007)",
                   "OBJ9: no node has this id (S006)", "node is not one of the key's targets (S006)",
                   "causal cycle", "file does not exist (S008)", "review_records/0 is stale"):
        assert needle in out, needle
