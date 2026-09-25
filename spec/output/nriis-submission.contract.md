# `build/NRIIS_SUBMISSION.md` — output contract

Draft, Phase 0 (contract only; renderer ships v0.1). This is the **one
canonical output** of GrantThai's one-input, one-output pipeline — see
`spec/contracts/one-input-one-output.md`.

## Frontmatter fields

| Field | Type | Notes |
|---|---|---|
| `grantthai_version` | string | tool version that rendered this file |
| `schema_version` | string | `project.schema.json` version used |
| `renderer_version` | string | templates version |
| `project_id` | string | from `project.yaml` |
| `project_object_sha256` | string | computed as defined in `spec/common/object-hash.md` |
| `project_locked` | boolean | `lock.locked` from `project.yaml`; when false, the hash is of the current, unlocked object |
| `fund_profile` | string | `<agency>/<call-id>@<major.minor>` |
| `fund_profile_trust_level` | string | `FICTIONAL` < `COMMUNITY_EXTRACTED` < `HUMAN_VERIFIED` < `SECOND_CHECKED` (ordered). The rendered value is the **lowest** trust level among the profile itself and every rule the project used |
| `nriis_mapping` | string | `<form>@<observed-date>`; today `nrct-master-hss@NEEDS_VERIFICATION` |
| `authoring` | object | `{mode: human|ai_assisted, tools_disclosed: [], self_declared: true}` — default `human` |
| `submission_mode` | object | `{human_copy_paste: true, ai_assisted_fill: false, direct_submit: false}` — `ai_assisted_fill` becomes true only on explicit opt-in (never the package's original default of true) |
| `human_final_approval_required` | boolean | always `true` |
| `review` | object | `{RG0..RG4: {state, basis}}` |
| `submittable` | boolean | true/false, **against the bound fund profile only** |
| `real_world_verified` | boolean | false unless `fund_profile_trust_level` is at least `HUMAN_VERIFIED` and every rule used is current |
| `hold_reasons` | array | plain strings |
| `stale_rules` | array | rule ids |
| `accepted_by_requester_mappings` | array | mapping ids capped at CONTRIBUTORY |
| `validation_summary` | object | `{block: N, review: N, info: N}` — counts of `BLOCK` / `REVIEW` / `INFO` findings (the one severity vocabulary, defined in `validators/rules.yaml`) |
| `disclaimer` | string | the NOTICE constant, byte for byte from `spec/output/notice_constant.txt` |

## Body — required section order

Body **line 1** is the NOTICE constant (`spec/output/notice_constant.txt`,
one line, English and Thai), repeated in plain text because frontmatter is
usually dropped on copy/paste. `tools/ci/check_notice.py` checks that the
template puts it there.

1. **Readiness summary.** Every field with status `NEEDS_INPUT`, every
   marker (`NEEDS_VERIFICATION`, `HOLD_FOR_VERIFICATION`, `UI_DRIFT`),
   every `PROPOSED`/`ACCEPTED_BY_REQUESTER` mapping, every `AUTHOR_CHECKED`
   item, and every `BLOCK` / `REVIEW` finding — each with a plain-language
   next step.
2. **Copy/paste fields by NRIIS tab.** Tabs and order come from
   `mappings/nriis/section_to_tab.yaml` (today: General, Project, Workplan,
   Utilization, Attachments). **These tab names, their order and the field
   order within each tab describe one observed form and are
   `NEEDS_VERIFICATION`** until confirmed from a public call or TOR
   document (founder ruling K14). The rendered section heading says so.
   Each field block gives: label (EN, plus TH or
   `LABEL_TH: NEEDS_VERIFICATION`), a fenced plain value, `FIELD_ID`,
   `ORIGIN`, `STATUS` with its basis, `REQUIRED`, `INPUT_CONTROL`,
   `DEPENDENCIES`, `SOURCE_IDS`, `VALIDATION`, `AUTHORED_BY`, and an
   arithmetic-check line where one applies (e.g. workplan-sums-to-100,
   budget line totals).
   - **Attachments tab.** NRIIS attachments are uploaded files, which a
     Markdown file cannot contain. This section lists each required or
     declared attachment (`DOC.ATTACHMENTS.DOCUMENTS`) with its status
     (`NEEDS_INPUT` when not yet supplied) and a plain-language note; the
     person uploads their own files. GrantThai never generates or uploads
     attachments.
3. **Machine field metadata.** A structured block (YAML) mirroring section
   2 for programmatic re-reading.
4. **Validation and provenance appendix.** Gate records (RG0–RG4), the
   source manifest (no personal data), and the conflict log.

## Invariants

- Markers (`NEEDS_INPUT`, `NEEDS_VERIFICATION`, `HOLD_*`, etc.) are never
  silently dropped.
- The same project object rendered with the same renderer version gives a
  byte-identical file (determinism; see `tests/test_determinism.py`, v0.1).
- The body contains **no timestamps** (that would break determinism).
- Personal data in `PROFILE.*` fields renders only into the private
  `build/` directory, never into anything committed or shared by default
  (`grantthai export` removes it unless `--include-private` is passed).

## Release QA (developer-side, not a user requirement)

These are checks the GrantThai maintainers run on example projects before a
release (acceptance test AT-5). They are **not** conditions for a user to
trust or use their own file, and a user never needs any of them.

- **Required:** a cold read by a human who did not write the example
  project, against a named checklist (`docs/en/quality-gates.md`, written
  in v0.1).
- **Optional, additional:** a cold read by an AI reader. It can add
  signal; it is never required, and its absence never blocks a release
  (founder ruling 2026-09-25: AI stays optional).

## Optional secondary artifact (Citizen Mode only)

`grantthai build --concept-note` renders `build/RESEARCH_CONCEPT_NOTE.md`
from the *same* project object, for a citizen with no eligible PI partner
yet. This is a clearly separate, optional artifact — **it is never required
to enter NRIIS**, and it does not change the one-output contract for the
NRIIS entry path itself. See `spec/contracts/one-input-one-output.md`.
