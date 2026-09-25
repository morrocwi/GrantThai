# GrantThai MCP server

GrantThai ships an MCP server so a researcher's AI assistant can create one
overview file, `build/NRIIS_SUBMISSION.md`, from one `project.yaml`. Any
client that speaks MCP over stdio can use it: desktop chat apps, coding
agents, IDE assistants, or a local model runner.

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
- **The AI must not invent a Thai fund, NRIIS or institutional fact.** If one
  is not in the researcher's own material, the AI writes the literal value
  `NEEDS_VERIFICATION`. It is stored as a marker, not as text.
- **`grantthai_validate` only reports.** It never changes `project.yaml`.
  Its findings are about form and consistency. They are not a verdict on the
  research.
- **`grantthai_build` writes exactly one file** and returns its content.
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
| `grantthai_new_project` | `grantthai init` | Writes a blank `project.yaml`, with every required field `NEEDS_INPUT`. It refuses to overwrite an existing file. |
| `grantthai_list_fields` | `grantthai fields` | Lists the fields in NRIIS entry order (id, tab, type, required, English label, guidance). Thai labels are `NEEDS_VERIFICATION`. |
| `grantthai_set_field` | `grantthai set` | Writes one value as an AI-assisted `DRAFT`. Takes `field_id`, `value`, `researcher_verbatim`, `chain_node`, `source_ids`, `links` and `tool`. |
| `grantthai_validate` | `grantthai validate` | Returns the validation report of BLOCK, REVIEW and INFO findings. Report-only. |
| `grantthai_explain` | `grantthai explain` | Explains one rule id, such as `S001`, `B002` or `SCHEMA`. |
| `grantthai_build` | `grantthai build` | Writes `build/NRIIS_SUBMISSION.md` and returns `path`, `summary` and `markdown`. It always renders, even when there are BLOCK findings, and lists them in the file. |

Paths default to `project.yaml` in the root folder. `as_of` (YYYY-MM-DD)
fixes the date used for fund-rule staleness checks. Two builds of the same
input with the same `as_of` date are byte-identical.

The machine-readable contract is `spec/mcp/tools.schema.json`. Its
`examples` entry is the implemented tool list, and `tests/mcp` checks the
server against it.

## Resources

| URI | Content |
|---|---|
| `grantthai://notice` | The independence notice printed on line 1 of every output body. |
| `grantthai://fields` | The field registry as JSON, the same data `grantthai_list_fields` returns. |

## Typical flow

1. `grantthai_new_project`, or skip this step if the researcher already has
   a `project.yaml`.
2. `grantthai_list_fields` with `required_only: true`.
3. Ask the researcher for each value. Record each one with
   `grantthai_set_field`: set `researcher_verbatim: true` when you pass on
   the researcher's own words, and use `NEEDS_VERIFICATION` for any fund,
   NRIIS or institutional fact that is not in their material.
4. Run `grantthai_validate`, and use `grantthai_explain` on any finding.
5. Run `grantthai_build`, then give the researcher the path and ask them to
   check every AI-drafted value.

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

## Not in v0.1

- No review, lock or status promotion, over MCP or anywhere else.
- No submission to NRIIS or to any fund.
- No HTTP transport. The HTTP API is a separate surface.
