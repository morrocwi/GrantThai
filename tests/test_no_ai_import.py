"""tests/test_no_ai_import.py — pytest wrapper around
tools/ci/check_no_ai_import.py, so `pytest` alone exercises this guard."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_no_ai_import_on_repo():
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools/ci/check_no_ai_import.py"), "--root", str(ROOT)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_no_ai_import_fails_on_seeded_bad_fixture():
    bad_root = ROOT / "tests/fixtures/negative/no_ai_import"
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools/ci/check_no_ai_import.py"), "--root", str(bad_root)],
        capture_output=True, text=True,
    )
    assert result.returncode != 0
