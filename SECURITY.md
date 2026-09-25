# Security Policy

## Reporting a vulnerability

Contact: `NEEDS_INPUT` — the founder must supply a non-personal contact
address (e.g. a project or organisational email) before this is complete.
Do not open a public issue for a security vulnerability or a data leak
(such as personal data accidentally committed) until this contact is set.

## Scope

- GrantThai (v0.x) has no server and no network calls in its core path. The
  main security surfaces are: (1) accidental leakage of personal data or
  credentials into the repository, (2) supply-chain risk in dependencies,
  and (3) prompt-injection risk once `assist`/MCP ship (v0.3+).
- `gitleaks` runs in CI on every push and PR.
- The leak scan (`tools/ci/check_leak_pii.py`) keeps only generic patterns
  in the public source. Maintainer-specific terms (local account names,
  private workspace or repository names) are loaded at run time from an
  untracked, gitignored `.leakdeny.local` file or the `GRANTTHAI_LEAKDENY`
  environment variable (a CI secret), because a committed denylist would
  itself leak those terms.
- Fund profiles and templates are data-only records with no free-text
  "instructions" field, specifically to block prompt injection against any
  future AI-assisted feature.
- AI flags in `ai.json` and `llms*.txt` are advisory only (P11). The actual
  guards are the status-permission code and CI, not the advisory text.

## Versioning

Tags are signed and versions follow SemVer once releases begin (v0.1+).
Phase 0 has no tagged release.
