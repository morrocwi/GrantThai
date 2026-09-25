# Recording who said what (provenance)

GrantThai's knowledge principle: **the researcher's own information is the
source.** An AI helps collect it, shape it and check its structure. An AI
never validates knowledge, never turns its own prose into a source, and
never supplies Thai fund or NRIIS facts from memory.

Every value you write into `project.yaml` carries a `provenance` block. The
engine sets most of it; you choose `by` and, when needed, the class.

## Step 1: who wrote the words? (`by`)

| Situation | `by` | Stored as | Engine behaviour |
|---|---|---|---|
| The researcher said or wrote it (you may fix typos, split sentences, or move it into the right field without changing meaning) | `researcher` | `authored_by: human` | status `DRAFT` |
| You (the AI) wrote the sentence: a summary, rewording, translation, suggested objective, estimated number | `ai` | `authored_by: ai_draft`, class `INFERENCE` | status `DRAFT`; `SOURCE` is refused; the project is marked AI-assisted; the output lists the field under "AI-drafted values (the researcher must confirm)" |
| You drafted it, then the researcher read it and explicitly rewrote or adopted it as their own | `researcher_edited_ai_draft` | `authored_by: human_ai_assisted` | status `DRAFT`; the AI tool stays disclosed |

Rules:

- When in doubt, use `ai`. Under-claiming is always safe; over-claiming is not.
- Only move a value from `ai` to `researcher_edited_ai_draft` after the
  researcher has said, in this conversation, that the wording is theirs
  (for example "ใช่ ใช้ตามนี้" / "yes, use this"). Silence is not consent.
- Translating the researcher's Thai into English (or back) is AI work:
  record the translation with `by: ai` unless the researcher supplied it.
- No status ever goes above `DRAFT` through this skill. Nothing you do
  makes a value `VERIFIED`, `HUMAN_REVIEWED` or `LOCKED`.

## Step 2: what kind of statement is it? (`provenance_class`)

| Class | Use for | Needs a source? |
|---|---|---|
| `DECISION` (default for `researcher`) | choices the researcher makes: title, objectives, methods, workplan, team, budget numbers | no |
| `SOURCE` | a factual claim the researcher backs with a document, dataset, report, interview notes or their own documented experience | **yes**: at least one `source_ids` entry that resolves to a `sources` item (rule S008) |
| `INFERENCE` (default for `ai`) | a reasoned conclusion, e.g. a gap statement, or anything an AI drafted | no |
| `DERIVED` | computed from other fields, e.g. totals, summaries built from other records | no |

- `SOURCE` is only ever used with `by: researcher` (or
  `researcher_edited_ai_draft`) and only with a source the researcher gave
  you. The engine refuses `SOURCE` for `by: ai`.
- Add the researcher's source to `sources` with the citation the researcher
  gave. Do not look up, complete, or "improve" citations from memory. If a
  detail (year, page) is missing, leave it out or ask.
- `source_type` is filled in for you from the first source's `kind`
  (`PUBLISHED_LITERATURE`, `PRIMARY_DATA`, `OFFICIAL_DOCUMENT`,
  `EXPERT_OPINION`, `PROJECT_DOCUMENT`, `LIVED_EXPERIENCE_ACCOUNT`,
  `PRACTITIONER_KNOWLEDGE`, `EXPERT_REVIEW_RECORD`). An AI proposal is
  never a source kind.
- Set `contains_personal_data: true` on a source that names or identifies
  a person (interview notes, case accounts). The output then prints only
  `[private]` for it.

## Step 3: facts nobody has confirmed (`NEEDS_VERIFICATION`, `NEEDS_INPUT`)

- `NEEDS_INPUT`: the researcher has not given a value yet. Leave it. The
  output prints `NEEDS_INPUT` so the gap is visible. Never fill a required
  field with invented content to make validation pass.
- `NEEDS_VERIFICATION`: a value that depends on a Thai funding rule, an
  agency detail, an NRIIS label, tab name, tab order, deadline, rate,
  eligibility rule or code list, and that the researcher cannot back with
  the current call document. Write the literal string `NEEDS_VERIFICATION`;
  the engine stores it as an empty value plus a marker.
- Fund call details (call name, agency, fiscal year, plan, deadlines) come
  only from the call document the researcher has in hand. Ask for it. If
  they do not have it, use `NEEDS_VERIFICATION`.
- Do not translate NRIIS field labels into Thai. GrantThai prints every
  Thai NRIIS label as `NEEDS_VERIFICATION` on purpose.

## Disclosing the AI tool

When you write any `by: ai` value, set `tool:` in the answers file (or
`--tool` on the CLI) to the name of the AI product the researcher is
using, as the researcher wants it disclosed. This is a disclosure of a
tool that was used, recorded in the researcher's own file. It is not
authorship, and you must not add yourself as an author, co-author or
team member anywhere.
