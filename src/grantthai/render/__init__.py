"""grantthai.render — renderers, one per output route, and the dispatch.

    build_route(path, route=None, *, sub_profile=None, out_dir=None, as_of=None) -> Path
    render_route(raw, project_dir, *, route, sub_profile=None, as_of=None) -> (text, Result)

One work object in, exactly one file out per invocation:
<out_dir or the object's directory/build>/<route output filename>. A build
writes that one file and touches no other file, so building route B next to
route A's output leaves A's file byte-identical.

The nriis-proposal route renders through grantthai.render.submission
(unchanged; byte-identical to the pre-router output). Every other route is
rendered by the module named in RENDERERS, which exposes
    render(raw, project_dir, *, route, sub_profile, as_of) -> (text, engine.Result)
where `route` is a grantthai.routes.registry.Route. A route whose renderer
module is not present in this build raises RouteError; nothing is written.

This package MUST NEVER import grantthai.assist, grantthai.mcp,
grantthai.api, or any LLM SDK (openai, anthropic, google.generativeai,
etc.). Enforced by tools/ci/check_no_ai_import.py.
"""
from __future__ import annotations

import importlib
from pathlib import Path

RENDERERS = {
    "academic-article": "grantthai.render.article",
    "concept-note": "grantthai.render.concept_note",
}


def _render_nriis(raw: dict, project_dir: Path | None, *, route, sub_profile, as_of):
    from grantthai.render import submission as S
    from grantthai.validators import engine as E

    result = E.run(raw, project_dir, as_of, route=route.id, sub_profile=sub_profile)
    text = S._env().get_template(S.TEMPLATE).render(**S.build_context(raw, result))
    return text, result


def render_route(raw: dict, project_dir: Path | None = None, *, route: str, sub_profile: str | None = None,
                 as_of: str | None = None):
    """Render one route for a loaded object; returns (text, engine.Result)."""
    from grantthai.core import project as P
    from grantthai.routes import registry as R
    from grantthai.routes import resolve as RS

    rt = R.load(route)
    sp = RS.resolve_sub_profile(raw, rt, sub_profile)
    if rt.id == P.LEGACY_ROUTE:
        return _render_nriis(raw, project_dir, route=rt, sub_profile=sp, as_of=as_of)
    modname = RENDERERS.get(rt.id)
    try:
        mod = importlib.import_module(modname) if modname else None
    except ModuleNotFoundError as exc:
        if exc.name != modname:
            raise
        mod = None
    if mod is None:
        raise R.RouteError(f"route {rt.id!r} has no renderer in this build yet; nothing was written")
    return mod.render(raw, project_dir, route=rt, sub_profile=sp, as_of=as_of)


def build_route(path: str | Path | None = None, route: str | None = None, *, sub_profile: str | None = None,
                out_dir: str | Path | None = None, as_of: str | None = None) -> Path:
    """Discover the one input (work.yaml, else project.yaml; both present ->
    TwoCanonicalInputs), resolve the route (AmbiguousRoute when a person must
    choose), render, and write exactly one file. Always renders: BLOCK
    findings are listed in the file's readiness summary."""
    from grantthai.core import project as P
    from grantthai.routes import registry as R
    from grantthai.routes import resolve as RS

    src = P.discover(path).resolve()
    raw = P.load(src)
    rid = RS.resolve_route(raw, route)
    text, _ = render_route(raw, src.parent, route=rid, sub_profile=sub_profile, as_of=as_of)
    out = Path(out_dir) if out_dir else src.parent / "build"
    out.mkdir(parents=True, exist_ok=True)
    target = out / R.load(rid).output_filename
    target.write_text(text, encoding="utf-8", newline="\n")
    return target
