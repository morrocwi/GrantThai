"""grantthai.routes.registry — load routes/INDEX.yaml and route.yaml files.

Loading is lazy: a route file is read and validated against
spec/routes/route.schema.json only when that route is asked for. A route
whose INDEX status is `planned` has no file and cannot be loaded.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import yaml

from grantthai.core import project as P

INDEX_REL = "routes/INDEX.yaml"
ROUTE_SCHEMA_ID = "https://github.com/morrocwi/GrantThai/spec/routes/route.schema.json"
ALL = "all"


class RouteError(ValueError):
    """A route file is missing, planned, or fails its contract."""


class RouteNotFound(RouteError, KeyError):
    """No route in routes/INDEX.yaml has this id."""

    def __str__(self) -> str:  # KeyError would quote the message
        return self.args[0] if self.args else ""


@dataclass(frozen=True)
class Route:
    """One validated route.yaml. `raw` is the file's mapping."""
    id: str
    raw: dict

    @property
    def version(self) -> str:
        return str(self.raw.get("version"))

    @property
    def status(self) -> str:
        return str(self.raw.get("status"))

    @property
    def output_filename(self) -> str:
        return self.raw["output"]["filename"]

    @property
    def template(self) -> str:
        return self.raw["output"]["template"]

    @property
    def renderer_version(self) -> str:
        return str(self.raw["output"].get("renderer_version"))

    @property
    def needs_fund_binding(self) -> bool:
        return bool(self.raw.get("needs_fund_binding"))

    @property
    def accepts_work_types(self) -> tuple[str, ...]:
        return tuple(self.raw.get("accepts_work_types") or [])

    @property
    def default_for_work_types(self) -> tuple[str, ...]:
        return tuple(self.raw.get("default_for_work_types") or [])

    @property
    def required_fields(self):
        """"registry" (registry flags plus the form profile, the NRIIS rule)
        or a list of field ids (the route's own S001 BLOCK set)."""
        rf = self.raw.get("required_fields")
        return rf if rf == "registry" else tuple(rf or [])

    @property
    def include_families(self) -> frozenset:
        return frozenset((self.raw.get("rules") or {}).get("include_families") or [])

    @property
    def exclude_ids(self) -> frozenset:
        return frozenset((self.raw.get("rules") or {}).get("exclude_ids") or [])

    @property
    def ready_flag(self) -> str:
        return str((self.raw.get("readiness") or {}).get("ready_flag"))

    @property
    def always_hold(self) -> bool:
        return bool((self.raw.get("readiness") or {}).get("always_hold"))

    @property
    def sub_profile_default(self) -> str | None:
        sp = self.raw.get("sub_profiles")
        return sp.get("default") if isinstance(sp, dict) else None

    @property
    def sub_profile_dir(self) -> str | None:
        sp = self.raw.get("sub_profiles")
        return sp.get("dir") if isinstance(sp, dict) else None

    @property
    def placement(self) -> str | None:
        return self.raw.get("placement")

    @property
    def route_notice_en(self) -> str | None:
        return self.raw.get("route_notice_en")

    @property
    def exports(self) -> tuple[dict, ...]:
        """Optional alternative output formats (route.yaml `exports`)."""
        return tuple(e for e in self.raw.get("exports") or [] if isinstance(e, dict))

    def export(self, fmt: str) -> dict:
        for e in self.exports:
            if e.get("format") == fmt:
                return e
        known = ", ".join(e.get("format") for e in self.exports) or "none"
        raise RouteError(f"route {self.id} has no --format {fmt} export (formats: md, {known}); nothing was written")


@lru_cache(maxsize=None)
def index() -> dict:
    doc = P._read_yaml(INDEX_REL) or {}
    if not isinstance(doc, dict) or not isinstance(doc.get("routes"), list):
        raise RouteError(f"{INDEX_REL}: no `routes` list")
    return doc


def _entries() -> dict:
    return {e["id"]: e for e in index()["routes"] if isinstance(e, dict) and e.get("id")}


def route_ids(*, include_planned: bool = False) -> tuple[str, ...]:
    """Route ids in INDEX order; planned routes only when asked for."""
    return tuple(e["id"] for e in index()["routes"]
                 if isinstance(e, dict) and (include_planned or e.get("status") != "planned"))


@lru_cache(maxsize=None)
def load(route_id: str) -> Route:
    entries = _entries()
    if route_id not in entries:
        raise RouteNotFound(f"unknown route {route_id!r} (known: {', '.join(route_ids(include_planned=True))})")
    entry = entries[route_id]
    if entry.get("status") == "planned":
        raise RouteError(f"route {route_id!r} is planned and has no route file yet")
    rel = entry.get("path") or ""
    path = P.DATA_ROOT / rel
    if ".." in rel.split("/") or not path.is_file():
        raise RouteError(f"route {route_id!r}: no route file at {rel}")
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    errs = P.schema_errors(raw, ROUTE_SCHEMA_ID)
    if errs:
        raise RouteError(f"{rel}: " + "; ".join(errs))
    if raw.get("id") != route_id:
        raise RouteError(f"{rel}: id {raw.get('id')!r} does not equal the INDEX id {route_id!r}")
    return Route(route_id, raw)


def list_routes() -> list[dict]:
    """Every route in routes/INDEX.yaml, in INDEX order: id, title, output
    filename, accepted work types, status. A planned route is listed with
    its INDEX data only; a route whose file fails its contract is listed
    with `error` set. Listing never picks a route."""
    out = []
    for e in index()["routes"]:
        row = {"id": e["id"], "status": e.get("status"), "version": str(e.get("version")),
               "output_filename": e.get("output_filename"), "title_en": None,
               "accepts_work_types": [], "default_for_work_types": [], "needs_fund_binding": None,
               "ready_flag": None, "error": None}
        if e.get("status") != "planned":
            try:
                r = load(e["id"])
            except RouteError as exc:     # listed, never hidden; building it raises the same error
                row["error"] = str(exc)
                out.append(row)
                continue
            row.update({"title_en": r.raw.get("title_en"), "output_filename": r.output_filename,
                        "accepts_work_types": list(r.accepts_work_types),
                        "default_for_work_types": list(r.default_for_work_types),
                        "needs_fund_binding": r.needs_fund_binding, "ready_flag": r.ready_flag})
        out.append(row)
    return out


def rule_declares(route: Route, rule: dict) -> bool:
    """The rule's own `routes` names this route or `all` (default all)."""
    routes = rule.get("routes") or [ALL]
    return ALL in routes or route.id in routes


def route_config_admits(route: Route, rule: dict) -> bool:
    """The route's `rules` block admits the rule (family included, id not
    excluded)."""
    return rule.get("family") in route.include_families and rule.get("id") not in route.exclude_ids


def in_scope(route: Route, rule: dict) -> bool:
    """spec §4.1: evaluated only if the family is included, the id is not
    excluded, and the rule's `routes` names the route or all."""
    return rule_declares(route, rule) and route_config_admits(route, rule)
