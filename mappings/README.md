# mappings/

- `nriis/section_to_tab.yaml` — the single versioned table from core/05
  sections to NRIIS tabs (schema `spec/mappings/section_to_tab.schema.json`).
  Filled in Phase 0 from the handoff package's compact field map (core/02
  §9). **Every entry is `NEEDS_VERIFICATION`:** tab names, tab order and
  section placement describe one observed form (ruling K14).
  `registry/nriis-fields.jsonl` is generated from it.
- `nriis/nrct-master-hss@<observed-date>.yaml` — the one dated form
  mapping; ships only once a public document fixes that form's tabs and
  labels.
- `modes/*_to_core.yaml` — questionnaire answer → field mappings (schema
  `spec/mappings/mode_mapping.schema.json`). Stubs; expert ships v0.1,
  citizen v0.2.

See the repository root README.md and GRANTTHAI_STANDALONE.md for the full
system description, and docs/design/PLAN.md for the design plan this
scaffold follows (where they differ, spec/ wins).
