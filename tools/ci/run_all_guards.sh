#!/usr/bin/env bash
# tools/ci/run_all_guards.sh
#
# Runs every Phase 0 CI guard twice:
#   1. against the real repository tree — every guard must PASS.
#   2. against its own seeded bad fixture under tests/fixtures/negative/ —
#      every guard must FAIL.
#
# This is the acceptance check for Phase 0 (plan section I: "CI is green,
# and every guard fails on its seeded bad fixture").
#
# The leak/PII and gitleaks bad fixtures are GENERATED at run time into a
# temporary directory (tools/ci/make_negative_fixtures.py), so no
# PII-shaped or secret-shaped value is ever committed.
set -uo pipefail

cd "$(dirname "$0")/../.."
ROOT="$(pwd)"
PY="${PYTHON:-python3}"
FAIL=0
GEN_DIR="$(mktemp -d)"
trap 'rm -rf "$GEN_DIR"' EXIT
"$PY" tools/ci/make_negative_fixtures.py pii "$GEN_DIR/leak_pii" >/dev/null
"$PY" tools/ci/make_negative_fixtures.py gitleaks "$GEN_DIR/gitleaks" >/dev/null

run_guard () {
  local name="$1" script="$2" good_root="$3" bad_root="$4"
  echo "== $name : good tree ($good_root) — expect PASS =="
  if "$PY" "$script" --root "$good_root"; then
    echo "OK: $name passed on the good tree"
  else
    echo "UNEXPECTED FAIL: $name failed on the good tree" >&2
    FAIL=1
  fi
  echo
  if [ -n "$bad_root" ]; then
    echo "== $name : seeded bad fixture ($bad_root) — expect FAIL =="
    if "$PY" "$script" --root "$bad_root"; then
      echo "UNEXPECTED PASS: $name did not fail on its seeded bad fixture" >&2
      FAIL=1
    else
      echo "OK: $name correctly failed on the seeded bad fixture"
    fi
  fi
  echo "-----------------------------------------------------------"
}

run_guard "no-AI-import" tools/ci/check_no_ai_import.py "$ROOT" "$ROOT/tests/fixtures/negative/no_ai_import"
run_guard "no-hardcoded-rules" tools/ci/check_no_hardcoded_rules.py "$ROOT" "$ROOT/tests/fixtures/negative/no_hardcoded_rules"
run_guard "leak/PII" tools/ci/check_leak_pii.py "$ROOT" "$GEN_DIR/leak_pii"
run_guard "attribution" tools/ci/check_attribution.py "$ROOT" "$ROOT/tests/fixtures/negative/attribution"
run_guard "gitleaks" tools/ci/check_gitleaks.py "$ROOT" "$GEN_DIR/gitleaks"
run_guard "reuse" tools/ci/check_reuse.py "$ROOT" "$ROOT/tests/fixtures/negative/reuse"
run_guard "schema-lint (parse)" tools/ci/check_schema_lint.py "$ROOT" "$ROOT/tests/fixtures/negative/schema_lint"
run_guard "schema-lint (instances)" tools/ci/check_schema_lint.py "$ROOT" "$ROOT/tests/fixtures/negative/schema_instance"
run_guard "one-input-one-output" tools/ci/check_one_output.py "$ROOT" "$ROOT/tests/fixtures/negative/one_output"
run_guard "notice" tools/ci/check_notice.py "$ROOT" "$ROOT/tests/fixtures/negative/notice"

echo
if [ "$FAIL" -eq 0 ]; then
  echo "ALL GUARDS BEHAVED AS EXPECTED (pass on good tree, fail on seeded bad fixture)."
else
  echo "ONE OR MORE GUARDS DID NOT BEHAVE AS EXPECTED. See output above." >&2
fi
exit "$FAIL"
