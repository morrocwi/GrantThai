"""grantthai.mcp.server — GrantThai as an MCP server over stdio.

    grantthai-mcp [--root DIR] [--transport auto|sdk|builtin]
    python -m grantthai.mcp [--root DIR] [--transport auto|sdk|builtin]

Two transports serve the same tools (grantthai.mcp.tools):
  sdk      the official `mcp` Python SDK (pip install "grantthai[mcp]");
  builtin  a minimal JSON-RPC 2.0 stdio loop with no extra dependency
           (initialize, ping, tools/list, tools/call, resources/list,
           resources/read). `auto` (default) uses sdk when importable.

stdout carries protocol messages only; diagnostics go to stderr.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, TextIO

from grantthai.mcp import tools as T

PROTOCOL_VERSIONS = ("2025-06-18", "2025-03-26", "2024-11-05")


# ---------------------------------------------------------------------------
# builtin JSON-RPC transport
# ---------------------------------------------------------------------------

def _result(obj: dict) -> dict:
    return {"content": [{"type": "text", "text": T.dumps(obj)}], "structuredContent": obj, "isError": False}


def _error_result(msg: str) -> dict:
    return {"content": [{"type": "text", "text": msg}], "isError": True}


def handle_message(ctx: T.Context, msg: Any) -> dict | None:
    """Handle one JSON-RPC message. Returns the response, or None for a
    notification."""
    if not isinstance(msg, dict) or msg.get("jsonrpc") != "2.0" or not isinstance(msg.get("method"), str):
        return {"jsonrpc": "2.0", "id": msg.get("id") if isinstance(msg, dict) else None,
                "error": {"code": -32600, "message": "invalid request"}}
    mid = msg.get("id")
    is_note = "id" not in msg
    method = msg["method"]
    params = msg.get("params") or {}

    def ok(result: dict) -> dict:
        return {"jsonrpc": "2.0", "id": mid, "result": result}

    def err(code: int, message: str) -> dict:
        return {"jsonrpc": "2.0", "id": mid, "error": {"code": code, "message": message}}

    if is_note:
        return None  # notifications/initialized, notifications/cancelled, ...
    if method == "initialize":
        client = params.get("clientInfo") or {}
        if isinstance(client, dict) and client.get("name"):
            ctx.client_name = str(client["name"])
        asked = params.get("protocolVersion")
        version = asked if asked in PROTOCOL_VERSIONS else PROTOCOL_VERSIONS[0]
        return ok({"protocolVersion": version,
                   "capabilities": {"tools": {"listChanged": False},
                                    "resources": {"listChanged": False, "subscribe": False}},
                   "serverInfo": T.server_info(), "instructions": T.INSTRUCTIONS})
    if method == "ping":
        return ok({})
    if method == "tools/list":
        return ok({"tools": T.list_tools()})
    if method == "tools/call":
        name = params.get("name")
        if name not in T.HANDLERS:
            return err(-32602, f"unknown tool {name!r}")
        try:
            return ok(_result(T.call_tool(ctx, name, params.get("arguments"))))
        except T.ToolError as exc:
            return ok(_error_result(str(exc)))
    if method == "resources/list":
        return ok({"resources": T.list_resources()})
    if method == "resources/templates/list":
        return ok({"resourceTemplates": []})
    if method == "resources/read":
        uri = params.get("uri")
        try:
            text, mime = T.read_resource(uri)
        except T.ToolError as exc:
            return err(-32002, str(exc))
        return ok({"contents": [{"uri": uri, "mimeType": mime, "text": text}]})
    if method == "prompts/list":
        return ok({"prompts": []})
    return err(-32601, f"method not found: {method}")


def serve_builtin(ctx: T.Context, stdin: TextIO | None = None, stdout: TextIO | None = None) -> int:
    """Newline-delimited JSON-RPC over stdio (MCP stdio transport)."""
    stdin = stdin or sys.stdin
    stdout = stdout or sys.stdout
    for line in stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            resp: Any = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "parse error"}}
        else:
            if isinstance(msg, list):
                resp = [r for r in (handle_message(ctx, m) for m in msg) if r is not None] or None
            else:
                resp = handle_message(ctx, msg)
        if resp is not None:
            stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            stdout.flush()
    return 0


# ---------------------------------------------------------------------------
# official SDK transport
# ---------------------------------------------------------------------------

def sdk_available() -> bool:
    """True only for an installed official SDK of the 1.x line: the 2.x
    low-level Server dropped the decorator API this transport uses, so
    with 2.x (or no SDK) the built-in transport is used instead."""
    try:
        from importlib.metadata import version
        if int(version("mcp").split(".")[0]) != 1:
            return False
        import mcp.server.lowlevel  # noqa: F401
        import mcp.server.stdio  # noqa: F401
    except Exception:  # noqa: BLE001 - missing or unreadable SDK
        return False
    return True


def build_sdk_server(ctx: T.Context):
    """The same tools on the official SDK's low-level Server."""
    import mcp.types as mt
    from mcp.server.lowlevel import Server
    from mcp.server.lowlevel.helper_types import ReadResourceContents

    server = Server(T.SERVER_NAME, version=T.server_info()["version"], instructions=T.INSTRUCTIONS)

    def _client_name() -> None:
        if ctx.client_name:
            return
        try:
            info = server.request_context.session.client_params.clientInfo
            ctx.client_name = info.name or None
        except Exception:  # noqa: BLE001 - best effort only
            pass

    @server.list_tools()
    async def _list_tools() -> list[mt.Tool]:
        return [mt.Tool(name=t["name"], description=t["description"], inputSchema=t["inputSchema"],
                        annotations=mt.ToolAnnotations(**t["annotations"])) for t in T.list_tools()]

    @server.call_tool()
    async def _call_tool(name: str, arguments: dict) -> Any:
        _client_name()
        try:
            return T.call_tool(ctx, name, arguments)
        except T.ToolError as exc:
            return mt.CallToolResult(content=[mt.TextContent(type="text", text=str(exc))], isError=True)

    @server.list_resources()
    async def _list_resources() -> list[mt.Resource]:
        return [mt.Resource(**r) for r in T.list_resources()]

    @server.read_resource()
    async def _read_resource(uri) -> list[ReadResourceContents]:
        text, mime = T.read_resource(str(uri))
        return [ReadResourceContents(content=text, mime_type=mime)]

    return server


def serve_sdk(ctx: T.Context) -> int:
    import anyio
    from mcp.server.stdio import stdio_server

    server = build_sdk_server(ctx)

    async def _run() -> None:
        async with stdio_server() as (read, write):
            await server.run(read, write, server.create_initialization_options())

    anyio.run(_run)
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="grantthai-mcp",
                                 description="GrantThai MCP server (stdio): project.yaml -> build/NRIIS_SUBMISSION.md")
    ap.add_argument("--root", default=".", help="folder all project paths are resolved in (default: cwd)")
    ap.add_argument("--transport", choices=("auto", "sdk", "builtin"), default="auto")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve()
    if not root.is_dir():
        print(f"grantthai-mcp: --root {root} is not a folder", file=sys.stderr)
        return 2
    ctx = T.Context(root=root)
    use_sdk = a.transport == "sdk" or (a.transport == "auto" and sdk_available())
    if a.transport == "sdk" and not sdk_available():
        print('grantthai-mcp: the mcp SDK is not installed; pip install "grantthai[mcp]" '
              "or use --transport builtin", file=sys.stderr)
        return 2
    return serve_sdk(ctx) if use_sdk else serve_builtin(ctx)


if __name__ == "__main__":
    sys.exit(main())
