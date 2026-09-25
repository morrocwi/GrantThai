# `build/RESEARCH_CONCEPT_NOTE.md` — output contract

Draft, v0.3 router (renderer `src/grantthai/render/concept_note.py`,
renderer version `research_concept_note.md.j2@0.1.0`). This is the **one
output of the `concept-note` route** (`routes/concept-note/route.yaml`)
under the one-input, one-output contract restated per route — see
`spec/contracts/one-input-one-output.md`. Its siblings are
`spec/output/nriis-submission.contract.md` and
`spec/output/academic-article.contract.md`; building one route never
touches another route's file.

Before v0.3 the concept note was the "one exception" of the one-input,
one-output contract (an optional secondary artifact for Citizen Mode with no
eligible PI partner). In v0.3 it is an ordinary route, chosen by a person
(`--route concept-note` or `routing.default_route`), never by an AI.

## What this file is, and is not

- It is the researcher's own records arranged as a short **pre-proposal
  working document**, for talking an idea through with a partner, a
  supervisor or a prospective PI.
- It is **never submittable** to any funder system: the route sets
  `readiness.always_hold`, so the ready flag `submittable` is always
  `false` and a hold reason says why. It never replaces the NRIIS route.
- GrantThai composes no text in it. Every value is exactly what the work
  object says; a missing value prints `NEEDS_INPUT`.
- No budget, fund, workplan, team-arithmetic or eligibility rule runs on
  this route (`rules.include_families`: SCHEMA, R, CH, X, AI, FW).

## Frontmatter fields

| Field | Type | Notes |
|---|---|---|
| `grantthai_version` | string | tool version that rendered this file |
| `schema_version` | string | the work object's schema version (0.3, or 0.2 for a legacy file) |
| `renderer_version` | string | `research_concept_note.md.j2@0.1.0` |
| `route` | string | `concept-note` |
| `work_id` | string | from the work object (`work_id`, or `project_id` of a legacy file) |
| `work_type` | string | from the work object (`research_proposal` for a legacy file) |
| `work_content_sha256` | string | `content_sha256` (`spec/common/object-hash.md`); `routing` is excluded |
| `work_state_sha256` | string | `state_sha256`: the whole file as rendered |
| `work_locked` | boolean | true only while `lock.locked_content_sha256` equals `work_content_sha256` |
| `authoring` | object | as in the NRIIS contract |
| `submission_mode` | object | `{human_copy_paste: true, ai_assisted_fill: false, direct_submit: false}` |
| `human_final_approval_required` | boolean | always `true` |
| `review` | object | `{RG0..RG4: {state, basis}}` |
| `submittable` | boolean | always `false` (the route always holds) |
| `hold_reasons` | array | the always-hold line first, then one line per missing or stale review gate |
| `validation_summary` | object | `{block: N, review: N, info: N}` |
| `disclaimer` | string | the NOTICE constant, byte for byte from `spec/output/notice_constant.txt` |
| `route_notice` | string | `route_notice_en` from `routes/concept-note/route.yaml` |

## Body — required order

Body **line 1** is the NOTICE constant (unchanged). Body **line 2** is the
route notice. A fictional work object prints a FICTIONAL banner after them.

1. **Readiness summary**: BLOCK findings, REVIEW findings, NEEDS_INPUT,
   NEEDS_VERIFICATION, AI-drafted values, and INFO lines (rules not
   evaluated, RT001, RT002), each finding with a plain-language next step.
2. **Concept note by section**, in the order of
   `routes/concept-note/placement.yaml`. Section names are GrantThai's own
   headings; their Thai titles are `NEEDS_INPUT`. Every placed field is a
   shared-core field and prints exactly as it prints in every other route
   built from the same object.
3. **Machine field metadata** (YAML).
4. **Validation and provenance appendix**: review gates, source manifest
   (private sources print only `source_id`, `kind`, `[private]`),
   unresolved references, records not placed in this note (never dropped),
   and the AI Use Declaration appendix.

## Invariants

- Markers are never silently dropped; the body contains no timestamps.
- The same object, renderer version and route give a byte-identical file.
- Each invocation writes exactly one file and leaves any other route's file
  byte-identical.
