"""grantthai.api — a small, local-first HTTP API over grantthai.api_py.

Optional surface. The AI-free core packages never import it. It adds no
behaviour of its own: every endpoint calls one function of the Python API
(grantthai.api_py), so the hard ceiling of the core applies unchanged:

* a field written through the API ends at DRAFT (or NEEDS_INPUT when
  cleared); nothing here raises a status above DRAFT;
* an AI-drafted value (actor "ai_assisted") is stored as authored_by
  ai_draft / INFERENCE and can never be provenance_class SOURCE;
* validate is report-only and persists nothing;
* nothing is ever submitted to NRIIS.

Standard library only (wsgiref), so it runs wherever the engine runs.
Binds 127.0.0.1 by default. It stores no credentials and keeps no data
outside its working directory (one folder per project, holding
project.yaml and build/NRIIS_SUBMISSION.md).

    python -m grantthai.api [--host 127.0.0.1] [--port 8765] [--workdir DIR]

The OpenAPI 3.1 description is spec/api/openapi.yaml, also served at
GET /openapi.yaml and GET /openapi.json.
"""
from grantthai.api.app import GrantThaiAPI, make_app  # noqa: F401

__all__ = ["GrantThaiAPI", "make_app"]
