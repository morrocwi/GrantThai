"""python -m grantthai.api — serve the local HTTP API (standard library)."""
from __future__ import annotations

import argparse
import ipaddress
import sys
from wsgiref.simple_server import WSGIRequestHandler, make_server

from grantthai.api.app import make_app


class _QuietHandler(WSGIRequestHandler):
    def log_message(self, format, *args):  # request line only, never bodies
        sys.stderr.write("%s %s\n" % (self.command, self.path.split("?")[0]))


def _is_loopback(host: str) -> bool:
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m grantthai.api",
                                 description="GrantThai local HTTP API (project.yaml -> build/NRIIS_SUBMISSION.md).")
    ap.add_argument("--host", default="127.0.0.1", help="bind address (default 127.0.0.1, local only)")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--workdir", default="grantthai-work",
                    help="folder holding one sub-folder per project (default ./grantthai-work)")
    ap.add_argument("--allow-remote", action="store_true",
                    help="required to bind a non-loopback address; the API has no authentication")
    a = ap.parse_args(argv)
    if not _is_loopback(a.host) and not a.allow_remote:
        ap.error(f"{a.host} is not a loopback address; the API has no authentication. "
                 "Pass --allow-remote only behind your own authenticating proxy.")
    app = make_app(a.workdir)
    with make_server(a.host, a.port, app, handler_class=_QuietHandler) as srv:
        print(f"GrantThai API on http://{a.host}:{srv.server_port}  workdir={app.workdir}  "
              f"(OpenAPI: /openapi.yaml)", file=sys.stderr)
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
