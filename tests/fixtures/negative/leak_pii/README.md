# tests/fixtures/negative/leak_pii/

No PII-shaped value is committed here. The seeded bad fixture for the
leak/PII guard is generated at test run time by
`tools/ci/make_negative_fixtures.py pii <dir>` (synthetic values only: a
reserved `.test` e-mail domain, an unissuable phone number, and a
checksum-valid 13-digit number starting with 0, which no real Thai ID
does). See `tools/ci/run_all_guards.sh` and `tests/test_leak_pii.py`.
