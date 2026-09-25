"""tests/test_negative_fixtures.py — one real, on-disk negative fixture per
BLOCK rule that ships in v0.1 (AT-4). Each `tests/fixtures/negative/<RULE_ID>/`
holds a mutated copy of the FICTIONAL worked example (`project.yaml`) that
makes exactly that rule fire, plus `expected.json` naming the rule and its
severity. `validators/rules.yaml`'s `negative_fixture` field points here for
every such rule.

Also covers the small remainder explicitly, per rule.schema.json's
`not_evaluated_in_v0.1` convention:
- B003, B004, F004 ship v0.1 but are not evaluated by this build
  (`grantthai.validators.engine.V01_NOT_EVALUATED`) -> asserted here as the
  INFO "not evaluated" finding the engine always emits for them.
- B005 (REVIEW, evaluated) fires on a dedicated mutation, since v0.1's BLOCK
  rules are the only ones that get their own fixture directory.
"""
import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from grantthai import api_py as api  # noqa: E402
from grantthai.core import project as P  # noqa: E402
from grantthai.validators import engine as E  # noqa: E402

NEG_DIR = ROOT / "tests/fixtures/negative"
EXAMPLE = ROOT / "examples/lecturer-no-ai/project.yaml"
AS_OF = "2026-09-25"
RULE_DIR_RE = re.compile(r"^[A-Z]{1,4}[0-9]{3}$")

RULE_FIXTURE_DIRS = sorted(
    d for d in NEG_DIR.iterdir()
    if d.is_dir() and RULE_DIR_RE.match(d.name) and (d / "project.yaml").is_file()
)

# Every BLOCK rule that ships in v0.1 and IS evaluated by this build must
# have a fixture directory here (AT-4). Kept in sync with validators/rules.yaml.
EXPECTED_BLOCK_V01_EVALUATED = {
    "S001", "S002", "S003", "S004", "S005", "S006", "S007", "S008", "S012",
    "R003", "R004", "R005", "R006", "R007",
    "W001", "W003", "W004",
    "B001", "B002", "B006",
    "T001", "T002",
    "CH001", "CH002",
    "F001", "F003",
    "ELIG001",
    "X003",
}


def test_every_block_v01_evaluated_rule_has_a_fixture_dir():
    catalog = {r["id"]: r for r in P.rules_catalog()["rules"]}
    have = {d.name for d in RULE_FIXTURE_DIRS}
    for rid in EXPECTED_BLOCK_V01_EVALUATED:
        rule = catalog[rid]
        assert rule["ships"] == "v0.1" and rule["severity"] == "BLOCK"
        assert rid not in E.V01_NOT_EVALUATED
        assert rid in have, f"{rid}: BLOCK v0.1 evaluated rule has no tests/fixtures/negative/{rid}/"
    # and every rule-id-shaped fixture dir on disk is one we mean to have
    assert have == EXPECTED_BLOCK_V01_EVALUATED


@pytest.mark.parametrize("d", RULE_FIXTURE_DIRS, ids=lambda d: d.name)
def test_negative_fixture_rule_fires(d, tmp_path):
    expected = json.loads((d / "expected.json").read_text(encoding="utf-8"))
    assert expected["rule_id"] == d.name
    rep = api.validate(d / "project.yaml", as_of=expected.get("as_of", AS_OF))
    hits = [f for f in rep["findings"] if f["rule_id"] == d.name]
    assert hits, f"{d.name}: rule did not fire on its negative fixture"
    assert all(f["severity"] == expected["must_fire_severity"] for f in hits)


# -------------------------------------------------- not evaluated in v0.1 --

@pytest.mark.parametrize("rule_id", sorted(E.V01_NOT_EVALUATED))
def test_not_evaluated_in_v01_reports_info(rule_id):
    """B003, B004, F004: ship v0.1 but this build does not evaluate them, so
    every report carries exactly one INFO finding for the id instead of a
    BLOCK/REVIEW one (no silent skip)."""
    rep = api.validate(EXAMPLE, as_of=AS_OF)
    hits = [f for f in rep["findings"] if f["rule_id"] == rule_id]
    assert len(hits) == 1
    assert hits[0]["severity"] == "INFO"
    assert "not evaluated" in hits[0]["message_en"]


def test_v01_not_evaluated_set_matches_explicit_findings_list():
    # The explicit list this task named: B003, B004, F004 not evaluated;
    # B005, B006, F001, F003, ELIG001 evaluated (B006/F001/F003/ELIG001 get
    # their own fixture dir above; B005 gets its own mutation test below).
    assert E.V01_NOT_EVALUATED.keys() >= {"B003", "B004", "F004"}
    for rid in ("B005", "B006", "F001", "F003", "ELIG001"):
        assert rid not in E.V01_NOT_EVALUATED


# --------------------------------------------------------- B005 (REVIEW) --

def test_negative_equipment_no_justification_B005(tmp_path):
    """B005: an equipment line has no stated necessity. The example project
    has no equipment record at all, so this adds one instead of mutating an
    existing one."""
    doc = P.load(EXAMPLE)
    doc["fields"].append({
        "field_id": "BUDGET.PLAN.EQUIPMENT",
        "value": [{
            "id": "EQ1",
            "name": "FICTIONAL: field laptop",
            "quantity": 1,
            "unit_price": 20000,
            "total": 20000,
        }],
        "status": "DRAFT",
        "provenance": {
            "provenance_class": "DECISION", "source_type": "PROJECT_DOCUMENT",
            "evidence_role": "ORIENTING", "authored_by": "human",
        },
    })
    path = tmp_path / "project.yaml"
    P.save(doc, path)
    rep = api.validate(path, as_of=AS_OF)
    assert any(f["rule_id"] == "B005" and f["severity"] == "REVIEW" for f in rep["findings"])
