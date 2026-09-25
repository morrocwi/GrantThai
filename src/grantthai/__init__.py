"""GrantThai — open, unofficial research infrastructure.

Phase 0: package skeleton only. No implementation yet.

Hard rule (see spec/common/status_permissions.yaml, README "AI is optional
everywhere"): the AI-free core packages below (core, validators, review,
fund, mapping, render, interview, cli) MUST NEVER import grantthai.assist,
grantthai.mcp, grantthai.api, or any LLM SDK. This is enforced by
tests/test_no_ai_import and the CI "no-AI-import" guard
(tools/ci/check_no_ai_import.py).
"""

__version__ = "0.0.0-phase0"
