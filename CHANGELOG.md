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
  (56 rules), each with its schema.
- `docs/design/PLAN.md` (the founder's design plan, historical record) and
  the founder decisions log in `GOVERNANCE.md` (K1, K13, K14 ruled).
- `docs/sources.md`, `docs/deviations.md`, `docs/lineage.md`,
  `docs/ecosystem.md`, `docs/BUILD_GUIDE.md`.
- `AGENTS.md` (with `CLAUDE.md`/`GEMINI.md` pointers) as the binding entry
  point for any AI builder.
- `ai.json`, `llms.txt`, `llms-full.txt` discovery files (flags ADVISORY).
- `GRANTTHAI_STANDALONE.md` system/architecture guide.

No CLI, renderer, or web-form logic ships in Phase 0. See `docs/deviations.md`
for departures from the original handoff package and `docs/design/PLAN.md`
§I for the full phased roadmap.
