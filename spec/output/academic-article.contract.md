# `build/ACADEMIC_ARTICLE.md` — output contract

Draft, v0.3 router (contract and template ship in wave 1; the renderer
`src/grantthai/render/article.py` ships in wave 2; renderer version
`academic_article.md.j2@0.1.0`). This is the **one output of the
`academic-article` route** (`routes/academic-article/route.yaml`) under the
one-input, one-output contract restated per route — see
`spec/contracts/one-input-one-output.md`. The NRIIS route's contract is
`spec/output/nriis-submission.contract.md`; the two are siblings, and
building one route never touches the other route's file.

Founder reframe (2026-09-25): entering NRIIS is no longer the core; it is
one route of a router, because GrantThai opens to academic articles as
well. A route is a deterministic output route chosen by a person, never by
an AI.

## What this file is, and is not

- It is the researcher's own records, arranged as a **manuscript overview**
  the researcher writes the article from. Every section value is exactly
  what the work object says.
- It is **not** a manuscript. GrantThai composes no section text, reformats
  no citation, names no journal, and never says that a manuscript is
  sound, novel, publishable or accepted. The ready flag is
  `manuscript_ready` (no open `BLOCK` finding), never "accepted" or
  "publishable".
- Every venue fact is `NEEDS_VERIFICATION` unless the researcher supplied
  the venue's own document as a source (`ARTICLE.VENUE.TARGET`, rule
  ART010). GrantThai ships no venue registry.
- Both shipped sub-profiles (`thai-journal`, `international-journal`) are
  GrantThai defaults, `NEEDS_VERIFICATION`, not venue profiles.

## Frontmatter fields

| Field | Type | Notes |
|---|---|---|
| `grantthai_version` | string | tool version that rendered this file |
| `schema_version` | string | `work.schema.json` (0.3) or, for a legacy file, `project.schema.json` (0.2) version used |
| `renderer_version` | string | `academic_article.md.j2@0.1.0` |
| `route` | string | `academic-article` |
| `sub_profile` | string | the sub-profile in force (`routes/academic-article/sub_profiles/`); `NEEDS_VERIFICATION` always |
| `work_id` | string | from the work object (`work_id`, or `project_id` of a legacy file) |
| `work_type` | string | from the work object (`research_proposal` for a legacy file) |
| `article_kind` | string | `ARTICLE.META.KIND` value or `NEEDS_INPUT` |
| `article_language` | string | `ARTICLE.META.LANGUAGE` value or `NEEDS_INPUT` |
| `work_content_sha256` | string | `content_sha256` of the work object (`spec/common/object-hash.md`): authored content only; `routing` is excluded, so choosing a route never makes review records stale |
| `work_state_sha256` | string | `state_sha256`: the whole file as rendered |
| `work_locked` | boolean | `lock.locked`, true only while `lock.locked_content_sha256` equals `work_content_sha256` |
| `authoring` | object | as in the NRIIS contract: `{mode, tools_disclosed, self_declared, ai_use_declaration}` |
| `submission_mode` | object | `{human_copy_paste: true, ai_assisted_fill: false, direct_submit: false}` — GrantThai submits to no venue |
| `human_final_approval_required` | boolean | always `true` |
| `review` | object | `{RG0..RG4: {state, basis}}` |
| `manuscript_ready` | boolean | `validation_summary.block == 0`; **never** a statement about acceptance or publishability |
| `hold_reasons` | array | plain strings; one line per missing or stale review gate |
| `validation_summary` | object | `{block: N, review: N, info: N}` — the one severity vocabulary (`validators/rules.yaml`) |
| `disclaimer` | string | the NOTICE constant, byte for byte from `spec/output/notice_constant.txt` |
| `route_notice` | string | `route_notice_en` from `routes/academic-article/route.yaml` |

No `fund_profile`, `submittable` or `real_world_verified` key: the route
has `needs_fund_binding: false`, and the F family is out of scope.

## Body — required order

Body **line 1** is the NOTICE constant (unchanged; `tools/ci/check_notice.py`
checks every route template). Body **line 2** is the route notice: "GrantThai
is not affiliated with any journal or publisher. Venue requirements are
yours to confirm from the venue's own current author guidelines." A
fictional work object prints a FICTIONAL banner after them.

1. **Readiness summary**, in the order `routes/academic-article/route.yaml`
   `readiness.sections` gives: BLOCK findings, REVIEW findings,
   NEEDS_INPUT (route fields with no value, and other records still
   NEEDS_INPUT), NEEDS_VERIFICATION (venue facts and Thai labels, plus every
   marked record), AI-drafted values, and INFO lines for rules not
   evaluated by this version or not in scope for this route (RT002).
   Each finding carries a plain-language next step. The summary states
   `manuscript_ready` and that human final approval is always required.
2. **Manuscript overview by section**, in the order of
   `routes/academic-article/placement.yaml` (`front_matter`, `abstract`,
   `body`, `statements`, `figures_tables`, `references`, `venue`; file
   order, schema `spec/routes/placement.schema.json`). Section
   names are GrantThai's own descriptive headings, never a venue's; their
   Thai titles are `NEEDS_INPUT`. Each field block gives: label (EN, plus
   `LABEL_TH: NEEDS_VERIFICATION`), a fenced plain value, `FIELD_ID`
   (marked shared core when the field's registry scope is `shared`),
   `ORIGIN` (`VENUE_NATIVE` for route fields), `PROVENANCE`, `RENDER_FROM`
   on a section field (the records the researcher writes it from;
   GrantThai never composes it), `COPIED_FROM` when an empty route title
   was filled by copying the shared `CORE.GENERAL.TITLE_*` value (copy,
   never composition), `STATUS` with basis and markers, `REQUIRED`,
   `SOURCE_IDS`, `VALIDATION`, `AUTHORED_BY`.
   - **Structured fields** (`ARTICLE.FRONT.AUTHORS`, `ARTICLE.FRONT.CONTRIBUTIONS`,
     `ARTICLE.BODY.SECTIONS`, `ARTICLE.BODY.FIGURES_TABLES`,
     `ARTICLE.VENUE.TARGET`, `ARTICLE.STATEMENT.AI_USE`, structured
     abstracts; contracts in `spec/registry/structured_fields.schema.json`)
     render as a table, one row per item in `id` order as written, one
     column per declared key in schema order; `member_id` prints the
     referenced team member's id, and an unresolved id prints `UNRESOLVED`
     (rule S006).
   - **Authors.** Personal data (`full_name`, affiliation) renders only
     into the private `build/` directory (`PRIVACY.md`). An author entry
     whose name matches a disclosed AI tool (either name inside the
     other), or whose member full_name matches a generic AI-tool name
     pattern (`validators/ai_tool_name_patterns.yaml`) even when nothing
     is disclosed, is a BLOCK finding (ART007) and still prints, marked,
     so the researcher sees it.
   - **Venue.** Each `stated_requirements` item prints with its
     `source_ref`; an item without one prints `NEEDS_VERIFICATION` (ART010).
3. **Machine field metadata.** A YAML block mirroring section 2.
4. **Validation and provenance appendix**, in this order: review gates
   RG0–RG4 (`current` / `stale`); the source manifest
   (`spec/common/links-and-sources.md` §3; private sources print only
   `source_id`, `kind`, `[private]`); unresolved references (S006, S008);
   conflicts recorded in the work object (every reading printed, none
   merged); records not placed in the manuscript overview (route-specific
   fields of another route, never dropped); shared records read by this
   route; the **AI Use Declaration** appendix (same shape as the NRIIS
   contract section 4.7, with the responsible person pointing at the
   corresponding author, and a pointer to the in-text
   `ARTICLE.STATEMENT.AI_USE`, rule ART005); and the **Core Epistemic
   Structure** role-disclosure block (experience-based expert; interactional
   expert or None; each AI model used, with its role — the only place an AI
   model is named, and never as an author).
5. **Advisories (not decisions)** — printed only when a route-adjacent
   advisory's own fields are filled (spec §2.4); with those fields empty the
   section is absent and the file is byte-identical to a build without
   advisories.

## Invariants

- Markers (`NEEDS_INPUT`, `NEEDS_VERIFICATION`, `HOLD_*`) are never silently
  dropped.
- The same work object rendered with the same renderer version and the
  same route and sub-profile gives a byte-identical file (determinism;
  acceptance test AT-R2).
- Building this route into a directory that already holds another route's
  output leaves that file byte-identical (AT-R3); each invocation writes
  exactly one file.
- Shared-core values print identically in every route built from the same
  object (AT-R3).
- The body contains **no timestamps**.
- No venue is named by GrantThai; no citation is reformatted; no section
  text is composed.
- Personal data in `PROFILE.*` and `ARTICLE.FRONT.AUTHORS` renders only into the
  private `build/` directory.

## Release QA (developer-side, not a user requirement)

As for the NRIIS contract: a cold read by a human who did not write the
example work object, against `docs/en/quality-gates.md`; an AI cold read is
optional and never required. The shipped example for this route is
fictional and names no real journal (`examples/article-fictional/`).
