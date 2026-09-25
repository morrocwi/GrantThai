# Build guide — a step-by-step plan an AI (or human) can execute

Read `AGENTS.md` first. This file is the phase-by-phase build plan it
points to. Every phase names: exact files to create, the contract/schema
each must satisfy, commands, tests/fixtures, acceptance criteria, and what
NOT to do.

## Founder scope change, 2026-09-25 (binding)

The founder narrowed the next release to:

> "เอาแค่ สกิล mcp และ api ที่นักวิจัยใช้เอไอ ดึงไปใช้สร้างไฟล์สำหรับวางภาพรวมได้"
>
> ("Only the skill, MCP and API that a researcher using AI can pull in to
> create the file that lays out the overview.")

What this means for the phases below:

- **Built in v0.1.0:** the engine (one `project.yaml` → exactly one
  `build/NRIIS_SUBMISSION.md`), the AI-free CLI and Python API, and three
  thin wrappers over `src/grantthai/api_py.py`: the agent skill
  (`skills/grantthai/`), the MCP server (`src/grantthai/mcp/`, moved
  forward from v0.4) and the local HTTP API (`src/grantthai/api/`, moved
  forward from v0.4).
- **Knowledge principle for all three:** the researcher's own information
  is the source; AI never validates knowledge, never marks its own prose
  `SOURCE`, never invents Thai fund or NRIIS facts (`NEEDS_VERIFICATION`);
  AI drafts are `DRAFT`/`INFERENCE` for the researcher to confirm. The
  ceiling is enforced in `src/grantthai/core`, not by the wrappers.
- **Also in v0.1.0 (audit of the design sources, 2026-09-25):** registry
  `origin` per field (core/02 §2; only `NRIIS_NATIVE` fields are placed on
  a tab), the contradiction register (`registry/contradictions.yaml`,
  `docs/contradictions.md`, a defined "Conflicts and open contradictions"
  output section), 22 fields the forms ask for (sub-projects,
  past performance, ISCED, references, IP check, risks, entrepreneur,
  sustainability, team expertise and credentials, project-lead track
  record, funding alignment, theoretical foundations, propositions,
  boundary conditions), 12 more rules plus the full crosswalk
  (`validators/crosswalk.yaml`), and candidate Thai labels from public
  documents (`mappings/nriis/labels@nrct-manual-2566.yaml`, all
  `NEEDS_VERIFICATION`).
- **Deferred (not cancelled):** the offline web form, the launchers,
  `forms/*.md` import, Citizen Mode, review/lock, the concept note, the
  bridge ontology / SHACL, and the v0.3 `assist` package. The phase
  descriptions below remain the plan for those parts.

## Cold-start check

Before building anything, confirm you can answer every question below by
pointing at a file in this repository. If you cannot, stop and say so —
do not guess or invent an answer.

| Question | Answered by |
|---|---|
| What is the one input, and what is the one output? | `spec/contracts/one-input-one-output.md`, `README.md` |
| What schema does the input conform to? | `spec/project/project.schema.json` (+ `spec/common/field_record.schema.json`, `spec/common/evidence.schema.json`) |
| Which fields exist, with labels, types, required flags and input controls? | `registry/fields.jsonl` (schema `spec/registry/field.schema.json`) |
| What does each registry `type` mean for a value (JSON type, money/percent precision, dates)? | `spec/registry/types.yaml` |
| What keys does each repeating-group or group field hold (e.g. an activity's `weight_percent`, a budget line's `quantity`/`unit_price`/`line_total`, a team member's `project_role: PI` and `contribution_percent`)? | `spec/registry/structured_fields.schema.json` (`$defs/<field_id>`; lint-enforced for every `array<object>`/`object`/`rich_text\|object` field) |
| How do items link to each other, and what is `project:chain_edges`? | `spec/common/links-and-sources.md` §1–2 (reference implementation `src/grantthai/core/links.py`) |
| What is a resolvable source reference, and which fields need one? | `spec/common/links-and-sources.md` §3, `spec/common/source.schema.json` |
| What does a complete, valid project look like? | `examples/lecturer-no-ai/project.yaml` (FICTIONAL; `tests/test_example_project.py` recomputes the v0.1 link/sum/budget/source/DAG rules on it) |
| Which NRIIS tab does each field land on? | `mappings/nriis/section_to_tab.yaml` → generated `registry/nriis-fields.jsonl` (all `NEEDS_VERIFICATION`) |
| Which fields are NRIIS boxes and which are authoring-only? | `origin` in `registry/fields.jsonl` (core/02 §2): only `NRIIS_NATIVE` fields get an `NRIIS.*` record; `render_from` on a narrative field lists the records it is written from |
| Where do the design sources contradict each other, and what does GrantThai do meanwhile? | `docs/contradictions.md` / `registry/contradictions.yaml` (every entry OPEN, both readings kept); `conflicts` on registry records |
| Where do candidate Thai labels, OECD codes, budget categories and output/outcome/impact typologies come from? | `mappings/nriis/labels@nrct-manual-2566.yaml` (schema `spec/mappings/labels.schema.json`), each cited to a public document in `docs/sources.md` (SD-1..SD-4); all `NEEDS_VERIFICATION`, never official |
| Which package validation code (core/02 V-*, core/04 V-*, core/05 VAL.*) is which GrantThai rule? | `validators/crosswalk.yaml` |
| Which policy lenses and ecosystem positions can a project select? | `ecosystem/positions@2026-09.yaml` (RELAYED, `NEEDS_VERIFICATION`) |
| Which validation rules exist, with severity and chain step? | `validators/rules.yaml` (schema `spec/validators/rule.schema.json`) |
| How is the project object hashed, and why does a review or status change not make a review stale? | `spec/common/object-hash.md` (`content_sha256` vs `state_sha256`), reference `src/grantthai/core/object_hash.py`, golden vectors `tests/golden/object-hash/` |
| How are the JSON Schemas loaded (their `$id`s are URLs)? | Load every `spec/**/*.schema.json` into a local registry keyed by `$id` and resolve `$ref`s through it; never fetch the URL. See `build_registry` in `tools/ci/check_schema_lint.py` |
| What schema does the output conform to (section order, per-field block format, readiness-summary format)? | `spec/output/nriis-submission.contract.md` |
| What is the chain of research stages a project must populate? | `spec/common/chain.yaml` |
| What are the valid field statuses, and who can set which transition? | `spec/common/status.yaml`, `spec/common/status_permissions.yaml` |
| What are the review gates and what does a review record look like? | `spec/common/review_gates.yaml`, `spec/common/review.schema.json` |
| How is a fund profile structured, and who decides eligibility? | `spec/fund/fund-profile.schema.json` |
| What is the field-ID naming convention? | `spec/project/project.schema.json` (`field_id` pattern), and this file's "Field-ID convention" section below |
| Which packages may never import an LLM SDK, and how is that enforced? | `spec/common/status_permissions.yaml` ("hard_ceiling"), `tools/ci/check_no_ai_import.py` |
| What must never be hardcoded outside `funds/`? | `tools/ci/check_no_hardcoded_rules.py` (allowlist in its docstring) |
| Where does a Thai NRIIS field label come from, and what if none exists yet? | `spec/nriis/field.schema.json` ("NEEDS_VERIFICATION" convention), `docs/sources.md` |
| What is intentionally different from the original handoff package, and why? | `docs/deviations.md` |
| What must never be committed? | `docs/sources.md`, `AGENTS.md` "Public-repo exclusions" |
| What counts as "done" for the phase I'm building? | This file, per-phase "Acceptance" sections below |
| Which parts are known founder-input gaps, where a builder must stop rather than invent? | Rule family `ECO` (`ids_status: NEEDS_INPUT` in `validators/rules.yaml`; no rule ids exist yet), `spec/common/parity.yaml` (empty until v0.3), every `NEEDS_VERIFICATION` label/option list (K14) |

If a question above has no file to point at yet, that is a gap in this
guide, not license to invent an answer — flag it and, if you are extending
this guide, add the missing file/section rather than silently working
around it.

## Field-ID convention (stable across all phases)

Format: `<NS>.<GROUP>[.<SUB>].<NAME>`, characters `[A-Z0-9_]` only.

- Authoring namespaces: `PROFILE`, `FUND`, `CORE`, `METHOD`, `WORK`, `GEO`,
  `BUDGET`, `COMP`, `READY`, `RESULTS`, `DOC`, `AUDIT`, `BRIDGE`.
- Render-only namespace: `NRIIS.<TAB>.<FIELD>`, produced ONLY by
  `mappings/nriis/*.yaml` — never authored directly (P2, one-input
  contract).
- IDs are never reused. A rename appends an entry to `registry/aliases.yaml`
  instead of deleting/reusing the old ID.
- Registry fields keep their registry id (`registry/fields.jsonl`). Chain
  content that has no registry field (e.g. PriorKnowledge, Evidence, Claim
  items) uses `CORE.<NODE>.<NAME>`, e.g. `CORE.EVIDENCE.E1`,
  `CORE.CLAIM.C1`.
- In `project.yaml`, a field whose registry `chain_node` is set lives under
  `chain.<node>`; a field whose `chain_node` is null lives under `fields`.

## Build order (matches the original package brief's intended order)

1. Repository tree (Phase 0 — done; see below).
2. Field-ID convention (above — fixed, do not change without a
   `registry/aliases.yaml` migration path).
3. Project schema (`spec/project/project.schema.json`).
4. Fund profile schema (`spec/fund/fund-profile.schema.json`).
5. Field registry (`registry/fields.jsonl`, done in Phase 0) and the
   generated NRIIS render registry (`registry/nriis-fields.jsonl`, from
   `tools/registry/build_nriis_fields.py`).
6. Ontology (`ontology/grantthai.jsonld`, `context.jsonld`).
7. SHACL (generated from `spec/common/chain.yaml` — v0.2, not v0.1).
8. Validation-rule registry (`validators/rules.yaml`, catalog done in
   Phase 0; implementations ship v0.1/v0.2).
9. Mapping (`mappings/nriis/section_to_tab.yaml`, done in Phase 0 and
   `NEEDS_VERIFICATION` — tab names and order describe one observed form;
   `mappings/nriis/nrct-master-hss@<observed-date>.yaml` once a dated,
   public-document capture exists; `mappings/modes/*_to_core.yaml`).
10. Output contract (`spec/output/nriis-submission.contract.md` — done in
    Phase 0 as a draft; the renderer implementing it ships v0.1).
11. CLI contract (`spec/output/...` covers the render half; the CLI command
    table lives in `README.md`/`GRANTTHAI_STANDALONE.md` and is implemented
    in `src/grantthai/cli`).
12. MCP contract (`spec/mcp/tools.schema.json` — contract only, Phase 0;
    implementation v0.4).
13. One anonymized/fictional fixture end to end
    (`funds/example/FICTIONAL_CALL@0.1/`, `examples/lecturer-no-ai/`).
14. Pipeline (`grantthai validate` → `grantthai build`), wired to the
    fixture above, proven deterministic.

## Phase 0 — local scaffold (this repository's current state)

**Status: done.** Deliverables: tree skeleton, `.githooks/commit-msg` as
commit #1, governance/NOTICE/PRIVACY/SECURITY files, `spec/**` contracts,
`spec/mcp/tools.schema.json` (contract only), the field registry
(`registry/fields.jsonl`, derived from the handoff package core/05 under
founder ruling K13), the section-to-tab table, the rule catalog
(`validators/rules.yaml`), CI guards with seeded bad fixtures,
`docs/sources.md`, `docs/deviations.md`, `docs/design/PLAN.md`.

**Acceptance:** `bash tools/ci/run_all_guards.sh` exits 0 (every guard
passes on the real tree and fails on its own seeded bad fixture), `pytest`
passes, and `reuse lint` passes.

**Release:** the repository becomes public only after the independent
publish gate passes and the human founder approves (`GOVERNANCE.md`,
"Publication sequence").

**Do NOT, in Phase 0:** implement the renderer, the CLI, or web-form logic
beyond stubs.

## v0.1 — "Lecturer, no AI"

**Files to create:**
- `src/grantthai/core/*` — the project object model (load/save
  `project.yaml`, apply a field update, compute status transitions per
  `spec/common/status_permissions.yaml`).
- `src/grantthai/validators/*` — implement rule families S (S001-S008),
  R, W, B, T (T001-T002), CH001-CH002, F001-F004, ELIG001 from
  `validators/rules.yaml`. Link rules read `project:chain_edges` exactly as
  `spec/common/links-and-sources.md` defines it; reuse or match
  `src/grantthai/core/links.py` and `object_hash.py` (the golden vectors
  and `tests/test_example_project.py` must keep passing).
- `src/grantthai/render/*` — Jinja2 renderer implementing
  `templates/nriis_submission.md.j2` per
  `spec/output/nriis-submission.contract.md`.
- `src/grantthai/cli/*` — `init`, `fill --interactive`, `set`,
  `import-form`, `validate`, `explain`, `fund check`/`fund stale`, `build`,
  `export`, `doctor` (see `README.md`'s command table).
- `registry/fields.jsonl` — **already in the repository** (derived from
  core/05 in Phase 0). v0.1 adds Thai guidance text (`guidance.th`,
  currently `NEEDS_INPUT`) written by a human, and keeps every `label_th`
  `NEEDS_VERIFICATION` until a public-document capture exists (K14).
  v0.1 needs nothing from the private handoff package.
- `registry/nriis-fields.jsonl` — regenerate with
  `python tools/registry/build_nriis_fields.py` whenever the registry or
  `mappings/nriis/section_to_tab.yaml` changes (a test fails if it is out
  of date). The one dated NRIIS form mapping ships only once a public
  document fixes the form's tabs and labels.
- `ontology/grantthai.jsonld`, `context.jsonld` (core nodes only).
- `webform/index.html` (real implementation, generated from
  `registry/fields.jsonl`; no network calls, ever).
- `forms/*.md` (real per-tab content), `launchers/*` (real wrapper scripts).
- `interview/expert.th.yaml` (real Thai Expert question set).
- `examples/lecturer-no-ai/` (a full worked, FICTIONAL example).
- `docs/th/for-lecturers-no-ai.md`, `docs/en/for-lecturers-no-ai.md`.

**Contracts to satisfy:** `spec/project/project.schema.json`,
`spec/fund/fund-profile.schema.json` (against
`funds/example/FICTIONAL_CALL@0.1/`), `spec/nriis/field.schema.json`,
`spec/output/nriis-submission.contract.md`.

**Commands:** `grantthai validate project.yaml`, `grantthai build
project.yaml` (against the FICTIONAL fund profile).

**Tests/fixtures:** one negative fixture (`project.yaml` + `expected.json`
under `tests/fixtures/negative/<rule_id>/`) for every BLOCK rule that ships
in v0.1 AND is evaluated by this build — run by
`tests/test_negative_fixtures.py`. A BLOCK rule that v0.1 does not evaluate
(`grantthai.validators.engine.V01_NOT_EVALUATED`) points `negative_fixture`
at the literal `not_evaluated_in_v0.1` instead, and REVIEW/INFO rules that
v0.1 does evaluate point it at the `test:<path>::<function>` pytest
function that exercises them; see `spec/validators/rule.schema.json` for
the three accepted forms. Determinism (same input + same renderer version
⇒ byte-identical output) is `tests/test_engine.py::test_determinism_byte_identical`;
`tests/test_no_ai_import.py` (exists); workplan/budget arithmetic invariants
(weights sum to 100, budget line = qty×persons×times×unit) are asserted in
`tests/test_example_project.py` and exercised negatively by
`tests/test_engine.py::test_negative_budget_arithmetic_B002` and
`tests/fixtures/negative/W003/`, `B002/`.

**Acceptance (from the plan):**
- **AT-2:** a non-CLI lecturer persona works through webform → launcher →
  validate → build with AI extras absent, network off, no keys. Result:
  `submittable: true` (against the fictional profile), `real_world_verified:
  false`, `BLOCK == 0`.
- **AT-2b:** same path via the CLI.
- **AT-3a:** determinism, import-lint, and a network-off run all pass.
- **AT-4:** every BLOCK rule has a failing fixture; hypothesis arithmetic
  invariants hold.
- **AT-5:** a human cold read (by someone who did not write the example)
  passes against a named checklist (write the checklist as part of this
  deliverable, in `docs/en/quality-gates.md` and `docs/th/quality-gates.md`).
  An AI cold read may be added as an optional extra check; it is never
  required (founder ruling 2026-09-25: AI stays optional).
- **AT-6:** the independent release gate passes before any tag (see
  `GOVERNANCE.md` "Publication sequence" — a checker distinct from the
  maker plus the human founder's approval; not something to automate away).

**Do NOT, in v0.1:** build Citizen Mode, review/lock, SHACL, or any AI
feature. Do NOT let `ai_assisted_fill` default to anything but `false`.

## v0.2 — "Citizen, no AI" + review + lock

**Status of v0.2 (integration branch, 2026-09-25; not released).** Built:
form profiles, the writing layer, and review/lock/diff (`grantthai link`,
`review`, `accept-mapping`, `reject-mapping`, `lock`, `diff`, `explain
FIELD_ID`, `profiles`), plus one AI-simulated demo
(`examples/demo-seedbank/`, `docs/demo/`). **Not yet built** in v0.2
(open, founder ruling needed to defer or schedule): Citizen Mode and the
concept note, the lifecycle decision, bridge ontology and generated SHACL,
classification rules C001–C003, the rule families listed below. So AT-1 is
**not** passed; the demo is not an AT-1 run (its Gap/RQ text is simulated,
not human-authored). AT-2 extended (validate → link → review RG0–RG4 →
lock → build) is covered by `tests/test_lock.py`.

**Carried into v0.2 from the v0.1.0 audit of the design sources** (recorded
in `docs/deviations.md`):

- **Form profiles.** A `form_profile` concept in `mappings/nriis/` for the
  five proposal form types in SD-1 p47 (research, innovation, personnel
  development, system/standard, promotion activity) and for the funding
  units' own Word/PDF proposal templates uploaded to NRIIS (SD-2 p9, SD-3
  p9). v0.1 models one observed form (contradiction CX-09 covers tab count
  and order).
- **Lifecycle.** The core/04 project lifecycle (20 states, V-L01–V-L06:
  certification, contract change control, extension, progress and final
  reports, 5-year utilization reporting) as `spec/common/lifecycle.yaml`,
  or an explicit decision that it stays out of scope.
- **Writing layer.** core/02 §4A.2 compression targets, §4B section writing
  intent and micro-templates, §4E section purpose matrix and §15
  completeness checklist into `guidance/writing_intent.yaml`, referenced
  from registry `guidance`; the core/01 §30 copy/paste checklist and the
  SD-4 p166 validation page in the output contract.
- **Classification rules** C001–C003 (VAL.012) need an agreed topic → OECD
  mapping before they can be evaluated.
- Decisions on the OPEN contradictions CX-01..CX-10 (`docs/contradictions.md`).

**Files to create:** `interview/{expert.en,citizen.th,citizen.en}.yaml`,
`mappings/modes/citizen_to_core.yaml`, `templates/research_concept_note.md.j2`
(implementation), `ontology/bridge/*`, `ontology/shapes.shacl.ttl`
(generated from `spec/common/chain.yaml` — write the generator, not the
file by hand), `ontology/local_terms.yaml` (real seed entries, curator +
date per K16 once decided), `validators/crosswalk.yaml` (real aliases),
rule families CH003/E/E006-E008/U/P/G/X001-X006/ECO*,
`examples/{citizen-no-ai,citizen-with-pi-partner}/`,
`docs/{th,en}/for-citizens.md`, `docs/{th,en}/for-administrators.md`,
`src/grantthai/review/*` (`review --as --scope`, `accept-mapping`,
`reject-mapping`), `lock`/`diff` commands.

**Acceptance (AT-1, shipped material only):** starting from a written
experience account, the result is either `HOLD` + concept note (no PI) or a
submittable build (PI partner present). `BLOCK == 0` apart from `ELIG`;
`CH001`/`CH002` pass; every `Gap`/`RQ` is human-authored (citizen writes
them with guidance cards); no invented evidence; every gap marked; no
AI-authored field. **AT-2 extended:** review → lock.

**Do NOT, in v0.2:** ship any AI-assisted feature. Do NOT let a missing
review gate block `build` or the concept note — it downgrades claim
strength and adds a `hold_reason` instead (`spec/common/review_gates.yaml`).

## v0.3 — optional AI assist

**Files to create:** `src/grantthai/assist/*` (`ask`, `propose-mapping`,
`find-gaps`, `search-terms`, `draft <FIELD_ID>`), `examples/citizen-ai-assisted/`,
populate `spec/common/parity.yaml` with a tested human equivalent per AI
feature, enable `.github/workflows/parity.yml` (currently `if: false`).

**Acceptance:** **AT-3b** byte-identical build with and without the
`assist` extra installed; AI output always `PROPOSED` or `DRAFT`; rules
X002/X003 catch misuse; every AI feature has a tested human equivalent.

**Do NOT:** let anything in `assist` import into `core`/`validators`/etc.
(one-way dependency only — CI already enforces the reverse direction).

**AI-use ceiling (landed early, unreleased).** Every AI feature, in this
phase and every other, stays under `docs/policy/ai-use-ceiling.md`, built
on the GenAI guideline 2569 (`docs/sources.md`). What exists and must be
kept when `assist` is built:

- `authoring.ai_use_declaration` in `spec/project/project.schema.json`
  (tools with version, stages and purpose; influence; human verification;
  data handling; log reference; optional risk self-assessment; the
  researcher's confirmation). Every AI-assisted write goes through
  `grantthai.core.project.record_ai_tool` (called by `set_field` with
  `actor="ai_assisted"` and a `tool`), which resets the confirmation when
  tools or stages change. An `assist` command must pass its tool name and
  version the same way, and must never set `declaration_confirmed_by_human`.
- The data warning (`grantthai.core.pii.DATA_WARNING_TH/EN`) is shown
  before any data is accepted; MCP and HTTP return it on project creation.
- Rules AI001-AI004 (`validators/rules.yaml`, REVIEW only, source
  `docs/policy/ai-use-ceiling.md`; the rule schema forbids BLOCK for that
  source). AI003 uses `grantthai.core.pii`, the same patterns as the
  leak/PII guard.
- Output section 4.7 (`spec/output/nriis-submission.contract.md`): the AI
  Use Declaration, a GrantThai appendix modelled on the guideline's
  Appendix A (p.34), never an NRIIS field. Any single risk level printed is
  labelled GrantThai's convention.
- Tests: `tests/test_ai_use_ceiling.py`.

**Do NOT:** make an AI rule BLOCK while the guideline's binding status is
OPEN; present the convention risk level as the guideline's; add the
declaration to an NRIIS tab; name the guideline's drafting committee.

## v0.3 router — one work object, many routes (unreleased, landed 2026-09-25)

**Founder reframe (binding, verbatim):** "การลงใน NRIIS ไม่ใช่แกนหลักอีกต่อไป
แต่เป็นแค่ทางเลือกหนึ่งของ router เพราะเราจะเปิดให้ตั้งแต่การทำบทความวิชาการด้วย" —
entering NRIIS is no longer the core; it is one option of a router, because
GrantThai opens to academic articles as well. "Router" here means a
**deterministic output route chosen by a person**, never an AI decision
(`docs/deviations.md`, K-R1). Design record: `docs/design/PLAN.md` §N.

**What exists (files):**
- Input: `spec/work/work.schema.json` 0.3.0-draft (`work_id`, `work_type`,
  `routing`, optional `fund_binding`); a superset of `project.yaml` 0.2.
  Legacy files are read unchanged as `work_type: research_proposal`,
  `routing.default_route: nriis-proposal`. `spec/common/object-hash.md`
  excludes `routing` from `content_sha256` (K-R3).
- Router: `routes/INDEX.yaml`, `routes/nriis-proposal/route.yaml` (wraps
  the existing NRIIS assets in place, nothing moved),
  `routes/academic-article/{route,placement}.yaml` +
  `sub_profiles/{thai-journal,international-journal}.yaml` (both
  `NEEDS_VERIFICATION`, GrantThai defaults, not venue profiles),
  `routes/concept-note/{route,placement}.yaml`; schemas in
  `spec/routes/`.
- Registry: `scope` and `route_ids` on every field
  (`tools/registry/partition.py`), 24 `ARTICLE.*` fields with origin
  `VENUE_NATIVE` (K-R2), every Thai label `NEEDS_VERIFICATION`.
- Engine: `src/grantthai/routes/{registry,resolve}.py`; `core/project.py`
  (work.yaml discovery, both-present refusal, legacy view, `migrate`);
  `validators/engine.py` takes a route, evaluates only the rule families
  in the route's scope, reports out-of-scope rules as one INFO (RT002),
  runs `_fund()` only when `needs_fund_binding`; family ART (ART001–ART011,
  `validators/rules.yaml`, REVIEW except ART007 BLOCK: an AI tool listed
  as an author); renderers `render/submission.py` (untouched),
  `render/article.py`, `render/concept_note.py`, dispatched by
  `render/__init__.py::build_route`.
- Surfaces: CLI `route list|check|build`, `build --route`, `init
  --work-type`, `migrate [--rename] [--dry-run]`; `api_py.list_routes`,
  `check_route`, `build(route=)`, `migrate`, `new_work`; MCP
  `grantthai_list_routes`, `grantthai_check_route`, `route` on build and
  validate; HTTP `GET /routes`, `POST /projects/{id}/routes/{route}/check`,
  `route` on build; skill step 0 "choose the route with the researcher".
- Guards: `tools/ci/check_one_output.py` (one template and one unique
  output filename per route, contract cross-references, runtime
  one-file-per-build check on every shipped example, three seeded bad
  fixtures) and `tools/ci/check_notice.py` (NOTICE on body line 1 of every
  route template; the route notice on line 2 where declared).
- Contract: `spec/contracts/one-input-one-output.md` 0.3.0-draft, one
  output per route; the concept note is a route, not an exception.

**Route resolution (the tool never picks):** `--route`; else
`routing.default_route`; else a legacy 0.2 file → `nriis-proposal`; else
the one route in `routing.declared_routes` (several declared: exit 2
listing them); else, only when nothing is declared, the single route whose
`default_for_work_types` lists the `work_type`;
else exit 2 with the candidates (`AmbiguousRoute`; MCP and HTTP return the
list). A directory with both `work.yaml` and `project.yaml` exits 2.

**Acceptance:**
- **AT-R1** `examples/lecturer-no-ai` and `examples/demo-seedbank` build
  byte-identical `NRIIS_SUBMISSION.md` through `build`, `build --route
  nriis-proposal` and `route build`, against the golden snapshot taken
  before the change (`tests/golden/routes/`).
- **AT-R2** the fictional article example builds exactly one
  `build/ACADEMIC_ARTICLE.md` with the NOTICE on line 1, BLOCK = 0 and the
  seeded ART findings, deterministic across two runs.
- **AT-R3** one object builds `NRIIS_SUBMISSION.md` and
  `ACADEMIC_ARTICLE.md` in two invocations; each creates one file and
  leaves the other byte-identical; shared-core values are identical in
  both; editing `routing` does not change `content_sha256`.
- Every guard passes on the tree and fails on its seeded fixtures
  (`bash tools/ci/run_all_guards.sh`), run once at the end, not per edit.

**Do NOT:** let any surface default the route when the resolution is
ambiguous; name a journal, an index, a fee or a word limit anywhere (a
venue fact enters only through `ARTICLE.VENUE.TARGET` with the
researcher's source, ART010); let `manuscript_ready` read as accepted or
publishable; make any ART rule BLOCK on a journal fact; compose section
text; move the NRIIS assets under `routes/` (deferred, needs its own
decision); change the NOTICE constant (K-R6 open); reuse the word "route"
for the TOKE infrastructure advisory (that command is `advise infra`, not
built here).

**Open founder decisions:** K-R4 (file name `work.yaml` vs keep
`project.yaml`), K-R5 (output name and whether both sub-profiles ship),
K-R6 (NOTICE wording), K-R7 (next routes: thesis proposal, conference
abstract, final report; whether a dated, human-checked venue profile
should ever exist), K-R8 (router first, TOKE rebased onto it).

### v0.3 router: 7SSA structure profiles (academic-article; unreleased)

Founder request (2026-09-25): "ให้ router ใช้เทมเพลทนี้เมื่อต้องทำงานประเภทนี้" —
the router uses the 7SSA template for this kind of work. 7SSA (Seven-Section
Scholarly Architecture) comes from the founder-authored 7SSA master schema
v1.0 and the GLOSA-7SSA LaTeX template (registered in glosa). It is a third
axis of the academic-article route next to the sub-profile: how the body is
arranged, not which venue.

**Deliverables (S1 data, S2 render):**
- `routes/academic-article/profiles/`: `7ssa-world`, `7ssa-thai-7`,
  `7ssa-thai-5`, `7ssa-thai-4` and `INDEX.yaml` (sectors S1-S7, their slots
  with required/optional, the fields they read, writing order, compression
  rules A-D, eight article-type overlays);
  `spec/routes/structure_profile.schema.json`, linted by
  `tools/ci/check_schema_lint.py`.
- Registry: `ARTICLE.SSA.ARTICLE_TYPE`, `.GAP`, `.CONTRIBUTION`,
  `.BEFORE_AFTER`, `ARTICLE.STATEMENT.OTHER` (`RECOMMENDED_EXTENSION`);
  `ssa_sector` / `ssa_slot` on `ARTICLE.BODY.SECTIONS` items.
- Selection: `routing.structure_profiles` (outside `content_sha256`) or
  `--structure-profile`; the router lists candidates when `work_type` is
  `academic_article` and `ARTICLE.SSA.ARTICLE_TYPE` is one of the eight
  types (INFO RT004). Nothing ever writes the key but the researcher.
- Rules 7SSA-01..7SSA-10 (family SSA, REVIEW/INFO; the rule schema refuses a
  BLOCK from a 7SSA source), each with `tests/fixtures/negative/7SSA-NN/`;
  Thai explanations in `skills/grantthai/reference/rules-th.md`.
- Render: `templates/article_7ssa.md.j2` (a `route_partial` included by the
  article template, still one `ACADEMIC_ARTICLE.md`);
  `src/grantthai/render/ssa.py` compresses 7 -> 5 -> 4 visible sections as
  a pure function that keeps an `[S#]` marker per sector and drops no
  researcher text.
- Export: `grantthai build --route academic-article --format tex` writes
  one `build/ACADEMIC_ARTICLE.tex` from `templates/tex/glosa_7ssa_v1.tex`
  (byte-identical glosa copy, sha256 in `templates/tex/SOURCE.yaml`) through
  `templates/tex/glosa_7ssa_v1.fillmap.yaml` (212 rows, one per `[FILL`).
  English only; review and audit state is always `NEEDS_INPUT`; the
  publisher-policy cells print `NEEDS_VERIFICATION`.
- Contradictions CX-7SSA-01..12 (`docs/contradictions.md`), deviations in
  `docs/deviations.md`.

**Acceptance (`tests/test_7ssa.py`):**
- **AT-7SSA-1** `examples/article-7ssa-fictional` builds exactly one
  `ACADEMIC_ARTICLE.md` with seven `[S#]` markers, the NOTICE on line 1,
  BLOCK = 0 and no 7SSA finding, byte-identical across runs.
- **AT-7SSA-2** the same object renders as thai-7, thai-5 and thai-4 with
  the source's headings, all seven markers, byte-identical reruns, the same
  `content_sha256` and the same multiset of researcher strings (plus a
  seeded property test of the compression function).
- **AT-7SSA-3** `--format tex` writes exactly one `.tex` from the pinned
  template and compiles with `latexmk` when it is installed (otherwise the
  test is skipped with that reason).
- AT-R1/R2/R3 unchanged: with no profile selected every output is
  byte-identical to the output before 7SSA.

**Do NOT:** select a profile for the researcher; use any quartile as a gate
or readiness input; store per-sector VERIFIED status or integrity booleans;
use an AI simulation (desk reject, red team) as a review; compute the
source's word budget, contribution density or formula-like labels (none is
a registered equation); write bridging prose when merging sections; edit
the vendored LaTeX template (re-vendor and re-pin instead).

**Open founder decisions** (7SSA integration spec §4.2): K-S2 (the
eight-section world layout), K-S5 (a XeLaTeX derivative for Thai), K-S7
(glosa schema additions), K-S8 (origin `RECOMMENDED_EXTENSION` or a new
founder-standard origin).

## v0.4 — interfaces

**Status:** MCP and REST shipped early in v0.1.0 (founder scope change
2026-09-25, above). Browser-assist is still open.

**Files to create:** `src/grantthai/mcp/*` implementing
`spec/mcp/tools.schema.json`, optional `src/grantthai/api/*` (REST/OpenAPI),
browser-assist per rules A1-A8.

**Acceptance:** none of these can set status above `DRAFT` or submit
anything; UI drift sets `UI_DRIFT`; no credentials are ever stored.

## v0.5 — real fund profiles, network, labels

**Files to create:** the first real, non-fictional fund profile (dated,
human-maintained, second-checked), the Thai NRIIS label capture (within
K14's terms; v0.1.0 already carries *candidate* labels from public
documents in `mappings/nriis/labels@nrct-manual-2566.yaml` — v0.5 confirms
or replaces them against current call/TOR documents), opt-in network directories (`network/directories.schema.yaml`
populated, per K11).

**Acceptance:** every rule sourced, dated, second-checked; the staleness
job (`.github/workflows/staleness-report.yml`) opens issues rather than
silently editing anything.

## What NOT to do, at any phase

- Do not invent a Thai fund rule, agency threshold, or NRIIS label from
  training-data recall. Write `NEEDS_VERIFICATION` and cite where a real
  source would go (`docs/sources.md`).
- Do not let AI set any field above `DRAFT`, or treat an
  `ACCEPTED_BY_REQUESTER` mapping as more than `CONTRIBUTORY` evidence.
- Do not give a route a second template, share a template between routes,
  or reuse an output filename across routes — the one-input-one-output
  contract requires exactly one template and one unique output file per
  route (`tools/ci/check_one_output.py` enforces this, with three seeded
  bad fixtures).
- Do not let a tool or an AI pick the output route; the route is the
  person's declaration, and an ambiguous resolution stops with the
  candidate list.
- Do not add AI/vendor attribution anywhere outside
  `docs/lineage.md`/the README footers, and even there, never as authorship.
- Do not skip a phase's acceptance criteria to reach a later phase faster.
