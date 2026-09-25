"""grantthai.guidance — the writing layer (v0.2).

Reads `guidance/writing_intent.yaml` (schema
`spec/guidance/writing_intent.schema.json`): per-field purpose,
micro-template, length target, keep-out list and quality traits, plus the
completeness checklist. Guidance only: nothing here changes a status, and
length findings are REVIEW-level (rules W101/W102).

This package MUST NEVER import grantthai.assist, grantthai.mcp,
grantthai.api, or any LLM SDK (tools/ci/check_no_ai_import.py).
"""
from grantthai.guidance.writing import (  # noqa: F401
    checklist,
    explain_field,
    intent,
    length_findings,
    load,
)
