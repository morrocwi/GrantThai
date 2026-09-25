"""grantthai.routes.resolve — which route and sub-profile a build uses.

Resolution order (spec §2.3):
  1. the explicit route (--route / route=);
  2. routing.default_route in the work object;
  3. a legacy 0.2 project.yaml -> nriis-proposal;
  3a. routing.declared_routes, when the researcher declared any: exactly one
      declared route -> that route; several -> stop and list the declared
      routes (AmbiguousRoute). The work_type default never overrides what a
      person declared (clarification of spec §2.3, docs/deviations.md);
  4. only when nothing is declared: exactly one route lists the object's
     work_type in default_for_work_types;
  5. otherwise stop and list the candidates (AmbiguousRoute; CLI exit 2).
The tool never picks between routes: that choice is the researcher's.
"""
from __future__ import annotations

from grantthai.core import project as P
from grantthai.routes import registry as R


class AmbiguousRoute(ValueError):
    """No route can be resolved without a person choosing one."""

    def __init__(self, message: str, candidates: list[str]):
        super().__init__(message)
        self.candidates = list(candidates)


def resolve_route(doc: dict, route: str | None = None) -> str:
    """The route id for `doc` (a loaded work.yaml or project.yaml)."""
    if route:
        R.load(route)          # unknown or planned -> RouteError
        return route
    view = P.work_view(doc)
    if view["default_route"]:
        R.load(view["default_route"])
        return view["default_route"]
    declared = [r for r in view["declared_routes"] if isinstance(r, str) and r.strip()]
    if len(declared) == 1:
        R.load(declared[0])
        return declared[0]
    if declared:
        raise AmbiguousRoute(
            f"no route chosen for {view['work_id']}: routing.declared_routes lists {', '.join(declared)} and "
            "no routing.default_route; choose one with --route or set routing.default_route; GrantThai never "
            "picks a route", declared)
    wt = view["work_type"]
    ids = R.route_ids()
    defaults = [rid for rid in ids if wt in R.load(rid).default_for_work_types]
    if len(defaults) == 1:
        return defaults[0]
    candidates = [rid for rid in ids if wt in R.load(rid).accepts_work_types] or list(ids)
    raise AmbiguousRoute(
        f"no route chosen for {view['work_id']} (work_type {wt}): choose one with --route "
        f"({', '.join(candidates)}) or set routing.default_route; GrantThai never picks a route", candidates)


def resolve_sub_profile(doc: dict, route: R.Route | str, sub_profile: str | None = None) -> str | None:
    """--sub-profile, else routing.sub_profiles[route] (for nriis-proposal a
    legacy top-level form_profile is read too), else the route's default
    (null for nriis-proposal = the observed form)."""
    r = route if isinstance(route, R.Route) else R.load(route)
    if sub_profile:
        return sub_profile
    subs = P.work_view(doc)["sub_profiles"]
    if r.id in subs:
        return subs[r.id]
    return r.sub_profile_default
