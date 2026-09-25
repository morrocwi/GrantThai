# registry/

Field-ID registry.

- `fields.jsonl` — the core authoring fields, one JSON record per line,
  schema `spec/registry/field.schema.json`. **Derived** in Phase 0 from the
  handoff package core/05 (founder-owned, ruling K13), with lineage
  `derived_from: core/05@sha256:14e85efafc8633b7f50f792b0a3f71ed7abcd2f27fbea857c90064521004860e`
  on every record.
- `nriis-fields.jsonl` — render-only `NRIIS.<TAB>.<FIELD>` records,
  schema `spec/nriis/field.schema.json`. **Generated**, never hand-edited:
  `python tools/registry/build_nriis_fields.py` (a test fails when it is
  out of date).
- `aliases.yaml` — renamed field-ID history. IDs are never reused.

## What each registry field carries

| Key | Meaning |
|---|---|
| `field_id` | GrantThai id, `<NS>.<GROUP>[.<SUB>].<NAME>` |
| `source_field_id` | the id in core/05 it was re-keyed from |
| `section` | core/05 section; mapped to an NRIIS tab by `mappings/nriis/section_to_tab.yaml` |
| `chain_node` | the `spec/common/chain.yaml` node it belongs to, or null for project-level fields (a GrantThai DECISION) |
| `label_en` | core/05's descriptive English label — **not** an official NRIIS label (`label_en_basis: descriptive`) |
| `label_th` | `NEEDS_VERIFICATION` for every field (ruling K14: labels come later from public documents) |
| `type`, `cardinality`, `required`, `allowed_values`, `dependencies`, `validation_notes`, `source_status` | copied from core/05 (dependencies re-keyed) |
| `input_control` | derived from `type` by the table below |
| `observed_form` | `nrct-master-hss@NEEDS_VERIFICATION`: core/05 describes one observed form; its date is not recorded |
| `guidance.en` | core/05's field description (replaces core/05's `ai_prompt`, which is not carried over) |
| `guidance.th` | `NEEDS_INPUT` — to be written by a person in v0.1 |
| `authored_by` | `imported` |
| `markers` | `[NEEDS_VERIFICATION]` on every record |

One description was reworded during derivation: the team-members field
referred to an agency's verification status by name; it now says
"funder-system registration/verification status (NEEDS_VERIFICATION)".

## Re-key table (core/05 prefix → GrantThai prefix)

| core/05 | GrantThai | Example |
|---|---|---|
| `FUND.` | `FUND.CALL.` | `FUND.FISCAL_YEAR` → `FUND.CALL.FISCAL_YEAR` |
| `META.` | `DOC.META.` | `META.PROJECT_ID` → `DOC.META.PROJECT_ID` |
| `GEN.` | `CORE.GENERAL.` | `GEN.TITLE_TH` → `CORE.GENERAL.TITLE_TH` |
| `TEAM.` | `PROFILE.TEAM.` | `TEAM.MEMBERS` → `PROFILE.TEAM.MEMBERS` |
| `CORE.` | `CORE.RESEARCH.` | `CORE.RQ.PRIMARY` → `CORE.RESEARCH.RQ.PRIMARY` |
| `NARR.` | `CORE.NARRATIVE.` | `NARR.SUMMARY` → `CORE.NARRATIVE.SUMMARY` |
| `METHOD.` | `METHOD.PLAN.` | `METHOD.DESIGN` → `METHOD.PLAN.DESIGN` |
| `WORK.` | `WORK.PLAN.` | `WORK.ACTIVITIES` → `WORK.PLAN.ACTIVITIES` |
| `GEO.` | `GEO.AREA.` | `GEO.RESEARCH_SITES` → `GEO.AREA.RESEARCH_SITES` |
| `BUDGET.` | `BUDGET.PLAN.` | `BUDGET.ITEMS` → `BUDGET.PLAN.ITEMS` |
| `COMP.` | `COMP.STANDARD.` | `COMP.HUMAN` → `COMP.STANDARD.HUMAN` |
| `TRL.`, `SRL.` | `READY.TRL.`, `READY.SRL.` | `TRL.CURRENT` → `READY.TRL.CURRENT` |
| `PATH.` | `RESULTS.PATHWAY.` | `PATH.EXPERTS` → `RESULTS.PATHWAY.EXPERTS` |
| `RESULTS.` | `RESULTS.CHAIN.` | `RESULTS.OUTPUTS` → `RESULTS.CHAIN.OUTPUTS` |
| `AUDIT.` | `AUDIT.REVISION.` | `AUDIT.LOG` → `AUDIT.REVISION.LOG` |
| `PARTNERS` | `WORK.PARTNERS.ORGANIZATIONS` | — |
| `ATTACHMENTS` | `DOC.ATTACHMENTS.DOCUMENTS` | — |

## `type` → `input_control`

`string` text · `text`, `rich_text` textarea · `integer`, `money` number ·
`datetime` datetime · `boolean` checkbox · `enum`, `reference` select ·
`enum|string` select_or_text · `boolean|string` checkbox_or_text ·
`array<string>` repeating_text · `array<text>` repeating_textarea ·
`array<object>` repeating_group · `object` group · `rich_text|object`
textarea_or_group.
