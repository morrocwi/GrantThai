# examples/lecturer-no-ai/

**FICTIONAL.** Every value in this example is synthetic. No real place
name appears together with a real institution name, per PRIVACY.md.

`project.yaml` is a fully populated worked example of the one input: every
registry field with `required: true`, every required chain stage,
structured values per `spec/registry/structured_fields.schema.json`, links
and a `sources` registry per `spec/common/links-and-sources.md`, bound to
the FICTIONAL fund profile (`funds/example/FICTIONAL_CALL@0.1/`).

- `tools/ci/check_schema_lint.py` validates it (schema, structured values,
  reference and source resolution, unique ids, acyclic causal edges).
- `tests/test_example_project.py` recomputes the v0.1 link, sum, budget,
  source and DAG rules on it from the contracts alone; all pass.
- Every status is `DRAFT`: no validator or review has been run on it.

In v0.1 it backs acceptance tests AT-2 and AT-2b (see docs/BUILD_GUIDE.md):
`grantthai validate` and `grantthai build` against it must give
`BLOCK == 0`.
