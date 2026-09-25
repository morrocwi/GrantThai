---
grantthai_version: 0.3.0
schema_version: 0.2.0-draft
renderer_version: nriis_submission.md.j2@0.3.0
project_id: FICTIONAL-DEMO-SEEDBANK-0001
project_content_sha256: 62896930208d5a390b8440d50774f7fd876b3eb34bc869fe630f70aeaf66fdaf
project_state_sha256: d58b3479418b59f9bc1963aa9afe7531adba98d879b68436611697bcc0537a09
project_locked: false
fund_profile: example/FICTIONAL_CALL@0.1
fund_profile_trust_level: FICTIONAL
nriis_mapping: nrct-master-hss@NEEDS_VERIFICATION
form_profile: ff_full_proposal@nriis-2570
authoring:
  mode: ai_assisted
  tools_disclosed:
  - AI assistant (simulated interview; demo only)
  self_declared: true
  ai_use_declaration: unconfirmed
submission_mode:
  human_copy_paste: true
  ai_assisted_fill: false
  direct_submit: false
human_final_approval_required: true
review:
  RG0:
    state: not_reviewed
    basis: no review record
  RG1:
    state: not_reviewed
    basis: no review record
  RG2:
    state: not_reviewed
    basis: no review record
  RG3:
    state: not_reviewed
    basis: no review record
  RG4:
    state: not_reviewed
    basis: no review record
submittable: true
real_world_verified: false
hold_reasons:
- 'RG0: no review record (claim strength downgraded; build is not blocked)'
- 'RG1: no review record (claim strength downgraded; build is not blocked)'
- 'RG2: no review record (claim strength downgraded; build is not blocked)'
- 'RG3: no review record (claim strength downgraded; build is not blocked)'
- 'RG4: no review record (claim strength downgraded; build is not blocked)'
stale_rules: []
accepted_by_requester_mappings: []
validation_summary:
  block: 0
  review: 3
  info: 31
disclaimer: GrantThai is an independent, unofficial project. It is NOT affiliated with, endorsed by, sponsored by, or officially connected to NRCT, TSRI, any PMU, or NRIIS. / GrantThai เป็นโครงการอิสระ ไม่เป็นทางการ และไม่ผูกพันกับ วช. สกสว. หน่วยบริหารจัดการทุน (PMU) ใด ๆ หรือระบบ NRIIS
---
GrantThai is an independent, unofficial project. It is NOT affiliated with, endorsed by, sponsored by, or officially connected to NRCT, TSRI, any PMU, or NRIIS. / GrantThai เป็นโครงการอิสระ ไม่เป็นทางการ และไม่ผูกพันกับ วช. สกสว. หน่วยบริหารจัดการทุน (PMU) ใด ๆ หรือระบบ NRIIS

> **FICTIONAL / สมมติ: bound to a fictional test call.** The fund profile `example/FICTIONAL_CALL@0.1` is not a real call. Nothing in this worksheet is submittable to any real fund; "submittable" below refers to the fictional test call only.

# NRIIS submission worksheet: FICTIONAL-DEMO-SEEDBANK-0001

This file is the researcher's own information, arranged for copy/paste into NRIIS by a person. GrantThai never submits anything. Every value below is exactly what `project.yaml` says; a missing value prints as `NEEDS_INPUT`, and any NRIIS label, tab name or order not confirmed from a public document prints as `NEEDS_VERIFICATION`. Validation findings are structural and logical checks only: they do not mean the content is true, sound or fundable.

## 1. Readiness summary

- Findings: BLOCK 0 / REVIEW 3 / INFO 31
- Submittable to a real call: n/a (fictional call). Against the fictional test profile `example/FICTIONAL_CALL@0.1` only: yes
- Hold reasons:
  - RG0: no review record (claim strength downgraded; build is not blocked)
  - RG1: no review record (claim strength downgraded; build is not blocked)
  - RG2: no review record (claim strength downgraded; build is not blocked)
  - RG3: no review record (claim strength downgraded; build is not blocked)
  - RG4: no review record (claim strength downgraded; build is not blocked)
- Open contradictions and conflicts: 10 (listed in section 4.4; none is resolved by GrantThai).
- Human final approval is always required before anything is entered into NRIIS.

### 1.1 BLOCK findings (fix before the project can be locked)
- None.

### 1.2 REVIEW findings (a person should look)
- **FW001** [CORE.NARRATIVE.THEORY, CORE.NARRATIVE.REFERENCES]: CORE.NARRATIVE.THEORY has content but CORE.NARRATIVE.REFERENCES is empty; 78 of 100 funded final reports carry a reference list (corpus-100 pattern FWP-06). Next step: List the works the theory and literature boxes draw on (CORE.NARRATIVE.REFERENCES), or record why there are none. Practice, not a fund rule.
- **AI001**: The AI Use Declaration is incomplete: human_verification is empty (GenAI guideline 2569 p.11-12, p.34). Next step: The researcher fills authoring.ai_use_declaration in project.yaml (tools with version, stages and purpose; influence_on_conclusions; human_verification; data_handling) and, after reading it, sets declaration_confirmed_by_human: true themselves. An AI never sets that flag.
- **AI001**: The AI Use Declaration is not confirmed by the researcher (declaration_confirmed_by_human is not true; GenAI guideline 2569 p.12 item 4: the user confirms the output was checked). Next step: The researcher fills authoring.ai_use_declaration in project.yaml (tools with version, stages and purpose; influence_on_conclusions; human_verification; data_handling) and, after reading it, sets declaration_confirmed_by_human: true themselves. An AI never sets that flag.

### 1.3 NEEDS_INPUT (required NRIIS fields with no value)
- None.
- Other records in project.yaml still NEEDS_INPUT: `CORE.ALIGNMENT.FUND_SELECTION`, `CORE.NARRATIVE.REFERENCES`, `CORE.NARRATIVE.IP_CHECK`, `FUND.CALL.KEY_RESULTS`, `CORE.PRIORKNOWLEDGE.PK2`

### 1.4 Markers
- Every NRIIS label (Thai), tab name, tab order and field order in section 2 is `NEEDS_VERIFICATION` (observed form `GENERAL > PROJECT > WORKPLAN > UTILIZATION > ATTACHMENTS`, not yet confirmed from a public call or TOR document). Next step: check each against the current call before entering it.
- `FUND.CALL.FISCAL_YEAR`: NEEDS_VERIFICATION. Next step: confirm this value against a current, cited source.
- `CORE.GENERAL.RESEARCH_ISSUE`: NEEDS_VERIFICATION. Next step: confirm this value against a current, cited source.
- `CORE.GENERAL.PLAN`: NEEDS_VERIFICATION. Next step: confirm this value against a current, cited source.
- `CORE.GENERAL.OECD.PRIMARY`: NEEDS_VERIFICATION. Next step: confirm this value against a current, cited source.
- `CORE.GENERAL.OECD.SECONDARY`: NEEDS_VERIFICATION. Next step: confirm this value against a current, cited source.
- `CORE.ALIGNMENT.FUND_SELECTION`: NEEDS_VERIFICATION. Next step: confirm this value against a current, cited source.
- `COMP.STANDARD.HUMAN`: NEEDS_VERIFICATION. Next step: confirm this value against a current, cited source.
- `FUND.CALL.KEY_RESULTS`: NEEDS_VERIFICATION. Next step: confirm this value against a current, cited source.

### 1.5 AI-drafted values (the researcher must confirm)
- `CORE.GENERAL.TITLE_EN`: authored_by is `human_ai_assisted`, an AI-assisted value the researcher adopted (DRAFT, not a source). Next step: read it and confirm it says what you mean; keep authored_by as human_ai_assisted unless you rewrite it yourself.
- `CORE.GENERAL.KEYWORDS_EN`: authored_by is `ai_draft`, an AI draft not yet adopted (DRAFT, not a source). Next step: rewrite it in your own words and set authored_by to human, or adopt it as it stands and set authored_by to human_ai_assisted.
- `CORE.NARRATIVE.SUMMARY`: authored_by is `ai_draft`, an AI draft not yet adopted (DRAFT, not a source). Next step: rewrite it in your own words and set authored_by to human, or adopt it as it stands and set authored_by to human_ai_assisted.
- `CORE.NARRATIVE.RATIONALE`: authored_by is `human_ai_assisted`, an AI-assisted value the researcher adopted (DRAFT, not a source). Next step: read it and confirm it says what you mean; keep authored_by as human_ai_assisted unless you rewrite it yourself.
- `CORE.NARRATIVE.METHOD`: authored_by is `human_ai_assisted`, an AI-assisted value the researcher adopted (DRAFT, not a source). Next step: read it and confirm it says what you mean; keep authored_by as human_ai_assisted unless you rewrite it yourself.
- `CORE.RESEARCH.GAP`: authored_by is `human_ai_assisted`, an AI-assisted value the researcher adopted (DRAFT, not a source). Next step: read it and confirm it says what you mean; keep authored_by as human_ai_assisted unless you rewrite it yourself.

### 1.6 Mappings and self-checked reviews
- None.

### 1.7 Rules not evaluated by this version (INFO)
- B003 not evaluated: budget-rate rules: spec/fund/fund-profile.schema.json has no rate slot yet, so no rate can be checked.
- B004 not evaluated: prohibited costs: spec/fund/fund-profile.schema.json has no prohibited-cost slot yet, so this rule cannot fire.
- F004 not evaluated: historical rule reuse needs rule lineage across profile versions, which v0.1 does not track (F003 still blocks a non-ACTIVE profile).
- CH003 not evaluated: ships v0.2; not yet implemented in this build.
- E001 not evaluated: ships v0.2; not yet implemented in this build.
- E002 not evaluated: ships v0.2; not yet implemented in this build.
- E003 not evaluated: ships v0.2; not yet implemented in this build.
- E004 not evaluated: ships v0.2; not yet implemented in this build.
- E005 not evaluated: ships v0.2; not yet implemented in this build.
- E006 not evaluated: ships v0.2; not yet implemented in this build.
- E007 not evaluated: ships v0.2; not yet implemented in this build.
- E008 not evaluated: ships v0.2; not yet implemented in this build.
- U001 not evaluated: ships v0.2; not yet implemented in this build.
- U002 not evaluated: ships v0.2; not yet implemented in this build.
- U003 not evaluated: ships v0.2; not yet implemented in this build.
- U004 not evaluated: ships v0.2; not yet implemented in this build.
- U005 not evaluated: ships v0.2; not yet implemented in this build.
- P001 not evaluated: ships v0.2; not yet implemented in this build.
- P002 not evaluated: ships v0.2; not yet implemented in this build.
- P003 not evaluated: ships v0.2; not yet implemented in this build.
- G001 not evaluated: ships v0.2; not yet implemented in this build.
- G002 not evaluated: ships v0.2; not yet implemented in this build.
- G003 not evaluated: ships v0.2; not yet implemented in this build.
- X001 not evaluated: ships v0.2; not yet implemented in this build.
- X002 not evaluated: ships v0.2; not yet implemented in this build.
- X004 not evaluated: ships v0.2; not yet implemented in this build.
- X005 not evaluated: ships v0.2; not yet implemented in this build.
- X006 not evaluated: ships v0.2; not yet implemented in this build.
- C001 not evaluated: ships v0.2; not yet implemented in this build.
- C002 not evaluated: ships v0.2; not yet implemented in this build.
- C003 not evaluated: ships v0.2; not yet implemented in this build.

### 1.8 Form profile `ff_full_proposal@nriis-2570` (NEEDS_VERIFICATION)
- The profile in force is itself NEEDS_VERIFICATION: check which fields and tabs it requires against the current public form before relying on it.
- Unmapped profile items (NEEDS_VERIFICATION): items the form asks for that GrantThai has no single field for.
  - SD-5 part 1: fund focus areas 1-6, at most 2 per project (p1): Focus areas 3-6 need at least one choice; 1-2 are cross-cutting and optional. GrantThai has no focus-area field; CORE.ALIGNMENT.FUND_SELECTION is the nearest free-text home. Nearest fields: `CORE.ALIGNMENT.FUND_SELECTION`.
  - SD-5 part 1: work being built on (only if focus area 6 is chosen) (p1): Prior result (at most 100 words), project name, owner, owner's affiliation, year, TRL/SRL of that work. GrantThai holds these in separate fields; the combined item has no single registry field. Nearest fields: `CORE.GENERAL.PAST_PERFORMANCE`, `READY.TRL.CURRENT`, `READY.SRL.CURRENT`.
- Candidate budget rules (listed, not evaluated): check them yourself against the current call.
  - B101-candidate (p9): Equipment at most 20 percent of the budget-receiving unit's research and innovation budget (a unit-level cap, not a per-project check).
  - B102-candidate (p9): No institutional overhead is supported.
  - B103-candidate (p9): Project total rounded to whole hundreds (currency units); line items broken down by multiplication, for the requested year only.

## 2. Copy/paste fields by NRIIS tab

Tab names, their order and the field order within each tab describe one observed form and are **NEEDS_VERIFICATION**. A Thai label marked "candidate" was read from a public document edition (docs/sources.md) and is also NEEDS_VERIFICATION: check it against the current call; it is never an official label.

### Tab 1: GENERAL (NEEDS_VERIFICATION); candidate part label (candidate, NEEDS_VERIFICATION): "1. ข้อมูลทั่วไป" (SD-1 p15)
#### GENERAL.1 Fiscal Year

LABEL_TH: NEEDS_VERIFICATION

```text
2570
```

- FIELD_ID: `FUND.CALL.FISCAL_YEAR` (NRIIS map: `NRIIS.GENERAL.FUND_CALL_FISCAL_YEAR`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=OFFICIAL_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record); markers: NEEDS_VERIFICATION
- REQUIRED: true
- INPUT_CONTROL: number
- DEPENDENCIES: none
- SOURCE_IDS: SRC-SD5, SRC-T01
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human (self-declared)

#### GENERAL.2 Funding Call Name

LABEL_TH: NEEDS_VERIFICATION

```text
GrantThai FICTIONAL test fund call
```

- FIELD_ID: `FUND.CALL.NAME` (NRIIS map: `NRIIS.GENERAL.FUND_CALL_NAME`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: true
- INPUT_CONTROL: text
- DEPENDENCIES: none
- SOURCE_IDS: SRC-FCALL, SRC-T01
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human (self-declared)

#### GENERAL.3 Funding Call Code

LABEL_TH: NEEDS_VERIFICATION

```text
(optional, not supplied)
```

- FIELD_ID: `FUND.CALL.CODE` (NRIIS map: `NRIIS.GENERAL.FUND_CALL_CODE`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: text
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### GENERAL.4 Funding Agency

LABEL_TH: NEEDS_VERIFICATION

```text
GrantThai project (not a real funding agency)
```

- FIELD_ID: `FUND.CALL.AGENCY` (NRIIS map: `NRIIS.GENERAL.FUND_CALL_AGENCY`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: true
- INPUT_CONTROL: text
- DEPENDENCIES: none
- SOURCE_IDS: SRC-FCALL, SRC-T01
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human (self-declared)

#### GENERAL.5 Application Open Datetime

LABEL_TH: NEEDS_VERIFICATION

```text
(optional, not supplied)
```

- FIELD_ID: `FUND.CALL.OPEN` (NRIIS map: `NRIIS.GENERAL.FUND_CALL_OPEN`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: datetime
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### GENERAL.6 Application Close Datetime

LABEL_TH: NEEDS_VERIFICATION

```text
(optional, not supplied)
```

- FIELD_ID: `FUND.CALL.CLOSE` (NRIIS map: `NRIIS.GENERAL.FUND_CALL_CLOSE`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: datetime
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### GENERAL.7 Program Code

LABEL_TH: NEEDS_VERIFICATION

```text
(optional, not supplied)
```

- FIELD_ID: `FUND.CALL.PROGRAM.CODE` (NRIIS map: `NRIIS.GENERAL.FUND_CALL_PROGRAM_CODE`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: text
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### GENERAL.8 Program Name

LABEL_TH: NEEDS_VERIFICATION

```text
(optional, not supplied)
```

- FIELD_ID: `FUND.CALL.PROGRAM.NAME` (NRIIS map: `NRIIS.GENERAL.FUND_CALL_PROGRAM_NAME`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: text
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### GENERAL.9 Main Plan Code

LABEL_TH: NEEDS_VERIFICATION

```text
(optional, not supplied)
```

- FIELD_ID: `FUND.CALL.PLAN.CODE` (NRIIS map: `NRIIS.GENERAL.FUND_CALL_PLAN_CODE`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: text
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### GENERAL.10 Main Plan Name

LABEL_TH: NEEDS_VERIFICATION

```text
(optional, not supplied)
```

- FIELD_ID: `FUND.CALL.PLAN.NAME` (NRIIS map: `NRIIS.GENERAL.FUND_CALL_PLAN_NAME`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: text
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### GENERAL.11 Sub-plan Name

LABEL_TH: NEEDS_VERIFICATION

```text
(optional, not supplied)
```

- FIELD_ID: `FUND.CALL.SUBPLAN` (NRIIS map: `NRIIS.GENERAL.FUND_CALL_SUBPLAN`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: text
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### GENERAL.12 Research Issue / Funding Topic

LABEL_TH: NEEDS_VERIFICATION

```text
จุดมุ่งเน้นที่ 4 งานวิจัยเพื่อการพัฒนาเชิงพื้นที่ (ตามที่ผู้วิจัยสมมติระบุจากแบบฟอร์ม)
```

- FIELD_ID: `CORE.GENERAL.RESEARCH_ISSUE` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_RESEARCH_ISSUE`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=OFFICIAL_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record); markers: NEEDS_VERIFICATION
- REQUIRED: true
- INPUT_CONTROL: select
- DEPENDENCIES: none
- SOURCE_IDS: SRC-SD5, SRC-T02
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human (self-declared)

#### GENERAL.13 Funding Plan

LABEL_TH: NEEDS_VERIFICATION

```text
จุดมุ่งเน้นที่ 4 งานวิจัยเพื่อการพัฒนาเชิงพื้นที่ (แผนที่หน่วยงานใช้ยื่น: ยังไม่ยืนยัน)
```

- FIELD_ID: `CORE.GENERAL.PLAN` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_PLAN`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=OFFICIAL_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record); markers: NEEDS_VERIFICATION
- REQUIRED: true
- INPUT_CONTROL: select
- DEPENDENCIES: FUND.CALL.PLAN.NAME
- SOURCE_IDS: SRC-SD5, SRC-T02
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human (self-declared)

#### GENERAL.14 Project Title (Thai)

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "ชื่อโครงการ" (SD-1 p15, item 1.1))

```text
เครือข่ายเรียนรู้ธนาคารเมล็ดพันธุ์ข้าวพื้นบ้านโดยชุมชน อำเภอสมมติ จังหวัดสมมติ ก
```

- FIELD_ID: `CORE.GENERAL.TITLE_TH` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_TITLE_TH`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: true
- INPUT_CONTROL: text
- DEPENDENCIES: none
- SOURCE_IDS: SRC-T03
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human (self-declared)

#### GENERAL.15 Project Title (English)

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "ชื่อโครงการ" (SD-1 p15, item 1.1))

```text
A community-led learning network of local rice seed banks in a fictional southern district
```

- FIELD_ID: `CORE.GENERAL.TITLE_EN` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_TITLE_EN`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: true
- INPUT_CONTROL: text
- DEPENDENCIES: none
- SOURCE_IDS: SRC-T03
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human_ai_assisted (self-declared)

#### GENERAL.16 Requested Budget

LABEL_TH: NEEDS_VERIFICATION

```text
480000
```

- FIELD_ID: `CORE.GENERAL.REQUESTED_BUDGET` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_REQUESTED_BUDGET`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DERIVED, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: true
- INPUT_CONTROL: number
- DEPENDENCIES: BUDGET.PLAN.TOTAL
- SOURCE_IDS: SRC-T17
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human (self-declared)
- ARITHMETIC CHECK: value 480000.00 vs sum of budget lines 480000.00: OK

#### GENERAL.17 Total Project Budget

LABEL_TH: NEEDS_VERIFICATION

```text
480000
```

- FIELD_ID: `CORE.GENERAL.TOTAL_BUDGET` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_TOTAL_BUDGET`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DERIVED, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: true
- INPUT_CONTROL: number
- DEPENDENCIES: BUDGET.PLAN.TOTAL
- SOURCE_IDS: SRC-T17
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human (self-declared)
- ARITHMETIC CHECK: value 480000.00 vs sum of budget lines 480000.00: OK

#### GENERAL.18 Research Type

LABEL_TH: NEEDS_VERIFICATION

```text
(optional, not supplied)
```

- FIELD_ID: `CORE.GENERAL.RESEARCH_TYPE` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_RESEARCH_TYPE`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: select
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### GENERAL.19 National Strategic/Flagship Project Submission

LABEL_TH: NEEDS_VERIFICATION

```text
(optional, not supplied)
```

- FIELD_ID: `CORE.GENERAL.FLAGSHIP` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_FLAGSHIP`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: checkbox
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### GENERAL.20 Most Relevant Sub-master Plan

LABEL_TH: NEEDS_VERIFICATION

```text
(optional, not supplied)
```

- FIELD_ID: `CORE.GENERAL.MASTER_PLAN` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_MASTER_PLAN`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: select_or_text
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### GENERAL.21 Project Characteristic

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "ลักษณะโครงการ" (SD-1 p15, item 1.3))

```text
(optional, not supplied)
```

- FIELD_ID: `CORE.GENERAL.CHARACTERISTIC` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_CHARACTERISTIC`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: select
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- CONFLICTS: CX-05 (OPEN; see section 4.4)
- AUTHORED_BY: none (no record)

#### GENERAL.22 Contractual Commitment

LABEL_TH: NEEDS_VERIFICATION

```text
(optional, not supplied)
```

- FIELD_ID: `CORE.GENERAL.CONTRACT` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_CONTRACT`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: checkbox_or_text
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### GENERAL.23 Duration - Years

LABEL_TH: NEEDS_VERIFICATION

```text
1
```

- FIELD_ID: `CORE.GENERAL.DURATION_Y` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_DURATION_Y`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: true
- INPUT_CONTROL: number
- DEPENDENCIES: none
- SOURCE_IDS: SRC-T03
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human (self-declared)

#### GENERAL.24 Duration - Additional Months

LABEL_TH: NEEDS_VERIFICATION

```text
0
```

- FIELD_ID: `CORE.GENERAL.DURATION_M` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_DURATION_M`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: true
- INPUT_CONTROL: number
- DEPENDENCIES: none
- SOURCE_IDS: SRC-T03
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human (self-declared)

#### GENERAL.25 Submitted to Other Funders

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "โครงการยื่นเสนอขอรับทุนจากหน่วยงานอื่น" (SD-1 p15, item 1.4))

```text
false
```

- FIELD_ID: `CORE.GENERAL.OTHER_FUNDER` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_OTHER_FUNDER`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: true
- INPUT_CONTROL: checkbox
- DEPENDENCIES: none
- SOURCE_IDS: SRC-T03
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human (self-declared)

#### GENERAL.26 Other Funding Agency

LABEL_TH: NEEDS_VERIFICATION

```text
(optional, not supplied)
```

- FIELD_ID: `CORE.GENERAL.OTHER_FUNDER.AGENCY` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_OTHER_FUNDER_AGENCY`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: text
- DEPENDENCIES: CORE.GENERAL.OTHER_FUNDER=true
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### GENERAL.27 Other Submitted Project Title

LABEL_TH: NEEDS_VERIFICATION

```text
(optional, not supplied)
```

- FIELD_ID: `CORE.GENERAL.OTHER_FUNDER.TITLE` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_OTHER_FUNDER_TITLE`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: text
- DEPENDENCIES: CORE.GENERAL.OTHER_FUNDER=true
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### GENERAL.28 Difference from This Proposal

LABEL_TH: NEEDS_VERIFICATION

```text
(optional, not supplied)
```

- FIELD_ID: `CORE.GENERAL.OTHER_FUNDER.DIFF` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_OTHER_FUNDER_DIFF`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: textarea
- DEPENDENCIES: CORE.GENERAL.OTHER_FUNDER=true
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### GENERAL.29 Keywords (Thai)

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "คำสำคัญ (Keywords)" (SD-1 p15, item 1.5))

```text
ธนาคารเมล็ดพันธุ์ชุมชน
ข้าวพื้นบ้าน
การวิจัยเชิงปฏิบัติการแบบมีส่วนร่วม
เครือข่ายเรียนรู้
```

- FIELD_ID: `CORE.GENERAL.KEYWORDS_TH` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_KEYWORDS_TH`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: true
- INPUT_CONTROL: repeating_text
- DEPENDENCIES: none
- SOURCE_IDS: SRC-T04
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human (self-declared)

#### GENERAL.30 Keywords (English)

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "คำสำคัญ (Keywords)" (SD-1 p15, item 1.5))

```text
community seed bank
local rice varieties
participatory action research
learning network
```

- FIELD_ID: `CORE.GENERAL.KEYWORDS_EN` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_KEYWORDS_EN`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=INFERENCE, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: true
- INPUT_CONTROL: repeating_text
- DEPENDENCIES: none
- SOURCE_IDS: SRC-T04
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: ai_draft (self-declared)

#### GENERAL.31 OECD Primary Research Field

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "สาขาการวิจัยหลัก/ย่อย OECD" (SD-1 p15, item 1.6))

```text
6
```

- FIELD_ID: `CORE.GENERAL.OECD.PRIMARY` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_OECD_PRIMARY`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record); markers: NEEDS_VERIFICATION
- REQUIRED: true
- INPUT_CONTROL: select
- DEPENDENCIES: none
- SOURCE_IDS: SRC-T04
- VALIDATION: no BLOCK/REVIEW finding
- CONFLICTS: CX-10 (OPEN; see section 4.4)
- AUTHORED_BY: human (self-declared)

#### GENERAL.32 OECD Secondary Research Field

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "สาขาการวิจัยหลัก/ย่อย OECD" (SD-1 p15, item 1.6))

```text
6.4
```

- FIELD_ID: `CORE.GENERAL.OECD.SECONDARY` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_OECD_SECONDARY`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record); markers: NEEDS_VERIFICATION
- REQUIRED: true
- INPUT_CONTROL: select
- DEPENDENCIES: none
- SOURCE_IDS: SRC-T04
- VALIDATION: no BLOCK/REVIEW finding
- CONFLICTS: CX-10 (OPEN; see section 4.4)
- AUTHORED_BY: human (self-declared)

#### GENERAL.33 Related Research Field

LABEL_TH: NEEDS_VERIFICATION

```text
(optional, not supplied)
```

- FIELD_ID: `CORE.GENERAL.OECD.RELATED` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_OECD_RELATED`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: select_or_text
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### GENERAL.34 Programme Name (if this project belongs to a programme)

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "ชื่อชุดโครงการ" (SD-4 p40, item 1.5))

```text
(optional, not supplied)
```

- FIELD_ID: `CORE.GENERAL.PROGRAMME_NAME` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_PROGRAMME_NAME`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: text
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### GENERAL.35 Sub-projects under this Project

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "ชื่อโครงการย่อยภายใต้โครงการ (ถ้ามี)" (SD-1 p15, item 1.2))

```text
(optional, not supplied)
```

- FIELD_ID: `CORE.GENERAL.SUBPROJECTS` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_SUBPROJECTS`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: repeating_group
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### GENERAL.36 Past Performance (continuing project)

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "ผลการดำเนินที่ผ่านมา (กรณีที่เป็นโครงการต่อเนื่อง)" (SD-1 p15, item 1.3))

```text
(optional, not supplied)
```

- FIELD_ID: `CORE.GENERAL.PAST_PERFORMANCE` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_PAST_PERFORMANCE`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: repeating_group
- DEPENDENCIES: CORE.GENERAL.CHARACTERISTIC=Continuing Project
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- CONFLICTS: CX-05 (OPEN; see section 4.4)
- AUTHORED_BY: none (no record)

#### GENERAL.37 ISCED Broad Field

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "ISCED Broad field" (SD-1 p15, item 1.7))

```text
(optional, not supplied)
```

- FIELD_ID: `CORE.GENERAL.ISCED.BROAD` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_ISCED_BROAD`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: select
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### GENERAL.38 ISCED Narrow Field

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "ISCED Narrow field" (SD-1 p15, item 1.7))

```text
(optional, not supplied)
```

- FIELD_ID: `CORE.GENERAL.ISCED.NARROW` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_ISCED_NARROW`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: select
- DEPENDENCIES: CORE.GENERAL.ISCED.BROAD
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### GENERAL.39 ISCED Detailed Field

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "ISCED Detailed field" (SD-1 p15, item 1.7))

```text
(optional, not supplied)
```

- FIELD_ID: `CORE.GENERAL.ISCED.DETAILED` (NRIIS map: `NRIIS.GENERAL.CORE_GENERAL_ISCED_DETAILED`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: select
- DEPENDENCIES: CORE.GENERAL.ISCED.NARROW
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### GENERAL.40 One-sentence Alignment Statement

LABEL_TH: NEEDS_VERIFICATION

```text
(optional, not supplied)
```

- FIELD_ID: `CORE.ALIGNMENT.STATEMENT` (NRIIS map: `NRIIS.GENERAL.CORE_ALIGNMENT_STATEMENT`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: text
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### GENERAL.41 Selected Fund Objectives and Key Results

LABEL_TH: NEEDS_VERIFICATION

```text
(optional, not supplied)
```

- FIELD_ID: `CORE.ALIGNMENT.FUND_SELECTION` (NRIIS map: `NRIIS.GENERAL.CORE_ALIGNMENT_FUND_SELECTION`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: EMPTY (basis: no value in project.yaml (optional)); markers: NEEDS_VERIFICATION
- REQUIRED: false
- INPUT_CONTROL: group
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human (self-declared)

#### GENERAL.42 Research Team Members

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "รายละเอียดของคณะผู้วิจัย" (SD-1 p15, item 1.8))

| id | full_name | organization | project_role | contribution_percent | registration_status | orcid | responsibilities | eligibility_facts |
|---|---|---|---|---|---|---|---|---|
| TM1 | นักวิจัยสมมติ ก. (FICTIONAL) | มหาวิทยาลัยสมมติ (FICTIONAL) | PI | 50 | NEEDS_VERIFICATION |  | ออกแบบการวิจัย, วิเคราะห์ข้อมูล, เขียนรายงาน |  |
| TM2 | นักวิจัยสมมติ ข. (FICTIONAL) | มหาวิทยาลัยสมมติ (FICTIONAL) | CO_RESEARCHER | 30 | NEEDS_VERIFICATION |  | ทดสอบความงอก, ดูแลธนาคารเมล็ดพันธุ์ด้านเทคนิค |  |
| TM3 | ผู้ร่วมวิจัยชุมชนสมมติ ค. (FICTIONAL) | บ้านสมมติหนึ่ง (FICTIONAL) | OTHER | 7 | NEEDS_VERIFICATION |  | ผู้ร่วมวิจัยชุมชน, ประสานครัวเรือน, จดบันทึกเวที |  |
| TM4 | ผู้ร่วมวิจัยชุมชนสมมติ ง. (FICTIONAL) | บ้านสมมติสอง (FICTIONAL) | OTHER | 7 | NEEDS_VERIFICATION |  | ผู้ร่วมวิจัยชุมชน, ประสานครัวเรือน |  |
| TM5 | ผู้ร่วมวิจัยชุมชนสมมติ จ. (FICTIONAL) | บ้านสมมติสาม (FICTIONAL) | OTHER | 6 | NEEDS_VERIFICATION |  | ผู้ร่วมวิจัยชุมชน, ประสานครัวเรือน |  |

- FIELD_ID: `PROFILE.TEAM.MEMBERS` (NRIIS map: `NRIIS.GENERAL.PROFILE_TEAM_MEMBERS`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: true
- INPUT_CONTROL: repeating_group
- DEPENDENCIES: none
- SOURCE_IDS: SRC-T14
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human (self-declared)
- ARITHMETIC CHECK: sum(contribution_percent) = 100.00 (must be 100.00): OK

#### GENERAL.43 Team Expertise and Other Ongoing Projects

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "ความชำนาญ/ความสนใจพิเศษ/ความรับผิดชอบต่อแผนงาน/โครงการ อื่นๆ ที่อยู่ระหว่างดำเนินการ" (SD-1 p15, item 1.8))

```text
(optional, not supplied)
```

- FIELD_ID: `PROFILE.TEAM.EXPERTISE` (NRIIS map: `NRIIS.GENERAL.PROFILE_TEAM_EXPERTISE`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: repeating_group
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

### Tab 2: PROJECT (NEEDS_VERIFICATION); candidate part label (candidate, NEEDS_VERIFICATION): "2. ข้อมูลโครงการวิจัย" (SD-1 p16)
#### PROJECT.1 Proposal Summary

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "บทสรุปข้อเสนอการวิจัยและนวัตกรรม" (SD-1 p16, item 2.1))

```text
(ร่างโดย AI ผู้วิจัยสมมติยังไม่ยืนยัน) โครงการหนึ่งปีนี้ใช้การวิจัยเชิงปฏิบัติการแบบมีส่วนร่วมสามวงกับครัวเรือนชาวนาและผู้ร่วมวิจัยชุมชนในสามหมู่บ้านของอำเภอสมมติ เพื่อสำรวจพันธุ์ข้าวพื้นบ้านที่เหลืออยู่ ออกแบบและทดลองกติกาธนาคารเมล็ดพันธุ์ที่ชุมชนตั้งเอง และเชื่อมธนาคารทั้งสามเป็นเครือข่ายเรียนรู้ ผลผลิตคือทะเบียนพันธุ์ กติกาสามชุด คู่มือ และข้อเสนอเชิงนโยบายถึงเจ้าหน้าที่ส่งเสริมการเกษตรของอำเภอ
```

- FIELD_ID: `CORE.NARRATIVE.SUMMARY` (NRIIS map: `NRIIS.PROJECT.CORE_NARRATIVE_SUMMARY`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=INFERENCE, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- RENDER_FROM: CORE.RESEARCH.NATIONAL_NEED, CORE.RESEARCH.PROBLEM, CORE.RESEARCH.GAP, CORE.RESEARCH.OBJECTIVES, METHOD.PLAN.DESIGN, RESULTS.CHAIN.OUTPUTS (write this box from these records; GrantThai does not compose it)
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: true
- INPUT_CONTROL: textarea
- DEPENDENCIES: CORE.RESEARCH.NATIONAL_NEED, CORE.RESEARCH.PROBLEM, CORE.RESEARCH.GAP, CORE.RESEARCH.OBJECTIVES, METHOD.PLAN.DESIGN, RESULTS.CHAIN.OUTPUTS
- SOURCE_IDS: SRC-T20
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: ai_draft (self-declared)

#### PROJECT.2 Rationale / Problem / Research Question

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "หลักการและเหตุผล" (SD-1 p16, item 2.2))

```text
ชาวนารายย่อยในอำเภอสมมติต้องซื้อเมล็ดพันธุ์ทุกฤดูและพันธุ์พื้นบ้านค่อย ๆ หายไป (สมมติ) ในสามหมู่บ้านครัวเรือนเก็บเมล็ดกันเองโดยไม่มีกติกากลางและเมล็ดงอกไม่ดี งานแลกเปลี่ยนที่เคยจัดครั้งเดียวไม่มีผู้ดูแลต่อ ยังไม่มีกติกาที่ชุมชนออกแบบเองสำหรับธนาคารเมล็ดพันธุ์ที่เชื่อมกันเป็นเครือข่าย โครงการนี้จึงถามว่าธนาคารแบบนี้ช่วยให้ครัวเรือนเข้าถึงเมล็ดพันธุ์ที่งอกดีได้หรือไม่ ภายใต้เงื่อนไขใด
```

- FIELD_ID: `CORE.NARRATIVE.RATIONALE` (NRIIS map: `NRIIS.PROJECT.CORE_NARRATIVE_RATIONALE`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DERIVED, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- RENDER_FROM: CORE.RESEARCH.NATIONAL_NEED, CORE.RESEARCH.PROBLEM, CORE.RESEARCH.GAP, CORE.RESEARCH.RQ.PRIMARY (write this box from these records; GrantThai does not compose it)
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: true
- INPUT_CONTROL: textarea
- DEPENDENCIES: CORE.RESEARCH.NATIONAL_NEED, CORE.RESEARCH.PROBLEM, CORE.RESEARCH.GAP, CORE.RESEARCH.RQ.PRIMARY
- SOURCE_IDS: SRC-T20
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human_ai_assisted (self-declared)

#### PROJECT.3 Objectives

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "วัตถุประสงค์" (SD-1 p16, item 2.3))

```text
1) สำรวจพันธุ์ข้าวพื้นบ้านและความรู้การเก็บเมล็ดพันธุ์ในสามหมู่บ้าน 2) ออกแบบและทดลองกติกาธนาคารเมล็ดพันธุ์ร่วมกับผู้ร่วมวิจัยชุมชน 3) สร้างเครือข่ายเรียนรู้ข้ามหมู่บ้านและคู่มือ
```

- FIELD_ID: `CORE.NARRATIVE.OBJECTIVES` (NRIIS map: `NRIIS.PROJECT.CORE_NARRATIVE_OBJECTIVES`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- RENDER_FROM: CORE.RESEARCH.OBJECTIVES (write this box from these records; GrantThai does not compose it)
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: true
- INPUT_CONTROL: textarea
- DEPENDENCIES: CORE.RESEARCH.OBJECTIVES
- SOURCE_IDS: SRC-T10
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human (self-declared)

#### PROJECT.4 Research / Development Framework

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "กรอบการวิจัย" (SD-1 p16, item 2.4))

```text
กติกาที่ชุมชนตั้งเอง ทำให้การยืม-คืนเมล็ดพันธุ์คาดการณ์ได้ ทำให้พันธุ์พื้นบ้านถูกปลูกซ้ำทุกฤดู
```

- FIELD_ID: `CORE.NARRATIVE.FRAMEWORK` (NRIIS map: `NRIIS.PROJECT.CORE_NARRATIVE_FRAMEWORK`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- RENDER_FROM: CORE.RESEARCH.CONSTRUCTS, CORE.RESEARCH.RELATIONSHIPS, CORE.RESEARCH.BOUNDARY_CONDITIONS, METHOD.PLAN.INTERVENTION (write this box from these records; GrantThai does not compose it)
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: true
- INPUT_CONTROL: textarea
- DEPENDENCIES: CORE.RESEARCH.CONSTRUCTS, CORE.RESEARCH.RELATIONSHIPS
- SOURCE_IDS: SRC-T20
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human (self-declared)

#### PROJECT.5 Concepts, Theories, Hypotheses / Innovation and Feasibility

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "แนวคิด ทฤษฎี และสมมติฐานงานวิจัย" (SD-1 p16, item 2.5))

```text
แนวคิดการจัดการทรัพยากรร่วมและทุนทางสังคม ตามความเข้าใจของผู้วิจัยสมมติ (ยังไม่ได้ใส่อ้างอิง)
```

- FIELD_ID: `CORE.NARRATIVE.THEORY` (NRIIS map: `NRIIS.PROJECT.CORE_NARRATIVE_THEORY`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- RENDER_FROM: CORE.RESEARCH.THEORETICAL_FOUNDATIONS, CORE.RESEARCH.CONSTRUCTS, CORE.RESEARCH.HYPOTHESES, CORE.RESEARCH.PROPOSITIONS, CORE.RESEARCH.INNOVATION, CORE.RESEARCH.FEASIBILITY (write this box from these records; GrantThai does not compose it)
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: true
- INPUT_CONTROL: textarea
- DEPENDENCIES: CORE.RESEARCH.CONSTRUCTS, CORE.RESEARCH.HYPOTHESES, CORE.RESEARCH.INNOVATION, CORE.RESEARCH.FEASIBILITY
- SOURCE_IDS: SRC-T20
- VALIDATION: FW001 REVIEW
- AUTHORED_BY: human (self-declared)

#### PROJECT.6 Research Methodology and Procedures

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "ระเบียบวิธีวิจัยและวิธีการดำเนินการวิจัย" (SD-1 p16, item 2.6))

```text
การวิจัยเชิงปฏิบัติการแบบมีส่วนร่วมสามวง (วางแผน ลงมือ สังเกต สะท้อนคิด) ในสามหมู่บ้าน วงที่ 1 สำรวจพันธุ์และความรู้ด้วยทะเบียนพันธุ์และสัมภาษณ์กึ่งโครงสร้าง วงที่ 2 ออกแบบกติกา ตั้งธนาคาร และทดสอบความงอก วงที่ 3 เวทีสะท้อนคิดและงานแลกเปลี่ยนข้ามหมู่บ้าน กลุ่มผู้ร่วมคือครัวเรือนทำนาที่สมัครใจประมาณ 60 ครัวเรือนและผู้อาวุโสประมาณ 15 คน วิเคราะห์เชิงประเด็นร่วมกับร้อยละการงอกและจำนวนการยืม-คืน ขอความยินยอมด้วยวาจาต่อหน้าพยานสำหรับผู้อ่านหนังสือไม่คล่อง และยื่นกรรมการจริยธรรมก่อนลงพื้นที่
```

- FIELD_ID: `CORE.NARRATIVE.METHOD` (NRIIS map: `NRIIS.PROJECT.CORE_NARRATIVE_METHOD`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DERIVED, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- RENDER_FROM: METHOD.PLAN.DESIGN, METHOD.PLAN.POPULATION, METHOD.PLAN.SAMPLE, METHOD.PLAN.RECRUITMENT, METHOD.PLAN.INTERVENTION, METHOD.PLAN.INSTRUMENTS, METHOD.PLAN.DATA_COLLECTION, METHOD.PLAN.ANALYSIS, METHOD.PLAN.QUALITY, METHOD.PLAN.ETHICS (write this box from these records; GrantThai does not compose it)
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: true
- INPUT_CONTROL: textarea
- DEPENDENCIES: METHOD.PLAN.DESIGN, METHOD.PLAN.POPULATION, METHOD.PLAN.SAMPLE, METHOD.PLAN.INSTRUMENTS, METHOD.PLAN.DATA_COLLECTION, METHOD.PLAN.ANALYSIS, METHOD.PLAN.ETHICS
- SOURCE_IDS: SRC-T20
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human_ai_assisted (self-declared)

#### PROJECT.7 References

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "เอกสาร/งานวิจัยอ้างอิงทางวิชาการเกี่ยวกับโครงการ" (SD-1 p16, item 2.7))

```text
(optional, not supplied)
```

- FIELD_ID: `CORE.NARRATIVE.REFERENCES` (NRIIS map: `NRIIS.PROJECT.CORE_NARRATIVE_REFERENCES`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: repeating_textarea
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: FW001 REVIEW
- AUTHORED_BY: human (self-declared)

#### PROJECT.8 Related Intellectual Property Check

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "การตรวจสอบทรัพย์สินทางปัญญาที่เกี่ยวข้อง" (SD-1 p16, item 2.8))

```text
(optional, not supplied)
```

- FIELD_ID: `CORE.NARRATIVE.IP_CHECK` (NRIIS map: `NRIIS.PROJECT.CORE_NARRATIVE_IP_CHECK`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: group
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human (self-declared)

### Tab 3: WORKPLAN (NEEDS_VERIFICATION); candidate part label (candidate, NEEDS_VERIFICATION): "3. ข้อมูลแผนงาน" (SD-1 p16-17)
#### WORKPLAN.1 Implementation Activities

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "แผนการดำเนินงานวิจัย" (SD-1 p16, item 3.1))

| id | year | name | months | weight_percent | objective_ids | method_ids | output_ids | budget_item_ids | depends_on_activity_ids | responsible_person_ids | deliverables |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ACT1 | 1 | เตรียมงาน ขอรับรองจริยธรรม ตั้งทีมผู้ร่วมวิจัยชุมชน | 1, 2 | 15 | OBJ1 | MP1 |  | BI4 |  | TM1 |  |
| ACT2 | 1 | สำรวจพันธุ์ข้าวพื้นบ้านและความรู้การเก็บเมล็ด | 2, 3, 4, 5, 6 | 30 | OBJ1 | MP1 |  | BI1, BI2, BI4 | ACT1 | TM1, TM3, TM4, TM5 |  |
| ACT3 | 1 | ตั้งและทดลองธนาคารเมล็ดพันธุ์ ทดสอบความงอก | 5, 6, 7, 8, 9, 10 | 35 | OBJ2 | MP2 | OUT1, OUT2 | BI1, BI2, BI3, BI4 | ACT2 | TM2 |  |
| ACT4 | 1 | เวทีสะท้อนคิด งานแลกเปลี่ยนเครือข่าย จัดทำคู่มือและรายงาน | 10, 11, 12 | 20 | OBJ3 | MP3 | OUT3, OUT4 | BI5, BI6 | ACT3 | TM1 |  |

- FIELD_ID: `WORK.PLAN.ACTIVITIES` (NRIIS map: `NRIIS.WORKPLAN.WORK_PLAN_ACTIVITIES`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: true
- INPUT_CONTROL: repeating_group
- DEPENDENCIES: none
- SOURCE_IDS: SRC-T15
- VALIDATION: no BLOCK/REVIEW finding
- CONFLICTS: CX-03 (OPEN; see section 4.4)
- AUTHORED_BY: human (self-declared)
- ARITHMETIC CHECK: sum(weight_percent) = 100.00 (must be 100.00): OK

#### WORKPLAN.2 Project Risks and Mitigation

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "ความเสี่ยงของโครงการ" (SD-1 p17, item 3.10))

| id | risk | risk_type | likelihood | impact | mitigation | activity_ids |
|---|---|---|---|---|---|---|
| RSK1 | น้ำท่วมช่วงปลายปีทำให้ลงพื้นที่ไม่ได้ | project delivery | medium | high | จัดเวทีสำคัญก่อนเดือนที่ 10 และให้ผู้ร่วมวิจัยชุมชนเก็บข้อมูลต่อได้ | ACT3, ACT4 |
| RSK2 | ครัวเรือนยืมเมล็ดแล้วไม่คืน | project delivery | medium | medium | ให้ชุมชนตั้งกติกาการคืนเองและทบทวนในเวที | ACT3 |
| RSK3 | ความรู้ของผู้อาวุโสถูกนำไปใช้โดยไม่ให้เครดิต | social and intellectual property | low | high | ขอความยินยอมเรื่องการเผยแพร่และระบุเครดิตตามที่เจ้าของความรู้ต้องการ | ACT2, ACT4 |

- FIELD_ID: `WORK.PLAN.RISKS` (NRIIS map: `NRIIS.WORKPLAN.WORK_PLAN_RISKS`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: false
- INPUT_CONTROL: repeating_group
- DEPENDENCIES: none
- SOURCE_IDS: SRC-T16
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human (self-declared)

#### WORKPLAN.3 Research / Implementation Sites

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "พื้นที่ทำวิจัย" (SD-1 p16, item 3.3))

| id | location_type | country | province | place_name | site_role | activity_ids |
|---|---|---|---|---|---|---|
| SITE1 | village | FICTIONAL country | จังหวัดสมมติ ก | บ้านสมมติหนึ่ง | เก็บข้อมูล ธนาคารเมล็ดพันธุ์ | ACT2, ACT3 |
| SITE2 | village | FICTIONAL country | จังหวัดสมมติ ก | บ้านสมมติสอง | เก็บข้อมูล ธนาคารเมล็ดพันธุ์ | ACT2, ACT3 |
| SITE3 | village | FICTIONAL country | จังหวัดสมมติ ก | บ้านสมมติสาม | เก็บข้อมูล ธนาคารเมล็ดพันธุ์ งานแลกเปลี่ยน | ACT2, ACT3, ACT4 |

- FIELD_ID: `GEO.AREA.RESEARCH_SITES` (NRIIS map: `NRIIS.WORKPLAN.GEO_AREA_RESEARCH_SITES`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: true
- INPUT_CONTROL: repeating_group
- DEPENDENCIES: none
- SOURCE_IDS: SRC-T15
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human (self-declared)

#### WORKPLAN.4 Benefit Areas

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "พื้นที่ที่ได้รับประโยชน์จากการวิจัย" (SD-1 p16, item 3.4))

```text
(optional, not supplied)
```

- FIELD_ID: `GEO.AREA.BENEFIT_AREAS` (NRIIS map: `NRIIS.WORKPLAN.GEO_AREA_BENEFIT_AREAS`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: repeating_group
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### WORKPLAN.5 Research User Organizations

LABEL_TH: NEEDS_VERIFICATION

```text
(optional, not supplied)
```

- FIELD_ID: `GEO.AREA.RESEARCH_USERS` (NRIIS map: `NRIIS.WORKPLAN.GEO_AREA_RESEARCH_USERS`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: repeating_group
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### WORKPLAN.6 Budget by Project Year

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "แผนการใช้จ่ายงบประมาณของโครงการวิจัย" (SD-1 p17, item 3.5))

| id | year | planned_total |
|---|---|---|
| BY1 | 1 | 480000 |

- FIELD_ID: `BUDGET.PLAN.YEARS` (NRIIS map: `NRIIS.WORKPLAN.BUDGET_PLAN_YEARS`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: true
- INPUT_CONTROL: repeating_group
- DEPENDENCIES: none
- SOURCE_IDS: SRC-T17
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human (self-declared)

#### WORKPLAN.7 Budget Line Items

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "แผนการใช้จ่ายงบประมาณของโครงการวิจัย" (SD-1 p17, item 3.5))

| id | year | budget_type | category | subcategory | item_label | description | quantity | unit | persons_or_items | times_or_months | unit_price | line_total | activity_ids | objective_ids | justification |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BI1 | 1 | ค่าจ้าง (ตามที่ผู้วิจัยสมมติจัดหมวด) | ค่าจ้าง |  | ผู้ช่วยวิจัยภาคสนาม | ผู้ช่วยวิจัยภาคสนาม 1 คน 10 เดือน | 1 | คน-เดือน | 1 | 10 | 12000 | 120000 | ACT2, ACT3 |  | เก็บข้อมูลและประสานสามหมู่บ้าน |
| BI2 | 1 | ค่าใช้สอย | ค่าใช้สอย |  | เวทีชุมชน | เวทีชุมชน 3 หมู่บ้าน 4 ครั้ง | 1 | ครั้ง | 3 | 4 | 15000 | 180000 | ACT2, ACT3 |  | วง PAR ต้องมีเวทีวางแผนและสะท้อนคิด |
| BI3 | 1 | ค่าวัสดุ | ค่าวัสดุ |  | วัสดุทดสอบความงอก | ชุดวัสดุทดสอบความงอก 3 หมู่บ้าน | 1 | ชุด | 3 | 1 | 20000 | 60000 | ACT3 |  | ทดสอบเมล็ดก่อนให้ยืม |
| BI4 | 1 | ค่าใช้สอย | ค่าใช้สอย |  | ค่าเดินทางลงพื้นที่ | นักวิจัย 2 คน 12 เดือน | 1 | คน-เดือน | 2 | 12 | 2500 | 60000 | ACT1, ACT2, ACT3 |  | ลงพื้นที่สามหมู่บ้านทุกเดือน |
| BI5 | 1 | ค่าใช้สอย | ค่าใช้สอย |  | พิมพ์คู่มือ | คู่มือธนาคารเมล็ดพันธุ์ 300 เล่ม | 1 | เล่ม | 300 | 1 | 100 | 30000 | ACT4 |  | แจกครัวเรือนและเครือข่าย |
| BI6 | 1 | ค่าใช้สอย | ค่าใช้สอย |  | งานแลกเปลี่ยนเครือข่าย | งานแลกเปลี่ยนข้ามหมู่บ้าน 1 ครั้ง | 1 | ครั้ง | 1 | 1 | 30000 | 30000 | ACT4 |  | เชื่อมสามธนาคารเป็นเครือข่าย |

- FIELD_ID: `BUDGET.PLAN.ITEMS` (NRIIS map: `NRIIS.WORKPLAN.BUDGET_PLAN_ITEMS`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: true
- INPUT_CONTROL: repeating_group
- DEPENDENCIES: none
- SOURCE_IDS: SRC-T17
- VALIDATION: no BLOCK/REVIEW finding
- CONFLICTS: CX-03 (OPEN; see section 4.4)
- AUTHORED_BY: human (self-declared)
- ARITHMETIC CHECK: BI1: 1 x 1 x 10 x 12000 = 120000.00; line_total 120000.00: OK; BI2: 1 x 3 x 4 x 15000 = 180000.00; line_total 180000.00: OK; BI3: 1 x 3 x 1 x 20000 = 60000.00; line_total 60000.00: OK; BI4: 1 x 2 x 12 x 2500 = 60000.00; line_total 60000.00: OK; BI5: 1 x 300 x 1 x 100 = 30000.00; line_total 30000.00: OK; BI6: 1 x 1 x 1 x 30000 = 30000.00; line_total 30000.00: OK; sum(line_total) = 480000.00

#### WORKPLAN.8 Equipment Procurement Details

LABEL_TH: NEEDS_VERIFICATION

```text
(optional, not supplied)
```

- FIELD_ID: `BUDGET.PLAN.EQUIPMENT` (NRIIS map: `NRIIS.WORKPLAN.BUDGET_PLAN_EQUIPMENT`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: repeating_group
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### WORKPLAN.9 Research Ethics

LABEL_TH: NEEDS_VERIFICATION

```text
(optional, not supplied)
```

- FIELD_ID: `COMP.STANDARD.RESEARCH_ETHICS` (NRIIS map: `NRIIS.WORKPLAN.COMP_STANDARD_RESEARCH_ETHICS`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: group
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### WORKPLAN.10 Human Research Standard

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "มาตรฐานการวิจัย: มีการวิจัยในมนุษย์" (SD-1 p17, item 3.6))

| key | value |
|---|---|
| applicable | true |
| status | จะยื่นก่อนลงพื้นที่ |
| committee | (สมมติ) คณะกรรมการจริยธรรมการวิจัยในมนุษย์ของมหาวิทยาลัยสมมติ |
| protocol_number |  |
| approval_date |  |
| attachment_ids | ATT1 |

- FIELD_ID: `COMP.STANDARD.HUMAN` (NRIIS map: `NRIIS.WORKPLAN.COMP_STANDARD_HUMAN`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record); markers: NEEDS_VERIFICATION
- REQUIRED: false
- INPUT_CONTROL: group
- DEPENDENCIES: none
- SOURCE_IDS: SRC-T13
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human (self-declared)

#### WORKPLAN.11 Biosafety Standard

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "มาตรฐานการวิจัย: มีการวิจัยที่เกี่ยวข้องกับงานด้านเทคโนโลยีชีวภาพสมัยใหม่" (SD-1 p17, item 3.6))

```text
(optional, not supplied)
```

- FIELD_ID: `COMP.STANDARD.BIOSAFETY` (NRIIS map: `NRIIS.WORKPLAN.COMP_STANDARD_BIOSAFETY`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: group
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### WORKPLAN.12 Animal Research Standard

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "มาตรฐานการวิจัย: มีการใช้สัตว์ทดลอง" (SD-1 p17, item 3.6))

```text
(optional, not supplied)
```

- FIELD_ID: `COMP.STANDARD.ANIMAL` (NRIIS map: `NRIIS.WORKPLAN.COMP_STANDARD_ANIMAL`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: group
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### WORKPLAN.13 Chemical Laboratory Safety Standard

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "มาตรฐานการวิจัย: มีการใช้ห้องปฏิบัติการที่เกี่ยวกับสารเคมี" (SD-1 p17, item 3.6))

```text
(optional, not supplied)
```

- FIELD_ID: `COMP.STANDARD.CHEMICAL` (NRIIS map: `NRIIS.WORKPLAN.COMP_STANDARD_CHEMICAL`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: group
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### WORKPLAN.14 Collaborating Organizations / Private Sector / Communities

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "หน่วยงานร่วมดำเนินการ/ภาคเอกชนหรือชุมชนที่ร่วมลงทุนหรือดำเนินการ" (SD-1 p17, item 3.7))

| id | organization_name | organization_type | year | collaboration_role | activity_ids | in_cash | in_kind | total_contribution | support_attachment_ids | in_kind_basis |
|---|---|---|---|---|---|---|---|---|---|---|
| PTN1 | (สมมติ) กลุ่มเกษตรกรทำนาอำเภอสมมติ | community group | 1 | ร่วมวิจัยและให้ใช้ศาลาเป็นที่ประชุมและที่เก็บเมล็ด | ACT2, ACT3, ACT4 |  |  |  |  | ใช้ศาลาโดยไม่คิดค่าใช้จ่าย ตามที่ผู้วิจัยสมมติแจ้ง ไม่ได้ประเมินมูลค่า |

- FIELD_ID: `WORK.PARTNERS.ORGANIZATIONS` (NRIIS map: `NRIIS.WORKPLAN.WORK_PARTNERS_ORGANIZATIONS`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: false
- INPUT_CONTROL: repeating_group
- DEPENDENCIES: none
- SOURCE_IDS: SRC-T14
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human (self-declared)

#### WORKPLAN.15 Current Technology Readiness Level

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "ระดับความพร้อมทางเทคโนโลยี (Technology Readiness Level: TRL)" (SD-1 p17, item 3.8.1))

```text
(optional, not supplied)
```

- FIELD_ID: `READY.TRL.CURRENT` (NRIIS map: `NRIIS.WORKPLAN.READY_TRL_CURRENT`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: group
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### WORKPLAN.16 Target Technology Readiness Level at Project End

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "ระดับความพร้อมทางเทคโนโลยี (Technology Readiness Level: TRL)" (SD-1 p17, item 3.8.1))

```text
(optional, not supplied)
```

- FIELD_ID: `READY.TRL.TARGET` (NRIIS map: `NRIIS.WORKPLAN.READY_TRL_TARGET`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: group
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### WORKPLAN.17 Current Societal Readiness Level

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "ระดับความพร้อมทางสังคม (Societal Readiness Level: SRL)" (SD-1 p17, item 3.8.2))

```text
(optional, not supplied)
```

- FIELD_ID: `READY.SRL.CURRENT` (NRIIS map: `NRIIS.WORKPLAN.READY_SRL_CURRENT`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: group
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### WORKPLAN.18 Target Societal Readiness Level at Project End

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "ระดับความพร้อมทางสังคม (Societal Readiness Level: SRL)" (SD-1 p17, item 3.8.2))

```text
(optional, not supplied)
```

- FIELD_ID: `READY.SRL.TARGET` (NRIIS map: `NRIIS.WORKPLAN.READY_SRL_TARGET`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: group
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

### Tab 4: UTILIZATION (NEEDS_VERIFICATION); candidate part label (candidate, NEEDS_VERIFICATION): "5. ผลผลิต/ผลลัพธ์/ผลกระทบ" (SD-1 p18)
#### UTILIZATION.1 Connections with Experts

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "การเชื่อมโยงกับนักวิจัยที่เป็นผู้เชี่ยวชาญในสาขาวิชาที่ทำการวิจัยทั้งในและต่างประเทศ (ถ้ามี)" (SD-1 p17, item 3.9.1))

```text
(optional, not supplied)
```

- FIELD_ID: `RESULTS.PATHWAY.EXPERTS` (NRIIS map: `NRIIS.UTILIZATION.RESULTS_PATHWAY_EXPERTS`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: textarea_or_group
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- CONFLICTS: CX-07 (OPEN; see section 4.4)
- AUTHORED_BY: none (no record)

#### UTILIZATION.2 Stakeholder and User Engagement

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "การเชื่อมโยงหรือความร่วมมือกับผู้มีส่วนได้ส่วนเสีย และผู้ใช้ประโยชน์จากงานวิจัย (Stakeholder and User Engagement)" (SD-1 p17, item 3.9.2))

```text
(optional, not supplied)
```

- FIELD_ID: `RESULTS.PATHWAY.STAKEHOLDERS` (NRIIS map: `NRIIS.UTILIZATION.RESULTS_PATHWAY_STAKEHOLDERS`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- RENDER_FROM: RESULTS.PATHWAY.SUSTAINABILITY (write this box from these records; GrantThai does not compose it)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: textarea_or_group
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- CONFLICTS: CX-07 (OPEN; see section 4.4)
- AUTHORED_BY: none (no record)

#### UTILIZATION.3 Primary Utilization Domain

LABEL_TH: NEEDS_VERIFICATION

```text
(optional, not supplied)
```

- FIELD_ID: `RESULTS.CHAIN.UTILIZATION_DOMAIN` (NRIIS map: `NRIIS.UTILIZATION.RESULTS_CHAIN_UTILIZATION_DOMAIN`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: select
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### UTILIZATION.4 Utilization Description

LABEL_TH: NEEDS_VERIFICATION

```text
(optional, not supplied)
```

- FIELD_ID: `RESULTS.CHAIN.UTILIZATION_DESC` (NRIIS map: `NRIIS.UTILIZATION.RESULTS_CHAIN_UTILIZATION_DESC`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: textarea
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### UTILIZATION.5 Benefit Summary

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "ประโยชน์ที่คาดว่าจะได้รับ" (SD-1 p18, item 5.1))

```text
(optional, not supplied)
```

- FIELD_ID: `RESULTS.CHAIN.BENEFIT_SUMMARY` (NRIIS map: `NRIIS.UTILIZATION.RESULTS_CHAIN_BENEFIT_SUMMARY`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: textarea
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: none (no record)

#### UTILIZATION.6 Users of R&I Outputs

LABEL_TH: NEEDS_VERIFICATION

| id | user_group | user_group_name | target_number | unit | intended_use | output_ids |
|---|---|---|---|---|---|---|
| USR1 | community organisation | (สมมติ) คณะกรรมการธนาคารเมล็ดพันธุ์สามหมู่บ้าน | 3 | คณะกรรมการ | ใช้กติกาและคู่มือดูแลธนาคารเมล็ดพันธุ์ | OUT2, OUT3 |
| USR2 | government agency | (สมมติ) เจ้าหน้าที่ส่งเสริมการเกษตรของอำเภอสมมติ | 1 | หน่วยงาน | พิจารณาข้อเสนอเชิงนโยบาย | OUT4 |

- FIELD_ID: `RESULTS.CHAIN.USERS` (NRIIS map: `NRIIS.UTILIZATION.RESULTS_CHAIN_USERS`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: false
- INPUT_CONTROL: repeating_group
- DEPENDENCIES: none
- SOURCE_IDS: SRC-T18
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human (self-declared)

#### UTILIZATION.7 Beneficiaries

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "ผู้ที่จะได้ประโยชน์จากโครงการ" (SD-1 p18, item 5.2))

| id | beneficiary_group | benefit_description | target_number | unit | outcome_ids |
|---|---|---|---|---|---|
| BEN1 | (สมมติ) ครัวเรือนชาวนาในสามหมู่บ้าน | เข้าถึงเมล็ดพันธุ์ข้าวพื้นบ้านโดยไม่ต้องซื้อ | 60 | ครัวเรือน | OC1 |

- FIELD_ID: `RESULTS.CHAIN.BENEFICIARIES` (NRIIS map: `NRIIS.UTILIZATION.RESULTS_CHAIN_BENEFICIARIES`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: false
- INPUT_CONTROL: repeating_group
- DEPENDENCIES: none
- SOURCE_IDS: SRC-T18
- VALIDATION: no BLOCK/REVIEW finding
- CONFLICTS: CX-04 (OPEN; see section 4.4)
- AUTHORED_BY: human (self-declared)

#### UTILIZATION.8 Expected Outputs

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "ผลผลิตที่คาดว่าจะได้รับ (Output)" (SD-1 p18, item 5.3))

| id | output_type | quantity | unit | description | objective_ids | activity_ids | user_ids | kr_ids | kr_role |
|---|---|---|---|---|---|---|---|---|---|
| OUT1 | NEEDS_VERIFICATION (form's 10 output types): knowledge record | 1 | ชุด | ทะเบียนพันธุ์ข้าวพื้นบ้านและความรู้การเก็บเมล็ดพันธุ์ | OBJ1 | ACT3 |  |  |  |
| OUT2 | NEEDS_VERIFICATION (form's 10 output types): community rules | 3 | ชุดกติกา | กติกาธนาคารเมล็ดพันธุ์ของสามหมู่บ้าน | OBJ2 | ACT3 |  |  |  |
| OUT3 | NEEDS_VERIFICATION (form's 10 output types): handbook | 1 | เล่ม | คู่มือธนาคารเมล็ดพันธุ์ชุมชน | OBJ3 | ACT4 |  |  |  |
| OUT4 | NEEDS_VERIFICATION (form's 10 output types): policy proposal | 1 | ฉบับ | ข้อเสนอเชิงนโยบายถึงสำนักงานเกษตรของอำเภอสมมติ | OBJ3 | ACT4 |  |  |  |

- FIELD_ID: `RESULTS.CHAIN.OUTPUTS` (NRIIS map: `NRIIS.UTILIZATION.RESULTS_CHAIN_OUTPUTS`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: true
- INPUT_CONTROL: repeating_group
- DEPENDENCIES: none
- SOURCE_IDS: SRC-T18
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human (self-declared)

#### UTILIZATION.9 Process from Outputs to Expected Outcomes

LABEL_TH: NEEDS_VERIFICATION

| id | output_ids | process | quantity | unit | brief_description | user_ids |
|---|---|---|---|---|---|---|
| PW1 | OUT2, OUT3 | คณะกรรมการใช้กติกาและคู่มือในการให้ยืมและรับคืนเมล็ดพันธุ์ฤดูถัดไป |  |  |  | USR1 |
| PW2 | OUT4 | ผู้วิจัยนำเสนอข้อเสนอต่อเจ้าหน้าที่ส่งเสริมการเกษตรของอำเภอ |  |  |  | USR2 |

- FIELD_ID: `RESULTS.CHAIN.OUTCOME_PROCESS` (NRIIS map: `NRIIS.UTILIZATION.RESULTS_CHAIN_OUTCOME_PROCESS`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: false
- INPUT_CONTROL: repeating_group
- DEPENDENCIES: none
- SOURCE_IDS: SRC-T18
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human (self-declared)

#### UTILIZATION.10 Expected Outcomes

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "ผลลัพธ์ (Expected Outcomes) ที่เกิดจากการนำผลงานไปใช้ประโยชน์ของผู้ใช้ (users)" (SD-1 p18, item 5.4))

| id | expected_change | indicator | baseline | target | measurement_period | pathway_ids | outcome_type | kr_ids |
|---|---|---|---|---|---|---|---|---|
| OC1 | ครัวเรือนยืมและคืนเมล็ดพันธุ์ตามกติกาในฤดูถัดไป | จำนวนครัวเรือนที่ยืมและคืนตามกติกา |  |  |  | PW1 | behavioral outcome |  |

- FIELD_ID: `RESULTS.CHAIN.OUTCOMES` (NRIIS map: `NRIIS.UTILIZATION.RESULTS_CHAIN_OUTCOMES`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: false
- INPUT_CONTROL: repeating_group
- DEPENDENCIES: none
- SOURCE_IDS: SRC-T18
- VALIDATION: no BLOCK/REVIEW finding
- CONFLICTS: CX-08 (OPEN; see section 4.4)
- AUTHORED_BY: human (self-declared)

#### UTILIZATION.11 Expected Impacts

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "ผลกระทบ (Expected Impacts)" (SD-1 p18, item 5.5))

| id | expected_impact | impact_description | outcome_ids | kr_ids | impact_type | claim_strength | sign | directness | intended |
|---|---|---|---|---|---|---|---|---|---|
| IMP1 | ช่วยรักษาพันธุ์ข้าวพื้นบ้านของอำเภอสมมติ | ผลระยะยาวที่โครงการนี้มีส่วนช่วย ไม่ใช่ผลของโครงการนี้อย่างเดียว | OC1 |  | environmental and social | CONTRIBUTORY | POSITIVE | INDIRECT | true |

- FIELD_ID: `RESULTS.CHAIN.IMPACTS` (NRIIS map: `NRIIS.UTILIZATION.RESULTS_CHAIN_IMPACTS`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: false
- INPUT_CONTROL: repeating_group
- DEPENDENCIES: none
- SOURCE_IDS: SRC-T18
- VALIDATION: no BLOCK/REVIEW finding
- CONFLICTS: CX-04 (OPEN; see section 4.4)
- AUTHORED_BY: human (self-declared)

#### UTILIZATION.12 Entrepreneur Information (startup / spin-off, if any)

LABEL_TH: NEEDS_VERIFICATION (candidate, NEEDS_VERIFICATION: "ข้อมูลผู้ประกอบการ (ถ้ามี)" (SD-1 p18, item 4))

```text
(optional, not supplied)
```

- FIELD_ID: `RESULTS.ENTREPRENEUR.PROFILE` (NRIIS map: `NRIIS.UTILIZATION.RESULTS_ENTREPRENEUR_PROFILE`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: none (no record)
- STATUS: EMPTY (basis: no value in project.yaml (optional))
- REQUIRED: false
- INPUT_CONTROL: group
- DEPENDENCIES: none
- SOURCE_IDS: none
- VALIDATION: no BLOCK/REVIEW finding
- CONFLICTS: CX-09 (OPEN; see section 4.4)
- AUTHORED_BY: none (no record)

### Tab 5: ATTACHMENTS (NEEDS_VERIFICATION); candidate part label (candidate, NEEDS_VERIFICATION): "ส่วนที่ 5 : เอกสารแนบ" (SD-4 p164)
#### ATTACHMENTS.1 Attached Documents

LABEL_TH: NEEDS_VERIFICATION

| id | file_name | document_type | file_type | related_section | required_status | supplied | version |
|---|---|---|---|---|---|---|---|
| ATT1 | ethics-approval.pdf | เอกสารรับรองจริยธรรม (ยังไม่มี) | pdf | Standards | UNKNOWN | false |  |

- FIELD_ID: `DOC.ATTACHMENTS.DOCUMENTS` (NRIIS map: `NRIIS.ATTACHMENTS.DOC_ATTACHMENTS_DOCUMENTS`)
- ORIGIN: NRIIS_NATIVE
- PROVENANCE: provenance_class=DECISION, source_type=PROJECT_DOCUMENT, evidence_role=ORIENTING
- STATUS: DRAFT (basis: as authored; report-only validation, no review record)
- REQUIRED: false
- INPUT_CONTROL: repeating_group
- DEPENDENCIES: none
- SOURCE_IDS: SRC-T13
- VALIDATION: no BLOCK/REVIEW finding
- AUTHORED_BY: human (self-declared)

## 3. Machine field metadata

```yaml
- nriis_field_id: NRIIS.GENERAL.FUND_CALL_FISCAL_YEAR
  field_id: FUND.CALL.FISCAL_YEAR
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 1
  required: true
  status: DRAFT
  markers:
  - NEEDS_VERIFICATION
  source_ids:
  - SRC-SD5
  - SRC-T01
  authored_by: human
- nriis_field_id: NRIIS.GENERAL.FUND_CALL_NAME
  field_id: FUND.CALL.NAME
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 2
  required: true
  status: DRAFT
  markers: []
  source_ids:
  - SRC-FCALL
  - SRC-T01
  authored_by: human
- nriis_field_id: NRIIS.GENERAL.FUND_CALL_CODE
  field_id: FUND.CALL.CODE
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 3
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.GENERAL.FUND_CALL_AGENCY
  field_id: FUND.CALL.AGENCY
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 4
  required: true
  status: DRAFT
  markers: []
  source_ids:
  - SRC-FCALL
  - SRC-T01
  authored_by: human
- nriis_field_id: NRIIS.GENERAL.FUND_CALL_OPEN
  field_id: FUND.CALL.OPEN
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 5
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.GENERAL.FUND_CALL_CLOSE
  field_id: FUND.CALL.CLOSE
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 6
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.GENERAL.FUND_CALL_PROGRAM_CODE
  field_id: FUND.CALL.PROGRAM.CODE
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 7
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.GENERAL.FUND_CALL_PROGRAM_NAME
  field_id: FUND.CALL.PROGRAM.NAME
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 8
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.GENERAL.FUND_CALL_PLAN_CODE
  field_id: FUND.CALL.PLAN.CODE
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 9
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.GENERAL.FUND_CALL_PLAN_NAME
  field_id: FUND.CALL.PLAN.NAME
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 10
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.GENERAL.FUND_CALL_SUBPLAN
  field_id: FUND.CALL.SUBPLAN
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 11
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_RESEARCH_ISSUE
  field_id: CORE.GENERAL.RESEARCH_ISSUE
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 12
  required: true
  status: DRAFT
  markers:
  - NEEDS_VERIFICATION
  source_ids:
  - SRC-SD5
  - SRC-T02
  authored_by: human
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_PLAN
  field_id: CORE.GENERAL.PLAN
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 13
  required: true
  status: DRAFT
  markers:
  - NEEDS_VERIFICATION
  source_ids:
  - SRC-SD5
  - SRC-T02
  authored_by: human
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_TITLE_TH
  field_id: CORE.GENERAL.TITLE_TH
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 14
  required: true
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T03
  authored_by: human
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_TITLE_EN
  field_id: CORE.GENERAL.TITLE_EN
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 15
  required: true
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T03
  authored_by: human_ai_assisted
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_REQUESTED_BUDGET
  field_id: CORE.GENERAL.REQUESTED_BUDGET
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 16
  required: true
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T17
  authored_by: human
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_TOTAL_BUDGET
  field_id: CORE.GENERAL.TOTAL_BUDGET
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 17
  required: true
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T17
  authored_by: human
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_RESEARCH_TYPE
  field_id: CORE.GENERAL.RESEARCH_TYPE
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 18
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_FLAGSHIP
  field_id: CORE.GENERAL.FLAGSHIP
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 19
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_MASTER_PLAN
  field_id: CORE.GENERAL.MASTER_PLAN
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 20
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_CHARACTERISTIC
  field_id: CORE.GENERAL.CHARACTERISTIC
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 21
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_CONTRACT
  field_id: CORE.GENERAL.CONTRACT
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 22
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_DURATION_Y
  field_id: CORE.GENERAL.DURATION_Y
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 23
  required: true
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T03
  authored_by: human
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_DURATION_M
  field_id: CORE.GENERAL.DURATION_M
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 24
  required: true
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T03
  authored_by: human
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_OTHER_FUNDER
  field_id: CORE.GENERAL.OTHER_FUNDER
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 25
  required: true
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T03
  authored_by: human
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_OTHER_FUNDER_AGENCY
  field_id: CORE.GENERAL.OTHER_FUNDER.AGENCY
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 26
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_OTHER_FUNDER_TITLE
  field_id: CORE.GENERAL.OTHER_FUNDER.TITLE
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 27
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_OTHER_FUNDER_DIFF
  field_id: CORE.GENERAL.OTHER_FUNDER.DIFF
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 28
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_KEYWORDS_TH
  field_id: CORE.GENERAL.KEYWORDS_TH
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 29
  required: true
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T04
  authored_by: human
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_KEYWORDS_EN
  field_id: CORE.GENERAL.KEYWORDS_EN
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 30
  required: true
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T04
  authored_by: ai_draft
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_OECD_PRIMARY
  field_id: CORE.GENERAL.OECD.PRIMARY
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 31
  required: true
  status: DRAFT
  markers:
  - NEEDS_VERIFICATION
  source_ids:
  - SRC-T04
  authored_by: human
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_OECD_SECONDARY
  field_id: CORE.GENERAL.OECD.SECONDARY
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 32
  required: true
  status: DRAFT
  markers:
  - NEEDS_VERIFICATION
  source_ids:
  - SRC-T04
  authored_by: human
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_OECD_RELATED
  field_id: CORE.GENERAL.OECD.RELATED
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 33
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_PROGRAMME_NAME
  field_id: CORE.GENERAL.PROGRAMME_NAME
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 34
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_SUBPROJECTS
  field_id: CORE.GENERAL.SUBPROJECTS
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 35
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_PAST_PERFORMANCE
  field_id: CORE.GENERAL.PAST_PERFORMANCE
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 36
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_ISCED_BROAD
  field_id: CORE.GENERAL.ISCED.BROAD
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 37
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_ISCED_NARROW
  field_id: CORE.GENERAL.ISCED.NARROW
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 38
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.GENERAL.CORE_GENERAL_ISCED_DETAILED
  field_id: CORE.GENERAL.ISCED.DETAILED
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 39
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.GENERAL.CORE_ALIGNMENT_STATEMENT
  field_id: CORE.ALIGNMENT.STATEMENT
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 40
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.GENERAL.CORE_ALIGNMENT_FUND_SELECTION
  field_id: CORE.ALIGNMENT.FUND_SELECTION
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 41
  required: false
  status: EMPTY
  markers:
  - NEEDS_VERIFICATION
  source_ids: []
  authored_by: human
- nriis_field_id: NRIIS.GENERAL.PROFILE_TEAM_MEMBERS
  field_id: PROFILE.TEAM.MEMBERS
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 42
  required: true
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T14
  authored_by: human
- nriis_field_id: NRIIS.GENERAL.PROFILE_TEAM_EXPERTISE
  field_id: PROFILE.TEAM.EXPERTISE
  origin: NRIIS_NATIVE
  tab: GENERAL
  entry_order: 43
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.PROJECT.CORE_NARRATIVE_SUMMARY
  field_id: CORE.NARRATIVE.SUMMARY
  origin: NRIIS_NATIVE
  tab: PROJECT
  entry_order: 1
  required: true
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T20
  authored_by: ai_draft
- nriis_field_id: NRIIS.PROJECT.CORE_NARRATIVE_RATIONALE
  field_id: CORE.NARRATIVE.RATIONALE
  origin: NRIIS_NATIVE
  tab: PROJECT
  entry_order: 2
  required: true
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T20
  authored_by: human_ai_assisted
- nriis_field_id: NRIIS.PROJECT.CORE_NARRATIVE_OBJECTIVES
  field_id: CORE.NARRATIVE.OBJECTIVES
  origin: NRIIS_NATIVE
  tab: PROJECT
  entry_order: 3
  required: true
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T10
  authored_by: human
- nriis_field_id: NRIIS.PROJECT.CORE_NARRATIVE_FRAMEWORK
  field_id: CORE.NARRATIVE.FRAMEWORK
  origin: NRIIS_NATIVE
  tab: PROJECT
  entry_order: 4
  required: true
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T20
  authored_by: human
- nriis_field_id: NRIIS.PROJECT.CORE_NARRATIVE_THEORY
  field_id: CORE.NARRATIVE.THEORY
  origin: NRIIS_NATIVE
  tab: PROJECT
  entry_order: 5
  required: true
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T20
  authored_by: human
- nriis_field_id: NRIIS.PROJECT.CORE_NARRATIVE_METHOD
  field_id: CORE.NARRATIVE.METHOD
  origin: NRIIS_NATIVE
  tab: PROJECT
  entry_order: 6
  required: true
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T20
  authored_by: human_ai_assisted
- nriis_field_id: NRIIS.PROJECT.CORE_NARRATIVE_REFERENCES
  field_id: CORE.NARRATIVE.REFERENCES
  origin: NRIIS_NATIVE
  tab: PROJECT
  entry_order: 7
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: human
- nriis_field_id: NRIIS.PROJECT.CORE_NARRATIVE_IP_CHECK
  field_id: CORE.NARRATIVE.IP_CHECK
  origin: NRIIS_NATIVE
  tab: PROJECT
  entry_order: 8
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: human
- nriis_field_id: NRIIS.WORKPLAN.WORK_PLAN_ACTIVITIES
  field_id: WORK.PLAN.ACTIVITIES
  origin: NRIIS_NATIVE
  tab: WORKPLAN
  entry_order: 1
  required: true
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T15
  authored_by: human
- nriis_field_id: NRIIS.WORKPLAN.WORK_PLAN_RISKS
  field_id: WORK.PLAN.RISKS
  origin: NRIIS_NATIVE
  tab: WORKPLAN
  entry_order: 2
  required: false
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T16
  authored_by: human
- nriis_field_id: NRIIS.WORKPLAN.GEO_AREA_RESEARCH_SITES
  field_id: GEO.AREA.RESEARCH_SITES
  origin: NRIIS_NATIVE
  tab: WORKPLAN
  entry_order: 3
  required: true
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T15
  authored_by: human
- nriis_field_id: NRIIS.WORKPLAN.GEO_AREA_BENEFIT_AREAS
  field_id: GEO.AREA.BENEFIT_AREAS
  origin: NRIIS_NATIVE
  tab: WORKPLAN
  entry_order: 4
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.WORKPLAN.GEO_AREA_RESEARCH_USERS
  field_id: GEO.AREA.RESEARCH_USERS
  origin: NRIIS_NATIVE
  tab: WORKPLAN
  entry_order: 5
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.WORKPLAN.BUDGET_PLAN_YEARS
  field_id: BUDGET.PLAN.YEARS
  origin: NRIIS_NATIVE
  tab: WORKPLAN
  entry_order: 6
  required: true
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T17
  authored_by: human
- nriis_field_id: NRIIS.WORKPLAN.BUDGET_PLAN_ITEMS
  field_id: BUDGET.PLAN.ITEMS
  origin: NRIIS_NATIVE
  tab: WORKPLAN
  entry_order: 7
  required: true
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T17
  authored_by: human
- nriis_field_id: NRIIS.WORKPLAN.BUDGET_PLAN_EQUIPMENT
  field_id: BUDGET.PLAN.EQUIPMENT
  origin: NRIIS_NATIVE
  tab: WORKPLAN
  entry_order: 8
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.WORKPLAN.COMP_STANDARD_RESEARCH_ETHICS
  field_id: COMP.STANDARD.RESEARCH_ETHICS
  origin: NRIIS_NATIVE
  tab: WORKPLAN
  entry_order: 9
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.WORKPLAN.COMP_STANDARD_HUMAN
  field_id: COMP.STANDARD.HUMAN
  origin: NRIIS_NATIVE
  tab: WORKPLAN
  entry_order: 10
  required: false
  status: DRAFT
  markers:
  - NEEDS_VERIFICATION
  source_ids:
  - SRC-T13
  authored_by: human
- nriis_field_id: NRIIS.WORKPLAN.COMP_STANDARD_BIOSAFETY
  field_id: COMP.STANDARD.BIOSAFETY
  origin: NRIIS_NATIVE
  tab: WORKPLAN
  entry_order: 11
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.WORKPLAN.COMP_STANDARD_ANIMAL
  field_id: COMP.STANDARD.ANIMAL
  origin: NRIIS_NATIVE
  tab: WORKPLAN
  entry_order: 12
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.WORKPLAN.COMP_STANDARD_CHEMICAL
  field_id: COMP.STANDARD.CHEMICAL
  origin: NRIIS_NATIVE
  tab: WORKPLAN
  entry_order: 13
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.WORKPLAN.WORK_PARTNERS_ORGANIZATIONS
  field_id: WORK.PARTNERS.ORGANIZATIONS
  origin: NRIIS_NATIVE
  tab: WORKPLAN
  entry_order: 14
  required: false
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T14
  authored_by: human
- nriis_field_id: NRIIS.WORKPLAN.READY_TRL_CURRENT
  field_id: READY.TRL.CURRENT
  origin: NRIIS_NATIVE
  tab: WORKPLAN
  entry_order: 15
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.WORKPLAN.READY_TRL_TARGET
  field_id: READY.TRL.TARGET
  origin: NRIIS_NATIVE
  tab: WORKPLAN
  entry_order: 16
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.WORKPLAN.READY_SRL_CURRENT
  field_id: READY.SRL.CURRENT
  origin: NRIIS_NATIVE
  tab: WORKPLAN
  entry_order: 17
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.WORKPLAN.READY_SRL_TARGET
  field_id: READY.SRL.TARGET
  origin: NRIIS_NATIVE
  tab: WORKPLAN
  entry_order: 18
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.UTILIZATION.RESULTS_PATHWAY_EXPERTS
  field_id: RESULTS.PATHWAY.EXPERTS
  origin: NRIIS_NATIVE
  tab: UTILIZATION
  entry_order: 1
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.UTILIZATION.RESULTS_PATHWAY_STAKEHOLDERS
  field_id: RESULTS.PATHWAY.STAKEHOLDERS
  origin: NRIIS_NATIVE
  tab: UTILIZATION
  entry_order: 2
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.UTILIZATION.RESULTS_CHAIN_UTILIZATION_DOMAIN
  field_id: RESULTS.CHAIN.UTILIZATION_DOMAIN
  origin: NRIIS_NATIVE
  tab: UTILIZATION
  entry_order: 3
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.UTILIZATION.RESULTS_CHAIN_UTILIZATION_DESC
  field_id: RESULTS.CHAIN.UTILIZATION_DESC
  origin: NRIIS_NATIVE
  tab: UTILIZATION
  entry_order: 4
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.UTILIZATION.RESULTS_CHAIN_BENEFIT_SUMMARY
  field_id: RESULTS.CHAIN.BENEFIT_SUMMARY
  origin: NRIIS_NATIVE
  tab: UTILIZATION
  entry_order: 5
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.UTILIZATION.RESULTS_CHAIN_USERS
  field_id: RESULTS.CHAIN.USERS
  origin: NRIIS_NATIVE
  tab: UTILIZATION
  entry_order: 6
  required: false
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T18
  authored_by: human
- nriis_field_id: NRIIS.UTILIZATION.RESULTS_CHAIN_BENEFICIARIES
  field_id: RESULTS.CHAIN.BENEFICIARIES
  origin: NRIIS_NATIVE
  tab: UTILIZATION
  entry_order: 7
  required: false
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T18
  authored_by: human
- nriis_field_id: NRIIS.UTILIZATION.RESULTS_CHAIN_OUTPUTS
  field_id: RESULTS.CHAIN.OUTPUTS
  origin: NRIIS_NATIVE
  tab: UTILIZATION
  entry_order: 8
  required: true
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T18
  authored_by: human
- nriis_field_id: NRIIS.UTILIZATION.RESULTS_CHAIN_OUTCOME_PROCESS
  field_id: RESULTS.CHAIN.OUTCOME_PROCESS
  origin: NRIIS_NATIVE
  tab: UTILIZATION
  entry_order: 9
  required: false
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T18
  authored_by: human
- nriis_field_id: NRIIS.UTILIZATION.RESULTS_CHAIN_OUTCOMES
  field_id: RESULTS.CHAIN.OUTCOMES
  origin: NRIIS_NATIVE
  tab: UTILIZATION
  entry_order: 10
  required: false
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T18
  authored_by: human
- nriis_field_id: NRIIS.UTILIZATION.RESULTS_CHAIN_IMPACTS
  field_id: RESULTS.CHAIN.IMPACTS
  origin: NRIIS_NATIVE
  tab: UTILIZATION
  entry_order: 11
  required: false
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T18
  authored_by: human
- nriis_field_id: NRIIS.UTILIZATION.RESULTS_ENTREPRENEUR_PROFILE
  field_id: RESULTS.ENTREPRENEUR.PROFILE
  origin: NRIIS_NATIVE
  tab: UTILIZATION
  entry_order: 12
  required: false
  status: EMPTY
  markers: []
  source_ids: []
  authored_by: null
- nriis_field_id: NRIIS.ATTACHMENTS.DOC_ATTACHMENTS_DOCUMENTS
  field_id: DOC.ATTACHMENTS.DOCUMENTS
  origin: NRIIS_NATIVE
  tab: ATTACHMENTS
  entry_order: 1
  required: false
  status: DRAFT
  markers: []
  source_ids:
  - SRC-T13
  authored_by: human
```

## 4. Validation and provenance appendix

### 4.1 Review gates
- RG0: not_reviewed (no review record)
- RG1: not_reviewed (no review record)
- RG2: not_reviewed (no review record)
- RG3: not_reviewed (no review record)
- RG4: not_reviewed (no review record)

### 4.2 Source manifest
- `SRC-FCALL` (PROJECT_DOCUMENT): GrantThai FICTIONAL test fund call, fixture v0.1 (funds/example/FICTIONAL_CALL@0.1/fund-profile.yaml). Not a real call.; cited by: FUND.CALL.NAME, FUND.CALL.AGENCY
- `SRC-FN1` (PRIMARY_DATA): [private]
- `SRC-SD5` (OFFICIAL_DOCUMENT): Public blank FF full-proposal form, fiscal year 2570 (SD-5 in docs/sources.md). Cited by page only.; locator: PDF p1; cited by: FUND.CALL.FISCAL_YEAR, CORE.GENERAL.RESEARCH_ISSUE, CORE.GENERAL.PLAN
- `SRC-T01` (PROJECT_DOCUMENT): FICTIONAL simulated interview, docs/demo/transcript-seedbank.md; locator: T01; cited by: FUND.CALL.FISCAL_YEAR, FUND.CALL.NAME, FUND.CALL.AGENCY
- `SRC-T02` (PROJECT_DOCUMENT): FICTIONAL simulated interview, docs/demo/transcript-seedbank.md; locator: T02; cited by: CORE.GENERAL.RESEARCH_ISSUE, CORE.GENERAL.PLAN
- `SRC-T03` (PROJECT_DOCUMENT): FICTIONAL simulated interview, docs/demo/transcript-seedbank.md; locator: T03; cited by: CORE.GENERAL.TITLE_TH, CORE.GENERAL.TITLE_EN, CORE.GENERAL.DURATION_Y, CORE.GENERAL.DURATION_M, CORE.GENERAL.OTHER_FUNDER
- `SRC-T04` (PROJECT_DOCUMENT): FICTIONAL simulated interview, docs/demo/transcript-seedbank.md; locator: T04; cited by: CORE.GENERAL.KEYWORDS_TH, CORE.GENERAL.KEYWORDS_EN, CORE.GENERAL.OECD.PRIMARY, CORE.GENERAL.OECD.SECONDARY
- `SRC-T05` (PROJECT_DOCUMENT): FICTIONAL simulated interview, docs/demo/transcript-seedbank.md; locator: T05; cited by: CORE.RESEARCH.NATIONAL_NEED
- `SRC-T06` (PROJECT_DOCUMENT): FICTIONAL simulated interview, docs/demo/transcript-seedbank.md; locator: T06; cited by: CORE.RESEARCH.PROBLEM
- `SRC-T07` (PROJECT_DOCUMENT): FICTIONAL simulated interview, docs/demo/transcript-seedbank.md; locator: T07; cited by: CORE.PRIORKNOWLEDGE.PK1
- `SRC-T08` (PROJECT_DOCUMENT): FICTIONAL simulated interview, docs/demo/transcript-seedbank.md; locator: T08; cited by: CORE.RESEARCH.GAP
- `SRC-T09` (PROJECT_DOCUMENT): FICTIONAL simulated interview, docs/demo/transcript-seedbank.md; locator: T09; cited by: CORE.RESEARCH.RQ.PRIMARY, CORE.RESEARCH.RQ.SECONDARY
- `SRC-T10` (PROJECT_DOCUMENT): FICTIONAL simulated interview, docs/demo/transcript-seedbank.md; locator: T10; cited by: CORE.NARRATIVE.OBJECTIVES, CORE.RESEARCH.OBJECTIVES
- `SRC-T11` (PROJECT_DOCUMENT): FICTIONAL simulated interview, docs/demo/transcript-seedbank.md; locator: T11; cited by: METHOD.PLAN.DESIGN
- `SRC-T12` (PROJECT_DOCUMENT): FICTIONAL simulated interview, docs/demo/transcript-seedbank.md; locator: T12; cited by: METHOD.PLAN.SAMPLE, METHOD.PLAN.INSTRUMENTS, METHOD.PLAN.DATA_COLLECTION, METHOD.PLAN.ANALYSIS
- `SRC-T13` (PROJECT_DOCUMENT): FICTIONAL simulated interview, docs/demo/transcript-seedbank.md; locator: T13; cited by: COMP.STANDARD.HUMAN, DOC.ATTACHMENTS.DOCUMENTS, METHOD.PLAN.ETHICS
- `SRC-T14` (PROJECT_DOCUMENT): FICTIONAL simulated interview, docs/demo/transcript-seedbank.md; locator: T14; cited by: PROFILE.TEAM.MEMBERS, WORK.PARTNERS.ORGANIZATIONS
- `SRC-T15` (PROJECT_DOCUMENT): FICTIONAL simulated interview, docs/demo/transcript-seedbank.md; locator: T15; cited by: GEO.AREA.RESEARCH_SITES, WORK.PLAN.ACTIVITIES
- `SRC-T16` (PROJECT_DOCUMENT): FICTIONAL simulated interview, docs/demo/transcript-seedbank.md; locator: T16; cited by: WORK.PLAN.RISKS
- `SRC-T17` (PROJECT_DOCUMENT): FICTIONAL simulated interview, docs/demo/transcript-seedbank.md; locator: T17; cited by: CORE.GENERAL.REQUESTED_BUDGET, CORE.GENERAL.TOTAL_BUDGET, BUDGET.PLAN.YEARS, BUDGET.PLAN.TOTAL, BUDGET.PLAN.ITEMS
- `SRC-T18` (PROJECT_DOCUMENT): FICTIONAL simulated interview, docs/demo/transcript-seedbank.md; locator: T18; cited by: RESULTS.PATHWAY.SUSTAINABILITY, RESULTS.CHAIN.OUTPUTS, RESULTS.CHAIN.USERS, RESULTS.CHAIN.OUTCOME_PROCESS, RESULTS.CHAIN.OUTCOMES, RESULTS.CHAIN.IMPACTS, RESULTS.CHAIN.BENEFICIARIES
- `SRC-T19` (PROJECT_DOCUMENT): FICTIONAL simulated interview, docs/demo/transcript-seedbank.md; locator: T19; cited by: CORE.EVIDENCE.E1, CORE.CLAIM.C1
- `SRC-T20` (PROJECT_DOCUMENT): FICTIONAL simulated interview, docs/demo/transcript-seedbank.md; locator: T20; cited by: CORE.NARRATIVE.SUMMARY, CORE.NARRATIVE.RATIONALE, CORE.NARRATIVE.FRAMEWORK, CORE.NARRATIVE.THEORY, CORE.NARRATIVE.METHOD

### 4.3 Unresolved references
- None.

### 4.4 Conflicts and open contradictions

Conflicts are surfaced, never merged. Every reading is printed; the "GrantThai today" line is a working default, not a decision.

#### 4.4.1 Contradictions between the design sources (registry/contradictions.yaml)

- **CX-01** (OPEN): Research Core and Methodology: authoring fields or observed NRIIS fields?
  - Reading: core/02 §1 R4, §5 04 and 05: Research Core (04) and Methodology (05) are AUTHORING_CORE. R4: never present AUTHORING_CORE fields as if they were official NRIIS fields; they reach NRIIS through the narrative renderer (§6).
  - Reading: core/05 (CORE.*, METHOD.* records): source_status OBSERVED on every CORE.* and METHOD.* record, i.e. observed on the NRIIS form.
  - GrantThai today: origin AUTHORING_CORE (never placed on a tab); source_status kept exactly as core/05 wrote it. The narrative boxes carry render_from.
  - In this project: CORE.RESEARCH.GAP, CORE.RESEARCH.NATIONAL_NEED, CORE.RESEARCH.OBJECTIVES, CORE.RESEARCH.PROBLEM, CORE.RESEARCH.RQ.PRIMARY, CORE.RESEARCH.RQ.SECONDARY, METHOD.PLAN.ANALYSIS, METHOD.PLAN.DATA_COLLECTION, METHOD.PLAN.DESIGN, METHOD.PLAN.ETHICS, METHOD.PLAN.INSTRUMENTS, METHOD.PLAN.SAMPLE

- **CX-02** (OPEN): Need, Problem, Gap and Innovation: plain text or structured objects?
  - Reading: core/05 CORE.NATIONAL_NEED, CORE.PROBLEM, CORE.GAP, CORE.INNOVATION: type text.
  - Reading: core/02 §5 04.01, 04.02, 04.03, 04.08: objects with named keys (statement, context, evidence, what_is_known, what_is_new, ...).
  - GrantThai today: type rich_text|object: plain text or an object with the core/02 keys are both valid.
  - In this project: CORE.RESEARCH.GAP, CORE.RESEARCH.NATIONAL_NEED, CORE.RESEARCH.PROBLEM

- **CX-03** (OPEN): Direction of the Budget-Activity, Ethics-Method and Sites/Partners-Activity edges
  - Reading: core/06 §3 (top-level architecture) and core/02 §11 (cross-field consistency graph): BUDGET -> ACTIVITIES, ETHICS/COMPLIANCE -> METHODOLOGY, SITES/PARTNERS -> ACTIVITIES.
  - Reading: core/06 §4 (proposal entity graph) and §12 (budget graph): ACTIVITY -> BUDGET_ITEM, METHODOLOGY -> ETHICS_REQUIREMENT (RESEARCH_SITE -> ACTIVITY and PARTNER -> ACTIVITY agree with §3).
  - GrantThai today: spec/common/chain.yaml uses Activity -> BudgetItem and Method -> EthicsRequirement (core/06 §4/§12). Sites and partners are attribute links, not causal edges.
  - In this project: BUDGET.PLAN.ITEMS, METHOD.PLAN.ETHICS, WORK.PLAN.ACTIVITIES

- **CX-04** (OPEN): Does Impact follow Beneficiary, or do both follow Outcome?
  - Reading: core/06 §3: OUTCOMES -> BENEFICIARIES -> IMPACTS -> FUNDING KR (a line).
  - Reading: core/02 §11 and core/06 §4: Outcome -> Beneficiary and Outcome -> Impact (a fan-out); Impact -> Funding KR.
  - GrantThai today: spec/common/chain.yaml fans out from Outcome (core/02 §11, core/06 §4).
  - In this project: RESULTS.CHAIN.BENEFICIARIES, RESULTS.CHAIN.IMPACTS

- **CX-05** (OPEN): Project characteristic: new project only, or new or continuing?
  - Reading: core/05 GEN.CHARACTERISTIC: allowed_values ["New Project"] (one observed form).
  - Reading: SD-1 (edition 2566) p15, part 1 item 3: a new project, or a project continuing from an earlier fiscal year, with a past-performance table for a continuing project.
  - GrantThai today: allowed_values keeps "New Project"; "Continuing Project" is a candidate value (NEEDS_VERIFICATION) that is accepted with a REVIEW finding (S011). CORE.GENERAL.PAST_PERFORMANCE holds the table.
  - In this project: no record of this project (affects CORE.GENERAL.CHARACTERISTIC, CORE.GENERAL.PAST_PERFORMANCE)

- **CX-06** (OPEN): Two different full names for one funding-unit abbreviation
  - Reading: SD-1 (edition 2566) p5: gives one full name for the unit (exact string in docs/sources.md, SD-1 note).
  - Reading: SD-3 (revision 3, edition 2569) PDF p1: gives a different full name for the same abbreviation (exact string in docs/sources.md, SD-3 note).
  - GrantThai today: Not resolved here. GrantThai names no funding unit in its data; the difference is recorded in docs/sources.md only.
  - In this project: no record of this project (affects docs/sources.md)

- **CX-07** (OPEN): Expert connections and stakeholder engagement: which tab?
  - Reading: core/02 §9 compact field map: 08 Utilization and Translation Pathway -> NRIIS UTILIZATION / RESULTS.
  - Reading: SD-1 (edition 2566) p17, part 3 item 9: listed under part 3 (the plan section), items 9.1 and 9.2, together with post-project continuation by users.
  - GrantThai today: mappings/nriis/section_to_tab.yaml keeps TranslationPathway on UTILIZATION, marked NEEDS_VERIFICATION.
  - In this project: no record of this project (affects mappings/nriis/section_to_tab.yaml, RESULTS.PATHWAY.EXPERTS, RESULTS.PATHWAY.STAKEHOLDERS)

- **CX-08** (OPEN): Expected outcomes: an NRIIS form item or a recommended extension?
  - Reading: core/02 §5 09.04; core/05 RESULTS.OUTCOMES: RECOMMENDED_EXTENSION (core/02) / INFERRED_SCHEMA_EXTENSION (core/05): not confirmed as a native field.
  - Reading: SD-1 (edition 2566) p18, part 5 item 4: expected outcomes from users' use of the outputs are a numbered form item.
  - GrantThai today: origin NRIIS_NATIVE (placed on the UTILIZATION tab), source_status kept as core/05 wrote it, marker NEEDS_VERIFICATION.
  - In this project: RESULTS.CHAIN.OUTCOMES

- **CX-09** (OPEN): How many form parts (tabs), and in what order?
  - Reading: core/02 §9 compact field map: five: GENERAL, PROJECT, WORKPLAN, UTILIZATION, ATTACHMENTS/VALIDATION.
  - Reading: SD-1 (edition 2566) p15-18; SD-4 p164 and p166: part 1 general, 2 project, 3 plan, 4 entrepreneur information (if any), 5 output/outcome/impact; SD-4 adds part 5 attachments and part 6 a validation page (its numbering differs from SD-1).
  - Reading: SD-5 (FF full-proposal form, 2570) p1, p3, p6, p12: four parts: 1 general (p1), 2 project (p3), 3 workplan (p6), 4 outputs/outcomes/impacts (p12).
  - GrantThai today: five tabs kept (NEEDS_VERIFICATION). Entrepreneur information is placed on UTILIZATION. The validation page is not modelled (the worksheet's readiness summary plays that role). Form profiles shipped in v0.2 (mappings/nriis/form_profiles/); no profile overrides the tab order, so SD-5's four-part reading is recorded, not applied.
  - In this project: no record of this project (affects mappings/nriis/section_to_tab.yaml, section Entrepreneur, RESULTS.ENTREPRENEUR.PROFILE)

- **CX-10** (OPEN): OECD primary/secondary or main/sub field?
  - Reading: core/05 GEN.OECD.PRIMARY, GEN.OECD.SECONDARY: a primary and a secondary OECD research field, no option list.
  - Reading: SD-1 (edition 2566) p15 item 6 and p20: main/sub OECD field ('หลัก/ย่อย'), with a list of 6 main groups and their sub-fields on p20.
  - GrantThai today: PRIMARY takes a main-group candidate code (1-6), SECONDARY a sub-field candidate code (e.g. 6.3); the list is a candidate (NEEDS_VERIFICATION) and a value outside it gets a REVIEW finding (S011), never a BLOCK.
  - In this project: CORE.GENERAL.OECD.PRIMARY, CORE.GENERAL.OECD.SECONDARY

#### 4.4.2 Conflicts recorded in project.yaml
- None recorded.

### 4.5 Project records not placed on any NRIIS tab

These records are not NRIIS fields (origin AUTHORING_CORE, FUND_PROFILE, DERIVED or RECOMMENDED_EXTENSION, or a system-assigned section). Do not paste them as NRIIS boxes; where `feeds` is shown, they are what the listed narrative box is written from.

`BUDGET.PLAN.TOTAL` (ORIGIN: DERIVED; chain: fields; status: DRAFT; not on a tab because: calculated from other fields)

```text
480000
```

`RESULTS.PATHWAY.SUSTAINABILITY` (ORIGIN: AUTHORING_CORE; chain: fields; status: DRAFT; not on a tab because: authoring core, an internal research-design record (it reaches NRIIS only through the narrative box it feeds, if any); feeds: RESULTS.PATHWAY.STAKEHOLDERS)

```text
{
 "owner": "(สมมติ) คณะกรรมการธนาคารเมล็ดพันธุ์ของแต่ละหมู่บ้าน",
 "routine": "ทบทวนกติกาและทดสอบความงอกก่อนฤดูปลูกทุกปี",
 "resources_required": "ศาลาเก็บเมล็ดของกลุ่มเกษตรกร",
 "platform_or_network": "เครือข่ายเรียนรู้สามหมู่บ้าน",
 "continuity_mechanism": "งานแลกเปลี่ยนเมล็ดพันธุ์ประจำปีที่ชุมชนจัดเอง",
 "user_ids": [
  "USR1"
 ]
}
```

`CORE.RESEARCH.NATIONAL_NEED` (ORIGIN: AUTHORING_CORE; chain: Need; status: DRAFT; not on a tab because: authoring core, an internal research-design record (it reaches NRIIS only through the narrative box it feeds, if any); feeds: CORE.NARRATIVE.SUMMARY, CORE.NARRATIVE.RATIONALE)

```text
{
 "statement": "(สมมติ) ชาวนารายย่อยในอำเภอสมมติต้องซื้อเมล็ดพันธุ์ข้าวทุกฤดู ต้นทุนสูงขึ้น และพันธุ์ข้าวพื้นบ้านที่ปรับตัวกับน้ำท่วมขังค่อย ๆ หายไป",
 "affected_population_or_system": "(สมมติ) ครัวเรือนชาวนารายย่อยในอำเภอสมมติ"
}
```

`CORE.RESEARCH.PROBLEM` (ORIGIN: AUTHORING_CORE; chain: Problem; status: DRAFT; not on a tab because: authoring core, an internal research-design record (it reaches NRIIS only through the narrative box it feeds, if any); feeds: CORE.NARRATIVE.SUMMARY, CORE.NARRATIVE.RATIONALE)

```text
(สมมติ) ในสามหมู่บ้าน ครัวเรือนเก็บเมล็ดพันธุ์กันเองโดยไม่มีกติกากลาง เมล็ดที่เก็บไว้งอกไม่ดีหลายครั้ง และสองในสามหมู่บ้านบอกว่าพันธุ์พื้นบ้านบางพันธุ์หายไปแล้ว
```

`CORE.RESEARCH.GAP` (ORIGIN: AUTHORING_CORE; chain: Gap; status: DRAFT; not on a tab because: authoring core, an internal research-design record (it reaches NRIIS only through the narrative box it feeds, if any); feeds: CORE.NARRATIVE.SUMMARY, CORE.NARRATIVE.RATIONALE)

```text
ยังไม่มีกติกาและกระบวนการที่ชุมชนออกแบบเองสำหรับธนาคารเมล็ดพันธุ์ระดับหมู่บ้านที่เชื่อมกันเป็นเครือข่ายในอำเภอสมมติ และยังไม่รู้ว่าเงื่อนไขใดทำให้ธนาคารเมล็ดพันธุ์ดำเนินต่อได้หลังโครงการจบ
```

`CORE.RESEARCH.RQ.PRIMARY` (ORIGIN: AUTHORING_CORE; chain: RQ; status: DRAFT; not on a tab because: authoring core, an internal research-design record (it reaches NRIIS only through the narrative box it feeds, if any); feeds: CORE.NARRATIVE.RATIONALE)

```text
ธนาคารเมล็ดพันธุ์ที่ชุมชนออกแบบกติกาเองและเชื่อมกันเป็นเครือข่ายสามหมู่บ้าน ช่วยให้ครัวเรือนเข้าถึงเมล็ดพันธุ์ข้าวพื้นบ้านที่งอกดีในฤดูถัดไปได้หรือไม่ ภายใต้เงื่อนไขใด
```

`CORE.RESEARCH.RQ.SECONDARY` (ORIGIN: AUTHORING_CORE; chain: RQ; status: DRAFT; not on a tab because: authoring core, an internal research-design record (it reaches NRIIS only through the narrative box it feeds, if any))

```text
ตอนนี้มีพันธุ์ข้าวพื้นบ้านอะไรเหลืออยู่ และใครรู้วิธีเก็บเมล็ดพันธุ์
กติกาธนาคารเมล็ดพันธุ์แบบไหนที่ครัวเรือนยอมทำตามจริง
```

`CORE.RESEARCH.OBJECTIVES` (ORIGIN: AUTHORING_CORE; chain: Objective; status: DRAFT; not on a tab because: authoring core, an internal research-design record (it reaches NRIIS only through the narrative box it feeds, if any); feeds: CORE.NARRATIVE.SUMMARY, CORE.NARRATIVE.OBJECTIVES)

```text
[
 {
  "id": "OBJ1",
  "statement": "สำรวจพันธุ์ข้าวพื้นบ้านและความรู้การเก็บเมล็ดพันธุ์ในสามหมู่บ้าน",
  "rq_ids": [
   "CORE.RESEARCH.RQ.PRIMARY"
  ],
  "method_ids": [
   "MP1"
  ],
  "output_ids": [
   "OUT1"
  ]
 },
 {
  "id": "OBJ2",
  "statement": "ออกแบบและทดลองกติกาธนาคารเมล็ดพันธุ์ร่วมกับผู้ร่วมวิจัยชุมชน",
  "rq_ids": [
   "CORE.RESEARCH.RQ.PRIMARY"
  ],
  "method_ids": [
   "MP2"
  ],
  "output_ids": [
   "OUT2"
  ]
 },
 {
  "id": "OBJ3",
  "statement": "สร้างเครือข่ายเรียนรู้ข้ามหมู่บ้านและคู่มือธนาคารเมล็ดพันธุ์",
  "rq_ids": [
   "CORE.RESEARCH.RQ.PRIMARY"
  ],
  "method_ids": [
   "MP3"
  ],
  "output_ids": [
   "OUT3",
   "OUT4"
  ]
 }
]
```

`METHOD.PLAN.DESIGN` (ORIGIN: AUTHORING_CORE; chain: Method; status: DRAFT; not on a tab because: authoring core, an internal research-design record (it reaches NRIIS only through the narrative box it feeds, if any); feeds: CORE.NARRATIVE.SUMMARY, CORE.NARRATIVE.METHOD)

```text
{
 "paradigm": "participatory",
 "design_type": "การวิจัยเชิงปฏิบัติการแบบมีส่วนร่วม (PAR) สามวง",
 "approach": "qualitative with simple counts",
 "quantitative_component": "อัตราการงอก จำนวนพันธุ์ จำนวนครัวเรือนที่ยืมและคืนเมล็ด",
 "qualitative_component": "สัมภาษณ์กึ่งโครงสร้าง เวทีสะท้อนคิด",
 "phases": [
  {
   "id": "MP1",
   "name": "วงที่ 1 สำรวจ",
   "description": "สำรวจพันธุ์และความรู้การเก็บเมล็ดพันธุ์",
   "objective_ids": [
    "OBJ1"
   ]
  },
  {
   "id": "MP2",
   "name": "วงที่ 2 ตั้งและทดลองธนาคาร",
   "description": "ออกแบบกติกา ตั้งธนาคาร ทดสอบความงอก",
   "objective_ids": [
    "OBJ2"
   ]
  },
  {
   "id": "MP3",
   "name": "วงที่ 3 สะท้อนผลและขยายเครือข่าย",
   "description": "เวทีสะท้อนคิดและงานแลกเปลี่ยนข้ามหมู่บ้าน",
   "objective_ids": [
    "OBJ3"
   ]
  }
 ]
}
```

`METHOD.PLAN.SAMPLE` (ORIGIN: AUTHORING_CORE; chain: Method; status: DRAFT; not on a tab because: authoring core, an internal research-design record (it reaches NRIIS only through the narrative box it feeds, if any); feeds: CORE.NARRATIVE.METHOD)

```text
{
 "sampling_method": "เลือกแบบเจาะจง ครัวเรือนทำนาที่สมัครใจ",
 "groups": [
  {
   "id": "SG1",
   "description": "(สมมติ) ครัวเรือนทำนา หมู่บ้านละประมาณ 20 ครัวเรือน",
   "target_n": 60
  },
  {
   "id": "SG2",
   "description": "(สมมติ) ผู้อาวุโสที่รู้เรื่องพันธุ์ข้าว หมู่บ้านละ 3-5 คน",
   "target_n": 15
  }
 ],
 "sample_size_justification": "ครอบคลุมครัวเรือนที่สมัครใจในสามหมู่บ้าน เหมาะกับวง PAR ขนาดเล็ก"
}
```

`METHOD.PLAN.INSTRUMENTS` (ORIGIN: AUTHORING_CORE; chain: Method; status: DRAFT; not on a tab because: authoring core, an internal research-design record (it reaches NRIIS only through the narrative box it feeds, if any); feeds: CORE.NARRATIVE.METHOD)

```text
[
 {
  "id": "INS1",
  "name": "แบบบันทึกทะเบียนพันธุ์ข้าว",
  "purpose": "บันทึกพันธุ์ที่เหลือและผู้เก็บ",
  "instrument_type": "record form",
  "construct_measured": "จำนวนพันธุ์ที่ยังมีอยู่",
  "validity_method": "เพื่อนอาจารย์สองคนอ่านตรวจ",
  "reliability_method": "ทดลองใช้ในหมู่บ้านเดียวก่อน"
 },
 {
  "id": "INS2",
  "name": "แบบบันทึกทดสอบความงอก",
  "purpose": "วัดอัตราการงอกของเมล็ดที่ฝากธนาคาร",
  "instrument_type": "record form",
  "construct_measured": "อัตราการงอก",
  "validity_method": "นักวิจัยสายพืชศาสตร์ตรวจ",
  "reliability_method": "ทดสอบซ้ำสองชุด"
 },
 {
  "id": "INS3",
  "name": "แนวคำถามสัมภาษณ์กึ่งโครงสร้าง",
  "purpose": "ความรู้การเก็บเมล็ดและเหตุผลการทำตามกติกา",
  "instrument_type": "interview guide",
  "construct_measured": "ความรู้และเหตุผลการปฏิบัติตามกติกา",
  "validity_method": "เพื่อนอาจารย์สองคนอ่านตรวจ",
  "reliability_method": "ทดลองใช้ในหมู่บ้านเดียวก่อน"
 },
 {
  "id": "INS4",
  "name": "แบบบันทึกเวทีสะท้อนคิด",
  "purpose": "บันทึกบทเรียนแต่ละวง",
  "instrument_type": "meeting record",
  "construct_measured": "บทเรียนและการปรับกติกา",
  "validity_method": "ผู้ร่วมวิจัยชุมชนอ่านทวน",
  "reliability_method": "สองคนจดพร้อมกัน"
 }
]
```

`METHOD.PLAN.DATA_COLLECTION` (ORIGIN: AUTHORING_CORE; chain: Data; status: DRAFT; not on a tab because: authoring core, an internal research-design record (it reaches NRIIS only through the narrative box it feeds, if any); feeds: CORE.NARRATIVE.METHOD)

```text
[
 {
  "id": "DC1",
  "source": "ครัวเรือนและผู้อาวุโส (สำรวจ)",
  "collection_method": "ทะเบียนพันธุ์และสัมภาษณ์",
  "timing": "เดือน 2-6",
  "method_ids": [
   "MP1"
  ],
  "instrument_ids": [
   "INS1",
   "INS3"
  ],
  "activity_ids": [
   "ACT2"
  ],
  "responsible_person_ids": [
   "TM1",
   "TM3",
   "TM4",
   "TM5"
  ]
 },
 {
  "id": "DC2",
  "source": "ธนาคารเมล็ดพันธุ์สามหมู่บ้าน",
  "collection_method": "ทดสอบความงอกและบันทึกการยืม-คืน",
  "timing": "เดือน 5-10",
  "method_ids": [
   "MP2"
  ],
  "instrument_ids": [
   "INS2"
  ],
  "activity_ids": [
   "ACT3"
  ],
  "responsible_person_ids": [
   "TM2"
  ]
 },
 {
  "id": "DC3",
  "source": "เวทีสะท้อนคิดและงานแลกเปลี่ยน",
  "collection_method": "บันทึกเวที",
  "timing": "เดือน 6-12",
  "method_ids": [
   "MP2",
   "MP3"
  ],
  "instrument_ids": [
   "INS4"
  ],
  "activity_ids": [
   "ACT3",
   "ACT4"
  ],
  "responsible_person_ids": [
   "TM1"
  ]
 }
]
```

`METHOD.PLAN.ANALYSIS` (ORIGIN: AUTHORING_CORE; chain: Analysis; status: DRAFT; not on a tab because: authoring core, an internal research-design record (it reaches NRIIS only through the narrative box it feeds, if any); feeds: CORE.NARRATIVE.METHOD)

```text
{
 "quantitative_methods": [
  "ร้อยละการงอกต่อธนาคาร",
  "นับจำนวนพันธุ์และครัวเรือนที่ยืม-คืน"
 ],
 "qualitative_method": "วิเคราะห์เนื้อหาเชิงประเด็นจากสัมภาษณ์และบันทึกเวที",
 "software_or_tools": [
  "spreadsheet"
 ],
 "data_ids": [
  "DC1",
  "DC2",
  "DC3"
 ]
}
```

`METHOD.PLAN.ETHICS` (ORIGIN: AUTHORING_CORE; chain: EthicsRequirement; status: DRAFT; not on a tab because: authoring core, an internal research-design record (it reaches NRIIS only through the narrative box it feeds, if any); feeds: CORE.NARRATIVE.METHOD)

```text
{
 "human_participants": true,
 "informed_consent": "อ่านเอกสารให้ฟัง ขอความยินยอมด้วยวาจาต่อหน้าพยาน แล้วลงนามหรือพิมพ์ลายนิ้วมือ",
 "privacy": "ใช้รหัสแทนชื่อ",
 "confidentiality": "เก็บบันทึกที่มีชื่อแยกจากข้อมูลวิเคราะห์",
 "withdrawal": "ถอนตัวได้ทุกเมื่อ",
 "compensation": "ไม่มี",
 "risk_level": "minimal",
 "risk_management": "ให้เครดิตความรู้ของผู้อาวุโสตามที่เจ้าของความรู้ยินยอม",
 "vulnerable_groups": [
  "ผู้อาวุโสที่อ่านหนังสือไม่คล่อง"
 ],
 "conflict_of_interest": "ไม่มี"
}
```

`FUND.CALL.KEY_RESULTS` (ORIGIN: FUND_PROFILE; chain: KR; status: NEEDS_INPUT; not on a tab because: a requirement of the bound call, not an NRIIS form field)

```text
NEEDS_INPUT
```

`CORE.PRIORKNOWLEDGE.PK1` (ORIGIN: none (not a registry field); chain: PriorKnowledge; status: DRAFT; not on a tab because: chain content without a registry field (never an NRIIS field))

```text
(สมมติ) บ้านสมมติหนึ่งเคยจัดงานแลกเปลี่ยนเมล็ดพันธุ์ครั้งเดียว มีคนมาร่วมมาก แต่ไม่มีผู้ดูแลต่อ
```

`CORE.PRIORKNOWLEDGE.PK2` (ORIGIN: none (not a registry field); chain: PriorKnowledge; status: NEEDS_INPUT; not on a tab because: chain content without a registry field (never an NRIIS field))

```text
NEEDS_INPUT
```

`CORE.EVIDENCE.E1` (ORIGIN: none (not a registry field); chain: Evidence; status: DRAFT; not on a tab because: chain content without a registry field (never an NRIIS field))

```text
(สมมติ) งานแลกเปลี่ยนเมล็ดพันธุ์ครั้งเดียวในบ้านสมมติหนึ่งมีคนสนใจมาก ผู้วิจัยสมมติเห็นว่ายังเป็นหลักฐานที่อ่อน
```

`CORE.CLAIM.C1` (ORIGIN: none (not a registry field); chain: Claim; status: DRAFT; not on a tab because: chain content without a registry field (never an NRIIS field))

```text
ธนาคารเมล็ดพันธุ์ที่ชุมชนตั้งกติกาเองทำได้จริงในหมู่บ้านลักษณะนี้ และระบุเงื่อนไขที่ช่วยหรือขัดขวางได้
```

### 4.6 Completeness checklist

Guidance only, never validation (guidance/writing_intent.yaml; status DRAFT, NEEDS_VERIFICATION). `PASS` means only that the listed fields are filled or linked as the check describes; `HUMAN_CHECK` items are for the researcher to confirm and are never marked PASS by GrantThai. Thai wording: NEEDS_INPUT.

| id | state | fields | check |
|---|---|---|---|
| WC01 | PASS | CORE.RESEARCH.NATIONAL_NEED, CORE.RESEARCH.PROBLEM, CORE.RESEARCH.GAP, CORE.RESEARCH.RQ.PRIMARY | Need, problem, gap and the primary research question are all written. |
| WC02 | PASS | CORE.RESEARCH.OBJECTIVES | Every objective names the research question it answers. |
| WC03 | PASS | CORE.RESEARCH.OBJECTIVES | Every objective names the method that reaches it. |
| WC04 | PASS | CORE.RESEARCH.OBJECTIVES | Every objective names the output it produces. |
| WC05 | PASS | METHOD.PLAN.DESIGN, METHOD.PLAN.SAMPLE, METHOD.PLAN.INSTRUMENTS, METHOD.PLAN.DATA_COLLECTION, METHOD.PLAN.ANALYSIS, METHOD.PLAN.ETHICS | Design, sample, instruments, data collection, analysis and ethics are all written. |
| WC06 | PASS | RESULTS.CHAIN.OUTPUTS | Every output names the objective that produces it. |
| WC07 | OPEN | CORE.ALIGNMENT.STATEMENT | The one-sentence alignment statement is written. |
| WC08 | PASS | CORE.NARRATIVE.SUMMARY, CORE.NARRATIVE.RATIONALE, CORE.NARRATIVE.OBJECTIVES, CORE.NARRATIVE.FRAMEWORK, CORE.NARRATIVE.THEORY, CORE.NARRATIVE.METHOD | The narrative boxes (summary, rationale, objectives, framework, theory, method) are all written. |
| WC09 | PASS | CORE.NARRATIVE.SUMMARY, CORE.NARRATIVE.RATIONALE, CORE.NARRATIVE.METHOD, CORE.RESEARCH.OBJECTIVES, CORE.ALIGNMENT.STATEMENT | No narrative box or core field is outside its length target. |
| WC10 | PASS | CORE.GENERAL.TITLE_TH, CORE.GENERAL.TITLE_EN, CORE.GENERAL.KEYWORDS_TH, CORE.GENERAL.KEYWORDS_EN | Titles and keywords are written in both languages. |
| WC11 | HUMAN_CHECK | CORE.RESEARCH.NATIONAL_NEED, CORE.RESEARCH.PROBLEM, CORE.RESEARCH.GAP | Every factual claim in need, problem and gap has a source the reader can find. |
| WC12 | HUMAN_CHECK | CORE.NARRATIVE.SUMMARY, CORE.NARRATIVE.RATIONALE, CORE.NARRATIVE.OBJECTIVES, CORE.NARRATIVE.FRAMEWORK, CORE.NARRATIVE.THEORY, CORE.NARRATIVE.METHOD | Each narrative box says only what its render_from records say; nothing new is introduced in the box. |
| WC13 | HUMAN_CHECK | CORE.NARRATIVE.SUMMARY, CORE.NARRATIVE.RATIONALE | The summary and rationale read as the researcher's own words, and the person pasting them has re-read them once against the form. |
| WC14 | HUMAN_CHECK | RESULTS.CHAIN.IMPACTS, CORE.RESEARCH.NATIONAL_NEED | The results chain reaches the national need: at least one impact returns to it, with an honest claim strength. |

### 4.7 AI Use Declaration (GrantThai appendix, not an NRIIS field)

A GrantThai appendix, not an NRIIS box. Its shape follows the sample "AI Use Declaration" form in Appendix A (p.34) of the GenAI guideline 2569 (National Research Council of Thailand, September 2569; docs/sources.md). Whether NRIIS or this call asks for such a declaration is NEEDS_VERIFICATION: attach or paste it only if the call or your institution asks. Everything below is self-declared by the researcher and unverified; GrantThai checks only that it is filled in and confirmed (rule AI001), never that it is true.

1. Project title (p.34 item 1): เครือข่ายเรียนรู้ธนาคารเมล็ดพันธุ์ข้าวพื้นบ้านโดยชุมชน อำเภอสมมติ จังหวัดสมมติ ก
2. Responsible person / PI (p.34 item 2): the member marked PI in `PROFILE.TEAM.MEMBERS` (section 2).
3. AI tools used (p.34 items 3-4; p.11 tool, stage and purpose):

| tool | developer | version | stages | purpose | used on |
|---|---|---|---|---|---|
| AI assistant (simulated interview; demo only) | not applicable (simulated; demo only) | not applicable (simulated; demo only) | proposal_writing, language_editing | FICTIONAL: interviewed the persona; translated the English title and keywords; drafted the gap statement, rationale, method narrative and summary from the persona's answers | one simulated interview session (demo only) |

4. Influence on decisions or conclusions (p.11): FICTIONAL: the persona chose the research question, objectives, method and budget; the AI only reworded the persona's answers into narrative boxes. No research data or result was produced by the AI.
5. Types of data given to the AI and how personal or confidential data was kept out (p.14-16; p.34 item 5): FICTIONAL: only the persona's invented interview answers were given to the AI. The persona's field notes (SRC-FN1, personal data) were described by type, never pasted.
6. Prompts, settings and output log kept at (p.12-13 item 7; p.34 item 6): docs/demo/transcript-seedbank.md (turn ids T01-T21)
7. Human verification: what was checked, how, and who signs (p.12 item 4; p.34 item 7): NEEDS_INPUT
8. Values in project.yaml written with AI assistance: 6 (listed in section 1.5 for the researcher to confirm).
9. The researcher's own risk self-assessment, 1 (low) to 3 (high), on the five dimensions of the guideline's example scoring table (p.10-11, an example only):
   - Impact on research conclusions: 2
   - Accuracy risk (hallucination): 2
   - Data sensitivity: 1
   - Bias risk: 1
   - Reproducibility / checkability: 2
   - GrantThai convention level: 2. This is GrantThai's own convention (the highest of the five scores), not the guideline's: the guideline gives the five dimensions and example readings of levels 1-3 but no rule for combining them.
10. Declaration of responsibility (p.12 item 4; p.15 item 2.3; p.34 item 8): NOT CONFIRMED (NEEDS_INPUT). Only the researcher can confirm, after reading this declaration, by setting declaration_confirmed_by_human: true in project.yaml. An AI never sets it.

- Still missing (rule AI001): human_verification is empty.
