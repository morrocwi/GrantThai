"""tests/test_no_hardcoded_rules.py — pytest wrapper around
tools/ci/check_no_hardcoded_rules.py."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_no_hardcoded_rules_on_repo():
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools/ci/check_no_hardcoded_rules.py"), "--root", str(ROOT)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_no_hardcoded_rules_fails_on_seeded_bad_fixture():
    bad_root = ROOT / "tests/fixtures/negative/no_hardcoded_rules"
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools/ci/check_no_hardcoded_rules.py"), "--root", str(bad_root)],
        capture_output=True, text=True,
    )
    assert result.returncode != 0
