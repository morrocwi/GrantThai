# GrantThai — standalone system guide

*(Replaces the working name `OPEN_THAI_RESEARCH_STANDALONE.md` used during
planning — see decision K3. This is the system/architecture description
for any reader: contributor, reviewer, or another AI builder.)*

> GrantThai is an independent, unofficial project. It is NOT affiliated with, endorsed by, sponsored by, or officially connected to NRCT, TSRI, any PMU, or NRIIS. / GrantThai เป็นโครงการอิสระ ไม่เป็นทางการ และไม่ผูกพันกับ วช. สกสว. หน่วยบริหารจัดการทุน (PMU) ใด ๆ หรือระบบ NRIIS
>
> See `NOTICE`.

## 1. Purpose

GrantThai is open research infrastructure that helps any person turn a
real problem into one work object (`work.yaml`), checks it against
GrantThai's own rules (`validators/rules.yaml`), then renders that object
through the **route the person chooses** to exactly one file:
`build/ACADEMIC_ARTICLE.md` (academic article), `build/NRIIS_SUBMISSION.md`
(NRIIS research proposal) or `build/RESEARCH_CONCEPT_NOTE.md` (concept
note). Entering NRIIS is one route of this router, not the core (founder
reframe, 2026-09-25: "การลงใน NRIIS ไม่ใช่แกนหลักอีกต่อไป แต่เป็นแค่ทางเลือกหนึ่งของ
router เพราะเราจะเปิดให้ตั้งแต่การทำบทความวิชาการด้วย"). "Router" means a
deterministic output route declared by a person, never a choice made by an
AI. GrantThai is unofficial.
It has no affiliation with NRCT, TSRI, any PMU, or NRIIS (see `NOTICE`),
and it is not affiliated with any journal or publisher. See the README
philosophy sentences and `spec/contracts/one-input-one-output.md` for the
headline contract this entire system exists to serve.

## 2. Principles

- **P1 One object.** One piece of work gives one work object (checked
  against GrantThai rules), then exactly one file per route the person
  chooses, then one human-approved use of that file (a submission, a
  manuscript the person finishes, a note the person shares).
- **P2 Research logic is the truth.** NRIIS, a journal and a concept note
  are only render targets. Nobody authors `NRIIS.*` fields directly, and
  GrantThai never composes an article's section text.
- **P1a The person routes.** A route is declared in `work.yaml` or on the
  command line. The tool never picks between routes; when the choice is
  ambiguous it lists the candidates and stops. An AI surface may list
  routes and ask, never choose.
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

All modes compile to the same `work.yaml` (the one canonical input; a
legacy `project.yaml` is read unchanged as the NRIIS route).

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
         ROUTER (routes/INDEX.yaml; the person declares the route, never an AI)
           |                        |                          |
           v                        v                          v
  nriis-proposal            academic-article              concept-note
  NRIIS MAPPING             placement.yaml +              placement.yaml
  <form>@<observed-date>    sub-profile (NEEDS_VERIFICATION)
           |                        |                          |
           v                        v                          v
  RENDERER (Jinja2, deterministic; one template per route; NOTICE on body line 1)
           |                        |                          |
           v                        v                          v
  build/NRIIS_SUBMISSION.md  build/ACADEMIC_ARTICLE.md  build/RESEARCH_CONCEPT_NOTE.md
  (submittable: fund only)   (manuscript_ready: no BLOCK) (never submittable)
                   v
         Person copies/pastes, finishes the manuscript, or shares the note | optional browser-assist (v0.4)
                   v
         Research -> Validated knowledge -> User/Adoption -> Outcome -> Impact -(feedback)-> Need
```

The `PERSON ===(direct edge, no AI)===>` edge is the bypass edge: a person can
always author the research project core without any AI. Every diagram in
this repository draws it (here, in `docs/ecosystem.md`, and in
`spec/common/chain.yaml` as `human_direct: [Person, Project]`).

**Packages** (`src/grantthai/`): AI-free core — `core`, `validators`,
`review`, `fund`, `mapping`, `routes` (route registry and resolution),
`render` (one renderer per route, dispatched in `render/__init__.py`),
`interview`, `cli`. Optional —
`assist` (v0.3, extra `grantthai[ai]`), `mcp` and `api` (v0.4). No core
package may import `assist`, `mcp`, `api`, or any LLM SDK
(`tools/ci/check_no_ai_import.py` enforces this).

See `docs/ecosystem.md` for where GrantThai sits relative to the wider
Toledo conceptual framework and the Thailand R&I ecosystem.

## 5. Data contracts (summary — see `spec/` for the authoritative schemas)

- **Field IDs:** `<NS>.<GROUP>[.<SUB>].<NAME>`, `[A-Z0-9_]` only, never
  reused (renames go through `registry/aliases.yaml`). Render-only
  namespace `NRIIS.<TAB>.<FIELD>` is produced only by mappings.
- **Registry partition (0.3):** every field carries `scope` (`shared` =
  placed by more than one route; `route` = one route's output only) and
  `route_ids`, computed by `tools/registry/partition.py` from
  `routes/INDEX.yaml`. `origin` keeps its meaning; the new value
  `VENUE_NATIVE` marks a field that exists because a publication venue
  type asks for it (the `ARTICLE.*` namespace). Every Thai label of those
  fields is `NEEDS_VERIFICATION`.
- **Routes (0.3):** `routes/<id>/route.yaml` (`spec/routes/route.schema.json`)
  names the accepted work types, whether a fund binding is needed, exactly
  one template, one output filename, one contract, a placement, optional
  sub-profiles, the S001 required set, the rule families in scope and the
  ready flag. `routing` in `work.yaml` is the person's declaration and is
  excluded from `content_sha256`.
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

## 6. The outputs, one per route

`build/NRIIS_SUBMISSION.md`: see `spec/output/nriis-submission.contract.md`
for the full contract: frontmatter fields, the four-layer body (readiness
summary; copy/paste fields by NRIIS tab; machine field metadata;
validation/provenance appendix), and the invariants (markers never
dropped, deterministic output, no timestamps in the body, personal data
stays private). Unchanged by the router: a 0.2 file builds byte-identical
output (AT-R1).

`build/ACADEMIC_ARTICLE.md`: see `spec/output/academic-article.contract.md`.
A manuscript overview arranged from the researcher's own records (kind,
authors and CRediT-style roles, IMRaD or free sections, statements,
figures and tables, the target venue with the sources the researcher
supplied). `manuscript_ready` means only that no BLOCK finding is open;
it never means accepted or publishable. Body line 2 says GrantThai is not
affiliated with any journal or publisher.

`build/RESEARCH_CONCEPT_NOTE.md`: see
`spec/output/research-concept-note.contract.md`. A pre-proposal working
document; `submittable: false` always, with a HOLD. Release
QA (AT-5) needs a human cold read; an AI cold read is optional and
additional, never required, and no cold read is ever a condition for a
user to use their own file.

## 7. Interfaces

Core CLI commands (`init --work-type`, `migrate`, `set`, `route list`,
`route check`, `route build` / `build --route`, `validate --route`,
`fields --route`, `explain`, `review`, `accept-mapping`/`reject-mapping`,
`lock`, `diff`, `link`; deferred: `fill --interactive`, `import-form`,
`fund check`/`fund stale`, `export`, `doctor`, `interview`) are all AI-free
and network-free. The former `build --concept-note` flag is the
`concept-note` route.
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
fund profiles/network/labels. The **v0.3 router** (unreleased: `work.yaml`,
three routes, `route` commands, `migrate`, `ARTICLE.*` fields, ART rules)
landed ahead of the optional AI assist; NRIIS is one route of it. Full
detail, per-phase files and acceptance criteria: `docs/BUILD_GUIDE.md`.
