# The answers file (`answers.yaml`)

`scripts/grantthai_skill.py apply answers.yaml --project project.yaml`
writes an interview's answers into `project.yaml` through the GrantThai
Python API (`grantthai.api_py.set_field`). It is the easiest way for an AI
with a shell to write many fields, sources and links at once. Every rule
in `provenance.md` is enforced by the engine, not by this file.

You can apply the same answers file again after editing it: each field is
one record, so a second apply replaces the earlier value rather than
adding a copy. Sources are matched by `source_id` the same way.

```yaml
# Used only with --init, when project.yaml does not exist yet.
project:
  project_id: "MY-PROJECT-001"
  fund_profile_id: "example/FICTIONAL_CALL@0.1"   # the only profile shipped in v0.1
  mode: expert

# The AI product name, as the researcher wants it disclosed.
# Needed only when some answer has by: ai.
tool: "NAME OF THE AI TOOL"

# The researcher's own sources. Never add one the researcher did not give you.
sources:
  - source_id: SRC-1                     # ^SRC-[A-Z0-9][A-Z0-9-]*$
    kind: OFFICIAL_DOCUMENT               # see provenance.md for the list
    citation: "Exactly as the researcher gave it."
    locator: "Table 3"                    # optional
    contains_personal_data: false         # true for interview notes etc.

answers:
  # A plain field the researcher decided.
  - field_id: CORE.GENERAL.TITLE_TH
    value: "ชื่อโครงการตามที่ผู้วิจัยตั้ง"
    by: researcher

  # A factual statement backed by the researcher's source.
  - field_id: CORE.RESEARCH.PROBLEM
    value: "..."
    by: researcher
    provenance_class: SOURCE
    source_ids: [SRC-1]
    links: {need_ids: [CORE.RESEARCH.NATIONAL_NEED]}

  # An English title the AI translated: an AI draft for the researcher to confirm.
  - field_id: CORE.GENERAL.TITLE_EN
    value: "..."
    by: ai

  # A value that depends on an unverified Thai fund rule.
  - field_id: CORE.GENERAL.RESEARCH_ISSUE
    value: NEEDS_VERIFICATION
    by: researcher

  # Chain content with no registry field needs chain_node.
  - field_id: CORE.PRIORKNOWLEDGE.PK1
    chain_node: PriorKnowledge
    value: "..."
    by: researcher
    provenance_class: SOURCE
    source_ids: [SRC-2]
    links: {problem_ids: [CORE.RESEARCH.PROBLEM]}

  # Evidence records also carry supports_claim_id and claim_strength_cap.
  - field_id: CORE.EVIDENCE.E1
    chain_node: Evidence
    value: "..."
    by: researcher
    provenance_class: SOURCE
    evidence_role: SUPPORTING
    source_ids: [SRC-3]
    supports_claim_id: CORE.CLAIM.C1
    claim_strength_cap: FULL             # NONE | CONTRIBUTORY | FULL
```

Keys per answer: `field_id`, `value` (required); `by`
(`researcher` | `researcher_edited_ai_draft` | `ai`, default `researcher`);
`provenance_class`, `source_type`, `evidence_role`, `source_ids`, `links`,
`chain_node`, `supports_claim_id`, `claim_strength_cap`, `note` (a comment
for you; not written to `project.yaml`). Any other key is refused.

Values are YAML: numbers stay numbers (`50000`), lists are lists, and
structured fields are lists of objects with `id` keys (see
`interview.md` for each field's keys and id prefix). `NEEDS_INPUT` clears
a field; `NEEDS_VERIFICATION` stores an empty value plus that marker.

## Link keys on a record (`links`)

| On record | Key | Points to |
|---|---|---|
| `CORE.RESEARCH.PROBLEM` | `need_ids` | `CORE.RESEARCH.NATIONAL_NEED` |
| `CORE.PRIORKNOWLEDGE.*` | `problem_ids` | `CORE.RESEARCH.PROBLEM` |
| `CORE.RESEARCH.GAP` | `prior_knowledge_ids` | `CORE.PRIORKNOWLEDGE.*` records |
| `CORE.RESEARCH.RQ.PRIMARY` | `gap_ids` | `CORE.RESEARCH.GAP` |
| `CORE.CLAIM.*` | `output_ids` | output items (`OUT1` ...) |

Links between items (objective to method phase, activity to budget line,
and so on) are written inside the items themselves; see `interview.md`.
The full contract is `spec/common/links-and-sources.md`.
