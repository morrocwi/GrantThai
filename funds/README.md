# funds/

Dated, sourced fund-call profiles, schema `spec/fund/fund-profile.schema.json`.

- A profile lives at `funds/<agency>/<call-id>@<major.minor>/fund-profile.yaml`
  and its `id` is exactly `<agency>/<call-id>@<major.minor>`. A project
  binds it with `fund_binding.fund_profile_id` set to that id, so the id
  resolves to one path: `funds/<id>/fund-profile.yaml`.
- `funds/_template/` — a blank **DRAFT** profile. It validates against the
  schema as a DRAFT (NEEDS_INPUT is allowed in dates and the source sha256
  only while `status: DRAFT`).
- `funds/example/FICTIONAL_CALL@0.1/` — an ACTIVE, `trust_level: FICTIONAL`
  profile (`id: example/FICTIONAL_CALL@0.1`) used for testing. Not a real
  fund; no value in it is a real rule.

`tools/ci/check_schema_lint.py` validates every `fund-profile.yaml` against
the schema and checks that each `id` matches its path.

Ships: v0.1 (fictional), v0.5 (first real profile). See the repository
root README.md and GRANTTHAI_STANDALONE.md for the full system
description, and docs/design/PLAN.md for the design plan this scaffold
follows (where they differ, spec/ wins).
