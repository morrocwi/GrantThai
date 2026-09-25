# Demo comparison: a fictional proposal set against real, funded, public work

> **The demo is FICTIONAL.** `examples/demo-seedbank/` was produced by an AI assistant that played both the interviewer and a simulated researcher (`docs/demo/transcript-seedbank.md`). The real works below are used **only for structure and quality comparison**. Nothing from them is copied into the demo, and no real person's knowledge is represented by it.

GrantThai is an independent, unofficial project; see `NOTICE`.

Status of this file: `DRAFT`. Section 2 (the structural matrix) and the
facts about sources are checked as marked (`VERIFIED` = read in the
document by the author of this file; `relayed` = taken from the v0.2
research notes and not re-read). **Section 4 (quality scores) is
deliberately empty.** The maker of the demo must not score it. The scores
are to be filled by two scorers who did not write the demo, working on a
blind copy. Any score, including one from an AI scorer, is a reader's
reading, not a validation; an AI scorer's scores stay `DRAFT`.

## 1. What is compared, and why it is split in two

No funded **full proposal** was found in public in full (relayed, from
the v0.2 research). What is public are funded **final reports**. A report
shares the research core with a proposal (problem, objectives, framework,
method, ethics, results logic) but has none of the proposal-only parts
(budget lines, month-by-month workplan, key-result alignment, TRL/SRL). So:

- **Research-core dimensions (D1–D8, D11):** demo vs the funded reports R1–R3.
  A dimension a final report would not contain is marked `N/A-report`,
  never scored 1.
- **Proposal-only dimensions (D9, D10):** demo vs the items the public blank
  form R0 asks for. R0 is a form, not a funded work.

### Sources

Cited by title (as printed on the cover), first author, and contract or
handle only. No PDF is committed. No text is reproduced beyond fragments of
at most 15 words. No ethics approval numbers, team rosters or other
personal data are copied. sha256 values were computed on the downloaded
files (`VERIFIED`, 2026-09-25). Page counts were checked with `pdfinfo` on
the files with these hashes by an independent reviewer (2026-09-25).
**Access and licence status is `relayed` from the v0.2 research notes and
is `OPEN`:** a re-check on 2026-09-25 could not re-open the landing pages
(one returned a login page, one a server error). A human reader must open
each landing page and record its terms statement, URL and date before
this file is pushed. Nothing here depends on a licence: sources are cited,
not reproduced, and quotes are at most 15 words.

| Id | Title (as printed) | First author (public) | Funder / contract or handle | Type, PDF pages | Access and licence | sha256 |
|---|---|---|---|---|---|---|
| R0 | Blank Fundamental Fund full-proposal form, 2570 cycle (title as printed: `SD-5` in `docs/sources.md`) | none | public download page of nriis.go.th; `SD-5` in `docs/sources.md` | blank form, 52 | public; no licence statement: cite only | `f212e61beb19aea74b203bdc80d68d935f508006358fa4bf92d50adee90621ec` |
| R1 | การสังเคราะห์รูปแบบการสร้างความเข้มแข็งของชุมชนบนฐานการทำนาจังหวัดนราธิวาส | พรพันธุ์ เขมคุณาศัย | Thailand Research Fund, contract RDG60S0001 (January 2563) | final report, 139 | e-Library of Thailand Science Research and Innovation, full text, no login; only a copyright line, no licence (relayed, OPEN): treat as all rights reserved, short quotes only | `609c78be14b7fa0a05ab09d3a99473baddbdd3f01b6c21f1e1a63fcb4c4a2712` |
| R2 | การดูแลผู้สูงอายุที่มีภาวะพึ่งพิงแบบบูรณาการโดยการมีส่วนร่วมของชุมชนเพื่อเตรียมรับการระบาดซ้ำของโรคติดเชื้อไวรัสโคโรนา 2019 | สุพิชญา หวังปิติพาณิชย์ | Health Systems Research Institute, handle `hdl.handle.net/11228/5712` | final report, 130 | the institute's repository; the item's licence file is an unedited placeholder, so no licence is granted (relayed, OPEN): treat as all rights reserved | `25874ac8c86d97af2782f32df5a591724dda6937450c07d5bec0d402da84faa8` |
| R3 | โครงการการสังเคราะห์งานวิจัยภายใต้กรอบการวิจัยการพัฒนาคน ชุมชน และสังคมไทย | สมจิต แดนสีแก้ว | National Research Council of Thailand and Thailand Research Fund, contract RDG5840049 (May 2561) | final report, 101 | same terms as R1 | `054e1678a577a626691b534a00e6ed11e8efc37a3d6776f35fe6e1c0db79c0ec` |
| R4 (withdrawn; not used) | Outcome and impact evaluation of a large research and innovation programme: Genomics Thailand (English description; the Thai cover title names the funder by acronym) | not recorded | Thailand Science Research and Innovation, contract ORG65F3010 | evaluation report, 137 (`pdfinfo`, independent reviewer) | relayed, OPEN; withdrawn as the D7 anchor until its terms and contents are re-checked | `6b0408b1e93e18146bf31858c7f7292ddfea4e1efb95223a6bc15d5a7b04cc0a` |

One repository was excluded (relayed): its full texts need membership,
allow non-commercial use only, are watermarked with the downloader's name
and expire after 15 days. That does not fit a public repository.

## 2. Structural matrix: which parts each document has

Presence only, not quality. R0 pages are `VERIFIED` (form text, PDF pages).
R1 presence is `VERIFIED` from its table of contents on PDF p8 (it lists
the chapter-1 sections with printed page numbers). R2 and R3 presence is
relayed, with the PDF pages where the section heading word occurs in the
text layer (`VERIFIED` keyword hits, not a reading). The demo column is
the GrantThai field and the status the demo build shows.

| Part | R0 form item | R1 | R2 | R3 | Demo (field: status) |
|---|---|---|---|---|---|
| Significance / need / problem | part 2 item 2, p3 | ch. 1, TOC p8 | ch. 1 (relayed) | ch. 1 (relayed) | `CORE.RESEARCH.NATIONAL_NEED`, `.PROBLEM`: DRAFT (simulated persona) |
| Objectives | part 2, p3 | ch. 1, TOC p8 | 3, PDF p19 (`VERIFIED` in the DRAFT reading) | ch. 1 (relayed) | `CORE.RESEARCH.OBJECTIVES`: DRAFT, 3 items, each linked to the RQ, a method phase and an output |
| Research questions | not a separate item (OPEN) | ch. 1, TOC p8 | OPEN: not found (relayed) | ch. 1 (relayed) | `CORE.RESEARCH.RQ.PRIMARY`, `.SECONDARY`: DRAFT |
| Sites / target groups | part 3, p6 (research sites) | ch. 1, TOC p8 | 3 informant groups (relayed) | not applicable (synthesis) | `GEO.AREA.RESEARCH_SITES`, `METHOD.PLAN.SAMPLE`: DRAFT |
| Conceptual framework | part 2, p3 | p9, p38 (keyword) | p9, p20, p31 (keyword) | p13, p20, p59–60 (keyword) | `CORE.NARRATIVE.FRAMEWORK`: DRAFT, one sentence |
| Literature / theory | part 2, p3 | ch. 2, TOC p8 | ch. 2 (relayed) | ch. 2 (relayed) | `CORE.NARRATIVE.THEORY`: DRAFT, no references; `CORE.PRIORKNOWLEDGE.PK2`, `CORE.NARRATIVE.REFERENCES`: NEEDS_INPUT |
| Method | part 2, p3 | PAR (p23 keyword) | ch. 3 (relayed) | ch. 3 (relayed) | `METHOD.PLAN.*`: DRAFT, PAR in 3 cycles |
| Ethics | part 3 (standards), relayed | OPEN: no hit in full-text search of the final report (terms in the DRAFT reading, D6) | p41–42 (keyword) | several hits (keyword) | `METHOD.PLAN.ETHICS`: DRAFT; `COMP.STANDARD.HUMAN`: DRAFT, NEEDS_VERIFICATION |
| Expected results / indicators | part 4, p12 | ch. 1, TOC p8; indicators p27–31 (keyword) | guidelines and policy proposals, PDF p90–93 (`VERIFIED` in the DRAFT reading; replaces the earlier relayed "absent") | relayed: present | `RESULTS.CHAIN.OUTPUTS`, `.OUTCOMES`: DRAFT |
| Policy proposals | 10 output types in the annex (relayed) | ch. 5 (relayed) | p43 and ch. 5 (keyword and relayed) | p19–24, p85 (keyword) | `OUT4` "policy proposal": output type NEEDS_VERIFICATION (no dedicated type) |
| Output → outcome → impact | part 4, p12 | partial (relayed) | partial (relayed) | partial (relayed) | `RESULTS.CHAIN.OUTCOME_PROCESS`, `.OUTCOMES`, `.IMPACTS` (claim strength CONTRIBUTORY): DRAFT |
| Budget in categories | part 3, p9 | N/A-report | N/A-report | N/A-report | `BUDGET.PLAN.ITEMS` BI1–BI6, total 480,000 (arithmetic checked by B002); FF category rules listed, not evaluated |
| Workplan by month | part 3, p6 | N/A-report | N/A-report | N/A-report | `WORK.PLAN.ACTIVITIES` ACT1–ACT4, weights sum to 100 (W003) |
| Focus area / fund alignment | part 1, p1 | N/A-report | N/A-report | N/A-report | `CORE.GENERAL.RESEARCH_ISSUE`, `.PLAN`: DRAFT, NEEDS_VERIFICATION; `CORE.ALIGNMENT.FUND_SELECTION`, `FUND.CALL.KEY_RESULTS`: NEEDS_VERIFICATION; `CORE.ALIGNMENT.STATEMENT`: absent |
| Summary (at most 3000 words) | part 2 item 1, p3 | abstract (TOC p8) | abstract (relayed) | abstract (relayed) | `CORE.NARRATIVE.SUMMARY`: AI draft, **not adopted** by the persona |
| Keywords (at most 5) | part 2 item 9, p3 | N/A-report | N/A-report | N/A-report | `KEYWORDS_TH`: 4; `KEYWORDS_EN`: AI draft, not adopted |

### Demo value status (computed from `examples/demo-seedbank/project.yaml`)

- 59 records: 54 `DRAFT`, 5 `NEEDS_INPUT`; 8 `NEEDS_VERIFICATION` markers; no record above `DRAFT`; no `SOURCE` record.
- Authored by: 53 "human" (meaning the **simulated persona**; see section 5, gap G8), 4 AI drafts the persona adopted, 2 AI drafts not adopted.
- 51 of the 122 registry fields have a value. `grantthai validate`: BLOCK 0, REVIEW 0, INFO 31 (as of 2026-09-25). BLOCK 0 is structure and links only; it says nothing about quality.

## 3. Rubric (for the scorers)

Scale 1–5. Score only what both documents contain. Every score carries a
page (or field id for the demo) and an evidence fragment of at most 15
words. Scorers work on a blind copy of the demo build with the FICTIONAL
banners, the title and the project id removed.

| # | Dimension | 1 | 3 | 5 | Compared with |
|---|---|---|---|---|---|
| D1 | Problem and need | generic, no context | local problem with some data | need, problem and who is affected, each with a cited source | R1–R3 |
| D2 | Gap | missing | "little research" | specific gap against prior work, incl. funded projects | R1–R3 |
| D3 | RQ ↔ objectives | either missing | both, loosely linked | each objective answers a named RQ, numbered one to one | R1–R3 |
| D4 | Framework / theory | missing | theory named | framework with constructs, relations and cited origin | R1–R3 |
| D5 | Method fit | not stated | design named | design, sample, instruments, analysis, quality each trace to an objective | R1–R3 |
| D6 | Ethics / participants | missing | mentioned | consent, risk and approval route per participant group | R1–R3 |
| D7 | Output → outcome → impact | outputs only | outputs + outcomes | full pathway with users, beneficiaries and mechanism | R1–R3 |
| D8 | Partners and users | none | listed | named roles, co-research, plan for use after the project | R1–R3 |
| D9 | Fund / KR alignment | none | plan named | focus area, national plan and KR each linked to outputs | R0 only |
| D10 | Budget and workplan | missing | totals only | line arithmetic, R0 category rules, activity ↔ budget ↔ month links | R0 only |
| D11 | Epistemic honesty (GrantThai-specific) | invented facts | some gaps marked | every gap `NEEDS_INPUT`/`NEEDS_VERIFICATION`, sources cited, nothing AI-written above `DRAFT` | all |

## 4. Scores (PENDING, not by the maker)

One non-blind AI reading exists as a separate `DRAFT`:
`docs/demo/scored-reading-draft.md` (Thai: `scored-reading-draft.th.md`).
It is not one of the two blind scores, validates nothing, and does not
fill this table. The blind round is still pending.

| # | Demo (Scorer A) | Demo (Scorer B) | R1 | R2 | R3 | Evidence (page or field; ≤15-word fragment) |
|---|---|---|---|---|---|---|
| D1 | PENDING | PENDING | PENDING | PENDING | PENDING | |
| D2 | PENDING | PENDING | PENDING | PENDING | PENDING | |
| D3 | PENDING | PENDING | PENDING | PENDING | PENDING | |
| D4 | PENDING | PENDING | PENDING | PENDING | PENDING | |
| D5 | PENDING | PENDING | PENDING | PENDING | PENDING | |
| D6 | PENDING | PENDING | PENDING | PENDING | PENDING | |
| D7 | PENDING | PENDING | PENDING | PENDING | PENDING | |
| D8 | PENDING | PENDING | PENDING | PENDING | PENDING | |
| D9 | PENDING | PENDING | N/A-report | N/A-report | N/A-report | vs R0 |
| D10 | PENDING | PENDING | N/A-report | N/A-report | N/A-report | vs R0 |
| D11 | PENDING | PENDING | PENDING | PENDING | PENDING | |

What the maker expects the scorers to find, stated in advance so it can
be checked against their blind scores (`INSTINCT`, not a score): D2 and D4
weak (no literature, no references, gap built on one fictional event), D9
weak (no key results, alignment left `NEEDS_VERIFICATION`), D3, D5, D10
and D11 comparatively strong because GrantThai's links and arithmetic force
them.

## 5. What GrantThai could not represent: v0.3 candidates

From the v0.2 research (items G1–G7; items G1 and G3 are corrected here
against the SD-5 page text) and from running the demo (G8–G12).

| # | Gap | Evidence | Candidate change |
|---|---|---|---|
| G1 | Fund focus areas (1–6, at most 2) have no field; the "work being built on" block (prior result, owner, year, TRL/SRL) applies only when focus area 6 is chosen | R0 p1 (`VERIFIED`) | a `CORE.ALIGNMENT.FOCUS_AREAS` field with a candidate list, and a conditional requirement in the form profile |
| G2 | Target users and beneficiaries as a sector × count × benefit-type matrix | R0 p4 (relayed) | check `RESULTS.CHAIN.USERS`/`BENEFICIARIES` against the form's sectors |
| G3 | FF budget rules: equipment at most 20 percent **of the budget-receiving unit's** R&I budget (not per project), no overhead, whole hundreds, remuneration category closed | R0 p9 (`VERIFIED`) | a dated fund profile with a real, cited call; unit-level caps stay outside a single project's checks |
| G4 | Co-funding split between the fund and the receiving unit | R0 (page not pinned, relayed) | OPEN |
| G5 | Community co-researchers have no team role (the demo used `OTHER`) | R1 (relayed); demo T14 | add a `COMMUNITY_CO_RESEARCHER` role code (GrantThai code; the NRIIS label stays `NEEDS_VERIFICATION`) |
| G6 | "Policy proposal" is not an output type; no output-type list tied to the form's 10 types; no research-synthesis design | R0 annex (relayed); R2, R3 | a candidate output-type list from R0 with page cites |
| G7 | Summary word cap | R0 p3 (`VERIFIED`) | shipped in v0.2 as W101 (3000 words); see G9 |
| G8 | The provenance model has no value for a **simulated** author: the demo persona's statements are recorded `authored_by: human` | this demo | a project-level `simulation: true` flag or an `authored_by: simulated` value, rendered in the frontmatter |
| G9 | Length checks are blind for Thai prose (whitespace tokens undercount), so the checklist's WC09 shows `PASS` for Thai boxes that were never measured | demo build, section 4.6 | a Thai word or character measure, or `HUMAN_CHECK` instead of `PASS` when the text is Thai |
| G10 | The worksheet's section 1.5 listed adopted AI drafts (`human_ai_assisted`) and unadopted ones with the same "set authored_by to human" advice, which nudged a user to relabel adopted AI-assisted text as human-authored | demo build vs `grantthai_skill.py report` | fixed in v0.2: separate advice per value (`tests/test_engine.py`) |
| G11 | `reference/interview.md` does not give the id prefixes for partners (`PTN`) and impacts (`IMP`); the demo's first apply failed on them | demo run | fixed in v0.2: prefixes added to `reference/interview.md` |
| G12 | A form profile names a real form while the only fund binding is the fictional test call, so the frontmatter says "submittable: true" against a call that does not exist | demo build | partly fixed in v0.2: a FICTIONAL banner after the notice line and "Submittable to a real call: n/a (fictional call)" in the readiness summary; the frontmatter boolean stays (contract) |
