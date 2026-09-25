# GrantThai MCP server

GrantThai ships an MCP server so a researcher's AI assistant can turn one
work object (`work.yaml`, or a legacy `project.yaml`) into exactly one
overview file per output route: `build/NRIIS_SUBMISSION.md` (route
`nriis-proposal`), `build/ACADEMIC_ARTICLE.md` (route `academic-article`)
or `build/RESEARCH_CONCEPT_NOTE.md` (route `concept-note`). Since v0.3
NRIIS is one route of the router, not the core. Any client that speaks MCP
over stdio can use it: desktop chat apps, coding agents, IDE assistants,
or a local model runner.

The server is a thin wrapper over `grantthai.api_py`. Those are the same
functions the `grantthai` CLI calls, so the checks and the output are the
same. It does not call a model or the network, and it does not submit
anything to NRIIS or to any fund.

## What stays true over MCP

- **The researcher's own information is the source.** The AI drafts and the
  researcher confirms.
- **Every value written through `grantthai_set_field` is an AI-assisted
  draft at status `DRAFT`.** A cleared value is `NEEDS_INPUT`. No tool can
  set a higher status. A status cannot even be passed as an argument.
- **The AI's own wording is stored as `authored_by: ai_draft` with
  `provenance_class: INFERENCE`.** If the researcher gave the value word for
  word, the AI passes `researcher_verbatim: true`. The value is then stored
  as `authored_by: human_ai_assisted` with `provenance_class: DECISION`.
  `SOURCE` is never available over MCP.
- **The output lists every AI-assisted value** under "AI-drafted values (the
  researcher must confirm)". The client's name is recorded as a disclosed
  tool.
- **The AI-use ceiling applies** (`docs/policy/ai-use-ceiling.md`). Every
  `grantthai_set_field` call records the tool in
  `authoring.ai_use_declaration.tools`: the `tool` argument or the client's
  name from `initialize`, the `tool_version` argument or the client's
  declared version, and the `stage` argument (default `proposal_writing`).
  A new tool or stage resets `declaration_confirmed_by_human` to false. No
  MCP call can set that flag: only the researcher sets it, in
  `project.yaml`, after reading output section 4.7 (the AI Use Declaration,
  a GrantThai appendix, not an NRIIS field). Rules AI001-AI004 (REVIEW)
  report a missing or unconfirmed declaration, AI-drafted evidence,
  personal-data-shaped strings in AI-assisted values, and a self-assessed
  risk of 3.
- **Show the data warning before accepting any data.**
  `grantthai_new_project` returns `data_warning` (`th` and `en`), and the
  server instructions repeat it: personal data that identifies anyone,
  participants' records, confidential, unpublished or pre-patent material
  and dual-use information must not go into a public AI (GenAI guideline
  2569 p.14-16). Show it to the researcher before asking for any data.
- **The AI must not invent a Thai fund, NRIIS, institutional or journal
  fact.** If one is not in the researcher's own material, the AI writes the
  literal value `NEEDS_VERIFICATION`. It is stored as a marker, not as text.
- **`grantthai_validate` and `grantthai_check_route` only report.** They
  never change the work file. Their findings are about form and
  consistency. They are not a verdict on the research.
- **`grantthai_build` writes exactly one file** (the chosen route's) and
  returns its content. Building a second route leaves the first route's
  file byte-identical.
- **The route is the researcher's choice, never the server's.** With no
  `route` argument the server resolves it only from what a person declared
  (`routing.default_route` in `work.yaml`, a legacy `project.yaml`, or the
  one route that is the default for the file's `work_type`). When none of
  these decides, `grantthai_build` and `grantthai_validate` return
  `candidates` and build nothing; the assistant shows the list, asks the
  researcher, and calls again with `route`. The server never defaults the
  route. (This is the v0.3 "router": a deterministic output route chosen by
  a person, not an AI routing anything.)
- **Every path is resolved inside one root folder.** The root is `--root`,
  or the server's working folder by default. A path outside that folder is
  refused.

## Install

```bash
pip install -e ".[mcp]"      # from a GrantThai checkout; adds the official MCP SDK
# or, with no extra dependency (built-in JSON-RPC stdio transport):
pip install -e .
```

In v0.1 the data files (`spec/`, `registry/`, `templates/`, `validators/`
and the others) are read from the source checkout. If you run the server
from somewhere else, set `GRANTTHAI_HOME` to the checkout folder.

Run the server:

```bash
grantthai-mcp --root /path/to/my-proposal            # the SDK transport if installed, else built-in
python -m grantthai.mcp --root /path/to/my-proposal --transport builtin
```

`--transport auto` is the default. It uses the official `mcp` SDK when a
1.x release is installed and the built-in stdio loop otherwise (the 2.x SDK
changed the server API this transport uses, so the extra pins `mcp<2`). Both serve the same
tools. stdout carries protocol messages only.

## Tools

| Tool | Wraps | Effect |
|---|---|---|
| `grantthai_new_project` | `grantthai init` | Writes a blank work file with every required field `NEEDS_INPUT`: a `work.yaml` (schema 0.3) when `work_type` is given, else a legacy `project.yaml` (0.2). It writes no route, refuses to overwrite an existing file and refuses a second canonical input in the same folder. The result says which route a build would use (`default_route`) or lists `candidates`. |
| `grantthai_list_routes` | `grantthai route list` | Lists every output route: id, title, status, output filename, accepted and default work types, fund-binding need, ready flag. The list never chooses. |
| `grantthai_list_fields` | `grantthai fields` | Lists the fields of one route (optional `route`). Without it: NRIIS boxes in entry order, then fields with tab `NOT_ON_TAB`; for another route its placement order, then `NOT_PLACED` (id, tab, origin, type, required, English label, guidance). Thai labels are `NEEDS_VERIFICATION`. |
| `grantthai_set_field` | `grantthai set` | Writes one value as an AI-assisted `DRAFT`. Takes `field_id`, `value`, `researcher_verbatim`, `chain_node`, `source_ids`, `links`, `tool`, `tool_version` and `stage`, and records the tool in `authoring.ai_use_declaration.tools`. |
| `grantthai_validate` | `grantthai validate` | Returns the validation report of BLOCK, REVIEW and INFO findings for one route (optional `route`, `sub_profile`). Report-only. Ambiguous route: `candidates`, no report. |
| `grantthai_check_route` | `grantthai route check` | The report for an explicitly named `route` (required). Only that route's rules run; RT002 counts the rest in one INFO line. Report-only. |
| `grantthai_explain` | `grantthai explain` | Explains one rule id, such as `S001`, `B002`, `ART007`, `RT002` or `SCHEMA`. |
| `grantthai_build` | `grantthai build` | Writes `build/<route output filename>` and returns `path`, `route`, `filename`, `summary` and `markdown`. It always renders, even when there are BLOCK findings, and lists them in the file. Ambiguous route: `candidates`, nothing written. |

`project_path` defaults to the root folder, where `work.yaml` is found
first, then `project.yaml` (both present is refused). `as_of` (YYYY-MM-DD)
fixes the date used for fund-rule staleness checks. Two builds of the same
input, route and `as_of` date are byte-identical.

### The ambiguity result

A `work.yaml` with `work_type: final_report` and no `routing.default_route`
has no single default route. `grantthai_build` with no `route` then returns,
and writes nothing:

```json
{
  "project_path": "work.yaml",
  "route": null,
  "candidates": ["nriis-proposal", "academic-article", "concept-note"],
  "path": null,
  "note": "No output route could be resolved from the researcher's own declaration. Show the researcher `candidates` ... GrantThai never picks a route."
}
```

The assistant shows the candidates, asks, and calls `grantthai_build`
again with `route`. A legacy `project.yaml` never hits this: it is always
`nriis-proposal`, so v0.1 clients keep working unchanged.

### One example per route

- **NRIIS proposal** (unchanged from v0.1): `grantthai_new_project`
  (no `work_type`, or `work_type: research_proposal`), fill fields,
  `grantthai_build` with `route: nriis-proposal` or none. Output
  `build/NRIIS_SUBMISSION.md`, ready flag `submittable` against the
  FICTIONAL fund profile only.
- **Academic article**: `grantthai_new_project` with
  `work_type: academic_article` (writes `work.yaml`, no fund binding),
  `grantthai_list_fields` with `route: academic-article`, fill the
  ARTICLE.* fields from the researcher's own results (every journal fact
  `NEEDS_VERIFICATION` unless they supply the venue's document),
  `grantthai_check_route` with `route: academic-article` and optionally
  `sub_profile: thai-journal`, then `grantthai_build` with
  `route: academic-article`. Output `build/ACADEMIC_ARTICLE.md`; its
  `manuscript_ready` flag means "no BLOCK open", never accepted or
  publishable. ART007 (an AI tool listed as an author) is the one BLOCK.
- **Concept note**: `work_type: concept_note`, then `grantthai_build` with
  `route: concept-note`. Output `build/RESEARCH_CONCEPT_NOTE.md`, always a
  HOLD: a concept note enters no system.

The machine-readable contract is `spec/mcp/tools.schema.json`. Its
`examples` entry is the implemented tool list, and `tests/mcp` checks the
server against it.

## Resources

| URI | Content |
|---|---|
| `grantthai://notice` | The independence notice printed on line 1 of every output body. |
| `grantthai://fields` | The field registry as JSON, the same data `grantthai_list_fields` returns. |
| `grantthai://routes` | Every output route as JSON, the same data `grantthai_list_routes` returns. |

## Typical flow

1. `grantthai_list_routes`; show the routes and ask the researcher which
   output they want. Never choose for them.
2. `grantthai_new_project` (with `work_type` for a `work.yaml`), or skip
   this step if the researcher already has a work file. Show the
   researcher `data_warning` before asking for any data.
3. `grantthai_list_fields` with `required_only: true` and the chosen
   `route`.
4. Ask the researcher for each value. Record each one with
   `grantthai_set_field`: set `researcher_verbatim: true` when you pass on
   the researcher's own words, and use `NEEDS_VERIFICATION` for any fund,
   NRIIS, institutional or journal fact that is not in their material.
5. Run `grantthai_check_route` (or `grantthai_validate` with `route`), and
   use `grantthai_explain` on any finding.
6. Run `grantthai_build` with `route`, then give the researcher the path
   and ask them to check every AI-drafted value and the AI Use Declaration
   (section 4.7), fill in what it still lacks, and confirm it themselves.
   If they want a second route from the same file, build it separately.

## Client configuration

Replace `/path/to/GrantThai` with your checkout and `/path/to/my-proposal`
with the folder that holds (or will hold) `project.yaml`. If `grantthai-mcp`
is not on the client's `PATH`, use the full path to the Python interpreter
of the environment you installed into, with `"args": ["-m",
"grantthai.mcp", ...]`.

### Claude Desktop (`claude_desktop_config.json`)

```json
{
  "mcpServers": {
    "grantthai": {
      "command": "grantthai-mcp",
      "args": ["--root", "/path/to/my-proposal"],
      "env": { "GRANTTHAI_HOME": "/path/to/GrantThai" }
    }
  }
}
```

### Claude Code (project `.mcp.json`, in the proposal folder)

```json
{
  "mcpServers": {
    "grantthai": {
      "type": "stdio",
      "command": "grantthai-mcp",
      "args": ["--root", "."],
      "env": { "GRANTTHAI_HOME": "/path/to/GrantThai" }
    }
  }
}
```

Or from a shell: `claude mcp add grantthai -e GRANTTHAI_HOME=/path/to/GrantThai -- grantthai-mcp --root .`

### Codex CLI (`~/.codex/config.toml`)

```toml
[mcp_servers.grantthai]
command = "grantthai-mcp"
args = ["--root", "/path/to/my-proposal"]
env = { GRANTTHAI_HOME = "/path/to/GrantThai" }
```

### Gemini CLI (`~/.gemini/settings.json` or `.gemini/settings.json`)

```json
{
  "mcpServers": {
    "grantthai": {
      "command": "grantthai-mcp",
      "args": ["--root", "/path/to/my-proposal"],
      "env": { "GRANTTHAI_HOME": "/path/to/GrantThai" }
    }
  }
}
```

### VS Code (`.vscode/mcp.json`)

```json
{
  "servers": {
    "grantthai": {
      "type": "stdio",
      "command": "grantthai-mcp",
      "args": ["--root", "${workspaceFolder}"],
      "env": { "GRANTTHAI_HOME": "/path/to/GrantThai" }
    }
  }
}
```

### Other clients, including local-model runners

Any MCP client that can start a stdio server works. Point it at the command
`grantthai-mcp --root <folder>`, or at `python -m grantthai.mcp --root
<folder>`. If the client has no MCP support, the same functions are
available from the `grantthai` CLI and from `grantthai.api_py`.

## Not over MCP

- No review, lock or status promotion, over MCP or anywhere else.
- No submission to NRIIS, to any fund or to any journal.
- No route choice: the server never picks between routes.
- No `migrate`: upgrading a `project.yaml` to `work.yaml` changes the
  content hash and is a person's decision at the terminal.
- No HTTP transport. The HTTP API is a separate surface.
