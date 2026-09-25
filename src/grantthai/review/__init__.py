"""grantthai.review — named human review records, mapping acceptance, the
object LOCK and project diffs (v0.2 module C).

Everything here is AI-free and local-CLI only. There is deliberately no
MCP or REST exposure: `grantthai.api_py` does not import this package, so
neither `grantthai.mcp` nor `grantthai.api` can reach a function that
raises a status above DRAFT (spec/common/status_permissions.yaml,
"hard_ceiling"; tests/test_review.py::test_hard_ceiling_*).

Modules:
    records  - status transition table (spec/common/status_permissions.yaml),
               named review records, staleness, the deterministic-validator
               promotion to STRUCTURE_CHECKED / LOGIC_LINKED
    mapping  - accept / reject a LocalTerm -> AcademicConcept mapping
    lock     - the object LOCK and its broken-state check
    diff     - content / status / staleness diff of two project objects

This package MUST NEVER import grantthai.assist, grantthai.mcp,
grantthai.api, or any LLM SDK (openai, anthropic, google.generativeai,
etc.). Enforced by tools/ci/check_no_ai_import.py.
"""
