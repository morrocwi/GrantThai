"""AT-R1 (v0.3 router): a legacy project.yaml built with no route, with
--route nriis-proposal, and through `route build` gives a
build/NRIIS_SUBMISSION.md byte-identical to the golden snapshot rendered
before the router existed (tests/golden/routes/, from corpus-100)."""
import shutil
from pathlib import Path

import pytest

from grantthai import api_py as api
from grantthai.cli import main

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "tests/golden/routes"
AS_OF = "2026-09-25"
EXAMPLES = ["lecturer-no-ai", "demo-seedbank"]


def _golden(ex: str) -> bytes:
    return (GOLDEN / ex / "NRIIS_SUBMISSION.md").read_bytes()


@pytest.mark.parametrize("ex", EXAMPLES)
def test_cli_build_three_ways_is_byte_identical_to_golden(ex, tmp_path):
    src = ROOT / "examples" / ex / "project.yaml"
    argvs = {
        "build": ["build", str(src)],
        "build-route": ["build", str(src), "--route", "nriis-proposal"],
        "route-build": ["route", "build", "--route", "nriis-proposal", str(src)],
        "build-dir": ["build", str(src.parent), "--route", "nriis-proposal"],
    }
    for name, argv in argvs.items():
        out = tmp_path / name
        assert main(argv + ["--out", str(out), "--as-of", AS_OF]) == 0, name
        assert sorted(p.name for p in out.iterdir()) == ["NRIIS_SUBMISSION.md"], name
        assert (out / "NRIIS_SUBMISSION.md").read_bytes() == _golden(ex), name


@pytest.mark.parametrize("ex", EXAMPLES)
def test_api_build_with_and_without_route_is_byte_identical(ex, tmp_path):
    shutil.copy(ROOT / "examples" / ex / "project.yaml", tmp_path / "project.yaml")
    a = api.build(tmp_path / "project.yaml", as_of=AS_OF).read_bytes()
    b = api.build(tmp_path, route="nriis-proposal", out_dir=tmp_path / "b", as_of=AS_OF).read_bytes()
    assert a == b == _golden(ex)
    assert sorted(p.name for p in (tmp_path / "build").iterdir()) == ["NRIIS_SUBMISSION.md"]


@pytest.mark.parametrize("ex", EXAMPLES)
def test_legacy_report_has_no_router_or_article_findings(ex):
    rep = api.validate(ROOT / "examples" / ex / "project.yaml", as_of=AS_OF)
    ids = {f["rule_id"] for f in rep["findings"]}
    assert not {i for i in ids if i.startswith(("ART", "RT"))}
    assert rep == api.validate(ROOT / "examples" / ex / "project.yaml", as_of=AS_OF, route="nriis-proposal")


def test_migrated_work_yaml_changes_only_version_and_hashes(tmp_path):
    """A migrated 0.3 work.yaml (form_profile moved under routing) renders the
    same NRIIS file apart from schema_version and the two object hashes."""
    shutil.copy(ROOT / "examples/demo-seedbank/project.yaml", tmp_path / "project.yaml")
    res = api.migrate(tmp_path / "project.yaml", rename=True)
    assert res["written"].endswith("work.yaml") and not (tmp_path / "project.yaml").exists()
    out = api.build(tmp_path, as_of=AS_OF).read_text(encoding="utf-8").splitlines()
    gold = _golden("demo-seedbank").decode("utf-8").splitlines()
    assert len(out) == len(gold)
    diff = [(a, b) for a, b in zip(out, gold) if a != b]
    assert [a.split(":", 1)[0] for a, _ in diff] == ["schema_version", "project_content_sha256",
                                                    "project_state_sha256"]
