"""grantthai.cli — the AI-free command line.

One work object (work.yaml 0.3, or a legacy project.yaml 0.2 read
unchanged) -> one output route chosen by the researcher -> exactly one file
per invocation. A PATH may be the file or its directory; with no PATH the
current directory is searched for work.yaml, then project.yaml, and the
command stops (exit 2) when both are present.

    grantthai init [PATH] [--work-type T] [--work-id ID] [--fund FUND_PROFILE_ID] [--mode MODE]
    grantthai migrate [PATH] [--rename] [--dry-run]
    grantthai route list | check --route ID [PATH] | build --route ID [PATH] | profiles [PATH]
    grantthai set FIELD_ID VALUE [--project PATH] [--string] [--chain-node NODE]
                  [--source-id SRC-..]... [--provenance-class C]
                  [--ai --tool NAME [--tool-version V] [--stage STAGE]]
    grantthai validate [PATH] [--route ID] [--sub-profile SP] [--structure-profile P] [--json] [--as-of YYYY-MM-DD]
    grantthai explain RULE_ID|FIELD_ID
    grantthai explain-field FIELD_ID
    grantthai build [PATH] [--route ID] [--sub-profile SP] [--out DIR] [--as-of YYYY-MM-DD]
    grantthai fields [--route ID] [--tab TAB] [--required]
    grantthai profiles
    grantthai link | review | accept-mapping | reject-mapping | lock | diff   (v0.2, named human only)

This package MUST NEVER import grantthai.assist, grantthai.mcp,
grantthai.api, or any LLM SDK. Enforced by tools/ci/check_no_ai_import.py.
"""
from __future__ import annotations

import argparse
import json
import sys

from grantthai import __version__
from grantthai import api_py as api
from grantthai.cli import cmd_explain_field, cmd_review, cmd_route
from grantthai.core import project as P
from grantthai.core.object_hash import load_project_text


def _value(text: str, force_string: bool):
    if force_string:
        return text
    try:
        return load_project_text(text)
    except Exception:
        return text


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="grantthai",
                                 description="one work object -> one output route (chosen by you) -> one file")
    ap.add_argument("--version", action="version", version=f"grantthai {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init", help="write a blank work.yaml (0.3)")
    p.add_argument("path", nargs="?", default=P.WORK_FILE)
    p.add_argument("--work-id", "--project-id", dest="work_id", default="NEEDS_INPUT")
    p.add_argument("--work-type", default=P.LEGACY_WORK_TYPE,
                   help="research_proposal (default), academic_article, concept_note, ... ; sets defaults only")
    p.add_argument("--fund", default=None, help="fund profile id (written when the work type's default route "
                                                "needs one, or when given)")
    p.add_argument("--mode", default="expert", choices=["expert", "human_direct", "citizen"])

    p = sub.add_parser("migrate", help="rewrite a legacy project.yaml as work.yaml 0.3; prints stale review gates")
    p.add_argument("path", nargs="?", default=None)
    p.add_argument("--rename", action="store_true", help="write work.yaml and remove project.yaml")
    p.add_argument("--dry-run", action="store_true", help="report only; write nothing")

    p = sub.add_parser("set", help="set one field (status becomes DRAFT)")
    p.add_argument("field_id")
    p.add_argument("value", help="YAML value; NEEDS_INPUT clears it")
    p.add_argument("--project", default=None, help="work.yaml / project.yaml (default: discovered)")
    p.add_argument("--string", action="store_true", help="store VALUE as a string, unparsed")
    p.add_argument("--chain-node")
    p.add_argument("--source-id", action="append", dest="source_ids")
    p.add_argument("--provenance-class", choices=["SOURCE", "INFERENCE", "DECISION", "DERIVED"])
    p.add_argument("--ai", action="store_true", help="the value is an AI draft (stored as ai_draft, never SOURCE)")
    p.add_argument("--tool", help="disclosed tool name for an AI draft (also recorded in "
                                  "authoring.ai_use_declaration.tools)")
    p.add_argument("--tool-version", help="the tool's version, as the researcher states it")
    p.add_argument("--stage", choices=list(P.AI_USE_STAGES),
                   help=f"research stage of this AI use (default {P.DEFAULT_AI_STAGE})")

    p = sub.add_parser("validate", help="report-only validation (for one route)")
    p.add_argument("path", nargs="?", default=None)
    p.add_argument("--route")
    p.add_argument("--sub-profile")
    p.add_argument("--structure-profile", help="a 7SSA structure profile (overrides routing.structure_profiles)")
    p.add_argument("--json", action="store_true")
    p.add_argument("--as-of")

    p = sub.add_parser("explain", help="explain a rule id or a field id")
    p.add_argument("rule_id", metavar="RULE_ID|FIELD_ID")

    p = sub.add_parser("build", help="render exactly one build/<route output file> (same as `route build`)")
    p.add_argument("path", nargs="?", default=None)
    p.add_argument("--route")
    p.add_argument("--sub-profile")
    p.add_argument("--out")
    p.add_argument("--as-of")

    p = sub.add_parser("fields", help="list fields: NRIIS boxes in entry order then NOT_ON_TAB, or with --route "
                                      "that route's placement order then NOT_PLACED")
    p.add_argument("--route")
    p.add_argument("--tab")
    p.add_argument("--required", action="store_true")

    sub.add_parser("profiles", help="list form profiles (every one NEEDS_VERIFICATION)")
    cmd_explain_field.register(sub)
    cmd_review.register(sub)
    cmd_route.register(sub)

    a = ap.parse_args(argv)
    try:
        rc = cmd_review.run(a)
        if rc is not None:
            return rc
        rc = cmd_route.run(a)
        if rc is not None:
            return rc
        if a.cmd == "explain-field":
            return cmd_explain_field.run(a)
        if a.cmd == "profiles":
            from grantthai.mapping import form_profile as FP
            for pid in FP.profile_ids():
                print(json.dumps(FP.describe(pid), ensure_ascii=False))
            return 0
        if a.cmd == "init":
            api.new_work(a.work_id, a.work_type, a.fund, a.mode, path=a.path)
            print(f"wrote {a.path}")
            return 0
        if a.cmd == "migrate":
            res = api.migrate(P.discover(a.path), rename=a.rename, dry_run=a.dry_run)
            print(json.dumps(res, ensure_ascii=False, indent=2))
            return 0
        if a.cmd == "set":
            prov = {"provenance_class": a.provenance_class} if a.provenance_class else None
            rec = api.set_field(P.discover(a.project), a.field_id, _value(a.value, a.string),
                                actor="ai_assisted" if a.ai else "human", chain_node=a.chain_node,
                                provenance=prov, source_ids=a.source_ids, tool=a.tool,
                                tool_version=a.tool_version, stage=a.stage)
            print(f"{rec['field_id']}: {rec['status']}")
            return 0
        if a.cmd == "validate":
            rep = api.validate(a.path, as_of=a.as_of, route=a.route, sub_profile=a.sub_profile,
                               structure_profile=a.structure_profile)
            return cmd_route.print_report(rep, a.json, a.route)
        if a.cmd == "explain":
            print(json.dumps(cmd_explain_field.explain_any(a.rule_id), ensure_ascii=False, indent=2))
            return 0
        if a.cmd == "build":
            out = api.build(a.path, route=a.route, sub_profile=a.sub_profile, out_dir=a.out, as_of=a.as_of)
            print(str(out))
            return 0
        if a.cmd == "fields":
            for f in api.list_fields(tab=a.tab, required_only=a.required, route=a.route):
                print(f"{f['tab']}.{f['entry_order']}\t{f['field_id']}\t{f['type']}\t"
                      f"{'required' if f['required'] else 'optional'}\t{f['label_en']}")
            return 0
    except (ValueError, KeyError, FileExistsError, FileNotFoundError, RuntimeError, PermissionError) as exc:
        print(f"grantthai: error: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    sys.exit(main())
