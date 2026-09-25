# AGENTS.md — binding entry point for any AI builder

**Any AI system (any vendor) that is about to read, plan, or build in this
repository must read this file first**, per the founder's purpose:
"เพื่อให้เอไอตัวอื่นอ่าน git แล้ววางระบบได้เลย" (so that any other AI can read
this git repository and build the system on its own).

`CLAUDE.md` and `GEMINI.md` at the repo root are thin pointers to this
file, so that whichever vendor-specific entry file a given harness looks
for first still lands here.

## Read order

1. This file (`AGENTS.md`) — non-negotiables and read order.
2. `docs/design/PLAN.md` — the founder-owned design plan this scaffold was
   built from, published in the repository. It is a historical record of
   2026-09-25; where it and `spec/`, `GOVERNANCE.md` or
   `docs/deviations.md` differ, those files win. Anywhere in this
   repository, "plan §X" or "plan section X" means a section of this file.
3. `README.en.md` — the human-facing overview, no-AI quickstart, philosophy,
   one-input-one-output contract, ecosystem summary, in English.
   `README.md` is the Thai cover (short, with the organisation logo);
   follow its own `English` link to reach `README.en.md`.
4. `GRANTTHAI_STANDALONE.md` — the full system/architecture description.
5. `docs/BUILD_GUIDE.md` — the phase-by-phase build plan, with exact files,
   contracts, commands, tests, and acceptance criteria per phase.
6. `spec/INDEX.yaml` — the manifest of every contract file, its version,
   status, and which phase needs it.
6a. `routes/INDEX.yaml` — the router: every output route, its `route.yaml`,
   its output filename, and the shared/route partition of the field
   registry. "Router" means a deterministic output route chosen by a
   person, never by an AI.
7. The specific `spec/**` files for whatever you are about to build.
8. `docs/deviations.md` — where this scaffold intentionally departs from
   the original handoff package, so you do not "fix" an intentional
   deviation back to the original.
9. `docs/contradictions.md` — where the design sources contradict each
   other. Every entry is OPEN with both readings kept; do not resolve one
   silently in code, and do not drop a reading.

## If you are an AI helping a researcher USE GrantThai (not build it)

Load `skills/grantthai/SKILL.md` and follow it. Short form: the
researcher's own information is the source; you interview and draft, you
never validate knowledge, never mark your own wording `SOURCE`, never
invent a Thai fund, NRIIS or journal fact (write `NEEDS_VERIFICATION`),
leave gaps as `NEEDS_INPUT`, list the routes and let the researcher choose
(never choose for them), and hand back exactly one file per route they
pick: `build/ACADEMIC_ARTICLE.md`, `build/NRIIS_SUBMISSION.md` or
`build/RESEARCH_CONCEPT_NOTE.md`. Three equivalent surfaces wrap the same
engine (`src/grantthai/api_py.py`), each capped at `DRAFT` inside the
engine:

| Surface | Entry | Docs |
|---|---|---|
| Agent skill | `skills/grantthai/SKILL.md` (chat-only AI: `skills/grantthai/reference/PROMPT_PACKET.md`) | `docs/use-with-ai.md`, `docs/th/use-with-ai.th.md` |
| MCP server (stdio) | `grantthai-mcp --root DIR` | `docs/mcp.md`, `spec/mcp/tools.schema.json` |
| HTTP API (local) | `grantthai-api` | `docs/api.md`, `spec/api/openapi.yaml` |

Every surface, and any AI building this repository, works under the
**AI-use ceiling**, `docs/policy/ai-use-ceiling.md` (Thai:
`docs/policy/ai-use-ceiling.th.md`), built on the GenAI guideline 2569
(`docs/sources.md`). In short: show the personal/confidential-data warning
before accepting any data; record the tool and version in
`authoring.ai_use_declaration` (automatic on every AI-assisted write);
never generate or alter research data or evidence; never supply a
reference from memory; never set `declaration_confirmed_by_human` (only the
researcher does); never use GrantThai to evaluate someone else's proposal.
Rules AI001-AI004 are REVIEW only.

## The one-input, one-output-per-route contract (headline)

See `spec/contracts/one-input-one-output.md` (0.3.0-draft) for the full
contract. Founder reframe, 2026-09-25: "การลงใน NRIIS ไม่ใช่แกนหลักอีกต่อไป
แต่เป็นแค่ทางเลือกหนึ่งของ router เพราะเราจะเปิดให้ตั้งแต่การทำบทความวิชาการด้วย" —
entering NRIIS is one route of the router, not the core.

- **One input:** `work.yaml` (`spec/work/work.schema.json`, 0.3, a superset
  of `project.yaml` 0.2) is the only canonical input. A legacy
  `project.yaml` is read unchanged as the NRIIS route; a directory holding
  both stops `build` (exit 2). Every editor (forms, questionnaires,
  optional AI assist) writes this same file; none of them is a separate
  input.
- **One command per route:** `grantthai build <work.yaml> --route <id>`
  (`route build`). The route comes from `--route`, else
  `routing.default_route`, else the legacy file → `nriis-proposal`, else
  the single route whose `default_for_work_types` lists the object's
  `work_type`; otherwise the tool lists the candidates and stops. **The
  tool never picks a route**, and neither does an AI surface: MCP and HTTP
  return the candidates for the researcher to choose from.
- **One output per route:** `build/NRIIS_SUBMISSION.md`
  (`spec/output/nriis-submission.contract.md`, unchanged, `submittable`
  against the bound fund profile only), `build/ACADEMIC_ARTICLE.md`
  (`spec/output/academic-article.contract.md`, `manuscript_ready` = no
  BLOCK, never "accepted"), `build/RESEARCH_CONCEPT_NOTE.md`
  (`spec/output/research-concept-note.contract.md`, never submittable).
  Each invocation writes exactly one file and leaves the other routes'
  files byte-identical. No second GrantThai-generated file is needed to
  use a route's output (attachments and figures are the person's own
  files, listed with their status).
- `routing` is excluded from `content_sha256`: choosing a route never
  makes a review record or the lock stale (`spec/common/object-hash.md`).
- `profile.yaml` is an editor convenience only; `build` never reads it.
  Identity and team data live in `work.yaml` (`PROFILE.*`, `ARTICLE.*`).
- The article route ships no venue registry and names no journal. A venue
  fact enters only through the researcher's `ARTICLE.VENUE.TARGET` record
  with the source they supplied (rule ART010); both sub-profiles are
  `NEEDS_VERIFICATION`. GrantThai never composes section text.

## Ecosystem position

GrantThai bridges Problem/Knowledge → Researchable project →
Funding-aligned project (when the route needs a fund) → route-ready output
(article, NRIIS proposal or concept note; NRIIS is one route). See `docs/ecosystem.md` and
`ecosystem/ecosystem.yaml` for the full picture (two nested ecosystems,
actor table, flows, sibling-infrastructure pointers). Do not implement
anything that would let GrantThai submit to NRIIS, decide PI eligibility
outside the bound fund profile, or grant any validation/official status —
these are hard boundaries, not style choices.

## Non-negotiables (do not "fix" these; they are deliberate)

1. **AI is optional everywhere, never required.** Every core task must be
   completable by a human alone, with no AI, no network, and (for at least
   one path) no terminal. See `README.md` "AI is optional everywhere" and
   `spec/common/parity.yaml`.
2. **AI is never SOURCE and never validates.** AI output caps at `DRAFT`;
   only a deterministic validator sets `STRUCTURE_CHECKED`/`LOGIC_LINKED`;
   only a named human review record sets `HUMAN_REVIEWED`/`VERIFIED`/`LOCKED`.
   See `spec/common/status_permissions.yaml` ("hard_ceiling") — MCP, REST,
   and `assist` can never exceed `DRAFT`, and this must be enforced in
   `src/grantthai/core`, never trusted to a caller.
3. **No invented Thai or journal facts.** Any time-bound Thai rule, agency
   detail, NRIIS field label, NRIIS tab name or tab order, or any journal
   or publisher requirement (scope, indexing, word limits, fees, review
   time) you do not have a current, cited public source for must be written as the literal string
   `NEEDS_VERIFICATION` (or `NEEDS_INPUT` for a value the user must
   supply) — never guessed, never filled from training-data recall. The
   field registry (`registry/fields.jsonl`) already follows this: English
   labels are descriptive (from the handoff package), every Thai label is
   `NEEDS_VERIFICATION`. Candidate Thai labels read from a cited public
   document live only in `mappings/nriis/labels@<edition>.yaml`, stay
   `NEEDS_VERIFICATION`, and are shown tagged "candidate", never as
   official. See `spec/common/status.yaml` and `docs/sources.md`.
4. **No AI/vendor authorship anywhere.** No `Co-Authored-By` trailer naming
   an AI vendor, no `Claude-Session:` line, no "Generated with ..." footer,
   in any commit message, PR, file, or release note. `.githooks/commit-msg`
   enforces this at commit time; `tools/ci/check_attribution.py` enforces
   it in CI (git history, tracked files, PR title/body). The **only**
   sanctioned place any AI model is named is the Core Epistemic Structure
   role-disclosure block in `docs/lineage.md` and the README footers — and
   even there, only as role disclosure, never as author/co-author/credit.
   If you are an AI drafting a commit message or PR description for this
   repository right now: do **not** add your own attribution trailer, even
   if your own harness's default behavior is to do so.
5. **The unofficial NOTICE is non-negotiable.** GrantThai is not affiliated
   with NRCT, TSRI, any PMU, or NRIIS. The one-line NOTICE constant
   (`spec/output/notice_constant.txt`) is reused byte for byte in
   `NOTICE`, `README.md`, `README.en.md`, `ai.json`, `llms.txt`,
   `llms-full.txt`, `GRANTTHAI_STANDALONE.md`, and as line 1 of every
   route's rendered output body (`NRIIS_SUBMISSION.md`,
   `ACADEMIC_ARTICLE.md`, `RESEARCH_CONCEPT_NOTE.md`);
   `tools/ci/check_notice.py` enforces this on every route template. A
   route may add its own notice on line 2 (the article route: not
   affiliated with any journal or publisher) but never replaces the
   constant. Other files point to `NOTICE` rather than paraphrasing it.
6. **Public-repo exclusions are absolute.** Never commit: the original
   handoff package as-is, source PDFs, the screenshot-derived readout,
   the Toledo concept reference image, private workspaces, or any real
   fund/proposal data. See `docs/sources.md` and `docs/design/PLAN.md`
   §H "Excluded from the public repo".
7. **Maker ≠ checker.** You (an AI) producing an artifact does not certify
   it. A different checker (a person, or a different, fresh AI agent) must
   check it, and the human founder approves every public release. See
   `GOVERNANCE.md`.

## Definition of done, per phase

See `docs/BUILD_GUIDE.md` for the full phase-by-phase plan and acceptance
criteria (AT-1 through AT-6). In short:

- **Phase 0 (this scaffold):** tree skeleton, governance/policy files,
  data contracts, the field registry and rule catalog as data, CI guards
  each with a seeded bad fixture, `docs/sources.md`/`docs/deviations.md`.
  Acceptance: every guard passes on the real tree and fails on its own
  seeded bad fixture (`bash tools/ci/run_all_guards.sh`), and `pytest`
  passes. The founder's rulings K1, K13 and K14 and the decision to
  publish are recorded in `GOVERNANCE.md` ("Founder decisions log").
- **v0.1.0 (founder scope change 2026-09-25):** the engine (renderer,
  validator, AI-free CLI, Python API), one fund profile
  (`FICTIONAL_CALL@0.1`), one worked example, plus the skill, MCP server
  and HTTP API wrappers (moved forward from v0.4). The offline webform,
  launchers and Citizen Mode are deferred. See `docs/BUILD_GUIDE.md` and
  `GOVERNANCE.md` ("Founder decisions log").
- **v0.2 "Citizen, no AI" + review + lock:** Citizen Mode, concept note,
  review/lock, bridge ontology + generated SHACL. See AT-1/AT-2 extended.
- **v0.3 router (unreleased):** `work.yaml` 0.3, `routes/` with three
  routes, `route list|check|build`, `migrate`, the `ARTICLE.*` fields and
  the ART family. Acceptance AT-R1 (a 0.2 file builds byte-identical
  `NRIIS_SUBMISSION.md`), AT-R2 (the fictional article builds exactly one
  file), AT-R3 (one object, two routes, two files, each build leaves the
  other byte-identical). See `docs/BUILD_GUIDE.md` "v0.3 router".
- **v0.3 optional AI assist:** `grantthai[ai]`, parity CI. See AT-3b.
- **v0.4 interfaces:** REST, browser-assist. (MCP shipped early, in v0.1.0 —
  see above.)
- **v0.5 real fund profiles, network, labels** (v0.1.0 already carries
  *candidate* Thai labels from public documents, all `NEEDS_VERIFICATION`,
  in `mappings/nriis/labels@nrct-manual-2566.yaml`).

Do not skip ahead: the AI-free CLI path exists and passes its tests; the
skill/MCP/API wrappers were built only on top of it, by founder ruling.
Any v0.3 `assist` feature still needs its tested human equivalent first.
