# Contributing to GrantThai

Thank you for considering a contribution. Please read `GOVERNANCE.md` and
`docs/deviations.md` first for the design decisions already made, and
`AGENTS.md` if you (human or AI) are about to build a new phase.

## Developer Certificate of Origin (DCO)

Contributions from anyone other than the maintainer, from the first public
release onward, must be signed off under the [Developer Certificate of
Origin](https://developercertificate.org/) (DCO vs CLA is still open as
decision K7; DCO is the default in use). The maintainer's initial Phase 0
scaffold commits pre-date this rule. Add a `Signed-off-by` trailer to every
commit, e.g.:

```
Signed-off-by: Your Name <your.email@example.com>
```

`git commit -s` adds this automatically. This is separate from, and not a
substitute for, the attribution rules below.

## No AI/vendor attribution

`.githooks/commit-msg` rejects `Co-Authored-By` lines naming an AI vendor,
`Claude-Session:` trailers, and "Generated with ..." footers. If you use an
AI assistant while contributing, do not let it add these — see
`GOVERNANCE.md` and the README's Core Epistemic Structure section for the
one sanctioned place a model may be named (role disclosure only, in
`docs/lineage.md`).

Run once after cloning:

```
git config core.hooksPath .githooks
```

## Local leak denylist (optional, maintainers)

`tools/ci/check_leak_pii.py` loads maintainer-specific leak patterns from
an untracked `.leakdeny.local` file at the repository root (one regular
expression per line; the file is gitignored) or from the
`GRANTTHAI_LEAKDENY` environment variable. Never commit such a list.

## Fund profile changes

Any change under `funds/**` needs: a cited official source, a
capture/verification date, and review by a second human (maker ≠ checker).
See `spec/fund/fund-profile.schema.json`.

## Pull requests

- One logical change per PR where practical.
- CI must pass, including the guard scripts and their seeded fixtures
  under `tests/`.
- A different person reviews and merges than the one who authored the
  change (maker ≠ checker), per `GOVERNANCE.md`.
