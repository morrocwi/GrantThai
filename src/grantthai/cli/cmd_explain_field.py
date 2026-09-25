"""grantthai.cli.cmd_explain_field — `grantthai explain FIELD_ID` (v0.2).

Module A ships this file; the integrator wires it into
`grantthai.cli.__init__` (see `register` and `explain_any`). Until then the
subcommand `explain-field` is also registered so the module can be used and
tested on its own.

    grantthai explain FIELD_ID      -> registry record + writing intent
    grantthai explain RULE_ID       -> unchanged (validators.engine.explain)
    grantthai explain-field FIELD_ID

Never imports grantthai.assist, grantthai.mcp, grantthai.api or an LLM SDK.
"""
from __future__ import annotations

import argparse
import json

from grantthai.guidance import writing
from grantthai.validators import engine as _E


def explain_any(arg: str) -> dict:
    """Route one `explain` argument: a field id (registry pattern) goes to
    the writing layer, anything else keeps today's rule-id behaviour."""
    if writing.FIELD_ID_RE.match(arg):
        return writing.explain_field(arg)
    return _E.explain(arg)


def run(args: argparse.Namespace) -> int:
    print(json.dumps(writing.explain_field(args.field_id), ensure_ascii=False, indent=2))
    return 0


def register(subparsers) -> None:
    p = subparsers.add_parser("explain-field", help="explain a field id: registry record plus writing intent")
    p.add_argument("field_id")
    p.set_defaults(func=run)
