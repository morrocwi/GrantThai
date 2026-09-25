"""tests/test_example_project.py — the FICTIONAL worked example
examples/lecturer-no-ai/project.yaml is complete enough for every v0.1 rule
that reads links, sums, budget arithmetic, sources or the chain graph, and
those rules can be computed from the contracts alone
(spec/registry/structured_fields.schema.json,
spec/common/links-and-sources.md). This is a readout of the contract, not
the v0.1 validator."""
import json
import sys
from decimal import Decimal
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from grantthai.core import links  # noqa: E402
from grantthai.core.object_hash import load_project_text  # noqa: E402

EXAMPLE = ROOT / "examples/lecturer-no-ai/project.yaml"
STRUCTURED = json.loads((ROOT / "spec/registry/structured_fields.schema.json").read_text(encoding="utf-8"))
CHAIN = yaml.safe_load((ROOT / "spec/common/chain.yaml").read_text(encoding="utf-8"))
REGISTRY = [json.loads(x) for x in (ROOT / "registry/fields.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
RULES = yaml.safe_load((ROOT / "validators/rules.yaml").read_text(encoding="utf-8"))["rules"]


def q(x):
    d = x if isinstance(x, Decimal) else Decimal(repr(x))
    return d.quantize(Decimal("0.01"))


def records(doc):
    return {r["field_id"]: r for r, _ in links.iter_records(doc)}


def items(doc, fid):
    return records(doc)[fid]["value"]


def setup():
    doc = load_project_text(EXAMPLE.read_text(encoding="utf-8"))
    return doc, links.derive(doc, STRUCTURED, CHAIN)


def incoming(rep, node, from_pred):
    return any(b == node and k == "causal" and from_pred(a) for a, b, k in rep.edges)


def outgoing(rep, node, to_pred):
    return any(a == node and k == "causal" and to_pred(b) for a, b, k in rep.edges)


def in_field(rep, fid):
    return lambda nid: nid in rep.nodes and rep.nodes[nid].field_id == fid


def test_structure_rules_S001_S004_S006_S007_S008():
    doc, rep = setup()
    recs = records(doc)
    for r in REGISTRY:  # S001: every required registry field present and non-null
        if r["required"]:
            assert r["field_id"] in recs and recs[r["field_id"]]["value"] is not None, r["field_id"]
    ids = [r["field_id"] for r, _ in links.iter_records(doc)]
    assert len(ids) == len(set(ids))                        # S004
    assert rep.unresolved == []                             # S006
    assert rep.duplicates == []                             # S007
    assert links.resolve_sources(doc, EXAMPLE.parent) == []  # S008


def test_research_logic_R001_to_R007():
    doc, rep = setup()
    recs = records(doc)
    assert recs["CORE.RESEARCH.PROBLEM"]["source_ids"]                                   # R001
    pks = [a for a, b, k in rep.edges if b == "CORE.RESEARCH.GAP" and rep.nodes[a].chain_key == "PriorKnowledge"]
    assert pks and all(recs[p].get("source_ids") for p in pks)                          # R002
    assert incoming(rep, "CORE.RESEARCH.RQ.PRIMARY", lambda a: a == "CORE.RESEARCH.GAP")  # R003
    rq = lambda a: a in ("CORE.RESEARCH.RQ.PRIMARY", "CORE.RESEARCH.RQ.SECONDARY")
    design = in_field(rep, "METHOD.PLAN.DESIGN")
    for o in items(doc, "CORE.RESEARCH.OBJECTIVES"):
        assert incoming(rep, o["id"], rq)                                                # R004
        assert outgoing(rep, o["id"], design)                                            # R005
    phases = [p["id"] for p in items(doc, "METHOD.PLAN.DESIGN").get("phases") or []] or ["METHOD.PLAN.DESIGN"]
    for p in phases:
        assert outgoing(rep, p, in_field(rep, "METHOD.PLAN.DATA_COLLECTION"))            # R006
    assert incoming(rep, "METHOD.PLAN.ANALYSIS", in_field(rep, "METHOD.PLAN.DATA_COLLECTION"))  # R007


def test_workplan_budget_team_W_B_T():
    doc, rep = setup()
    acts = items(doc, "WORK.PLAN.ACTIVITIES")
    obj_or_design = lambda a: in_field(rep, "CORE.RESEARCH.OBJECTIVES")(a) or in_field(rep, "METHOD.PLAN.DESIGN")(a)
    team = {m["id"] for m in items(doc, "PROFILE.TEAM.MEMBERS")}
    for a in acts:
        assert incoming(rep, a["id"], obj_or_design)                                     # W001
        assert set(a.get("responsible_person_ids") or []) & team                        # W002
    assert sum(q(a["weight_percent"]) for a in acts) == q(100)                           # W003
    for o in items(doc, "RESULTS.CHAIN.OUTPUTS"):
        assert incoming(rep, o["id"], in_field(rep, "WORK.PLAN.ACTIVITIES"))            # W004
    lines = items(doc, "BUDGET.PLAN.ITEMS")
    for b in lines:
        assert incoming(rep, b["id"], in_field(rep, "WORK.PLAN.ACTIVITIES"))            # B001
        assert q(b["line_total"]) == q(Decimal(repr(b["quantity"])) * Decimal(repr(b["persons_or_items"]))
                                      * Decimal(repr(b["times_or_months"])) * Decimal(repr(b["unit_price"])))  # B002
    total = sum(q(b["line_total"]) for b in lines)
    recs = records(doc)
    for fid in ("BUDGET.PLAN.TOTAL", "CORE.GENERAL.REQUESTED_BUDGET", "CORE.GENERAL.TOTAL_BUDGET"):
        assert q(recs[fid]["value"]) == total                                            # B002
    members = items(doc, "PROFILE.TEAM.MEMBERS")
    assert sum(q(m["contribution_percent"]) for m in members) == q(100)                  # T001
    assert [m["project_role"] for m in members].count("PI") == 1                         # T002


def test_chain_CH001_CH002():
    doc, rep = setup()
    assert links.find_cycle(rep.causal_edges()) is None                                  # CH001
    for stage in CHAIN["required_stages"]:                                               # CH002
        assert any(r.get("value") is not None for r in doc["chain"].get(stage) or []), stage
    assert any(k == "causal" for _, _, k in rep.edges)


def test_link_rules_read_chain_edges():
    by_id = {r["id"]: r for r in RULES}
    for rid in ("R002", "R003", "R004", "R005", "R006", "R007", "W001", "W004", "B001", "CH001"):
        assert "project:chain_edges" in by_id[rid]["inputs"], rid
    for rid in ("R001", "R002", "S008"):
        assert "project:sources" in by_id[rid]["inputs"], rid


def test_cycle_and_bad_reference_are_detected():
    doc, _ = setup()
    acts = records(doc)["WORK.PLAN.ACTIVITIES"]["value"]
    acts[0]["depends_on_activity_ids"] = ["ACT3"]            # ACT1 <- ACT3 <- ACT2 <- ACT1
    acts[1]["objective_ids"].append("OUT1")                  # wrong target field
    rep = links.derive(doc, STRUCTURED, CHAIN)
    assert links.find_cycle(rep.causal_edges()) is not None
    assert any(r.target == "OUT1" for r, _ in rep.unresolved)
