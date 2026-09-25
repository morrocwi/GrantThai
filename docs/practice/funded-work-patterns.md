# Practice shared by funded work: what 100 funded Thai final reports have in common

> **No report text is reproduced here, and no PDF is included in this
> repository.** The numbers come from the public metadata and structural
> flags in `docs/demo/corpus-100.csv`. Where a pattern rests on a page, the
> page is cited by corpus id and PDF page number, with at most a few words
> of the page's own wording. No personal data is recorded.

GrantThai is an independent, unofficial project; see `NOTICE`.

Status of this file: `DRAFT`. Tags: `VERIFIED` = computed from the CSV by
`tools/corpus/practice_stats.py`, or read on the cited PDF page;
`INSTINCT` = a judgement; `OPEN` = not settled.

Thai version: [`funded-work-patterns.th.md`](funded-work-patterns.th.md).

## 1. The question

The founder asked GrantThai to take the 100 funded final reports, pull out
what they share *significantly*, and use it to strengthen GrantThai's
practice guidance. This file answers that question. It does three things:

1. It sets a threshold for "significant" before looking at the numbers
   (§2) and applies it with a script (§3).
2. It reads 8 documents closely to describe *how* funded work writes the
   parts that most documents share (§4).
3. It says what changed in GrantThai as a result (§5), and what the
   corpus cannot show (§6).

## 2. Method

**Corpus.** The 100 documents in `docs/demo/corpus-100.md`: 83 from the
Health Systems Research Institute repository ("HSRI" below) and 17 from the
Prince of Songkla University repository ("PSU" below). All are
completed-work documents (97 technical reports, 3 forum proceedings). None
is a proposal. Year bands (Buddhist Era): ≤2559 (n=31), 2560–62 (n=30),
2563–68 (n=39).

**Tiers.** Fixed before the table was computed:

| Tier | Test | What GrantThai does with it |
|---|---|---|
| **CORE** | present in ≥70 of the 100 **and** ≥50% in each source subset (HSRI and PSU), so no single source carries it | guidance, and a REVIEW rule where no existing rule covers it |
| **CONTEXTUAL** | 40–69% overall, or concentrated in one source (a proxy for funder and discipline) | guidance, tied to the context where it holds; no rule |
| **EMERGING** | below 40% overall, but rising across the three year bands: the 2563–68 band is the highest and at least 15 points above the ≤2559 band | guidance marked as emerging; no rule |
| RARE | below 40% and not rising | no practice claim |
| NO_CLAIM | proposal-only items (budget, workplan, key results, TRL, SRL) | no practice claim: a final report drops them, so their absence says nothing about a proposal |

"Report" in the tier column marks a pattern that belongs to the report
stage (results, discussion, appendix, acknowledgement). It has no proposal
field, so it supports guidance only.

**Script.** `python tools/corpus/practice_stats.py` reads only
`docs/demo/corpus-100.csv` and prints the table in §3.
`tests/test_practice_patterns.py` recomputes it and fails if a count or a
tier in `guidance/writing_intent.yaml` or `validators/rules.yaml` drifts
from the CSV.

**Detection limits (`VERIFIED`).**

- Detection is **heading-based** (`tools/corpus/corpus_extract.py`). A part
  written inside running text is missed. Research questions appear as a
  heading in 4% of documents (reports usually state their aims as
  objectives); ethics appears as a heading in 6%, but as a heading, an
  ethics-committee phrase or an informed-consent phrase in 29%. Both are
  undercounted.
- The objective-item count counts sub-bullets too, so it is noisy
  (`INSTINCT`). FWP-03 uses only "two or more items", which is robust to
  that noise.
- References are undercounted where the list is placed after the appendix
  (HSRI-073 counts 0 but cites numbered sources on p73).
- The two sources differ in size (83 and 17). The PSU subset is small: one
  document moves its percentage by about 6 points.
- **These are final reports.** A proposal-only part (budget, workplan, key
  results, TRL, SRL) gets no practice claim from this corpus in either
  direction.

## 3. Evidence table

`VERIFIED`: `python tools/corpus/practice_stats.py` on
`docs/demo/corpus-100.csv` (n = 100; HSRI 83, PSU 17). "Trend" gives the
percentage in each year band.

| Id | Pattern | N/100 | HSRI % | PSU % | Trend (≤2559 / 2560–62 / 2563–68) | Tier | GrantThai field_ids | What to do |
|---|---|---:|---:|---:|---|---|---|---|
| FWP-01 | Background / rationale section | 91 | 89 | 100 | flat (84 / 90 / 97) | CORE | `CORE.NARRATIVE.RATIONALE`, `CORE.RESEARCH.PROBLEM`, `CORE.RESEARCH.NATIONAL_NEED` | Required field; S001 (BLOCK) and R001 already apply. Guidance: problem with a sourced figure. |
| FWP-02 | Objectives section | 82 | 80 | 94 | flat (74 / 87 / 85) | CORE | `CORE.RESEARCH.OBJECTIVES`, `CORE.NARRATIVE.OBJECTIVES` | Required field; S001 already applies. Keep objectives as their own list. |
| FWP-03 | Objectives written as a numbered list (>= 2 items) | 77 | 76 | 82 | flat (71 / 77 / 82) | CORE | `CORE.RESEARCH.OBJECTIVES`, `CORE.NARRATIVE.OBJECTIVES` | **Rule FW002** (REVIEW). Number objectives; reuse the numbers in method and analysis. |
| FWP-04 | Method section | 80 | 81 | 76 | rising (68 / 77 / 92) | CORE | `CORE.NARRATIVE.METHOD`, `METHOD.PLAN.DESIGN` | Required fields; S001 already applies. Say who/what, how data are collected, how analysed. |
| FWP-05 | Objectives and method both present | 74 | 73 | 76 | rising (65 / 73 / 82) | CORE | `CORE.RESEARCH.OBJECTIVES`, `METHOD.PLAN.DESIGN` | R004/R005 already link each objective to an RQ and a method. Guidance: a design table. |
| FWP-06 | Reference list | 78 | 78 | 76 | rising (71 / 70 / 90) | CORE | `CORE.NARRATIVE.REFERENCES`, `CORE.NARRATIVE.THEORY` | **Rule FW001** (REVIEW). A theory or foundations box needs a reference list. |
| FWP-07 | Results section | 85 | 83 | 94 | rising (71 / 83 / 97) | CORE (report) | (none: report-stage) | Report stage: no proposal field, no rule. |
| FWP-08 | Discussion / conclusion section | 90 | 89 | 94 | flat (87 / 87 / 95) | CORE (report) | (none: report-stage) | Report stage: no rule. Plan now how findings will be set against prior studies. |
| FWP-09 | Literature review section | 64 | 65 | 59 | rising (55 / 60 / 74) | CONTEXTUAL | `CORE.NARRATIVE.THEORY`, `CORE.RESEARCH.THEORETICAL_FOUNDATIONS`, `CORE.RESEARCH.GAP` | Guidance: numbered topic list mirroring objectives; end with related studies. |
| FWP-10 | Method sub-parts (population, instruments, data collection, analysis, or sample-size basis) | 66 | 70 | 47 | rising (52 / 60 / 82) | CONTEXTUAL | `CORE.NARRATIVE.METHOD`, `METHOD.PLAN.POPULATION`, `METHOD.PLAN.SAMPLE`, `METHOD.PLAN.INSTRUMENTS`, `METHOD.PLAN.DATA_COLLECTION`, `METHOD.PLAN.ANALYSIS` | Guidance only (PSU 47%): use the sub-parts that fit the design. |
| FWP-11 | Abstract (Thai or English) | 64 | 59 | 88 | rising (35 / 63 / 87) | CONTEXTUAL | `CORE.NARRATIVE.SUMMARY` | Guidance: a stand-alone summary. |
| FWP-12 | Keywords | 50 | 47 | 65 | rising (29 / 47 / 69) | CONTEXTUAL | `CORE.GENERAL.KEYWORDS_TH`, `CORE.GENERAL.KEYWORDS_EN` | Guidance: keywords naming object, group or site, and method. |
| FWP-13 | Recommendations of any kind (section or policy phrase) | 59 | 67 | 18 | rising (42 / 40 / 87) | CONTEXTUAL | `RESULTS.CHAIN.UTILIZATION_DESC`, `RESULTS.CHAIN.USERS` | Guidance (HSRI-concentrated): name the agency or level expected to act. |
| FWP-14 | Policy-recommendation phrase | 47 | 54 | 12 | rising (32 / 33 / 69) | CONTEXTUAL | `RESULTS.CHAIN.UTILIZATION_DESC`, `RESULTS.CHAIN.USERS` | Guidance (HSRI-concentrated): actor + action per recommendation. Existing P/U rules cover policy claims. |
| FWP-15 | Outputs, expected benefit or utilization section | 58 | 60 | 47 | rising (45 / 43 / 79) | CONTEXTUAL | `RESULTS.CHAIN.OUTPUTS`, `RESULTS.CHAIN.BENEFIT_SUMMARY`, `RESULTS.CHAIN.UTILIZATION_DESC` | Guidance: outputs by type, with count and verification. |
| FWP-16 | Strategy / national-plan wording | 58 | 65 | 24 | flat (71 / 40 / 62) | CONTEXTUAL | `CORE.RESEARCH.NATIONAL_NEED`, `CORE.GENERAL.MASTER_PLAN` | Guidance only when the call asks for alignment. |
| FWP-17 | Data-analysis sub-section | 44 | 48 | 24 | rising (29 / 30 / 67) | CONTEXTUAL | `METHOD.PLAN.ANALYSIS` | Guidance: analyses numbered in objective order. |
| FWP-18 | Population / sample sub-section | 38 | 46 | 0 | rising (23 / 37 / 51) | EMERGING | `METHOD.PLAN.POPULATION`, `METHOD.PLAN.SAMPLE` | Guidance: population before sample, with site rationale. |
| FWP-19 | Sample-size basis stated (formula or named method) | 35 | 40 | 12 | rising (26 / 20 / 54) | EMERGING | `METHOD.PLAN.SAMPLE` | Guidance: sample-size method with every parameter. |
| FWP-20 | Data-collection sub-section | 33 | 35 | 24 | rising (23 / 30 / 44) | EMERGING | `METHOD.PLAN.DATA_COLLECTION` | Guidance: who collects what, from whom, with which instrument. |
| FWP-21 | Instruments sub-section | 24 | 29 | 0 | flat (29 / 17 / 26) | RARE | `METHOD.PLAN.INSTRUMENTS` | No practice claim (rare as a heading). R008 already checks instruments name a construct. |
| FWP-22 | Conceptual framework section | 31 | 37 | 0 | rising (23 / 20 / 46) | EMERGING | `CORE.NARRATIVE.FRAMEWORK` | Guidance: a diagram whose boxes the instruments measure. |
| FWP-23 | Expert or stakeholder validation of instruments or draft proposals | 32 | 35 | 18 | rising (29 / 13 / 49) | EMERGING | `METHOD.PLAN.QUALITY` | Guidance: how instruments or drafts are checked. |
| FWP-24 | Ethics (section, committee approval or informed consent) | 29 | 34 | 6 | rising (23 / 23 / 38) | EMERGING | `METHOD.PLAN.ETHICS` | Guidance: participant protection inside the method. Undercounted. |
| FWP-25 | Limitations of the study stated | 15 | 18 | 0 | rising (6 / 3 / 31) | EMERGING | `METHOD.PLAN.QUALITY` | Guidance: known limits of data sources and design. |
| FWP-26 | Research users named | 16 | 18 | 6 | rising (6 / 13 / 26) | EMERGING | `RESULTS.CHAIN.USERS`, `RESULTS.CHAIN.BENEFICIARIES` | Guidance: user agencies linked to outputs. |
| FWP-27 | Operational definitions | 19 | 20 | 12 | rising (13 / 7 / 33) | EMERGING | `CORE.RESEARCH.CONSTRUCTS` | No guidance added yet (constructs already carry definitions). |
| FWP-28 | Triangulation named | 11 | 13 | 0 | rising (0 / 7 / 23) | EMERGING | `METHOD.PLAN.QUALITY` | No guidance added yet. |
| FWP-29 | Scope section | 40 | 41 | 35 | flat (35 / 37 / 46) | CONTEXTUAL | `CORE.RESEARCH.BOUNDARY_CONDITIONS` | No guidance added yet (flat). |
| FWP-30 | Executive summary | 42 | 46 | 24 | flat (39 / 37 / 49) | CONTEXTUAL | `CORE.NARRATIVE.SUMMARY` | No guidance added (summary covered by FWP-11). |
| FWP-31 | Research question as a heading | 4 | 5 | 0 | flat (6 / 0 / 5) | RARE | `CORE.RESEARCH.RQ.PRIMARY` | No practice claim. Keep the RQ field: it anchors R003/R004. Undercounted: aims are usually written as objectives. |
| FWP-32 | Hypothesis section | 5 | 4 | 12 | flat (0 / 3 / 10) | RARE | `CORE.RESEARCH.HYPOTHESES` | No practice claim. |
| FWP-33 | Appendix | 66 | 64 | 76 | rising (48 / 73 / 74) | CONTEXTUAL (report) | `DOC.ATTACHMENTS.DOCUMENTS` | Report stage: no rule. |
| FWP-34 | Acknowledgement | 62 | 58 | 82 | rising (42 / 67 / 74) | CONTEXTUAL (report) | (none: report-stage) | Report stage: no rule. |
| FWP-35 | Budget section or amount | 52 | 59 | 18 | flat (61 / 47 / 49) | NO_CLAIM | `BUDGET.PLAN.ITEMS`, `BUDGET.PLAN.TOTAL` | No claim: proposal-stage item dropped from reports. |
| FWP-36 | Workplan / timeline section | 31 | 37 | 0 | rising (23 / 20 / 46) | NO_CLAIM | `WORK.PLAN.ACTIVITIES` | No claim: proposal-stage item dropped from reports. |
| FWP-37 | Key results, TRL or SRL wording | 4 | 4 | 6 | flat (0 / 0 / 10) | NO_CLAIM | `CORE.ALIGNMENT.STATEMENT`, `READY.TRL.CURRENT`, `READY.SRL.CURRENT` | No claim: terms postdate most reports; outside this corpus. |

**Reading the table (`INSTINCT`).** Six proposal-relevant patterns are
CORE: a background, a separate objectives section, objectives written as
a numbered list, a method section, objectives and method together, and a
reference list. Two further CORE patterns (results, discussion) belong to
the report stage. Almost everything else rises over time: reports from
2563 on carry more literature review, analysis, sample-size basis,
framework, recommendations and stated limitations than older reports. The
funded record is becoming more structured, so a proposal written today
should expect a reader who looks for those parts.

## 4. How strong funded work writes: 8 documents read closely

The 8 documents were chosen to spread across source (5 HSRI, 3 PSU), year
band (1 from ≤2559, 3 from 2560–62, 4 from 2563–68) and design (survey,
mixed-method policy study, multi-site clinical study, device evaluation,
cost-utility analysis, animal feeding trial, field ecology, household
survey with focus groups). Pages are PDF pages. Every observation below
was read on the page cited (`VERIFIED`); the summary of each pattern is a
judgement (`INSTINCT`).

| Doc | Year (BE) | Field and design | PDF pages |
|---|---|---|---|
| HSRI-010 | 2557 | stroke care: time to treatment, cross-sectional survey | 57 |
| HSRI-041 | 2565 | nursing workforce policy, mixed methods | 168 |
| HSRI-047 | 2566 | hip-fracture care, multi-site indicators and interviews | 108 |
| HSRI-073 | 2562 | diagnostic imaging, cost-utility and budget impact | 283 |
| HSRI-080 | 2565 | 3D-printed cranial implant, device testing and economic evaluation | 138 |
| PSU-015 | 2561 | seagrass carbon storage, field ecology and remote sensing | 71 |
| PSU-026 | 2562 | treated palm fronds as goat feed, Latin-square feeding trial | 75 |
| PSU-039 | 2563 | rubber cooperatives in a price crisis, household survey and focus groups | 44 |

### 4.1 Objectives are numbered, and the numbers come back

Seven of the 8 list their objectives as numbered items, one aim per
item, most opening with "เพื่อ" [in order to] and a verb (HSRI-010 p13;
HSRI-041 p19; HSRI-047 p26; HSRI-073 p21; HSRI-080 p13; PSU-015 p10;
PSU-026 p12). HSRI-041 first states one general objective and then three
specific ones (p19); HSRI-073 splits one objective into three numbered
sub-items, one per clinical indication (p21). The eighth, PSU-039, is a
short report that states its aims in one sentence of its summary (p3).
The strongest documents reuse the numbers later: HSRI-010 numbers its
two analyses in the same order as its two objectives, so analysis 1
answers objective 1 (p13, p24). HSRI-047 points objective 1 straight at
an indicator table, "ตารางตัวชี้วัดที่ 1.2" [indicator table 1.2] (p26).
The last objective is often "develop policy recommendations"
(HSRI-041 p19, HSRI-047 p26), which makes the recommendations chapter an
answer to a stated objective rather than an add-on.

*For a GrantThai proposal:* number the objectives, keep the numbers when
the method and analysis refer back to them (FWP-03, rule FW002), and let
the objective items carry their method and output links (rules R004, R005).

### 4.2 The literature review is organised by the questions, not by authors

Three documents open the review with a numbered list of the topics it will
cover (HSRI-010 p14; HSRI-041 p23; PSU-026 p14). The list follows the
logic of the study: in HSRI-010 it runs from the disease, to its care, to
the factors that delay treatment, and that last topic is objective 2
(p14, p13). In HSRI-041 the middle topics are the three parts of the
framework: producing, distributing and retaining nurses (p20, p23). Each
list ends with a block of "งานวิจัยที่เกี่ยวข้อง" [related studies]
(HSRI-041 p23; PSU-026 p14). The discussion later returns to those
studies and says whether the new findings are "สอดคล้อง" [consistent] or
"ขัดแย้ง" [contradicting] (PSU-039 p43), or "แตกต่างจาก" [differ from]
them (HSRI-010 p45–46).

*For a GrantThai proposal:* make the theory box and theoretical
foundations a short numbered topic list in objective order, cite every
prior finding, and let the gap come out of the related-studies block
(FWP-09, FWP-06, rule FW001).

### 4.3 The method chapter answers who, with what, how, and how checked

The survey and mixed-method reports use the same sequence of sub-parts:
population and sample, site, instrument, instrument quality, data
collection, analysis. HSRI-010 gives the sample-size formula with every
parameter and the resulting number (p21–22), then the three parts of its
questionnaire (p22), then a quality check by three experts with a content
validity index and a pilot with 20 patients (p23), then numbered analyses
(p24). PSU-039, a short report, compresses the same content into numbered
steps, each naming who, how many and how, and stratifies its sample by
cooperative size with a cited reason (p6). The experimental reports
replace population and instruments with the design, the treatments and
the duration (PSU-026 p36). Ethics sits inside the method, not in a
separate chapter: consent, the right to withdraw, confidentiality and
data retention (HSRI-041 p56; PSU-039 p7; HSRI-010 p23 for consent). This
is one reason heading detection undercounts ethics.

*For a GrantThai proposal:* fill `METHOD.PLAN.*` in that order, give the
sample-size basis with its parameters, say how the instruments will be
checked, and write participant protection into the method (FWP-04,
FWP-10, FWP-19, FWP-23, FWP-24).

### 4.4 Results lead to discussion, then limitations, then recommendations

The chapter order is stable: results, then discussion against prior
studies, then limitations, then recommendations. HSRI-047 shows the full
sequence in one chapter: discussion, then "ข้อจำกัดของการศึกษาและอุปสรรคในการทำวิจัย"
[limitations of the study and obstacles to the research] (p87), which
names the reliability of each data source and how the team adapted data
collection during the epidemic, then policy recommendations (p88).
Limitations are still uncommon (15/100) but rising (6% to 31%).

*For a GrantThai proposal:* a proposal has no results, but it can say now
which data sources have known limits and how the analysis will handle them
(`METHOD.PLAN.QUALITY`, FWP-25).

### 4.5 Policy recommendations name who should act

Where recommendations exist, the strong ones name the actor first.
HSRI-041 groups its policy recommendations by the three parts of its
framework (p7), and in the full chapter opens each numbered item with the
agencies responsible (p122). HSRI-073 groups them by result and attaches a figure to each:
a target price and a budget impact (p167). HSRI-080 names the payer
agencies as "หน่วยงานผู้ใช้ประโยชน์จากงานวิจัย" [research-user agencies]
already in its introduction (p14). This is CONTEXTUAL, not CORE: policy
wording is concentrated in the HSRI reports (54% against 12%).

*For a GrantThai proposal:* when the project aims at policy or practice,
name the agency or level expected to act and link it to an output
(`RESULTS.CHAIN.USERS`, `RESULTS.CHAIN.UTILIZATION_DESC`; FWP-13, FWP-14,
FWP-26).

### 4.6 Outputs and benefits are typed, counted and verifiable

HSRI-080 splits expected benefits into policy and commercial ones (p13–14).
PSU-015 lists its outputs by type (publications, conference
presentations, technology transfer, one policy proposal), each with a
count and the evidence that it exists, such as a DOI or a named event
(p67–68). HSRI-047 lists numbered outcome indicators (p21).

*For a GrantThai proposal:* write outputs by type with a count and how
each will be shown to exist (`RESULTS.CHAIN.OUTPUTS`, FWP-15).

## 5. What changed in GrantThai

**Rules (REVIEW only; none is BLOCK).** A rule is added only for a CORE
pattern that no existing rule already covers.

| Rule | Pattern | Fires when | Evidence |
|---|---|---|---|
| FW001 | FWP-06 reference list | `CORE.NARRATIVE.THEORY` or `CORE.RESEARCH.THEORETICAL_FOUNDATIONS` has content but `CORE.NARRATIVE.REFERENCES` is empty or absent | 78/100 (HSRI 78%, PSU 76%) |
| FW002 | FWP-03 numbered objectives | two or more objective items, but the objectives narrative shows fewer than two item numbers (1) 2), (1) (2), 1. 2., ข้อ 1; Thai digits count) | 77/100 (HSRI 76%, PSU 82%) |

The other CORE patterns are already checked: FWP-01, FWP-02 and FWP-04 by
S001 (their fields are required) and R001 (the problem needs a source);
FWP-05 by R004 and R005 (each objective links to a research question and
a method). FWP-07 and FWP-08 are report-stage.

Rules suggested in the brief but **not** added, because the evidence does
not reach CORE:

- method sub-parts (population, instruments, analysis): FWP-10 is 66/100
  and only 47% in PSU; FWP-17, FWP-18 and FWP-21 are lower still;
- a policy or user-level recommendation: FWP-13 and FWP-14 are
  CONTEXTUAL (HSRI-concentrated); the existing P and U rule families cover
  policy claims and users;
- stated limitations: FWP-25 is EMERGING (15/100).

These are guidance, not rules.

**Guidance.** `guidance/writing_intent.yaml` has a `practice:` list on 25
fields (32 entries) with the pattern id, the evidence ("N/100 funded
reports (corpus-100)"), the tier, the context for a non-CORE pattern,
advice in English and Thai, what not to do, and the deep-read pages.
`grantthai explain <FIELD_ID>` shows them.

**Skill.** `skills/grantthai/SKILL.md` and
`skills/grantthai/reference/interview.md` now ask for numbered objectives
linked to methods, the scope of the literature, population, instruments
and analysis, ethics, and who receives the recommendations, with the
corpus count behind each question. `skills/grantthai/reference/rules-th.md`
explains FW001 and FW002 in Thai.

**Demo.** The fictional demo now shows one REVIEW finding, FW001: its theory
box says it has no references yet and its reference list is empty. The
demo is left as it is, so the finding stays visible.

## 6. Limits

- The corpus leans toward health systems research (83 of 100). PSU stands
  in for science, engineering, agriculture and social science, with only 17
  documents.
- Source is a proxy for funder and discipline. It is not coded per document.
- No document from the national research funding agency's e-Library is
  included (see `docs/demo/comparison.md`, note of 2026-09-25), so reports
  written to key-result and readiness-level templates are missing.
- Heading-based detection misses parts written in running text (§2).
- A pattern shared by funded reports is a description of funded work, not
  a cause of funding. Unfunded work may share it too; this corpus has no
  unfunded comparison group (`OPEN`).
- Final reports are not proposals. The patterns apply to the parts a
  proposal and a report share (problem, objectives, literature, method,
  intended use). Budget, workplan, key results, TRL and SRL get no claim.
- The advice wording (English and Thai) is GrantThai's own, `DRAFT`. It is
  not the wording of any form or fund.

## 7. Reproduce

```bash
python tools/corpus/practice_stats.py                 # the table in §3 (markdown)
python tools/corpus/practice_stats.py --format tsv    # the same, tab-separated
python -m pytest -q tests/test_practice_patterns.py   # counts and tiers match the CSV
```
