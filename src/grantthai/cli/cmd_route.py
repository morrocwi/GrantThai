"""grantthai route list | check | build — the output router (v0.3).

    grantthai route list [--json]
    grantthai route check --route ID [PATH] [--sub-profile SP] [--json] [--as-of D]
    grantthai route build --route ID [PATH] [--sub-profile SP] [--out DIR] [--as-of D]

A route is always chosen by a person. `route list` only lists; `check` and
`build` require --route. `grantthai build [PATH] --route ID` is the same as
`route build`. Ambiguity, an unknown route and two canonical inputs in one
directory all exit 2.

This module MUST NEVER import grantthai.assist, grantthai.mcp,
grantthai.api, or any LLM SDK. Enforced by tools/ci/check_no_ai_import.py.
"""
from __future__ import annotations

import json

from grantthai import api_py as api


def register(sub) -> None:
    p = sub.add_parser("route", help="output routes: list | check | build (a person chooses the route)")
    rs = p.add_subparsers(dest="route_cmd", required=True)
    q = rs.add_parser("list", help="every route: id, title, output file, accepted work types, status")
    q.add_argument("--json", action="store_true")
    q = rs.add_parser("check", help="route-scoped validation (report-only)")
    q.add_argument("path", nargs="?", default=None, help="work.yaml / project.yaml or its directory")
    q.add_argument("--route", required=True)
    q.add_argument("--sub-profile")
    q.add_argument("--json", action="store_true")
    q.add_argument("--as-of")
    q = rs.add_parser("build", help="render exactly one build/<route output file>")
    q.add_argument("path", nargs="?", default=None, help="work.yaml / project.yaml or its directory")
    q.add_argument("--route", required=True)
    q.add_argument("--sub-profile")
    q.add_argument("--out")
    q.add_argument("--as-of")


def print_report(rep: dict, as_json: bool, route: str | None = None) -> int:
    if as_json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        s = rep["summary"]
        where = f" [route {route}]" if route else ""
        print(f"{rep['project_id']}{where}: BLOCK {s['block']} / REVIEW {s['review']} / INFO {s['info']}")
        for f in rep["findings"]:
            if f["severity"] != "INFO":
                print(f"  {f['severity']} {f['rule_id']}: {f['message_en']}")
    return 1 if rep["summary"]["block"] else 0


def run(a) -> int | None:
    if a.cmd != "route":
        return None
    if a.route_cmd == "list":
        rows = api.list_routes()
        if a.json:
            print(json.dumps(rows, ensure_ascii=False, indent=2))
        else:
            for r in rows:
                print(f"{r['id']}\t{r['status']}\t{r['output_filename']}\t"
                      f"{','.join(r['accepts_work_types']) or '-'}\t"
                      f"{r['title_en'] or ''}{'  ERROR: ' + r['error'] if r['error'] else ''}")
        return 0
    if a.route_cmd == "check":
        rep = api.check_route(a.path, a.route, sub_profile=a.sub_profile, as_of=a.as_of)
        return print_report(rep, a.json, a.route)
    if a.route_cmd == "build":
        print(str(api.build(a.path, route=a.route, sub_profile=a.sub_profile, out_dir=a.out, as_of=a.as_of)))
        return 0
    return 2
