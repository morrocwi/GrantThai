"""grantthai.mapping.form_profile — form profiles (v0.2).

A form profile (`mappings/nriis/form_profiles/<id>.yaml`,
`spec/mappings/form_profile.schema.json`) describes one proposal form type or
funding-unit template read from a cited public document. A project selects
one with the optional top-level `form_profile` key of project.yaml; absent or
null means the observed form (`mappings/nriis/section_to_tab.yaml`),
unchanged.

A profile can only:

* add required fields (`require`), on top of the registry's `required` flags;
* restrict (`render_only`) or drop (`hide`) the fields rendered on the tabs;
* override the tab order (`tab_order`);
* list form items GrantThai has no registry field for (`extra_items`); and
* list candidate budget rules (`budget_rules`), which are never evaluated.

Every profile is NEEDS_VERIFICATION (founder ruling K14). Nothing here
touches field status or object hashes; `form_profile` is project content, so
setting it changes `content_sha256` (spec/common/object-hash.md).

This package MUST NEVER import grantthai.assist, grantthai.mcp,
grantthai.api, or any LLM SDK. Enforced by tools/ci/check_no_ai_import.py.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from grantthai.core import project as P

SCHEMA_ID = "https://github.com/morrocwi/GrantThai/spec/mappings/form_profile.schema.json"
PROFILES_REL = "mappings/nriis/form_profiles"
PROJECT_KEY = "form_profile"


class FormProfileError(ValueError):
    """A profile file is missing, malformed, or references an unknown field."""


class FormProfileNotFound(FormProfileError, KeyError):
    """No shipped profile has this id."""


@dataclass(frozen=True)
class ProfileView:
    """What the validator and renderer read for one project.

    `required` — every registry field id that must have a value: the
    registry's own `required: true` fields plus the profile's `require`,
    minus the profile's `hide` (a hidden field is never required).
    `rendered` — registry field ids, in registry order, that the renderer may
    place on a tab: all of them, or `render_only`, minus `hide`.
    `tab_order` — the profile's override or section_to_tab.yaml's order.
    `extra_items`, `budget_rules` — copied from the profile, for display only.
    `profile_id` — the profile in force, or None for the observed form.
    """
    profile_id: str | None
    required: frozenset[str]
    rendered: tuple[str, ...]
    tab_order: tuple[str, ...]
    extra_items: tuple[dict, ...]
    budget_rules: tuple[dict, ...]
    status_marker: str = "NEEDS_VERIFICATION"

    @property
    def profile_required(self) -> frozenset[str]:
        """Fields required only because of the profile (not by the registry)."""
        return self.required - _registry_required()


def profiles_dir() -> Path:
    return P.DATA_ROOT / PROFILES_REL


def profile_ids() -> tuple[str, ...]:
    """Ids of every shipped profile, sorted."""
    d = profiles_dir()
    if not d.is_dir():
        return ()
    return tuple(sorted(p.name[: -len(".yaml")] for p in d.glob("*.yaml")))


def check(profile: dict) -> list[str]:
    """Problems with a profile object: schema errors, unknown field ids, an
    id that does not match the pattern, a hidden field also required or
    render_only, a budget rule that claims to be evaluable. Empty = ok."""
    errs = list(P.schema_errors(profile, SCHEMA_ID))
    if errs:
        return errs
    known = set(P.registry_by_id())
    refs: list[tuple[str, str]] = []
    refs += [("require", f) for f in profile.get("require") or []]
    refs += [("hide", f) for f in profile.get("hide") or []]
    refs += [("render_only", f) for f in profile.get("render_only") or []]
    refs += [("require_basis", f) for f in profile.get("require_basis") or {}]
    for item in profile.get("extra_items") or []:
        refs += [("extra_items.nearest_field_ids", f) for f in item.get("nearest_field_ids") or []]
    for where, fid in refs:
        if fid not in known:
            errs.append(f"{where}: {fid} is not in registry/fields.jsonl")
    hide = set(profile.get("hide") or [])
    for fid in profile.get("require") or []:
        if fid in hide:
            errs.append(f"require: {fid} is also listed under hide")
    for fid in profile.get("render_only") or []:
        if fid in hide:
            errs.append(f"render_only: {fid} is also listed under hide")
    basis = profile.get("require_basis") or {}
    for fid in basis:
        if fid not in (profile.get("require") or []):
            errs.append(f"require_basis: {fid} is not under require")
    return sorted(errs)


@lru_cache(maxsize=None)
def _load_cached(profile_id: str) -> dict:
    path = profiles_dir() / f"{profile_id}.yaml"
    if "/" in profile_id or "\\" in profile_id or not path.is_file():
        raise FormProfileNotFound(profile_id)
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise FormProfileError(f"{path.name}: not a mapping")
    if raw.get("id") != profile_id:
        raise FormProfileError(f"{path.name}: id {raw.get('id')!r} does not match the file name")
    errs = check(raw)
    if errs:
        raise FormProfileError(f"{path.name}: " + "; ".join(errs))
    return raw


def load(profile_id: str) -> dict:
    """The validated profile object for `profile_id` (a fresh copy).
    Raises FormProfileNotFound for an unknown id and FormProfileError for a
    file that fails its contract."""
    import copy
    return copy.deepcopy(_load_cached(profile_id))


@lru_cache(maxsize=None)
def _registry_required() -> frozenset[str]:
    return frozenset(r["field_id"] for r in P.registry() if r.get("required"))


@lru_cache(maxsize=None)
def _registry_order() -> tuple[str, ...]:
    return tuple(r["field_id"] for r in P.registry())


def default_tab_order() -> tuple[str, ...]:
    return tuple(P.tab_mapping().get("tab_order") or [])


def view(profile: dict | None) -> ProfileView:
    """Build the ProfileView for a profile object (None = observed form).
    The object is checked first; a bad one raises FormProfileError."""
    if profile is None:
        return ProfileView(
            profile_id=None,
            required=_registry_required(),
            rendered=_registry_order(),
            tab_order=default_tab_order(),
            extra_items=(),
            budget_rules=(),
        )
    errs = check(profile)
    if errs:
        raise FormProfileError("; ".join(errs))
    hide = set(profile.get("hide") or [])
    only = profile.get("render_only")
    rendered = tuple(f for f in _registry_order()
                     if f not in hide and (only is None or f in set(only)))
    required = (_registry_required() | set(profile.get("require") or [])) - hide
    return ProfileView(
        profile_id=str(profile["id"]),
        required=frozenset(required),
        rendered=rendered,
        tab_order=tuple(profile.get("tab_order") or default_tab_order()),
        extra_items=tuple(dict(x) for x in profile.get("extra_items") or []),
        budget_rules=tuple(dict(x) for x in profile.get("budget_rules") or []),
    )


def selected(doc: dict) -> str | None:
    """The profile id a project.yaml object selects, or None."""
    v = doc.get(PROJECT_KEY)
    return None if v in (None, "") else str(v)


def resolve(doc: dict) -> ProfileView:
    """The ProfileView for a project.yaml object. `form_profile` absent or
    null = observed form. An unknown id raises FormProfileNotFound; the
    validator turns that into a SCHEMA finding rather than crashing."""
    pid = selected(doc)
    return view(None if pid is None else load(pid))


def describe(profile_id: str) -> dict[str, Any]:
    """A small, deterministic summary of one profile for CLI/README use."""
    p = load(profile_id)
    v = view(p)
    return {
        "id": p["id"],
        "title_en": p["title_en"],
        "status_marker": p["status_marker"],
        "source": dict(p["source"]),
        "adds_required": sorted(v.profile_required),
        "hides": sorted(p.get("hide") or []),
        "render_only": None if p.get("render_only") is None else sorted(p["render_only"]),
        "tab_order": list(v.tab_order),
        "extra_items": len(v.extra_items),
        "budget_rules": [r["id"] for r in v.budget_rules],
    }
