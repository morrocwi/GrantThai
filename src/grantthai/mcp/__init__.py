"""grantthai.mcp — OPTIONAL MCP server (stdio) over grantthai.api_py.

Tools: grantthai_new_project, grantthai_list_fields, grantthai_set_field,
grantthai_validate, grantthai_explain, grantthai_build. Resources:
grantthai://notice, grantthai://fields. See docs/mcp.md.

Never loaded in the core path: the core packages (grantthai.core,
.validators, .review, .fund, .mapping, .render, .interview, .cli) never
import this package. Nothing in this package may set a field's status
above DRAFT or submit anything (spec/common/status_permissions.yaml,
'hard_ceiling'; spec/mcp/tools.schema.json).
"""
