"""grantthai.api.app — the WSGI application (standard library only).

Endpoints (see spec/api/openapi.yaml):

    GET   /health
    GET   /openapi.yaml | /openapi.json
    GET   /fields                        ?tab=&required=true
    GET   /rules/{rule_id}               explain one validator rule
    POST  /projects                      create a blank project.yaml
    GET   /projects/{id}                 read project.yaml (as JSON)
    PATCH /projects/{id}/fields          set one or more fields (DRAFT at most)
    POST  /projects/{id}/validate        validation report (report-only)
    POST  /projects/{id}/build           -> build/NRIIS_SUBMISSION.md text

Every handler is a thin call into grantthai.api_py.
"""
from __future__ import annotations

import json
import re
import secrets
from datetime import date
from pathlib import Path
from typing import Any, Callable
from urllib.parse import parse_qs

import yaml

from grantthai import api_py
from grantthai.core import project as _P

MAX_BODY_BYTES = 1_000_000
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")
SET_KEYS = {"field_id", "value", "actor", "researcher_verbatim", "chain_node", "provenance",
            "source_ids", "links", "tool"}
PROVENANCE_KEYS = {"provenance_class", "source_type", "evidence_role"}
DEFAULT_TOOL_NAME = "http-client"
CREATE_KEYS = {"project_id", "fund_profile_id", "mode"}


class HTTPError(Exception):
    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status
        self.message = message


_REASONS = {200: "OK", 201: "Created", 400: "Bad Request", 404: "Not Found",
            405: "Method Not Allowed", 409: "Conflict", 413: "Payload Too Large",
            500: "Internal Server Error"}


def _openapi_path() -> Path:
    return _P.DATA_ROOT / "spec" / "api" / "openapi.yaml"


def _check_as_of(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise HTTPError(400, "as_of must be a YYYY-MM-DD string")
    try:
        date.fromisoformat(value)
    except ValueError:
        raise HTTPError(400, "as_of must be a YYYY-MM-DD date") from None
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise HTTPError(400, "as_of must be a YYYY-MM-DD date")
    return value


class GrantThaiAPI:
    """WSGI callable. `workdir` holds one folder per project."""

    def __init__(self, workdir: str | Path):
        self.workdir = Path(workdir).resolve()
        self.routes: list[tuple[str, re.Pattern, Callable]] = [
            ("GET", re.compile(r"^/health$"), self.health),
            ("GET", re.compile(r"^/openapi\.yaml$"), self.openapi_yaml),
            ("GET", re.compile(r"^/openapi\.json$"), self.openapi_json),
            ("GET", re.compile(r"^/fields$"), self.fields),
            ("GET", re.compile(r"^/rules/(?P<rule_id>[^/]+)$"), self.rule),
            ("POST", re.compile(r"^/projects$"), self.create_project),
            ("GET", re.compile(r"^/projects/(?P<pid>[^/]+)$"), self.get_project),
            ("PATCH", re.compile(r"^/projects/(?P<pid>[^/]+)/fields$"), self.set_fields),
            ("POST", re.compile(r"^/projects/(?P<pid>[^/]+)/validate$"), self.validate),
            ("POST", re.compile(r"^/projects/(?P<pid>[^/]+)/build$"), self.build),
        ]

    # ------------------------------------------------------------------ WSGI
    def __call__(self, environ: dict, start_response: Callable):
        method = environ.get("REQUEST_METHOD", "GET").upper()
        path = environ.get("PATH_INFO", "/") or "/"
        query = parse_qs(environ.get("QUERY_STRING", ""), keep_blank_values=True)
        try:
            handler, params, allowed = None, {}, []
            for m, rx, fn in self.routes:
                match = rx.match(path)
                if match:
                    allowed.append(m)
                    if m == method:
                        handler, params = fn, match.groupdict()
                        break
            if handler is None:
                if allowed:
                    raise HTTPError(405, f"method {method} not allowed on {path}; use {', '.join(allowed)}")
                raise HTTPError(404, f"no endpoint {path}")
            body = self._read_body(environ) if method in ("POST", "PATCH") else None
            status, ctype, payload = handler(body=body, query=query, **params)
        except HTTPError as e:
            status, ctype, payload = e.status, "application/json", {"error": e.message}
        except Exception as e:  # never leak a traceback to the caller
            status, ctype, payload = 500, "application/json", {"error": f"internal error: {type(e).__name__}"}
        if ctype == "application/json":
            data = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
            ctype = "application/json; charset=utf-8"
        else:
            data = payload.encode("utf-8") if isinstance(payload, str) else payload
            ctype = f"{ctype}; charset=utf-8"
        start_response(f"{status} {_REASONS.get(status, '')}".strip(),
                       [("Content-Type", ctype), ("Content-Length", str(len(data))),
                        ("Cache-Control", "no-store")])
        return [data]

    @staticmethod
    def _read_body(environ: dict) -> Any:
        try:
            length = int(environ.get("CONTENT_LENGTH") or 0)
        except ValueError:
            raise HTTPError(400, "bad Content-Length") from None
        if length > MAX_BODY_BYTES:
            raise HTTPError(413, f"body larger than {MAX_BODY_BYTES} bytes")
        raw = environ["wsgi.input"].read(length) if length else b""
        if not raw.strip():
            return {}
        try:
            return json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise HTTPError(400, "body must be JSON (UTF-8)") from None

    # --------------------------------------------------------------- helpers
    def _project_file(self, pid: str, must_exist: bool = True) -> Path:
        if not ID_RE.match(pid):
            raise HTTPError(400, "project id must match ^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")
        path = self.workdir / pid / "project.yaml"
        if must_exist and not path.is_file():
            raise HTTPError(404, f"no project {pid!r}")
        return path

    @staticmethod
    def _obj(body: Any, allowed: set[str], what: str) -> dict:
        if not isinstance(body, dict):
            raise HTTPError(400, f"{what} must be a JSON object")
        extra = sorted(set(body) - allowed)
        if extra:
            raise HTTPError(400, f"unknown key(s) in {what}: {', '.join(extra)}")
        return body

    @staticmethod
    def _set_kwargs(u: dict, i: int) -> dict:
        """Every write over HTTP is recorded as AI-assisted, like MCP: the
        caller is an assistant acting for the researcher. The AI's own
        wording is authored_by ai_draft / INFERENCE; a value the researcher
        gave word for word (researcher_verbatim: true) is human_ai_assisted /
        DECISION. SOURCE is refused by the engine for every AI-assisted
        write, and authored_by cannot be chosen by the caller."""
        actor = u.get("actor")
        if actor is not None and actor != "ai_assisted":
            raise HTTPError(400, f"update {i}: actor must be ai_assisted (every HTTP write is AI-assisted; "
                                 "use researcher_verbatim: true for the researcher's own words)")
        verbatim = u.get("researcher_verbatim", False)
        if not isinstance(verbatim, bool):
            raise HTTPError(400, f"update {i}: researcher_verbatim must be true or false")
        prov = ({"provenance_class": "DECISION", "authored_by": "human_ai_assisted"} if verbatim
                else {"provenance_class": "INFERENCE", "authored_by": "ai_draft"})
        extra_prov = u.get("provenance")
        if extra_prov is not None:
            if not isinstance(extra_prov, dict):
                raise HTTPError(400, f"update {i}: provenance must be an object")
            bad = sorted(set(extra_prov) - PROVENANCE_KEYS)
            if bad:
                raise HTTPError(400, f"update {i}: provenance may only set {', '.join(sorted(PROVENANCE_KEYS))} "
                                     f"(refused: {', '.join(bad)})")
            prov.update(extra_prov)
        if u.get("tool") is not None and not isinstance(u["tool"], str):
            raise HTTPError(400, f"update {i}: tool must be a string")
        kwargs: dict = {"actor": "ai_assisted", "provenance": prov,
                        "tool": u.get("tool") or DEFAULT_TOOL_NAME}
        for k in ("chain_node", "source_ids", "links"):
            if u.get(k) is not None:
                kwargs[k] = u[k]
        return kwargs

    # -------------------------------------------------------------- handlers
    def health(self, **_):
        return 200, "application/json", {"status": "ok", "service": "grantthai-api",
                                         "can_submit": False, "max_status": "DRAFT"}

    def openapi_yaml(self, **_):
        return 200, "application/yaml", _openapi_path().read_text(encoding="utf-8")

    def openapi_json(self, **_):
        return 200, "application/json", yaml.safe_load(_openapi_path().read_text(encoding="utf-8"))

    def fields(self, query: dict, **_):
        tab = (query.get("tab") or [None])[0] or None
        req = (query.get("required") or ["false"])[0].lower() in ("1", "true", "yes")
        return 200, "application/json", {"fields": api_py.list_fields(tab=tab, required_only=req)}

    def rule(self, rule_id: str, **_):
        try:
            return 200, "application/json", api_py.explain(rule_id)
        except KeyError:
            raise HTTPError(404, f"unknown rule id {rule_id!r}") from None

    def create_project(self, body: Any, **_):
        body = self._obj(body, CREATE_KEYS, "request body")
        project_id = body.get("project_id")
        if project_id is not None and (not isinstance(project_id, str) or not ID_RE.match(project_id)):
            raise HTTPError(400, "project_id must match ^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")
        pid = project_id or f"p-{secrets.token_hex(6)}"
        path = self._project_file(pid, must_exist=False)
        if path.exists():
            raise HTTPError(409, f"project {pid!r} already exists")
        kwargs: dict = {"project_id": project_id or "NEEDS_INPUT", "path": path}
        for key in ("fund_profile_id", "mode"):
            if body.get(key) is not None:
                if not isinstance(body[key], str):
                    raise HTTPError(400, f"{key} must be a string")
                kwargs[key] = body[key]
        if kwargs.get("mode", "expert") not in ("expert", "human_direct", "citizen"):
            raise HTTPError(400, "mode must be expert, human_direct or citizen")
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            doc = api_py.new_project(**kwargs)
        except FileExistsError:
            raise HTTPError(409, f"project {pid!r} already exists") from None
        return 201, "application/json", {"id": pid, "project": doc}

    def get_project(self, pid: str, **_):
        return 200, "application/json", {"id": pid, "project": api_py.load(self._project_file(pid))}

    def set_fields(self, pid: str, body: Any, **_):
        path = self._project_file(pid)
        if isinstance(body, dict) and "updates" in body:
            self._obj(body, {"updates"}, "request body")
            updates = body["updates"]
        else:
            updates = [body]
        if not isinstance(updates, list) or not updates:
            raise HTTPError(400, "updates must be a non-empty list")
        doc = api_py.load(path)
        written = []
        for i, u in enumerate(updates):
            u = self._obj(u, SET_KEYS, f"update {i}")
            if "field_id" not in u or "value" not in u:
                raise HTTPError(400, f"update {i}: field_id and value are required")
            kwargs = self._set_kwargs(u, i)
            try:
                rec = api_py.set_field(doc, u["field_id"], u["value"], save=False, **kwargs)
            except (ValueError, TypeError) as e:
                # all-or-nothing: nothing is written when one update is refused
                raise HTTPError(400, f"update {i} ({u.get('field_id')}): {e}") from None
            written.append(json.loads(json.dumps(rec, default=str)))
        api_py.save(doc, path)
        return 200, "application/json", {"id": pid, "written": written,
                                         "note": "stored as AI-assisted DRAFT (or NEEDS_INPUT); the researcher confirms them"}

    def validate(self, pid: str, body: Any, **_):
        body = self._obj(body, {"as_of"}, "request body")
        report = api_py.validate(self._project_file(pid), as_of=_check_as_of(body.get("as_of")))
        return 200, "application/json", report

    def build(self, pid: str, body: Any, query: dict, **_):
        body = self._obj(body, {"as_of"}, "request body")
        as_of = _check_as_of(body.get("as_of"))
        out = api_py.build(self._project_file(pid), as_of=as_of)
        text = out.read_text(encoding="utf-8")
        fmt = (query.get("format") or ["markdown"])[0]
        if fmt == "json":
            report = api_py.validate(self._project_file(pid), as_of=as_of)
            return 200, "application/json", {
                "id": pid, "filename": "NRIIS_SUBMISSION.md", "markdown": text,
                "summary": report.get("summary"),
            }
        if fmt != "markdown":
            raise HTTPError(400, "format must be markdown or json")
        return 200, "text/markdown", text


def make_app(workdir: str | Path = "grantthai-work") -> GrantThaiAPI:
    return GrantThaiAPI(workdir)
