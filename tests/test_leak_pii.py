"""tests/test_leak_pii.py — the leak/PII guard passes on the repository and
fails on a fixture generated at run time (no PII-shaped value committed)."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "ci"))

import make_negative_fixtures as gen  # noqa: E402


def run(*args):
    return subprocess.run([sys.executable, *args], capture_output=True, text=True)


def test_leak_pii_passes_on_repo():
    r = run(str(ROOT / "tools/ci/check_leak_pii.py"), "--root", str(ROOT))
    assert r.returncode == 0, r.stdout + r.stderr


def test_leak_pii_fails_on_generated_fixture(tmp_path):
    run(str(ROOT / "tools/ci/make_negative_fixtures.py"), "pii", str(tmp_path))
    r = run(str(ROOT / "tools/ci/check_leak_pii.py"), "--root", str(tmp_path))
    assert r.returncode != 0
    assert "checksum-valid Thai national ID" in r.stdout
    assert "phone-number-shaped" in r.stdout
    assert "email address found" in r.stdout


def test_generated_id_is_synthetic_and_checksum_valid():
    import random
    rng = random.Random(0)
    for _ in range(50):
        tid = gen.synthetic_thai_id(rng)
        assert len(tid) == 13 and tid[0] == "0"
        assert gen.thai_id_check_digit(tid[:12]) == tid[12]
