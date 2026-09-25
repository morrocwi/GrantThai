# `build/NRIIS_SUBMISSION.md` — output contract

Draft, Phase 0 (contract only; renderer ships v0.1; v0.2 adds the
`form_profile` key, gate hold reasons, the form-profile subsection and the
completeness checklist, renderer `nriis_submission.md.j2@0.2.0`; the AI-use
ceiling adds the AI Use Declaration appendix, section 4.7, renderer
`nriis_submission.md.j2@0.3.0`). This is the **one
canonical output** of GrantThai's one-input, one-output pipeline — see
`spec/contracts/one-input-one-output.md`.

## Frontmatter fields

| Field | Type | Notes |
|---|---|---|
| `grantthai_version` | string | tool version that rendered this file |
| `schema_version` | string | `project.schema.json` version used |
| `renderer_version` | string | templates version |
| `project_id` | string | from `project.yaml` |
| `project_content_sha256` | string | `content_sha256` of `project.yaml` (`spec/common/object-hash.md`): authored content only, so it equals the hash current review records and the lock bind to |
| `project_state_sha256` | string | `state_sha256`: the whole file as rendered, statuses and reviews included |
| `project_locked` | boolean | `lock.locked` from `project.yaml`, true only while `lock.locked_content_sha256` equals `project_content_sha256` |
| `fund_profile` | string | `<agency>/<call-id>@<major.minor>` |
| `fund_profile_trust_level` | string | `FICTIONAL` < `COMMUNITY_EXTRACTED` < `HUMAN_VERIFIED` < `SECOND_CHECKED` (ordered). The rendered value is the **lowest** trust level among the profile itself and every rule the project used |
| `nriis_mapping` | string | `<form>@<observed-date>`; today `nrct-master-hss@NEEDS_VERIFICATION` |
| `form_profile` | string or null | v0.2: the form profile in force (`mappings/nriis/form_profiles/`), or `null` for the observed form. Every profile is `NEEDS_VERIFICATION` |
| `authoring` | object | `{mode: human|ai_assisted, tools_disclosed: [], self_declared: true, ai_use_declaration: none|unconfirmed|confirmed_by_researcher}` — default `human`. `ai_use_declaration` summarises `authoring.ai_use_declaration` in `project.yaml` (self-declared; `confirmed_by_researcher` only when the researcher set `declaration_confirmed_by_human: true`) |
| `submission_mode` | object | `{human_copy_paste: true, ai_assisted_fill: false, direct_submit: false}` — `ai_assisted_fill` becomes true only on explicit opt-in (never the package's original default of true) |
| `human_final_approval_required` | boolean | always `true` |
| `review` | object | `{RG0..RG4: {state, basis}}` |
| `submittable` | boolean | true/false, **against the bound fund profile only** |
| `real_world_verified` | boolean | false unless `fund_profile_trust_level` is at least `HUMAN_VERIFIED` and every rule used is current |
| `hold_reasons` | array | plain strings; since v0.2 also one line per review gate RG0–RG4 that is missing or stale (`spec/common/review_gates.yaml` missing-gate policy: never blocks `build`) |
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
   item, every `BLOCK` / `REVIEW` finding — each with a plain-language
   next step — and the count of open contradictions and conflicts
   (section 4.4). When a form profile is in force (v0.2), a subsection
   names it (`NEEDS_VERIFICATION`), lists its unmapped profile items
   (items the form asks for that have no single registry field) and its
   candidate budget rules, labelled "listed, not evaluated". A field the
   profile requires prints `REQUIRED: true (form profile <id>,
   NEEDS_VERIFICATION)`; the profile may also restrict which fields are
   placed on a tab (`render_only`, `hide`) but never renames a tab.
2. **Copy/paste fields by NRIIS tab.** Tabs and order come from
   `mappings/nriis/section_to_tab.yaml` (today: General, Project, Workplan,
   Utilization, Attachments). **These tab names, their order and the field
   order within each tab describe one observed form and are
   `NEEDS_VERIFICATION`** until confirmed from a public call or TOR
   document (founder ruling K14). The rendered section heading says so.
   **Only fields with registry `origin: NRIIS_NATIVE` are placed here**
   (core/02 rule R4: an authoring-core field is never presented as an
   NRIIS field). Each field block gives: label (EN, plus TH or
   `LABEL_TH: NEEDS_VERIFICATION`; where a public document edition gives
   one, the line adds a candidate Thai label tagged
   `(candidate, NEEDS_VERIFICATION: "<label>" (<SD-n> p<page>, item <n>))`
   from `mappings/nriis/labels@<edition>.yaml` — never declared official,
   never from the screenshot-derived readout, K14; the tab heading shows a
   candidate part label the same way), a fenced plain value, `FIELD_ID`,
   `ORIGIN` (the registry origin, core/02 §2), `PROVENANCE` (the record's
   provenance class, source type and evidence role), `RENDER_FROM` on a
   narrative field (the records the box is written from; GrantThai never
   composes the text), `STATUS` with its basis, `REQUIRED`,
   `INPUT_CONTROL`, `DEPENDENCIES`, `SOURCE_IDS`, `VALIDATION`,
   `AUTHORED_BY`, `CONFLICTS` when the registry lists an open
   contradiction for the field, and an arithmetic-check line where one
   applies (e.g. workplan-sums-to-100, budget line totals).
   - **Structured fields** (`array<object>`, `object`,
     `rich_text|object`; value contracts in
     `spec/registry/structured_fields.schema.json`) render as a table,
     one row per item in `id` order as written, one column per declared
     key in schema order; `*_ids` columns print the referenced ids
     comma-separated, and an unresolved id is printed with the marker
     `UNRESOLVED` (rule S006).
   - **Attachments tab.** NRIIS attachments are uploaded files, which a
     Markdown file cannot contain. This section lists each required or
     declared attachment (`DOC.ATTACHMENTS.DOCUMENTS`) with its status
     (`NEEDS_INPUT` when not yet supplied) and a plain-language note; the
     person uploads their own files. GrantThai never generates or uploads
     attachments.
3. **Machine field metadata.** A structured block (YAML) mirroring section
   2 for programmatic re-reading.
4. **Validation and provenance appendix**, in this order:
   1. gate records RG0–RG4, each marked `current` or `stale`
      (`spec/common/object-hash.md`);
   2. the source manifest, exactly as defined in
      `spec/common/links-and-sources.md` §3 ("Source manifest in the
      output"; entries with `contains_personal_data: true` print only
      `source_id`, `kind` and `[private]`);
   3. unresolved references: every `source_ids` entry (S008) and every
      link reference (S006) that did not resolve, with the field id or
      item id that holds it;
   4. **conflicts and open contradictions** — defined as:
      1. every entry of `registry/contradictions.yaml` (contradictions
         between the design sources; see `docs/contradictions.md`), each
         with its id, status, **every** reading with its source, the
         current GrantThai behaviour labelled as a working default, and the
         project records it touches;
      2. every entry of a field record's `conflicts` list in `project.yaml`
         (`spec/common/field_record.schema.json`), with the field id, its
         status, every reading with its `source_ids`, and the researcher's
         decision note if any.

      Conflicts are surfaced, never merged: no reading is dropped, and a
      `DECIDED_BY_RESEARCHER` conflict still prints every reading;
   5. project records not placed on any NRIIS tab: every record whose
      field is not `NRIIS_NATIVE` (or whose section is `not_on_tab`), with
      its `ORIGIN`, the reason it is not a box, the narrative boxes it
      feeds (`render_from`), and its value. These are never to be pasted as
      NRIIS boxes;
   6. **completeness checklist** (v0.2; `guidance/writing_intent.yaml`,
      `grantthai.guidance.writing.checklist`): one row per item WC01–WCnn,
      in id order: id, state (`PASS` | `OPEN` | `HUMAN_CHECK`), the field
      ids it covers, and the check text in English (Thai `NEEDS_INPUT`
      until sourced). Deterministic items are computed; `HUMAN_CHECK` items
      are for the researcher to confirm and are never marked PASS by the
      renderer. No timestamps. A line above the table states the file's
      status (`DRAFT`, `NEEDS_VERIFICATION`) and that it is guidance, not
      validation.

   7. **AI Use Declaration** (the AI-use ceiling, `docs/policy/ai-use-ceiling.md`).
      A GrantThai appendix, **not an NRIIS field**: its heading says so,
      and whether NRIIS or a call asks for such a declaration is
      `NEEDS_VERIFICATION`. It follows the order of the sample form in
      Appendix A (p.34) of the GenAI guideline 2569 (`docs/sources.md`):
      project title; responsible person (a pointer to the PI in
      `PROFILE.TEAM.MEMBERS`, never a second copy of personal data); a table
      of AI tools (name, developer, version, stages, purpose, used on);
      influence on decisions or conclusions; types of data given to the AI
      and how personal or confidential data was kept out; where the prompt
      and output log is kept; human verification; the count of AI-assisted
      values (section 1.5); the researcher's own risk self-assessment on the
      guideline's five example dimensions, with one **GrantThai convention
      level** (the highest score) labelled as GrantThai's convention, never
      the guideline's; and the declaration of responsibility, printed as
      confirmed only when `declaration_confirmed_by_human` is true, otherwise
      `NOT CONFIRMED (NEEDS_INPUT)`. Missing items are listed (rule AI001).
      Values print exactly as written; an empty value prints `NEEDS_INPUT`.
      When no AI use is recorded and no declaration exists, one line says
      so. Nothing in this section is ever placed on an NRIIS tab.

   (Version 0.1 of this contract listed an undefined "conflict log"; item 4
   is its defined replacement. See `docs/deviations.md`.)

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
