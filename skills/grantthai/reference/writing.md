# Writing guide: what each box is for, and how long it should be

This file explains the writing layer (`guidance/writing_intent.yaml`,
schema `spec/guidance/writing_intent.schema.json`) for an AI helping a
researcher use GrantThai. The file itself is the source; if this page and
the file differ, the file wins. Read it through the engine:

```
grantthai explain CORE.RESEARCH.OBJECTIVES     # registry record + writing intent
```

(A rule id such as `S001` still explains the rule. Until the integrator
wires `explain` for field ids, the subcommand is `explain-field`.)

## What the writing layer is, and is not

It **is**: for every research-core, methodology and results-chain field,

- `purpose` — what the box is for, in one sentence;
- `micro_template` — the shape of a good entry, with `<slots>` the
  researcher fills from their own knowledge;
- `length_target` — a range in words, items or characters, with its
  `basis` (where the target comes from);
- `keep_out` — what does not belong in the box;
- `quality_traits` — what a reader looks for, each with `seen_in`: a real,
  publicly available funded report cited by id and PDF page only, or
  `NEEDS_INPUT` when no reader has recorded a page yet;

plus a **completeness checklist** (`WC01`–`WC14`) evaluated by
`grantthai.guidance.writing.checklist`.

It is **not** a validator of knowledge. Nothing in it moves a status. A
length finding (`W101` above target, `W102` below target) is REVIEW-level
only: the researcher may keep a longer or shorter text and say why.

## How to use it in the interview

1. Before asking about a field, read its `purpose` and `micro_template`
   and turn the slots into questions in the researcher's language. The
   template is a shape, never content: every `<slot>` is filled from what
   the researcher says (`by: researcher`) or leaves `NEEDS_INPUT`.
2. Show `keep_out` when a draft drifts: prestige metrics without relevance,
   a novelty claim with no prior-knowledge record, a user group that is
   not in the users table.
3. After `grantthai validate`, read any `W101`/`W102` finding aloud as
   guidance, not as an error: "the target is about N words; yours is M;
   keep it if it says what it must".
4. Before `grantthai build`, walk the checklist. `PASS` and `OPEN` are
   computed; `HUMAN_CHECK` items are for the researcher to confirm by
   reading, and you record their answer, never your own.

## Honesty markers you must keep

- Every Thai `th` string in the file is `NEEDS_INPUT`. Do not fill Thai
  wording into it from memory; a Thai text needs a cited source.
- The handoff-package sections behind the targets (core/02 §4A.2, §4B,
  §4E, §15; core/01 §30) and the public document behind the validation
  page (SD-4 p166) are relayed, not read, for this file, so every basis
  that cites them carries `NEEDS_VERIFICATION`, and a target GrantThai set
  itself says `proposed_default`.
- The 3,000-word cap on the summary and rationale is the registry's
  "observed instruction" and is `NEEDS_VERIFICATION`.
- Word counts are whitespace tokens. Thai prose without spaces counts low,
  so `W102` is never raised on Thai text and a `W101` message says it is a
  token count.

## Rule ids

| Rule | Severity | Meaning |
|---|---|---|
| W101 | REVIEW | a non-empty value is above its `length_target.max` |
| W102 | REVIEW | a non-empty value is below its `length_target.min` (not raised for Thai prose) |

An empty value is not a length finding; that is `S001` (`NEEDS_INPUT`).
