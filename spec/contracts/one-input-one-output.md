# The one-input, one-output contract

**Founder's core goal (verbatim, 2026-09-25):** "อย่าลืมนะ เป้าหมายคือ input
เข้าทางเดียว แล้ว ออกมาเป็นรายงานที่พร้อมเข้าระบบลงทะเบียน NRIIS ได้เลยเป็นไฟล์เดียว"
— one input path in, one file out that is ready to enter into NRIIS.

This is the headline contract for the whole system. Every other design
choice in this repository (webform, questionnaires, optional AI assist,
review gates, fund binding) exists to feed exactly one input and produce
exactly one output. The output side is specified in
`spec/output/nriis-submission.contract.md`.

## ONE INPUT

`project.yaml`, valid against `spec/project/project.schema.json`, is the
**only file `grantthai build` reads** apart from the bound fund profile
(below) and GrantThai's own shipped data (registry, mappings, rules,
templates).

- The offline web form (`webform/index.html`), the Markdown forms
  (`forms/*.md`), the Citizen and Expert questionnaires
  (`interview/*.yaml`), `grantthai init`, `grantthai fill --interactive`,
  `grantthai set`, and any optional AI-assisted feature (v0.3+,
  `src/grantthai/assist`) are all **editors** of this one file.
- Editors are never treated as separate inputs, and their outputs are never
  silently merged from multiple sources at build time. Exactly one
  `project.yaml` goes into `grantthai build`.
- **Identity and team data.** Everything about people that the submission
  uses (names, roles, institutions, ORCID, team contribution percentages)
  lives **in `project.yaml`**, in `PROFILE.*` fields (for example
  `PROFILE.TEAM.MEMBERS`). A local `profile.yaml`
  (`spec/profile/profile.schema.json`) is only an **editor convenience**:
  `grantthai init` and the web form may read it to pre-fill `PROFILE.*`
  fields while the person is editing, and the values are then *copied*
  into `project.yaml`. `grantthai build` — and every other command that
  produces output — **never reads `profile.yaml`**. If the two disagree,
  `project.yaml` is what gets rendered.
- **Fund profile = bound reference, not a second input.** It is named by
  `fund_binding.fund_profile_id` inside `project.yaml`. The id has the
  form `<agency>/<call-id>@<major.minor>` and resolves to exactly one path:
  `funds/<fund_profile_id>/fund-profile.yaml` (for example
  `example/FICTIONAL_CALL@0.1` →
  `funds/example/FICTIONAL_CALL@0.1/fund-profile.yaml`). The profile's own
  `id` field must equal the id it is looked up by.

## ONE COMMAND

```
grantthai build <project.yaml>
```

No other command produces the NRIIS-facing output. The full command list
(all planned; none implemented in Phase 0):

| Command | Reads | Writes | NRIIS-facing output? |
|---|---|---|---|
| `init --role --lang` | — | a local `profile.yaml` and a private workspace | no |
| `fill --interactive`, `set <FIELD_ID>` | `project.yaml` (+ `profile.yaml` only to pre-fill) | `project.yaml` | no |
| `import-form <file or forms/>` | a web-form export or `forms/*.md` | `project.yaml` | no |
| `validate` | `project.yaml`, bound fund profile | a validation report (`spec/common/validation_report.schema.json`); may persist validator statuses | no |
| `explain <RULE_ID>` | `validators/rules.yaml` | — | no |
| `fund check`, `fund stale` | `project.yaml`, bound fund profile | a report | no |
| `build` | `project.yaml`, bound fund profile | `build/NRIIS_SUBMISSION.md` | **yes — the one output** |
| `build --concept-note` (v0.2) | same | also `build/RESEARCH_CONCEPT_NOTE.md` | no (optional extra, see below) |
| `export` | `project.yaml` | a shareable copy of `project.yaml` with `PROFILE.*` personal data removed (`--include-private` keeps it, with a warning) | no |
| `doctor` | environment | a report | no |
| `interview`, `review`, `accept-mapping`, `reject-mapping`, `lock`, `diff` (v0.2) | `project.yaml` | `project.yaml` or a report | no |

## ONE OUTPUT

`build/NRIIS_SUBMISSION.md` — a single, self-contained file containing
(`build/` is the directory next to the `project.yaml` that was built, i.e.
`<directory of project.yaml>/build/NRIIS_SUBMISSION.md`, unless `--out`
names another directory):

- a readiness summary at the top (`BLOCK` / `REVIEW` / `INFO` findings,
  `NEEDS_INPUT`, `NEEDS_VERIFICATION`, holds), and
- every field grouped by NRIIS tab, in the observed-form order (tab names
  and order are `NEEDS_VERIFICATION`, see the output contract),

ready for copy/paste (or, from v0.4, optional browser-assisted entry, still
human-approved). **No second GrantThai-generated file is needed to enter
data into NRIIS.** Supporting documents that NRIIS asks to be uploaded (the
attachments tab) are the person's own files: the output lists which ones
are needed and their status, and never generates them.

### The one exception, and why it does not break the contract

Citizen Mode (v0.2) may additionally render
`build/RESEARCH_CONCEPT_NOTE.md` via `--concept-note`, for a citizen who
has no eligible PI partner and is therefore not yet build-ready for NRIIS
at all. This is:

- a **separate, explicitly optional** artifact, produced by an explicit
  flag, from the same one `project.yaml`;
- **never part of the NRIIS entry path** — a person with a
  `RESEARCH_CONCEPT_NOTE.md` still has no `submittable: true`
  `NRIIS_SUBMISSION.md` and knows it from the file's own frontmatter
  (`submittable: false`, `HOLD_FOR_VERIFICATION`);
- never produced in place of `NRIIS_SUBMISSION.md` — `grantthai build`
  without the flag always renders `NRIIS_SUBMISSION.md` (possibly with
  `submittable: false` and a `HOLD` marker), never nothing.

## CI guard

`tools/ci/check_one_output.py` asserts:

1. `templates/` contains exactly one template tagged
   `output_kind: primary_submission` (`templates/nriis_submission.md.j2`).
2. `spec/output/nriis-submission.contract.md` and this file both exist and
   each names the other's path (cross-reference).
3. Once the renderer ships (v0.1+), running `grantthai build` against a
   fixture project produces exactly one file under `build/` named
   `NRIIS_SUBMISSION.md` (the optional `RESEARCH_CONCEPT_NOTE.md` is
   allowed only when `--concept-note` was explicitly passed).

In Phase 0, check 3 is not implemented (no renderer exists yet); the guard
runs checks 1–2, and a seeded bad fixture (two files tagged
`primary_submission`) makes check 1 fail, proving the guard is live.
