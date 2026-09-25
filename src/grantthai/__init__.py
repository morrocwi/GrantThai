"""GrantThai — open, unofficial research infrastructure.

v0.1: the AI-free engine (core, validators, render, cli) and the thin
Python API grantthai.api_py: one work.yaml (or legacy project.yaml) -> one
file per chosen route (build/NRIIS_SUBMISSION.md, build/ACADEMIC_ARTICLE.md
or build/RESEARCH_CONCEPT_NOTE.md).

Hard rule (see spec/common/status_permissions.yaml, README "AI is optional
everywhere"): the AI-free core packages below (core, validators, review,
fund, mapping, render, interview, cli) MUST NEVER import grantthai.assist,
grantthai.mcp, grantthai.api, or any LLM SDK. This is enforced by
tests/test_no_ai_import and the CI "no-AI-import" guard
(tools/ci/check_no_ai_import.py).
"""

__version__ = "0.2.0"
