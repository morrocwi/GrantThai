# tests/

Phase 0: guard tests (`test_no_ai_import.py`, `test_no_hardcoded_rules.py`,
`test_leak_pii.py`, `test_schema_lint.py`, `test_registry.py`) plus fixtures
(`fixtures/positive/` must validate; `fixtures/negative/` must fail their
guard; PII- and secret-shaped fixtures are generated at run time by
`tools/ci/make_negative_fixtures.py`). `golden/` and
`acceptance/` ship real content in v0.1+ once the renderer and CLI exist.
Run everything with `bash tools/ci/run_all_guards.sh` (guard scripts) and
`pytest` (this directory) once `pip install -e .[dev]` has been run.
