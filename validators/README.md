# validators/

- `rules.yaml` — the rule catalog as data (schema
  `spec/validators/rule.schema.json`): 72 rules with id, family, ship
  version, severity (`BLOCK` / `REVIEW` / `INFO`), description, inputs
  (field ids or chain nodes), chain step, source and the path of the
  negative fixture each BLOCK rule needs (AT-4). Implementations live in
  `src/grantthai/validators` (v0.1 for families S, R, W, B, T, CH001–CH002,
  F, ELIG, plus X003 and E009 shipped early; v0.2 for the rest, each
  reported as one INFO finding). Structure checks are JSON Schema's job.
- `crosswalk.yaml` — every validation code of the handoff package (core/02
  §10: 37, core/04 §30: 41, core/05: 12 VAL.* codes) mapped to GrantThai
  rule ids, with coverage `full` / `partial` / `none` and a note wherever
  coverage is not full.

See the repository root README.md and GRANTTHAI_STANDALONE.md for the full
system description, and docs/design/PLAN.md for the design plan this
scaffold follows (where they differ, spec/ wins).
