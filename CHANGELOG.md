# Changelog

All notable changes to GrantThai are documented in this file. Format loosely
follows [Keep a Changelog](https://keepachangelog.com/); versions follow
SemVer from v0.1 onward.

## [Unreleased] — Phase 0

### Added

- Repository tree skeleton (`spec/`, `docs/`, `src/grantthai/`, `funds/`,
  `tests/`, etc.).
- `.githooks/commit-msg` attribution guard, installed as commit #1.
- Governance and policy documents: `GOVERNANCE.md`, `NOTICE`, `PRIVACY.md`,
  `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `CITATION.cff`.
- Licensing: `LICENSE` (Apache-2.0), `LICENSES/` (Apache-2.0, CC BY 4.0
  texts), `REUSE.toml` (founder ruling K13).
- Data-contract drafts (structure only): `spec/common/*.yaml`,
  `spec/profile/`, `spec/project/`, `spec/fund/`, `spec/nriis/`,
  `spec/mcp/tools.schema.json` (contract only), `spec/output/`,
  `spec/contracts/one-input-one-output.md`.
- CI guards with seeded bad fixtures: no-AI-import, no-hardcoded-rules,
  leak/PII scan (maintainer-specific terms loaded from an untracked local
  file), attribution scan, gitleaks, REUSE lint, schema lint with instance
  validation, one-input-one-output, NOTICE constant. The leak/PII and
  gitleaks bad fixtures are generated at test run time.
- Field registry `registry/fields.jsonl` (100 fields derived from the
  handoff package core/05; every Thai label `NEEDS_VERIFICATION`), the
  generated `registry/nriis-fields.jsonl`, `mappings/nriis/section_to_tab.yaml`
  (`NEEDS_VERIFICATION`), and the rule catalog `validators/rules.yaml`
  (56 rules at first, 60 after the additions below), each with its schema.
- `docs/design/PLAN.md` (the founder's design plan, historical record) and
  the founder decisions log in `GOVERNANCE.md` (K1, K13, K14 ruled).
- `docs/sources.md`, `docs/deviations.md`, `docs/lineage.md`,
  `docs/ecosystem.md`, `docs/BUILD_GUIDE.md`.
- `AGENTS.md` (with `CLAUDE.md`/`GEMINI.md` pointers) as the binding entry
  point for any AI builder.
- `ai.json`, `llms.txt`, `llms-full.txt` discovery files (flags ADVISORY).
- `GRANTTHAI_STANDALONE.md` system/architecture guide.

### Added — cold-start contract fixes (round-2 independent review)

- `spec/registry/structured_fields.schema.json`: a machine value contract
  for every registry field of type `array<object>`, `object` or
  `rich_text|object` (46 fields), with key names derived from the handoff
  package core/02 (renames recorded per field and in `docs/deviations.md`),
  per-item ids (`x-grantthai-node`) and annotated references
  (`x-grantthai-ref`). `spec/registry/types.yaml` states the value
  semantics of every registry `type`; `field.schema.json` now enums `type`.
- `spec/common/links-and-sources.md`: the link model (nodes, reference
  resolution, how `project:chain_edges` is derived, causal vs feedback
  edges) and what a resolvable source reference is (offline only).
  `spec/common/source.schema.json` and a top-level `sources` list in
  `project.yaml`; `links` and a `source_ids` pattern on field records.
- Rules: S006 (unresolved reference), S007 (duplicate node id), S008
  (unresolvable source), T002 (exactly one PI); R001–R007, W001–W004,
  B001–B002, T001, CH001, ELIG001, S002 and S004 restated in terms of the
  new keys and `project:chain_edges` (60 rules).
- `spec/common/object-hash.md` v0.2: two hashes. `content_sha256` excludes
  statuses, review records, the lock and mapping acceptance, so a review
  record stays current when it takes effect; `state_sha256` covers the
  whole file. Review records carry `content_sha256`, the lock
  `locked_content_sha256`; output frontmatter and validation reports carry
  both hashes. Reference implementation `src/grantthai/core/object_hash.py`
  (checked against an independent RFC 8785 implementation), golden vectors
  in `tests/golden/object-hash/`.
- `spec/common/status.yaml`: precise `STRUCTURE_CHECKED` and `LOGIC_LINKED`
  criteria, including fields that no link rule reads.
- Output contract: structured fields render as tables; the appendix is
  gate records, source manifest and unresolved references (the undefined
  "conflict log" is removed); the output path is `<dir of project.yaml>/build/`.
- `examples/lecturer-no-ai/project.yaml`: a fully populated FICTIONAL
  worked example; `tests/test_example_project.py` recomputes the v0.1
  link, sum, budget, source and DAG rules on it from the contracts alone.
- `tools/ci/check_schema_lint.py` now enforces the structured-field
  contracts and checks project instances for placement, structured values,
  reference and source resolution, duplicate ids, causal cycles and stale
  review records, with a seeded bad fixture
  (`tests/fixtures/negative/schema_instance/examples/badlinks/`).
- Registry: the `CORE.RESEARCH.INNOVATION` descriptive label is now
  "Innovation / What Is New".

No CLI, renderer, or web-form logic ships in Phase 0. See `docs/deviations.md`
for departures from the original handoff package and `docs/design/PLAN.md`
§I for the full phased roadmap.
