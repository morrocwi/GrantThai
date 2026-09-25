> **FICTIONAL. สมมติทั้งหมด.** Everything in this folder was produced by an AI assistant that simulated both the interviewer and the researcher. No real researcher, village or finding is described. It is a test of GrantThai, not a proposal and not evidence.

# examples/demo-seedbank/

GrantThai is an independent, unofficial project; see `NOTICE`.

> **FICTIONAL.** A demo of the tool, made entirely by an AI assistant; see the banner above.

Demo topic 1 for v0.2: a community seed-bank learning network for
smallholder rice growers in a fictional southern district, as
participatory action research with community co-researchers.

| File | What it is |
|---|---|
| `../../docs/demo/transcript-seedbank.md` | the simulated interview (turns T01–T21), marking the persona's answers and the AI drafts |
| `answers.yaml` | the answers file an AI with a shell writes from that interview (`skills/grantthai/reference/answers-format.md`) |
| `project.yaml` | the one input, produced by `grantthai_skill.py apply` |
| `NRIIS_SUBMISSION.md` | a committed copy of the one output, `build/NRIIS_SUBMISSION.md` (the `build/` folder itself is git-ignored) |
| `../../docs/demo/comparison.md` | the comparison with real, funded, public reports and the public FF form, and the gaps found; its section 4 waits for two blind scorers |
| `../../docs/demo/scored-reading-draft.md` (Thai: `.th.md`) | one non-blind AI reading with scores (`DRAFT`), not the blind scores |

## Reproduce

From the repository root (Python 3.10+, `pip install -e .`):

```bash
rm examples/demo-seedbank/project.yaml
python skills/grantthai/scripts/grantthai_skill.py apply --init \
    --project examples/demo-seedbank/project.yaml examples/demo-seedbank/answers.yaml
grantthai validate examples/demo-seedbank/project.yaml --as-of 2026-09-25
grantthai build examples/demo-seedbank/project.yaml --as-of 2026-09-25
```

`tests/test_demo.py` checks that the committed `NRIIS_SUBMISSION.md` is
byte for byte what `build --as-of 2026-09-25` gives for the committed
`project.yaml`.

## What the result says, and does not say

- `grantthai validate`: BLOCK 0, REVIEW 3 (structure and links only). This
  does not mean the project is sound, novel or fundable. The REVIEW
  findings (unreleased, after v0.2.0) are FW001: the theory box has content
  but the reference list is empty, while 78 of 100 funded final reports
  carry one (`docs/practice/funded-work-patterns.md`); and AI001, twice:
  the AI Use Declaration has no human verification yet and is not confirmed
  (`docs/policy/ai-use-ceiling.md`). The demo is left this way on purpose
  so the findings stay visible.
- The AI Use Declaration (`authoring.ai_use_declaration`, output section
  4.7) is written for the simulated persona, including its risk
  self-assessment. The level printed there is GrantThai's convention, not
  the guideline's. `declaration_confirmed_by_human` stays false: only a
  real researcher can confirm it.
- No value is `SOURCE`; every record is `DRAFT` or `NEEDS_INPUT`; there are
  no review records and no lock, because no named human has reviewed
  anything. `authoring.mode` is `ai_assisted` and the tool is disclosed
  generically.
- **`authored_by: human` here means the simulated persona.** GrantThai has
  no value for a simulated author yet (gap G8 in `docs/demo/comparison.md`).
- Still open, on purpose: the literature review and references
  (`NEEDS_INPUT`), the IP check (`NEEDS_INPUT`), key results and fund
  alignment (`NEEDS_VERIFICATION`), the summary (an AI draft the persona did
  not adopt), the English keywords (an AI translation not adopted).
- The fiscal year, focus area, OECD codes and ethics route are
  `NEEDS_VERIFICATION`: they were read from a public form or a candidate
  list, not confirmed against a current call.
- The project is bound to the fictional test call
  `example/FICTIONAL_CALL@0.1` (GrantThai ships no real fund profile), with
  the form profile `ff_full_proposal@nriis-2570` (`NEEDS_VERIFICATION`). The
  output says so in a FICTIONAL banner right after the notice line, and its
  readiness summary prints "Submittable to a real call: n/a (fictional
  call)". The frontmatter key `submittable: true` is against that fictional
  call only (`fund_profile_trust_level: FICTIONAL`).
- This demo is **not** an AT-1 pass: AT-1 needs a human-authored gap and
  research question.
