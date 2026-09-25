"""tests/test_schema_lint.py — schema-lint validates instances and the chain
contract, not only parsing."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "ci"))

import check_schema_lint as lint  # noqa: E402

GUARD = str(ROOT / "tools/ci/check_schema_lint.py")


def run(root):
    return subprocess.run([sys.executable, GUARD, "--root", str(root)], capture_output=True, text=True)


def test_schema_lint_passes_on_repo():
    r = run(ROOT)
    assert r.returncode == 0, r.stdout + r.stderr


def test_schema_lint_fails_on_parse_errors():
    assert run(ROOT / "tests/fixtures/negative/schema_lint").returncode != 0


def test_schema_lint_fails_on_invalid_instances():
    r = run(ROOT / "tests/fixtures/negative/schema_instance")
    assert r.returncode != 0
    assert "must equal its path id" in r.stdout
    assert "fund_binding/fund_profile_id" in r.stdout


def test_chain_check_catches_undeclared_duplicate_and_cycle():
    bad = {
        "nodes": {"core": ["A", "B"]},
        "edges": {"causal": [["A", "B"], ["A", "B"], ["B", "A"], ["A", "Ghost"]]},
        "required_stages": ["A"],
    }
    msgs = "\n".join(lint.check_chain(bad))
    assert "undeclared node Ghost" in msgs
    assert "duplicate causal edge" in msgs
    assert "causal cycle" in msgs


def test_real_chain_is_clean():
    import yaml
    chain = yaml.safe_load((ROOT / "spec/common/chain.yaml").read_text(encoding="utf-8"))
    assert lint.check_chain(chain) == []
