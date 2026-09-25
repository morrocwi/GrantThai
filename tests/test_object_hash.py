"""tests/test_object_hash.py — spec/common/object-hash.md: golden vectors,
and the content hash is unaffected by review/status state."""
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from grantthai.core.object_hash import (  # noqa: E402
    canonical_bytes, content_sha256, content_view, load_project_text, state_sha256,
)

GOLDEN = ROOT / "tests/golden/object-hash"


def load(path):
    return load_project_text(Path(path).read_text(encoding="utf-8"))


def test_golden_vectors():
    for vec in json.loads((GOLDEN / "expected.json").read_text(encoding="utf-8")):
        doc = load(GOLDEN / vec["input"])
        assert content_sha256(doc) == vec["content_sha256"], vec["input"]
        assert state_sha256(doc) == vec["state_sha256"], vec["input"]
        if "canonical_content_json" in vec:
            assert canonical_bytes(content_view(doc)).decode("utf-8") == vec["canonical_content_json"]


def test_review_record_and_status_changes_do_not_change_content_hash():
    doc = load(ROOT / "examples/lecturer-no-ai/project.yaml")
    before_content, before_state = content_sha256(doc), state_sha256(doc)

    reviewed = copy.deepcopy(doc)
    reviewed["review_records"].append({
        "gate_id": "RG0", "reviewer_name": "FICTIONAL Reviewer", "reviewer_role": "lecturer",
        "scope": "Problem, PriorKnowledge", "independence": "self", "date": "2026-09-25",
        "content_sha256": before_content, "outcome": "HUMAN_REVIEWED",
    })
    for rec in reviewed["fields"] + [r for recs in reviewed["chain"].values() for r in recs]:
        rec["status"] = "HUMAN_REVIEWED"
    reviewed["lock"] = {"locked": True, "locked_at": "2026-09-25", "locked_by": "FICTIONAL Lecturer A",
                        "locked_content_sha256": before_content}

    assert content_sha256(reviewed) == before_content          # review stays current
    assert state_sha256(reviewed) != before_state              # but the state changed
    assert reviewed["review_records"][0]["content_sha256"] == content_sha256(reviewed)


def test_authored_edits_change_content_hash():
    doc = load(ROOT / "examples/lecturer-no-ai/project.yaml")
    h = content_sha256(doc)
    for mutate in (
        lambda d: d["fields"][0].__setitem__("value", 2028),
        lambda d: d["fields"][0].__setitem__("markers", ["NEEDS_VERIFICATION"]),
        lambda d: d["chain"]["RQ"][0]["links"].__setitem__("gap_ids", []),
        lambda d: d["sources"][0].__setitem__("locator", "Table 4"),
    ):
        d = copy.deepcopy(doc)
        mutate(d)
        assert content_sha256(d) != h


def test_loader_is_yaml12_like():
    doc = load_project_text("a: yes\nb: 2026-09-25\nc: true\nd: off\n")
    assert doc == {"a": "yes", "b": "2026-09-25", "c": True, "d": "off"}


def test_nfc_and_number_form():
    composed = load_project_text('v: "Caf\\u00e9"\nn: 1500.0\n')
    decomposed = load_project_text('v: "Cafe\\u0301"\nn: 1500\n')
    assert canonical_bytes(composed) == canonical_bytes(decomposed) == '{"n":1500,"v":"Café"}'.encode()
