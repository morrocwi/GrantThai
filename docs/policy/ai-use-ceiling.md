# GrantThai AI-use ceiling

Thai version: [ai-use-ceiling.th.md](ai-use-ceiling.th.md).

**Status: DRAFT.** Written by an AI assistant from a page-by-page extraction
of the guideline and an independent verification of that extraction. It has
not yet had its own independent check (maker is not checker, `GOVERNANCE.md`)
or the founder's approval.

This file is GrantThai's **AI-use ceiling**: the most any AI may do in
GrantThai, whether it helps a researcher use GrantThai or helps build this
repository. It is built on one source, cited by page on every line:

> สำนักงานการวิจัยแห่งชาติ (National Research Council of Thailand), *แนวทางการประยุกต์ใช้ Generative AI อย่างมีจริยธรรมสำหรับนักวิจัย*
> (guidelines for the ethical use of generative AI by researchers), September 2569, 36 pages.
> Called **"the guideline"** or **"GenAI guideline 2569"** below. Bibliographic entry: `docs/sources.md`.

Page numbers are PDF pages; in this document they equal the printed page
numbers. The guideline's text is paraphrased here; the few quoted phrases
are short. The guideline is third-party work and is not reproduced.

## 0. How to read this ceiling

- **G:** gives the guideline's own force for a point, read from its Thai
  wording: ต้อง / ห้าม = MUST / MUST NOT; ควร / ไม่ควร = SHOULD / SHOULD
  NOT; อาจ / สามารถ = MAY. Where the guideline only gives an example
  (เช่น, ตัวอย่าง) this file says so.
- **Stricter** marks a line where GrantThai asks for more than the
  guideline. That extra part is GrantThai's own rule, not the guideline's.
- **GrantThai convention** marks something GrantThai derives that the
  guideline does not state (for example a single risk level).
- **The guideline is guidance.** It calls itself แนวทาง / แนวปฏิบัติ
  (p.2, p.4) and calls its advice to funders good practice for each body
  to adapt (p.21). It does not itself say whether it binds anyone. Whether
  it binds a given researcher is **OPEN**: a funder or institution may make
  it a condition (p.22 item 6 and the sample form on p.34 invite that).
  The statutes it lists on p.14 (the Personal Data Protection Act 2562,
  the Computer Crime Act 2560, the Copyright Act 2537, the Trade Secrets
  Act 2545, and the nuclear, radiation, biological and chemical weapons
  laws) bind on their own, whatever the guideline's status.
- **Scope of the guideline:** generative AI only. It says it does not yet
  cover agentic AI, data-analysis systems, automated systems or hardware,
  and that separate guidance will follow (p.4). GrantThai's AI surfaces
  (an AI agent calling tools) are closer to agentic use. Until the agentic
  guidance exists, GrantThai applies the generative-AI rules as its
  minimum (**OPEN**, see section 12).

## 1. Scope of this ceiling

It applies to:

1. any AI that helps a researcher use GrantThai: the agent skill
   (`skills/grantthai/SKILL.md`), the chat prompt packet, the MCP server
   and the HTTP API, and a chat AI that edits `project.yaml` by hand;
2. any AI that helps build or maintain this repository (`AGENTS.md`);
3. the human-AI research workflow GrantThai's own team uses (section 11).

GrantThai does not police how a researcher works outside GrantThai. It
records what the researcher declares, checks that the declaration is there
and filled in, and says plainly what it cannot check (section 8).

## 2. Stage by stage: what AI may and may not do

The stages match `authoring.ai_use_declaration.tools[].stages`
(`spec/project/project.schema.json`). "review" in that list means reviewing
the project's own drafts, never reviewing someone else's work.

| Stage | AI may (guideline) | AI may not (guideline) | In GrantThai |
|---|---|---|---|
| Idea | help think and suggest directions, as a thinking tool (MAY, p.23) | replace the researcher's academic decisions; the researcher judges soundness, feasibility and correctness (MUST NOT / MUST, p.23) | The researcher states the problem, question and objectives; the AI interviews and drafts. Stage `idea`. |
| Proposal writing | improve language, help draft (MAY, p.23) | copy AI output straight into a proposal (MUST NOT, p.23); use AI content without editing (Don't, p.29); put confidential project data or participants' personal data into public AI (the example given for the MUST on confidentiality, p.23) | Every AI value is `DRAFT`, `ai_draft` / `INFERENCE`, listed in output section 1.5 until the researcher rewrites or adopts it. **Stricter:** each AI value needs the researcher's own substantive edit or explicit adoption (C3); section 1.5 of the output asks for one or the other, field by field. Stage `proposal_writing`. |
| Literature | search, summarise, map knowledge (MAY, p.23) | leave content unchecked (MUST check, p.23); use references without checking they exist and fit (MUST, p.28); invented citations are a known limit (p.24) | The AI never supplies a reference from memory; sources come only from the researcher (`sources`, rule S008 checks they resolve in the file, not that they exist). Stage `literature`. |
| Data | help prepare data under the researcher's control (MAY, p.24, p.29) | generate or alter research data or experimental results, or create or edit factual or primary-data images (MUST NOT, p.11, p.24, p.25); alter data or results to fit a hypothesis (MUST NOT, p.25); put personal data into public AI (MUST NOT, p.14) | Rule **AI002** (REVIEW): a data-bearing record drafted by AI. Rule X003 (BLOCK): an AI draft marked `SOURCE`. Rule **AI003** (REVIEW): personal-data-shaped strings in AI-assisted values. The data warning comes first (section 5.1). Stage `data`. |
| Analysis | pre-process data, pre-analyse large data, draft visualisations, under control (MAY, p.24, p.29) | analyse data or images without checking, or publish unchecked results (MUST NOT, p.25); forget that both random and systematic error occur, and that two runs that agree can mislead (MUST be careful, p.24-25) | GrantThai does no analysis; it holds only the analysis plan. Out of scope for the engine; the stage is declared if used. Stage `analysis`. |
| Writing | help with language and find suitable references (MAY, p.25) | leave AI text unchecked; delegate checking to AI or automated tools; lack real human contribution (inside a framework the researcher MAY consider, p.25-26, whose items are worded as MUST); automated plagiarism (MUST prevent, p.26) | Narrative boxes are written from the researcher's records (`RENDER_FROM`); GrantThai never composes them. Stages `writing`, `language_editing`. |
| Review | nothing, for others' work | upload any part of someone else's manuscript (MUST NOT, p.27); use AI to evaluate or translate it (SHOULD NOT, p.27); in grant review, upload or use AI for any judgement (SHOULD NOT, p.27) | **Stricter:** GrantThai and its skill must never be used to process someone else's proposal or manuscript for evaluation (MUST NOT). GrantThai serves applicants only. |
| Publication | disclose use (MUST, p.10, p.26); illustrations if the journal allows, never mistakable for data, disclosed (MAY with conditions, p.11) | illustrations that could affect key scientific content (MUST NOT, p.25 item 4); GenAI images without disclosure or without a copyright check (Don't, p.29) | The academic-article route prepares a manuscript overview (`build/ACADEMIC_ARTICLE.md`) that the researcher writes the article from; GrantThai submits and publishes nothing. ART005 asks for the in-text AI-use statement, ART009 flags a data-bearing AI illustration, ART011 an undisclosed AI illustration caption, ART007 (BLOCK) an AI listed as an author. The venue's own rules are `NEEDS_VERIFICATION`. Stage `publication` if declared. |

Across every stage, a named human checks every AI output before it is used
or released (G: MUST, p.6 item 1.5; p.9 calls human checking a
“ขั้นตอนบังคับ”, a mandatory step; p.10: at every risk level).

Lines that hold at every stage:

- **C3. No AI text goes into a proposal or paper verbatim or unedited.**
  G: MUST NOT copy directly (p.23); Don't use AI content without editing
  (p.29). **Stricter:** the researcher's own substantive edit or explicit
  adoption of each AI value (the guideline also counts prompt design,
  choosing among outputs and deep integration as human contribution,
  p.26 items 2.3-2.4).
- **C10. No AI-made or AI-altered research data, results or factual
  images; illustrations labelled.** G: MUST NOT (p.11, p.24, p.25);
  illustrations only where allowed, never mistakable for data, disclosed
  (p.11); label them (SHOULD, p.25 item 6).
- **C11. A human checks every reference for existence and fit.** G: MUST
  (p.28). **Stricter:** the AI supplies no reference from memory.
- **C13. Thai-context facts need a source or a check by someone who knows
  the context.** G: SHOULD (p.19 item 4). **Stricter:** MUST, and an
  unsourced Thai fact is written as the literal `NEEDS_VERIFICATION`.

## 3. Disclosure duties

- **C5. Disclose every use, at every stage, including language editing.**
  G: MUST disclose that GenAI was used at any stage, from ideas to language
  editing, with detail suited to the risk (p.10); MUST be able to state the
  tool, the stage, the purpose, how it influenced decisions or conclusions,
  and how it was overseen and checked (p.11 item 2); MUST state clearly
  where and how much, and give more detail when AI shapes results or
  interpretation (p.26 item 3.1). Model, version, prompt and human edits are
  given as examples of detail, and methodology or acknowledgement as places
  where it MAY go (p.12). **Stricter:** GrantThai asks for every item
  (tool, version, stages, purpose, influence, human verification, data
  handling) every time, with no low-risk exemption.
- **Tension kept open (OPEN).** p.11 reads a low-risk score as needing no
  detailed disclosure or acknowledgement, and p.27 notes that some
  publishers do not require disclosure of grammar checks; p.10, p.26 and
  p.30 (Don't: use AI in an important part of the research without
  reporting it) say use is always disclosed. The reading GrantThai uses:
  the fact of use is always disclosed; the amount of detail scales with
  risk. Both readings are recorded here; neither is dropped.
- **C6. A proposal carries an AI Use Declaration.** G: funders SHOULD ask
  for transparency about AI use both in preparing a proposal and in the
  research, without disadvantage to those who disclose (p.7 item 4.6, p.22
  item 6); Appendix A (p.34) is a sample form that funders or institutions
  MAY adapt, kept as evidence for later audit. GrantThai renders the
  declaration as a GrantThai appendix in every route output: section 4.7
  of `build/NRIIS_SUBMISSION.md` (not an NRIIS field; whether NRIIS or a
  call asks for it is `NEEDS_VERIFICATION`), section 4.7 of
  `build/ACADEMIC_ARTICLE.md` (beside the manuscript's own in-text
  statement, `ARTICLE.STATEMENT.AI_USE`, rule ART005) and section 4.5 of
  `build/RESEARCH_CONCEPT_NOTE.md`. **Stricter:** always rendered when AI
  was used.
- **C4. AI is never an author, co-author or credited contributor.** G: an
  AI cannot be an author or co-author because it cannot take responsibility
  (p.23); naming it an author is generally not accepted, and use may be
  explained in methodology or acknowledgement (p.11-12); ICMJE authorship
  criteria (p.5). **Stricter:** no acknowledgement as credit and no commit
  trailer. For this repository, `tools/ci/check_attribution.py` and the
  commit hook enforce it; for a researcher's proposal it is a skill rule
  (non-negotiable 6), which no CI can enforce.
- **Captions on AI images and slides** (G: MUST, p.12 item 3) and
  **journal AI rules** (G: MUST check, p.27; if none, disclose by risk,
  p.12 item 6) apply at publication. GrantThai submits and publishes
  nothing; the academic-article route only reminds the researcher (ART005,
  ART011, and the sub-profile notes, all `NEEDS_VERIFICATION`: the
  journal's own GenAI rule comes first).
- Do not disclose prompts that contain sensitive data (G: SHOULD NOT,
  p.12). The declaration asks for the **type** of data, never the data
  (p.34 item 5), and `log_ref` points to the log instead of holding it.

## 4. Accountability

- **C1. AI drafts and suggests; it does not decide, validate or bear
  responsibility.** G: the researcher MUST be responsible for GenAI output
  (p.6 item 1.3; p.15 item 2.3; p.29 Don't: make GenAI the responsible
  party); do not replace academic decisions (MUST NOT, p.23); the final
  decision is human (MUST, p.18). In GrantThai, AI output tops out at
  `DRAFT`. That `hard_ceiling` is enforced in the core for the programmatic
  surfaces (MCP, HTTP, `assist`, `grantthai set --ai`); for a file a chat
  AI edits by hand, rule X003 and the output's status basis ("no review
  record") cover it.
- **C2. A named human checks every AI output before use or release;
  another AI never substitutes.** G: MUST (p.9: another GenAI may do a
  preliminary check but cannot replace human judgement, because models may
  err in the same direction; p.10: at every risk level; p.25: analysis;
  p.26: inside the framework offered for consideration).
- **C16. Agreement is not validation.** Two AI runs or two models that
  agree are not evidence of correctness. G: p.9 (models may hallucinate in
  the same direction); p.24-25 (systematic error; two agreeing runs can
  mislead; MUST be careful of both random and systematic error). GrantThai
  never counts AI agreement as a check.
- **C12. No AI judging people, eligibility or research quality.** G:
  SHOULD NOT use GenAI to decide the worth of a person, the suitability of
  a group, the ranking of rights or opportunities, or research quality
  automatically (p.18 item 1); for funders, GenAI “ไม่สามารถมีบทบาท”
  (cannot have a role) in academic evaluation (p.22 item 5.2).
  **Stricter:** MUST NOT in GrantThai. The skill never tells a researcher
  the work is sound, novel or fundable, and GrantThai decides no
  eligibility beyond what the bound fund profile states.
- **Declaration of responsibility.** G: in every case the user MUST confirm
  the output was checked, as taking full responsibility (p.12 item 4); the
  sample form ends with the PI's signature and date (p.34 item 8).
  GrantThai: `declaration_confirmed_by_human`, set only by the researcher.
  Any AI surface that adds a tool or a stage resets it to `false`.

## 5. Data: personal, confidential, dual-use and intellectual property

- **C8. Nothing sensitive goes into a public AI.** G: entering data into a
  public GenAI is like sending it to a third party (p.14; p.28). Personal
  data that identifies someone (for example names, national ID numbers,
  health data): MUST NOT (p.14 item 1.1). Dual-use data (for example
  pathogen sequences, methods for toxins or drugs, weapons-related
  engineering models): MUST NOT into public or external GenAI; allowed only
  in a closed system the organisation controls, with approval, a recorded
  reason and oversight (p.15 item 1.4). Other sensitive data: do not put it
  into public AI; closed (enterprise or local) systems only if necessary
  (p.16 item 3.2; p.28 says researchers must avoid personal, sensitive and
  confidential data). Contracts, trade secrets, pre-patent material and
  unpublished data: SHOULD take care, since input may count as public
  disclosure depending on the provider's terms (p.15 item 1.3). Once in,
  data is practically impossible to remove, so the safe default is not to
  input it at all (p.16 item 3.3, “เข้าง่าย ออกยาก”). **Stricter:** in
  GrantThai all of these are MUST NOT for public AI, and every closed-system
  use needs approval and a recorded reason, not only dual-use data.
- **C9. Research on personal data.** G: collect only what is needed, with a
  legal basis (MUST, p.15 item 1.2); anonymise or pseudonymise before input
  (SHOULD, p.15); REC/IRB approval before the research starts (MUST, p.15).
  **Stricter:** anonymisation is MUST, and approval must be in place before
  any AI touches the data.
- **Terms of service.** G: read the provider's terms on data retention and
  training use (SHOULD, p.15 item 3.1); check privacy settings and turn off
  chat-history sharing (SHOULD, p.16 item 3.4). Whether a given account
  counts as a closed system is for a human to check (section 8).
- **Copyright and IP.** G: weigh fair use before inputting copyrighted
  works (SHOULD, p.15 item 1.5); check AI output for plagiarism (SHOULD,
  p.15 item 2.1; MUST prevent automated plagiarism, p.26); no copyright
  subsists in AI-made work under current law, yet the researcher MUST
  answer for all content (p.15 item 2.3); do not publish false or harmful
  AI output (imperative under a SHOULD heading, p.15 item 2.2; liability
  under the Computer Crime Act). GrantThai's rule E009 asks who owns any IP
  the project will use.
- **C10. No AI-made or AI-altered data, results or factual images.** See
  section 2 (Data, Analysis, Publication). Rule **AI002**.

### 5.1 The warning shown before any data is accepted

Before an AI operator accepts any research data from a researcher, it shows
this warning (the text lives once, in `src/grantthai/core/pii.py`, as
`DATA_WARNING_TH` and `DATA_WARNING_EN`), and records the AI tool's name and
version in `authoring.ai_use_declaration`:

- the skill: `python scripts/grantthai_skill.py warning`;
- MCP: the `data_warning` field of the `grantthai_new_project` result and
  the server instructions;
- HTTP: the `data_warning` field of the `POST /projects` response.

Personal data of team members (names, organisations, ORCID) is entered by
the researcher (`grantthai set` without `--ai`, or by editing
`project.yaml`) unless the AI runs locally or under an enterprise agreement
and the researcher agrees. G: p.14 item 1.1, p.23. A dual-use topic stops
the AI drafting: the value is marked `HOLD_FOR_VERIFICATION` and the
researcher decides where to work on it (G: p.15 item 1.4).

## 6. Record keeping

- **C7. Keep a log.** G: SHOULD keep logs and prompts to allow checking
  after the research (p.6 item 1.4); SHOULD record the tool version and the
  date and time of use, prompts with their outputs (outputs are
  non-deterministic), and validation evidence with a log of key changes
  (p.12-13 item 7). **Stricter:** MUST for anything that will be published.
- In GrantThai: `tools[].version`, `tools[].used_on` and `log_ref` (where
  the researcher keeps the log). GrantThai stores no prompt and no chat.
- **C14. Team agreement.** G: a research team SHOULD agree in writing, before
  starting, on the scope of AI use and how it is disclosed (p.12 item 5).
  Kept as SHOULD. GrantThai has no field for it; it is a human duty.

## 7. Where GrantThai is stricter than the guideline

Each row is GrantThai's own rule. None of it is attributed to the guideline.

| Ceiling line | Guideline | GrantThai |
|---|---|---|
| C3 no AI text verbatim | MUST NOT copy directly (p.23); Don't use without edits (p.29); human contribution may be prompt design, choosing among outputs, or deep integration (p.26 items 2.3-2.4) | the researcher's own substantive edit or explicit adoption of every AI value |
| C4 no AI credit | AI cannot be an author (p.23); acknowledgement is one place to disclose (p.12) | no acknowledgement as credit, no commit trailer |
| C5 disclosure | fact of use always; detail by risk (p.10-11) | every item, every time, no low-risk exemption |
| C6 declaration | sample form funders MAY adapt (p.34) | always rendered when AI was used |
| C7 log | SHOULD (p.6, p.12-13) | MUST for anything published |
| C8 sensitive data | MUST NOT personal and dual-use data; SHOULD take care with confidential, unpublished, pre-patent data (p.14-16) | MUST NOT for all of them in public AI; approval and a recorded reason for every closed-system use |
| C9 personal-data research | anonymise SHOULD (p.15) | anonymise MUST; approval before any AI use |
| C11 references | MUST check existence and fit (p.28) | the AI supplies no reference from memory at all |
| C12 judging and reviewing | SHOULD NOT, except uploading a manuscript, which is MUST NOT (p.18, p.27) | MUST NOT |
| C13 Thai context | SHOULD check with someone who knows the context and use Thai sources (p.19 item 4) | MUST, with the literal marker `NEEDS_VERIFICATION` when unsourced |

## 8. Human duties GrantThai cannot check

GrantThai checks shape and links, never truth. These stay with people:

| Duty | Guideline | Why GrantThai cannot check it |
|---|---|---|
| the content is correct | p.9, p.10, p.26 | validators check structure only |
| the researcher edited AI text enough | p.23, p.26 | an edit's substance cannot be measured |
| the declaration is true and complete | p.11-12 | AI001 sees only that it is filled and confirmed |
| the confirmation still covers every AI use | p.12 | it resets when a tool or stage is added, not on every later AI value |
| no personal or confidential data went into an AI chat | p.14-16 | the chat is outside GrantThai; AI003 sees only shapes (ID numbers, phone numbers, e-mail addresses), never names or health details |
| the AI account is a closed system | p.16 | depends on each account's terms |
| REC/IRB approval exists | p.15 | GrantThai records what the researcher states |
| every reference exists and fits | p.28 | S008 checks only that a cited source is in the file |
| logs are kept | p.12-13 | `log_ref` is a pointer |
| plagiarism and copyright checks | p.12, p.15, p.26 | no text comparison is run |
| the team agreed its AI use in writing | p.12 | no field for it |
| the funder's or journal's own AI rules | p.27 | calls differ; `NEEDS_VERIFICATION` |

## 9. How GrantThai enforces it

Four rules, all **REVIEW** (never BLOCK: the guideline's binding status is
OPEN, and GrantThai cannot see whether a declaration is true). Source:
`validators/rules.yaml`, family `AI`. Thai explanations:
`skills/grantthai/reference/rules-th.md`.

| Rule | Fires when | Guideline pages |
|---|---|---|
| AI001 | AI use is recorded but `authoring.ai_use_declaration` is missing, incomplete (a tool without version, stages or purpose; no influence, human verification or data-handling statement), or not confirmed by the researcher | p.6, p.10-12, p.22, p.34 |
| AI002 | a data-bearing record (chain Evidence, Observation or LivedExperience, or source type PRIMARY_DATA) is authored `ai_draft`; extends X003 | p.11, p.24, p.25 |
| AI003 | a value written with AI assistance contains a personal-data-shaped string (checksum-valid Thai national ID, phone number, e-mail address; the same patterns as the repository leak guard, `src/grantthai/core/pii.py`); the finding names the kind, never the string | p.14, p.15, p.23 |
| AI004 | the researcher's own risk self-assessment scores any dimension 3. The single level printed is a **GrantThai convention** (the highest of the five scores); the guideline's table is an example with no rule for combining scores (p.10-11) | p.10-11, p.14-16 |

Mechanisms around the rules:

- Every AI-assisted write (`grantthai set --ai`, MCP `grantthai_set_field`,
  HTTP `PATCH /projects/{id}/fields`, the skill's `apply`) records the tool
  in `authoring.ai_use_declaration.tools`: its name (MCP: the client's
  declared name; HTTP: the `tool` field), its version when declared (MCP:
  the client's declared version), and the stage (default
  `proposal_writing`). Purpose stays `NEEDS_INPUT` for the researcher.
- Only the researcher sets `declaration_confirmed_by_human`, by editing
  `project.yaml`. The skill's answers file refuses it; no MCP or HTTP call
  can set it.
- Output section 4.7 renders the declaration in the shape of Appendix A
  (p.34), labelled as a GrantThai appendix, with the convention level
  labelled as GrantThai's.

## 10. Crosswalk: every normative point of the guideline

`status`: **satisfied** = an existing GrantThai mechanism already meets it;
**new** = added with this ceiling; **partial** = GrantThai meets part of it
and the rest is a human duty (section 8); **out of scope** = it concerns
institutions, funders, reviewers, publication or clinical work, or activity
GrantThai does not perform. N58 is added from the independent verification
of the extraction (points on p.24-25 the first pass left out).

| id | p. | Guideline (modality, paraphrased) | GrantThai mechanism | status |
|---|---|---|---|---|
| N01 | 6 | researchers MUST assess GenAI's limits, bias and risk | optional `risk_self_assessment`; AI004 | partial |
| N02 | 6 | MUST disclose GenAI use, for example the model and purpose | `ai_use_declaration.tools` (name, version, purpose); AI001 | new |
| N03 | 6, 15, 29 | the researcher MUST be responsible for GenAI output; GenAI cannot be the responsible party | `DRAFT` ceiling; X003; human final approval always required; declaration item 10 | satisfied |
| N04 | 6 | SHOULD keep logs and prompts for checking after the research | `log_ref`; C7 (stricter) | partial |
| N05 | 6, 9 | MUST keep a human in the loop; p.9 calls it a mandatory step | AI output caps at `DRAFT`; section 1.5 lists AI values; AI001 confirmation | satisfied |
| N06 | 9 | MAY use another GenAI for a preliminary check; it cannot replace human judgement | validators never validate knowledge; C2, C16 | satisfied |
| N07 | 8-9 | SHOULD ground answers: specific prompts that separate fact from opinion, state confidence and say when information is insufficient; external sources, checked; retrieval from chosen sources; research-specific tools | only the researcher's own sources; `NEEDS_VERIFICATION` / `NEEDS_INPUT` instead of guessing; tool choice is a human duty | partial |
| N08 | 10 | MUST disclose use at any stage, language editing included, with detail by risk; MUST check output before use at every risk level | C5; AI001 | new |
| N09 | 10-11 | example only: five dimensions scored 1-3 and example readings of levels 1-3; no rule for combining them | `risk_self_assessment`; AI004; the level is a GrantThai convention | new |
| N10 | 11, 24, 25 | MUST NOT generate or alter research data, results or factual images; MUST NOT alter data to fit a hypothesis or alter published results | AI002 (REVIEW); X003 (BLOCK); no gap-filling (skill non-negotiable 4) | new |
| N11 | 11, 25 | MAY make illustrations if the journal allows, never mistakable for primary data, checked and disclosed; MUST NOT make illustrations that could affect key scientific content (p.25 item 4); SHOULD label them (p.25 item 6) | GrantThai makes no images | out of scope |
| N12 | 11-12 | MUST be able to state tool, stage, purpose, influence on conclusions and oversight (p.11); MAY say so in methodology or acknowledgement, with model, version, prompt and human edits as examples (p.12) | declaration fields and section 4.7 | new |
| N13 | 5, 11-12, 23 | AI cannot be an author or co-author because it cannot take responsibility (p.23); naming it an author is generally not accepted (p.11-12); ICMJE criteria (p.5) | stricter C4; repository CI; skill non-negotiable 6 for proposals | satisfied |
| N14 | 12 | SHOULD NOT disclose prompts containing sensitive data | declaration asks for data type only; `log_ref` is a pointer | new |
| N15 | 12 | MUST caption AI-made slides, posters and images; SHOULD check the licence; MUST check for copying | GrantThai makes no slides or images | out of scope |
| N16 | 12 | MUST give enough detail to reproduce without revealing sensitive prompts; the user MUST confirm the output was checked | `declaration_confirmed_by_human`; AI001 | new |
| N17 | 12 | a team SHOULD agree in writing on AI use and disclosure before starting | C14; human duty (no field) | out of scope |
| N18 | 12, 27 | authors MUST check the journal's GenAI rules (p.27); if there are none, disclose by risk (p.12) | GrantThai submits and publishes nothing. The academic-article route prepares a manuscript overview only: ART005 asks for the in-text AI-use statement and cites p.27; the thai-journal and international-journal sub-profiles say the journal's own GenAI rule comes first. The journal's and the call's own rules are `NEEDS_VERIFICATION` | partial |
| N19 | 12-13 | SHOULD record tool version and date, prompts and outputs, validation evidence and key changes | `tools[].version`, `tools[].used_on`, `log_ref`; C7 | partial |
| N20 | 14 | MUST assess data risk before use, choose a suitable model, check the output's lawfulness, and protect sensitive data and IP under Thai law | data warning (section 5.1); `data_handling` | new |
| N21 | 14, 28 | entering data into public GenAI is like sending it to a third party | stated in the data warning | new |
| N22 | 14 | MUST NOT put identifiable personal data into public GenAI | data warning; AI003; team data entered by the researcher | new |
| N23 | 15 | MUST collect only what is needed with a legal basis; SHOULD anonymise before input; MUST have REC/IRB approval before research on personal data | C9 (stricter); ethics fields exist (`METHOD.PLAN.ETHICS`); approval is a human duty | partial |
| N24 | 15 | SHOULD take care with confidential, trade-secret, pre-patent and unpublished material (may count as public disclosure) | data warning, stricter (do not) | new |
| N25 | 15 | MUST NOT put dual-use data into public or external GenAI; MAY use a closed organisational system with approval, a recorded reason and oversight | data warning; the skill stops and marks `HOLD_FOR_VERIFICATION` | new |
| N26 | 15 | SHOULD weigh fair use before inputting copyrighted works | human duty | out of scope |
| N27 | 15 | SHOULD check GenAI content for plagiarism before use | human duty (section 8) | out of scope |
| N28 | 15 | do not publish false GenAI output with fraudulent intent, or harmful output (imperative under a SHOULD heading; liability under the Computer Crime Act) | GrantThai publishes nothing | out of scope |
| N29 | 15 | no copyright in AI-made work under current law, but the researcher MUST answer for all content | declaration item 10; C1 | satisfied |
| N30 | 15-16, 28 | SHOULD read the provider's terms on retention and training; do not put sensitive data into public AI (p.16; p.28 must avoid); closed systems only if necessary; SHOULD turn off chat-history sharing | data warning; reading terms is a human duty | partial |
| N31 | 17-18 | SHOULD NOT assume AI output is neutral; tool, not arbiter; SHOULD NOT let it decide on persons, groups, rights or research quality; the final decision MUST be human | skill never judges soundness, novelty or fundability; no eligibility decision beyond the fund profile; C12 | satisfied |
| N32 | 18-19 | MAY reduce bias by triangulation, neutral prompts, review by context-holders, comparing models and prompts (each SHOULD) | human duty; C16 | out of scope |
| N33 | 19 | SHOULD have Thai-context output checked by someone who knows the context, and use Thai sources | stricter C13: `NEEDS_VERIFICATION` for any unsourced Thai fact (AGENTS.md non-negotiable 3) | satisfied |
| N34 | 19 | SHOULD consider unequal access to tools and skills, for example in the limitations section | AI is optional everywhere; every task has a no-AI path (AGENTS.md non-negotiable 1) | satisfied |
| N35 | 23 | MAY use GenAI to search, summarise, map knowledge, edit language and generate ideas | the skill's interview and drafting, capped at `DRAFT` and disclosed | satisfied |
| N36 | 23 | MUST NOT copy GenAI text straight into a proposal or article; MUST NOT replace academic decisions; the researcher MUST judge soundness | section 1.5 lists AI values; explicit adoption; C3 (stricter); the edit itself is a human duty | partial |
| N37 | 23 | MUST keep confidentiality in mind; not inputting confidential project data or participants' personal data into public GenAI is the example given | data warning; team data entered by the researcher | new |
| N38 | 24 | MUST disclose each use in designing experiments or models; SHOULD say which part and method, tool, version, date and how | declaration stages and tools; GrantThai designs no experiments | partial |
| N39 | 25 | MUST NOT analyse data or images without checking or publish unchecked results; SHOULD disclose in the methodology (p.25 item 7) | GrantThai performs no analysis | out of scope |
| N40 | 25-26 | inside a three-point framework the researcher MAY consider: authors MUST check, correct and confirm AI text themselves, compare it with reliable sources, not delegate checking to GenAI or automated tools, and answer for the whole work | validators never validate knowledge; C2 rests on p.9 and p.10 | satisfied |
| N41 | 26 | same framework: substantial human contribution; a short prompt with unedited output does not count; prompt design, choosing among outputs and deep integration do count (items 2.3-2.4); MUST prevent automated plagiarism | C3 (stricter reading); human duty | partial |
| N42 | 26 | SHOULD keep disclosure proportionate to the field; MUST state clearly where and how much; MUST give more detail when AI shapes results or interpretation; SHOULD reach an Open Science level | `influence_on_conclusions`; AI004 | new |
| N43 | 27 | reviewers MUST NOT upload any part of a manuscript to GenAI | C12 (stricter): GrantThai is never used on others' work | out of scope |
| N44 | 27 | reviewers SHOULD NOT use GenAI to evaluate or translate a manuscript | C12 (stricter) | out of scope |
| N45 | 27 | grant reviewers SHOULD NOT upload or use GenAI for any judgement | C12 (stricter) | out of scope |
| N46 | 28 | MUST check that GenAI-produced references exist and fit the content | the skill supplies no reference from memory; S008 checks resolution in the file only; existence is a human duty | partial |
| N47 | 30 | clinical research: GenAI for preliminary information only; MUST NOT predict diagnosis or decide treatment without expert review and ethics approval; MUST NOT enter patient identifiers into public AI | GrantThai is not a clinical tool; the data warning covers identifiers | out of scope |
| N48 | 6, 20-21 | institutions MUST govern GenAI use strictly (p.20); listed measures without a modal: policy aligned with national policy and reviewed regularly, secure tools (own tools SHOULD have cybersecurity certification), training, mentoring, monitoring and audit, clear sanctions | institutional | out of scope |
| N49 | 20 | institutions SHOULD provide a sandbox for high-risk work; use inside it MUST be under human oversight; high-risk work SHOULD be approved and MUST pass accuracy, fairness and limitation checks before publication; a sandbox does not replace the researcher's responsibility | institutional | out of scope |
| N50 | 20 | institutions SHOULD define a pre-use risk assessment for every stage (impact, accuracy, sensitivity, bias, reproducibility) and use it to set disclosure, sandbox use and expert review | institutional; AI004 shows the researcher's own scores | out of scope |
| N51 | 6 | ethics committees review GenAI use in human-subject and sensitive-data work, set conditions, and guard against rights violations and bias | committee role | out of scope |
| N52 | 7, 21-22 | funders and regulators SHOULD set policy and standards (OECD, UNESCO, EU AI Act), security requirements, require legal compliance, fund training and set sanctions (offered as good practice, p.21) | funder role | out of scope |
| N53 | 7, 22 | funders SHOULD require transparency about AI use in preparing proposals and in research, without disadvantage to those who disclose | section 4.7 is ready if a call asks; whether it does is `NEEDS_VERIFICATION` | new |
| N54 | 22 | a funder's own GenAI use: human oversight and transparency; GenAI cannot have a role in evaluating academic content; tool choice MUST weigh quality, transparency, data protection and IP | funder role | out of scope |
| N55 | 34 | sample AI Use Declaration for a proposal or article: title, responsible person, tool with developer and version, purpose, type of data input (not the raw data), prompt, settings, code or output (or an attachment), validation measures (who checks, who signs), signature and date; funders or institutions MAY adapt it; kept as audit evidence | section 4.7 follows its order; signature is `declaration_confirmed_by_human` with `confirmed_by` and `confirmed_on` | new |
| N56 | 35-36 | the National Science and Technology Development Agency's AI Disclosure Statement: within its own practice it MUST be attached; a checklist of use types and a signed statement | another institution's form; the researcher uses it if their institution asks | out of scope |
| N57 | 30 | the guidance SHOULD be reviewed regularly as technology, law and standards change | C15: this ceiling is reviewed when the guideline changes or agentic guidance appears | new |
| N58 | 24-25 | known limits: training-data bias, sycophantic answers shaped to what the user seems to want, invented citations, black-box answers that call for cross-validation; random and systematic error; two agreeing runs may be wrongly taken as correct; the researcher MUST be careful of both kinds of error | C16; the skill supplies no citations; AI output is never evidence (X003, AI002) | new |

Other points recorded, none of which changes the ceiling: the stakeholder
groups on p.7 also name the public, research participants and end users
(to receive accurate, transparent information) and AI developers and
providers (responsible for safety and transparency, supporting licence
compliance); p.21 item 4 asks institutions to promote GenAI research for
the Thai language and context; p.22 items 5.1-5.3 put a funder's own AI
use under human oversight; p.29 asks that data analysis record the method
and tools used.

## 11. For our own Human-AI research workflow (glosa P20, P06, P10)

GrantThai's team also produces research with AI. The guideline read against
the glosa methodology (<https://github.com/morrocwi/glosa>), relayed from the
extraction and its independent verification:

| Point | Finding | Why |
|---|---|---|
| P20 names each AI model with its role, never as author (N02, N13) | compliant, stricter | every model is named, not "AI was used", and roles are separated |
| P20 lacks version, date of use, stage, a log reference and a statement that a human checked (N12, N16, N19) | **gap** | proposed: an "AI Use Detail" line after the role block (dates, stages, log reference, human check) |
| P07 discloses next to the AI-filled text, not in one closing paragraph (N12, N42) | compliant, stricter | more precise than the guideline's sample statements |
| P06 many models are not independence (N06) | compliant | matches p.9: models may err in the same direction |
| P06 lets an AI checker at I2/I3 set `PASSED` toward K1 when a human approver exists | **risk of conflict** with p.9 (another AI cannot replace human judgement) and the p.26 framework | a publication approval is not a content check; proposed: publishing research needs a record that a human checked the content, never an AI checker in its place |
| P10 R1 leak scan and R4 citation accuracy (N14, N22, N46) | compliant | |
| P10 rejects outside authority as the source of legitimacy | no conflict | the guideline asks for context-holders' review (p.19), not outside validation as legitimacy |
| logs: decision notes and handoffs exist, but no per-artifact prompt and output log (N19) | partial | C7 asks for it for anything published |
| agentic use (tool-calling agents, subagents) | **OPEN** | excluded from the guideline (p.4); the generative-AI rules apply as the minimum |
| files sent to cloud models (N21, N30) | **OPEN** | whether an account counts as closed or enterprise (p.16) depends on its terms, not yet checked; personal or health data needs anonymisation and REC approval first |

## 12. Open items

1. The disclosure tension between p.10, p.26, p.30 and p.11, p.27
   (section 3). Both readings are kept.
2. How the five risk scores combine. The guideline gives no rule; the
   single level GrantThai prints is its own convention.
3. Whether the guideline binds a given researcher (section 0).
4. The agentic-AI scope (p.4).
5. Whether NRIIS or a call has a field or attachment for an AI
   declaration: `NEEDS_VERIFICATION`.
6. Ethics committees' own AI use and AI in teaching: not addressed by the
   guideline.
7. Whether a given AI account is a closed or enterprise system (p.16).
8. The guideline's public download address is not recorded yet
   (`docs/sources.md`): `NEEDS_VERIFICATION`.

## 13. Review of this ceiling

- **C15.** Review this ceiling when the guideline is revised (G: guidance
  SHOULD be reviewed regularly, p.30) or when agentic-AI guidance appears
  (p.4). Until then the generative-AI rules are the minimum for agentic use.
- Where each line is: C3, C10, C11, C13 in section 2; C4, C5, C6 in
  section 3; C1, C2, C12, C16 in section 4; C8, C9 in section 5; C7, C14 in
  section 6; C15 here. Section 7 lists every line that is stricter than the
  guideline.
