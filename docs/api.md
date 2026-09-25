# GrantThai HTTP API

A small HTTP API that lets a researcher's AI assistant fill in the
researcher's `project.yaml` and build the one overview file,
`build/NRIIS_SUBMISSION.md`. It works with any vendor's assistant, or none.

The API adds no rules of its own. Each endpoint calls one function of
the Python API (`grantthai.api_py`), which is also what the CLI, the skill
and the MCP server use. The OpenAPI 3.1 description is
[`spec/api/openapi.yaml`](../spec/api/openapi.yaml).

## Start it

It needs the standard library only, plus the engine's own dependencies.

```sh
pip install -e .                      # from a GrantThai checkout
python -m grantthai.api               # http://127.0.0.1:8765, data in ./grantthai-work
python -m grantthai.api --port 9000 --workdir ~/my-grant
```

- **Local by default.** It binds `127.0.0.1`. It has no authentication,
  so binding any other address needs `--allow-remote`, and you should only
  do that behind your own authenticating proxy.
- **Where data lives.** The working directory holds one folder per
  project, each with `project.yaml` and `build/NRIIS_SUBMISSION.md`.
  Nothing else is stored, and no credentials are kept.
- **Where the engine finds its data.** The engine reads `spec/`,
  `registry/` and `templates/` from the checkout, or from the folder
  named in `GRANTTHAI_HOME`.

## Endpoints

| Method | Path | What it does | Wraps |
|---|---|---|---|
| GET | `/health` | Liveness check | – |
| GET | `/openapi.yaml`, `/openapi.json` | This API's description | – |
| GET | `/fields?tab=&required=true` | Fields in NRIIS entry order | `list_fields` |
| GET | `/rules/{rule_id}` | Explain one validator rule | `explain` |
| POST | `/projects` | Create a blank `project.yaml` | `new_project` |
| GET | `/projects/{id}` | Read `project.yaml` as JSON | `load` |
| PATCH | `/projects/{id}/fields` | Set one or more fields | `set_field` |
| POST | `/projects/{id}/validate` | Get the validation report; changes nothing | `validate` |
| POST | `/projects/{id}/build` | Write and return `NRIIS_SUBMISSION.md` | `build` |

`build` returns the Markdown text by default. Add `?format=json` to get
`{id, filename, markdown, summary}` instead. Both `validate` and `build`
take an optional body `{"as_of": "YYYY-MM-DD"}`. The same input with the
same `as_of` gives byte-identical output. Leave `as_of` out and the
engine uses today's date, so the fund-rule freshness check (F002) can
change from one day to the next.

## Rules the engine enforces for every caller

- **The researcher's own information is the source.** A value written
  through the API ends at `DRAFT`, or at `NEEDS_INPUT` when it is cleared.
  No endpoint raises a status higher than that, and a `status` key in a
  request is refused. Nothing is ever submitted to NRIIS.
- **AI drafts are labelled.** An AI assistant must send
  `"actor": "ai_assisted"`, and may name itself in `"tool"`. Its value is
  stored as `authored_by: ai_draft` and `INFERENCE`, and the output lists
  it under the AI-drafted values the researcher must confirm. Asking for
  `provenance_class: SOURCE` on an AI draft is refused with a 400.
- **No invented facts.** Do not make up Thai fund, NRIIS or institution
  facts. Send `"NEEDS_VERIFICATION"` instead; it is stored as an empty
  value plus that marker.
- **Batches are all-or-nothing.** In `{"updates": [...]}`, if any update
  is refused, nothing is written.
- **Validate is report-only.** It never changes `project.yaml`.

## Example

```sh
curl -s -X POST 127.0.0.1:8765/projects -H 'content-type: application/json' \
     -d '{"project_id":"my-grant"}'
curl -s '127.0.0.1:8765/fields?required=true'
curl -s -X PATCH 127.0.0.1:8765/projects/my-grant/fields -H 'content-type: application/json' \
     -d '{"updates":[{"field_id":"<FIELD_ID>","value":"<researcher text>"},
                     {"field_id":"<FIELD_ID>","value":"<AI draft>","actor":"ai_assisted","tool":"<assistant>"}]}'
curl -s -X POST 127.0.0.1:8765/projects/my-grant/validate -d '{"as_of":"2026-09-25"}'
curl -s -X POST 127.0.0.1:8765/projects/my-grant/build    -d '{"as_of":"2026-09-25"}' > NRIIS_SUBMISSION.md
```

## Using it from an AI assistant

- **Assistants that import OpenAPI** (custom GPT Actions and similar):
  import `spec/api/openapi.yaml`, or `GET /openapi.json`, and change
  `servers[0].url` to an HTTPS address you control. A cloud-hosted
  assistant cannot reach `127.0.0.1`. To expose the API, put it behind
  your own authenticating HTTPS proxy and start it with `--allow-remote`.
- **Local assistants and scripts:** call the endpoints directly, or skip
  HTTP and use `grantthai.api_py`, the CLI, or the MCP server.

## Limits in v0.1

- **No packaged console script.** There is no `grantthai-api` command
  yet, so run the server with `python -m grantthai.api`. Adding one needs
  a change to `pyproject.toml`, which is outside this surface.
- **Standard library only.** It uses `wsgiref`, with no FastAPI or
  uvicorn. It is meant for one person on one machine, not for serving
  many users.
- **No way to upload a whole file.** You cannot send a full
  `project.yaml`, which keeps the status ceiling from being bypassed. To
  work on an existing file, copy it to `<workdir>/<id>/project.yaml`.
