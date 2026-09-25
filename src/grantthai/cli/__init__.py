"""grantthai.cli — the AI-free command line (v0.1 subset).

    grantthai init [PATH] [--project-id ID] [--fund FUND_PROFILE_ID] [--mode MODE]
    grantthai set FIELD_ID VALUE [--project PATH] [--string] [--chain-node NODE]
                  [--source-id SRC-..]... [--provenance-class C] [--ai --tool NAME]
    grantthai validate [PATH] [--json] [--as-of YYYY-MM-DD]
    grantthai explain RULE_ID
    grantthai build [PATH] [--out DIR] [--as-of YYYY-MM-DD]
    grantthai fields [--tab TAB] [--required]

This package MUST NEVER import grantthai.assist, grantthai.mcp,
grantthai.api, or any LLM SDK. Enforced by tools/ci/check_no_ai_import.py.
"""
from __future__ import annotations

import argparse
import json
import sys

from grantthai import __version__
from grantthai import api_py as api
from grantthai.core.object_hash import load_project_text


def _value(text: str, force_string: bool):
    if force_string:
        return text
    try:
        return load_project_text(text)
    except Exception:
        return text


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="grantthai", description="project.yaml -> build/NRIIS_SUBMISSION.md")
    ap.add_argument("--version", action="version", version=f"grantthai {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init", help="write a blank project.yaml")
    p.add_argument("path", nargs="?", default="project.yaml")
    p.add_argument("--project-id", default="NEEDS_INPUT")
    p.add_argument("--fund", default="example/FICTIONAL_CALL@0.1")
    p.add_argument("--mode", default="expert", choices=["expert", "human_direct", "citizen"])

    p = sub.add_parser("set", help="set one field (status becomes DRAFT)")
    p.add_argument("field_id")
    p.add_argument("value", help="YAML value; NEEDS_INPUT clears it")
    p.add_argument("--project", default="project.yaml")
    p.add_argument("--string", action="store_true", help="store VALUE as a string, unparsed")
    p.add_argument("--chain-node")
    p.add_argument("--source-id", action="append", dest="source_ids")
    p.add_argument("--provenance-class", choices=["SOURCE", "INFERENCE", "DECISION", "DERIVED"])
    p.add_argument("--ai", action="store_true", help="the value is an AI draft (stored as ai_draft, never SOURCE)")
    p.add_argument("--tool", help="disclosed tool name for an AI draft")

    p = sub.add_parser("validate", help="report-only validation")
    p.add_argument("path", nargs="?", default="project.yaml")
    p.add_argument("--json", action="store_true")
    p.add_argument("--as-of")

    p = sub.add_parser("explain", help="explain a rule id")
    p.add_argument("rule_id")

    p = sub.add_parser("build", help="render build/NRIIS_SUBMISSION.md")
    p.add_argument("path", nargs="?", default="project.yaml")
    p.add_argument("--out")
    p.add_argument("--as-of")

    p = sub.add_parser("fields", help="list every field: NRIIS boxes in entry order, then NOT_ON_TAB fields")
    p.add_argument("--tab")
    p.add_argument("--required", action="store_true")

    a = ap.parse_args(argv)
    try:
        if a.cmd == "init":
            api.new_project(a.project_id, a.fund, a.mode, path=a.path)
            print(f"wrote {a.path}")
            return 0
        if a.cmd == "set":
            prov = {"provenance_class": a.provenance_class} if a.provenance_class else None
            rec = api.set_field(a.project, a.field_id, _value(a.value, a.string),
                                actor="ai_assisted" if a.ai else "human", chain_node=a.chain_node,
                                provenance=prov, source_ids=a.source_ids, tool=a.tool)
            print(f"{rec['field_id']}: {rec['status']}")
            return 0
        if a.cmd == "validate":
            rep = api.validate(a.path, as_of=a.as_of)
            if a.json:
                print(json.dumps(rep, ensure_ascii=False, indent=2))
            else:
                s = rep["summary"]
                print(f"{rep['project_id']}: BLOCK {s['block']} / REVIEW {s['review']} / INFO {s['info']}")
                for f in rep["findings"]:
                    if f["severity"] != "INFO":
                        print(f"  {f['severity']} {f['rule_id']}: {f['message_en']}")
            return 1 if rep["summary"]["block"] else 0
        if a.cmd == "explain":
            print(json.dumps(api.explain(a.rule_id), ensure_ascii=False, indent=2))
            return 0
        if a.cmd == "build":
            out = api.build(a.path, out_dir=a.out, as_of=a.as_of)
            print(str(out))
            return 0
        if a.cmd == "fields":
            for f in api.list_fields(tab=a.tab, required_only=a.required):
                print(f"{f['tab']}.{f['entry_order']}\t{f['field_id']}\t{f['type']}\t"
                      f"{'required' if f['required'] else 'optional'}\t{f['label_en']}")
            return 0
    except (ValueError, KeyError, FileExistsError, FileNotFoundError, RuntimeError) as exc:
        print(f"grantthai: error: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    sys.exit(main())
