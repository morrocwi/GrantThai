# Scored comparison: the fictional demo against funded, public Thai research

> **The demo is FICTIONAL.** `examples/demo-seedbank/` was made by an AI assistant that played both interviewer and researcher. The real works below are used only as a benchmark for structure and quality. Nothing from them is copied into the demo.

GrantThai is an independent, unofficial project; see `NOTICE`.

**Status: `DRAFT`.** This file is one reading by an AI reviewer that did
not write the demo. It is **not blind**: the reviewer knew which document
was the demo. It does not replace the two independent scorers that
`docs/demo/comparison.md` section 4 still waits for, and it validates
nothing. Every PDF page cited was read by this reviewer (`VERIFIED`)
unless marked `relayed`; scores and the verdict are `INSTINCT`.

## 1. What is compared

| Id | Document | Used for |
|---|---|---|
| Demo | `examples/demo-seedbank/NRIIS_SUBMISSION.md` and its `project.yaml` | all dimensions |
| R0 | blank Fundamental Fund full-proposal form, 2570 cycle (`SD-5` in `docs/sources.md`), 52 pp. | proposal-only items (D9, D10) |
| R1 | community strength on a rice-farming base, Narathiwat; first author พรพันธุ์ เขมคุณาศัย; contract RDG60S0001 | research core, D1–D8, D11 |
| R2 | integrated community care for dependent older people before a COVID-19 recurrence; first author สุพิชญา หวังปิติพาณิชย์; `hdl.handle.net/11228/5712` | research core |
| R3 | synthesis of funded research on developing people, communities and Thai society; first author สมจิต แดนสีแก้ว; contract RDG5840049 | research core |
| R4 | outcome and impact evaluation of the Genomics Thailand programme; contract ORG65F3010 | anchor for D7 only |

Titles, hashes and access terms: `docs/demo/comparison.md` section 1.
No source grants an open licence, so only short fragments are quoted, with
a page. Personal details and approval numbers printed in R1 and R2 are not
copied.

**Asymmetry that limits every conclusion.** R1–R3 are funded **final
reports**; the demo is a simulated **proposal**. Reports show data a
proposal cannot have and drop budget and plan parts. Dimensions a report
would not contain are `N/A-report`.

## 2. Field coverage

Grouped by form part (a per-field matrix over the 122 registry fields is
improvement 9). Presence only, not quality.

| Form part (R0 item, page) | R1 | R2 | R3 | Demo (status) | GrantThai gap? |
|---|---|---|---|---|---|
| Need and problem (part 2, p3) | ch. 1, PDF p20–22 | ch. 1, PDF p13–18 | ch. 1, PDF p16–18 | `CORE.RESEARCH.NATIONAL_NEED`, `.PROBLEM`: DRAFT | N |
| Gap against prior work | not found in ch. 1 (OPEN) | not found (OPEN) | gaps between funded projects, PDF p22 | `CORE.RESEARCH.GAP`: DRAFT; `PK2`: NEEDS_INPUT | N |
| Research questions | 4, PDF p23 | none found | 1 with sub-questions, PDF p19 | `RQ.PRIMARY` + 2 secondary: DRAFT | N |
| Objectives | 4, PDF p23 | 3, PDF p19 | 4, PDF p20 | 3, linked: DRAFT | N |
| Sites and target groups (part 3, p6) | 3 named communities to sub-district, PDF p23–25 | 6 provinces, 3 groups, PDF p37 | not applicable (synthesis) | 3 fictional villages, 2 sample groups | N |
| Framework (part 2, p3) | diagram page, PDF p38 | adapted from two cited models, PDF p20 | input–process–outcome diagram, PDF p20 | one sentence: DRAFT | N |
| Literature and references | ch. 2, many cited sources, PDF p31–34 | ch. 2; bibliography PDF p94 | ch. 2; references PDF p97 | theory named, no references: NEEDS_INPUT | N |
| Method | PAR in 5 stages, PDF p39 | descriptive, sample size calculated, PDF p38 | qualitative synthesis, PDF p9 | PAR in 3 cycles, instruments, analysis | Y: no synthesis/meta design value (G6) |
| Ethics (part 3, standards) | not found by keyword (OPEN) | two committees, consent, PDF p40–42 | consent and confidentiality, PDF p44–45 | consent route, vulnerable group, approval pending | N |
| Outputs, users, beneficiaries (part 2 item 8, p4; part 4, p12) | expected results, PDF p25 | guidelines and policy proposals, PDF p90–93 | phased outputs and use plan, PDF p22–23 | 4 outputs, 2 users, 1 beneficiary group | Y: sector × count matrix unconfirmed (G2) |
| Output → outcome process (part 4, p12–13) | partial | partial | use plan, PDF p23 | 2 pathways, 1 outcome | Y: policy use is a **process** type on R0 p13, the demo models it as an output (OUT4) |
| Impact | partial | partial | policy recommendations with lead agencies and 5-year horizon, PDF p7–8 | 1 impact, CONTRIBUTORY | N |
| Focus area, plan, key results (part 1, p1) | N/A-report | N/A-report | N/A-report | free text NEEDS_VERIFICATION; KR NEEDS_INPUT | Y: no focus-area field (G1) |
| Workplan by month (part 3, p6) | N/A-report | N/A-report | phase table with months, PDF p22 | 4 activities, months, weights | N |
| Budget in categories (part 3, p9) | N/A-report | N/A-report | N/A-report | 6 lines, arithmetic checked | Y: R0 category rules not evaluated (G3) |

**Coverage of 12 research-core parts** (need, problem, gap, RQ,
objectives, sites, framework, literature, method, ethics, results, policy
use): R1 10/12, R2 10/12, R3 11/11 (sites not applicable), demo 11/12
(literature missing). Presence flatters the demo, because GrantThai asks
for every part by design.

## 3. Rubric scores (1–5, one non-blind AI reading, DRAFT)

Anchors: `docs/demo/comparison.md` section 3.

| # | Demo | R1 | R2 | R3 | Evidence |
|---|---|---|---|---|---|
| D1 Problem and need | 2 | 4 | 5 | 4 | Demo: local need marked “(สมมติ)”, no data or source. R1: cited area figure for abandoned paddy (PDF p20). R2: cited national ageing and dependency figures (PDF p13–14, p17). R3: cited national development plans (PDF p16–17). |
| D2 Gap | 2 | 2 | 2 | 4 | Demo gap is one local absence, AI-assisted, no prior work (`CORE.RESEARCH.GAP`). R1 and R2: no gap against prior work found in the pages read (OPEN). R3 synthesises 9 funded projects and names gaps between them as an output (PDF p22). |
| D3 RQ ↔ objectives | 3 | 5 | 1 | 3 | Demo: 3 numbered objectives all point to the one primary RQ; secondary RQs are not linked. R1: 4 RQs and 4 objectives numbered one to one (PDF p23). R2: no RQ found, so the anchor gives 1, although the work was funded. R3: 1 RQ with sub-questions against 4 objectives (PDF p19–20). |
| D4 Framework / theory | 2 | 4 | 4 | 4 | Demo: one causal sentence, theory “ยังไม่ได้ใส่อ้างอิง” (not yet referenced). R1: framework page (PDF p38) and a concept chapter with indicator sources (PDF p31). R2: model adapted from two cited authors, 4 phases (PDF p20). R3: input–process–outcome diagram with constructs (PDF p20). |
| D5 Method fit | 4 | 3 | 3 | 3 | Demo: design, sample, 4 instruments with validity and reliability notes, analysis, each tied to a phase and objective (`METHOD.PLAN.*`). R1: 5 PAR stages (PDF p39); per-objective instruments not verified. R2: sample size says one author's formula, then applies another's (PDF p38). R3: two visits per project and 4 synthesis forums (PDF p9); analysis rules not seen. |
| D6 Ethics / participants | 4 | 1 | 4 | 4 | Demo: oral consent with a witness for elders who read poorly, coded names, risk to elders' knowledge credit; approval not yet sought. R1: no ethics text found by keyword (OPEN; text layer may hide it). R2: two committees, consent, withdrawal (PDF p40–42), but proxy consent for cognitively impaired elders was not seen (OPEN). R3: oral and signed consent, confidentiality (PDF p44–45). |
| D7 Output → outcome → impact | 3 | 3 | 3 | 4 | Demo: full chain with named users and a CONTRIBUTORY impact, but the only outcome has no baseline, target or period, and no key-result link; R4 checks pathways against key results (PDF p31). R1: expected results and a push to policy (PDF p25). R2: guidelines and proposals for agencies (PDF p90–93), no indicators. R3: phased outputs, use plan, lead agencies and a 5-year horizon (PDF p7–8, p22–23). |
| D8 Partners and users | 4 | 5 | 3 | 3 | Demo: community co-researchers on the team, one partner group, sustainability owner and routine. R1: farmer teams as co-researchers, partner network maps (figure list PDF p16–18), public channels. R2: volunteers and caregivers as informants, not partners. R3: funded project teams as participants. |
| D9 Fund / KR alignment (vs R0) | 2 | N/A-report | N/A-report | N/A-report | Demo names focus area 4 as NEEDS_VERIFICATION; `FUND.CALL.KEY_RESULTS` NEEDS_INPUT; no output carries a `kr_id`. |
| D10 Budget and workplan (vs R0) | 4 | N/A-report | N/A-report | N/A-report | Demo: line arithmetic and weights checked (B002, W003); activity ↔ budget ↔ month links. Missing: unit-rate basis, objective links on budget lines, R0 category rules only listed. |
| D11 Epistemic honesty | 4 | 3 | 3 | 3 | Demo: 8 NEEDS_VERIFICATION markers, 5 NEEDS_INPUT, nothing above DRAFT; but simulated answers are stored as `authored_by: human` (G8), and "Submittable: yes" refers to a fictional call (G12). R1–R3 cite their figures but mark no uncertainty; R2's abstract leaves a formula's author blank (PDF p3); R2 keeps a future-tense approval sentence from its proposal (PDF p41). |

**Totals over D1–D8:** demo 24, R1 27, R2 25, R3 29 (`INSTINCT`, one
reader). D11 was designed around GrantThai's own markers, so it favours the
demo by construction; it is left out of the totals.

## 4. What the funded works do that the demo and GrantThai do not

1. **Evidence behind the need.** All three cite national or area data
   with a source. The demo's need has neither, and no rule asks for a
   SUPPORTING source on the need.
2. **Argument from literature.** Each report has a literature chapter and
   references. The demo has neither, and the output prints the gap as
   "(optional, not supplied)", not as a finding.
3. **A framework with parts.** R2 and R3 name constructs and their origin.
   The demo's framework is one sentence; nothing checks it against the
   stored constructs.
4. **Position against earlier funded work.** R3 is built on 9 funded
   projects. The demo cites nothing funded. R0 asks for this only under
   focus area 6 (p1), and GrantThai has no field for it (G1).
5. **Budget realism.** No rate is explained (15,000 per forum, 12,000
   per assistant month); forums take 37.5% of the budget; community
   co-researchers are unpaid (`compensation: ไม่มี`). B003 is not
   evaluated, so arithmetic passes and realism is unexamined.
6. **Workplan logic.** R3 ties each phase to outputs and dates (PDF p22).
   The demo's activity table has no deliverables. ACT1 and ACT2 have no
   outputs. OUT1, the survey register, is linked to ACT3, not to the survey
   activity ACT2. Ethics approval is planned for months 1–2 while
   interviews start in month 2, with no risk entry.
7. **Impact that can be observed.** R3 names who acts on each
   recommendation and over what period. The demo's only outcome happens
   "next season", after the 12-month project, with no baseline or target.
   R0 asks for outputs that can really be delivered (p12).
8. **Key-result alignment.** R4 judges pathways against key results. The
   demo honestly says NEEDS_INPUT, so it cannot compete where a funder
   looks first.

## 5. What GrantThai enforces that the funded works lacked

These are report flaws; the proposals behind them are not public.

- **Provenance per value.** Every demo value cites its transcript turn.
  R2 keeps a future-tense sentence about seeking approval "after funding",
  apparently carried over from its proposal unmarked (PDF p41).
- **Gaps stay visible.** The demo prints NEEDS_INPUT and
  NEEDS_VERIFICATION. R2's abstract drops a citation silently (PDF p3).
- **Internal consistency checks.** Budget arithmetic and activity weights
  are recomputed. R2 names one sample-size formula and uses another (PDF
  p38). R3's scope period and its phase table disagree by a month (PDF
  p21 vs p22).
- **Contradiction register.** Ten open contradictions are listed, none
  resolved silently.
- **Personal data.** Sources carry `contains_personal_data`; private ones
  print as private. R1 prints community members' names and ages in figure
  captions (figure list, PDF p14).
- **AI ceiling and disclosure.** No AI value is above DRAFT; the AI role
  is declared.

## 6. Improvements, ranked

| Rank | Change | File(s) | Why |
|---|---|---|---|
| 1 | Implement the U, P, X004 and E rules the catalog says ship in v0.2; the demo shows BLOCK 0 / REVIEW 0 partly because 31 rules are listed as not evaluated (section 1.7) | `src/grantthai/validators/engine.py`, `validators/rules.yaml`, tests | U001 would flag outputs with no `user_ids` (all four in the demo); X004 would flag claims with only ORIENTING evidence |
| 2 | New REVIEW rules: outcome without baseline, target or measurement period; outcome dated after project end; activity without deliverable or output; output linked to an activity that does not produce it | `validators/rules.yaml`, engine, `tests/` | the demo's D7 and workplan flaws pass silently |
| 3 | Make a missing need source and missing references a REVIEW finding when the bound form asks for them, not "(optional, not supplied)" | `mappings/nriis/form_profiles/ff_full_proposal@nriis-2570.yaml`, `templates/nriis_submission.md.j2` | funded works all do this; the demo got no signal |
| 4 | `authored_by: simulated` or a project-level `simulation: true`, printed in the frontmatter (G8) | `spec/common/provenance.schema.json`, `src/grantthai/core/project.py`, renderer | stops a demo passing as human-authored |
| 5 | Budget rate basis: a `rate_basis` per line, B003 evaluated against a dated profile, and a REVIEW when unpaid community co-researchers carry team share | `spec/fund/fund-profile.schema.json`, `validators/rules.yaml`, `skills/grantthai/reference/interview.md` | realism, not only arithmetic |
| 6 | Focus-area field and the conditional "work being built on" block (G1); key-result prompt in the interview | `registry/fields.jsonl`, FF form profile, `skills/grantthai/reference/interview.md` | D9 is where the demo is weakest against R0 |
| 7 | Model policy use as an output → outcome process type (R0 p13) as well as an output; add `COMMUNITY_CO_RESEARCHER` role (G5, G6) | `spec/registry/structured_fields.schema.json`, `registry/fields.jsonl` | the demo had to misfile OUT4 and use role `OTHER` |
| 8 | Thai length measure or `HUMAN_CHECK` instead of PASS (G9) | `src/grantthai/guidance/writing.py`, `guidance/writing_intent.yaml` | the checklist currently passes unmeasured Thai text |
| 9 | Generate the full per-field coverage matrix from the registry and a form profile | `tools/` script, `docs/demo/` | this file had to group rows by hand |
| 10 | Run the blind two-scorer round | `docs/demo/comparison.md` section 4 | this reading is not blind and not independent of GrantThai's design |

Ranks 1–3 are v0.2.x (rules already specified or small). Ranks 4–9 are
v0.3 candidates. Rank 10 needs people, not code.

## 7. Verdict

**Not at parity** (`INSTINCT`, one non-blind reading). On structure the
GrantThai output meets or exceeds the funded reports. It covers more of
R0's parts, links every objective to method, output and activity, checks
its own arithmetic, and is more honest about what it does not know. On
substance it is below every benchmark on need evidence, literature,
framework, key-result alignment and impact that can be observed. Those are
the parts a funder's reviewers read first.

Most of that gap is content a researcher must supply, and GrantThai
correctly refuses to invent it. The tool's share of the gap is that it
does not **say** these parts are weak: the demo passes with BLOCK 0 /
REVIEW 0. Closing ranks 1–3 would not make the demo fundable. It would
make GrantThai tell the researcher, before a reviewer does, what the
funded works already do.
