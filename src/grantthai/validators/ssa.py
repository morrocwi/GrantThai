"""grantthai.validators.ssa — the SSA family (7SSA structure profiles).

Loaded by grantthai.validators.engine when the route in force includes the
SSA family (routes/academic-article/route.yaml `rules`). Exposes

    EVALUATED  frozenset of the rule ids this module evaluates
    check(ctx) adds findings through ctx.add (engine._Ctx)

Every rule fires only while a 7SSA structure profile is selected
(ctx.structure_profile: --structure-profile or routing.structure_profiles).
With none selected this module finds nothing, so the plain academic-article
output is unchanged. Every rule is a structural presence check on the
researcher's own records; none judges whether a gap is real, a contribution
new or an argument sound. Severities come from validators/rules.yaml
(REVIEW or INFO; the rule schema forbids BLOCK for a 7SSA-sourced rule).

Report-only: nothing here changes the work object.
"""
from __future__ import annotations

from grantthai.routes import structure as ST

EVALUATED = frozenset(f"7SSA-{n:02d}" for n in range(1, 11))

KIND = "ARTICLE.META.KIND"
TYPE = "ARTICLE.SSA.ARTICLE_TYPE"
GAP = "ARTICLE.SSA.GAP"
CONTRIB = "ARTICLE.SSA.CONTRIBUTION"
BEFORE_AFTER = "ARTICLE.SSA.BEFORE_AFTER"
BODY = "ARTICLE.BODY.SECTIONS"
ABSTRACT = ("ARTICLE.FRONT.ABSTRACT_TH", "ARTICLE.FRONT.ABSTRACT_EN")
REVIEW_TYPES = ("integrative_review", "cs_sok")


def _slot(state: dict, sid: str, name: str) -> bool:
    return any(s["filled"] for s in state["sectors"][sid]["slots"] if s["slot"] == name)


def check(c) -> None:
    from grantthai.validators import engine as E   # late: engine imports this module

    pid = getattr(c, "structure_profile", None)
    route = c.route
    if not pid or not ST.has_profiles(route):
        return
    try:
        prof = ST.load_profile(route, pid)
    except ST.StructureProfileNotFound:
        known = ", ".join(ST.profile_ids(route)) or "none"
        c.findings.append(E.Finding(
            "SCHEMA", "BLOCK", f"structure profile {pid!r} is not a shipped structure profile of route {route.id} "
                               f"(known: {known}).", [],
            f"Choose one of {known} (--structure-profile or routing.structure_profiles.{route.id}), or remove it."))
        return

    items = c.items(BODY)
    atype = c.value(TYPE)
    state = ST.sector_state(c.value, items, route, atype)
    secs = state["sectors"]

    # 7SSA-01 a sector with no tagged item and no required slot filled
    for sid in ST.SECTORS:
        s = secs[sid]
        if not s["items"] and not s["any_required_filled"]:
            c.add("7SSA-01", f"Sector {sid} ({s['name_en']}) has no {BODY} item tagged ssa_sector {sid} and none of "
                  f"its required slots is filled. It prints NEEDS_INPUT under its [{sid}] marker in profile {pid}.",
                  [BODY], f"Write the {sid} content yourself as a {BODY} item with ssa_sector {sid} (7SSA audit "
                  f"question: {s['audit_question_en']}).")

    # 7SSA-02 problem before contribution
    order = [it.get("ssa_sector") for it in items]
    first4 = order.index("S4") if "S4" in order else None
    first5 = order.index("S5") if "S5" in order else None
    if first5 is not None and (first4 is None or first5 < first4):
        c.add("7SSA-02", f"The first {BODY} item tagged S5 (contribution) comes before any item tagged S4 "
              "(problem): the problem is not stated before the contribution.", [BODY],
              "Order the body items so the problem (S4) is written before the contribution (S5).")
    elif ST.filled(c.value(CONTRIB)) and not ST.filled(c.value(GAP)):
        c.add("7SSA-02", f"{CONTRIB} is filled but {GAP} is empty: the contribution answers no stated problem.",
              [GAP, CONTRIB], f"Record the problem in {GAP} (gap_type, unresolved_problem, consequence_if_unresolved).")

    # 7SSA-03 Sector 6 objection / boundary / limitations
    missing = [n for n in ("strongest_objection", "boundary_conditions", "limitations") if not _slot(state, "S6", n)]
    if missing:
        c.add("7SSA-03", f"Sector 6 has no filled {', '.join(missing)} slot.", [BODY],
              f"Add {BODY} items with ssa_sector S6 and ssa_slot {', '.join(missing)}, written by you.")

    # 7SSA-04 Thai layout carries both abstracts
    if prof.get("heading_lang") == "th":
        empty = [f for f in ABSTRACT if not ST.filled(c.value(f))]
        if empty:
            c.add("7SSA-04", f"Structure profile {pid} (Thai headings) is selected and {', '.join(empty)} "
                  f"{'is' if len(empty) == 1 else 'are'} empty.", empty,
                  "Write the missing abstract yourself; the source's Thai layout carries a Thai and an English abstract.")

    # 7SSA-05 contribution one sentence / difference from prior
    cv = c.value(CONTRIB) if isinstance(c.value(CONTRIB), dict) else {}
    missing = [k for k in ("one_sentence", "difference_from_prior") if not ST.filled(cv.get(k))]
    if missing:
        c.add("7SSA-05", f"{CONTRIB} has no {' and no '.join(missing)}.", [CONTRIB],
              f"State the contribution in one sentence and how it differs from the nearest prior object, in {CONTRIB}.")

    # 7SSA-06 gap consequence
    gv = c.value(GAP) if isinstance(c.value(GAP), dict) else {}
    if not ST.filled(gv.get("consequence_if_unresolved")):
        c.add("7SSA-06", f"{GAP} has no consequence_if_unresolved.", [GAP],
              f"Say in {GAP}.consequence_if_unresolved what the field cannot explain or decide while the problem "
              "stays open.")

    # 7SSA-07 before / after
    if not (_slot(state, "S7", "before_state") or _slot(state, "S7", "after_state")):
        c.add("7SSA-07", f"Sector 7 has no before/after statement ({BEFORE_AFTER} before_state/after_state, or an "
              "S7 body item with those slots).", [BEFORE_AFTER],
              f"Write what the field understood before the article and what it can do after it, in {BEFORE_AFTER}.")

    # 7SSA-08 empirical kind outside 7SSA
    kind = c.value(KIND)
    if isinstance(kind, str) and kind in (prof.get("excludes_article_kind") or []):
        c.add("7SSA-08", f"{KIND} is {kind}, which the 7SSA source places outside its scope; structure profile {pid} "
              "still renders.", [KIND],
              "Keep the profile if it is what you want, or remove routing.structure_profiles for this route.")

    # 7SSA-09 profile language vs sub-profile
    pair = prof.get("pairs_with_sub_profile")
    if pair and c.sub_profile and pair != c.sub_profile:
        c.add("7SSA-09", f"Structure profile {pid} pairs with sub-profile {pair}, but sub-profile {c.sub_profile} is "
              "in force; the build still renders.", [],
              f"Choose the profile that matches the sub-profile, or set routing.sub_profiles.{route.id} to {pair}.")

    # 7SSA-10 review / SoK corpus
    if atype in REVIEW_TYPES:
        missing = [n for n in ("corpus_method", "inclusion_logic") if not _slot(state, "S2", n)]
        if missing:
            c.add("7SSA-10", f"{TYPE} is {atype} and Sector 2 has no filled {', '.join(missing)} slot.", [TYPE, BODY],
                  f"Describe the corpus and how works were included, as {BODY} items with ssa_sector S2 and ssa_slot "
                  f"{', '.join(missing)}.")
