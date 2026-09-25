# tests/golden/routes/

Acceptance AT-R1 of the v0.3 router: NRIIS is now one output route, and
adding the router must not change a single byte of the NRIIS output.

`<example>/NRIIS_SUBMISSION.md` was rendered from branch `corpus-100`
(commit 0d79ef1, before any router code existed) with

    grantthai build examples/<example>/project.yaml --out tests/golden/routes/<example> --as-of 2026-09-25

for `lecturer-no-ai` and `demo-seedbank`. `tests/test_routes_at_r1.py`
builds the same inputs through `build`, `build --route nriis-proposal`,
`route build --route nriis-proposal` and `api_py.build(route=...)`, and
requires each result to equal these files byte for byte. Refresh them only
through a reviewed decision that the NRIIS output is meant to change.

Provenance: re-pinned 2026-09-25 for the 0.3.0 version string; content
unchanged, diff checked (the only changed line in each file is
`grantthai_version: 0.2.0` -> `grantthai_version: 0.3.0`).

AT-R1 compares against these files only. `examples/*/build/` is
git-ignored and may hold a stale local build from an older version (for
example `grantthai_version 0.1.0`); rebuild or delete it before comparing
anything by hand, or it will look like a regression that is not there.
