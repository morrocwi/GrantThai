#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Yaoharee Lahtee and ARAYA NIKAH SOCIAL ENTERPRISE CO.
# SPDX-License-Identifier: Apache-2.0
"""tools/corpus/practice_stats.py

Which practices do the 100 funded final reports in docs/demo/corpus-100.csv
share *significantly*? Reads only the public CSV (no PDF, no report text)
and prints the evidence table used in docs/practice/funded-work-patterns.md.

Tiers (stated in the docs, applied here mechanically):

  CORE        present in >= 70 of the 100 documents AND >= 50% in each
              source subset (HSRI repository n=83, PSU repository n=17), so
              no single source carries the pattern.
  CONTEXTUAL  40-69% overall, or >= 70% overall but below 50% in one
              source subset (concentrated in one funder/discipline).
  EMERGING    below 40% overall but rising across the three year bands
              (BE <=2559, 2560-62, 2563-68): the latest band is the highest
              and at least 15 points above the earliest.
  RARE        below 40% overall and not rising: no practice claim.
  NO_CLAIM    a proposal-only item (budget, workplan, key results, TRL,
              SRL): absence from a final report says nothing about a
              proposal, so this corpus makes no claim about it.

A "report_only" pattern (results, discussion, appendix, acknowledgement)
keeps its tier but has no proposal field; it supports guidance only.

Detection is heading-based (tools/corpus/corpus_extract.py): research
questions and ethics are undercounted, because reports often state them
in running text rather than under a heading.

Usage:
    python tools/corpus/practice_stats.py [--csv docs/demo/corpus-100.csv] [--format md|tsv]
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

BANDS = ("<=2559", "2560-62", "2563-68")


def band(year: str) -> str:
    y = int(year)
    return BANDS[0] if y <= 2559 else (BANDS[1] if y <= 2562 else BANDS[2])


def _on(r: dict, col: str) -> bool:
    return str(r.get(col, "")).strip() not in ("", "0")


def _int(r: dict, col: str) -> int:
    try:
        return int(str(r.get(col, "")).strip() or 0)
    except ValueError:
        return 0


def _any(*cols):
    return lambda r: any(_on(r, c) for c in cols)


# pattern_id, label, test(row), GrantThai field_ids, kind
#   kind: "proposal" (feeds a proposal field), "report_only", "proposal_only"
PATTERNS = [
    ("FWP-01", "Background / rationale section", _any("has_background"),
     "CORE.NARRATIVE.RATIONALE; CORE.RESEARCH.PROBLEM; CORE.RESEARCH.NATIONAL_NEED", "proposal"),
    ("FWP-02", "Objectives section", _any("has_objectives"),
     "CORE.RESEARCH.OBJECTIVES; CORE.NARRATIVE.OBJECTIVES", "proposal"),
    ("FWP-03", "Objectives written as a numbered list (>= 2 items)", lambda r: _int(r, "objectives_items") >= 2,
     "CORE.RESEARCH.OBJECTIVES; CORE.NARRATIVE.OBJECTIVES", "proposal"),
    ("FWP-04", "Method section", _any("has_methods"),
     "CORE.NARRATIVE.METHOD; METHOD.PLAN.DESIGN", "proposal"),
    ("FWP-05", "Objectives and method both present", lambda r: _on(r, "has_objectives") and _on(r, "has_methods"),
     "CORE.RESEARCH.OBJECTIVES; METHOD.PLAN.DESIGN", "proposal"),
    ("FWP-06", "Reference list", lambda r: _on(r, "has_references") or _int(r, "references_count") > 0,
     "CORE.NARRATIVE.REFERENCES; CORE.NARRATIVE.THEORY", "proposal"),
    ("FWP-07", "Results section", _any("has_results"), "(none: report-stage)", "report_only"),
    ("FWP-08", "Discussion / conclusion section", _any("has_discussion_conclusion"),
     "(none: report-stage)", "report_only"),
    ("FWP-09", "Literature review section", _any("has_lit_review"),
     "CORE.NARRATIVE.THEORY; CORE.RESEARCH.THEORETICAL_FOUNDATIONS; CORE.RESEARCH.GAP", "proposal"),
    ("FWP-10", "Method sub-parts (population, instruments, data collection, analysis, or sample-size basis)",
     _any("has_population", "has_instruments", "has_data_collection", "has_analysis", "mention_sample_size_basis"),
     "CORE.NARRATIVE.METHOD; METHOD.PLAN.POPULATION; METHOD.PLAN.SAMPLE; METHOD.PLAN.INSTRUMENTS; "
     "METHOD.PLAN.DATA_COLLECTION; "
     "METHOD.PLAN.ANALYSIS", "proposal"),
    ("FWP-11", "Abstract (Thai or English)", _any("has_abstract_th", "has_abstract_en"),
     "CORE.NARRATIVE.SUMMARY", "proposal"),
    ("FWP-12", "Keywords", _any("has_keywords"), "CORE.GENERAL.KEYWORDS_TH; CORE.GENERAL.KEYWORDS_EN", "proposal"),
    ("FWP-13", "Recommendations of any kind (section or policy phrase)",
     _any("has_recommendations", "has_policy_recommendations", "mention_policy_rec"),
     "RESULTS.CHAIN.UTILIZATION_DESC; RESULTS.CHAIN.USERS", "proposal"),
    ("FWP-14", "Policy-recommendation phrase", _any("mention_policy_rec"),
     "RESULTS.CHAIN.UTILIZATION_DESC; RESULTS.CHAIN.USERS", "proposal"),
    ("FWP-15", "Outputs, expected benefit or utilization section",
     _any("has_outputs", "has_expected_benefit", "has_utilization"),
     "RESULTS.CHAIN.OUTPUTS; RESULTS.CHAIN.BENEFIT_SUMMARY; RESULTS.CHAIN.UTILIZATION_DESC", "proposal"),
    ("FWP-16", "Strategy / national-plan wording", _any("mention_strategy"),
     "CORE.RESEARCH.NATIONAL_NEED; CORE.GENERAL.MASTER_PLAN", "proposal"),
    ("FWP-17", "Data-analysis sub-section", _any("has_analysis"), "METHOD.PLAN.ANALYSIS", "proposal"),
    ("FWP-18", "Population / sample sub-section", _any("has_population"),
     "METHOD.PLAN.POPULATION; METHOD.PLAN.SAMPLE", "proposal"),
    ("FWP-19", "Sample-size basis stated (formula or named method)", _any("mention_sample_size_basis"),
     "METHOD.PLAN.SAMPLE", "proposal"),
    ("FWP-20", "Data-collection sub-section", _any("has_data_collection"), "METHOD.PLAN.DATA_COLLECTION", "proposal"),
    ("FWP-21", "Instruments sub-section", _any("has_instruments"), "METHOD.PLAN.INSTRUMENTS", "proposal"),
    ("FWP-22", "Conceptual framework section", _any("has_framework"), "CORE.NARRATIVE.FRAMEWORK", "proposal"),
    ("FWP-23", "Expert or stakeholder validation of instruments or draft proposals", _any("mention_expert_validation"),
     "METHOD.PLAN.QUALITY", "proposal"),
    ("FWP-24", "Ethics (section, committee approval or informed consent)",
     _any("has_ethics", "mention_ethics_approval", "mention_informed_consent"), "METHOD.PLAN.ETHICS", "proposal"),
    ("FWP-25", "Limitations of the study stated", _any("mention_limitations"), "METHOD.PLAN.QUALITY", "proposal"),
    ("FWP-26", "Research users named", _any("mention_users", "mention_beneficiaries", "has_users_section"),
     "RESULTS.CHAIN.USERS; RESULTS.CHAIN.BENEFICIARIES", "proposal"),
    ("FWP-27", "Operational definitions", _any("has_definitions"), "CORE.RESEARCH.CONSTRUCTS", "proposal"),
    ("FWP-28", "Triangulation named", _any("mention_triangulation"), "METHOD.PLAN.QUALITY", "proposal"),
    ("FWP-29", "Scope section", _any("has_scope"), "CORE.RESEARCH.BOUNDARY_CONDITIONS", "proposal"),
    ("FWP-30", "Executive summary", _any("has_executive_summary"), "CORE.NARRATIVE.SUMMARY", "proposal"),
    ("FWP-31", "Research question as a heading", _any("has_rq"), "CORE.RESEARCH.RQ.PRIMARY", "proposal"),
    ("FWP-32", "Hypothesis section", _any("has_hypothesis"), "CORE.RESEARCH.HYPOTHESES", "proposal"),
    ("FWP-33", "Appendix", _any("has_appendix"), "DOC.ATTACHMENTS.DOCUMENTS", "report_only"),
    ("FWP-34", "Acknowledgement", _any("has_acknowledgement"), "(none: report-stage)", "report_only"),
    ("FWP-35", "Budget section or amount", _any("has_budget", "mention_budget_amount"),
     "BUDGET.PLAN.ITEMS; BUDGET.PLAN.TOTAL", "proposal_only"),
    ("FWP-36", "Workplan / timeline section", _any("has_workplan"), "WORK.PLAN.ACTIVITIES", "proposal_only"),
    ("FWP-37", "Key results, TRL or SRL wording", _any("mention_kr", "mention_trl", "mention_srl"),
     "CORE.ALIGNMENT.STATEMENT; READY.TRL.CURRENT; READY.SRL.CURRENT", "proposal_only"),
]


def pct(rows: list, test) -> int:
    return round(100 * sum(1 for r in rows if test(r)) / len(rows)) if rows else 0


def tier(overall: int, sub_a: int, sub_b: int, bands: list, kind: str) -> str:
    if kind == "proposal_only":
        return "NO_CLAIM"
    if overall >= 70 and min(sub_a, sub_b) >= 50:
        return "CORE"
    if overall >= 40:
        return "CONTEXTUAL"
    if bands[2] == max(bands) and bands[2] - bands[0] >= 15:
        return "EMERGING"
    return "RARE"


def trend(bands: list) -> str:
    if bands[2] == max(bands) and bands[2] - bands[0] >= 15:
        return "rising"
    if bands[0] == max(bands) and bands[0] - bands[2] >= 15:
        return "falling"
    return "flat"


def compute(csv_path: Path) -> tuple[list, dict]:
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8")))
    hsri = [r for r in rows if "HSRI" in r["source_repository"]]
    psu = [r for r in rows if "PSU" in r["source_repository"]]
    by_band = {b: [r for r in rows if band(r["year_be"]) == b] for b in BANDS}
    out = []
    for pid, label, test, fields, kind in PATTERNS:
        n = sum(1 for r in rows if test(r))
        a, b = pct(hsri, test), pct(psu, test)
        bands = [pct(by_band[x], test) for x in BANDS]
        out.append({
            "pattern_id": pid, "pattern": label, "n": n, "all_pct": pct(rows, test),
            "hsri_pct": a, "psu_pct": b, "bands": bands, "trend": trend(bands),
            "tier": tier(pct(rows, test), a, b, bands, kind), "kind": kind, "field_ids": fields,
        })
    sizes = {"all": len(rows), "hsri": len(hsri), "psu": len(psu), **{b: len(v) for b, v in by_band.items()}}
    return out, sizes


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--csv", default=str(Path(__file__).resolve().parents[2] / "docs/demo/corpus-100.csv"))
    ap.add_argument("--format", choices=("md", "tsv"), default="md")
    a = ap.parse_args(argv)
    rows, sizes = compute(Path(a.csv))
    if a.format == "tsv":
        print("pattern_id\tpattern\tn\tall\thsri\tpsu\tband1\tband2\tband3\ttrend\ttier\tkind\tfield_ids")
        for r in rows:
            print("\t".join(map(str, [r["pattern_id"], r["pattern"], r["n"], r["all_pct"], r["hsri_pct"],
                                      r["psu_pct"], *r["bands"], r["trend"], r["tier"], r["kind"],
                                      r["field_ids"]])))
        return 0
    print(f"n = {sizes['all']} (HSRI {sizes['hsri']}, PSU {sizes['psu']}; "
          f"BE <=2559 {sizes['<=2559']}, 2560-62 {sizes['2560-62']}, 2563-68 {sizes['2563-68']})\n")
    print("| Id | Pattern | N/100 | HSRI % | PSU % | Bands % (<=2559 / 60-62 / 63-68) | Trend | Tier | Kind |")
    print("|---|---|---:|---:|---:|---|---|---|---|")
    for r in rows:
        print(f"| {r['pattern_id']} | {r['pattern']} | {r['n']} | {r['hsri_pct']} | {r['psu_pct']} | "
              f"{' / '.join(map(str, r['bands']))} | {r['trend']} | {r['tier']} | {r['kind']} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
