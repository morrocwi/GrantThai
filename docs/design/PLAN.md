# GrantThai design plan (historical record)

> **Status of this document.** This is the founder-owned design plan
> ("final work plan", 2026-09-25) that the Phase 0 scaffold was built from.
> The founder owns it (see `GOVERNANCE.md`, founder decisions log, K13) and
> it is published here so that every reference in this repository can be
> followed without any private file. It is a **historical record of the plan
> as written on 2026-09-25, before the founder's rulings of the same day**.
> Where this plan and `spec/`, `GOVERNANCE.md` or `docs/deviations.md`
> differ, **those files win**; this file is not edited to track them.
>
> Editorial changes made for publication (nothing else was changed):
> a local filesystem path was replaced by a neutral description, one
> reference to a private workspace rule was reworded, and the names of
> three excluded source files were replaced by generic descriptions (see
> `docs/sources.md`).
>
> Points in this plan that were later decided or superseded (details in
> `GOVERNANCE.md`, "Founder decisions log"):
>
> - **K1, K13, K14** were ruled by the founder on 2026-09-25. K13: the
>   founder owns core 01–06; derivatives are licensed Apache-2.0 (code) and
>   CC BY 4.0 (docs, spec, data). K14: labels from the screenshot-derived
>   readout are not used; NRIIS labels and tab order come later from public
>   documents and stay `NEEDS_VERIFICATION`. The "stays private until K13"
>   lines below are therefore historical.
> - **Independent check** (§H "Publication sequence", step 4): the rule
>   "AI review never counts as the independent check" was replaced by the
>   founder's policy recorded in `GOVERNANCE.md` (a checker distinct from
>   the maker, plus the human founder's approval of every public release).
> - **Cold reads** (§F invariants, §I AT-5): a human cold read is the
>   required release check; an AI cold read is optional and additional, never
>   required, and never a condition for a user to trust their own file.
> - **Profile** (§B, §C): `profile.yaml` is an editor convenience only;
>   `grantthai build` never reads it. Identity and team data used in a
>   submission live in `project.yaml` (`PROFILE.*` fields). See
>   `spec/contracts/one-input-one-output.md`.
> - **Public wording** (§E): GrantThai says "checked against GrantThai
>   rules", not "validated".
> - **CC0** (§H licences): not used; there is no CC0 content in this
>   repository.

---

GrantThai final work plan (chair), 2026-09-25

---

## บทสรุปสำหรับผู้ก่อตั้ง (Thai executive summary)

GrantThai คือโครงสร้างพื้นฐานวิจัยแบบเปิดภายใต้ Toledo Framework ใช้เปลี่ยนปัญหาจริงให้เป็น "โครงการวิจัยหนึ่งชิ้นที่ผ่านการตรวจแล้ว" จากนั้นเรนเดอร์ออกมาเป็นไฟล์ `build/NRIIS_SUBMISSION.md` เพียงไฟล์เดียว NRIIS เป็นแค่ปลายทางของการแสดงผล ตรรกะงานวิจัยเป็นตัวตั้ง

ตามที่ผู้ก่อตั้งแก้ไขเพิ่มเติม **AI เป็นตัวเลือกเสริมทุกขั้น ไม่ใช่แกนหลัก** อาจารย์หรือนักวิชาการลงทะเบียนและทำโครงการจนได้ไฟล์ส่งครบได้เองโดยไม่ใช้ AI ไม่ต้องต่อเน็ต และไม่ต้องใช้ terminal เพราะมีฟอร์ม HTML แบบออฟไลน์ให้ด้วย

การแก้ไขหลักหลังรอบ critic มีดังนี้
1. ลำดับเวอร์ชันใหม่: v0.1 = อาจารย์ทำเองโดยไม่ใช้ AI, v0.2 = ประชาชนทำเองโดยไม่ใช้ AI, v0.3 = เพิ่ม AI แบบเลือกใช้ได้, v0.4 = MCP/REST, v0.5 = ทุนจริง
2. ข้อเสนอ mapping ที่มาจาก AI ผ่านได้ยากกว่างานของนักวิชาการ ไม่ใช่ง่ายกว่า
3. คำว่า VERIFIED ที่ได้จากการตรวจงานตัวเองจะแสดงเป็น AUTHOR_CHECKED
4. สร้าง repo เป็น PRIVATE ก่อน และจะเปลี่ยนเป็น public หลังผ่าน gate อิสระเท่านั้น
5. ติดตั้ง hook ห้ามชื่อ AI/vendor ตั้งแต่ commit แรก

**เรื่องที่ต้องให้ผู้ก่อตั้งตัดสินก่อนเผยแพร่สาธารณะ (หมวด K)**
- K1: ถ้อยคำปรัชญาประโยคที่ 2
- K13: ใครเป็นผู้เขียนและใครถือสิทธิ์ในเอกสาร core 01–06
- K14: ที่มาของ label ภาษาไทยของ NRIIS ที่ได้จากภาพหน้าจอ
- K7: สัญญาอนุญาต (licence)
- K4: ความเสี่ยงเรื่องชื่อหรือการสื่อว่าได้รับการรับรอง

---

**Tags.**
- VERIFIED: read in the package. Line cites are relayed from the seat digests. I re-read these myself: the 01 §63 MVP list, 01 `submission_mode.ai_assisted_fill: true`, the 01 lock prerequisite "Fund profile current = YES", 05 having 0 `label_th` keys, and brief lines 12-25, 98-106 and 190-216.
- INSTINCT: a design judgment.
- OPEN: unresolved.
- NEEDS_VERIFICATION: a Thai rule or fact that is tied to a date or edition.

I wrote no files and ran no git. The plan has no equations. The arithmetic checks are validation rules, not Toledo objects.

Package root: the private handoff package (not in this repository; see `docs/sources.md`).

## A. Purpose and principles

**Purpose.** GrantThai is open research infrastructure in Yaoharee Lahtee's Toledo Framework (conceptual framework only; see H).
- It helps any person turn a real problem into one validated research project object.
- It renders that object to one `build/NRIIS_SUBMISSION.md`.
- It is unofficial and has no affiliation with NRCT, TSRI, any PMU or NRIIS.

**Philosophy sentences.** Verbatim, used in the README, `llms.txt` and `ai.json`:
1. "GrantThai lowers the entry barrier to research, not the standard of research."
2. "Toledo connects lived experience with academic knowledge through AI-assisted translation, while evidence, methodology, and human expertise remain the gates to verifiable knowledge."

Sentence 2 makes AI mediation the headline (K1). Resolving it is a **blocker for the first public push**, though it does not block local scaffolding. The chair proposes this wording to the founder, and makes no silent change: "...through translation — by people, and optionally with AI assistance — while evidence, methodology, and human expertise remain the gates to verifiable knowledge." Until the founder rules, the verbatim sentence is followed by: "Translation may be done by a person alone; AI assistance is optional at every step."

**Principles (binding):**
- **P1 One object.** One project gives one validated project object, then one `build/NRIIS_SUBMISSION.md`, then one human-approved submission (B:38-43).
- **P2 Research logic is the truth.** NRIIS is only a render target. Nobody authors `NRIIS.*` fields directly (A:999, 02:1727).
- **P3 No AI required.** Every role can finish every core task without AI, without network access and without the NRIIS API: register, author, validate, build, review and lock. At least one of these paths needs no terminal either.
- **P4 AI proposes, never proves.**
  - AI output is never SOURCE and never moves above DRAFT.
  - AI critique is never an independent review.
  - AI-proposed items face a *higher* acceptance bar than a human author's own judgment.
- **P5 Experience is not evidence.** Lived experience is ORIENTING. It becomes SUPPORTING only when it is re-collected under a declared method.
- **P6 Time-bound rules live only in dated fund profiles** (A:104, 03:2432, 04:120-145).
- **P7 Mark missing input; never invent it.** Use NEEDS_INPUT or NEEDS_VERIFICATION (B:148-156).
- **P8 Never force a category.** Ecosystem and policy positions are optional. Only declared positions are validated.
- **P9 Humans decide.** Every build carries `direct_submit: false` and `human_final_approval_required: true` (A:561-563).
- **P10 Status states its basis.** Any "checked" or "verified" status is rendered with who checked it and how independent they were.
- **P11 Advisory text is not enforcement.** AI flags in `ai.json` and `llms*.txt` are requests to the reader. The real guards are the status-permission code and CI.

**Canonical chain (amended).** LIVED EXPERIENCE → TRANSLATION (by a person; AI-assisted optionally) → RESEARCH METHOD → HUMAN/EXPERT VALIDATION → VERIFIABLE KNOWLEDGE → SOCIAL/ECONOMIC/PUBLIC VALUE.
- The brief B:12-25 has "AI-SUPPORTED TRANSLATION" and "AI is a translator, scaffold, router" (VERIFIED). The amendment overrides these.
- "router" is dropped from all repo prose.

## B. User roles and modes

**Modes.** All modes compile to the same `project.yaml` (A:2417).

| Mode | Surface | Primary users | AI | Ships |
|---|---|---|---|---|
| **Expert Mode** | A field-by-field form through one of three routes: the offline static HTML form (no terminal), `grantthai fill --interactive`, or direct YAML. The full chain is shown, and the policy layer is optional. | lecturer, university or independent researcher, graduate student | optional (v0.3+) | v0.1 |
| **Human-direct** | Per-tab `forms/*.md` or `project.yaml` in any text editor, then `validate` and `build` | any expert user, administrator | none | v0.1 |
| **Citizen Mode** | Plain-Thai questionnaire. Q0a asks "what happened?" and Q0b "what words does your community use?". Then come the 12 Simple-mode questions (A:2380-2393), experience first and fund last, each with a "why this matters" card. | citizen, practitioner, civil-society actor, social entrepreneur | optional (v0.3+); never writes Problem, Gap, RQ or Evidence text | v0.2 |
| **Review view** | `grantthai review --as <role> --scope` writes named review records | expert reviewer, mentor, administrator | none | v0.2 |

- Expert Mode can start from either the fund or the problem. Citizen Mode starts from experience. Both entry points merge at PROBLEM.
- The README's first screen is the no-AI lecturer path.

**Roles** are self-declared capability tags in `profile.yaml`. They are **UX defaults, not permissions**: they choose the default mode and the wording of guidance.
- Status authority comes from gate records (E), not from role tags, because GrantThai cannot verify employment or degrees.
- PI eligibility is decided only by the attached fund profile (ELIG001). The core holds no eligibility thresholds.
- The Citizen "partner needed" gate text says "the fund profile decides eligibility". It does not quote บพข./บพค. thresholds, which are NEEDS_VERIFICATION.

Role tags: citizen, practitioner, civil_society, social_entrepreneur, graduate_student, lecturer, university_researcher, independent_researcher, research_administrator, expert_reviewer, mentor. Institution is a record, not a person.

**Registration (v0.x).**
- `grantthai init --role --lang`, or the HTML form's "New profile", writes a local, user-owned `profile.yaml` (02 group 00, 02:1406-1450) and a private workspace outside the repo.
- There are no accounts, no server and no OAuth. ORCID is optional and typed by hand. NRIIS credentials are never stored (A:2005-2018).
- A hosted account layer is deferred until a DPIA and a named PDPA data controller exist. It would call the same library and export the same files.
- This reading of "ลงทะเบียนเข้าระบบเอง" (registering oneself) is INSTINCT (K2).

**Citizen with no eligible PI (v0.2).**
- The build always renders. With no eligible PI it carries `submittable: false` and `HOLD_FOR_VERIFICATION` (04:359-362).
- `--concept-note` renders `build/RESEARCH_CONCEPT_NOTE.md` from the same object.
- The chair default produces both files (K5).

## C. System architecture

```
 STREAM A (lived experience)          STREAM B (academic knowledge)
        \                                     /
         +--> TRANSLATION: person (default) | AI-assisted (optional, v0.3) --+
               (AI output = PROPOSED Mapping only, never SOURCE)             |
 Profile --> RESEARCH PROJECT CORE (project.yaml, fund-independent) <-- Evidence + source manifest
                   | + Toledo bridge KG (LocalTerm/Concept mappings)
                   |-- Fund Profile <id>@<ver> (dated; bound at build time)
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
 (every diagram also draws a direct Person -> Research Core edge that bypasses AI)
```

**Packages.** Everything lives under `src/grantthai/`:
- AI-free core: `core`, `validators`, `review`, `fund`, `mapping`, `render`, `interview`, `cli`.
- Optional: `assist` (v0.3, extra `grantthai[ai]`), plus `mcp` and `api` (v0.4).

**Hard rule.** No core package imports `assist`, `mcp`, `api` or any LLM SDK. CI enforces this with import-lint.
- The fund profile is a parallel input bound at build time (A:192-193).
- The spec's AI Router, Writer and Reviewer lane (A:200-205) becomes optional and lives in `assist`.

## D. Repository tree (public engine only)

```
GrantThai/
  README.md          TH/EN. Order: no-AI lecturer quickstart; philosophy lines; unofficial notice;
                     "no Toledo equations or proofs here"; AI-optional parity table; links to AI files;
                     footer = Core Epistemic Structure block
  GRANTTHAI_STANDALONE.md   system guide for any reader (replaces OPEN_THAI_RESEARCH_STANDALONE.md; K3)
  ai.json, llms.txt, llms-full.txt   discovery; flags marked ADVISORY; "AI optional"
  NOTICE             one canonical unofficial/non-affiliation list (NRCT, TSRI, PMUs, NRIIS), reused verbatim everywhere
  LICENSE, LICENSES/, REUSE.toml, CITATION.cff (founder only)
  SECURITY.md, PRIVACY.md (TH/EN), CODE_OF_CONDUCT.md, CONTRIBUTING.md (DCO), GOVERNANCE.md, CHANGELOG.md
  spec/common/  chain.yaml, status.yaml, status_permissions.yaml, review_gates.yaml (RG0-RG4),
                provenance.schema.json, roles.yaml (UX defaults), review.schema.json,
                mapping_proposal.schema.json, evidence.schema.json, parity.yaml
  spec/profile/profile.schema.json    spec/project/project.schema.json
  spec/fund/fund-profile.schema.json  spec/nriis/field.schema.json
  spec/mcp/tools.schema.json          contract only (implementation v0.4)
  spec/output/nriis-submission.contract.md
  registry/fields.jsonl, aliases.yaml, nriis-fields.jsonl
  mappings/nriis/section_to_tab.yaml  single versioned 05-section -> 02-tab table; others generated from it
  mappings/nriis/nrct-master-hss@<observed-date>.yaml   the only observed form (05:1)
  mappings/modes/expert_to_core.yaml (v0.1), citizen_to_core.yaml (v0.2)
  interview/expert.th.yaml (v0.1); expert.en, citizen.th, citizen.en (v0.2)
  forms/{general,project,workplan,utilization,attachments}.md
  webform/index.html  offline single-file form, no network calls, exports project.yaml (generated from registry)
  ontology/grantthai.jsonld, context.jsonld (v0.1); shapes.shacl.ttl generated from chain.yaml (v0.2)
  ontology/bridge/ (v0.2); ontology/local_terms.yaml (human-curated, dated seed; v0.2)
  funds/_template/; funds/example/FICTIONAL_CALL@0.1/ (ACTIVE, fictional values, trust_level: FICTIONAL)
  ecosystem/positions@2026-09.yaml   optional picklist, RELAYED, dated (v0.2)
  validators/rules.yaml, crosswalk.yaml (v0.2)
  templates/nriis_submission.md.j2, research_concept_note.md.j2 (v0.2), project.blank.yaml
  launchers/         double-click build/validate scripts (Linux/macOS/Windows) that wrap the CLI
  src/grantthai/...  (C)
  network/*.schema.yaml   schema only, ship empty (letter §14; v0.5)
  docs/th, docs/en   for-lecturers-no-ai, for-citizens, for-administrators, for-fund-profile-maintainers,
                     quality-gates, evidence-model, glossary, how-to-find-a-partner, sources, lineage, deviations
  examples/lecturer-no-ai/ (v0.1); citizen-no-ai/, citizen-with-pi-partner/ (v0.2); citizen-ai-assisted/ (v0.3)
                     every example file carries a FICTIONAL banner
  tests/ golden, fixtures/{positive,negative/<rule_id>}, acceptance, test_no_ai_import, test_determinism,
         test_invariants (hypothesis), test_no_hardcoded_rules, test_parity_manifest (v0.3)
  .githooks/commit-msg      vendor-attribution block, installed before commit #1
  .github/workflows/ ci, schema, leak-scan, reuse, fund-profile-ci, attribution-scan (full history + PR title/body
                     + release notes), staleness-report (monthly; opens an issue, never edits), parity (v0.3)
  .github/CODEOWNERS  funds/**, spec/**, NOTICE need a maintainer
  .gitignore          A:467-480 + profile.yaml, build/, workspaces/, *.har, cookies/, screenshots/, .env*
```

**Never committed:**
- the handoff package as-is (00 brief, core 01-06, README, MANIFEST.json);
- source PDFs, NRIIS screenshots and HAR files;
- private workspaces;
- real or anonymised proposals.

## E. Data contracts

**Field IDs.** Format `<NS>.<GROUP>[.<SUB>].<NAME>`, using `[A-Z0-9_]`. IDs are never reused. Renames go through `aliases.yaml`.
- Authoring namespaces: PROFILE, FUND, CORE, METHOD, WORK, GEO, BUDGET, COMP, READY, RESULTS, DOC, AUDIT, BRIDGE.
- Render-only namespace: `NRIIS.<TAB>.<FIELD>` (A:577), produced only by mappings.
- Field records use the 02:131-142 fields, plus `authored_by`, `guidance{th,en}` (replacing `ai_prompt`) and `derived_from: core/0N@sha256`.
- Array items get sub-schemas from 02.

**Labels.**
- 05 has 0 `label_th` keys (VERIFIED). v0.1 renders the English label plus `LABEL_TH: NEEDS_VERIFICATION`.
- Thai labels enter only from public call or TOR documents, or from a dated human capture after the NRIIS terms of use are checked (K14).

**Provenance.** The four classes stay unchanged: SOURCE, INFERENCE, DECISION, DERIVED (B:139-144, 04:1284). Three orthogonal fields are added:
- `source_type`: the 01:1374-1384 types, plus LIVED_EXPERIENCE_ACCOUNT, PRACTITIONER_KNOWLEDGE, EXPERT_REVIEW_RECORD and AI_TRANSLATION_PROPOSAL.
- `evidence_role`: ORIENTING or SUPPORTING.
- `authored_by`: human, human_ai_assisted, ai_draft or imported. It is **self-declared and unverified**, never a quality signal, and the output disclaimer says so.

Two rules follow. AI_TRANSLATION_PROPOSAL is never SOURCE. A citizen's account is SOURCE only for "person reported X".

**Status vocabulary** (`status.yaml`):
- EMPTY → NEEDS_INPUT → DRAFT → STRUCTURE_CHECKED → LOGIC_LINKED → HUMAN_REVIEWED → VERIFIED → LOCKED → SUBMITTED.
- Separate markers: NEEDS_VERIFICATION, HOLD_FOR_VERIFICATION, UI_DRIFT.
- Field LOCKED and object LOCK are documented as different things.
- STRUCTURE_CHECKED means "schema-valid; source reference present and resolvable". It does *not* mean the source supports the value.
- LOGIC_LINKED means "required chain links exist". It does *not* mean the method fits.
- These names deliberately depart from 01:626-636, which lets AI set the checked states. The departure is recorded in `docs/deviations.md`.

| Transition | Who can make it |
|---|---|
| EMPTY → NEEDS_INPUT → DRAFT | any author, human or AI-assisted |
| DRAFT → STRUCTURE_CHECKED → LOGIC_LINKED | deterministic validator pass only |
| → HUMAN_REVIEWED, VERIFIED | a named human via a review record with scope and independence (`self` or `independent`) |
| → LOCKED | named human; needs 01:2210-2216 (BLOCK = 0, budget reconciled, human review present, fund profile ACTIVE and current); any edit breaks the lock |
| → SUBMITTED | recorded by a named human after the external act |

- MCP, REST and `assist` can never set anything above DRAFT.
- Rendered basis: `VERIFIED` with `independence: self` renders as **`AUTHOR_CHECKED`**. `VERIFIED(independent: <role>, <date>)` renders as written.
- Public prose says "validated against GrantThai rules". The founder's own term "verified project object" is kept only in `docs/lineage.md`.

**Review gates** (`spec/common/review_gates.yaml`). The RG prefix avoids a clash with the G001-G003 geography rules.
- RG0 intake complete; RG1 concept (LocalTerm/Concept); RG2 method; RG3 claim; RG4 pre-lock.
- A "named review record" is a reviewer name, role, scope, independence, date and the sha256 of the object reviewed. There is no cryptographic signing in v0.x.
- A missing gate **never blocks** `build` or the concept note. It downgrades claim strength and adds a `hold_reason`.
- Self-review is allowed and disclosed, and blocks only when the fund profile sets `independent_review_required` (K6).

**Mappings.** `Mapping` exists only for the Stream-A bridge (LocalTerm → AcademicConcept). An expert who uses a concept they already know needs no Mapping.

| proposed_by | Acceptance | Resulting state | Downstream limit |
|---|---|---|---|
| human (the author) | self-accept, `independence: self` disclosed | ACCEPTED_SELF | none beyond the normal claim rules |
| ai | accepted by the requester only | ACCEPTED_BY_REQUESTER | cannot support a Claim above CONTRIBUTORY; listed in the readiness summary |
| ai | review record with reviewer ≠ requester, role and independence given | ACCEPTED_REVIEWED | normal |
| any | none | PROPOSED | X002 blocks downstream use |

**Chain.** `spec/common/chain.yaml` is the union of B:74-91, P10, A:771-782 and letter §6.
- Two entry points merge at PROBLEM: Experience → Observation → Problem, and Need → Problem.
- The shared spine continues: PriorKnowledge (required) → Gap → RQ → Objective → Framework → Hypothesis → Method → Activity → Data → Analysis → Evidence → Claim → Output → User → Adoption → Outcome → {Beneficiary, Impact} → KR.
- `causal` edges form a DAG, checked by CH001. `feedback` edges may loop: KR→Need and Impact→KR.
- Direction choices: Activity→BudgetItem, Method→EthicsRequirement, Hypothesis→Method.

**Knowledge graph (KG).**
- Core nodes, about 27: Project, Person, Need, Problem, PriorKnowledge, Gap, ResearchQuestion, Objective, Construct, Hypothesis, Method, Activity, BudgetItem, Site, Partner, EthicsRequirement, Evidence, Claim, Output, User, Adoption, Outcome, Beneficiary, Impact, FundCall, FundObjective, FundKR.
- Bridge nodes (v0.2): LivedExperience, Observation, PractitionerKnowledge, LocalTerm, AcademicConcept, ResearchConcept, Expert, Institution, ResearchNetwork, Mapping, ReviewRecord.
- AI translation is modelled as a Mapping with `proposed_by.kind=ai`, not as a node type.
- Edges: the letter §11 edges, plus the human-direct edges Person-proposesMapping, Person-consults→Expert, Person-partnersWith→Institution and Person-seeksReview→Expert.
- The 45-node model (A:1157-1208) is deferred.

**Validation engines.** There are two, not three.
- JSON Schema checks structure. Python rules in `validators/rules.yaml` check logic.
- SHACL is *generated* from `chain.yaml` in v0.2, never hand-maintained.
- Leaving SHACL out of v0.1 departs from 01 §63 item 6 (VERIFIED) and needs founder sign-off (K15).

**Rule families.** Canonical IDs use the 01 families. IDs from 02, 04 and 05 are aliases in `crosswalk.yaml` (v0.2). Each rule has a severity of BLOCK, REVIEW or INFO.

| Ships | Family | What it checks |
|---|---|---|
| v0.1 | S, R, W, B (01:1541-1617) | structure, research logic, workplan sums to 100, budget (line = qty×persons×times×unit; totals match) |
| v0.1 | T001 | team contributions sum to 100 (02:1605) |
| v0.1 | CH001-CH002 | causal DAG; required stages present |
| v0.1 | F001-F004 | fund rule has a source; staleness; profile ACTIVE; no historical rule reused (03:2334-2367) |
| v0.1 | ELIG001 | PI eligibility per the fund profile |
| v0.2 | CH003 | claim-strength downgrade (02:1194-1199) |
| v0.2 | E, E006-E008 | ethics; third parties, dual roles and vulnerable groups in experience accounts |
| v0.2 | U, P, G | utilization, policy, geography |
| v0.2 | X001-X006 | experience used as SUPPORTING; PROPOSED mapping used downstream; ai_draft marked SOURCE; claim with no evidence path; review lacking scope, identity or date; review used as empirical evidence |
| v0.2 | ECO* | ecosystem checks for declared positions only |
| CI only | PARITY, DET | build parity and determinism |

**Precedence.** Law > current call > funder guide > institution rule > current NRIIS requirement > project decision > historical guide (04:65-81, 03:2334-2367).
- Conflicts are surfaced, never merged (A:1406-1412).
- The brief's list (B:249-255) is rewritten to point here.

**Fund profiles.** Stored at `funds/<agency>/<call-id>@<major.minor>/`.
- Fields: `status` (DRAFT, ACTIVE or EXPIRED), `effective_from/to`, `verified_at`, and a `source_manifest` (title, issuer, edition, URL, sha256, retrieval date; no author metadata).
- Every rule records `{value, source_id, locator, quoted_text_th, trust_level, verified_at, verified_by_role}`.
- Trust levels: FICTIONAL, COMMUNITY_EXTRACTED (AI extraction allowed; a human double-check is required before use), HUMAN_VERIFIED, SECOND_CHECKED.

**No-hardcoded-rules CI.**
- Allowlisted paths: `funds/`, `examples/`, `NOTICE`, `docs/sources.md`, `mappings/nriis/`, and the single disclaimer constant.
- Elsewhere CI rejects agency acronyms, and numbers next to a unit: `บาท`, `baht`, `ปีงบประมาณ`, `FY`.
- It does not reject bare `25\d\d`.

## F. `build/NRIIS_SUBMISSION.md` contract

The filename is the founder's letter contract (§9), so it stays. Whether it implies endorsement is K4.

**Frontmatter fields:**
- Versions and identity: `grantthai_version`, `schema_version`, `renderer_version`, `project_id`, `project_object_sha256`.
- Bindings: `fund_profile: <ID>@<ver>` with its `trust_level`, and `nriis_mapping: <form>@<observed-date>`.
- `authoring: {mode: human|ai_assisted, tools_disclosed: [], self_declared: true}`. The default is `human`.
- `submission_mode: {human_copy_paste: true, ai_assisted_fill: false, direct_submit: false}`. `ai_assisted_fill` becomes true only when the user opts into browser-assist. This replaces 01:558-563, which defaults it to true (VERIFIED).
- `human_final_approval_required: true`.
- `review: {RG0..RG4: state + basis}`.
- `submittable: true|false`, meaning submittable *against the bound profile*.
- `real_world_verified: false` unless the profile's trust level is at least HUMAN_VERIFIED and every rule is current.
- `hold_reasons: []`, `stale_rules: []`, `accepted_by_requester_mappings: []`, `validation_summary: {block, review, info}`.
- `disclaimer`: the NOTICE constant.

**Body:**
- **Line 1 repeats the disclaimer** in plain text, because copy/paste usually drops the frontmatter.
- Four layers follow (A:514-520):
  1. **Readiness summary.** Every NEEDS_INPUT, NEEDS_VERIFICATION, HOLD, PROPOSED or ACCEPTED_BY_REQUESTER mapping, AUTHOR_CHECKED item and BLOCK, each with a plain-language next step.
  2. **Copy/paste fields by NRIIS tab.** General, Project, Workplan, Utilization, Attachments (02:2451-2474), via `section_to_tab.yaml`. Each block gives the label (EN, plus TH or `LABEL_TH: NEEDS_VERIFICATION`), a fenced plain value, FIELD_ID, ORIGIN, STATUS with its basis, REQUIRED, INPUT_CONTROL, DEPENDENCIES, SOURCE_IDS, VALIDATION, AUTHORED_BY, and an arithmetic check line where one applies. The spec's 00-30 section numbering (A:642-674) is form-specific and NEEDS_VERIFICATION.
  3. **Machine field metadata.**
  4. **Validation and provenance appendix.** Gate records, the source manifest (no personal data) and the conflict log.

**Invariants:**
- Markers are never dropped.
- The same locked object with the same renderer version gives byte-identical output.
- The body contains no timestamps.
- Profile PII renders only into the private `build/`.
- Two **equal** acceptance checks apply: a cold read by a human who did not write the project, and a cold read by an AI reader (B:215, VERIFIED binding).

## G. Interfaces, each with an AI-free equivalent

**Core CLI.** No network, no AI. The same functions are wrapped by `launchers/` and read by `webform/`.

| Command | Purpose | Ships |
|---|---|---|
| `init --role --lang` | registration | v0.1 |
| `fill --interactive` | guided form | v0.1 |
| `set <FIELD_ID>` | set one field | v0.1 |
| `import-form <project.yaml or forms/>` | import from the web form or Markdown forms | v0.1 |
| `validate` | run the rules | v0.1 |
| `explain <RULE_ID>` | plain-language explanation | v0.1 |
| `fund check` / `fund stale` | fund fit and staleness | v0.1 |
| `build` | render the output | v0.1 |
| `export` | excludes PII by default; `--include-private` opts in with a warning | v0.1 |
| `doctor` | refuses to build inside a public-repo clone | v0.1 |
| `interview --mode citizen\|expert` | questionnaire | v0.2 |
| `review --as --scope` | named review record | v0.2 |
| `accept-mapping` / `reject-mapping` | decide on a mapping | v0.2 |
| `build --concept-note` | concept note | v0.2 |
| `lock`, `diff` | lock and compare versions | v0.2 |

**Optional interfaces:**
- **`grantthai[ai]` (v0.3):** `assist ask`, `propose-mapping`, `find-gaps`, `search-terms`, and `draft <FIELD_ID>` (Expert Mode only; shown side by side for the user to copy in). The brief's "prompts" and "agents" folders (B:98-106, VERIFIED) live here. This deviation is recorded.
- **MCP, REST/OpenAPI and browser-assist (v0.4).**
  - They implement the Phase-0 contract `spec/mcp/tools.schema.json` (B:194 asks for the contract early; VERIFIED).
  - They are one-to-one library wrappers with no API-only logic (A:1845-1867), and they cannot set anything above DRAFT.
  - Browser-assist follows rules A1-A8, sets UI_DRIFT when the UI changes, stores no credentials or cookies, and never submits.

**Parity manifest.** `spec/common/parity.yaml` is machine-readable. From v0.3, CI fails any `assist`, MCP or REST command that has no human-equivalent command with a passing test. It is also rendered as a table in the README.

| AI feature | Human-only equivalent |
|---|---|
| intake assistant | Citizen questionnaire + `citizen_to_core.yaml` |
| field drafting | `webform/`, `forms/*.md`, `fill --interactive`, `guidance` |
| LocalTerm→Concept proposal | glossary lookup + human `proposesMapping`, or "own words + CONCEPT NEEDS_INPUT" |
| critique | `validate` + expert review record |
| fund-fit | `fund check` |
| handoff package | `NRIIS_SUBMISSION.md` + `GRANTTHAI_STANDALONE.md` |
| MCP / browser-assist | human copy/paste |

## H. Governance, licences, privacy, security, exclusions

**Rights precondition (K13, blocker for public).**
- Core 01-06 carry no author or licence line (VERIFIED, headers only). Much of them is probably AI-drafted (INSTINCT).
- The founder must confirm authorship and rights before any derived file is licensed.
- Until then, the repo stays private and every derived file keeps `derived_from: core/0N@sha256` lineage.

**Licences (K7; INSTINCT).**
- Code: Apache-2.0. Spec, docs, ontology and templates: CC BY 4.0.
- Registry and fund-profile facts: CC0-1.0 **only** where they are restated in our own words with a source. Otherwise CC BY 4.0, with a notice that no third-party rights are granted.
- Whether Thai Copyright Act s.7 covers these facts is OPEN.
- NRIIS labels carry no licence claim until K14 is resolved.
- Rendered proposals belong to the user. `reuse lint` runs in CI.
- Recorded dissent: AGPL was raised and not adopted; the founder decides.

**Authorship.** `CITATION.cff` names the founder only. No AI or vendor name appears as author, co-author or credit anywhere.
- `.githooks/commit-msg` is installed **before commit #1**. The CI attribution scan covers the full history, PR titles and bodies, and release notes.
- Every worker prompt tells the worker to omit harness-added `Co-Authored-By` trailers and "Generated with" PR footers. The founder's attribution rule overrides any harness default.
- The Core Epistemic Structure block (role disclosure) goes in `docs/lineage.md` and the README footer. This is the only place a model is named, by role.
- Contributors sign off under the DCO.

**Toledo.**
- The README states: "Toledo here means the conceptual framework; GrantThai contains no Toledo-registered equations and no proofs."
- `docs/lineage.md` holds pointers only, through main.hub routing. No Toledo content is copied.
- Banned wording: "validated by Toledo", "Coq-verified", "NRIIS-compliant", "officially compatible", "verified project object" (in public prose).
- Any future score goes through Toledo first. A single numeric quality score is rejected.

**Governance.**
- Protected main branch, maker ≠ checker on every PR.
- `funds/**` changes need a cited official source, a date and a second human.
- Dissent is kept in `GOVERNANCE.md`, and forks keep their lineage.

**Publication sequence.**
1. Scaffold locally with the chair's defaults.
2. Create `github.com/morrocwi/GrantThai` as **PRIVATE** and check visibility with `gh api`.
3. Cut PR branches from `origin/main` and check that `origin/main..HEAD` holds only the intended commits.
4. Run the independent adversarial gate. It must be a different agent or person from the maker, and AI review never counts as the independent check. It covers: leak scan with a denylist of PDF author strings, licence coverage, tier fidelity, citation accuracy, overclaim, and whether every Thai rule string is dated and sourced.
5. Get founder answers to K1, K3, K4, K7, K13 and K14.
6. Flip to public and re-check visibility.
7. If a Forgejo mirror is added, register the repo in the repository registry.

**Privacy (PDPA).**
- There is no server in v0.x, and the tool collects nothing.
- Examples use obviously synthetic names and checksum-invalid IDs, carry a FICTIONAL banner, and never name a real place together with an institution.
- Pre-commit runs a Thai national ID check with checksum, plus phone and email checks.
- A hosted service needs a DPIA and a named data controller first (K2).

**Security.**
- gitleaks runs in CI. Tags are signed and versions follow SemVer.
- Fund profiles and templates are data only, with no free-text "instructions" field, which blocks prompt injection.
- The docs state that the AI flags are advisory.

**Excluded from the public repo:**

| Item | Decision |
|---|---|
| Handoff package as-is (00, 01-06, README, MANIFEST.json) | never committed; derived only, with lineage |
| Source PDFs (NRCT FY2566 manual, บพข., บพค.) | excluded; `docs/sources.md` gives issuer, title, edition, sha256 and official URL (NEEDS_VERIFICATION) only; no author metadata |
| University lecture slides on writing a research proposal (issuer NEEDS_VERIFICATION) | excluded; a bibliographic citation at most |
| An excluded AI readout of NRIIS portal screenshots (a .txt file) and the screenshots behind it | excluded. It is an AI readout of three screenshots (txt:1-3), so INFERENCE. Its cost labels (06:518-544) ship only after K14 |
| The Toledo concept reference image | excluded. A redraw is possible (K8) without the photo, email or SDG icons, showing the direct human edge, and it goes through the gate |
| 03 §26 snapshot (UHC, RISE, EV2026_*) | only as RELAYED and dated in `ecosystem/…@2026-09` |
| Real fund IDs, rates and dates | only in dated profiles after verification |
| Proposals, profiles, `build/` | never public |

## I. Phased roadmap

**Phase 0: local scaffold, private remote.**
- *Deliverables:*
  - the tree skeleton and the commit-msg hook as commit #1;
  - governance, NOTICE, PRIVACY and SECURITY files;
  - `chain.yaml`, `status*.yaml`, `review_gates.yaml`, `roles.yaml`, `parity.yaml` (empty) and provenance;
  - `spec/mcp/tools.schema.json` as a contract only;
  - CI guards: no-AI-import, no-hardcoded-rules with the allowlist, leak, PII and attribution scans, reuse and schema lint;
  - `docs/sources.md` and `docs/deviations.md`.
- *Acceptance:* CI is green, and every guard fails on its seeded bad fixture. Founder answers are not required at this stage.

**v0.1: "Lecturer, no AI"** (01 §63 MVP + P3).
- *Deliverables:*
  - project, profile, fund and field schemas;
  - `fields.jsonl` re-keyed from 05 with `guidance{th,en}`;
  - `nriis-fields.jsonl`, `section_to_tab.yaml` and the one dated mapping, whose header states the one-form basis;
  - core ontology JSON-LD;
  - the v0.1 rules, each with one negative fixture;
  - the renderer;
  - the CLI subset, `webform/`, `forms/*.md` and `launchers/`;
  - the Thai Expert question set;
  - `FICTIONAL_CALL@0.1` (ACTIVE, `trust_level: FICTIONAL`);
  - `examples/lecturer-no-ai`;
  - the for-lecturers-no-ai docs in TH and EN.
- *Acceptance:*
  - **AT-2:** a non-CLI lecturer persona works through webform → launcher → validate → build with the AI extras absent, the network off and no keys. The result is a `submittable: true` (against the fictional profile), `real_world_verified: false` file with BLOCK = 0.
  - **AT-2b:** the same path via the CLI.
  - **AT-3a:** determinism, import-lint and a network-off run pass.
  - **AT-4:** every BLOCK rule has a failing fixture, and hypothesis arithmetic invariants hold.
  - **AT-5:** human and AI cold reads pass against a named checklist.
  - **AT-6:** the independent release gate passes before the tag.

**v0.2: "Citizen, no AI" + review + lock.**
- *Deliverables:*
  - Citizen Mode (TH and EN) and the English Expert question set;
  - the concept note and the HOLD path;
  - review records RG0-RG4, `lock` and `diff`;
  - the bridge ontology, with SHACL generated from `chain.yaml`;
  - `local_terms.yaml` seeded with human-curated, dated entries (curator per K16);
  - "own words + CONCEPT NEEDS_INPUT" as a non-blocking path;
  - the CH003, E, U, P, G, X and ECO rules, and the crosswalk;
  - the two citizen examples;
  - the for-citizens and for-administrators docs.
- *Acceptance:*
  - **AT-1 (letter §18), shipped material only:** starting from a written experience account, the result is either HOLD plus a concept note (no PI) or a submittable build (PI partner). It must have BLOCK = 0 apart from ELIG, pass CH001 and CH002, have every Gap and RQ human-authored (the citizen writes them with guidance cards), invent no evidence, mark every gap, and have no AI-authored field.
  - **AT-2 extended:** review → lock.

**v0.3: optional AI assist.**
- *Deliverables:* `grantthai[ai]`, the `citizen-ai-assisted` example, frontmatter disclosure, and the parity CI.
- *Acceptance:*
  - **AT-3b:** byte-identical build with and without the extra.
  - AI output is always PROPOSED or DRAFT, and X002 and X003 catch misuse.
  - Every AI feature has a tested human equivalent in `parity.yaml`.

**v0.4: interfaces.**
- *Deliverables:* MCP from the Phase-0 contract, optional REST/OpenAPI, and browser-assist (A1-A8).
- *Acceptance:* none of them can go above DRAFT or submit; UI drift sets UI_DRIFT; no credentials are stored.

**v0.5: real fund profiles, network, labels.**
- *Deliverables:*
  - the first real profile (K10), maintained by a human with a second checker;
  - the Thai label capture, dated and within the K14 terms;
  - opt-in network directories (K11).
- *Acceptance:* every rule is sourced, dated and second-checked, and the staleness job opens issues.

**Later.** Hosted UI (after a DPIA and a named controller, never the only source of truth), more NRIIS form mappings, a TypeScript package, the 45-node KG, and a Zenodo DOI after the gate (K12).

**Recorded deviations from the package:**
- MCP implementation moves from v0.1 (B:134, B:194) to v0.4; only the contract ships early.
- SHACL moves from v0.1 (01 §63) to v0.2 (K15).
- 01 §64 puts AI routing in v0.2; here it is v0.3, after the no-AI citizen path.
- `ai_assisted_fill` now defaults to false.
- The status names change as described in E.

## J. Risks and mitigations

| Risk | Mitigation |
|---|---|
| The one-form basis (05:1) is taken as general NRIIS truth | `observed_form` and date on every record; other forms NEEDS_VERIFICATION |
| AI becomes necessary in practice | P3; the non-CLI webform in v0.1; `parity.yaml` CI; AI mappings face the higher bar; README leads with the no-AI path |
| AI or requester acceptance looks like validation | ACCEPTED_BY_REQUESTER caps claims at CONTRIBUTORY and is listed in the readiness summary |
| Status overclaim | STRUCTURE_CHECKED/LOGIC_LINKED names; `AUTHOR_CHECKED` rendering; basis always shown |
| Experience laundered into evidence | `evidence_role`, X001, generated SHACL, claim downgrade |
| Ghost-writing for citizens | AI never writes Problem, Gap, RQ or Evidence text in Citizen Mode |
| Ineligible citizen proposal | partner gate, ELIG001, `submittable: false`, concept note |
| v0.1 too large to ship | scope held to 01 §63 + the lecturer no-AI path; everything else later |
| Fictional profile blocks every test | ACTIVE FICTIONAL profile; `submittable` vs `real_world_verified` split |
| Stale or poisoned fund rules | per-rule source and trust level, second human, staleness job |
| Implied endorsement | one NOTICE constant; disclaimer on body line 1; banned wording; K4 |
| Rights in core 01-06 or NRIIS labels | K13/K14 before public; lineage hashes; no CC0 on labels |
| PII, IP or PDF-metadata leaks | private workspace; `doctor`; export excludes PII by default; author-string denylist; fictional examples |
| Vendor attribution slips through the harness | hook before commit #1; history, PR and release scan; worker prompt rule |
| Repo goes public before the gate | create PRIVATE; visibility checked before and after |
| Duplicated kernel (03 Part II = 04) or schema drift | one `chain.yaml`; one `section_to_tab.yaml`; which package copy is canonical stays OPEN |
| Glossary or label errors | human-curated, dated; LABEL_TH marked NEEDS_VERIFICATION until captured |

## K. Decisions needed from the founder

The first five items block the first public push; no scaffolding work is blocked.

1. **K1 Philosophy sentence 2.** Keep it verbatim with the rider, or adopt the proposed neutral wording in A?
2. **K13 Core 01-06.** Who authored them, what is AI-drafted, and may derivatives be licensed as in H?
3. **K14 NRIIS screenshots and labels.** Whose account or form did the three screenshots show (real applicant data?), and have the NRIIS terms of use been checked? Labels will come from public TOR documents in the meantime.
4. **K7 Licences.** The Apache-2.0 / CC BY 4.0 / limited CC0 split, or copyleft? DCO or CLA?
5. **K4 Endorsement.** Has "GrantThai" been checked for trademark risk (NEEDS_VERIFICATION)? Keep the filename `NRIIS_SUBMISSION.md` and the phrase "NRIIS-ready", or use `SUBMISSION_DRAFT.md` with `target: NRIIS`?
6. **K3 Names.** Are `GrantThai`, `grantthai` and `GRANTTHAI_STANDALONE.md` final, retiring the OPEN_THAI_* and `thai-research` names?
7. **K2 Registration.** Local `init` or webform (default), or hosted accounts? If hosted, who operates it and who is the PDPA controller?
8. **K5 Citizen with no PI.** HOLD build plus concept note (default), or a mandatory PI partner?
9. **K6 Review independence.** Is self-review with disclosure and AUTHOR_CHECKED rendering enough for lock? May an outside expert set VERIFIED(independent)?
10. **K8 Poster.** Exclude it, or publish a redraw that meets the constraints in H?
11. **K9 Contact.** Which non-personal address goes in SECURITY.md and the Code of Conduct?
12. **K10 First real fund.** Which call comes first, who supplies the current document, and who is the second checker?
13. **K11 Directories.** Public opt-in expert and mentor directory, or schema only? Is `formation_log` only a personal trace, or a future credential?
14. **K12 Zenodo.** Should there be a DOI, `isPartOf` the Toledo hub, and under which author and ORCID?
15. **K15** Sign off on deferring SHACL from v0.1 (a deviation from 01 §63).
16. **K16** Who curates and dates the seed glossary (`local_terms.yaml`) for v0.2?

## L. Change log vs draft

**Critic parity**

| # | Finding | Decision | Where |
|---|---|---|---|
| 1 | reviewer ≠ proposer burdened humans more than AI | Applied. Mapping is only for the bridge; a human author self-accepts with disclosure | E |
| 2 | citizen acceptance of an AI mapping looked like validation | Applied. ACCEPTED_BY_REQUESTER caps claims at CONTRIBUTORY | E, F |
| 3 | empty glossary made AI necessary | Applied. Human-curated seed; own-words path; AT-1 uses shipped material only | I v0.2, K16 |
| 4 | AI as the headline | Applied. K1 blocks the public push; neutral wording proposed; "router" dropped | A, K |
| 5 | CLI/YAML-only registration | Applied. Offline webform and launchers in v0.1; AT-2 uses a non-CLI persona | B, D, I |
| 6 | SOURCE_/METHOD_CHECKED overclaimed | Applied. Renamed STRUCTURE_CHECKED and LOGIC_LINKED | E |
| 7 | role caps unverifiable; VERIFIED on self-review | Applied. Roles become UX defaults; status comes from gate records; basis rendered | B, E |
| 8 | citizen path depended on the network | Applied. A missing gate downgrades claims and adds a hold reason; it never blocks | E |
| 9 | `ai_assisted_fill` default | Applied. Default false | F |
| 10 | parity tested only on output bytes | Applied. `parity.yaml` plus CI | G |
| 11 | AI files placed first | Applied. README order fixed | D |
| 12 | `authored_by` could hide AI use | Applied. Marked self-declared in the disclaimer | E, F |
| 13 | diagrams drew AI as a hub | Partly applied. The bypass edge is required in every diagram and checked at the release gate, not by automated CI (INSTINCT: diagram parsing is not reliable) | C, H |

**Critic feasible**

| # | Finding | Decision | Where |
|---|---|---|---|
| 1 | v0.1 too large | Applied. v0.1 = 01 §63 + lecturer no-AI path; citizen features and AI moved later | I |
| 2 | fictional profile blocked every test | Applied. ACTIVE FICTIONAL profile; `submittable` vs `real_world_verified` | E, F |
| 3 | CI rule failed on the repo's own files | Applied. Path allowlist and unit-adjacent patterns | E |
| 4 | no Thai label source | Applied. `LABEL_TH: NEEDS_VERIFICATION`; capture in v0.5 | E, I |
| 5 | G0-G4 undefined and clashing with G rules | Applied. RG0-RG4 in `review_gates.yaml`; "named" records, not "signed" | E |
| 6 | AT-3 in v0.1 tested a package from v0.2 | Applied. Split into AT-3a and AT-3b | I |
| 7 | "coherent" had no measure | Applied. Concrete AT-1 criteria and a checklist | I |
| 8 | three validation engines | Applied. Two engines; SHACL generated; K15 | E |
| 9 | status overclaim | Applied (merged with parity 6); deviation documented | E |
| 10 | prompts/agents and MCP contract dropped | Applied. Contract in Phase 0; prompts and agents move to `assist` | D, G |
| 11 | AI reader demoted | Applied. Human and AI cold reads are equal checks | F |
| 12 | Phase 0 waited on the founder | Applied. Only the public push waits | I, K |
| 13 | eligibility thresholds in gate text | Applied. Gate text defers to the fund profile | B |
| 14 | section-to-tab drift | Applied. `section_to_tab.yaml` | D |

**Critic publish**

| # | Finding | Decision | Where |
|---|---|---|---|
| 1 | rights in core 01-06 unknown | Applied. K13 blocks public; lineage hashes; package never committed | H, K |
| 2 | labels from logged-in screenshots | Applied. K14; labels from public TOR documents; no screenshots or HAR files committed | E, H |
| 3 | "VERIFIED" overclaimed | Applied. AUTHOR_CHECKED rendering; public prose changed | E |
| 4 | disclaimer only in frontmatter; endorsement risk | Disclaimer on body line 1 and one agency list: applied. Filename rename: **rejected as the default**, because `NRIIS_SUBMISSION.md` is the founder's letter contract (§9); left to K4 | F, K |
| 5 | attribution guard too late | Applied. Hook before commit #1; history, PR and release scan; worker prompt rule | H |
| 6 | Core Epistemic Structure block missing | Applied. README footer and `lineage.md` | D, H |
| 7 | Toledo overclaim | Applied. "Conceptual framework, no equations or proofs" statement | H |
| 8 | public before the gate | Applied. Create PRIVATE, check with `gh api`, then flip | H |
| 9 | PDF author metadata | Applied. Denylist; `sources.md` without author fields | H |
| 10 | CC0 validity | Applied. CC0 only for facts restated in our own words; otherwise CC BY | H |
| 11 | AI flags only advisory | Applied. P11; docs say so | A, H |
| 12 | export default backwards | Applied. PII excluded by default | G |
| 13 | fictional names might match real people | Applied. Synthetic names, checksum-invalid IDs, banner | H |
| 14 | "signed" records | Applied. "Named review records" | E |
| 15 | SDG icons on the poster | Applied | H |
| 16 | NRCT in the scaffold vs the CI ban | Applied (merged with feasible 3) | E |

**Findings rejected outright:** none. Two were applied only in part: parity 13 (release-gate checklist, not CI) and publish 4 (filename rename left to K4).

**Other chair changes:**
- The version order is now AI-free Expert → AI-free Citizen → AI → interfaces → real funds. This follows from the founder amendment together with feasible 1.
- The draft's AT-1 for v0.1 moved to v0.2.