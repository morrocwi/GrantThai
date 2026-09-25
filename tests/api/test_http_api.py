"""tests/api/test_http_api.py — the local HTTP API (grantthai.api).

Driven through a small in-process WSGI test client, plus one real-socket
round trip. Checks that every endpoint is a thin wrapper over
grantthai.api_py, that the hard ceiling holds over HTTP, and that
spec/api/openapi.yaml matches the routes."""
import io
import json
import re
import shutil
import sys
import threading
import urllib.request
from pathlib import Path
from wsgiref.simple_server import WSGIRequestHandler, make_server

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from grantthai import api_py  # noqa: E402
from grantthai.api import make_app  # noqa: E402

EXAMPLE = ROOT / "examples/lecturer-no-ai/project.yaml"
OPENAPI = ROOT / "spec/api/openapi.yaml"
AS_OF = "2026-09-25"


class Client:
    def __init__(self, app):
        self.app = app

    def request(self, method, path, body=None, raw=None):
        path, _, qs = path.partition("?")
        data = raw if raw is not None else (b"" if body is None else json.dumps(body).encode("utf-8"))
        environ = {"REQUEST_METHOD": method, "PATH_INFO": path, "QUERY_STRING": qs,
                   "CONTENT_LENGTH": str(len(data)), "CONTENT_TYPE": "application/json",
                   "wsgi.input": io.BytesIO(data)}
        out = {}

        def start_response(status, headers):
            out["status"] = int(status.split()[0])
            out["headers"] = dict(headers)

        body_bytes = b"".join(self.app(environ, start_response))
        ctype = out["headers"]["Content-Type"]
        text = body_bytes.decode("utf-8")
        return out["status"], ctype, (json.loads(text) if ctype.startswith("application/json") else text)

    def get(self, path):
        return self.request("GET", path)

    def post(self, path, body=None):
        return self.request("POST", path, body)

    def patch(self, path, body=None):
        return self.request("PATCH", path, body)


@pytest.fixture
def client(tmp_path):
    return Client(make_app(tmp_path / "work"))


@pytest.fixture
def example_client(tmp_path):
    work = tmp_path / "work"
    (work / "lecturer").mkdir(parents=True)
    shutil.copy(EXAMPLE, work / "lecturer" / "project.yaml")
    return Client(make_app(work)), work


def _required_field(record_type="string"):
    for f in api_py.list_fields(required_only=True):
        if f["type"] == record_type and not f["chain_node"] and not f["allowed_values"]:
            return f["field_id"]
    pytest.skip(f"no plain required {record_type} field in the registry")


# ----------------------------------------------------------------- basics

def test_health_and_fields(client):
    s, _, j = client.get("/health")
    assert s == 200 and j["can_submit"] is False and j["max_status"] == "DRAFT"
    s, _, j = client.get("/fields?required=true")
    assert s == 200 and j["fields"] == api_py.list_fields(required_only=True)
    assert all(f["required"] for f in j["fields"])


def test_explain_rule(client):
    s, _, j = client.get("/rules/B002")
    assert s == 200 and j == api_py.explain("B002")
    s, _, j = client.get("/rules/NOPE999")
    assert s == 404 and "error" in j


def test_unknown_route_and_method(client):
    assert client.get("/nope")[0] == 404
    assert client.request("DELETE", "/projects")[0] == 405


# ------------------------------------------------------------ full flow

def test_create_set_validate_build(client, tmp_path):
    s, _, j = client.post("/projects", {"project_id": "demo-1"})
    assert s == 201 and j["id"] == "demo-1"
    assert (tmp_path / "work/demo-1/project.yaml").is_file()
    assert client.post("/projects", {"project_id": "demo-1"})[0] == 409

    fid = _required_field()
    s, _, j = client.patch("/projects/demo-1/fields", {"field_id": fid, "value": "Researcher's own text"})
    assert s == 200 and j["written"][0]["status"] == "DRAFT"

    s, _, rep = client.post("/projects/demo-1/validate", {"as_of": AS_OF})
    assert s == 200 and set(rep["summary"]) >= {"block", "review", "info"}
    assert rep == api_py.validate(tmp_path / "work/demo-1/project.yaml", as_of=AS_OF)

    s, ctype, md = client.post("/projects/demo-1/build", {"as_of": AS_OF})
    assert s == 200 and ctype.startswith("text/markdown")
    assert "NEEDS_INPUT" in md
    built = list((tmp_path / "work/demo-1").rglob("*.md"))
    assert built == [tmp_path / "work/demo-1/build/NRIIS_SUBMISSION.md"]
    assert built[0].read_text(encoding="utf-8") == md


def test_generated_id(client):
    s, _, j = client.post("/projects")
    assert s == 201 and re.fullmatch(r"p-[0-9a-f]{12}", j["id"])
    assert j["project"]["project_id"] == "NEEDS_INPUT"
    s, _, g = client.get(f"/projects/{j['id']}")
    assert s == 200 and g["project"] == j["project"]


def test_example_build_matches_engine_and_is_deterministic(example_client, tmp_path):
    client, work = example_client
    s, _, md1 = client.post("/projects/lecturer/build", {"as_of": AS_OF})
    s2, _, md2 = client.post("/projects/lecturer/build", {"as_of": AS_OF})
    assert s == s2 == 200 and md1 == md2
    ref_dir = tmp_path / "ref"
    ref_dir.mkdir()
    shutil.copy(EXAMPLE, ref_dir / "project.yaml")
    ref = api_py.build(ref_dir / "project.yaml", as_of=AS_OF).read_text(encoding="utf-8")
    assert md1 == ref
    s, _, j = client.post("/projects/lecturer/build?format=json", {"as_of": AS_OF})
    assert s == 200 and j["markdown"] == ref and j["filename"] == "NRIIS_SUBMISSION.md"
    assert j["summary"]["block"] == 0


def test_validate_is_report_only(example_client):
    client, work = example_client
    before = (work / "lecturer/project.yaml").read_bytes()
    assert client.post("/projects/lecturer/validate", {"as_of": AS_OF})[0] == 200
    assert (work / "lecturer/project.yaml").read_bytes() == before


# ------------------------------------------------------ hard ceiling

def test_ai_draft_is_marked_and_never_source(client, tmp_path):
    client.post("/projects", {"project_id": "ai"})
    fid = _required_field()
    s, _, j = client.patch("/projects/ai/fields", {"field_id": fid, "value": "drafted", "actor": "ai_assisted",
                                                   "tool": "some-assistant"})
    assert s == 200
    rec = j["written"][0]
    assert rec["status"] == "DRAFT"
    assert rec["provenance"]["authored_by"] == "ai_draft"
    assert rec["provenance"]["provenance_class"] == "INFERENCE"
    doc = api_py.load(tmp_path / "work/ai/project.yaml")
    assert doc["authoring"]["mode"] == "ai_assisted"
    assert "some-assistant" in doc["authoring"]["tools_disclosed"]

    before = (tmp_path / "work/ai/project.yaml").read_bytes()
    s, _, j = client.patch("/projects/ai/fields", {"field_id": fid, "value": "x", "actor": "ai_assisted",
                                                   "provenance": {"provenance_class": "SOURCE"}})
    assert s == 400 and "SOURCE" in j["error"]
    assert (tmp_path / "work/ai/project.yaml").read_bytes() == before


def test_every_http_write_is_ai_assisted(client, tmp_path):
    """No actor given still records an AI draft; actor human is refused;
    the researcher's own words go in with researcher_verbatim."""
    client.post("/projects", {"project_id": "aa"})
    fid = _required_field()
    s, _, j = client.patch("/projects/aa/fields", {"field_id": fid, "value": "no actor sent"})
    assert s == 200
    rec = j["written"][0]
    assert rec["provenance"]["authored_by"] == "ai_draft"
    assert rec["provenance"]["provenance_class"] == "INFERENCE"
    doc = api_py.load(tmp_path / "work/aa/project.yaml")
    assert doc["authoring"]["mode"] == "ai_assisted" and doc["authoring"]["tools_disclosed"]

    s, _, j = client.patch("/projects/aa/fields", {"field_id": fid, "value": "x", "actor": "human"})
    assert s == 400 and "actor" in j["error"]
    s, _, j = client.patch("/projects/aa/fields", {"field_id": fid, "value": "x",
                                                   "provenance": {"authored_by": "human"}})
    assert s == 400 and "authored_by" in j["error"]
    s, _, j = client.patch("/projects/aa/fields", {"field_id": fid, "value": "x", "researcher_verbatim": True,
                                                   "provenance": {"provenance_class": "SOURCE"}})
    assert s == 400 and "SOURCE" in j["error"]

    s, _, j = client.patch("/projects/aa/fields", {"field_id": fid, "value": "researcher's words",
                                                   "researcher_verbatim": True})
    rec = j["written"][0]
    assert s == 200 and rec["status"] == "DRAFT"
    assert rec["provenance"]["authored_by"] == "human_ai_assisted"
    assert rec["provenance"]["provenance_class"] == "DECISION"


def test_status_cannot_be_raised_through_patch(client):
    client.post("/projects", {"project_id": "st"})
    fid = _required_field()
    s, _, j = client.patch("/projects/st/fields", {"field_id": fid, "value": "v", "status": "APPROVED"})
    assert s == 400 and "status" in j["error"]


def test_needs_verification_becomes_marker(client):
    client.post("/projects", {"project_id": "nv"})
    fid = _required_field()
    s, _, j = client.patch("/projects/nv/fields", {"field_id": fid, "value": "NEEDS_VERIFICATION"})
    rec = j["written"][0]
    assert s == 200 and rec["value"] is None and "NEEDS_VERIFICATION" in rec["markers"]


def test_batch_is_all_or_nothing(client, tmp_path):
    client.post("/projects", {"project_id": "b"})
    fid = _required_field()
    before = (tmp_path / "work/b/project.yaml").read_bytes()
    s, _, j = client.patch("/projects/b/fields", {"updates": [
        {"field_id": fid, "value": "ok"},
        {"field_id": "NOT_A_FIELD", "value": "x"},
    ]})
    assert s == 400 and "update 1" in j["error"]
    assert (tmp_path / "work/b/project.yaml").read_bytes() == before


# --------------------------------------------------- input handling

@pytest.mark.parametrize("pid", ["../etc", "a/b", "..", ".hidden", "x" * 65])
def test_bad_project_ids_rejected(client, pid):
    s, _, _ = client.post("/projects", {"project_id": pid})
    assert s == 400


def test_path_traversal_in_url(client):
    s, _, _ = client.get("/projects/..%2F..%2Fetc")
    assert s in (400, 404)
    assert client.post("/projects/..%2Fx/build")[0] in (400, 404)


def test_bad_inputs(client):
    client.post("/projects", {"project_id": "in"})
    assert client.request("POST", "/projects", raw=b"{not json")[0] == 400
    assert client.post("/projects", {"project_id": "z", "extra": 1})[0] == 400
    assert client.post("/projects", {"mode": "bogus"})[0] == 400
    assert client.post("/projects/in/validate", {"as_of": "tomorrow"})[0] == 400
    assert client.post("/projects/in/build?format=pdf")[0] == 400
    assert client.post("/projects/missing/validate")[0] == 404
    assert client.patch("/projects/in/fields", {"updates": []})[0] == 400
    assert client.patch("/projects/in/fields", {"field_id": "x"})[0] == 400


# ------------------------------------------------------------ OpenAPI

def _route_templates(app):
    out = set()
    for method, rx, _ in app.routes:
        tpl = rx.pattern.strip("^$").replace("\\.", ".")
        tpl = re.sub(r"\(\?P<(\w+)>\[\^/\]\+\)", r"{\1}", tpl).replace("{pid}", "{id}")
        out.add((method.lower(), tpl))
    return out


def test_openapi_matches_routes(client):
    spec = yaml.safe_load(OPENAPI.read_text(encoding="utf-8"))
    assert spec["openapi"].startswith("3.1")
    documented = {(m, p) for p, ops in spec["paths"].items() for m in ops}
    served = {r for r in _route_templates(client.app) if not r[1].startswith("/openapi")}
    assert documented == served
    op_ids = [op["operationId"] for ops in spec["paths"].values() for op in ops.values()]
    assert len(op_ids) == len(set(op_ids))
    assert spec["servers"][0]["url"].startswith("http://127.0.0.1")


def test_openapi_served(client):
    s, ctype, text = client.get("/openapi.yaml")
    assert s == 200 and ctype.startswith("application/yaml") and text == OPENAPI.read_text(encoding="utf-8")
    s, _, j = client.get("/openapi.json")
    assert s == 200 and j == yaml.safe_load(text)


def test_openapi_schemas_are_valid_and_describe_responses(client):
    jsonschema = pytest.importorskip("jsonschema")
    spec = yaml.safe_load(OPENAPI.read_text(encoding="utf-8"))
    comps = spec["components"]["schemas"]
    for name, sch in comps.items():
        jsonschema.Draft202012Validator.check_schema(sch)
    v = jsonschema.Draft202012Validator(comps["FieldInfo"])
    for f in client.get("/fields")[2]["fields"]:
        v.validate(f)


# ------------------------------------------------------- real socket

class _Quiet(WSGIRequestHandler):
    def log_message(self, *a):
        pass


def test_real_socket_round_trip(tmp_path):
    srv = make_server("127.0.0.1", 0, make_app(tmp_path / "w"), handler_class=_Quiet)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    try:
        base = f"http://127.0.0.1:{srv.server_port}"
        req = urllib.request.Request(base + "/projects", data=json.dumps({"project_id": "sock"}).encode(),
                                     headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=10) as r:
            assert r.status == 201
        req = urllib.request.Request(base + "/projects/sock/build", data=json.dumps({"as_of": AS_OF}).encode(),
                                     headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=30) as r:
            assert r.status == 200 and "text/markdown" in r.headers["Content-Type"]
            assert r.read().decode("utf-8")
    finally:
        srv.shutdown()
        srv.server_close()


def test_main_refuses_non_loopback_without_flag():
    from grantthai.api.__main__ import _is_loopback, main
    assert _is_loopback("127.0.0.1") and _is_loopback("::1")
    assert not _is_loopback("0.0.0.0")
    with pytest.raises(SystemExit):
        main(["--host", "0.0.0.0", "--port", "0"])
