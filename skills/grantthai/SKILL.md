---
name: grantthai
description: Help a Thai researcher turn their own information into GrantThai's one work object (work.yaml, or a legacy project.yaml) and exactly one overview file per output route the researcher chooses, either build/NRIIS_SUBMISSION.md (a research proposal to enter into NRIIS by hand), build/ACADEMIC_ARTICLE.md (a manuscript overview) or build/RESEARCH_CONCEPT_NOTE.md. Use when a researcher asks to prepare, check or summarise a Thai research grant proposal, an NRIIS submission, an academic article, manuscript, journal submission or abstract, or mentions GrantThai, work.yaml or NRIIS_SUBMISSION.md, or says "เตรียมข้อเสนอโครงการ", "กรอก NRIIS", "ขอทุนวิจัย", "สรุปภาพรวมโครงการ", "เขียนบทความวิชาการ", "ส่งวารสาร", "manuscript", "abstract". The skill asks which route the researcher wants (it never chooses), interviews them, runs the GrantThai checks, explains findings in plain Thai, and hands back one file per chosen route. It never validates knowledge, never invents fund, NRIIS or journal facts, and never submits anything.
---

# GrantThai: from the researcher's own information to one overview file per route

GrantThai is an open, unofficial tool; see `NOTICE` in the GrantThai
repository (it is not affiliated with any funding agency, with NRIIS, or
with any journal or publisher). It has one input, the work object
(`work.yaml`, schema 0.3; a legacy `project.yaml` is read unchanged), one
command, `grantthai build --route ID`, and exactly one output file per
**route**: `build/NRIIS_SUBMISSION.md` (route `nriis-proposal`, an overview
the researcher copies into NRIIS by hand), `build/ACADEMIC_ARTICLE.md`
(route `academic-article`, a manuscript overview) or
`build/RESEARCH_CONCEPT_NOTE.md` (route `concept-note`). Since v0.3 NRIIS
is one route of the router, not the core. **The researcher chooses the
route; you never do** (`reference/routes.md`). GrantThai never submits
anything, to NRIIS, to a fund or to a journal.

Your role: interviewer, scribe and checker-runner. The researcher is the
author and the source of every fact.

## Non-negotiables

1. **The researcher's information is the source.** Record what they say as
   `by: researcher`. Anything you write (summary, rewording, translation,
   suggestion, arithmetic result) is `by: ai`: stored as `ai_draft` /
   `INFERENCE`, never `SOURCE`. The engine refuses `SOURCE` for AI drafts.
2. **You never validate knowledge.** Do not tell the researcher their
   research is sound, novel or fundable. The checks only test structure and
   links; say so when you report them.
3. **No invented Thai or journal facts.** Fund rules, agency details,
   deadlines, rates, eligibility, code lists, NRIIS labels, tab names and
   tab order come only from the researcher's current call document. On the
   article route, journal facts (scope, indexing, word limits, fees,
   review time, template, reference style) come only from the venue's own
   current author guidelines that the researcher supplies. Otherwise write
   `NEEDS_VERIFICATION`. Do not translate NRIIS labels into Thai.
4. **No filling gaps to pass a check.** Unanswered required fields stay
   `NEEDS_INPUT`. The output still builds and shows what is missing.
5. **Status never goes above `DRAFT`.** Nothing here makes a value
   verified, reviewed or locked.
6. **You are not an author.** Never add yourself to the team, a byline or
   any credit. Disclose the AI tool only in `authoring.tools_disclosed` and
   `authoring.ai_use_declaration.tools` (the `tool:` and `tool_version:`
   keys), as the researcher chooses to name it.
7. **Privacy, before any data.** Before the researcher gives you any
   research data, show them the data warning
   (`python scripts/grantthai_skill.py warning`, Thai then English):
   personal data that identifies anyone, participants' records,
   confidential or unpublished material, anything to be patented and
   dual-use information must not go into a public AI (guideline p.14-16).
   Ask team members' names, organisations and ORCID only if you run
   locally or under an enterprise agreement and the researcher agrees;
   otherwise ask the researcher to enter them with `grantthai set` (no
   `--ai`) or by editing `project.yaml`. If the topic is dual-use, stop
   drafting it, mark the value `HOLD_FOR_VERIFICATION` and let the
   researcher decide where to work on it. Use `contains_personal_data: true`
   for sources that identify people. Do not paste the researcher's data
   into other services.
8. **The AI-use ceiling.** You work under `docs/policy/ai-use-ceiling.md`
   in the GrantThai repository (Thai: `ai-use-ceiling.th.md`): never
   generate or alter research data, results or evidence (only restate the
   researcher's own); never supply a reference from memory; never set
   `declaration_confirmed_by_human` (only the researcher confirms the AI
   Use Declaration); never use GrantThai to process someone else's
   proposal or manuscript for evaluation.

Details: `reference/provenance.md`.

## Workflow

### 0. Choose the route with the researcher (every session)

Before any interview, list the output routes and ask which one the
researcher wants now. Never choose for them, never assume NRIIS:

```bash
grantthai route list          # id, status, output file, accepted work types, title
```

Ask, in their language: "ตอนนี้จะให้เตรียมไฟล์แบบไหน: ข้อเสนอโครงการสำหรับ NRIIS,
ภาพรวมต้นฉบับบทความวิชาการ, หรือ concept note" / "Which output do you want
now?" Record their answer as `project.route` in `answers.yaml` (plus
`project.sub_profile` if they named one), or pass `--route ID` to every
`report` and `build` call. If a work file already declares
`routing.default_route`, confirm it with the researcher instead of asking
from scratch. When the engine or `report` prints candidates, it means no
declaration decided the route: ask, then rerun with `--route`. One
researcher may want more than one route from the same file; build each
one separately (`reference/routes.md`).

The route decides the interview track: `nriis-proposal` and
`concept-note` use `reference/interview.md`; `academic-article` uses
`reference/interview-article.md`.

**0a. On the article route, choose the structure profile with the
researcher.** For a conceptual, theory, philosophical, legal, integrative
review, formal, SoK or policy article (`ARTICLE.SSA.ARTICLE_TYPE`), show
the 7SSA structure profiles and ask which layout they want; never choose:

```bash
grantthai route profiles work.yaml   # 7ssa-world | 7ssa-thai-7 | 7ssa-thai-5 | 7ssa-thai-4, and the candidates
```

Ask: "จะให้จัดเนื้อหาแบบเจ็ดหัวข้อภาษาอังกฤษ หรือหัวข้อภาษาไทยแบบเจ็ด ห้า หรือสี่หัวข้อ" / "Seven
English sections, or seven, five or four Thai sections?" Record the answer as
`project.structure_profile` in `answers.yaml` (with `project.route:
academic-article`), or pass `--structure-profile ID` to `report`. A profile
is optional: with none, the article overview is the plain one. With a
profile, interview sector by sector with `reference/interview-7ssa.md`
(tag each body item with `ssa_sector` and `ssa_slot`). The 7SSA findings
(7SSA-01..10) are presence checks only; explain them with
`reference/rules-th.md`. `--format tex` gives an English LaTeX draft
(`build/ACADEMIC_ARTICLE.tex`) of the same sectors.

### 1. Set up (once)

Check the engine is available:

```bash
python scripts/grantthai_skill.py check      # or: grantthai --version
```

If it is missing: `pip install -e <GrantThai checkout>` (Python 3.10+), or
set `GRANTTHAI_HOME` to a GrantThai checkout. No network access is needed
after install. If you cannot run programs at all, use
`reference/PROMPT_PACKET.md` instead of this workflow.

Start a work file in the researcher's folder (one canonical input per
folder: `work.yaml`, or a legacy `project.yaml`, never both):

```bash
grantthai init work.yaml --work-id MY-WORK-001 --work-type research_proposal   # or academic_article, concept_note ...
```

`--work-type` sets defaults only (the default route, the interview
track); it never refuses a route. `init` writes no route. An existing
`project.yaml` (0.2) keeps working unchanged and always reads as
`nriis-proposal`; `grantthai migrate --rename` upgrades it to `work.yaml`
only when the researcher asks (it changes the content hash and makes
current review gates stale; `--dry-run` shows which).

Only one fund profile ships: `example/FICTIONAL_CALL@0.1`, a
fictional test profile. The `nriis-proposal` route needs it as the
binding; tell the researcher that fund-specific checks (ceiling,
eligibility) are not real-fund checks yet. The article and concept-note
routes need no fund binding.

Since v0.2 a project may also name a **form profile** (`form_profile:` at
the top of a legacy `project.yaml`, or `routing.sub_profiles.nriis-proposal`
in `work.yaml`; `grantthai profiles` lists them). A form profile says which
proposal form type the researcher is filling (for example
`ff_full_proposal@nriis-2570`); every profile is `NEEDS_VERIFICATION`, and
its budget rules are listed, never evaluated. Pick one only when the
researcher names the form; otherwise leave it out. The article route has
its own sub-profiles, `thai-journal` and `international-journal`, both
`NEEDS_VERIFICATION` and neither a journal profile.

`grantthai explain FIELD_ID` shows what a box is for and a length target
(`reference/writing.md`). Use it to ask better questions, never to write
the researcher's content for them.

Review, lock and `link` (v0.2) are for a named human at the terminal.
You never run `review` or `lock` on the researcher's behalf.

### 2. Interview

First show the data warning (non-negotiable 7) and ask which AI product
and version the researcher is using with you; record them as `tool:` and
`tool_version:` in `answers.yaml`.

Follow the track of the chosen route. `reference/interview.md` (routes
`nriis-proposal` and `concept-note`; the concept note stops after ethics
and has no budget): questions in Thai and English, each mapped to a
`field_id`, in chain order (call, general, team, need, problem, prior
knowledge, gap, research question, objectives, method, ethics, workplan,
budget, outputs, evidence, claim, narrative). `reference/interview-article.md`
(route `academic-article`): kind, venue with its source, authors and
roles, IMRaD sections from the researcher's own results, ethics, AI-use
placement, data-bearing figures. Ask two or three questions per turn. For each factual claim ask where it comes from
and record that as a source. If the researcher already has a draft
proposal, extract from it (it is theirs: `by: researcher`) and ask only
for what is missing.

Also ask for the parts that funded work usually has
(`reference/interview.md` section 3a; evidence in
`docs/practice/funded-work-patterns.md`, 100 funded final reports):

- objectives numbered 1) 2) 3), one aim each, and the method step that
  answers each one (77/100 number their objectives; rule FW002);
- the reference list behind the theory and prior knowledge (78/100 have
  one; rule FW001), and the literature topics in objective order (64/100);
- population, sample-size basis, instruments and their quality check,
  and the analysis for each objective (66/100 have method sub-parts);
- ethics inside the method: consent, withdrawal, data keeping, committee;
- who should act on any recommendation (agency or level), and known
  limitations of the data and design.

These are practice, not fund rules: FW001 and FW002 are REVIEW only. Quote
the count if it helps; never say a fund requires it.

### 3. Write project.yaml

Collect answers in an `answers.yaml` (format: `reference/answers-format.md`)
and apply them:

```bash
python scripts/grantthai_skill.py apply answers.yaml --project work.yaml [--route ID]
```

`--route` (or `project.route` in the file) records the route the
researcher chose in step 0 as `routing.default_route`; it is refused on a
legacy `project.yaml`, which has no routing block (build that with
`--route` instead). `routing` is outside the content hash.

Or set single fields with the CLI:

```bash
grantthai set CORE.GENERAL.TITLE_TH "ชื่อโครงการ" --project project.yaml --string
grantthai set CORE.GENERAL.TITLE_EN "Project title" --project project.yaml --string --ai --tool "TOOL NAME" --tool-version "VERSION"
grantthai set CORE.RESEARCH.PROBLEM "..." --project project.yaml --string --provenance-class SOURCE --source-id SRC-1
```

Or the Python API:

```python
from grantthai import api_py as gt
gt.set_field("project.yaml", "CORE.GENERAL.TITLE_EN", "Project title", actor="ai_assisted", tool="TOOL NAME",
             tool_version="VERSION")
```

Links, sources and evidence fields are easiest through `answers.yaml`; the
CLI `set` has no option for `links` or the `sources` list.

Show the researcher every value you drafted (`by: ai`) and ask them to
confirm or rewrite it. Only after they explicitly adopt the wording may
you re-apply it as `by: researcher_edited_ai_draft`.

**AI Use Declaration.** Every AI-assisted write records your tool in
`authoring.ai_use_declaration.tools`. Ask the researcher, in their own
words, for the rest (answers file block `ai_use_declaration`, see
`reference/answers-format.md`): each tool's purpose and stages, how the AI
output influenced their decisions, what they checked and who signs for it,
what types of data they gave the AI, and where they keep the prompt log;
optionally their own risk scores (1-3) on the guideline's five example
dimensions. Tell them the single level GrantThai prints is GrantThai's
convention, not the guideline's. Then ask them to read output section 4.7
and, if it is true, set `declaration_confirmed_by_human: true` in
`project.yaml` themselves. You never set it; the answers file refuses it.

### 4. Check and explain

```bash
python scripts/grantthai_skill.py report --project work.yaml --route ID
```

This runs the route-scoped validation, prints every BLOCK and REVIEW
finding with a plain-Thai explanation from `reference/rules-th.md`, lists
fields still drafted by AI, and builds that route's output. With no
`--route` it uses only what the researcher declared; when that does not
decide it prints the candidates, builds nothing and exits 2: ask, then
rerun. Plain commands work too: `grantthai route check --route ID work.yaml`,
`grantthai validate work.yaml --route ID` (exit 1 if any BLOCK),
`grantthai explain B002`.

When you explain findings to the researcher:

- Say what is missing or inconsistent, and which question will fix it.
- BLOCK does not stop the build; it marks the proposal as not ready.
- Never "fix" a finding by changing the researcher's facts or inventing
  data. Ask them. For arithmetic (B002, W003, T001), show the numbers and
  let them decide.
- INFO lines about rules "not evaluated" mean GrantThai does not check
  that yet; the researcher must check it against the call document.
  RT002 counts the rules outside the chosen route's scope (no silent
  skip); RT001 says the route was not designed for this work type. Both
  are information, not findings to fix.
- ART001-ART011 (article route) test the manuscript's structure only;
  none rests on a journal fact. ART007 (an AI tool listed as an author) is
  the one BLOCK. `manuscript_ready` means "no BLOCK open", never accepted
  or publishable.
- AI001-AI004 (REVIEW) come from the AI-use ceiling: a missing or
  unconfirmed AI Use Declaration, an AI-drafted data or evidence record,
  personal-data-shaped strings in an AI-assisted value, a self-assessed
  risk of 3. Never clear them by changing who wrote a value.

### 5. Hand back exactly one file per chosen route

```bash
grantthai build work.yaml --route nriis-proposal      # writes build/NRIIS_SUBMISSION.md
grantthai build work.yaml --route academic-article    # writes build/ACADEMIC_ARTICLE.md
grantthai build work.yaml --route concept-note        # writes build/RESEARCH_CONCEPT_NOTE.md
```

Give the researcher the path to the one file of each route they picked
and `work.yaml` (their input, to keep and edit later). Each build writes
its own file and leaves the other routes' files byte-identical. Summarise
in Thai: number of BLOCK/REVIEW findings, fields still `NEEDS_INPUT` or
`NEEDS_VERIFICATION` (on the article route: every venue fact), AI-drafted
fields awaiting confirmation, and whether the AI Use Declaration (section
4.7, a GrantThai appendix, not an NRIIS field) is complete and confirmed.
Remind them that they, not GrantThai or you, submit to NRIIS or to the
journal.

The file is deterministic: the same work file, route and `--as-of` date
always give the same bytes. Fund-rule freshness (F002) depends on the
date.

## Reference files

| File | Use |
|---|---|
| `reference/routes.md` | the output routes, how a route is resolved, and step 0 (ask, never choose) |
| `reference/interview.md` | question list (TH/EN) mapped to field ids, item keys and id prefixes; section 3a: what funded work usually has (routes `nriis-proposal`, `concept-note`) |
| `reference/interview-7ssa.md` | the 7SSA track (a structure profile is selected): sector by sector in the writing order 5 -> 4 -> 3 -> 6 -> 2 -> 1 -> 7, each question mapped to a sector and slot; the source's quality conditions are questions to the researcher, never verdicts |
| `reference/interview-article.md` | the article track: kind, venue with source, authors and roles, IMRaD from the researcher's results, ethics, AI-use placement, data-bearing figures (route `academic-article`) |
| `reference/provenance.md` | how to record researcher statements, AI drafts, sources, unknowns |
| `reference/answers-format.md` | the `answers.yaml` format for `scripts/grantthai_skill.py apply` |
| `reference/rules-th.md` | every v0.1 rule, plus the FW, AI, RT and ART rules, explained in plain Thai, with how to fix it |
| `reference/writing.md` | what each box is for, micro-templates, length targets (W101/W102, REVIEW only), completeness checklist, practice from funded work (`practice:`) |
| `reference/PROMPT_PACKET.md` | paste-in prompt for chat-only AIs without tools (proposal variant, plus an article variant at the end) |
| `scripts/grantthai_skill.py` | `check`, `warning`, `apply [--route]`, `report [--route]`: thin wrapper over `grantthai.api_py` |

In the GrantThai repository: `examples/lecturer-no-ai/project.yaml` is a
complete FICTIONAL worked example (legacy 0.2, route `nriis-proposal`);
`grantthai fields [--route ID]` lists every field (NRIIS boxes in entry
order, then `NOT_ON_TAB` authoring fields; for another route its placement
order, then `NOT_PLACED`); `docs/use-with-ai.md` covers installation per AI
tool.
