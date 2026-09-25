# GrantThai — standalone system guide

*(Replaces the working name `OPEN_THAI_RESEARCH_STANDALONE.md` used during
planning — see decision K3. This is the system/architecture description
for any reader: contributor, reviewer, or another AI builder.)*

> GrantThai is an independent, unofficial project. It is NOT affiliated with, endorsed by, sponsored by, or officially connected to NRCT, TSRI, any PMU, or NRIIS. / GrantThai เป็นโครงการอิสระ ไม่เป็นทางการ และไม่ผูกพันกับ วช. สกสว. หน่วยบริหารจัดการทุน (PMU) ใด ๆ หรือระบบ NRIIS
>
> See `NOTICE`.

## 1. Purpose

GrantThai is open research infrastructure that helps any person turn a
real problem into one research project object, checks it against
GrantThai's own rules (`validators/rules.yaml`), then renders that object
to one file: `build/NRIIS_SUBMISSION.md`. It is unofficial. It has
no affiliation with NRCT, TSRI, any PMU, or NRIIS. See the README
philosophy sentences and `spec/contracts/one-input-one-output.md` for the
headline contract this entire system exists to serve.

## 2. Principles

- **P1 One object.** One project gives one project object (checked
  against GrantThai rules), then one `build/NRIIS_SUBMISSION.md`, then one
  human-approved submission.
- **P2 Research logic is the truth.** NRIIS is only a render target.
  Nobody authors `NRIIS.*` fields directly.
- **P3 No AI required.** Every role can finish every core task without AI,
  without network access, and without the NRIIS API. At least one path
  (the offline web form) needs no terminal either.
- **P4 AI proposes, never proves.** AI output is never `SOURCE` and never
  moves above `DRAFT`. AI critique is never recorded as an independent
  review of a research project.
  AI-proposed items face a *higher* acceptance bar than a human author's
  own judgment.
- **P5 Experience is not evidence.** Lived experience is `ORIENTING`. It
  becomes `SUPPORTING` only when re-collected under a declared method.
- **P6 Time-bound rules live only in dated fund profiles.**
- **P7 Mark missing input; never invent it.** Use `NEEDS_INPUT` or
  `NEEDS_VERIFICATION`.
- **P8 Never force a category.** Ecosystem and policy positions are
  optional. Only declared positions are checked.
- **P9 Humans decide.** Every build carries `direct_submit: false` and
  `human_final_approval_required: true`.
- **P10 Status states its basis.** Any "checked" or "verified" status is
  rendered with who checked it and how independent they were.
- **P11 Advisory text is not enforcement.** AI flags in `ai.json` and
  `llms*.txt` are requests to the reader. The real guards are the
  status-permission code and CI.

**Canonical chain (amended):** LIVED EXPERIENCE → TRANSLATION (by a person;
AI-assisted optionally) → RESEARCH METHOD → HUMAN/EXPERT VALIDATION →
VERIFIABLE KNOWLEDGE → SOCIAL/ECONOMIC/PUBLIC VALUE. See
`spec/common/chain.yaml` for the full node/edge graph.

## 3. Modes

All modes compile to the same `project.yaml` (the one canonical input).

| Mode | Surface | Primary users | AI | Ships |
|---|---|---|---|---|
| Expert Mode | offline HTML form, `grantthai fill --interactive`, or direct YAML | lecturer, university/independent researcher, graduate student | optional (v0.3+) | v0.1 |
| Human-direct | `forms/*.md` or `project.yaml` in any editor, then `validate`/`build` | any expert user, administrator | none | v0.1 |
| Citizen Mode | plain-Thai questionnaire, experience first, fund last | citizen, practitioner, civil-society actor, social entrepreneur | optional (v0.3+); never writes Problem/Gap/RQ/Evidence text | v0.2 |
| Review view | `grantthai review --as <role> --scope` | expert reviewer, mentor, administrator | none | v0.2 |

Roles (`spec/common/roles.yaml`) are self-declared UX defaults, never
permissions. Status authority comes from review-gate records
(`spec/common/review_gates.yaml`), not role tags — GrantThai cannot verify
employment or degrees. PI eligibility is decided only by the bound fund
profile (`ELIG001`); the core schema holds no eligibility thresholds.

## 4. Architecture

```
 STREAM A (lived experience)          STREAM B (academic knowledge)
        \                                     /
         +--> TRANSLATION: person (default) | AI-assisted (optional, v0.3) --+
               (AI output = PROPOSED Mapping only, never SOURCE)             |
                                                                            v
 PERSON ===(direct edge, no AI)===> RESEARCH PROJECT CORE (project.yaml, fund-independent)
                   |  <-- Evidence + source manifest
                   |  + Toledo bridge KG (LocalTerm/Concept mappings)
                   |  (PROFILE.* fields may be pre-filled from an optional local
                   |   profile.yaml while editing; build never reads profile.yaml)
                   |-- Fund Profile <agency>/<call-id>@<ver> (dated; bound reference)
                   |-- Ecosystem positions (optional, dated, RELAYED)
                   v
         DETERMINISTIC VALIDATORS (JSON Schema = structure; Python rules = logic)
                   v
         REVIEW GATES RG0-RG4 (named human records)
                   v
         NRIIS MAPPING <form>@<observed-date> --> RENDERER (Jinja2, deterministic)
                   v
         build/NRIIS_SUBMISSION.md (+ optional RESEARCH_CONCEPT_NOTE.md)
                   v
         Person copies/pastes | optional browser-assist (v0.4)
                   v
         Research -> Validated knowledge -> User/Adoption -> Outcome -> Impact -(feedback)-> Need
```

The `PERSON ===(direct edge, no AI)===>` edge is the bypass edge: a person can
always author the research project core without any AI. Every diagram in
this repository draws it (here, in `docs/ecosystem.md`, and in
`spec/common/chain.yaml` as `human_direct: [Person, Project]`).

**Packages** (`src/grantthai/`): AI-free core — `core`, `validators`,
`review`, `fund`, `mapping`, `render`, `interview`, `cli`. Optional —
`assist` (v0.3, extra `grantthai[ai]`), `mcp` and `api` (v0.4). No core
package may import `assist`, `mcp`, `api`, or any LLM SDK
(`tools/ci/check_no_ai_import.py` enforces this).

See `docs/ecosystem.md` for where GrantThai sits relative to the wider
Toledo conceptual framework and the Thailand R&I ecosystem.

## 5. Data contracts (summary — see `spec/` for the authoritative schemas)

- **Field IDs:** `<NS>.<GROUP>[.<SUB>].<NAME>`, `[A-Z0-9_]` only, never
  reused (renames go through `registry/aliases.yaml`). Render-only
  namespace `NRIIS.<TAB>.<FIELD>` is produced only by mappings.
- **Provenance:** four classes — `SOURCE`, `INFERENCE`, `DECISION`,
  `DERIVED` — plus `source_type`, `evidence_role`
  (`ORIENTING`/`SUPPORTING`), and `authored_by`
  (`human`/`human_ai_assisted`/`ai_draft`/`imported`, self-declared and
  unverified). `AI_TRANSLATION_PROPOSAL` is never `SOURCE`.
- **Status vocabulary:** `EMPTY → NEEDS_INPUT → DRAFT →
  STRUCTURE_CHECKED → LOGIC_LINKED → HUMAN_REVIEWED → VERIFIED → LOCKED →
  SUBMITTED`, plus `NEEDS_VERIFICATION`, `HOLD_FOR_VERIFICATION`,
  `UI_DRIFT`. `VERIFIED` with `independence: self` renders as
  `AUTHOR_CHECKED`.
- **Review gates:** RG0 intake, RG1 concept, RG2 method, RG3 claim, RG4
  pre-lock. A missing gate never blocks `build` — it downgrades claim
  strength and adds a `hold_reason`.
- **Mappings:** the LocalTerm→AcademicConcept bridge only. A human
  self-accepts with disclosure (`ACCEPTED_SELF`); an AI proposal accepted
  by the requester (`ACCEPTED_BY_REQUESTER`) caps claims at `CONTRIBUTORY`.
- **Fund profiles:** `funds/<agency>/<call-id>@<major.minor>/`, with
  `status`, `effective_from/to`, `verified_at`, `source_manifest` (no
  author metadata), and per-rule `trust_level`
  (`FICTIONAL`/`COMMUNITY_EXTRACTED`/`HUMAN_VERIFIED`/`SECOND_CHECKED`).
- **Precedence:** law > current call > funder guide > institution rule >
  current NRIIS requirement > project decision > historical guide.
  Conflicts are surfaced, never merged.

## 6. `build/NRIIS_SUBMISSION.md`

See `spec/output/nriis-submission.contract.md` for the full contract:
frontmatter fields, the four-layer body (readiness summary; copy/paste
fields by NRIIS tab; machine field metadata; validation/provenance
appendix), and the invariants (markers never dropped, deterministic
output, no timestamps in the body, personal data stays private). Release
QA (AT-5) needs a human cold read; an AI cold read is optional and
additional, never required, and no cold read is ever a condition for a
user to use their own file.

## 7. Interfaces

Core CLI commands (`init`, `fill --interactive`, `set`, `import-form`,
`validate`, `explain`, `fund check`/`fund stale`, `build`, `export`,
`doctor`, plus v0.2's `interview`, `review`, `accept-mapping`/`reject-mapping`,
`build --concept-note`, `lock`, `diff`) are all AI-free and network-free.
The double-click launchers wrap `import-form`, `validate` and `build`; the
offline web form edits and exports `project.yaml`. Launchers need a local
Python with GrantThai installed from the downloaded repository (no network
after download); how that install is packaged for non-technical users is
`NEEDS_INPUT` for v0.1. See `spec/contracts/one-input-one-output.md` for
the full command table. Optional interfaces
(`grantthai[ai]` v0.3; MCP/REST/browser-assist v0.4) implement the same
functions and can never exceed `DRAFT` or submit anything. See
`spec/common/parity.yaml` for the AI/human parity manifest.

## 8. Governance, licensing, privacy, security

See `GOVERNANCE.md`, `LICENSE`/`LICENSES/`/`REUSE.toml`, `PRIVACY.md`,
`SECURITY.md`. In summary: maker ≠ checker on every PR; code is
Apache-2.0, docs/spec/ontology/templates/data are CC BY 4.0 (founder
ruling K13; `REUSE.toml` is the per-path map); there is no server
in v0.x and no data collection; `gitleaks` runs in CI.

## 9. What is excluded from this repository

The original handoff package as-is, source PDFs, the NRIIS-screenshot
readout, the Toledo concept reference image, private workspaces, and
any real fund/proposal data. See `docs/sources.md` for the full
bibliographic list (hashes only, no author metadata) and
`docs/deviations.md` for every intentional departure from the original
package.

## 10. Roadmap

Phase 0 (tree skeleton, governance/policy files) → **v0.1.0 "Lecturer, no
AI" (released 2026-09-25: engine, one fund profile, one worked example,
skill, MCP server and HTTP API)** → v0.2 "Citizen, no AI" + review + lock →
v0.3 optional AI assist → v0.4 REST/browser-assist interfaces → v0.5 real
fund profiles/network/labels. Full detail, per-phase files and acceptance
criteria: `docs/BUILD_GUIDE.md`.
