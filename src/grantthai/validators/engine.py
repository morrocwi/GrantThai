"""grantthai.validators.engine — the deterministic v0.1 validator.

Reads the rule catalog `validators/rules.yaml` for ids and severities
(nothing is hardcoded here about a fund: thresholds come only from the
bound fund profile). Every rule in the catalog is accounted for in every
report: a rule that v0.1 evaluates yields BLOCK/REVIEW findings when it
fails; a rule that v0.1 does NOT evaluate yields exactly one INFO finding
saying so and why (no silent skip).

Report-only: running the validator never changes a status in project.yaml.
"""
from __future__ import annotations

import datetime as _dt
import re
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from grantthai.core import links
from grantthai.core import project as P
from grantthai.core.object_hash import content_sha256, state_sha256

# Rules whose ids ship in v0.1 but which this build does not evaluate, with
# the reason printed in their INFO finding.
V01_NOT_EVALUATED = {
    "B003": "budget-rate rules: spec/fund/fund-profile.schema.json has no rate slot yet, so no rate can be checked",
    "B004": "prohibited costs: spec/fund/fund-profile.schema.json has no prohibited-cost slot yet, so this rule cannot fire",
    "F004": "historical rule reuse needs rule lineage across profile versions, which v0.1 does not track (F003 still blocks a non-ACTIVE profile)",
}

TRUST_ORDER = ["FICTIONAL", "COMMUNITY_EXTRACTED", "HUMAN_VERIFIED", "SECOND_CHECKED"]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2})?$")
CENT = Decimal("0.01")


@dataclass
class Finding:
    rule_id: str
    severity: str
    message_en: str
    field_ids: list = field(default_factory=list)
    next_step_en: str = ""

    def as_dict(self) -> dict:
        d = {"rule_id": self.rule_id, "severity": self.severity}
        if self.field_ids:
            d["field_ids"] = list(self.field_ids)
        d["message_en"] = self.message_en
        if self.next_step_en:
            d["next_step_en"] = self.next_step_en
        return d


@dataclass
class Result:
    """Everything the renderer needs besides the project itself."""
    report: dict
    findings: list
    link_report: Any
    source_problems: list
    fund_profile: dict | None
    fund_profile_id: str | None
    hold_reasons: list
    stale_rules: list
    trust_level: str
    real_world_verified: bool
    submittable: bool


def q(x) -> Decimal:
    d = x if isinstance(x, Decimal) else Decimal(repr(x))
    return d.quantize(CENT)


def _num(x) -> Decimal | None:
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        return None
    try:
        return Decimal(repr(x))
    except InvalidOperation:
        return None


class _Ctx:
    def __init__(self, raw: dict, project_dir: Path | None, as_of: str):
        self.raw = raw
        self.doc = P.normalized(raw)
        self.project_dir = project_dir
        self.as_of = as_of
        self.reg = P.registry_by_id()
        self.structured = P.schema(P.STRUCTURED_SCHEMA_ID)
        self.rep = links.derive(self.doc, self.structured, P.chain_config())
        self.recs = P.records_by_id(self.doc)
        self.source_problems = links.resolve_sources(self.doc, project_dir)
        self.fund, self.fund_id, self.fund_problems = P.load_fund_profile(self.doc)
        self.findings: list[Finding] = []
        rules = P.rules_catalog()["rules"]
        self.rules = {r["id"]: r for r in rules}
        self.rule_order = [r["id"] for r in rules]

    # helpers ---------------------------------------------------------
    def add(self, rule_id: str, msg: str, field_ids=(), next_step: str = ""):
        sev = self.rules[rule_id]["severity"] if rule_id in self.rules else "BLOCK"
        self.findings.append(Finding(rule_id, sev, msg, list(field_ids), next_step))

    def value(self, fid):
        rec = self.recs.get(fid)
        return None if rec is None else rec.get("value")

    def items(self, fid) -> list:
        v = self.value(fid)
        return [x for x in v if isinstance(x, dict)] if isinstance(v, list) else []

    def in_field(self, fid):
        return lambda nid: nid in self.rep.nodes and self.rep.nodes[nid].field_id == fid

    def incoming(self, node, pred):
        return any(b == node and k == "causal" and pred(a) for a, b, k in self.rep.edges)

    def outgoing(self, node, pred):
        return any(a == node and k == "causal" and pred(b) for a, b, k in self.rep.edges)

    def resolvable_sources(self, fid) -> list:
        rec = self.recs.get(fid) or {}
        bad = {sid for h, sid, _ in self.source_problems if h == fid}
        return [s for s in rec.get("source_ids") or [] if s not in bad]


# --------------------------------------------------------------------------
# S — structure
# --------------------------------------------------------------------------

def _type_ok(rtype: str, v: Any) -> bool:
    if rtype in ("string", "text", "rich_text", "enum", "reference", "enum|string"):
        return isinstance(v, str)
    if rtype == "datetime":
        return isinstance(v, str) and bool(DATE_RE.match(v))
    if rtype == "integer":
        return isinstance(v, int) and not isinstance(v, bool)
    if rtype == "money":
        d = _num(v)
        return d is not None and d >= 0 and d.as_tuple().exponent >= -2
    if rtype == "boolean":
        return isinstance(v, bool)
    if rtype == "boolean|string":
        return isinstance(v, (bool, str))
    if rtype in ("array<string>", "array<text>"):
        return isinstance(v, list) and all(isinstance(x, str) for x in v)
    if rtype == "array<object>":
        return isinstance(v, list)
    if rtype == "object":
        return isinstance(v, dict)
    if rtype == "rich_text|object":
        return isinstance(v, (str, dict))
    return True


def _structure(c: _Ctx):
    ids = [r.get("field_id") for r, _ in P.iter_records(c.doc)]
    # S001 required fields
    for r in P.registry():
        if r.get("required") and c.value(r["field_id"]) is None:
            c.add("S001", f"Required field {r['field_id']} ({r['label_en']}) is missing or NEEDS_INPUT.",
                  [r["field_id"]], f"Fill it: grantthai set {r['field_id']} <value> (or edit project.yaml).")
    for rec, _ in P.iter_records(c.doc):
        fid, v = rec.get("field_id"), rec.get("value")
        reg = c.reg.get(fid)
        if reg is None or v is None:
            continue
        rtype = reg["type"]
        # S002 type / structured contract
        if not _type_ok(rtype, v):
            c.add("S002", f"{fid}: value does not match registry type {rtype}.", [fid],
                  "Correct the value's type (spec/registry/types.yaml).")
        elif rtype in ("array<object>", "object", "rich_text|object") and fid in c.structured.get("$defs", {}) \
                and not (rtype == "rich_text|object" and isinstance(v, str)):
            errs = P.schema_errors(v, P.STRUCTURED_SCHEMA_ID, "/$defs/" + fid)
            for e in errs:
                c.add("S002", f"{fid}: {e}", [fid],
                      f"Fix the value against spec/registry/structured_fields.schema.json#/$defs/{fid}.")
        # S003 allowed values
        allowed = reg.get("allowed_values")
        if rtype in ("enum", "reference") and isinstance(allowed, list) and isinstance(v, str) and v not in allowed:
            c.add("S003", f"{fid}: {v!r} is not one of the allowed values {allowed}.", [fid],
                  "Choose one of the listed values.")
        # S004 cardinality
        if reg.get("cardinality") == "1..N" and isinstance(v, list) and len(v) == 0:
            c.add("S004", f"{fid}: needs at least one item (cardinality 1..N).", [fid], "Add at least one item.")
    # S004 duplicate records
    for fid in sorted({f for f in ids if isinstance(f, str) and f in c.reg and ids.count(f) > 1}):
        c.add("S004", f"{fid} appears as {ids.count(fid)} records; a registry field is at most one record.",
              [fid], "Merge the duplicate records into one.")
    # S005 conditional fields
    for r in P.registry():
        for dep in r.get("dependencies") or []:
            if "=" not in dep:
                continue
            cond_fid, cond_val = dep.split("=", 1)
            cur = c.value(cond_fid)
            expected = {"true": True, "false": False}.get(cond_val, cond_val)
            active = cur == expected
            filled = c.value(r["field_id"]) not in (None, "", [])
            if active and not filled:
                c.add("S005", f"{r['field_id']} is required because {dep}, but it is empty.", [r["field_id"], cond_fid],
                      f"Fill {r['field_id']}.")
            if not active and filled:
                c.add("S005", f"{r['field_id']} is filled, but its condition {dep} is false.", [r["field_id"], cond_fid],
                      f"Clear {r['field_id']} or change {cond_fid}.")
    # S006 unresolved references
    for ref, reason in c.rep.unresolved:
        holder = c.rep.nodes.get(ref.source)
        fid = holder.field_id if holder else ref.source
        c.add("S006", f"{ref.source}.{ref.key} -> {ref.target}: {reason} (printed as UNRESOLVED).", [fid],
              "Point the reference at an existing id of the right kind, or remove it.")
    # S007 duplicate ids
    for dup in sorted(set(c.rep.duplicates)):
        c.add("S007", f"Id {dup} is used by more than one node.", [], "Give every item a unique id.")
    # S008 sources
    for holder, sid, reason in c.source_problems:
        c.add("S008", f"{holder}: source {sid or '(none)'} not resolvable offline: {reason}.", [holder],
              "Add a matching entry to `sources` (citation, kind, contains_personal_data) or fix the id.")


# --------------------------------------------------------------------------
# R / W / B / T / CH — research logic, workplan, budget, team, chain
# --------------------------------------------------------------------------

def _logic(c: _Ctx):
    if c.recs.get("CORE.RESEARCH.PROBLEM") is not None and not c.resolvable_sources("CORE.RESEARCH.PROBLEM"):
        c.add("R001", "The research problem has no resolvable source reference.", ["CORE.RESEARCH.PROBLEM"],
              "Cite where the problem is documented (source_ids -> sources).")
    if c.recs.get("CORE.RESEARCH.GAP") is not None:
        pks = [a for a, b, k in c.rep.edges if b == "CORE.RESEARCH.GAP" and k == "causal"
               and c.rep.nodes.get(a) is not None and c.rep.nodes[a].chain_key == "PriorKnowledge"]
        if not pks:
            c.add("R002", "The Gap has no incoming link from a PriorKnowledge record.", ["CORE.RESEARCH.GAP"],
                  "Add links.prior_knowledge_ids to the Gap record.")
        for pk in pks:
            if not c.resolvable_sources(pk):
                c.add("R002", f"PriorKnowledge {pk} (linked to the Gap) has no resolvable source.", [pk],
                      "Cite the literature this prior knowledge comes from.")
    if c.recs.get("CORE.RESEARCH.RQ.PRIMARY") is not None and not c.incoming(
            "CORE.RESEARCH.RQ.PRIMARY", lambda a: a == "CORE.RESEARCH.GAP"):
        c.add("R003", "The primary research question is not linked from the Gap.", ["CORE.RESEARCH.RQ.PRIMARY"],
              "Add links.gap_ids: [CORE.RESEARCH.GAP] to the RQ record.")
    rq = lambda a: a in ("CORE.RESEARCH.RQ.PRIMARY", "CORE.RESEARCH.RQ.SECONDARY")
    design = c.in_field("METHOD.PLAN.DESIGN")
    for o in c.items("CORE.RESEARCH.OBJECTIVES"):
        oid = o.get("id")
        if not c.incoming(oid, rq):
            c.add("R004", f"Objective {oid} is not linked from a research question.", ["CORE.RESEARCH.OBJECTIVES"],
                  f"Add rq_ids to objective {oid}.")
        if c.recs.get("METHOD.PLAN.DESIGN") is not None and not c.outgoing(oid, design):
            c.add("R005", f"Objective {oid} is not linked to the method design.", ["CORE.RESEARCH.OBJECTIVES"],
                  f"Add method_ids to objective {oid}.")
    dv = c.value("METHOD.PLAN.DESIGN")
    if isinstance(dv, dict) and c.recs.get("METHOD.PLAN.DATA_COLLECTION") is not None:
        phases = [p.get("id") for p in dv.get("phases") or [] if isinstance(p, dict)] or ["METHOD.PLAN.DESIGN"]
        for ph in phases:
            if not c.outgoing(ph, c.in_field("METHOD.PLAN.DATA_COLLECTION")):
                c.add("R006", f"Method {ph} is not linked to any data-collection item.", ["METHOD.PLAN.DESIGN"],
                      f"Add method_ids: [{ph}] to a METHOD.PLAN.DATA_COLLECTION item.")
    if c.recs.get("METHOD.PLAN.ANALYSIS") is not None and not c.incoming(
            "METHOD.PLAN.ANALYSIS", c.in_field("METHOD.PLAN.DATA_COLLECTION")):
        c.add("R007", "The analysis plan is not linked from a data-collection item.", ["METHOD.PLAN.ANALYSIS"],
              "Add data_ids to METHOD.PLAN.ANALYSIS.")

    # W
    obj_or_design = lambda a: c.in_field("CORE.RESEARCH.OBJECTIVES")(a) or design(a)
    team = {m.get("id") for m in c.items("PROFILE.TEAM.MEMBERS")}
    acts = c.items("WORK.PLAN.ACTIVITIES")
    for a in acts:
        aid = a.get("id")
        if not c.incoming(aid, obj_or_design):
            c.add("W001", f"Activity {aid} is not linked from an objective or method.", ["WORK.PLAN.ACTIVITIES"],
                  f"Add objective_ids or method_ids to activity {aid}.")
        if not (set(a.get("responsible_person_ids") or []) & team):
            c.add("W002", f"Activity {aid} has no responsible team member.", ["WORK.PLAN.ACTIVITIES"],
                  f"Add responsible_person_ids (a TM id) to activity {aid}.")
    if acts:
        weights = [_num(a.get("weight_percent")) for a in acts]
        if any(w is None for w in weights):
            c.add("W003", "An activity has no weight_percent.", ["WORK.PLAN.ACTIVITIES"], "Give every activity a weight.")
        elif sum(q(w) for w in weights) != q(100):
            c.add("W003", f"Activity weights sum to {sum(q(w) for w in weights)}, not 100.", ["WORK.PLAN.ACTIVITIES"],
                  "Adjust weight_percent so the activities sum to 100.")
    for o in c.items("RESULTS.CHAIN.OUTPUTS"):
        if not c.incoming(o.get("id"), c.in_field("WORK.PLAN.ACTIVITIES")):
            c.add("W004", f"Output {o.get('id')} is not produced by any activity.", ["RESULTS.CHAIN.OUTPUTS"],
                  f"Add activity_ids to output {o.get('id')}.")

    # B
    lines = c.items("BUDGET.PLAN.ITEMS")
    for b in lines:
        bid = b.get("id")
        if not c.incoming(bid, c.in_field("WORK.PLAN.ACTIVITIES")):
            c.add("B001", f"Budget item {bid} is not linked to an activity.", ["BUDGET.PLAN.ITEMS"],
                  f"Add activity_ids to budget item {bid}.")
        parts = [_num(b.get(k)) for k in ("quantity", "persons_or_items", "times_or_months", "unit_price")]
        lt = _num(b.get("line_total"))
        if any(p is None for p in parts) or lt is None:
            c.add("B002", f"Budget item {bid}: a factor or line_total is missing.", ["BUDGET.PLAN.ITEMS"],
                  "Fill quantity, persons_or_items, times_or_months, unit_price and line_total.")
        else:
            prod = parts[0] * parts[1] * parts[2] * parts[3]
            if q(lt) != q(prod):
                c.add("B002", f"Budget item {bid}: line_total {q(lt)} != {parts[0]} x {parts[1]} x {parts[2]} x {parts[3]} = {q(prod)}.",
                      ["BUDGET.PLAN.ITEMS"], f"Set line_total of {bid} to {q(prod)} or fix a factor.")
    if lines and all(_num(b.get("line_total")) is not None for b in lines):
        total = sum(q(_num(b.get("line_total"))) for b in lines)
        for fid in ("BUDGET.PLAN.TOTAL", "CORE.GENERAL.REQUESTED_BUDGET", "CORE.GENERAL.TOTAL_BUDGET"):
            v = _num(c.value(fid))
            if c.value(fid) is not None and (v is None or q(v) != total):
                c.add("B002", f"{fid} = {c.value(fid)} but budget lines sum to {total}.", [fid, "BUDGET.PLAN.ITEMS"],
                      f"Set {fid} to {total} or fix the budget lines.")
    for e in c.items("BUDGET.PLAN.EQUIPMENT"):
        if not (e.get("justification") or "").strip():
            c.add("B005", f"Equipment {e.get('id')} has no stated necessity.", ["BUDGET.PLAN.EQUIPMENT"],
                  "Add a justification for the equipment.")

    # T
    members = c.items("PROFILE.TEAM.MEMBERS")
    if members:
        pct = [_num(m.get("contribution_percent")) for m in members]
        if any(p is None for p in pct):
            c.add("T001", "A team member has no contribution_percent.", ["PROFILE.TEAM.MEMBERS"],
                  "Give every member a contribution_percent.")
        elif sum(q(p) for p in pct) != q(100):
            c.add("T001", f"Team contributions sum to {sum(q(p) for p in pct)}, not 100.", ["PROFILE.TEAM.MEMBERS"],
                  "Adjust contribution_percent so the team sums to 100.")
        n_pi = [m.get("project_role") for m in members].count("PI")
        if n_pi != 1:
            c.add("T002", f"The team has {n_pi} members with project_role PI; exactly one is required.",
                  ["PROFILE.TEAM.MEMBERS"], "Mark exactly one member as PI.")

    # CH
    cyc = links.find_cycle(c.rep.causal_edges())
    if cyc:
        c.add("CH001", "The project chain has a cycle: " + " -> ".join(cyc) + ".", [],
              "Remove one of the links in the cycle.")
    for stage in P.chain_config().get("required_stages") or []:
        recs = (c.doc.get("chain") or {}).get(stage) or []
        if not any(isinstance(r, dict) and r.get("value") is not None for r in recs):
            c.add("CH002", f"Required chain stage {stage} is not populated.", [],
                  f"Add at least one {stage} record under chain.{stage}.")


# --------------------------------------------------------------------------
# F / ELIG — the bound fund profile
# --------------------------------------------------------------------------

def _fund(c: _Ctx) -> tuple[list, list, str]:
    hold, stale = [], []
    prof = c.fund
    if prof is None or c.fund_problems:
        for p in c.fund_problems:
            c.add("F003", f"The bound fund profile cannot be used: {p}.", [],
                  "Bind an existing profile in fund_binding.fund_profile_id.")
        hold.append("fund profile not usable")
        return hold, stale, "FICTIONAL"
    if prof.get("status") != "ACTIVE":
        c.add("F003", f"The bound fund profile {c.fund_id} is {prof.get('status')}, not ACTIVE.", [],
              "Bind an ACTIVE fund profile.")
        hold.append(f"fund profile {c.fund_id} is not ACTIVE")
    rules = [r for r in prof.get("rules") or [] if isinstance(r, dict)]
    for r in rules:
        if not str(r.get("source_id") or "").strip():
            c.add("F001", f"Fund rule {r.get('rule_id')} has no source_id.", [], "Record where the rule comes from.")
    eff_to = prof.get("effective_to")
    expired = not (isinstance(eff_to, str) and DATE_RE.match(eff_to)) or eff_to < c.as_of
    for r in rules:
        va = r.get("verified_at")
        if expired or not (isinstance(va, str) and DATE_RE.match(va)):
            stale.append(r.get("rule_id"))
    for rid in sorted(stale):
        c.add("F002", f"Fund rule {rid} is stale as of {c.as_of} (profile effective_to {eff_to}).", [],
              "Re-verify the rule against its source and update the profile.")
    # B006 ceiling (only from the bound, ACTIVE profile)
    if prof.get("status") == "ACTIVE":
        for r in rules:
            if r.get("rule_id") == "F.BUDGET_CEILING" and _num(r.get("value")) is not None:
                tot = _num(c.value("BUDGET.PLAN.TOTAL"))
                if tot is not None and q(tot) > q(_num(r["value"])):
                    c.add("B006", f"BUDGET.PLAN.TOTAL {q(tot)} exceeds the fund ceiling {q(_num(r['value']))} "
                          f"({c.fund_id} rule F.BUDGET_CEILING).", ["BUDGET.PLAN.TOTAL"],
                          "Reduce the budget or bind a different call.")
    # ELIG001 — only what the profile states; GrantThai has no thresholds.
    elig = prof.get("eligibility") or {}
    pis = [m for m in c.items("PROFILE.TEAM.MEMBERS") if m.get("project_role") == "PI"]
    if len(pis) == 1 and elig.get("pi_requires_partner_institution") is True:
        facts = pis[0].get("eligibility_facts") or {}
        if facts.get("partner_institution") in (None, "", False):
            c.add("ELIG001", "The fund profile requires the PI to have a partner institution; the PI's "
                  "eligibility_facts.partner_institution is not stated.", ["PROFILE.TEAM.MEMBERS"],
                  "State eligibility_facts.partner_institution for the PI, or find an eligible PI partner.")
            hold.append("PI eligibility not shown (ELIG001)")
    levels = [prof.get("trust_level")] + [r.get("trust_level") for r in rules]
    levels = [lv for lv in levels if lv in TRUST_ORDER]
    trust = min(levels, key=TRUST_ORDER.index) if levels else "FICTIONAL"
    return hold, sorted(s for s in stale if s), trust


# --------------------------------------------------------------------------

def run(raw: dict, project_dir: Path | None = None, as_of: str | None = None) -> Result:
    """Validate a loaded project.yaml object. `as_of` (YYYY-MM-DD, default
    today) is the date fund-rule staleness is judged against."""
    as_of = as_of or _dt.date.today().isoformat()
    c = _Ctx(raw, project_dir, as_of)

    schema_errs = P.schema_errors(raw, P.PROJECT_SCHEMA_ID)
    for e in schema_errs:
        c.findings.append(Finding("SCHEMA", "BLOCK", f"project.yaml: {e}", [],
                                  "Fix project.yaml so it validates against spec/project/project.schema.json."))
    _structure(c)
    _logic(c)
    hold, stale, trust = _fund(c)

    for rec, _ in P.iter_records(c.doc):
        if "HOLD_FOR_VERIFICATION" in (rec.get("markers") or []):
            hold.append(f"{rec.get('field_id')}: {rec.get('hold_reason') or 'HOLD_FOR_VERIFICATION'}")

    # Account for every catalog rule not evaluated by v0.1 (no silent skip).
    for rid in c.rule_order:
        rule = c.rules[rid]
        if rid in V01_NOT_EVALUATED:
            reason = V01_NOT_EVALUATED[rid]
        elif rule.get("ships") != "v0.1":
            reason = f"ships {rule.get('ships')}; not evaluated by v0.1"
        else:
            continue
        c.findings.append(Finding(rid, "INFO", f"{rid} not evaluated: {reason}.", [],
                                  f"See `grantthai explain {rid}`."))

    order = {rid: i for i, rid in enumerate(["SCHEMA"] + c.rule_order)}
    sev_order = {"BLOCK": 0, "REVIEW": 1, "INFO": 2}
    findings = sorted(c.findings, key=lambda f: (sev_order[f.severity], order.get(f.rule_id, 999)))
    summary = {s.lower(): sum(1 for f in findings if f.severity == s) for s in ("BLOCK", "REVIEW", "INFO")}
    report = {
        "project_id": str(raw.get("project_id")),
        "project_content_sha256": content_sha256(raw),
        "project_state_sha256": state_sha256(raw),
        "rules_version": str(P.rules_catalog().get("version")),
        "fund_profile": c.fund_id or "",
        "summary": summary,
        "findings": [f.as_dict() for f in findings],
    }
    rwv = (trust in ("HUMAN_VERIFIED", "SECOND_CHECKED")) and not stale
    return Result(
        report=report, findings=findings, link_report=c.rep, source_problems=c.source_problems,
        fund_profile=c.fund, fund_profile_id=c.fund_id, hold_reasons=hold, stale_rules=stale,
        trust_level=trust, real_world_verified=rwv,
        submittable=(summary["block"] == 0 and not hold),
    )


def explain(rule_id: str) -> dict:
    """The catalog entry for a rule plus how v0.1 treats it."""
    if rule_id == "SCHEMA":
        return {"id": "SCHEMA", "severity": "BLOCK", "family": "S", "implemented_in_v0_1": True,
                "description_en": "project.yaml does not validate against spec/project/project.schema.json "
                                  "(checked through the local schema registry; nothing is fetched)."}
    rules = {r["id"]: r for r in P.rules_catalog()["rules"]}
    if rule_id not in rules:
        raise KeyError(f"unknown rule id {rule_id!r}")
    out = dict(rules[rule_id])
    if rule_id in V01_NOT_EVALUATED:
        out["implemented_in_v0_1"] = False
        out["v0_1_note"] = V01_NOT_EVALUATED[rule_id]
    else:
        out["implemented_in_v0_1"] = out.get("ships") == "v0.1"
    return out
