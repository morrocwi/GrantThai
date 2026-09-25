# validators/

- `rules.yaml` — the rule catalog as data (schema
  `spec/validators/rule.schema.json`): 92 rules with id, family, ship
  version, severity (`BLOCK` / `REVIEW` / `INFO`), description, inputs
  (field ids or chain nodes), chain step, source, the path of the
  negative fixture each BLOCK rule needs (AT-4) and, since the v0.3
  router, `routes:` — the output routes the rule is evaluated for
  (`nriis-proposal`, `academic-article`, `concept-note`) or `[all]`.
  Implementations live in `src/grantthai/validators` (v0.1 for families
  S, R, W, B, T, CH001–CH002, F, ELIG, plus X003 and E009 shipped early;
  v0.2 for the rest, each reported as one INFO finding; v0.3 adds FW, AI
  and the academic-article-only ART family, ART001–ART011: REVIEW except
  ART007, the one BLOCK, an AI tool listed as an author). Structure checks
  are JSON Schema's job. A route is chosen by a person, never by an AI.
- `ai_tool_name_patterns.yaml` — generic AI-tool name patterns (data, no
  product or vendor names) that ART007 matches against an author member's
  full_name, so an AI listed as an author is caught even when no tool was
  disclosed. A bare "AI" token is not a pattern: it is also a given name.
- `crosswalk.yaml` — every validation code of the handoff package (core/02
  §10: 37, core/04 §30: 41, core/05: 12 VAL.* codes) mapped to GrantThai
  rule ids, with coverage `full` / `partial` / `none` and a note wherever
  coverage is not full; plus `route_scope`, the per-family route scope
  (spec/router §4.2), which `tests/test_rules_added.py` checks against the
  `routes:` key of every rule so the two cannot drift.

See the repository root README.md and GRANTTHAI_STANDALONE.md for the full
system description, and docs/design/PLAN.md for the design plan this
scaffold follows (where they differ, spec/ wins).
