# validators/

- `rules.yaml` — the rule catalog as data (schema
  `spec/validators/rule.schema.json`): 60 rules with id, family, ship
  version, severity (`BLOCK` / `REVIEW` / `INFO`), description, inputs
  (field ids or chain nodes), chain step, source and the path of the
  negative fixture each BLOCK rule needs (AT-4). Implementations live in
  `src/grantthai/validators` (v0.1 for families S, R, W, B, T, CH001–CH002,
  F, ELIG; v0.2 for the rest). Structure checks are JSON Schema's job.
- `crosswalk.yaml` — aliases for rule ids from core/02, core/04 and core/05
  onto the canonical ids (v0.2).

See the repository root README.md and GRANTTHAI_STANDALONE.md for the full
system description, and docs/design/PLAN.md for the design plan this
scaffold follows (where they differ, spec/ wins).
