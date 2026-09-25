#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Yaoharee Lahtee and ARAYA NIKAH SOCIAL ENTERPRISE CO.
# SPDX-License-Identifier: Apache-2.0
"""grantthai_skill.py — the small helper the GrantThai agent skill uses.

It is a thin wrapper over the GrantThai Python API (grantthai.api_py). It
does not call any AI model and it adds no rule of its own: every status,
provenance and validation decision is made by the GrantThai engine.

    python grantthai_skill.py check
        Is the engine importable? Prints the version and where it found it.

    python grantthai_skill.py warning
        Print the personal/confidential-data warning (Thai, then English).
        Show it to the researcher BEFORE accepting any research data
        (docs/policy/ai-use-ceiling.md, section 5).

    python grantthai_skill.py apply ANSWERS.yaml [--project work.yaml] [--init] [--route ID]
        Write the interview answers (and the researcher's sources) into
        the work file (work.yaml 0.3, or a legacy project.yaml) through
        api_py.set_field. --init creates the file first when it does not
        exist yet (work.yaml when `project.work_type` is given, else a
        legacy project.yaml). --route ID (or `project.route` in the answers
        file) records the output route THE RESEARCHER CHOSE as
        routing.default_route; never write one they did not choose.

    python grantthai_skill.py report [--project work.yaml] [--route ID] [--sub-profile SP]
                                      [--as-of YYYY-MM-DD] [--json]
        Validate for one route, explain every BLOCK and REVIEW finding in
        plain Thai (from reference/rules-th.md), then build that route's one
        output file (build/NRIIS_SUBMISSION.md, ACADEMIC_ARTICLE.md or
        RESEARCH_CONCEPT_NOTE.md) and print its path. With no --route the
        route comes only from the researcher's declaration; when that does
        not decide, the candidates are printed, nothing is built, exit 2.

The answers file format is described in reference/answers-format.md.

Engine lookup order: an installed `grantthai` package; otherwise
$GRANTTHAI_HOME/src (a GrantThai checkout); otherwise the checkout this
file sits in (skills/grantthai/scripts -> repository root).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
SKILL_DIR = HERE.parent
RULES_TH = SKILL_DIR / "reference" / "rules-th.md"

# Keys an answer entry may carry. Anything else is a mistake in the
# answers file and is refused rather than silently dropped.
ANSWER_KEYS = {
    "field_id", "value", "by", "provenance_class", "source_type", "evidence_role",
    "source_ids", "links", "chain_node", "supports_claim_id", "claim_strength_cap", "note",
    "markers",
}
# Markers an answer may attach to a value it supplies (v0.2): a value read
# from a public document or an unconfirmed call keeps NEEDS_VERIFICATION.
ANSWER_MARKERS = {"NEEDS_VERIFICATION", "HOLD_FOR_VERIFICATION"}
# Who wrote the words in `value`.
BY_VALUES = {
    "researcher": ("human", "human"),                          # the researcher said or wrote it
    "researcher_edited_ai_draft": ("human", "human_ai_assisted"),  # researcher rewrote/adopted an AI draft
    "ai": ("ai_assisted", "ai_draft"),                         # an AI draft, not yet confirmed
}
SOURCE_KEYS = {"source_id", "kind", "citation", "locator", "url", "file", "sha256",
               "accessed", "contains_personal_data"}
# Keys of the answers file's `project` block. `route` and `sub_profile` are
# the researcher's choice of output route (v0.3 router); the script records
# them and never decides them.
PROJECT_KEYS = {"project_id", "work_id", "work_type", "fund_profile_id", "mode", "form_profile", "route",
                "sub_profile"}
# Keys of the answers file's ai_use_declaration block. The researcher's
# confirmation (declaration_confirmed_by_human, confirmed_by, confirmed_on)
# is refused here: only the researcher sets it, in project.yaml.
DECLARATION_KEYS = {"tools", "influence_on_conclusions", "human_verification", "data_handling",
                    "log_ref", "risk_self_assessment"}
DECLARATION_HUMAN_ONLY = {"declaration_confirmed_by_human", "confirmed_by", "confirmed_on"}
TOOL_KEYS = {"name", "developer", "version", "stages", "purpose", "used_on"}


def _import_api():
    try:
        from grantthai import api_py  # type: ignore
        return api_py
    except ImportError:
        pass
    candidates = []
    if os.environ.get("GRANTTHAI_HOME"):
        candidates.append(Path(os.environ["GRANTTHAI_HOME"]) / "src")
    candidates.append(SKILL_DIR.parents[1] / "src")
    for c in candidates:
        if (c / "grantthai" / "api_py.py").exists():
            sys.path.insert(0, str(c))
            if not os.environ.get("GRANTTHAI_HOME"):
                os.environ["GRANTTHAI_HOME"] = str(c.parent)
            from grantthai import api_py  # type: ignore
            return api_py
    raise SystemExit(
        "GrantThai engine not found. Install it from a GrantThai checkout with "
        "`pip install -e .`, or set GRANTTHAI_HOME to the checkout folder.")


def _yaml():
    import yaml  # pyyaml is a GrantThai dependency
    return yaml


# --------------------------------------------------------------------------
# Thai explanations (reference/rules-th.md is the one source)
# --------------------------------------------------------------------------
def load_rules_th(path: Path = RULES_TH) -> dict[str, str]:
    """Map rule id -> the plain-Thai text under its '### <ID>' heading."""
    out: dict[str, str] = {}
    current = None
    buf: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^###\s+([A-Z]+[0-9]*)\s*$", line)
        if m:
            if current:
                out[current] = "\n".join(buf).strip()
            current, buf = m.group(1), []
        elif line.startswith("## ") and current:
            out[current] = "\n".join(buf).strip()
            current, buf = None, []
        elif current:
            buf.append(line)
    if current:
        out[current] = "\n".join(buf).strip()
    return out


# --------------------------------------------------------------------------
# apply
# --------------------------------------------------------------------------
def _upsert_sources(doc: dict, sources: list[dict]) -> None:
    existing = doc.setdefault("sources", [])
    by_id = {s.get("source_id"): s for s in existing}
    for s in sources:
        extra = set(s) - SOURCE_KEYS
        if extra:
            raise ValueError(f"source {s.get('source_id')}: unknown keys {sorted(extra)}")
        if "kind" in s and s["kind"] == "AI_TRANSLATION_PROPOSAL":
            raise ValueError("an AI proposal is never a source")
        s = dict(s)
        s.setdefault("contains_personal_data", False)
        if s.get("source_id") in by_id:
            by_id[s["source_id"]].clear()
            by_id[s["source_id"]].update(s)
        else:
            existing.append(s)
            by_id[s["source_id"]] = s


def _is_work(doc: dict) -> bool:
    return str(doc.get("schema_version", "")).startswith("0.3")


def set_route(doc: dict, route: str, sub_profile: str | None = None) -> str:
    """Record the output route the researcher chose (routing.default_route,
    plus declared_routes and, when given, sub_profiles[route]) on a work.yaml
    0.3 object. A legacy 0.2 project.yaml has no `routing` key: refuse and
    point at `grantthai migrate`. The route id itself is checked by the
    engine at validate/build time (an unknown id is reported there)."""
    if not _is_work(doc):
        raise ValueError("this is a legacy project.yaml (0.2): it has no routing block. Build it with "
                         "`--route ID` instead, or run `grantthai migrate --rename` to get a work.yaml first")
    routing = doc.setdefault("routing", {})
    declared = list(routing.get("declared_routes") or [])
    if route not in declared:
        declared.append(route)
    routing["declared_routes"] = declared
    routing["default_route"] = route
    if sub_profile:
        routing.setdefault("sub_profiles", {})[route] = sub_profile
    return f"routing.default_route: {route} (the researcher's choice; not part of content_sha256)"


def apply_answers(api, project_path: Path, answers_doc: dict, *, init: bool = False,
                  route: str | None = None) -> list[str]:
    """Apply an answers document to the work file. Returns one line per field."""
    meta = answers_doc.get("project") or {}
    extra = set(meta) - PROJECT_KEYS
    if extra:
        raise ValueError(f"project: unknown keys {sorted(extra)}")
    if not project_path.exists():
        if not init:
            raise FileNotFoundError(f"{project_path} does not exist (use --init to create it)")
        wid = meta.get("work_id", meta.get("project_id", "NEEDS_INPUT"))
        if meta.get("work_type"):
            api.new_work(wid, meta["work_type"], fund_profile_id=meta.get("fund_profile_id"),
                         mode=meta.get("mode", "expert"), path=project_path)
        else:
            api.new_project(project_id=wid,
                            fund_profile_id=meta.get("fund_profile_id", "example/FICTIONAL_CALL@0.1"),
                            mode=meta.get("mode", "expert"), path=project_path)
    doc = api.load(project_path)
    lines = []
    if "form_profile" in meta:
        # v0.2: the proposal form type (mappings/nriis/form_profiles/; every
        # profile is NEEDS_VERIFICATION). The engine reports an unknown id.
        if _is_work(doc):
            doc.setdefault("routing", {}).setdefault("sub_profiles", {})["nriis-proposal"] = meta["form_profile"]
        else:
            doc["form_profile"] = meta["form_profile"]
    chosen = route or meta.get("route")
    if chosen:
        lines.append(set_route(doc, chosen, meta.get("sub_profile")))
    elif meta.get("sub_profile"):
        raise ValueError("project.sub_profile needs project.route (the route it belongs to)")
    _upsert_sources(doc, answers_doc.get("sources") or [])
    source_kind = {s.get("source_id"): s.get("kind") for s in doc.get("sources") or []}
    tool = answers_doc.get("tool")
    tool_version = answers_doc.get("tool_version")
    tool_stage = answers_doc.get("tool_stage")
    for i, a in enumerate(answers_doc.get("answers") or []):
        extra = set(a) - ANSWER_KEYS
        if extra:
            raise ValueError(f"answer #{i + 1} ({a.get('field_id')}): unknown keys {sorted(extra)}")
        if "field_id" not in a or "value" not in a:
            raise ValueError(f"answer #{i + 1}: field_id and value are required")
        # `by` has no default for real content: who wrote the words must be
        # stated every time (reference/provenance.md: when in doubt, `ai`).
        # A bare marker (null / NEEDS_INPUT / NEEDS_VERIFICATION) has no words.
        if "by" not in a and a["value"] not in (None, "NEEDS_INPUT", "NEEDS_VERIFICATION"):
            raise ValueError(f"answer #{i + 1} ({a['field_id']}): `by` is required "
                             f"(one of {sorted(BY_VALUES)}; when in doubt use ai)")
        by = a.get("by", "researcher")
        if by not in BY_VALUES:
            raise ValueError(f"answer #{i + 1} ({a['field_id']}): by must be one of {sorted(BY_VALUES)}")
        actor, authored_by = BY_VALUES[by]
        prov: dict[str, Any] = {}
        for k in ("provenance_class", "source_type", "evidence_role"):
            if a.get(k):
                prov[k] = a[k]
        if a.get("source_ids") and "source_type" not in prov:
            kind = source_kind.get(a["source_ids"][0])
            if kind:
                prov["source_type"] = kind
        if authored_by == "human_ai_assisted":
            prov["authored_by"] = "human_ai_assisted"
        if actor == "ai_assisted" and prov.get("provenance_class") == "SOURCE":
            raise ValueError(f"{a['field_id']}: an AI draft can never be provenance_class SOURCE")
        rec = api.set_field(doc, a["field_id"], a["value"], actor=actor,
                            chain_node=a.get("chain_node"), provenance=prov or None,
                            source_ids=a.get("source_ids"), links=a.get("links"),
                            tool=tool if actor == "ai_assisted" else None,
                            tool_version=tool_version if actor == "ai_assisted" else None,
                            stage=tool_stage if actor == "ai_assisted" else None, save=False)
        if a.get("markers"):
            bad = set(a["markers"]) - ANSWER_MARKERS
            if bad:
                raise ValueError(f"{a['field_id']}: markers must be among {sorted(ANSWER_MARKERS)}, not {sorted(bad)}")
            rec["markers"] = sorted(set(list(rec.get("markers") or []) + list(a["markers"])))
        if "supports_claim_id" in a:
            rec["supports_claim_id"] = a["supports_claim_id"]
        if "claim_strength_cap" in a:
            rec["claim_strength_cap"] = a["claim_strength_cap"]
        lines.append(f"{rec['field_id']}: {rec['status']} "
                     f"({rec['provenance']['provenance_class']}, {rec['provenance']['authored_by']})")
    if authored_by_any_human_ai(doc) and tool:
        api.record_ai_tool(doc, tool, version=tool_version, stage=tool_stage, save=False)
    if answers_doc.get("ai_use_declaration") is not None:
        lines.extend(merge_declaration(doc, answers_doc["ai_use_declaration"]))
    api.save(doc, project_path)
    return lines


def merge_declaration(doc: dict, block: Any) -> list[str]:
    """Merge the answers file's ai_use_declaration block into project.yaml
    (authoring.ai_use_declaration). Tools merge by name. The researcher's
    confirmation keys are refused. Any change resets the confirmation."""
    if not isinstance(block, dict):
        raise ValueError("ai_use_declaration must be a mapping")
    human_only = set(block) & DECLARATION_HUMAN_ONLY
    if human_only:
        raise ValueError(f"ai_use_declaration: {sorted(human_only)} can only be set by the researcher, "
                         "in project.yaml, after reading the declaration (never from an answers file)")
    extra = set(block) - DECLARATION_KEYS
    if extra:
        raise ValueError(f"ai_use_declaration: unknown keys {sorted(extra)}")
    auth = doc.setdefault("authoring", {"mode": "human", "tools_disclosed": [], "self_declared": True})
    decl = auth.setdefault("ai_use_declaration", {})
    before = json.dumps(decl, sort_keys=True, ensure_ascii=False)
    for t in block.get("tools") or []:
        if not isinstance(t, dict) or not t.get("name"):
            raise ValueError("ai_use_declaration.tools: every entry needs a name")
        bad = set(t) - TOOL_KEYS
        if bad:
            raise ValueError(f"ai_use_declaration.tools {t['name']!r}: unknown keys {sorted(bad)}")
        tools = decl.setdefault("tools", [])
        cur = next((x for x in tools if isinstance(x, dict) and x.get("name") == t["name"]), None)
        if cur is None:
            cur = {"name": t["name"]}
            tools.append(cur)
        for k in ("developer", "version", "purpose", "used_on"):
            if t.get(k) is not None:
                cur[k] = t[k]
        if t.get("stages"):
            cur["stages"] = list(dict.fromkeys(list(cur.get("stages") or []) + list(t["stages"])))
    for k in ("influence_on_conclusions", "human_verification", "data_handling", "log_ref",
              "risk_self_assessment"):
        if block.get(k) is not None:
            decl[k] = block[k]
    changed = json.dumps(decl, sort_keys=True, ensure_ascii=False) != before
    if changed or "declaration_confirmed_by_human" not in decl:
        decl["declaration_confirmed_by_human"] = False
    return ["authoring.ai_use_declaration: " + ("updated; the researcher must confirm it"
                                                if changed else "unchanged")]


def authored_by_any_human_ai(doc: dict) -> bool:
    for rec in doc.get("fields") or []:
        if (rec.get("provenance") or {}).get("authored_by") == "human_ai_assisted":
            return True
    for recs in (doc.get("chain") or {}).values():
        for rec in recs or []:
            if (rec.get("provenance") or {}).get("authored_by") == "human_ai_assisted":
                return True
    return False


# --------------------------------------------------------------------------
# report
# --------------------------------------------------------------------------
def report(api, project_path: Path, *, as_of: str | None = None, route: str | None = None,
           sub_profile: str | None = None) -> dict:
    """Validate and build ONE route. The route is --route, else what the
    researcher declared in the file (routing.default_route; a legacy
    project.yaml is nriis-proposal; else the one default route of the
    work_type). When none of these decides, nothing is validated or built
    and the result carries `candidates` for the researcher to choose from."""
    try:
        rid = api.resolve_route(project_path, route)
    except api.AmbiguousRoute as exc:
        return {"route": None, "candidates": list(exc.candidates), "summary": None, "findings": [],
                "output": None, "ai_drafts_to_confirm": [],
                "note": "ยังไม่ได้เลือกเส้นทางผลลัพธ์ ให้ถามผู้วิจัยว่าจะให้สร้างไฟล์แบบไหน แล้วรันใหม่ด้วย --route "
                        "(GrantThai และ AI ไม่เลือกเส้นทางแทนผู้วิจัย)"}
    rep = api.validate(project_path, as_of=as_of, route=rid, sub_profile=sub_profile)
    th = load_rules_th()
    explained = []
    for f in rep["findings"]:
        if f["severity"] == "INFO":
            continue
        explained.append({**f, "explain_th": th.get(f["rule_id"],
                          "ยังไม่มีคำอธิบายภาษาไทยสำหรับกฎนี้ ดูคำอธิบายภาษาอังกฤษด้วยคำสั่ง "
                          f"`grantthai explain {f['rule_id']}`")})
    out = api.build(project_path, route=rid, sub_profile=sub_profile, as_of=as_of)
    ai_drafts = []
    doc = api.load(project_path)
    for rec in list(doc.get("fields") or []) + [r for rs in (doc.get("chain") or {}).values() for r in rs or []]:
        if (rec.get("provenance") or {}).get("authored_by") == "ai_draft":
            ai_drafts.append(rec["field_id"])
    return {"route": rid, "candidates": [], "summary": rep["summary"], "findings": explained,
            "output": str(out), "ai_drafts_to_confirm": ai_drafts}


def _print_report(r: dict) -> None:
    if r.get("candidates"):
        print(r["note"])
        print("เส้นทางที่เลือกได้ (ดูรายละเอียดด้วย `grantthai route list`):")
        for rid in r["candidates"]:
            print(f"  - {rid}")
        return
    s = r["summary"]
    print(f"เส้นทางผลลัพธ์: {r['route']}")
    print(f"ผลตรวจ: BLOCK {s['block']} / REVIEW {s['review']} / INFO {s['info']}")
    # One Thai explanation per rule, then every finding of that rule.
    by_rule: dict[str, list[dict]] = {}
    for f in r["findings"]:
        by_rule.setdefault(f["rule_id"], []).append(f)
    for rule_id, fs in by_rule.items():
        print()
        print(f"[{fs[0]['severity']}] {rule_id} ({len(fs)})")
        for line in fs[0]["explain_th"].splitlines():
            print(f"    {line}")
        for f in fs:
            print(f"  - {f['message_en']}")
    if r["ai_drafts_to_confirm"]:
        print()
        print("ช่องที่ AI ร่างไว้ ผู้วิจัยต้องอ่านและยืนยันเอง:")
        for fid in r["ai_drafts_to_confirm"]:
            print(f"  - {fid}")
    print()
    print(f"ไฟล์ผลลัพธ์ (ไฟล์เดียว): {r['output']}")


def _discover(api) -> Path:
    """The one canonical input in the current folder (work.yaml first, then
    project.yaml); both present is refused by the engine."""
    from grantthai.core import project as P  # type: ignore
    return P.discover(None)


def _discover_or_new(api, answers: dict) -> Path:
    try:
        return _discover(api)
    except FileNotFoundError:
        meta = answers.get("project") or {}
        return Path("work.yaml" if meta.get("work_type") else "project.yaml")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="grantthai_skill")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    sub.add_parser("warning")
    p = sub.add_parser("apply")
    p.add_argument("answers")
    p.add_argument("--project", default=None, help="work.yaml / project.yaml (default: the one in the current folder)")
    p.add_argument("--init", action="store_true")
    p.add_argument("--route", default=None, help="the output route the RESEARCHER chose (recorded as routing.default_route)")
    p = sub.add_parser("report")
    p.add_argument("--project", default=None, help="work.yaml / project.yaml (default: the one in the current folder)")
    p.add_argument("--route", default=None, help="the output route the RESEARCHER chose")
    p.add_argument("--sub-profile", default=None)
    p.add_argument("--as-of")
    p.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    api = _import_api()
    try:
        if a.cmd == "check":
            import grantthai
            print(f"grantthai {getattr(grantthai, '__version__', '?')} found at "
                  f"{Path(grantthai.__file__).resolve().parent}")
            return 0
        if a.cmd == "warning":
            w = api.data_warning()
            print(w["th"])
            print()
            print(w["en"])
            return 0
        if a.cmd == "apply":
            answers = _yaml().safe_load(Path(a.answers).read_text(encoding="utf-8")) or {}
            project = Path(a.project) if a.project else _discover_or_new(api, answers)
            for line in apply_answers(api, project, answers, init=a.init, route=a.route):
                print(line)
            return 0
        if a.cmd == "report":
            project = Path(a.project) if a.project else _discover(api)
            r = report(api, project, as_of=a.as_of, route=a.route, sub_profile=a.sub_profile)
            if a.json:
                print(json.dumps(r, ensure_ascii=False, indent=2))
            else:
                _print_report(r)
            if r.get("candidates"):
                return 2
            return 1 if r["summary"]["block"] else 0
    except (ValueError, KeyError, FileExistsError, FileNotFoundError) as exc:
        print(f"grantthai_skill: error: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    sys.exit(main())
