# Governance

## Maintainer

- Developer / maintainer: Yaoharee Lahtee (เยาฮารี หละตี), ORCID
  0009-0005-3861-0626.
- Developing organisation: ARAYA NIKAH SOCIAL ENTERPRISE CO.
  (อารยานิกะห์ วิสาหกิจเพื่อสังคม).
- Joint work: ผลงานร่วมกับ ศูนย์ความรู้พลเมืองปัญญาประดิษฐ์ ซึ่งเป็นศูนย์ของ
  อารยานิกะห์ วิสาหกิจเพื่อสังคม (a joint work with
  ศูนย์ความรู้พลเมืองปัญญาประดิษฐ์, a centre of ARAYA NIKAH SOCIAL
  ENTERPRISE CO.).

This is a statement of who builds and maintains GrantThai, not a claim of
affiliation with NRCT, TSRI, any PMU, or NRIIS — see `NOTICE`.

## Maker ≠ checker (binding)

Every PR into `main` needs review from someone other than its author. The
person or process that produced an artifact never certifies it themselves.
This applies to code, specs, fund-profile data, and documentation equally.

- `funds/**` changes require a cited official source, a capture/verification
  date, and a second human sign-off before merge (see
  `spec/fund/fund-profile.schema.json` and `docs/sources.md`).
- `spec/**` and `NOTICE` changes require a maintainer review
  (`.github/CODEOWNERS`).

### What counts as an independent check (repository releases)

*(Founder ruling, 2026-09-25. This replaces the earlier wording "AI review
never counts as the independent check".)*

- An **independent check** is a review by a checker who is **distinct from
  the maker**: a different person, or a different, fresh AI agent that did
  not produce the content.
- An AI review is therefore a valid maker ≠ checker check. It is not the
  last step: **the human founder approves every public release** (a public
  `git push`, a visibility change, a tag, a Zenodo deposit).
- A review by a person, or by an agent from a different vendor, raises the
  independence further and is preferred when available, but is not required.

This is a rule about *releasing this repository*. It is separate from the
review records **inside a project** (`spec/common/review_gates.yaml`): there,
a status of `VERIFIED(independent)` needs a named human review record, and AI
critique is never recorded as an independent review of a research project
(principle P4).

## Publication sequence

1. Scaffold locally (done: Phase 0).
2. Run the independent adversarial publish gate (leak and privacy scan,
   licence coverage, tier fidelity, citation accuracy, overclaim, every Thai
   rule string dated and sourced). The checker must be distinct from the
   maker (see above). Unresolved blocker or major findings stop the release.
3. The human founder approves the release.
4. Create or flip the GitHub repository to public and re-check its
   visibility (`gh api repos/<owner>/<repo> --jq .visibility`) before and
   after.
5. If a mirror is added later, register it in the maintainer's shared
   remote manifest so that divergence between remotes fails loudly.

## Branch protection

`main` will be protected once the GitHub repository exists (setting it up
is `NEEDS_INPUT` for the maintainer). After that, all changes land through a
pull request; direct pushes to `main` are not the normal path.

## Dissent is kept, not erased

When a reviewer or contributor disagrees with a decision that is adopted
anyway, the dissent is recorded here rather than deleted from history.

### Recorded dissent

- **AGPL vs Apache-2.0/CC BY 4.0 licensing (2026-09-25).** AGPL was raised
  as an option for the code license during planning. It was not adopted;
  Apache-2.0 (code) and CC BY 4.0 (docs, spec, data) were chosen instead
  (founder ruling K13, below). This entry preserves that AGPL was considered
  and rejected, not merely omitted. See `docs/design/PLAN.md` §H, K7.
- **Filename `NRIIS_SUBMISSION.md` (2026-09-25).** A critic-round finding
  proposed renaming the output file to reduce implied-endorsement risk.
  This was rejected as the default because the filename is the founder's
  own letter contract; it remains open as decision K4. See
  `docs/design/PLAN.md` §L (Critic publish, finding 4).
- **Diagram AI-hub risk (2026-09-25).** A finding that diagrams draw AI as
  a hub was only partly applied: the "bypass" edge (Person → Research Core
  directly, no AI) is required in every diagram and is checked at the
  human release gate, not by automated CI, because diagram parsing was
  judged unreliable (INSTINCT). See `docs/design/PLAN.md` §L (Critic
  parity, finding 13).
- **"AI review never counts" (2026-09-25).** The design plan (§H step 4)
  said AI review never counts as the independent check. The founder
  replaced this with the policy above. The earlier wording is kept in
  `docs/design/PLAN.md` as history.

## Rule precedence (no silent merging)

Law > current fund call > funder guide > institution rule > current NRIIS
requirement > project decision > historical guide. Conflicts between these
are surfaced to the human, never silently merged. See
`spec/common/chain.yaml` and `validators/rules.yaml`.

## Founder decisions log

The open questions K1–K16 are listed in `docs/design/PLAN.md` §K. Rulings
are recorded here with their date. A decision not listed as ruled is still
open; the plan's default applies until the founder rules.

| ID | Decision | Status | Date |
|---|---|---|---|
| K1 | Philosophy sentence 2 uses the neutral wording: "Toledo connects lived experience with academic knowledge through translation — by people, and optionally with AI assistance — while evidence, methodology, and human expertise remain the gates to verifiable knowledge." | RULED | 2026-09-25 |
| K13 | The founder, Yaoharee Lahtee, owns core files 01–06 of the handoff package. Files derived from them are licensed Apache-2.0 (code) and CC BY 4.0 (documentation, specifications and data). This also settles the licence split asked in K7; CC0 is not used. | RULED | 2026-09-25 |
| K14 | Labels from the screenshot-derived readout are **not** used. NRIIS labels and tab order will come later from public documents and stay `NEEDS_VERIFICATION` until then. | RULED | 2026-09-25 |
| — | The repository goes **public** after the independent publish gate passes. | RULED | 2026-09-25 |
| — | Independent-check policy for releases: a checker distinct from the maker (a different person or a different, fresh AI agent), plus the human founder's approval of every public release (see "What counts as an independent check"). | RULED | 2026-09-25 |
| — | AI stays optional: any "cold read" acceptance check must be satisfiable by a human alone; an AI cold read is optional and additional, never required. | RULED | 2026-09-25 |
| — | The design plan is founder-owned and published as `docs/design/PLAN.md` (local paths removed; excluded file names generalised). | RULED | 2026-09-25 |
| — | Scope of the next release: "เอาแค่ สกิล mcp และ api ที่นักวิจัยใช้เอไอ ดึงไปใช้สร้างไฟล์สำหรับวางภาพรวมได้" ("only the skill, MCP and API that a researcher's AI can pull in to create the overview file"). v0.1.0 ships the engine plus the skill, MCP server and HTTP API over it; the web form, launchers, Citizen Mode, review/lock and SHACL are deferred. The researcher's own information is the source; AI output stays `DRAFT`, never `SOURCE`, never validates. | RULED | 2026-09-25 |
| K7 | DCO vs CLA for outside contributions. The plan default (DCO) is in use. | OPEN | — |
| K3 | Final names (`GrantThai`, `grantthai`, `GRANTTHAI_STANDALONE.md`). Plan default in use. | OPEN | — |
| K4 | Endorsement and trademark risk of the name and of `NRIIS_SUBMISSION.md`. Plan default in use (filename kept). | OPEN | — |
| K2, K5, K6, K8–K12, K15, K16 | See `docs/design/PLAN.md` §K. Plan defaults in use. | OPEN | — |

The founder's public-release ruling did not make K2–K12, K15 or K16 a
precondition for the public push; they stay open with the plan defaults in
effect.
