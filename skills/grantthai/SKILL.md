---
name: grantthai
description: Help a Thai researcher turn their own project information into GrantThai's one input file (project.yaml) and its one overview output (build/NRIIS_SUBMISSION.md) for entering a research proposal into NRIIS by hand. Use when a researcher asks to prepare, organise, check or summarise a Thai research grant proposal, an NRIIS submission, a proposal to a Thai national research fund, or mentions GrantThai, project.yaml or NRIIS_SUBMISSION.md, or says things like "เตรียมข้อเสนอโครงการ", "กรอก NRIIS", "ขอทุนวิจัย", "สรุปภาพรวมโครงการ". The skill interviews the researcher, records who said what (researcher statement vs AI draft), runs the GrantThai checks, explains findings in plain Thai, and hands back exactly one file. It never validates knowledge, never invents Thai fund or NRIIS facts, and never submits anything.
---

# GrantThai: from the researcher's own information to one overview file

GrantThai is an open, unofficial tool; see `NOTICE` in the GrantThai
repository (it is not affiliated with any funding agency or with NRIIS).
It has one input, `project.yaml`, one command, `grantthai build`, and one
output, `build/NRIIS_SUBMISSION.md`: an overview the researcher reads and
copies into NRIIS by hand. GrantThai never submits anything.

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
3. **No invented Thai facts.** Fund rules, agency details, deadlines,
   rates, eligibility, code lists, NRIIS labels, tab names and tab order
   come only from the researcher's current call document. Otherwise write
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

### 1. Set up (once)

Check the engine is available:

```bash
python scripts/grantthai_skill.py check      # or: grantthai --version
```

If it is missing: `pip install -e <GrantThai checkout>` (Python 3.10+), or
set `GRANTTHAI_HOME` to a GrantThai checkout. No network access is needed
after install. If you cannot run programs at all, use
`reference/PROMPT_PACKET.md` instead of this workflow.

Start a project in the researcher's folder:

```bash
grantthai init project.yaml --project-id MY-PROJECT-001
```

Only one fund profile ships: `example/FICTIONAL_CALL@0.1`, a
fictional test profile. Keep it as the binding and tell the researcher
that fund-specific checks (ceiling, eligibility) are not real-fund checks
yet.

Since v0.2 a project may also name a **form profile** (`form_profile:` at
the top of `project.yaml`; `grantthai profiles` lists them). A form profile
says which proposal form type the researcher is filling (for example
`ff_full_proposal@nriis-2570`); every profile is `NEEDS_VERIFICATION`, and
its budget rules are listed, never evaluated. Pick one only when the
researcher names the form; otherwise leave it out.

`grantthai explain FIELD_ID` shows what a box is for and a length target
(`reference/writing.md`). Use it to ask better questions, never to write
the researcher's content for them.

Review, lock and `link` (v0.2) are for a named human at the terminal.
You never run `review` or `lock` on the researcher's behalf.

### 2. Interview

First show the data warning (non-negotiable 7) and ask which AI product
and version the researcher is using with you; record them as `tool:` and
`tool_version:` in `answers.yaml`.

Follow `reference/interview.md`: questions in Thai and English, each
mapped to a `field_id`, in chain order (call, general, team, need,
problem, prior knowledge, gap, research question, objectives, method,
ethics, workplan, budget, outputs, evidence, claim, narrative). Ask two or
three questions per turn. For each factual claim ask where it comes from
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
python scripts/grantthai_skill.py apply answers.yaml --project project.yaml
```

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
python scripts/grantthai_skill.py report --project project.yaml
```

This runs `grantthai validate`, prints every BLOCK and REVIEW finding with
a plain-Thai explanation from `reference/rules-th.md`, lists fields still
drafted by AI, and builds the output. Plain commands work too:
`grantthai validate project.yaml` (exit 1 if any BLOCK),
`grantthai explain B002`.

When you explain findings to the researcher:

- Say what is missing or inconsistent, and which question will fix it.
- BLOCK does not stop the build; it marks the proposal as not ready.
- Never "fix" a finding by changing the researcher's facts or inventing
  data. Ask them. For arithmetic (B002, W003, T001), show the numbers and
  let them decide.
- INFO lines about rules "not evaluated" mean GrantThai v0.1 does not
  check that yet; the researcher must check it against the call document.
- AI001-AI004 (REVIEW) come from the AI-use ceiling: a missing or
  unconfirmed AI Use Declaration, an AI-drafted data or evidence record,
  personal-data-shaped strings in an AI-assisted value, a self-assessed
  risk of 3. Never clear them by changing who wrote a value.

### 5. Hand back the one file

```bash
grantthai build project.yaml     # writes build/NRIIS_SUBMISSION.md
```

Give the researcher the path to `build/NRIIS_SUBMISSION.md` (the only
output) and `project.yaml` (their input, to keep and edit later). Summarise
in Thai: number of BLOCK/REVIEW findings, fields still `NEEDS_INPUT` or
`NEEDS_VERIFICATION`, AI-drafted fields awaiting confirmation, and whether
the AI Use Declaration (section 4.7, a GrantThai appendix, not an NRIIS
field) is complete and confirmed. Remind
them that they, not GrantThai or you, submit to NRIIS.

The file is deterministic: the same `project.yaml` and the same
`--as-of` date always give the same bytes. Fund-rule freshness (F002)
depends on the date.

## Reference files

| File | Use |
|---|---|
| `reference/interview.md` | question list (TH/EN) mapped to field ids, item keys and id prefixes; section 3a: what funded work usually has |
| `reference/provenance.md` | how to record researcher statements, AI drafts, sources, unknowns |
| `reference/answers-format.md` | the `answers.yaml` format for `scripts/grantthai_skill.py apply` |
| `reference/rules-th.md` | every v0.1 rule, plus the FW and AI rules, explained in plain Thai, with how to fix it |
| `reference/writing.md` | what each box is for, micro-templates, length targets (W101/W102, REVIEW only), completeness checklist, practice from funded work (`practice:`) |
| `reference/PROMPT_PACKET.md` | paste-in prompt for chat-only AIs without tools |
| `scripts/grantthai_skill.py` | `check`, `warning`, `apply`, `report`: thin wrapper over `grantthai.api_py` |

In the GrantThai repository: `examples/lecturer-no-ai/project.yaml` is a
complete FICTIONAL worked example; `grantthai fields` lists every field
(NRIIS boxes in entry order, then `NOT_ON_TAB` authoring fields); `docs/use-with-ai.md` covers installation per AI tool.
