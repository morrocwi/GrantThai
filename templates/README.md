# templates/

**Phase 0 stub.** Jinja2 render templates: nriis_submission.md.j2 (the one primary output template; the `nriis-proposal` route), research_concept_note.md.j2 (v0.2, optional secondary artifact; the `concept-note` route in v0.3), academic_article.md.j2 (v0.3 router: the one output template of the `academic-article` route, tagged `output_kind: route_output` / `route: academic-article`, contract `spec/output/academic-article.contract.md`, rendered by `src/grantthai/render/article.py`), project.blank.yaml (a blank, schema-conformant starting point). Every route template keeps the NOTICE constant as its first body line.

Ships: v0.1. See the repository root README.md and GRANTTHAI_STANDALONE.md
for the full system description, and docs/design/PLAN.md for the
design plan this scaffold follows (where they differ, spec/ wins).
