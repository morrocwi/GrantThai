"""grantthai.validators.article — the ART family (academic-article route).

Loaded by grantthai.validators.engine only when the route in force includes
the ART family (routes/academic-article/route.yaml `rules`). Exposes

    EVALUATED  frozenset of the rule ids this module evaluates
    check(ctx) adds findings through ctx.add (engine._Ctx)

Every rule here is structural. None judges whether a manuscript is sound,
novel or publishable, and none rests on a journal fact: journal
requirements are NEEDS_VERIFICATION, so the family has exactly one BLOCK,
ART007 (an AI tool listed as an author), which rests on GrantThai's own
non-negotiable 4. Everything else is REVIEW (severities come from
validators/rules.yaml; nothing is hardcoded here).

Sub-profiles (routes/academic-article/sub_profiles/<id>.yaml) are GrantThai
defaults, NEEDS_VERIFICATION, never venue profiles. A venue value enters
only through the researcher's ARTICLE.VENUE.TARGET.stated_requirements,
and only when the item carries a source_ref that resolves to an entry in
the work object's `sources` (ART010 otherwise). The item names this module
reads are GrantThai's own keys (VENUE_ITEM_* below).

Report-only: nothing here changes the work object.
"""
from __future__ import annotations

import re
from functools import lru_cache
from typing import Any

import yaml

from grantthai.core import project as P

EVALUATED = frozenset(f"ART{n:03d}" for n in range(1, 12))

KIND = "ARTICLE.META.KIND"
AUTHORS = "ARTICLE.FRONT.AUTHORS"
CONTRIB = "ARTICLE.FRONT.CONTRIBUTIONS"
ABSTRACT = {"th": "ARTICLE.FRONT.ABSTRACT_TH", "en": "ARTICLE.FRONT.ABSTRACT_EN"}
KEYWORDS = {"th": "CORE.GENERAL.KEYWORDS_TH", "en": "CORE.GENERAL.KEYWORDS_EN"}
IMRAD = ("ARTICLE.SECTION.INTRODUCTION", "ARTICLE.SECTION.METHODS", "ARTICLE.SECTION.RESULTS",
         "ARTICLE.SECTION.DISCUSSION")
SECTION_TEXT = IMRAD + ("ARTICLE.SECTION.CONCLUSION", "ARTICLE.SECTION.LIMITATIONS")
BODY_SECTIONS = "ARTICLE.BODY.SECTIONS"
FIGURES = "ARTICLE.BODY.FIGURES_TABLES"
REFERENCES = "CORE.NARRATIVE.REFERENCES"
AI_USE = "ARTICLE.STATEMENT.AI_USE"
ETHICS = "ARTICLE.STATEMENT.ETHICS"
VENUE = "ARTICLE.VENUE.TARGET"
TEAM = "PROFILE.TEAM.MEMBERS"

EMPIRICAL = "empirical_research"

# The proposed_default keyword band when neither the sub-profile nor a
# sourced venue item gives one (rules.yaml ART002; NEEDS_VERIFICATION).
DEFAULT_KEYWORD_BAND = (3, 6)
DEFAULT_LANGS = ("en",)

# GrantThai's own item keys in ARTICLE.VENUE.TARGET.stated_requirements that
# ART001/ART002 read (only with a resolvable source_ref). Other items are
# printed, never interpreted.
VENUE_ITEM_ABSTRACT_LANGS = ("abstract_languages",)
VENUE_ITEM_KW_MIN = ("keyword_count_min", "keywords_min")
VENUE_ITEM_KW_MAX = ("keyword_count_max", "keywords_max")

# ART011: a caption discloses an AI-made illustration when it mentions AI,
# "generated", or the disclosed tool's name.
_DISCLOSURE_RE = re.compile(r"(?i)(?<![a-z])(ai|a\.i\.)(?![a-z])|generat|ปัญญาประดิษฐ์|เอไอ")


def _filled(v: Any) -> bool:
    if v is None:
        return False
    if isinstance(v, str):
        return v.strip() not in ("", "NEEDS_INPUT", "NEEDS_VERIFICATION")
    if isinstance(v, (list, dict)):
        return any(_filled(x) for x in (v.values() if isinstance(v, dict) else v))
    return True


def _norm(s: Any) -> str:
    return " ".join(str(s or "").casefold().split())


def _mentions(text: str, name: str) -> bool:
    """`name` (a disclosed tool) appears in `text`, case-insensitive: equal
    after whitespace folding, or as a whole-word run inside it."""
    t, n = _norm(text), _norm(name)
    if not t or not n:
        return False
    if t == n:
        return True
    return re.search(r"(?<!\w)" + re.escape(n) + r"(?!\w)", t) is not None


_PAREN_RE = re.compile(r"[\(\[][^\)\]]*[\)\]]")
_PAREN_INNER_RE = re.compile(r"[\(\[]([^\)\]]*)[\)\]]")


def _tool_variants(name: str) -> list[str]:
    """A disclosed tool name, the name with any parenthetical removed, and
    each parenthetical on its own: 'Tool X (model Y)' -> ['Tool X (model Y)',
    'Tool X', 'model Y']."""
    out = [name]
    bare = " ".join(_PAREN_RE.sub(" ", name).split())
    out.append(bare)
    out += [" ".join(m.split()) for m in _PAREN_INNER_RE.findall(name)]
    seen, res = set(), []
    for v in out:
        k = _norm(v)
        if len(k) >= 3 and k not in seen:
            seen.add(k)
            res.append(v)
    return res


def _names_tool(text: str, tool: str) -> bool:
    """An author-side string and a disclosed tool name refer to the same
    thing: either contains the other as a whole-word run (after removing
    parentheticals from the tool name), case-insensitive. Both directions,
    so 'Tool X' as a member matches a disclosed 'Tool X (model Y)'."""
    if len(_norm(text)) < 3:
        return False
    return any(_mentions(text, v) or _mentions(v, text) for v in _tool_variants(tool))


@lru_cache(maxsize=None)
def _generic_patterns() -> tuple:
    """validators/ai_tool_name_patterns.yaml, compiled (data, not code)."""
    path = P.DATA_ROOT / "validators" / "ai_tool_name_patterns.yaml"
    if not path.is_file():
        return ()
    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    out = []
    for it in doc.get("patterns") or []:
        pat = it.get("pattern") if isinstance(it, dict) else None
        if isinstance(pat, str) and pat:
            out.append(re.compile(pat, re.IGNORECASE))
    return tuple(out)


def _generic_ai_name(full_name: str) -> bool:
    t = _norm(full_name)
    return bool(t) and any(p.search(t) for p in _generic_patterns())


# --------------------------------------------------------------------------
# sub-profile (spec/routes/sub_profile.schema.json shape; every value is a
# proposed_default, NEEDS_VERIFICATION)
# --------------------------------------------------------------------------

@lru_cache(maxsize=None)
def _sub_profile_file(dir_rel: str, sp_id: str) -> dict | None:
    if not dir_rel or not sp_id or ".." in sp_id or "/" in sp_id:
        return None
    path = P.DATA_ROOT / dir_rel / f"{sp_id}.yaml"
    if not path.is_file():
        return None
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    return doc if isinstance(doc, dict) else None


def sub_profile_ids(route) -> list[str]:
    d = route.sub_profile_dir
    if not d or not (P.DATA_ROOT / d).is_dir():
        return []
    return sorted(p.stem for p in (P.DATA_ROOT / d).glob("*.yaml"))


def sub_profile_view(route, sp_id: str | None) -> dict:
    """{id, found, abstract_langs, keyword_langs, kw_min, kw_max}. An
    unknown id reads as the GrantThai defaults with found False."""
    out = {"id": sp_id, "found": False, "abstract_langs": list(DEFAULT_LANGS),
           "keyword_langs": list(DEFAULT_LANGS), "kw_min": DEFAULT_KEYWORD_BAND[0],
           "kw_max": DEFAULT_KEYWORD_BAND[1]}
    doc = _sub_profile_file(route.sub_profile_dir or "", sp_id or "")
    if doc is None:
        return out
    out["found"] = True
    langs = doc.get("languages") if isinstance(doc.get("languages"), dict) else {}
    for key, slot in (("abstract", "abstract_langs"), ("keywords", "keyword_langs")):
        v = langs.get(key)
        if isinstance(v, list) and [x for x in v if x in ("th", "en")]:
            out[slot] = [x for x in v if x in ("th", "en")]
    for req in doc.get("requirements") or []:
        if not isinstance(req, dict) or isinstance(req.get("value"), bool) or not isinstance(req.get("value"), int):
            continue
        if req.get("item") == "keyword_count_min":
            out["kw_min"] = req["value"]
        if req.get("item") == "keyword_count_max":
            out["kw_max"] = req["value"]
    return out


# --------------------------------------------------------------------------
# venue items (only sourced ones are read)
# --------------------------------------------------------------------------

def _source_ids(c) -> set:
    return {s.get("source_id") for s in c.doc.get("sources") or [] if isinstance(s, dict)}


def _sourced_items(c) -> list[dict]:
    venue = c.value(VENUE)
    if not isinstance(venue, dict):
        return []
    known = _source_ids(c)
    return [it for it in venue.get("stated_requirements") or []
            if isinstance(it, dict) and str(it.get("source_ref") or "").strip() in known]


def _venue_int(items: list[dict], names: tuple) -> tuple[int, str] | None:
    for it in items:
        if it.get("item") in names:
            try:
                return int(str(it.get("value")).strip()), it["source_ref"]
            except ValueError:
                continue
    return None


# --------------------------------------------------------------------------

def _member_names(c) -> dict:
    """TM id -> the strings an author entry is compared on."""
    out = {}
    for m in c.items(TEAM):
        out[m.get("id")] = [str(m.get(k)) for k in ("full_name", "organization") if _filled(m.get(k))]
    return out


def _disclosed_tools(c) -> list[str]:
    auth = c.raw.get("authoring") if isinstance(c.raw.get("authoring"), dict) else {}
    decl = auth.get("ai_use_declaration") if isinstance(auth.get("ai_use_declaration"), dict) else {}
    names = [t.get("name") for t in decl.get("tools") or [] if isinstance(t, dict)]
    names += list(auth.get("tools_disclosed") or [])
    out = []
    for n in names:
        if isinstance(n, str) and n.strip() and n.strip() not in out:
            out.append(n.strip())
    return out


def check(c) -> None:
    from grantthai.validators import engine as E   # late: engine imports this module

    route = c.route
    sp = sub_profile_view(route, c.sub_profile)
    if c.sub_profile and not sp["found"]:
        known = ", ".join(sub_profile_ids(route)) or "none"
        c.findings.append(E.Finding(
            "SCHEMA", "BLOCK", f"sub-profile {c.sub_profile!r} is not a shipped sub-profile of route {route.id} "
                               f"(known: {known}).", [],
            f"Choose one of {known} (--sub-profile or routing.sub_profiles.{route.id}), or remove it."))
    sourced = _sourced_items(c)

    # ART001 abstract per language
    langs = list(sp["abstract_langs"])
    for it in sourced:
        if it.get("item") in VENUE_ITEM_ABSTRACT_LANGS:
            for tok in re.split(r"[\s,+/]+", str(it.get("value") or "").casefold()):
                if tok in ("th", "en") and tok not in langs:
                    langs.append(tok)
    for lang in ("th", "en"):
        if lang in langs and not _filled(c.value(ABSTRACT[lang])):
            c.add("ART001", f"{ABSTRACT[lang]} is empty, and sub-profile {sp['id'] or '(default)'} (GrantThai "
                  f"default, NEEDS_VERIFICATION) or a sourced venue item asks for an abstract in {lang}.",
                  [ABSTRACT[lang]],
                  f"Write the {lang} abstract from your own results (grantthai set {ABSTRACT[lang]} ...), or "
                  "choose the sub-profile that matches the venue's own author guidelines.")

    # ART002 keyword count
    lo, hi = sp["kw_min"], sp["kw_max"]
    basis = f"sub-profile {sp['id'] or '(default)'} band, proposed_default, NEEDS_VERIFICATION"
    vmin, vmax = _venue_int(sourced, VENUE_ITEM_KW_MIN), _venue_int(sourced, VENUE_ITEM_KW_MAX)
    if vmin or vmax:
        lo = vmin[0] if vmin else lo
        hi = vmax[0] if vmax else hi
        basis = "venue item(s) with source " + ", ".join(x[1] for x in (vmin, vmax) if x)
    for lang in sp["keyword_langs"]:
        v = c.value(KEYWORDS[lang])
        n = len([x for x in v if _filled(x)]) if isinstance(v, list) else (1 if _filled(v) else 0)
        if not (lo <= n <= hi):
            c.add("ART002", f"{KEYWORDS[lang]} has {n} keyword(s), outside {lo}-{hi} ({basis}).",
                  [KEYWORDS[lang]],
                  "Adjust the keywords to the venue's own current author guidelines; record the venue's number "
                  f"in {VENUE} stated_requirements (item keyword_count_min / keyword_count_max) with its source.")

    # ART003 body structure
    kind = c.value(KIND)
    if isinstance(kind, str) and _filled(kind):
        if kind == EMPIRICAL:
            empty = [f for f in IMRAD if not _filled(c.value(f))]
            if empty:
                c.add("ART003", f"Article kind is {EMPIRICAL}, but {', '.join(empty)} "
                      f"{'is' if len(empty) == 1 else 'are'} empty.", [KIND] + empty,
                      "Write each section yourself from the records listed under RENDER_FROM; GrantThai never "
                      "composes section text.")
        elif not [s for s in c.items(BODY_SECTIONS)]:
            c.add("ART003", f"Article kind is {kind}, and {BODY_SECTIONS} has no section.", [KIND, BODY_SECTIONS],
                  f"List the article's own sections in {BODY_SECTIONS} (heading and your text).")

    # ART004 references
    has_text = [f for f in SECTION_TEXT if _filled(c.value(f))]
    if any(_filled(s.get("text")) for s in c.items(BODY_SECTIONS)):
        has_text.append(BODY_SECTIONS)
    if has_text and not _filled(c.value(REFERENCES)):
        c.add("ART004", f"{', '.join(has_text)} has text but {REFERENCES} is empty; 78 of 100 funded final "
              "reports carry a reference list (corpus-100 pattern FWP-06; reports, not articles).",
              has_text + [REFERENCES],
              f"List the works the manuscript draws on in {REFERENCES}, or record why there are none. GrantThai "
              "never reformats citations.")

    # ART005 in-text AI-use statement
    if E.ai_use_recorded(c.raw, c.doc):
        st = c.value(AI_USE)
        st = st if isinstance(st, dict) else {}
        missing = [k for k in ("text", "placement") if not _filled(st.get(k))]
        if missing:
            c.add("ART005", f"AI use is recorded in the work object, but {AI_USE} has no "
                  f"{' and no '.join(missing)} (GenAI guideline 2569 p.11-12: say which tool, at which stage, "
                  "for what, and how it was checked, in the methods or the acknowledgements; p.27: the venue's "
                  "own GenAI rule comes first, NEEDS_VERIFICATION).", [AI_USE],
                  f"Write the statement yourself in {AI_USE}.text and choose placement methods or "
                  "acknowledgements. It complements authoring.ai_use_declaration (AI001).")

    # ART006 contributions
    authors = c.items(AUTHORS)
    contribs = c.items(CONTRIB)
    if len(authors) > 1 and not contribs:
        c.add("ART006", f"{len(authors)} authors are listed but {CONTRIB} is empty (CRediT role vocabulary, "
              "RELAYED, NEEDS_VERIFICATION).", [AUTHORS, CONTRIB],
              f"Record each author's roles in {CONTRIB}; whether the venue asks for a contribution statement is "
              "NEEDS_VERIFICATION.")
    elif contribs:
        with_role = {x.get("member_id") for x in contribs if x.get("roles")}
        for a in authors:
            if a.get("member_id") not in with_role:
                c.add("ART006", f"Author {a.get('id')} ({a.get('member_id')}) has no {CONTRIB} entry with a "
                      "role.", [AUTHORS, CONTRIB],
                      f"Add a {CONTRIB} entry with at least one role for {a.get('member_id')}.")

    # ART007 BLOCK: an AI tool is never an author. Matched against the
    # disclosed tools (both directions, parentheticals removed) and, whether
    # or not anything was disclosed, against the generic AI-tool name
    # patterns in validators/ai_tool_name_patterns.yaml (full_name only).
    tools = _disclosed_tools(c)
    names = _member_names(c)
    full = {m.get("id"): str(m.get("full_name")) for m in c.items(TEAM) if _filled(m.get("full_name"))}
    for fid, entries, extra in ((AUTHORS, authors, ("affiliation_as_typed",)), (CONTRIB, contribs, ())):
        for e in entries:
            texts = list(names.get(e.get("member_id"), [])) + [str(e.get(k)) for k in extra if _filled(e.get(k))]
            hit = next((t for t in tools for s in texts if _names_tool(s, t)), None)
            if hit:
                what = f"the disclosed AI tool {hit!r}"
            elif _generic_ai_name(full.get(e.get("member_id"), "")):
                what = (f"a member whose full_name reads as an AI tool ({e.get('member_id')}; generic pattern in "
                        "validators/ai_tool_name_patterns.yaml, whether or not the tool was disclosed)")
            else:
                continue
            c.add("ART007", f"{fid} entry {e.get('id')} names {what}. An AI tool is never an author or a "
                  "credited contributor (AGENTS.md non-negotiable 4; GenAI guideline 2569 p.5, p.23).", [fid],
                  f"Remove entry {e.get('id')} from {fid}. Disclose the tool's use in {AI_USE} and "
                  "authoring.ai_use_declaration instead. If the member is a person, correct the full_name.")

    # ART008 ethics statement
    human = c.value("COMP.STANDARD.HUMAN")
    signals = []
    if human is True or (isinstance(human, dict) and human.get("applicable") is True):
        signals.append("COMP.STANDARD.HUMAN")
    if any(isinstance(r, dict) and r.get("value") is not None
           for r in (c.doc.get("chain") or {}).get("EthicsRequirement") or []):
        signals.append("chain EthicsRequirement")
    if _filled(c.value("METHOD.PLAN.POPULATION")):
        signals.append("METHOD.PLAN.POPULATION")
    if signals and not _filled(c.value(ETHICS)):
        c.add("ART008", f"Human-participant signals ({', '.join(signals)}) are present but {ETHICS} is empty.",
              [ETHICS],
              f"Write the ethics statement in {ETHICS}: the committee and the approval identifier exactly as you "
              "have them. GrantThai never fills them in.")

    # ART009 / ART011 figures and tables
    for it in c.items(FIGURES):
        ai_ill = it.get("ai_generated_illustration") is True
        if ai_ill and it.get("data_bearing") is True:
            c.add("ART009", f"{FIGURES} item {it.get('id')} is data-bearing and marked as an AI-generated "
                  "illustration. An AI may not generate or alter research data, results or factual images "
                  "(GenAI guideline 2569 p.11, p.24-25).", [FIGURES],
                  f"Replace {it.get('id')} with a figure or table made from your own data, or, if it is only an "
                  "illustration, set data_bearing: false.")
        if ai_ill:
            cap = str(it.get("caption") or "")
            if not (_DISCLOSURE_RE.search(cap) or any(_mentions(cap, t) or _norm(t) in _norm(cap)
                                                       for t in tools)):
                c.add("ART011", f"{FIGURES} item {it.get('id')} is an AI-generated illustration and its caption "
                      "does not say so (GenAI guideline 2569 p.11, p.25).", [FIGURES],
                      f"Say in the caption of {it.get('id')} that it was made with an AI tool, and name the tool.")

    # ART010 venue facts need a source the researcher supplied
    venue = c.value(VENUE)
    if isinstance(venue, dict):
        known = _source_ids(c)
        reqs = [it for it in venue.get("stated_requirements") or [] if isinstance(it, dict)]
        for it in reqs:
            ref = str(it.get("source_ref") or "").strip()
            if not ref:
                c.add("ART010", f"{VENUE} stated requirement {it.get('item')!r} has no source_ref; it prints "
                      "NEEDS_VERIFICATION.", [VENUE],
                      "Add the venue's own current author guidelines to `sources` and point source_ref at it, or "
                      "remove the item.")
            elif ref not in known:
                c.add("ART010", f"{VENUE} stated requirement {it.get('item')!r} cites source {ref}, which is not "
                      "in `sources`; it prints NEEDS_VERIFICATION.", [VENUE],
                      f"Add {ref} to `sources` (citation, kind, contains_personal_data) or fix the id.")
        refs = [r for r in venue.get("source_refs") or [] if str(r).strip()]
        if _filled(venue.get("name_as_typed")) and not refs and not any(
                str(it.get("source_ref") or "").strip() for it in reqs):
            c.add("ART010", f"{VENUE}.name_as_typed is set with no source at all; any fact about the venue prints "
                  "NEEDS_VERIFICATION.", [VENUE],
                  "Add the venue's own document (for example its current author guidelines) to `sources` and "
                  "list it in source_refs.")
        for r in refs:
            if r not in known:
                c.add("ART010", f"{VENUE}.source_refs cites {r}, which is not in `sources`.", [VENUE],
                      f"Add {r} to `sources` or fix the id.")
