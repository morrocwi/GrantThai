"""grantthai.routes — the router: one work object, many output routes.

"Router" here means a deterministic OUTPUT ROUTE chosen by a person (the
researcher), never a choice made by an AI (decision K-R1). A route is
declared as data in routes/<id>/route.yaml and listed in routes/INDEX.yaml.
Each build through a route writes exactly one file,
build/<route output filename>. NRIIS is one route among several.

    registry.list_routes() -> list[dict]      # every INDEX entry, planned ones included
    registry.load(route_id) -> Route          # validated route.yaml (lazy, one file per route)
    registry.in_scope(route, rule) -> bool    # rule scoping for the validator
    resolve.resolve_route(doc, route=None) -> str            # resolution order; AmbiguousRoute
    resolve.resolve_sub_profile(doc, route, sub_profile=None) -> str | None

This package MUST NEVER import grantthai.assist, grantthai.mcp,
grantthai.api, or any LLM SDK. Enforced by tools/ci/check_no_ai_import.py.
"""
from grantthai.routes.registry import Route, RouteError, RouteNotFound, list_routes, load, route_ids
from grantthai.routes.resolve import AmbiguousRoute, resolve_route, resolve_sub_profile

__all__ = ["Route", "RouteError", "RouteNotFound", "AmbiguousRoute", "list_routes", "load", "route_ids",
           "resolve_route", "resolve_sub_profile"]
