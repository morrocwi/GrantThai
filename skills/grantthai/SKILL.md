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
   any credit. Disclose the AI tool only in `authoring.tools_disclosed`
   (the `tool:` key), as the researcher chooses to name it.
7. **Privacy.** Use `contains_personal_data: true` for sources that
   identify people. Do not paste the researcher's data into other services.

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

Only one fund profile ships in v0.1: `example/FICTIONAL_CALL@0.1`, a
fictional test profile. Keep it as the binding and tell the researcher
that fund-specific checks (ceiling, eligibility) are not real-fund checks
yet.

### 2. Interview

Follow `reference/interview.md`: questions in Thai and English, each
mapped to a `field_id`, in chain order (call, general, team, need,
problem, prior knowledge, gap, research question, objectives, method,
ethics, workplan, budget, outputs, evidence, claim, narrative). Ask two or
three questions per turn. For each factual claim ask where it comes from
and record that as a source. If the researcher already has a draft
proposal, extract from it (it is theirs: `by: researcher`) and ask only
for what is missing.

### 3. Write project.yaml

Collect answers in an `answers.yaml` (format: `reference/answers-format.md`)
and apply them:

```bash
python scripts/grantthai_skill.py apply answers.yaml --project project.yaml
```

Or set single fields with the CLI:

```bash
grantthai set CORE.GENERAL.TITLE_TH "ชื่อโครงการ" --project project.yaml --string
grantthai set CORE.GENERAL.TITLE_EN "Project title" --project project.yaml --string --ai --tool "TOOL NAME"
grantthai set CORE.RESEARCH.PROBLEM "..." --project project.yaml --string --provenance-class SOURCE --source-id SRC-1
```

Or the Python API:

```python
from grantthai import api_py as gt
gt.set_field("project.yaml", "CORE.GENERAL.TITLE_EN", "Project title", actor="ai_assisted", tool="TOOL NAME")
```

Links, sources and evidence fields are easiest through `answers.yaml`; the
CLI `set` has no option for `links` or the `sources` list.

Show the researcher every value you drafted (`by: ai`) and ask them to
confirm or rewrite it. Only after they explicitly adopt the wording may
you re-apply it as `by: researcher_edited_ai_draft`.

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

### 5. Hand back the one file

```bash
grantthai build project.yaml     # writes build/NRIIS_SUBMISSION.md
```

Give the researcher the path to `build/NRIIS_SUBMISSION.md` (the only
output) and `project.yaml` (their input, to keep and edit later). Summarise
in Thai: number of BLOCK/REVIEW findings, fields still `NEEDS_INPUT` or
`NEEDS_VERIFICATION`, and AI-drafted fields awaiting confirmation. Remind
them that they, not GrantThai or you, submit to NRIIS.

The file is deterministic: the same `project.yaml` and the same
`--as-of` date always give the same bytes. Fund-rule freshness (F002)
depends on the date.

## Reference files

| File | Use |
|---|---|
| `reference/interview.md` | question list (TH/EN) mapped to field ids, item keys and id prefixes |
| `reference/provenance.md` | how to record researcher statements, AI drafts, sources, unknowns |
| `reference/answers-format.md` | the `answers.yaml` format for `scripts/grantthai_skill.py apply` |
| `reference/rules-th.md` | every v0.1 rule explained in plain Thai, with how to fix it |
| `reference/PROMPT_PACKET.md` | paste-in prompt for chat-only AIs without tools |
| `scripts/grantthai_skill.py` | `check`, `apply`, `report`: thin wrapper over `grantthai.api_py` |

In the GrantThai repository: `examples/lecturer-no-ai/project.yaml` is a
complete FICTIONAL worked example; `grantthai fields` lists every field in
NRIIS entry order; `docs/use-with-ai.md` covers installation per AI tool.
