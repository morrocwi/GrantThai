"""grantthai.cli.cmd_review — local-CLI-only review, mapping acceptance,
lock, diff and status-linking commands (v0.2 module C).

    grantthai link PROJECT [--as-of YYYY-MM-DD]
    grantthai review PROJECT --as ROLE --name NAME --gate RGn
                     --scope F1,F2|@chain:Node --independence self|independent
                     [--outcome HUMAN_REVIEWED|VERIFIED] [--basis TEXT] --date YYYY-MM-DD
    grantthai accept-mapping PROJECT ID --name NAME --date YYYY-MM-DD [--role ROLE] [--basis TEXT]
    grantthai reject-mapping PROJECT ID --name NAME --date YYYY-MM-DD [--role ROLE] [--basis TEXT]
    grantthai lock PROJECT --by NAME --date YYYY-MM-DD [--as-of YYYY-MM-DD]
    grantthai diff A B [--json]

`register(subparsers)` adds these to the main parser; `run(args)` executes
one of them and returns an exit code, or None when `args.cmd` is not one
of ours. Nothing here is reachable over MCP or REST (see
grantthai.review). `link` persists the deterministic validator's
STRUCTURE_CHECKED / LOGIC_LINKED statuses (spec/common/status.yaml says the
local `validate` does this; the integrator may fold `link` into it).

This module MUST NEVER import grantthai.assist, grantthai.mcp,
grantthai.api, or any LLM SDK. Enforced by tools/ci/check_no_ai_import.py.
"""
from __future__ import annotations

import json
from pathlib import Path

from grantthai.core import project as P
from grantthai.review import diff as D
from grantthai.review import lock as L
from grantthai.review import mapping as M
from grantthai.review import records as R
from grantthai.validators import engine as E

COMMANDS = ("link", "review", "accept-mapping", "reject-mapping", "lock", "diff")


def register(subparsers) -> None:
    p = subparsers.add_parser("link", help="persist STRUCTURE_CHECKED / LOGIC_LINKED from a local validator run")
    p.add_argument("project")
    p.add_argument("--as-of")

    p = subparsers.add_parser("review", help="write a named review record for one gate (named human only)")
    p.add_argument("project")
    p.add_argument("--as", dest="role", required=True, help="reviewer role, e.g. pi, co-researcher, external")
    p.add_argument("--name", required=True, help="reviewer name (a review is a named human act)")
    p.add_argument("--gate", required=True, choices=list(R.GATES))
    p.add_argument("--scope", required=True, help="F1,F2 or @chain:Node")
    p.add_argument("--independence", required=True, choices=list(R.INDEPENDENCE))
    p.add_argument("--outcome", choices=list(R.OUTCOMES))
    p.add_argument("--basis")
    p.add_argument("--date", required=True, help="YYYY-MM-DD")

    for name, help_ in (("accept-mapping", "accept a mapping proposal (named human only)"),
                        ("reject-mapping", "reject a mapping proposal back to PROPOSED")):
        p = subparsers.add_parser(name, help=help_)
        p.add_argument("project")
        p.add_argument("mapping_id")
        p.add_argument("--name", required=True)
        p.add_argument("--date", required=True)
        p.add_argument("--role", default="reviewer")
        p.add_argument("--basis")

    p = subparsers.add_parser("lock", help="apply the object LOCK (named human only)")
    p.add_argument("project")
    p.add_argument("--by", required=True, help="name of the person locking")
    p.add_argument("--date", required=True)
    p.add_argument("--as-of")

    p = subparsers.add_parser("diff", help="compare two project.yaml files (content, statuses, stale reviews, lock)")
    p.add_argument("a")
    p.add_argument("b")
    p.add_argument("--json", action="store_true")


def run(a) -> int | None:
    """Execute one of this module's commands. Raises ValueError /
    PermissionError for the main CLI to report; returns None if `a.cmd`
    is not ours."""
    if a.cmd not in COMMANDS:
        return None
    if a.cmd == "diff":
        out = D.diff(P.load(a.a), P.load(a.b))
        if a.json:
            print(json.dumps(out, ensure_ascii=False, indent=2))
        else:
            print(f"content changed: {'yes' if out['content_changed'] else 'no'}")
            for fc in out["field_changes"]:
                print(f"  {fc['change']} {fc['field_id']}" + (f" ({', '.join(fc['keys'])})" if fc["keys"] else ""))
            for sc in out["status_changes"]:
                print(f"  status {sc['field_id']}: {sc['from']} -> {sc['to']}")
            for mc in out["mapping_changes"]:
                print(f"  mapping {mc['id']}: {mc['from']} -> {mc['to']}")
            print(f"stale reviews: {', '.join(out['stale_reviews']) or 'none'}")
            print(f"lock: {out['lock']['a']} -> {out['lock']['b']}")
        return 0

    path = Path(a.project).resolve()
    doc = P.load(path)
    if a.cmd == "link":
        res = E.run(doc, path.parent, a.as_of)
        changed = R.link_statuses(doc, res.findings)
        P.save(doc, path)
        for fid, st in changed.items():
            print(f"{fid}: {st}")
        print(f"{len(changed)} status change(s); BLOCK {res.report['summary']['block']}")
        return 0
    if a.cmd == "review":
        rec = R.add_review(doc, gate_id=a.gate, reviewer_name=a.name, reviewer_role=a.role,
                           scope=a.scope, independence=a.independence, outcome=a.outcome,
                           basis=a.basis, date=a.date)
        P.save(doc, path)
        shown = "AUTHOR_CHECKED" if (rec["independence"] == "self" and rec["outcome"] == "VERIFIED") else rec["outcome"]
        print(f"{rec['gate_id']}: {shown} ({rec['independence']} review by {rec['reviewer_role']}, "
              f"{rec['date']}); content_sha256 {rec['content_sha256'][:12]}")
        return 0
    if a.cmd in ("accept-mapping", "reject-mapping"):
        fn = M.accept if a.cmd == "accept-mapping" else M.reject
        m = fn(doc, a.mapping_id, reviewer_name=a.name, date=a.date, reviewer_role=a.role, basis=a.basis)
        P.save(doc, path)
        print(f"{m['id']}: {m['acceptance_state']}")
        return 0
    if a.cmd == "lock":
        rep = E.run(doc, path.parent, a.as_of).report
        lk = L.lock(doc, locked_by=a.by, date=a.date, validation=rep)
        P.save(doc, path)
        print(f"locked by {lk['locked_by']} on {lk['locked_at']}; content_sha256 {lk['locked_content_sha256']}")
        return 0
    return None
