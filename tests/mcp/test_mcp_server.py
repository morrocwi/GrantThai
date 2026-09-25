"""tests/mcp/test_mcp_server.py — the MCP surface (grantthai.mcp).

Tools are called in-process through grantthai.mcp.tools.call_tool and the
builtin JSON-RPC handler; one test runs the stdio server as a subprocess,
and one drives the official SDK transport when `mcp` is installed."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from grantthai.core import project as P  # noqa: E402
from grantthai.mcp import server as S  # noqa: E402
from grantthai.mcp import tools as T  # noqa: E402

EXAMPLE = ROOT / "examples/lecturer-no-ai/project.yaml"
AS_OF = "2026-09-25"
NOTICE = (ROOT / "spec/output/notice_constant.txt").read_text(encoding="utf-8").rstrip("\n")
EXPECTED_TOOLS = {"grantthai_new_project", "grantthai_list_fields", "grantthai_set_field",
                  "grantthai_validate", "grantthai_explain", "grantthai_build"}
STATUS_RANK = {"NEEDS_INPUT": 0, "EMPTY": 0, "DRAFT": 1}


@pytest.fixture
def ctx(tmp_path):
    return T.Context(root=tmp_path, client_name="test-client")


@pytest.fixture
def example(tmp_path):
    shutil.copy(EXAMPLE, tmp_path / "project.yaml")
    return tmp_path / "project.yaml"


def _statuses(path):
    return {r["field_id"]: r.get("status") for r, _ in P.iter_records(P.load(path))}


def test_tool_list_matches_spec_contract():
    spec = json.loads((ROOT / "spec/mcp/tools.schema.json").read_text(encoding="utf-8"))
    example = spec["examples"][0]
    jsonschema.validate(example, spec)
    names = {t["name"] for t in T.list_tools()}
    assert names == EXPECTED_TOOLS == {t["name"] for t in example["tools"]}
    for t in example["tools"]:
        assert t["max_status_ceiling"] == "DRAFT" and t["can_submit"] is False
        assert t["wraps_cli_command"] == T.TOOLS_BY_NAME[t["name"]]["wraps_cli_command"]
        assert t["status_effect"] == T.TOOLS_BY_NAME[t["name"]]["status_effect"]
    for t in T.list_tools():
        jsonschema.Draft202012Validator.check_schema(t["inputSchema"])


def test_wrapped_cli_commands_exist():
    from grantthai import cli
    src = Path(cli.__file__).read_text(encoding="utf-8")
    for t in T.TOOL_SPECS:
        sub = t["wraps_cli_command"].split()[1]
        assert f'add_parser("{sub}"' in src, sub


def test_full_flow_blank_project(ctx, tmp_path):
    r = T.call_tool(ctx, "grantthai_new_project", {"project_id": "PRJ-TEST"})
    assert r["project_path"] == "project.yaml" and r["needs_input"]
    with pytest.raises(T.ToolError, match="already exists"):
        T.call_tool(ctx, "grantthai_new_project", {})

    fields = T.call_tool(ctx, "grantthai_list_fields", {"required_only": True})
    assert fields["count"] == len(fields["fields"]) > 0
    fid = next(f["field_id"] for f in fields["fields"] if f["type"] == "string")

    rec = T.call_tool(ctx, "grantthai_set_field", {"field_id": fid, "value": "A draft title"})["record"]
    assert rec["status"] == "DRAFT"
    assert rec["provenance"]["authored_by"] == "ai_draft"
    assert rec["provenance"]["provenance_class"] == "INFERENCE"
    doc = P.load(tmp_path / "project.yaml")
    assert doc["authoring"]["mode"] == "ai_assisted"
    assert "test-client" in doc["authoring"]["tools_disclosed"]

    rep = T.call_tool(ctx, "grantthai_validate", {"as_of": AS_OF})
    assert rep["summary"]["block"] > 0  # blank project still has missing required fields
    before = (tmp_path / "project.yaml").read_bytes()
    T.call_tool(ctx, "grantthai_validate", {"as_of": AS_OF})
    assert (tmp_path / "project.yaml").read_bytes() == before  # report-only

    b = T.call_tool(ctx, "grantthai_build", {"as_of": AS_OF})
    assert b["path"] == "build/NRIIS_SUBMISSION.md"
    assert b["markdown"] == (tmp_path / "build/NRIIS_SUBMISSION.md").read_text(encoding="utf-8")
    assert "NEEDS_INPUT" in b["markdown"]
    assert "A draft title" in b["markdown"]
    assert sorted(p.name for p in (tmp_path / "build").iterdir()) == ["NRIIS_SUBMISSION.md"]


def test_build_example_one_file_zero_block_deterministic(ctx, example, tmp_path):
    b1 = T.call_tool(ctx, "grantthai_build", {"as_of": AS_OF})
    b2 = T.call_tool(ctx, "grantthai_build", {"as_of": AS_OF})
    assert b1["summary"]["block"] == 0
    assert b1["markdown"] == b2["markdown"]
    assert NOTICE in b1["markdown"]
    assert [p.name for p in (tmp_path / "build").iterdir()] == ["NRIIS_SUBMISSION.md"]


def test_status_never_above_draft_and_never_source(ctx, example):
    fids = [f["field_id"] for f in T.call_tool(ctx, "grantthai_list_fields", {})["fields"]
            if f["type"] == "string"][:5]
    for fid in fids:
        T.call_tool(ctx, "grantthai_set_field", {"field_id": fid, "value": "x", "researcher_verbatim": True})
    st = _statuses(example)
    for fid in fids:
        assert STATUS_RANK[st[fid]] <= STATUS_RANK["DRAFT"]
    for r, _ in P.iter_records(P.load(example)):
        if r["field_id"] in fids:
            assert r["provenance"]["provenance_class"] != "SOURCE"
            assert r["provenance"]["authored_by"] == "human_ai_assisted"
            assert r["provenance"]["provenance_class"] == "DECISION"
    # SOURCE and status cannot even be requested
    for extra in ({"provenance_class": "SOURCE"}, {"status": "REVIEWED"}, {"submit": True}):
        with pytest.raises(T.ToolError, match="invalid arguments"):
            T.call_tool(ctx, "grantthai_set_field", {"field_id": fids[0], "value": "y", **extra})


def test_needs_verification_becomes_marker(ctx, example):
    fid = next(f["field_id"] for f in T.call_tool(ctx, "grantthai_list_fields", {})["fields"]
               if f["type"] == "string")
    rec = T.call_tool(ctx, "grantthai_set_field", {"field_id": fid, "value": "NEEDS_VERIFICATION"})["record"]
    assert rec["value"] is None and "NEEDS_VERIFICATION" in rec["markers"]
    assert rec["status"] == "NEEDS_INPUT"


def test_explain_and_errors(ctx, example):
    assert T.call_tool(ctx, "grantthai_explain", {"rule_id": "S001"})
    with pytest.raises(T.ToolError):
        T.call_tool(ctx, "grantthai_explain", {"rule_id": "NOPE999"})
    with pytest.raises(T.ToolError, match="not in registry"):
        T.call_tool(ctx, "grantthai_set_field", {"field_id": "NOT.A.FIELD", "value": "x"})
    with pytest.raises(T.ToolError, match="outside"):
        T.call_tool(ctx, "grantthai_validate", {"project_path": "../escape/project.yaml"})
    with pytest.raises(T.ToolError, match="outside"):
        T.call_tool(ctx, "grantthai_build", {"out_dir": "/tmp"})
    with pytest.raises(T.ToolError, match="unknown tool"):
        T.call_tool(ctx, "grantthai_submit", {})


def test_resources(ctx):
    uris = {r["uri"] for r in T.list_resources()}
    assert uris == {T.NOTICE_URI, T.FIELDS_URI}
    text, mime = T.read_resource(T.NOTICE_URI)
    assert text.rstrip("\n") == NOTICE and mime == "text/plain"
    text, mime = T.read_resource(T.FIELDS_URI)
    assert mime == "application/json" and json.loads(text)[0]["field_id"]


def test_builtin_jsonrpc_in_process(tmp_path, example):
    ctx = T.Context(root=tmp_path)
    init = S.handle_message(ctx, {"jsonrpc": "2.0", "id": 1, "method": "initialize",
                                  "params": {"protocolVersion": "2025-06-18",
                                             "clientInfo": {"name": "some-client"}, "capabilities": {}}})
    assert init["result"]["serverInfo"]["name"] == "grantthai"
    assert ctx.client_name == "some-client"
    assert S.handle_message(ctx, {"jsonrpc": "2.0", "method": "notifications/initialized"}) is None
    lst = S.handle_message(ctx, {"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    assert {t["name"] for t in lst["result"]["tools"]} == EXPECTED_TOOLS
    ok = S.handle_message(ctx, {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                                "params": {"name": "grantthai_validate", "arguments": {"as_of": AS_OF}}})
    assert ok["result"]["isError"] is False
    assert json.loads(ok["result"]["content"][0]["text"])["summary"]["block"] == 0
    bad = S.handle_message(ctx, {"jsonrpc": "2.0", "id": 4, "method": "tools/call",
                                 "params": {"name": "grantthai_explain", "arguments": {}}})
    assert bad["result"]["isError"] is True
    miss = S.handle_message(ctx, {"jsonrpc": "2.0", "id": 5, "method": "nope"})
    assert miss["error"]["code"] == -32601
    res = S.handle_message(ctx, {"jsonrpc": "2.0", "id": 6, "method": "resources/read",
                                 "params": {"uri": T.NOTICE_URI}})
    assert res["result"]["contents"][0]["text"].rstrip("\n") == NOTICE


def test_builtin_stdio_subprocess(tmp_path, example):
    msgs = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize",
         "params": {"protocolVersion": "2025-06-18", "clientInfo": {"name": "t"}, "capabilities": {}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
         "params": {"name": "grantthai_build", "arguments": {"as_of": AS_OF}}},
    ]
    env = {"PYTHONPATH": str(ROOT / "src"), "PATH": "/usr/bin:/bin"}
    r = subprocess.run([sys.executable, "-m", "grantthai.mcp", "--root", str(tmp_path), "--transport", "builtin"],
                       input="\n".join(json.dumps(m) for m in msgs) + "\n", capture_output=True, text=True,
                       env=env, timeout=120)
    assert r.returncode == 0, r.stderr
    lines = [json.loads(x) for x in r.stdout.splitlines()]
    assert [x["id"] for x in lines] == [1, 2]
    out = lines[1]["result"]["structuredContent"]
    assert out["path"] == "build/NRIIS_SUBMISSION.md" and out["summary"]["block"] == 0
    assert (tmp_path / "build/NRIIS_SUBMISSION.md").exists()


def test_sdk_transport(tmp_path, example):
    pytest.importorskip("mcp")
    import anyio
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    params = StdioServerParameters(command=sys.executable,
                                   args=["-m", "grantthai.mcp", "--root", str(tmp_path), "--transport", "sdk"],
                                   env={"PYTHONPATH": str(ROOT / "src"), "PATH": "/usr/bin:/bin"})

    async def run():
        with anyio.fail_after(120):
            await session()

    async def session():
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as s:
                await s.initialize()
                names = {t.name for t in (await s.list_tools()).tools}
                assert names == EXPECTED_TOOLS
                res = await s.call_tool("grantthai_build", {"as_of": AS_OF})
                assert not res.isError
                assert res.structuredContent["summary"]["block"] == 0
                rec = await s.call_tool("grantthai_set_field",
                                        {"field_id": "NOT.A.FIELD", "value": "x"})
                assert rec.isError
                rr = await s.read_resource(T.NOTICE_URI)
                assert rr.contents[0].text.rstrip("\n") == NOTICE

    anyio.run(run)
    assert (tmp_path / "build/NRIIS_SUBMISSION.md").exists()
