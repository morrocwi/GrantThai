"""grantthai.core — AI-free core package (Phase 0: two reference modules
only — object_hash.py implements spec/common/object-hash.md and links.py
implements spec/common/links-and-sources.md; the project object model and
status engine ship in v0.1).

This package MUST NEVER import grantthai.assist, grantthai.mcp,
grantthai.api, or any LLM SDK (openai, anthropic, google.generativeai,
etc.). Enforced by tools/ci/check_no_ai_import.py.
"""
