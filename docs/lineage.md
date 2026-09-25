# Lineage

## Core Epistemic Structure (role disclosure)

This block and the README footer are the two sanctioned places where an AI
model is named as having been used in producing this repository. Other
mentions of vendor or model names in the repository are guard patterns,
SDK package names in import-ban lists, tooling file names (such as the `CLAUDE.md`/`GEMINI.md` pointer files) or
guard-test fixtures, not usage statements. This is a role disclosure, not
an authorship, co-author, or credit line — see `NOTICE`, `CITATION.cff`,
and `GOVERNANCE.md`.

- **Core respondent / experience-based expert:** Yaoharee Lahtee.
- **Interactional expert:** None.
- **AI model(s) used (role only):**
  - GPT-5.6-sol (OpenAI, via Codex) — co-drafting of the handoff package
    and overall picture with the author.
  - Claude Opus 5.5 — planning meeting chair/seats, adversarial gate
    review, drafting fixes.
  - Claude Sonnet 5 — scaffolding and verification.

  None of the above is an author, co-author, or credited contributor of
  GrantThai.

## Handoff-package lineage

Every file in this repository derived from the original AI build-handoff
package's core files 01–06 carries a `derived_from: core/0N@sha256:<hash>`
tag in its own header or metadata. The package itself is never committed —
see `docs/sources.md` for the full hash table and exclusion list.

Rights status for core 01–06: **resolved** by founder ruling K13
(2026-09-25). The founder owns core 01–06; derived files are licensed
Apache-2.0 (code) and CC BY 4.0 (documentation, specifications and data).
See `GOVERNANCE.md`, "Founder decisions log". The lineage tags stay, so
that every derived artifact remains traceable to its source.

## The founder's own term

The founder's own term for a fully checked project object is "verified
project object". This repository deliberately does **not** use that phrase
in rendered output or public prose — see `spec/common/status.yaml`
("restricted_term") — because it risks being read as third-party
verification or endorsement. It is preserved here, once, as the founder's
own language, distinct from GrantThai's actual, more modest claim:
"checked against GrantThai rules" (a statement about internal consistency
with this project's own schema and rule set, not an external guarantee of
scientific merit or funding success).

## Toledo (conceptual framework only — no equations copied)

GrantThai's "Toledo" reference is conceptual only: the idea that lived
experience and academic knowledge are connected through a human-gated
translation step, with evidence, methodology, and human expertise as the
gates to verifiable knowledge (see the README philosophy sentences).

**GrantThai contains no Toledo-registered equations and no proofs.** No
Toledo content is copied into this repository. These are pointers only,
routed through `main.hub`, per the founder's Human-AI Readout Programme
conventions:

- Toledo equation registry and proof framework (a separate repository;
  related to, but not the same thing as, the conceptual "Toledo" framework
  named in the philosophy sentences):
  <https://github.com/morrocwi/toledo> — DOI
  [10.5281/zenodo.22537318](https://doi.org/10.5281/zenodo.22537318)
- glosa (human-AI knowledge co-production methodology):
  <https://github.com/morrocwi/glosa>
- main.hub (routing layer across the founder's public repos):
  <https://github.com/morrocwi/main.hub>

## Banned wording (public prose)

The following phrases must never appear in rendered output or public
prose (`docs/design/PLAN.md` §H):

- "validated by Toledo"
- "Coq-verified"
- "NRIIS-compliant"
- "officially compatible"
- "verified project object" (outside this file and the historical plan record `docs/design/PLAN.md`)

Any future single numeric quality score is rejected outright; any future
score of any kind goes through the Toledo reuse pipeline first (see the
founder's own workspace rules on equation discipline — out of scope for
this repository, referenced here only as a boundary condition).
