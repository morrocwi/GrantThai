# GrantThai HTTP API

A small HTTP API that lets a researcher's AI assistant fill in the
researcher's work file (`work.yaml` 0.3, or a legacy `project.yaml`) and
build exactly one overview file per output route: `build/NRIIS_SUBMISSION.md`
(route `nriis-proposal`), `build/ACADEMIC_ARTICLE.md` (route
`academic-article`) or `build/RESEARCH_CONCEPT_NOTE.md` (route
`concept-note`). Since v0.3 NRIIS is one route of the router, not the core.
It works with any vendor's assistant, or none.

The API adds no rules of its own. Each endpoint calls one function of
the Python API (`grantthai.api_py`), which is also what the CLI, the skill
and the MCP server use. The OpenAPI 3.1 description is
[`spec/api/openapi.yaml`](../spec/api/openapi.yaml).

## Start it

It needs the standard library only, plus the engine's own dependencies.

```sh
pip install -e .                      # from a GrantThai checkout
grantthai-api                         # http://127.0.0.1:8765, data in ./grantthai-work
grantthai-api --port 9000 --workdir ~/my-grant   # or: python -m grantthai.api ...
```

- **Local by default.** It binds `127.0.0.1`. It has no authentication,
  so binding any other address needs `--allow-remote`, and you should only
  do that behind your own authenticating proxy.
- **Where data lives.** The working directory holds one folder per
  project, each with its work file (`work.yaml`, or a legacy
  `project.yaml`; never both) and `build/<route output file>`. Nothing
  else is stored, and no credentials are kept.
- **Where the engine finds its data.** The engine reads `spec/`,
  `registry/` and `templates/` from the checkout, or from the folder
  named in `GRANTTHAI_HOME`.

## Endpoints

| Method | Path | What it does | Wraps |
|---|---|---|---|
| GET | `/health` | Liveness check | – |
| GET | `/openapi.yaml`, `/openapi.json` | This API's description | – |
| GET | `/fields?tab=&required=true&route=` | The fields of one route: NRIIS boxes in entry order, then `NOT_ON_TAB` fields (default); another route's placement order, then `NOT_PLACED` | `list_fields` |
| GET | `/routes` | Every output route; the list never chooses | `list_routes` |
| GET | `/rules/{rule_id}` | Explain one validator rule | `explain` |
| POST | `/projects` | Create a blank work file: `work.yaml` with `work_type`, else a legacy `project.yaml`; no route is written | `new_work` / `new_project` |
| GET | `/projects/{id}` | Read the work file as JSON | `load` |
| PATCH | `/projects/{id}/fields` | Set one or more fields | `set_field` |
| POST | `/projects/{id}/validate` | Get the validation report for one route; changes nothing | `validate` |
| POST | `/projects/{id}/routes/{route}/check` | The report for an explicitly named route; changes nothing | `check_route` |
| POST | `/projects/{id}/build` | Write and return the chosen route's one file | `build` |

`build` returns the Markdown text by default. Add `?format=json` to get
`{id, route, filename, markdown, summary}` instead. `validate` and
`build` take an optional body `{"as_of": "YYYY-MM-DD", "route": "...",
"sub_profile": "..."}`; `check` takes `{as_of, sub_profile}`. The same
input, route and `as_of` give byte-identical output. Leave `as_of` out and
the engine uses today's date, so the fund-rule freshness check (F002) can
change from one day to the next.

### The route is the researcher's choice

With no `route` in the body, the server resolves it only from what a
person declared: `routing.default_route` in `work.yaml`, `nriis-proposal`
for a legacy `project.yaml`, or the one route that is the default for the
file's `work_type`. When none of these decides, `validate` and `build`
answer **409** and write nothing:

```json
{"error": "no route chosen for W-1 (work_type final_report): choose one with --route (...) or set routing.default_route; GrantThai never picks a route",
 "candidates": ["nriis-proposal", "academic-article", "concept-note"]}
```

The assistant shows the candidates, asks the researcher, and repeats the
call with `"route"`. The server never picks. An unknown route is 404. A
legacy `project.yaml` with no route keeps the v0.1 behaviour
(`NRIIS_SUBMISSION.md`), so existing clients are unaffected. `POST /projects`
returns `default_route` (or `candidates`) so the assistant knows up front
whether it has to ask.

## Rules the engine enforces for every caller

- **The researcher's own information is the source.** A value written
  through the API ends at `DRAFT`, or at `NEEDS_INPUT` when it is cleared.
  No endpoint raises a status higher than that, and a `status` key in a
  request is refused. Nothing is ever submitted to NRIIS.
- **Every write is an AI-assisted draft.** The API assumes the caller is
  an assistant acting for the researcher, so every value is recorded as
  AI-assisted and the output lists it under the values the researcher must
  confirm. The assistant's own wording is stored as
  `authored_by: ai_draft` and `INFERENCE`. When the value is the
  researcher's own words, unchanged, send `"researcher_verbatim": true`;
  it is stored as `authored_by: human_ai_assisted` and `DECISION`. Name the
  assistant in `"tool"` (default `http-client`). `"actor": "human"`, a
  `provenance_class` of `SOURCE`, and any `authored_by` in a request are
  refused with a 400. A researcher who wants a value recorded as their own
  (or as `SOURCE`) sets it with the `grantthai` CLI or edits
  `project.yaml` directly.
- **The AI-use ceiling applies** (`docs/policy/ai-use-ceiling.md`).
  `POST /projects` returns `data_warning` (`th` and `en`): show it to the
  researcher before accepting any data (personal data that identifies
  anyone, participants' records, confidential, unpublished or pre-patent
  material and dual-use information must not go into a public AI; GenAI
  guideline 2569 p.14-16). Every field write records the tool in
  `authoring.ai_use_declaration.tools` with `"tool"`, `"tool_version"`
  (omitted: `NEEDS_INPUT`) and `"stage"` (default `proposal_writing`; one of
  `idea`, `proposal_writing`, `literature`, `data`, `analysis`, `writing`,
  `language_editing`, `review`, `publication`). A new tool or stage resets
  `declaration_confirmed_by_human` to false; no request can set it. The
  researcher confirms the declaration in `project.yaml` after reading output
  section 4.7 (a GrantThai appendix, not an NRIIS field). Rules AI001-AI004
  (REVIEW) report what is missing.
- **No invented facts.** Do not make up Thai fund, NRIIS, institution or
  journal facts (scope, indexing, word limits, fees, review time). Send
  `"NEEDS_VERIFICATION"` instead; it is stored as an empty value plus that
  marker.
- **Batches are all-or-nothing.** In `{"updates": [...]}`, if any update
  is refused, nothing is written.
- **Validate and check are report-only.** They never change the work file.
- **No route is ever chosen by the server** (see above).

## Example

```sh
curl -s -X POST 127.0.0.1:8765/projects -H 'content-type: application/json' \
     -d '{"project_id":"my-grant"}'
curl -s '127.0.0.1:8765/fields?required=true'
curl -s -X PATCH 127.0.0.1:8765/projects/my-grant/fields -H 'content-type: application/json' \
     -d '{"updates":[{"field_id":"<FIELD_ID>","value":"<researcher words>","researcher_verbatim":true,"tool":"<assistant>","tool_version":"<version>"},
                     {"field_id":"<FIELD_ID>","value":"<AI draft>","tool":"<assistant>"}]}'
curl -s -X POST 127.0.0.1:8765/projects/my-grant/validate -d '{"as_of":"2026-09-25"}'
curl -s -X POST 127.0.0.1:8765/projects/my-grant/build    -d '{"as_of":"2026-09-25"}' > NRIIS_SUBMISSION.md
```

One example per route (the researcher chose the route in each case):

```sh
# research proposal (NRIIS route): a legacy project.yaml, or work_type research_proposal
curl -s -X POST 127.0.0.1:8765/projects -H 'content-type: application/json' -d '{"project_id":"p1"}'
curl -s -X POST 127.0.0.1:8765/projects/p1/build -d '{"as_of":"2026-09-25","route":"nriis-proposal"}' > NRIIS_SUBMISSION.md

# academic article: work.yaml, no fund binding, ARTICLE.* fields from the researcher's own results
curl -s -X POST 127.0.0.1:8765/projects -H 'content-type: application/json' \
     -d '{"project_id":"a1","work_type":"academic_article"}'
curl -s '127.0.0.1:8765/fields?route=academic-article&required=true'
curl -s -X POST 127.0.0.1:8765/projects/a1/routes/academic-article/check -d '{"as_of":"2026-09-25","sub_profile":"thai-journal"}'
curl -s -X POST 127.0.0.1:8765/projects/a1/build -d '{"as_of":"2026-09-25","route":"academic-article"}' > ACADEMIC_ARTICLE.md

# concept note: never submittable (always a HOLD)
curl -s -X POST 127.0.0.1:8765/projects -H 'content-type: application/json' \
     -d '{"project_id":"c1","work_type":"concept_note"}'
curl -s -X POST 127.0.0.1:8765/projects/c1/build -d '{"as_of":"2026-09-25","route":"concept-note"}' > RESEARCH_CONCEPT_NOTE.md
```

`manuscript_ready` in `ACADEMIC_ARTICLE.md` means "no BLOCK finding is
open"; it never means accepted or publishable, and every journal fact in
it is `NEEDS_VERIFICATION` unless the researcher supplied the venue's own
document.

## Using it from an AI assistant

- **Assistants that import OpenAPI** (custom GPT Actions and similar):
  import `spec/api/openapi.yaml`, or `GET /openapi.json`, and change
  `servers[0].url` to an HTTPS address you control. A cloud-hosted
  assistant cannot reach `127.0.0.1`. To expose the API, put it behind
  your own authenticating HTTPS proxy and start it with `--allow-remote`.
- **Local assistants and scripts:** call the endpoints directly, or skip
  HTTP and use `grantthai.api_py`, the CLI, or the MCP server.

## Limits

- **Console script.** `grantthai-api` (installed with the package) is
  the same as `python -m grantthai.api`.
- **Standard library only.** It uses `wsgiref`, with no FastAPI or
  uvicorn. It is meant for one person on one machine, not for serving
  many users.
- **No way to upload a whole file.** You cannot send a full work file,
  which keeps the status ceiling from being bypassed. To work on an
  existing file, copy it to `<workdir>/<id>/work.yaml` (or
  `project.yaml`; never both).
- **No `migrate` and no `routing` writes.** Declaring `routing.default_route`
  in `work.yaml`, or upgrading a `project.yaml`, is done by a person at the
  terminal; over HTTP the route is named per request.
