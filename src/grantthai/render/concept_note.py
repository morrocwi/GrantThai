"""grantthai.render.concept_note — renders build/RESEARCH_CONCEPT_NOTE.md,
the one output of the concept-note route, per
spec/output/research-concept-note.contract.md.

    render(raw, project_dir, *, route, sub_profile, as_of) -> (text, engine.Result)

A concept note is a pre-proposal working document: never submittable to any
system (the route's readiness.always_hold), never a replacement for the
NRIIS route. Called through grantthai.render.build_route (one file per
invocation). Deterministic; values print exactly as the researcher wrote
them, with the same formatting as every other route (shared-core fields
print identically). The concept-note route has no sub-profiles; a
sub-profile passed to it is ignored and the frontmatter says null.

This module MUST NEVER import grantthai.assist, grantthai.mcp,
grantthai.api, or any LLM SDK (tools/ci/check_no_ai_import.py).
"""
from __future__ import annotations

from pathlib import Path

import yaml

from grantthai import __version__
from grantthai.core import project as P
from grantthai.core.object_hash import state_sha256
from grantthai.render import article as A
from grantthai.validators import engine as E


def render(raw: dict, project_dir: Path | None = None, *, route, sub_profile=None, as_of=None):
    result = E.run(raw, project_dir, as_of, route=route.id, sub_profile=None)
    ctx = A.common_context(raw, result, route, placement=A.read_placement(route))
    summary = ctx["summary"]
    frontmatter = {
        "grantthai_version": __version__,
        "schema_version": str(raw.get("schema_version")),
        "renderer_version": route.renderer_version,
        "route": route.id,
        "work_id": P.work_id(raw),
        "work_type": ctx["view"]["work_type"],
        "work_content_sha256": ctx["csha"],
        "work_state_sha256": state_sha256(raw),
        "work_locked": ctx["locked"],
        "authoring": ctx["authoring_fm"],
        "submission_mode": {"human_copy_paste": True, "ai_assisted_fill": False, "direct_submit": False},
        "human_final_approval_required": True,
        "review": ctx["gates"],
        # readiness.always_hold: a concept note is never submittable.
        route.ready_flag: False if route.always_hold else (summary["block"] == 0 and not ctx["hold_reasons"]),
        "hold_reasons": ctx["hold_reasons"],
        "validation_summary": dict(summary),
        "disclaimer": P.notice_constant(),
        "route_notice": route.route_notice_en or "",
    }
    context = {k: ctx[k] for k in ("summary", "hold_reasons", "blocks", "reviews", "infos", "needs_input",
                                   "record_needs_input", "marked", "ai_drafts", "sections", "meta_yaml", "gates",
                                   "sources", "unresolved", "unmapped", "ai_decl", "trust_level", "fictional")}
    context.update({
        "frontmatter_yaml": yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True,
                                           width=10**6).rstrip("\n"),
        "disclaimer": P.notice_constant(),
        "route_notice": route.route_notice_en or "",
        "work_id": P.work_id(raw),
        "route_id": route.id,
        "work_type": ctx["view"]["work_type"],
    })
    text = A._env().get_template(Path(route.template).name).render(**context)
    return text, result
