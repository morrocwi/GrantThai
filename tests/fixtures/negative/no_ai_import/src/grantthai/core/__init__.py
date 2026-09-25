"""Seeded BAD fixture: a core module must never import an LLM SDK."""
import openai  # noqa: F401 -- intentionally bad, for CI guard testing
