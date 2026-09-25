# 100 funded Thai research documents (97 reports, 3 forum proceedings), compared with GrantThai

> **No document text is reproduced here, and no PDF is included in this
> repository.** This file and `docs/demo/corpus-100.csv` hold only
> bibliographic metadata (as the source repositories record it), file hashes,
> structural flags and counts, and aggregate statistics. Where a finding rests
> on a single page, the page is cited by number, with at most a few words of
> the page's own wording. No ethics-approval numbers or personal data beyond
> a public citation (title and first author) are recorded.

GrantThai is an independent, unofficial project; see `NOTICE`. The GrantThai
demo (`examples/demo-seedbank/`) is **fictional**.

Status of this file: `DRAFT`. Tags used below: `VERIFIED` = computed from the
files with `tools/corpus/corpus_extract.py`, or read on the cited PDF page;
`INSTINCT` = a judgement; `OPEN` = not settled.

Thai version: [`corpus-100.th.md`](corpus-100.th.md).

## 1. Why this corpus

The v0.2 comparison (`docs/demo/comparison.md`) set the demo against three
funded reports. That is too few to say what funded Thai research documents
usually contain. This corpus has 100 funded research documents (97 technical reports and 3
forum proceedings, §3), so section
frequencies can be counted instead of guessed.

## 2. Sources, terms and how the files were fetched

**Where the documents come from.**

| Source | Documents used | How items were found |
|---|---|---|
| Health Systems Research Institute knowledge bank (`kb.hsri.or.th`), collection "Research Reports" | 83 | the repository's public REST browse of that collection |
| Prince of Songkla University knowledge bank (`kb.psu.ac.th`) | 17 | the repository's public REST browse by issue date (its `/search` path is disallowed by `robots.txt` and was not used) |

**Access rule.** Only files that anyone can download without an account were
used. Both repositories serve their full texts from the public record page.

**What was left out, and why.**

- **The e-Library of Thailand Science Research and Innovation.** Its own
  download link returns a member login page to a visitor who is not logged
  in, and each record page loads a CAPTCHA. A direct file path still served
  many PDFs without a login, but using it would go around a gate the site
  clearly intends. No full file from it was downloaded (0 documents): the
  catalogue step requested only the first 1 KB of each file to test access.
  The 53 records that answered were set aside pending the founder's
  decision. (The three reports in
  `docs/demo/comparison.md` are a separate, earlier selection.)
- One further national repository was excluded earlier on its terms: full
  texts need membership and are watermarked with the downloader's name.
- From the two repositories above, a catalogue of 213 rows yielded 135
  candidates (87 HSRI, 48 PSU). All 135 were requested; 132 were
  downloaded, and the other 3 were stopped because they were too large to
  fetch politely. 35 were not used: 23 had fewer than 20 pages, 5 had no
  text layer (scanned), 4 had a text layer that a legacy font made
  unreadable, and the 3 too-large files. The 100 documents below are all that remained, not a sample
  chosen by content.

**How files were fetched.** One request at a time, at least 2 seconds apart,
one connection, a User-Agent that names the project, and a stop rule on HTTP
429 or 403 (neither occurred). The PDFs were kept on the maintainer's own
machine only, outside the repository, and are not published.

**Terms.** No reuse licence is relied on. The files are treated as all
rights reserved: they are cited, counted and linked, never copied. Each row
below links the public record page. What the repositories' own metadata
says (`VERIFIED` from the records fetched for the catalogue): the HSRI
community records carry `dc.rights` "Creative Commond (CC BY-NC-SA 3.0 TH)"
(sic), its collection records carry "Creative Commond", and item records
carry `dc.rights` naming the institute itself. This is recorded as
metadata only; the all-rights-reserved treatment remains the safe default.
Robots: `kb.hsri.or.th/robots.txt` answers with a 301 redirect to the
repository home page, so HSRI serves no robots file (`VERIFIED`, re-checked
2026-09-25); `kb.psu.ac.th/robots.txt` disallows `/search`, which was not
used. `OPEN`: before this file is pushed, a person should read both
repositories' terms statements and record them here.

## 3. What the corpus is, and is not

| Item | Value | Tag |
|---|---|---|
| Documents | 100: HSRI repository 83, PSU repository 17 | `VERIFIED` |
| Type in the repository record | 97 "Technical Report", 3 "Document" | `VERIFIED` |
| Final reports vs proposals | All are **completed-work documents; none is a proposal** | `VERIFIED` |
| The 3 "Document" items | Proceedings of a community-health forum series, not research reports (HSRI-057 p3 names the forum; HSRI-095 p3 is a table of contents of case studies; HSRI-058 p3 opens with the forum's opening remarks) | `VERIFIED` |
| Partial file | PSU-044 starts at section 2, with no cover or front matter (p1) | `VERIFIED` |
| Year (Buddhist Era) | ≤2559: 31; 2560–62: 30; 2563–68: 39 | `VERIFIED` |
| Pages | median 92.5 (IQR 60–158, range 21–1,067) | `VERIFIED` |
| Funder in the repository record | 82 (70 name HSRI alone; 12 name other or co-funders); not recorded for 18 (16 PSU, 2 HSRI) | `VERIFIED` |
| Funding statement found in the file | 80 | `VERIFIED` |
| An agency name found in the funding statement or first 20 pages (as funder, publisher, staff affiliation or other mention; a funding phrase naming a body outside the coded list also counts) | 95. None was found in 5: HSRI-011, HSRI-024, HSRI-067, HSRI-070 (their repository records name HSRI) and PSU-044 (its record names a national environment-policy office). For these 5, "funded" rests on the repository record only | `VERIFIED` |
| Title in the record found on the first 3 pages | 83 (marked † in the table when not found) | `VERIFIED` |
| Why a † title was not found | a font that breaks Thai text extraction, or a wording difference between the record and the cover (HSRI-010: the record's "ระยะเวลาการมารับ" against the printed "ระยะเวลาในการมารับ", p1) | `INSTINCT` for the split; HSRI-010 `VERIFIED` |
| Discipline | Health systems (HSRI) 83; science, engineering, agriculture, social science and linguistics (PSU) 17 (by source, not coded per document) | `VERIFIED` (proxy) |

**Consequences.**

1. The corpus leans heavily toward health systems research.
2. 39 documents are from BE 2563 on, but none comes from the national
   research funding agency's e-Library, whose calls use key-result and
   readiness-level language (relayed, not checked here); TRL and SRL
   markers are 0% in this corpus (§4). So it **cannot test** GrantThai's
   key-result, TRL, SRL or strategy alignment fields (`OPEN`).
3. A section that is missing from a *final report* says nothing about
   whether a *proposal* needs it. Budget, workplan and ethics approval are
   proposal- or contract-stage items and are often dropped from reports.
4. An agency named on the first 20 pages may be the publisher, or the
   affiliation of a team member, or only mentioned in the text, rather
   than the funder (HSRI-057 names the health promotion fund on p3 only as
   a team member's affiliation, and the national health security office
   only in the forum's discussion, p6 and p8). The HSRI name appears in 74
   files.
5. Funder codes are not detected evenly. Some codes also match the
   agency's acronym (HSRI, NHSO, THAIHEALTH, NIEMS, and an older short form
   for TRF_SRI); the current acronyms of the national research council and
   of the successor fund are kept out of this repository and are not
   matched. Per-code counts (HSRI 74, NHSO 28, THAIHEALTH 14, NRC 5,
   TRF_SRI 3; funding statement or first 20 pages) are therefore not
   comparable across codes, and NRC and TRF_SRI are probably undercounted.

## 4. Section presence in the 100 documents

Percentage of documents in which the extractor found a heading for each
section, in the body or in the table of contents (`VERIFIED`, recomputable
with `python tools/corpus/corpus_extract.py stats --csv docs/demo/corpus-100.csv`).

| Section | All (n=100) | HSRI repository (n=83) | PSU repository (n=17) | BE ≤2559 (n=31) | BE 2560–62 (n=30) | BE 2563–68 (n=39) | Technical Report only (n=97) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Background / rationale | **91** | 89 | 100 | 84 | 90 | 97 | 94 |
| Discussion / conclusion | **90** | 89 | 94 | 87 | 87 | 95 | 93 |
| Results | **85** | 83 | 94 | 71 | 83 | 97 | 88 |
| Objectives | **82** | 80 | 94 | 74 | 87 | 85 | 85 |
| Methods | **80** | 81 | 76 | 68 | 77 | 92 | 82 |
| References | **78** | 78 | 76 | 71 | 70 | 90 | 79 |
| Appendix | **66** | 64 | 76 | 48 | 73 | 74 | 67 |
| Literature review | **64** | 65 | 59 | 55 | 60 | 74 | 66 |
| Acknowledgement | **62** | 58 | 82 | 42 | 67 | 74 | 64 |
| Thai abstract | **60** | 54 | 88 | 32 | 60 | 82 | 62 |
| English abstract | **53** | 49 | 71 | 19 | 57 | 77 | 55 |
| Keywords | **50** | 47 | 65 | 29 | 47 | 69 | 52 |
| Data analysis | **44** | 48 | 24 | 29 | 30 | 67 | 45 |
| Executive summary | **42** | 46 | 24 | 39 | 37 | 49 | 43 |
| Recommendations | **41** | 47 | 12 | 29 | 23 | 64 | 42 |
| Scope | **40** | 41 | 35 | 35 | 37 | 46 | 41 |
| Outputs / outcomes / impact | **38** | 40 | 29 | 32 | 27 | 51 | 39 |
| Population / sample | **38** | 46 | 0 | 23 | 37 | 51 | 39 |
| Data collection | **33** | 35 | 24 | 23 | 30 | 44 | 34 |
| Conceptual framework | **31** | 37 | 0 | 23 | 20 | 46 | 32 |
| Workplan / timeline | **31** | 37 | 0 | 23 | 20 | 46 | 32 |
| Expected benefit | **29** | 31 | 18 | 29 | 20 | 36 | 30 |
| Policy recommendations | **24** | 28 | 6 | 13 | 20 | 36 | 25 |
| Instruments | **24** | 29 | 0 | 29 | 17 | 26 | 25 |
| Definitions | **19** | 20 | 12 | 13 | 7 | 33 | 20 |
| Utilization | **13** | 11 | 24 | 6 | 10 | 21 | 13 |
| Budget | **11** | 13 | 0 | 19 | 7 | 8 | 11 |
| Research users (section) | **6** | 6 | 6 | 0 | 7 | 10 | 6 |
| Ethics | **6** | 7 | 0 | 3 | 0 | 13 | 6 |
| Hypothesis | **5** | 4 | 12 | 0 | 3 | 10 | 5 |
| Research question | **4** | 5 | 0 | 6 | 0 | 5 | 4 |
| Strategy alignment | **1** | 0 | 6 | 0 | 3 | 0 | 1 |
| Beneficiaries (section) | **0** | 0 | 0 | 0 | 0 | 0 | 0 |

Reports from BE 2563–68 more often have a framework, a data-analysis
section, ethics, recommendations and both abstracts: the reports are
becoming more structured (`VERIFIED` counts, `INSTINCT` reading).

### Size and counts (`VERIFIED`)

| Measure | Value |
|---|---|
| Pages | median 92.5; HSRI 99, PSU 71; BE 2563–68 band 138 |
| References (where a list could be counted, n=70) | median 40.5 (IQR 23–67); 8 documents above 100; max 255 |
| Objective items (where an objectives section was found, n=82) | median 5; 50 have 1–5, 28 have more than 5 (sub-points are counted too, so this is noisy) |
| Distinct table / figure captions | median 11 / 6 |
| Section size, median non-whitespace characters where measured | literature review 18,364 (n=60); background 6,740 (n=88); methods 4,371 (n=78); Thai abstract 2,501 (n=57); framework 1,048 (n=26); objectives 776 (n=82); references 7,388 (n=70) |

### Text markers anywhere in the body (% of documents, `VERIFIED`)

| Marker | % |
|---|---|
| "ยุทธศาสตร์" (strategy) | 58 |
| A baht amount | 49 |
| Policy-recommendation phrase | 47 |
| Sample-size phrase or named formula (Cochran, Yamane, Krejcie, G*Power) | 35 |
| Expert or stakeholder validation (ผู้ทรงคุณวุฒิ, expert panel, public hearing) | 32 |
| Ethics committee or IRB | 21 |
| Informed consent | 16 |
| Stated limitations of the study | 15 |
| Research users ("ผู้ใช้ประโยชน์") | 12 |
| Triangulation | 11 |
| National science, research and innovation plan | 6 |
| Key results (KR) / beneficiaries | 4 / 4 |
| TRL / SRL | 0 / 0 |
| Impact-pathway proxy (research users **and** outputs, utilization or benefit **and** recommendations) | **10** |

## 5. The GrantThai demo against these numbers

`examples/demo-seedbank/NRIIS_SUBMISSION.md` is a form worksheet, not a
narrative report, so only the content of each box can be compared. Sizes are
non-whitespace characters in `examples/demo-seedbank/project.yaml`
(`VERIFIED`).

| Demo box | Demo | Funded reports, median where present | Reading (`INSTINCT`) |
|---|---|---|---|
| `CORE.NARRATIVE.SUMMARY` | 390 | Thai abstract 2,501 | proposal-sized; acceptable |
| `CORE.NARRATIVE.RATIONALE` | 377 | background 6,740 | thin for a model example |
| `CORE.NARRATIVE.OBJECTIVES` | 173 (3 objectives) | 776 (median 5 items) | count in range |
| `CORE.NARRATIVE.FRAMEWORK` | 92 (one sentence) | 1,048; usually drawn as a diagram | thin |
| `CORE.NARRATIVE.THEORY` | 91, and it says itself that no references were added yet | literature review 18,364 | **weakest point** |
| `CORE.NARRATIVE.METHOD` | 466 | methods 4,371 | thin |
| `CORE.NARRATIVE.REFERENCES` | empty | 78% have a list; median 40.5 entries | **missing** |

The demo has an explicit research question and a linked results chain;
reports rarely show these as headings. That is a report-versus-proposal
difference, not a ranking (`INSTINCT`; the facts about `project.yaml` and
the rates below are `VERIFIED`):

- The demo has an explicit primary research question and two secondary
  ones. 4% of the reports have a research-question heading.
- The demo has a linked results chain: a research user (`USR1`), an outcome
  (`OC1`) and an impact (`IMP1`), with objectives linked to method and
  output ids. 10% of the reports reach the impact-pathway proxy.

**Key finding (`VERIFIED`).** The demo's findings line reads BLOCK 0 /
REVIEW 0 (`NRIIS_SUBMISSION.md`, line 65), although its required theory box
says no references were added and its references box is empty. No rule
flags a theory statement that cites nothing.

## 6. Registry coverage

### 6a. Sections in at least half the reports, against GrantThai fields (`VERIFIED` against `registry/fields.jsonl`)

| Section (share of reports) | GrantThai field | Gap |
|---|---|---|
| Background 91% | `CORE.NARRATIVE.RATIONALE`, `CORE.RESEARCH.PROBLEM`, `.NATIONAL_NEED` (required) | none |
| Objectives 82% | `CORE.RESEARCH.OBJECTIVES` (required) | none |
| Methods 80% | `CORE.NARRATIVE.METHOD` + `METHOD.PLAN.*` | none |
| References 78% | `CORE.NARRATIVE.REFERENCES`: **optional, 0..N** | optional in GrantThai, near-universal in funded work |
| Literature review 64% | `CORE.NARRATIVE.THEORY` (required), `CORE.RESEARCH.THEORETICAL_FOUNDATIONS` (optional), `CORE.RESEARCH.GAP` (required) | no field holds the review's structure (topics mapped to constructs) or its sources |
| Thai / English abstract 60% / 53% | one `CORE.NARRATIVE.SUMMARY` | no language split (whether the form needs one is `NEEDS_VERIFICATION`) |
| Keywords 50% | `CORE.GENERAL.KEYWORDS_TH` / `_EN` (required) | none |
| Results 85%, discussion 90%, appendix 66%, acknowledgement 62% | none, or `DOC.ATTACHMENTS` | expected: these are report-stage sections |

Two report-stage elements have no proposal field and could feed one:
**stated limitations** (15% of reports say so in words) and **recommendations for further work** (41% have a
recommendations section). `METHOD.PLAN.QUALITY` is the natural home for the
first. Its registry guidance (`guidance.en`) is empty, as it is for 81 of the
122 registry fields; `guidance/writing_intent.yaml` gives it a purpose and a
template, but its `seen_in` is still `NEEDS_INPUT` (`VERIFIED`).

### 6b. Required GrantThai fields that funded reports rarely show

| Required field | Seen in reports | Reading (`INSTINCT` unless marked) |
|---|---|---|
| `CORE.RESEARCH.RQ.PRIMARY` | 4% as a heading | reports state aims as objectives. Keep the RQ: rules R003–R004 hang on it |
| `METHOD.PLAN.ETHICS` | 6% as a heading; 21% mention an ethics committee | reported inside the methods, as on HSRI-041 p56 (`VERIFIED`); expected for a report |
| `WORK.PLAN.ACTIVITIES` | 31% | contract-stage item, often dropped from final reports |
| `BUDGET.PLAN.*`, `CORE.GENERAL.TOTAL_BUDGET` | 11% as a section; 49% give some baht amount | same |
| `RESULTS.CHAIN.OUTPUTS` | 38% | often a list of indicators (PSU-015 p67–68, `VERIFIED`) |
| Key results, alignment, TRL, SRL (not required) | 4%, 1%, 0%, 0% | these terms postdate most of the corpus, and none of the national agency's reports are included (`OPEN`) |

These gaps are **what a report-versus-proposal comparison should show**, so
they are not grounds for dropping any field.

## 7. Close reading of 8 documents

A stratified pick: 5 HSRI and 3 PSU, BE 2557–2566, covering clinical
services, workforce policy, clinical care evaluation, a medical device,
health-technology assessment, animal nutrition, marine ecology and
agricultural cooperatives. Page numbers are PDF pages. Each observation was
read on the cited page (`VERIFIED`); the cited pages were then re-opened
and checked by a second pass.

| Doc | Literature review | Method | Impact pathway |
|---|---|---|---|
| HSRI-010 (2557, delay to stroke treatment) | Opens with a list of topics running from the disease to the "factors affecting time to treatment" that the objectives study (p14) | Sample size from Cochran's formula with every parameter stated (n = 288.77, rounded to 300), p21–22; framework from the review (p11) | Executive summary placed at the end (p51); no users section |
| HSRI-041 (2565, nursing workforce) | Topics follow the framework's own three parts: production, distribution, retention (p20, p23) | Mixed methods; a design table matches objectives to data ("ตาราง 5", p56); Lincoln and Guba's trustworthiness criteria (p57); draft recommendations tested at an expert seminar (p56) | Recommendations **name the responsible body and the action** (p122) |
| HSRI-047 (2566, hip-fracture care) | The review feeds a research-framework figure that adds the effect of COVID-19 on care (p26) | Framework figures (p24, p26) | Discusses the national insurance data it used and the effect of COVID-19 (p88) |
| HSRI-080 (2565, 3D-printed titanium skull plate) | Clinical background with numbered citations (p15) | Tests tied to named ASTM, ISO and USP standards (p33) | Names the research-user agencies (p14) and splits benefits into policy and commercial (p13–14) |
| HSRI-073 (2562, PET/CT technology assessment) | An access framework built from cited literature, "(95-99)" (p73) | Cost-utility analysis (named in the abstract, p4) | Recommendations carry a **price and a budget figure** (p167) |
| PSU-026 (2562, goat feed from oil-palm fronds) | Numbered outline ending in "related research" (p14); 212 references counted | Latin-square design with ratios and duration stated (p36) | No users section |
| PSU-015 (2561, seagrass carbon) | Short review that defines the carbon pools (p11) | | Outputs with checkable evidence: a DOI (p67), a conference talk and a training workshop (p68), and **one policy recommendation** (p68) |
| PSU-039 (2563, rubber cooperatives) | The discussion places findings as consistent with ("สอดคล้อง") or contrary to ("ขัดแย้ง") earlier studies (p43) | Sample stratified by the cooperatives' share capital (p6) | Short utilization section |

**Patterns (`INSTINCT`, grounded in the rows above).**

1. **Literature review.** Strong reports open the review with a numbered
   list of topics that mirrors the objectives or the framework (HSRI-010,
   HSRI-041, PSU-026), end with "related research", and later place their
   own findings for or against earlier studies (PSU-039).
2. **Method.** Strong reports tie each objective to data and analysis in a
   design table, justify the sample size with numbers, name a quality
   standard (trustworthiness criteria, ASTM or ISO), and state the limits of
   their data.
3. **Impact pathway.** Where there is one, it is concrete: a named body and
   an action (HSRI-041), a price or budget figure (HSRI-073), named user
   agencies (HSRI-080), or checkable outputs (PSU-015). Most reports have
   none: the proxy reaches 10%.

## 8. Ranked improvements for GrantThai

Ordered by likely value to a reviewer against the cost to build
(`INSTINCT`). Each rests on a `VERIFIED` finding above. None is implemented
by this change.

| # | Level | Change | Evidence |
|---|---|---|---|
| 1 | Rule | A new REVIEW rule: `CORE.NARRATIVE.THEORY` or `THEORETICAL_FOUNDATIONS` is filled while `CORE.NARRATIVE.REFERENCES` is empty, or a theory entry links no reference. The demo passes today with REVIEW 0 | §5; 78% of reports have references |
| 2 | Field | Make `CORE.NARRATIVE.REFERENCES` required (1..N) for full proposals, and let `THEORETICAL_FOUNDATIONS` entries point to reference ids | §6a |
| 3 | Guidance | Fill `seen_in` in `guidance/writing_intent.yaml` with a document id and PDF page from §7 (id and page only, no quoted text, as the file's own policy allows). Write English guidance for the 81 registry fields that have none, starting with GAP, RQ, THEORY, `METHOD.PLAN.*`, QUALITY, `UTILIZATION_DESC` and OUTCOMES | §6a, §7 |
| 4 | Field + guidance | Give `METHOD.PLAN.QUALITY` a structure: validity and reliability (or trustworthiness) criteria, standards followed, known limits of the data. REVIEW when it is empty for a mixed-methods or qualitative design | HSRI-041 p57, HSRI-047 p88, HSRI-080 p33 |
| 5 | Field | Add a sample-size basis to `METHOD.PLAN.SAMPLE` (method, parameters, source); REVIEW when a quantitative design has none | 35% of reports; HSRI-010 p21–22 |
| 6 | Guidance | A shape for the literature review: open with a numbered topic list that mirrors constructs or objectives, end with related studies, and record each prior study's stance (supports / challenges) on its prior-knowledge record | HSRI-010 p14, HSRI-041 p23, PSU-026 p14, PSU-039 p43 |
| 7 | Renderer | Render an objective × design × data × analysis table from the existing R004–R007 links, ready to paste | HSRI-041 p56 |
| 8 | Field | Turn `RESULTS.CHAIN.UTILIZATION_DESC` into structured recommendation targets (body, intended action, evidence needed, budget implication) linked to users; REVIEW, extending P001 and U002, when a policy claim names no body | HSRI-041 p122, HSRI-073 p167, HSRI-080 p14 |
| 9 | Field | An output type on `RESULTS.CHAIN.OUTPUTS` (knowledge or publication, product, technology transfer, policy proposal) with a form of evidence (DOI, event, document) | PSU-015 p67–68 |
| 10 | Field | Let `CORE.NARRATIVE.FRAMEWORK` reference a diagram attachment; strong reports draw it | HSRI-010 p11, HSRI-041 p20, HSRI-047 p24 |
| 11 | Demo | Either upgrade the demo to model good practice (a few real-format references, a theory box with citations, a method with sample basis and quality criteria), or keep it thin on purpose and let rule 1 flag it in plain view | §5 |
| 12 | Guidance | Length targets: keep the `proposed_default` targets, but note that funded **reports** have a median of about 18,000 characters of review and 40 references (8 of 70 above 100). No reference cap until a form's own cap is read | §4 |
| 13 | Field (low) | An optional English summary, if an NRIIS form is seen to require one (`NEEDS_VERIFICATION`) | §6a |
| 14 | Corpus | Add at least 30 reports or public proposals from BE 2563 onward, from a source whose terms allow it, to test the key-result, TRL, SRL and alignment fields | §3 (`OPEN`) |

**Do not act on** the rarity of RQ, ethics, workplan, budget and alignment
sections in reports: that is the report-versus-proposal difference (§6b).
The demo's explicit RQ and results chain are proposal-stage content that
reports rarely show as headings, and should stay (`INSTINCT`).

## 9. Limitations

- **Reports, not proposals.** Every document is a completed-work document;
  three are forum proceedings. A section missing from a report is not
  evidence about proposals.
- **Two sources, one field.** 83 of 100 documents are health-systems
  reports from one repository. The national funding agency's e-Library is
  not represented (§2).
- **Detection accuracy.** Sections are found by headings, with patterns
  tolerant of the broken Thai text that older PDF fonts give. Headings with
  unusual wording are missed and some table cells may pass as headings. The
  research-question heading appears in 4% of documents, while RQ wording
  appears in the text of more. Reference counts are undercounted where a
  list follows the appendix (HSRI-073 has a list but counts 0). Objective
  counts include sub-points. No second, independent coding of the 100
  documents was done: percentages are a machine readout, not a hand count.
- **One reading.** The close reading in §7 was done by one AI assistant; a
  second pass re-opened the cited pages and corrected two citations. No
  human researcher has read these documents for this study yet. The
  patterns drawn from them are `INSTINCT`.
- **Funding status.** For 5 documents the file names no funding body; they
  count as funded only on their repository record (§3).
- **Recomputability.** Every number in §3–§6 comes from
  `docs/demo/corpus-100.csv` via `tools/corpus/corpus_extract.py stats`.
  Re-running `extract` needs the PDFs, which each reader must download from
  the record pages below; the sha256 column lets a reader confirm the file
  is the same one.

## 10. The 100 documents

Metadata as the repository records it: the title and first author are given
as the record gives them (a public citation), not re-typed from the file.
† = the record's title was not found on the file's first 3 pages by text
matching. Funder codes are this project's labels for a name found in the
file's funding statement or first 20 pages: HSRI = Health Systems Research
Institute; NHSO = National Health Security Office; THAIHEALTH = Thai Health
Promotion Foundation; NIEMS = National Institute for Emergency Medicine;
NRC = the national research council (full name only; its current
acronym is not matched); TRF_SRI = the national research fund or its
successor (full name or the fund's older short form; the successor's
acronym is not matched); GOV_BUDGET = government budget; UNIV_INCOME =
university income or research grant; OTHER_FUND = a funding phrase whose
body is not one of the coded names (HSRI-008: a university research centre
named on its opening pages). HSRI, NHSO, THAIHEALTH and NIEMS are also
matched by acronym, so codes are detected unevenly (§3, consequence 5).
A code shows that the name was found, not that the body funded the work: it
may be a publisher, an affiliation or another mention. The same data, with every
structural flag, is in [`corpus-100.csv`](corpus-100.csv).

| Id | Title (repository record) | First author (repository record) | Institution (record) | Funder (record) | Funder named in the file | Contract / handle | Year (BE) | Type | Pages | sha256 | Record page |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PSU-003 | การใช้สารพอลิอิเล็กโทรไลต์เพื่อเพิ่มประสิทธิภาพสารดึงในการบำบัดน้ำเสียหมึกพิมพ์ด้วยกระบวนการฟอร์เวิร์ดออสโมซิส | วัสสา คงนคร | มหาวิทยาลัยสงขลานครินทร์ | not in record | GOV_BUDGET, UNIV_INCOME | hdl 2016/12676 | 2561 | Technical Report | 57 | `98e9824363c115939bdd8415d765df88a96843053caed1e86441157a266a0c23` | https://kb.psu.ac.th/handle/2016/12676 |
| PSU-005 | การเคลือบผิวกระจกโซลาร์เซลล์ให้สามารถทำความสะอาดตัวเองได้ | จันทิมา ชั่งสิริพร | มหาวิทยาลัยสงขลานครินทร์ | not in record | GOV_BUDGET, NRC | hdl 2016/11849 | 2561 | Technical Report | 81 | `06735db10a451c21183866a96066cdd6cbaf3c0eb4a270c334a05a7280d0a7b5` | https://kb.psu.ac.th/handle/2016/11849 |
| PSU-008 | การโคลนและศึกษาสมบัติของยีนเลคตินสองชนิด (เลคตินแบบ C และเลคตินที่มีโดเมนไฟบริโนเจน) จากฮีโมไซท์ของกุ้งฟีเนียสที่ตอบสนองต่อการเหนี่ยวนำด้วยเชื้อก่อโรค | ประภาพร อุทารพันธุ์ | มหาวิทยาลัยสงขลานครินทร์ | not in record | GOV_BUDGET, TRF_SRI, UNIV_INCOME | hdl 2016/12621 | 2561 | Technical Report | 27 | `39e284b86292c3d4d2be67a620752bf993bcd49d81eb6c377bc1e51ac0ee3ff5` | https://kb.psu.ac.th/handle/2016/12621 |
| PSU-010 | ตัวดูดซับของแข็งชนิดใหม่ครัยโอเจลคอมโพสิทกราฟีนออกไซด์เคลือบโพลีไพโรลสำหรับสกัดและเพิ่มความเข้มข้นสารซัลโฟนาไมด์ | โอภาส บุญเกิด | มหาวิทยาลัยสงขลานครินทร์ | not in record | UNIV_INCOME | hdl 2016/12322 | 2561 | Technical Report | 23 | `c710ac6d77d0eb37739bc68042b883920f16ec01296e4c3af033d32431eb9372` | https://kb.psu.ac.th/handle/2016/12322 |
| PSU-014 | การพัฒนาเทคโนโลยีการฝากเซลล์สืบพันธุ์ในการเพาะเลี้ยงสัตว์น้ำ | วิไลวรรณ โชติเกียรติ | มหาวิทยาลัยสงขลานครินทร์ | not in record | GOV_BUDGET | hdl 2016/19484 | 2564 | Technical Report | 206 | `edfa8f50ed12931b71345615d2e2a05602ae1471dacacec97b23821db9e95b40` | https://kb.psu.ac.th/handle/2016/19484 |
| PSU-015 | รายงานวิจัยฉบับสมบูรณ์การกักเก็บคาร์บอนในหญ้าทะเล : บทบาทของหญ้าทะเลต่อการเปลี่ยนแปลงของภูมิอากาศโลก | อัญชนา ประเทพ | มหาวิทยาลัยสงขลานครินทร์ | not in record | GOV_BUDGET, UNIV_INCOME | hdl 2016/12361 | 2561 | Technical Report | 71 | `e654b32c335ca371b134ccaacdc32b68ce57019bf1f9305156c99fe00cb39491` | https://kb.psu.ac.th/handle/2016/12361 |
| PSU-016 | การแยกและคัดเลือกเชื้อเฮเทอโรโทรฟิคไนตริไฟอิงแบคทีเรียทนเค็มสำหรับการเพาะเลี้ยงกุ้ง | ยุทธพงษ์ สังข์น้อย | มหาวิทยาลัยสงขลานครินทร์ | not in record | UNIV_INCOME | hdl 2016/13243 | 2560 | Technical Report | 31 | `ce545b1605a43345b3395384092d94f63ebe1b51de2d6cf5bd91dbfa81f0776b` | https://kb.psu.ac.th/handle/2016/13243 |
| PSU-017 | รายงานวิจัยฉบับสมบูรณ์ชื่อชุดโครงการการสร้างพลังงานสะอาดรูปแบบใหม่และการจัดการพลังงานสำหรับการทำงานด้วยตัวเองของอุปกรณ์พกพาและเครือข่ายไร้สาย | นันทกาญจน์ มุรศิต | มหาวิทยาลัยสงขลานครินทร์ | not in record | GOV_BUDGET, UNIV_INCOME | hdl 2016/11914 | 2560 | Technical Report | 57 | `35e4efe165e9128f5e24df76be5a214c30ceb2fa86c440d7c746f034d5c4bd75` | https://kb.psu.ac.th/handle/2016/11914 |
| PSU-018 | การตรวจวัดและวิเคราะห์นิวไคลด์กัมมันตรังสีในดิน เพื่อประเมินการชะล้างและการสะสมของดินในพื้นที่คัดสรรในเขตแอ่งหาดใหญ่ | ไตรภพ ผ่องสุวรรณ | มหาวิทยาลัยสงขลานครินทร์ | not in record | UNIV_INCOME | hdl 2016/12620 | 2560 | Technical Report | 137 | `dd2dcd649b7db503c873e498f7dc640d8271b8826501200d6c471beb9dc3b20d` | https://kb.psu.ac.th/handle/2016/12620 |
| PSU-019 | อัตราการตกตะกอนช่วงปัจจุบันในทะเลสาบสงขลาโดยวิธีวัดไอโซโทปกัมมันตรังสี ตะกั่ว - 210 และซีเซียม - 137 | ไตรภพ ผ่องสุวรรณ | มหาวิทยาลัยสงขลานครินทร์ | not in record | GOV_BUDGET, UNIV_INCOME | hdl 2016/13227 | 2559 | Technical Report | 146 | `d5cf043c1a8cc1de60d510411cccd35dc9315c6b43f99d7366719701b2185c98` | https://kb.psu.ac.th/handle/2016/13227 |
| PSU-023 | ความหลากหลายและศักยภาพการเจริญเติบโตของพืชวงศ์ปาล์มภายใต้สภาพแวดล้อมสวนยางพาราในภาคใต้ | ระวี เจียรวิภา | มหาวิทยาลัยสงขลานครินทร์ | not in record | GOV_BUDGET, UNIV_INCOME | hdl 2016/12350 | 2562 | Technical Report | 68 | `eab4c978a117c7b59b4c616a3d9893982dcf13d457c37bddd1f075e16363dcc6` | https://kb.psu.ac.th/handle/2016/12350 |
| PSU-026 | การเพิ่มคุณค่าทางโภชนะของทางใบปาล์มน้ำมันโดยยูเรียและแคลเซียมไฮดรอกไซด์เป็นอาหารแพะ | ปิ่น จันจุฬา | มหาวิทยาลัยสงขลานครินทร์ | not in record | UNIV_INCOME | hdl 2016/12663 | 2562 | Technical Report | 75 | `f588b5e5075085e867c3b69eb57ec516a4d38561057d439937f4da290ce7d10e` | https://kb.psu.ac.th/handle/2016/12663 |
| PSU-028 | การใช้ประโยชน์ของกากผลปาล์มน้ำมันจากกระบวนการหีบแบบแห้งด้วยตัวทำละลายในสูตรอาหารแพะ † | ปิ่น จันจุฬา | มหาวิทยาลัยสงขลานครินทร์ | not in record | UNIV_INCOME | hdl 2016/13238 | 2561 | Technical Report | 49 | `a50dcb79e580a807f348b2f5799fb43200146005d628e1e75f56da542ac88127` | https://kb.psu.ac.th/handle/2016/13238 |
| PSU-036 | ผลร่วมของสารละลายฆ่าเชื้อและความร้อนระดับกลางต่อการลดปริมาณเชื้อจุลินทรีย์และการยืดอายุการเก็บรักษาโหระพาที่สภาวะต่าง ๆ | ดุสิดา ถิระวัฒน์ | มหาวิทยาลัยสงขลานครินทร์ | not in record | UNIV_INCOME | hdl 2016/12674 | 2560 | Technical Report | 79 | `5850cb01ac811a888b8df97f693088b3179fde3ed1617cd514601ed00972404d` | https://kb.psu.ac.th/handle/2016/12674 |
| PSU-038 | ลักษณะเหนือหน่วยเสียงและการเปลี่ยนแปลงของเสียงที่สะกดตามเสียงพูดในสติ๊กเกอร์ไลน์ภาษาไทย | จอมขวัญ สุทธินนท์ | มหาวิทยาลัยสงขลานครินทร์ | not in record | UNIV_INCOME | hdl 2016/13311 | 2563 | Technical Report | 192 | `7edd0d1c67da020d9e87413b085960782779b89e8926b3ccb9011e2e93bf5558` | https://kb.psu.ac.th/handle/2016/13311 |
| PSU-039 | การปรับตัวของสหกรณ์กองทุนสวนยาง ภายใต้สภาวะวิกฤตราคายางตกต่ำ | นฤมล พฤกษา | มหาวิทยาลัยสงขลานครินทร์ | not in record | NRC | hdl 2016/13179 | 2563 | Technical Report | 44 | `1980f26f6c3ad977a658a65772c89e305e8446009622f440683bbda1c69442ea` | https://kb.psu.ac.th/handle/2016/13179 |
| PSU-044 | รายงานฉบับสมบูรณ์ โครงการพัฒนาลุ่มน้ำทะเลสาบสงขลาอย่างยั่งยืน † | not in record | มหาวิทยาลัยสงขลานครินทร์ | สานักงานนโยบายและแผนทรัพยากรธรรมชาติและสิ่งแวดล้อม | none found | hdl 2016/14819 | 2557 | Technical Report | 192 | `778823dd421a7506469624fd17b6b0379401660852a438a7ee8c1ab0670b7b35` | https://kb.psu.ac.th/handle/2016/14819 |
| HSRI-002 | บทสังเคราะห์รายงานการประเมินแผนหลักการแพทย์ฉุกเฉินแห่งชาติ ปี 2553-2555 † | สำนักงานวิจัยเพื่อการพัฒนาหลักประกันสุขภาพไทย | not in record | สำนักงานการแพทย์ฉุกเฉินแห่งชาติ, สถาบันวิจัยระบบสาธารณสุข | HSRI, NHSO, NIEMS, THAIHEALTH | hdl 11228/3733; contract T55-11; id hs1992 | 2555 | Technical Report | 27 | `1759e005ef220ee8042a070a28fdff035f850f19f845eded52d3f569fb2ccc45` | https://kb.hsri.or.th/dspace/handle/11228/3733 |
| HSRI-005 | การถ่ายโอนสถานีอนามัยสู่ท้องถิ่น: การสังเคราะห์บทเรียนจากกรณีศึกษาพื้นที่ถ่ายโอน และข้อเสนอเชิงนโยบาย | ลือชัย ศรีเงินยวง | not in record | แผนงานวิจัยและพัฒนาการกระจายอำนาจด้านสุขภาพ สถาบันวิจัยระบบสาธารณสุข | HSRI, NHSO, THAIHEALTH | hdl 11228/3860; contract 54-039; id hs2057 | 2556 | Technical Report | 89 | `71c1d0deb8cc4d3ead5ac9dad8c9fd485b62f5e11b958fb633a52f9828516f52` | https://kb.hsri.or.th/dspace/handle/11228/3860 |
| HSRI-006 | ระบบราคาอ้างอิงของยาในประเทศไทย | เพชรรัตน์ พงษ์เจริญสุข | not in record | not in record | HSRI, NHSO | hdl 11228/3760; contract 53-066; id hs2029 | 2556 | Technical Report | 122 | `8d050fe863cdd6ce392b8b80540c853c9a07da43f80889709183cfb08e7f33e9` | https://kb.hsri.or.th/dspace/handle/11228/3760 |
| HSRI-007 | รายงานตัวชี้วัดการวิเคราะห์ข้อมูลการสั่งใช้ยา † | โครงการพัฒนาสารสนเทศด้านยาของผู้ป่วยนอกรายบุคคลในระบบประกันสุขภาพถ้วนหน้า | not in record | สถาบันวิจัยระบบสาธารณสุข | NHSO | hdl 11228/3764; contract 53-066; id hs2033 | 2556 | Technical Report | 71 | `ab0d57d558b7552da5ae813c7790662ffcd2fb467b5e765be93021906e589fbb` | https://kb.hsri.or.th/dspace/handle/11228/3764 |
| HSRI-008 | ผลงานวิจัยระบบบริการสุขภาพในโรงพยาบาลของประเทศไทยภายใน 10 ปี (พ.ศ.2545 – 2555) | สมพร หุ่นเลิศ | not in record | สถาบันวิจัยระบบสาธารณสุข, ศูนย์วิจัยเพื่อการพัฒนาระบบบริการสุขภาพ(TRC-HS) คณะแพทยศาสตร์ จุฬาลงกรณ์มหาวิทยาลัย | OTHER_FUND | hdl 11228/4415; contract 57-109; id hs2241 | 2556 | Technical Report | 92 | `ee56c09dae310fa5c894d6102ac99ddde69d27f8331a6a04192e4f96c073566b` | https://kb.hsri.or.th/dspace/handle/11228/4415 |
| HSRI-009 | การคาดการณ์ความต้องการและการวางแผนกำลังคนสำหรับระบบบริการทางการแพทย์ฉุกเฉิน † | นงลักษณ์ พะไกยะ | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, NHSO, NIEMS | hdl 11228/4207; id hs2140 | 2557 | Technical Report | 102 | `980560ba543110a408c7990910a9b69c259d62c252038dfcb6194b71668e3326` | https://kb.hsri.or.th/dspace/handle/11228/4207 |
| HSRI-010 | การศึกษาระยะเวลาการมารับการรักษาของผู้ป่วยโรคสมองขาดเลือด ในจังหวัดอุบลราชธานี † | พนัชญา ขันติจิตร | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, NHSO | hdl 11228/4315; contract 57-067; id hs2190 | 2557 | Technical Report | 57 | `b482d7f4154c2dd34885c1080c162ecd4e484c4bce20ab9e225fb6e5ce048182` | https://kb.hsri.or.th/dspace/handle/11228/4315 |
| HSRI-011 | การส่งเสริมการใช้ยาปฏิชีวนะอย่างสมเหตุผลในร้านยาปี พ.ศ. 2555 | สมาคมเภสัชกรรมชุมชน (ประเทศไทย) | not in record | สถาบันวิจัยระบบสาธารณสุข | none found | hdl 11228/4203; contract 54-058; id hs2130 | 2557 | Technical Report | 96 | `777c84be97659cbbc78a2017bc8316fa902c53bf7ba84ef563214beed1478139` | https://kb.hsri.or.th/dspace/handle/11228/4203 |
| HSRI-012 | การสำรวจสถานภาพความรู้ เรื่องเล่าเพื่อการเยียวยา † | ศิริวรรณ ลาภสมบูรนานนท์ | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/4029; contract 54-059; id hs2117 | 2557 | Technical Report | 68 | `482e3b2bb17a7c3c101fcb8fc1ac8720f377bd891d9ed666bee9fe18d67f60e2` | https://kb.hsri.or.th/dspace/handle/11228/4029 |
| HSRI-013 | ปัจจัยที่มีอิทธิพลต่อการจัดบริการเขตบริการสุขภาพด้านการแพทย์แผนไทยและการแพทย์ทางเลือกของสถานบริการในสังกัดกระทรวงสาธารณสุข | มณฑกา ธีรชัยสกุล | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, NHSO | hdl 11228/4272; contract 57-076; id hs2160 | 2558 | Technical Report | 40 | `173979ee4dbc3a2f1b698c8dd345b715cab20f75279c18642296fc3b848df42f` | https://kb.hsri.or.th/dspace/handle/11228/4272 |
| HSRI-014 | การพัฒนารูปแบบการดำเนินงานโดยชุมชนมีส่วนร่วมเพื่อลดพฤติกรรมการบริโภคเครื่องดื่มแอลกอฮอล์ † | กานต์นะรัตน์ จรามร | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/4292; contract 57-079; id hs2173 | 2558 | Technical Report | 59 | `c0c6ae6c9a43a60b92b57a5cbe536ecbd8a2ec23ba241f7cd468d8db7171b931` | https://kb.hsri.or.th/dspace/handle/11228/4292 |
| HSRI-015 | การล้มในผู้สูงอายุไทยในเขตเมืองและชานเมือง : อุบัติการณ์ ปัจจัยเสี่ยง การจัดการและการป้องกัน | ไพลวรรณ สัทธานนท์ | not in record | สถาบันวิจัยระบบสาธารณสุข, มูลนิธิสถาบันวิจัยและพัฒนาผู้สูงอายุไทย, สำนักงานคณะกรรมการวิจัยแห่งชาติ | HSRI | hdl 11228/4310; contract 56-028; id hs2185 | 2558 | Technical Report | 251 | `21d3074f979b250406cfb6bdf704924885094bebfc820f01200f46bdbdda2fa7` | https://kb.hsri.or.th/dspace/handle/11228/4310 |
| HSRI-016 | การพัฒนารูปแบบการป้องกันการป่วยโรคเบาหวานชนิดที่ 2 ในประชาชนกลุ่มเสี่ยง | นงลักษณ์ เทศนา | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/4264; contract 57-085; id hs2155 | 2558 | Technical Report | 113 | `77a5ff71b2a039ef191c638af7ed979701927ef71aa78f07c5405a318edab273` | https://kb.hsri.or.th/dspace/handle/11228/4264 |
| HSRI-017 | ระบบการดูแลทางสังคมสำหรับผู้สูงอายุ | วรรณลักษณ์ เมียนเกิด | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/4424; contract 58-047; id hs2248 | 2559 | Technical Report | 210 | `502443ae71322251b4c1b4ee2cb21b2f1978b45009ed4395f4898683ef989ea6` | https://kb.hsri.or.th/dspace/handle/11228/4424 |
| HSRI-018 | รูปแบบการบริหารจัดการศูนย์ประสานการส่งต่อ เขตสุขภาพที่ 6 | เกศรินทร์ ไทยศรีวงศ์ | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/4636; contract 59-034; id hs2302 | 2559 | Technical Report | 93 | `facfd050de14bd96923cc54530eb832e9957e9879f07f1f38e0a12282d4bf2b6` | https://kb.hsri.or.th/dspace/handle/11228/4636 |
| HSRI-019 | การประเมินสถานการณ์ของการบริการปฐมภูมิในเขตกรุงเทพมหานครด้วยการศึกษา Ambulatory care sensitive conditions | จิรุตม์ ศรีรัตนบัลล์ | not in record | ส่วนงานสำนักงานวิจัยเพื่อการพัฒนาหลักประกันสุขภาพไทย สถาบันวิจัยระบบสาธารณสุข | HSRI, NHSO | hdl 11228/4420; contract 58-019; id hs2245 | 2559 | Technical Report | 182 | `74f17d5f1712d0a57a49abad0844a501b5d5049335732c1b20897f7022a86265` | https://kb.hsri.or.th/dspace/handle/11228/4420 |
| HSRI-020 | ระบบฐานข้อมูลสารสนเทศเพื่อการดูแลคนพิการ † | วรลักษณ์ คงเด่นฟ้า | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, NHSO | hdl 11228/4456; contract 58-064; id hs2262 | 2559 | Technical Report | 388 | `4878f37f7db97c034b36869be4dd841e5dfa7d7c2b1341b9ed311efcd1a562bf` | https://kb.hsri.or.th/dspace/handle/11228/4456 |
| HSRI-021 | การพัฒนาและการประเมินชุดทดสอบสำหรับการตรวจหาแอนติบอดีต่อเด็งกี่/เลปโตสไปโรสิส/สครับไทฟัส ชนิด IgM/IgG ในชุดทดสอบเดียวกัน | อุไรวรรณ โฆษิตานนท์ | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/4764; contract 57-051; id hs2350 | 2560 | Technical Report | 64 | `49dceb5f0f41edf2a625513998d3b0669ee22c886c0102c1d3b72a0d8a020335` | https://kb.hsri.or.th/dspace/handle/11228/4764 |
| HSRI-022 | ผลของการออกกำลังและการบริโภคอาหารต่อการเกิดโรคสมองเสื่อม โรคไตเรื้อรัง โรคเบาหวาน และโรคหัวใจและหลอดเลือดในประชากรไทยในจังหวัดอุบลราชธานี โครงการต่อเนื่อง ปีที่ 2 | ประเสริฐ บุญเกิด | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, THAIHEALTH | hdl 11228/4895; contract 59-069; id hs2419 | 2560 | Technical Report | 107 | `ec59d5e6ecf15314b56cfe97eb3a43bd08f9c323e8b696fecbc058ba919a73d3` | https://kb.hsri.or.th/dspace/handle/11228/4895 |
| HSRI-023 | ความตระหนักรู้เกี่ยวกับการใช้ยาอย่างสมเหตุผลในบุคลากรทางการแพทย์ | กมลนัทธ์ ม่วงยิ้ม | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/4695; contract 57-110; id hs2334 | 2560 | Technical Report | 28 | `4fd2a118d03d9c192a3c2a98a10c9e97e7d57c4dbfe5a4c11bb099ca9f60cef7` | https://kb.hsri.or.th/dspace/handle/11228/4695 |
| HSRI-024 | หลักสูตรฝึกอบรมผู้ปกครองในการคัดกรองและปรับพฤติกรรมเด็กที่มีอาการสมาธิสั้น ปีที่ 1 | สมัย ศิริทองถาวร | not in record | สถาบันวิจัยระบบสาธารณสุข | none found | hdl 11228/4843; contract 59-008; id hs2391 | 2560 | Technical Report | 74 | `5e6666d617d6672647c8d13dc31e0ad91c92199e9c9f0dcc62bf169004f7fe0a` | https://kb.hsri.or.th/dspace/handle/11228/4843 |
| HSRI-025 | การวิเคราะห์ต้นทุน ประสิทธิผลของระบบการดูแลต่อเนื่องผู้ป่วยจิตเวชกลุ่มเสี่ยงในสถานบริการระดับปฐมภูมิ เปรียบเทียบกับระบบบริการปกติ † | จุฑามณี ดุษฎีประเสริฐ | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, NHSO | hdl 11228/5016; contract 61-017; id hs2467 | 2561 | Technical Report | 99 | `495ab04ea027731cc09a870e3c7048566e0140bada5ef4f3258f1c667a9236ed` | https://kb.hsri.or.th/dspace/handle/11228/5016 |
| HSRI-026 | การพัฒนารูปแบบการจัดการปัญหาภาวะอ้วนลงพุงและภาวะแทรกซ้อนของประชากรในเขตกรุงเทพมหานคร ปีที่ 2 | สุรัตน์ โคมินทร์ | not in record | not in record | HSRI, THAIHEALTH | hdl 11228/4931; contract 59-021; id hs2442 | 2561 | Technical Report | 314 | `840dc2e49f20a5ca67ec595ecc7e22d638ff74c2ed1196aa50834c758e6efb2c` | https://kb.hsri.or.th/dspace/handle/11228/4931 |
| HSRI-027 | การพัฒนากลไกการมีส่วนร่วมของภาคประชาสังคมต่อนโยบายของรัฐ เพื่อสนับสนุนการเข้าถึงยาของประชาชนไทย | อุษาวดี สุตะภักดิ์ | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, NHSO, THAIHEALTH | hdl 11228/4842; contract 60-027; id hs2389 | 2561 | Technical Report | 150 | `cf360123a974b28ea445d92665714c2ad552d50b7ac956d0f97032db3afbdbfb` | https://kb.hsri.or.th/dspace/handle/11228/4842 |
| HSRI-028 | การพัฒนาชุดตรวจสำเร็จรูป (แบบ ELISA และ แบบรวดเร็ว) เพื่อตรวจหา antifilarial IgG4 ที่จำเพาะต่อพยาธิเท้าช้างโดยใช้ ecombinant antigen | สิริจิต วงศ์กำชัย | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, NRC | hdl 11228/4961; contract 60-045; id hs2456 | 2561 | Technical Report | 143 | `210ff0a864c22965d95c26941c646675b59a3bc271f8eac8f73648f1b6d0ec74` | https://kb.hsri.or.th/dspace/handle/11228/4961 |
| HSRI-029 | การพัฒนาเครื่องวัดความเข้มข้นของเลือดแบบไม่รุกล้ำเพื่อการดูแลรักษาผู้ป่วยไข้เลือดออกเดงกี่ | ยศชนัน วงศ์สวัสดิ์ | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/5022; contract 60-025; id hs2470 | 2562 | Technical Report | 73 | `ee8ab502cf1d73e88eada7e44e0f1d3fb765f224b23b543416e2343b8294b99f` | https://kb.hsri.or.th/dspace/handle/11228/5022 |
| HSRI-030 | การพัฒนารูปแบบการดูแลผู้ป่วยนอกโรคหัวใจล้มเหลวโดยสหสาขาวิชาชีพ † | อุษาศิริ ศรีสกุล | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/5050; contract 61-001; id hs2485 | 2562 | Technical Report | 114 | `a3f3ccdf2108ecd4b51e4d97cc8ca24046d2c54619661c1c5f7ed32718559ba4` | https://kb.hsri.or.th/dspace/handle/11228/5050 |
| HSRI-031 | การพัฒนานักวิจัยหน้าใหม่ระดับพื้นที่จากงานประจำสู่งานวิจัยระดับประเทศ ปี 2562 : ฐานข้อมูลนักวิจัยหน้าใหม่ | ณัฏฐญา พัฒนะวาณิชนันท์ | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, NHSO, THAIHEALTH | hdl 11228/5124; contract 62-078; id hs2519 | 2562 | Technical Report | 21 | `4714564db4e0af829cb395bd8cc219e5fdb3b5304a715de3695986fa1dd4f5e6` | https://kb.hsri.or.th/dspace/handle/11228/5124 |
| HSRI-032 | การพัฒนาการตรวจวินิจฉัยโรคติดเชื้อรา Penicillium marneffei โดยใช้โมโนโคนอลแอนติบอดี 4D1 ที่จำเพาะต่อเชื้อ | สิริดา ยังฉิม | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/5166; contract 60-070; id hs2536 | 2562 | Technical Report | 121 | `d4b5f7d2839373ed02118b10a7b3f2d39395e2ec450c115a1a745d0eb285c5aa` | https://kb.hsri.or.th/dspace/handle/11228/5166 |
| HSRI-033 | การสังเคราะห์ข้อเสนอเชิงนโยบายเพื่อพัฒนาบทบาทของวิทยาลัยภายใต้พระราชบัญญัติสถาบันพระบรมราชชนกในการสร้างความเข้มแข็งของบุคลากรสาธารณสุขสำหรับการสนับสนุนทีมหมอครอบครัว | อติญาณ์ ศรเกษตริน | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/5261; contract 62-058; id hs2597 | 2563 | Technical Report | 165 | `e673a1e7d0b23a48d0c9ee91e5a40faed1336718fd31c54c45fe5140ba13ccd7` | https://kb.hsri.or.th/dspace/handle/11228/5261 |
| HSRI-034 | การวิจัยพัฒนารูปแบบและแนวทางการจัดบริการแบบบูรณาการโดยยึดประชาชนเป็นศูนย์กลางของเครือข่ายบริการปฐมภูมิ | ดวงดาว ศรียากูล | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/5212; contract 62-028; id hs2563 | 2563 | Technical Report | 74 | `555006d557b20fbe4cd6114c40f4e18b6860e962dfdced1cacd64d6ed3dc326d` | https://kb.hsri.or.th/dspace/handle/11228/5212 |
| HSRI-035 | การพัฒนาสภาพแวดล้อมภายในที่พักอาศัยเพื่อการฟื้นฟูผู้สูงอายุภาวะซึมเศร้า | นวลวรรณ ทวยเจริญ | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/5143; contract 61-029; id hs2528 | 2563 | Technical Report | 748 | `667ed07ff1d42cc0068040bda4cf6974139466c6f9ff77a5f98b2fd1a0a132ab` | https://kb.hsri.or.th/dspace/handle/11228/5143 |
| HSRI-036 | การศึกษาผลการรักษาทางคลินิก คุณภาพชีวิตและความคุ้มค่าคุ้มทุนของผู้ป่วยที่ได้รับการผ่าตัดเพื่อเปิดทางระบายน้ำจากช่องหน้าลูกตาไปใต้เยื่อบุตา (Trabeculectomy) เทียบกับการใช้ยาลดความดันตา | ปริญญ์ โรจนพงศ์พันธุ์ | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/5177; contract 60-043; id hs2543 | 2563 | Technical Report | 74 | `f3063b41c518ad6ec3c8b2da78ef8294286e734242566c437195b6df30751e60` | https://kb.hsri.or.th/dspace/handle/11228/5177 |
| HSRI-037 | การประกันสุขภาพและความล่าช้าในการเข้าถึงและรับการดูแลรักษาของผู้ป่วยวัณโรคที่เป็นแรงงานข้ามชาติชาวพม่าในพื้นที่ชายแดนของประเทศไทย | ทิพวรรณ เลียบสื่อตระกูล | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, THAIHEALTH | hdl 11228/5345; contract 62-082; id hs2658 | 2564 | Technical Report | 66 | `a678743787d3c044307da74d9c9e5ee280eee658b6917eb513ef206064bcd157` | https://kb.hsri.or.th/dspace/handle/11228/5345 |
| HSRI-038 | การประเมินผลเชิงพัฒนา (Developmental Evaluation) โครงการนำร่องผู้ป่วยรับยาที่ร้านยาเพื่อลดความแออัดในโรงพยาบาลกาฬสินธุ์ | กรแก้ว จันทภาษา | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, NHSO | hdl 11228/5464; contract 63-031; id hs2741 | 2564 | Technical Report | 58 | `9166a216ca47c72cb3c5c7895f7d0c65c2dbf2aa4ac588237d853fbaa310b320` | https://kb.hsri.or.th/dspace/handle/11228/5464 |
| HSRI-039 | การศึกษาปัจจัยที่มีส่วนร่วมและกลไกในระดับโมเลกุลที่ส่งผลให้เชื้อวัณโรคดื้อยาหลายขนานสายพันธุ์ Beijing ST10 กาญจนบุรี ซึ่งเป็น clonal outbreak MDR-TB strain มีความสามารถพิเศษในการแพร่เชื้อและก่อโรคได้ดีกว่าสายพันธุ์อื่นในประเทศไทย (ปีที่ 2) † | มาริสา พลพวก | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/5366; contract 63-039; id hs2680 | 2564 | Technical Report | 88 | `e60c7221fec0924d63848e63b9116dc26547cf9db12ea3782a6eef7fe22cbe76` | https://kb.hsri.or.th/dspace/handle/11228/5366 |
| HSRI-040 | การพัฒนาคุณภาพการดูแลผู้ป่วยวัณโรคดื้อยาหลายขนานโดยใช้ระบบทะเบียนวัณโรคแบบอิเล็กทรอนิกส์ | ณสิกาญจน์ อังคเศกวินัย | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/5303; contract 62-010; id hs2631 | 2564 | Technical Report | 51 | `27fe1c974ed91e80430f64b6f0e026e32df0f09197f8d7d52b802f7234a230d8` | https://kb.hsri.or.th/dspace/handle/11228/5303 |
| HSRI-041 | การสังเคราะห์ข้อเสนอเชิงนโยบายในการพัฒนากำลังคนด้านการพยาบาล: การผลิต การกระจาย การธำรงรักษา เพื่อตอบสนองต่อสถานการณ์การระบาดของโรคระบาดใหญ่ | อติญาณ์ ศรเกษตริน | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/5532; contract 64-021; id hs2777 | 2565 | Technical Report | 168 | `137acc601ca74d398340fb56505b3b68f6b2b68456e4f761227fbe9993c1617c` | https://kb.hsri.or.th/dspace/handle/11228/5532 |
| HSRI-042 | การศึกษาปัจจัยที่มีผลต่อคุณภาพชีวิตแพทย์และพยาบาลห้องฉุกเฉินในโรงพยาบาลภาครัฐและเอกชนที่ได้รับผลกระทบจากโควิด-19 ในเขตพื้นที่ EEC | พัชร์วลีย์ นวลละออง | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/5503; contract 64-070; id hs2770 | 2565 | Technical Report | 191 | `b442e3dd87148f86f2d6c19e3e47a2b12ad95cd4973fa8d48034a48be7dbf8a0` | https://kb.hsri.or.th/dspace/handle/11228/5503 |
| HSRI-043 | การศึกษาประเด็นท้าทายเพื่อพัฒนากรอบการติดตามและการประเมินผลของนโยบายวัคซีนโควิด-19 ในประเทศไทย | วรรณฤดี อิสรานุวัฒน์ชัย | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, NRC, TRF_SRI | hdl 11228/5605; contract 64-061; id hs2812 | 2565 | Technical Report | 214 | `2f9b68b2727ab6eefaa570511ed6f845f1fafd4855e27dd934e93842e5eef267` | https://kb.hsri.or.th/dspace/handle/11228/5605 |
| HSRI-044 | การทบทวนวรรณกรรมค่าอรรถประโยชน์ด้านสุขภาพสำหรับผู้ป่วยโรคมะเร็งในประเทศไทย | กฤตภาส กังวานรัตนกุล | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/5486; contract 64-066; id hs2753 | 2565 | Technical Report | 84 | `679b900d0ed6c696cb9e5b37c97a71fa4ac7066d3d89d29a79f51b9a70f52297` | https://kb.hsri.or.th/dspace/handle/11228/5486 |
| HSRI-045 | การพัฒนาระบบระเบียนสุขภาพอิเล็กทรอนิกส์ส่วนบุคคล (Personal Health Record : PHR) เชื่อมต่อโปรแกรมการจัดการข้อมูลวัคซีนโควิด-19 ในพื้นที่เขตสุขภาพที่ 9 † | มานิตา พรรณวดี | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/5830; contract 64-074; id hs2947 | 2566 | Technical Report | 158 | `73bc55b9413a69997bb9ad80d8c1943ef5f39dddaf60eeb1c6eb477f750c2bb3` | https://kb.hsri.or.th/dspace/handle/11228/5830 |
| HSRI-046 | รูปแบบการเสริมสร้างพลังชุมชนเพื่อป้องกันการระบาดใหม่ของโรคโควิค-19 ในพื้นที่ชายแดนภาคตะวันตกของประเทศไทย | ภารณี นิลกรณ์ | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/5993; contract 66-007; id hs3053 | 2566 | Technical Report | 209 | `c17a8c44c1c2c7ca72fce1dd10b8f1c0858f96931c69decb1b1f6d2769174c37` | https://kb.hsri.or.th/dspace/handle/11228/5993 |
| HSRI-047 | การประเมินระบบการดูแลผู้สูงอายุที่กระดูกสะโพกหักที่ผ่าตัดเร็วโดยทีมสหสาขาวิชาชีพในโรงพยาบาลนำร่องของประเทศไทยและผลกระทบของการระบาดของโควิด-19 ต่อระบบการดูแลผู้สูงอายุที่กระดูกสะโพกหัก (ปีที่1) | วราลักษณ์ ศรีนนท์ประเสริฐ | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, NHSO | hdl 11228/5827; contract 64-091; id hs2943 | 2566 | Technical Report | 108 | `7bfa811ebfa145598e7f19b31e6f0326649fad7ea914d7506d48494bed2daa71` | https://kb.hsri.or.th/dspace/handle/11228/5827 |
| HSRI-048 | การพัฒนานวัตกรรมการรักษาด้วยระบบนำส่งพอลิเมอร์เพื่อนำส่งสารสำคัญจากสมุนไพรไทยซึ่งมีเป้าหมายต่อการฟื้นฟูเซลล์ต้นกำเนิดควบคู่กับการประยุกต์ใช้ความรู้ทางด้านเภสัชจลนศาสตร์ และเภสัชพลศาสตร์ | กอบธัม สถิรกุล | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/5875; contract 64-043; id hs2976 | 2566 | Technical Report | 129 | `a3e20a55ee14b8d230680db72b4093539fdcb20ac88824c80afd42f88333f43c` | https://kb.hsri.or.th/dspace/handle/11228/5875 |
| HSRI-049 | การวิเคราะห์ระบบเฝ้าระวังและป้องกันการฆ่าตัวตายที่ใช้ชุมชนเป็นฐานเพื่อการขยายผลด้วยกรอบแนวคิด CFIR, RE-AIM และ NPT | มธุรส ทิพยมงคลกุล | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/6017; contract 66-010; id hs3078 | 2567 | Technical Report | 101 | `654a4a6e912e4a2e8506cd6cfa34fecbef00392c4ad580d3ee5df4f09efb8f85` | https://kb.hsri.or.th/dspace/handle/11228/6017 |
| HSRI-050 | ปัจจัยที่มีผลต่อพฤติกรรมการป้องกันโรคในช่วงการระบาดเเละหลังการระบาดของโรคโควิด-19 ในบุคลากรกรมควบคุมโรค กระทรวงสาธารณสุข | วาสินี ชลิศราพงศ์ | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/6013; contract 66-021; id hs3075 | 2567 | Technical Report | 116 | `8571211bc0a6bdf9f116dd6503f68bc816e25d8b45d6cb28ad748e64f8fa66e3` | https://kb.hsri.or.th/dspace/handle/11228/6013 |
| HSRI-051 | การประเมินผลการให้บริการรักษาอาการเจ็บป่วยเล็กน้อยของร้านยาในระบบหลักประกันสุขภาพแห่งชาติ | สุณี เลิศสินอุดม | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, NHSO | hdl 11228/6056; contract 66-059; id hs3088 | 2567 | Technical Report | 203 | `e64fb4e0a1c853bdafb97e8cf765279294d116f9c74ed4d03fccf8220f3aa557` | https://kb.hsri.or.th/dspace/handle/11228/6056 |
| HSRI-052 | การพัฒนาต้นแบบระบบความปลอดภัยทางทะเล ณ ตำบลเกาะเต่า จังหวัดสุราษฎร์ธานี | ประสิทธิ์ วุฒิสุทธิเมธาวี | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, NRC | hdl 11228/6098; contract 66-093; id hs3129 | 2567 | Technical Report | 90 | `bdc8501d6cfc50e2a711e4ac3a5c7a89142983d9867a96017dc6f970f503162c` | https://kb.hsri.or.th/dspace/handle/11228/6098 |
| HSRI-053 | การพัฒนาศักยภาพของกรรมการจริยธรรมที่เป็นผู้แทนภาคประชาชน (layperson) ระยะที่ 2 | จันทรา เหล่าถาวร | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/6237; contract 67-045; id hs3243 | 2568 | Technical Report | 178 | `6e0264d174fdda81783daa6e045cab9a1df054ca882bc3c789f9bd4c6acfe4cd` | https://kb.hsri.or.th/dspace/handle/11228/6237 |
| HSRI-054 | การถอดบทเรียนเพื่อนําไปสู่ข้อเสนอแนะเพื่อพัฒนานโยบายการบําบัดทดแทนไตภายใต้ระบบหลักประกันสุขภาพแห่งชาติ | ยศ ตีระวัฒนานนท์ | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, NHSO | hdl 11228/6242; contract 67-067; id hs3245 | 2568 | Technical Report | 138 | `9a34124393305cca4310453ae0de330ab88d48b91d613b5dd28bdbd85a440033` | https://kb.hsri.or.th/dspace/handle/11228/6242 |
| HSRI-055 | การศึกษาการออกฤทธิ์ของสารสกัดจากพืชสมุนไพร เพื่อใช้ในการรักษาผู้สูงวัยที่มีภาวะกระดูกพรุนและภาวะมวลกล้ามเนื้อน้อย | ยุทธนา เพ็งแจ่ม | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, TRF_SRI, UNIV_INCOME | hdl 11228/6238; contract 66-016; id hs3238 | 2568 | Technical Report | 92 | `65894f6ef27d5f8e9cdee7b8f0bff6bc823ae34d02eb6e47de02d231aa3cc716` | https://kb.hsri.or.th/dspace/handle/11228/6238 |
| HSRI-056 | ความเปราะบางและปัจจัยเสี่ยงที่เกี่ยวข้อง ประสิทธิผลของโปรแกรมการออกกำลังกายด้วยเครื่องฝึกเดินไอวอร์ค (I-walk) และโปรแกรมการออกกำลังกายที่บ้านต่อความสามารถในการเคลื่อนไหวของผู้สูงอายุไทยในจังหวัดปทุมธานี (ปีที่ 2) | พัชรี คุณค้ำชู | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/6260; contract 66-114; id hs3252 | 2568 | Technical Report | 71 | `a881793b2725964c864c1b0a3839b30545b8081ffc3b9f5757cd135364dd0674` | https://kb.hsri.or.th/dspace/handle/11228/6260 |
| HSRI-057 | ระบบการดูแลผู้พิการในชุมชน | พนิดา วสุธาพิทักษ์ | not in record | แผนงานพัฒนาระบบสุขภาพชุมชนภายใต้ความร่วมมือระหว่างรัฐบาลไทยกับองค์การอนามัยโลก, สถาบันวิจัยระบบสาธารณสุข | NHSO, THAIHEALTH | hdl 11228/3679; id | 2555 | Document | 51 | `6b6cf2138b4eafcffdfa548c110de6e6c30e115672d6de1eb9414620b4f06a7c` | https://kb.hsri.or.th/dspace/handle/11228/3679 |
| HSRI-058 | การจัดการโรคเรื้อรังในชุมชน | พนิดา วสุธาพิทักษ์ | not in record | แผนงานพัฒนาระบบสุขภาพชุมชนภายใต้ความร่วมมือระหว่างรัฐบาลไทยกับองค์การอนามัยโลก, สถาบันวิจัยระบบสาธารณสุข | NHSO, THAIHEALTH | hdl 11228/3678; id | 2555 | Document | 53 | `d1c91eeb49fc92db24bd054fea54b7b7af5eb642f007b26897f89bf93af670c9` | https://kb.hsri.or.th/dspace/handle/11228/3678 |
| HSRI-059 | ผลกระทบด้านสุขภาพและเศรษฐศาสตร์จากการติดเชื้อดื้อยาต้านจุลชีพในประเทศไทย | ภาณุมาศ ภูมาศ | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, NHSO | hdl 11228/3861; contract 55-030; id hs2027 | 2555 | Technical Report | 49 | `985fe2f79e517cc9ed3ae955c77848d8d421a81d6e08753bbd97affc0ea5e57b` | https://kb.hsri.or.th/dspace/handle/11228/3861 |
| HSRI-061 | การประเมินสมรรถนะระบบหลักประกันสุขภาพในการให้บริการผู้ป่วยโรคสมองขาดเลือด จากหลอดเลือดสมองตีบหรืออุดตัน : กรณีศึกษาโรงพยาบาลธรรมศาสตร์เฉลิมพระเกียรติ | สิรินาฏ นิภาพร | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, NHSO | hdl 11228/4017; contract T56-04; id hs2103 | 2556 | Technical Report | 69 | `2a6f607b441f1609b9f7bfe0a4be4d534fc1cafdde84be326b1d8b1414fda74c` | https://kb.hsri.or.th/dspace/handle/11228/4017 |
| HSRI-062 | แนวคิดและทัศนะต่อความเป็นธรรมของกลไกสำคัญในการอภิบาลระบบสุขภาพ | กฤษฎา บุญชัย | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, NHSO, THAIHEALTH | hdl 11228/3896; contract 55-049; id hs2074 | 2556 | Technical Report | 84 | `d1c796fb58be88df837662d0825285bd26f1e6581c3814695fe1e7467ada5eb1` | https://kb.hsri.or.th/dspace/handle/11228/3896 |
| HSRI-063 | การป้องกันการติดเชื้อดื้อยาในหออภิบาลผู้ป่วย | อะเคื้อ อุณหเลขกะ | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/4265; contract 57-036; id hs2153 | 2557 | Technical Report | 92 | `38eb35072ead8742e19d488d9e8e2bc372ad2f5d501a1d338167e15485e36e2d` | https://kb.hsri.or.th/dspace/handle/11228/4265 |
| HSRI-064 | การจัดลำดับความสำคัญและจัดทำแผนงานวิจัยด้านระบบบริการสุขภาพระดับชาติ | ปิยะ หาญวรวงศ์ชัย | not in record | สถาบันระบบวิจัยสาธารณสุข (สวรส.), สถาบันรับรองคุณภาพสถานพยาบาล (องค์การมหาชน), และคณะแพทยศาสตร์ จุฬาลงกรณ์มหาวิทยาลัย | HSRI | hdl 11228/4414; contract 57-109; id hs2239 | 2557 | Technical Report | 45 | `70734025aaab29235deb0ed0470d527e648abf6f091b5a591ae5b908af856e1b` | https://kb.hsri.or.th/dspace/handle/11228/4414 |
| HSRI-065 | ไท้เก๊กเพื่อการบำบัดฟื้นฟูผู้ป่วยโรคหลอดเลือดสมองเรื้อรัง | มงคล ศริวัฒน์ | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, THAIHEALTH | hdl 11228/4439; contract 58-006; id hs2256 | 2558 | Technical Report | 103 | `40b01812635aacc11f8ff166d35412c23c92cf9f81a27877eb504b5efb5a502f` | https://kb.hsri.or.th/dspace/handle/11228/4439 |
| HSRI-066 | ความพยายามและความสำเร็จของคณะกรรมการกำหนดระบบบริหารยา เวชภัณฑ์ การเบิกจ่ายค่าตรวจวินิจฉัยและค่าบริการทางการแพทย์ † | เดือนเด่น นิคมบริรักษ์ | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, NHSO | hdl 11228/4328; contract 58-042; id hs2206 | 2558 | Technical Report | 98 | `e1269a5f9a5b3d6d1efa0b9b0c5b04d7801841dd158998b246d2c885cb03bc6d` | https://kb.hsri.or.th/dspace/handle/11228/4328 |
| HSRI-067 | การตอบสนองและกลไกการดื้อยาต่อกลุ่มอนุพันธ์ artemisinin และยาต้านมาลาเรียที่ใช้ร่วมในเชื้อ Plasmodium falciparum | มฑิรุทธ มุ่งถิ่น | not in record | สถาบันวิจัยระบบสาธารณสุข | none found | hdl 11228/4668; contract 57-051; id hs2313 | 2559 | Technical Report | 59 | `9d0d199ca8c662ad65bda7e981cef2af15f06c25ab012c3436b7327d4c715ff3` | https://kb.hsri.or.th/dspace/handle/11228/4668 |
| HSRI-068 | การพัฒนาชุดวินิจฉัยโรคพิธิโอซีสในคนและในสัตว์ด้วยวิธีอิมมูโนโครมาโตกราฟฟี | อลิสา (เดือนเพ็ญ) แสนดี | not in record | สถาบันวิจัยระบบสาธารณสุข (สวรส.), สำนักงานพัฒนาวิทยาศาสตร์และเทคโนโลยีแห่งชาติ (สวทช.), สำนักงานคณะกรรมการวิจัยแห่งชาติ (วช), สถาบันวิจัยจุฬาภรณ์, คณะแพทยศาสตร์ โรงพยาบาลรามาธิบดี | HSRI | hdl 11228/4664; contract 57-051; id hs2317 | 2559 | Technical Report | 26 | `8c65092d6f79e3d45176e7c8f8d4293d841828118a89480322a66a70ea0e4fba` | https://kb.hsri.or.th/dspace/handle/11228/4664 |
| HSRI-069 | การศึกษาปัจจัยที่ส่งผลต่อความสำเร็จและแนวทางการขับเคลื่อนการดำเนินงานของคณะกรรมการสาธารณสุขจังหวัด (คสธจ.) | อุไรวรรณ อินทร์ม่วง | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/4828; contract 60-047; id hs2383 | 2560 | Technical Report | 104 | `7e0bea412dd9bf66d8091e287d2b0f94eeb9a88a4a4cd682de2926da4071b70c` | https://kb.hsri.or.th/dspace/handle/11228/4828 |
| HSRI-070 | กรณีศึกษา แนวปฏิบัติที่ดีในการดำเนินการตามกุญแจ PLEASE สู่การเป็น RDU Hospital † | ชัยรัตน์ ฉายากุล | not in record | สถาบันวิจัยระบบสาธารณสุข | none found | hdl 11228/4902; contract 58-048; id hs2424 | 2560 | Technical Report | 30 | `0ef691acc6ee0aeb1956a7e1a48782b893ee843607794b356bbb25ad5642e06c` | https://kb.hsri.or.th/dspace/handle/11228/4902 |
| HSRI-071 | การประเมินผลการนำสู่การปฏิบัติของสามมาตรการเชิงนโยบายของการส่งเสริมสุขภาพสำหรับกลุ่มวัยทำงาน ในระหว่าง ปี 2556 - 2560 | สุณี วงศ์คงคาเทพ | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, NHSO, THAIHEALTH | hdl 11228/5006; contract 60-068; id hs2460 | 2561 | Technical Report | 211 | `4c647137b0cc59699628f4ab6ee50ee100d874e6d8c21f851a378d2e3e6a7a08` | https://kb.hsri.or.th/dspace/handle/11228/5006 |
| HSRI-072 | การศึกษารูปแบบการจ้างงาน แพทย์ ทันตแพทย์ เภสัชกร และพยาบาล ในภาครัฐของประเทศไทยในระยะ 15 ปีข้างหน้า † | กฤษดา แสวงดี | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/4988; contract 61-037; id hs2461 | 2561 | Technical Report | 73 | `23ea7e6f1d3eab7553fb6ab278241c44b3381bae8f21c6c9ed93a4e50af2c037` | https://kb.hsri.or.th/dspace/handle/11228/4988 |
| HSRI-073 | การประเมินความคุ้มค่าและความเป็นไปได้ของบริการตรวจเพทซีทีในประเทศไทย | วิทธวัช พันธุมงคล | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, NHSO | hdl 11228/5179; contract 61-046; id hs2545 | 2562 | Technical Report | 283 | `452ff7d2ef3976e6786e6046258ae19d3bf0392f0c2c5eadb1c61c6fffd8a6e5` | https://kb.hsri.or.th/dspace/handle/11228/5179 |
| HSRI-074 | การศึกษาสถานการณ์และรูปแบบระบบบริการที่เป็นมิตรสำหรับคนต่างด้าวในประเทศไทย | จิราลักษณ์ นนทารักษ์ | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/5437; contract 62-065;62-066; id hs2726 | 2562 | Technical Report | 109 | `6e7ba6e4a1e14284920d26d946c3c2af0c8563680eb065af6535b2338ec282c1` | https://kb.hsri.or.th/dspace/handle/11228/5437 |
| HSRI-075 | ทางเลือกของการบริหารจัดการคลินิกชุมชนอบอุ่นในระบบหลักประกันสุขภาพแห่งชาติในเขตกรุงเทพมหานคร | จิรุตม์ ศรีรัตนบัลล์ | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, NHSO | hdl 11228/5314; id hs2630 | 2563 | Technical Report | 65 | `698c1fef610b28d80b77e424af1da83887e7f190a66f2ffa48796e260cc5a75c` | https://kb.hsri.or.th/dspace/handle/11228/5314 |
| HSRI-076 | ต้นแบบการใช้แอปพลิเคชันคุณลูกเพื่อส่งเสริมสุขภาพเด็กที่คลินิกสุขภาพเด็กดี | รสวันต์ อารีมิตร | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/5323; contract 62-049; id hs2650 | 2563 | Technical Report | 243 | `d79e40a396becc29f9ac18dfa40aea53b8db0179e246a41e4423e34d4c234763` | https://kb.hsri.or.th/dspace/handle/11228/5323 |
| HSRI-077 | การเฝ้าระวังโรคติดเชื้อไวรัสโคโรนา 2019 ในบ่อบำบัดน้ำเสียบริเวณจังหวัดที่พบผู้ป่วยยืนยันการติดเชื้อ | รัตนพร ตั้งวังวิวัฒน์ | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/5530; contract 64-077; id hs2776 | 2564 | Technical Report | 55 | `3fb6faf346e8e84682d8b8924bd95b39ad17e546056cc5d2ee849aae9ed54245` | https://kb.hsri.or.th/dspace/handle/11228/5530 |
| HSRI-078 | การพัฒนาเครื่องมือการประเมินสมรรถนะการดูแลการใช้ยาต้านจุลชีพของนักเรียนแพทย์ เภสัชกร และสัตวแพทย์ก่อนสำเร็จการศึกษาในประเทศไทย | Rungpetch Sakulbumrungsil | not in record | Ministry of Public Health, World Health Organization, Thai Health Promotion Foundation, Health Systems Research Institute, National Health Security Office, Health Intervention and Technology Assessment Program, Food and Drug Administration | HSRI, THAIHEALTH | hdl 11228/5555; contract 63-148; id he0149 | 2564 | Technical Report | 296 | `13b0adae7c9795d06cb8bc37d25cee3d2f78920907a80877eabb2cd6175dcdde` | https://kb.hsri.or.th/dspace/handle/11228/5555 |
| HSRI-079 | เภสัชพันธุศาสตร์ ในผู้ป่วยไทยที่ได้รับการปลูกถ่ายไต | ชาครีย์ กิติยากร, หม่อมหลวง | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/5866; contract 64-142; id hs2967 | 2565 | Technical Report | 30 | `e5720f3824ae4587333c0b6d28201a18ae4bf6aa85841010ca58ea721c591e90` | https://kb.hsri.or.th/dspace/handle/11228/5866 |
| HSRI-080 | แผ่นปิดกะโหลกศีรษะเฉพาะบุคคล ผลิตจากโลหะไทเทเนียมด้วยเทคโนโลยีการพิมพ์ 3 มิติ สำหรับผู้ป่วยกะโหลกศีรษะยุบในการศึกษาวิจัยทางคลินิกแบบหลายสถาบัน | บุญรัตน์ โล่ห์วงศ์วัฒน | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, NHSO | hdl 11228/5818; contract 63-141; id hs2939 | 2565 | Technical Report | 138 | `96eaf7b66419bb885373601b2077def2dae33a5d3c29f2152b786897201b840e` | https://kb.hsri.or.th/dspace/handle/11228/5818 |
| HSRI-081 | ประสิทธิผลการฝึกจัดการความเครียดด้วยวิธีการฝึกหายใจและการฝึกสติต่อหน้าที่บริหารจัดการของสมองและคลื่นไฟฟ้าสมองในกลุ่มพยาบาลวิชาชีพที่ทำงานในเขตสุขภาพที่ 4 | ยงยุทธ วงศ์ภิรมย์ศานติ์ | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/6027; contract 66-026; id hs3080 | 2566 | Technical Report | 156 | `6bdf5cd6f94f8f6544d3f2330745b402e56534b2840e27278c82f68412bdac23` | https://kb.hsri.or.th/dspace/handle/11228/6027 |
| HSRI-082 | การประเมินประสิทธิภาพการขับเคลื่อนธรรมนูญสุขภาพพื้นที่ในการเฝ้าระวังการแพร่ระบาดของโรคโคโรน่าไวรัส-2019 พื้นที่เขตสุขภาพ 10 | ปวีณา ลิมปิทีปราการ | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/6011; contract 66-008; id hs3070 | 2566 | Technical Report | 374 | `99130babc2e3be6790f95c2b83a52875f1684f1230ec9f9a5398e5990215bb84` | https://kb.hsri.or.th/dspace/handle/11228/6011 |
| HSRI-083 | การศึกษาบทบาทหน้าที่ของคณะกรรมการสุขภาพระดับพื้นที่ (กสพ.) ภายหลังการถ่ายโอนโรงพยาบาลส่งเสริมสุขภาพตำบลในองค์การบริหารส่วนจังหวัด : กรณีศึกษาจังหวัดน่าน ระยอง ปราจีนบุรี นครราชสีมา สงขลา และภูเก็ต | ชัญญาวีร์ ไชยวงศ์ | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, NHSO | hdl 11228/6231; contract 67-064; id hs3234 | 2567 | Technical Report | 139 | `f0f78b3177e3396cb2f502b1bc1f858fde829773b2885b5322f5e92a062d6a37` | https://kb.hsri.or.th/dspace/handle/11228/6231 |
| HSRI-084 | การติดตามประเมินผลการจัดระบบบริการสุขภาพผู้สูงอายุติดเตียง และพึ่งพิงระดับปฐมภูมิ ภายหลังการถ่ายโอนโรงพยาบาลส่งเสริมสุขภาพตำบลไปยังองค์การบริหารส่วนจังหวัด | อัจฉราวดี ศรียะศักดิ์ | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI, NHSO | hdl 11228/6230; contract 67-070; id hs3233 | 2567 | Technical Report | 219 | `a6e24dc06d7c3cd778057dd5c91d82a27ed4f38960707b20c2489f964642c195` | https://kb.hsri.or.th/dspace/handle/11228/6230 |
| HSRI-085 | การวิเคราะห์ทางเศรษฐศาสตร์และการประเมินผลตอบแทนทางสังคมของเศรษฐกิจสุขภาพในประเทศไทย | พรพจน์ ศรีดัน | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/6387; contract 68-014; id hs3344 | 2568 | Technical Report | 1067 | `115b62dd40b04657d9d2e386e373ee51d65e1f3c5b2b1bf107132f5d4f0271ba` | https://kb.hsri.or.th/dspace/handle/11228/6387 |
| HSRI-086 | การสำรวจสุขภาพประชาชนไทยโดยการตรวจร่างกาย ครั้งที่ 7 พ.ศ. 2567-2568 † | เริงฤดี ปธานวนิช | not in record | สถาบันวิจัยระบบสาธารณสุข | HSRI | hdl 11228/6360; contract 68-085; id hs3330 | 2568 | Technical Report | 359 | `af19c6cbf3b4d86cca903757a29babc9a9e6f79fd4064ec1ba891576f1f6199f` | https://kb.hsri.or.th/dspace/handle/11228/6360 |
| HSRI-095 | การสร้างภูมิคุ้มกันสำหรับเด็ก เยาวชน และครอบครัว | สุมาลี ประทุมนันท์ | not in record | แผนงานพัฒนาระบบสุขภาพชุมชนภายใต้ความร่วมมือระหว่างรัฐบาลไทยกับองค์การอนามัยโลก, สถาบันวิจัยระบบสาธารณสุข | THAIHEALTH | hdl 11228/3680; id | 2555 | Document | 45 | `109bb5b5c0eef90af9cdc450ad9a5ab800ba78d1a4bedaa97a9fdcf4c80815a0` | https://kb.hsri.or.th/dspace/handle/11228/3680 |

---

### Core Epistemic Structure (role disclosure)

- **Core respondent / experience-based expert:** Yaoharee Lahtee (set the
  goal: 100 funded, public documents to compare against the demo).
- **Interactional expert:** None.
- **AI model(s) used (role only, not authorship):** an AI assistant built
  the catalogue, fetched the files under the rules in §2, ran the
  extractor, did the close reading in §7 and drafted this file. The models
  are named once, in the Core Epistemic Structure footer of `README.md`.
