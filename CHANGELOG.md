# Changelog

All notable changes to GrantThai are documented in this file. Format loosely
follows [Keep a Changelog](https://keepachangelog.com/); versions follow
SemVer from v0.1 onward.

## [Unreleased]

### Changed — the router: NRIIS is one route, not the core
- Founder reframe (2026-09-25, verbatim): "การลงใน NRIIS ไม่ใช่แกนหลักอีกต่อไป
  แต่เป็นแค่ทางเลือกหนึ่งของ router เพราะเราจะเปิดให้ตั้งแต่การทำบทความวิชาการด้วย" —
  entering NRIIS is no longer the core; it is one option of a router,
  because GrantThai opens to academic articles as well. "Router" means a
  deterministic output route chosen by a person, never by an AI; the old
  sense "AI as router" stays dropped (`docs/deviations.md`, K-R1; PLAN §N).
- `spec/contracts/one-input-one-output.md` 0.3.0-draft: one input, one
  command per route, exactly one file per route. The concept note is an
  ordinary route, no longer "the one exception". The NRIIS route's output
  is byte-identical to before (AT-R1, `tests/golden/routes/`).
- `tools/ci/check_one_output.py` is restated per route (one template and
  one unique output filename per route, contract cross-references, a
  runtime one-file-per-build check on every shipped example) with three
  seeded bad fixtures; `tools/ci/check_notice.py` checks every route
  template for the NOTICE on body line 1 and the route notice on line 2.
- The NOTICE constant is unchanged (K-R6 open). The article route adds its
  own line under it: GrantThai is not affiliated with any journal or
  publisher.
- `README.md`, `README.en.md`, `AGENTS.md`, `GRANTTHAI_STANDALONE.md`,
  `docs/ecosystem.md` (the GrantThai box shows the routes),
  `docs/BUILD_GUIDE.md` ("v0.3 router"), `docs/design/PLAN.md` §N
  (appended addendum), `llms.txt`, `llms-full.txt`, `ai.json`.

### Added — the router
- `work.yaml` 0.3 (`spec/work/work.schema.json`): `work_id`, `work_type`,
  `routing` (declared routes, default route, sub-profiles) and an optional
  `fund_binding`, required only by routes with `needs_fund_binding`. A
  superset of `project.yaml` 0.2; legacy files are read unchanged as the
  NRIIS route. `routing` is excluded from `content_sha256`
  (`spec/common/object-hash.md`, K-R3).
- `routes/`: `INDEX.yaml` and three routes — `nriis-proposal` (wraps the
  existing assets in place), `academic-article` (placement, sub-profiles
  `thai-journal` and `international-journal`, both `NEEDS_VERIFICATION`),
  `concept-note`; schemas in `spec/routes/`.
- `grantthai route list | check | build`, `build --route`, `init
  --work-type`, `migrate [--rename] [--dry-run]`; `api_py.list_routes`,
  `check_route`, `build(route=)`, `migrate`, `new_work`; MCP
  `grantthai_list_routes`, `grantthai_check_route` and a `route` argument;
  HTTP `GET /routes`, `POST /projects/{id}/routes/{route}/check`. Every
  surface returns the candidate list instead of picking when the route is
  ambiguous.
- Registry: `scope` and `route_ids` on every field
  (`tools/registry/partition.py`); the `ARTICLE.*` fields with the new
  origin `VENUE_NATIVE` (K-R2), every Thai label `NEEDS_VERIFICATION`.
- Family ART (ART001–ART011): REVIEW, except ART007 (an AI tool listed as
  an author) BLOCK. No rule rests on a journal fact; GrantThai ships no
  venue registry (ART010). Rules carry `routes:` and the engine evaluates
  only the families in the chosen route's scope (RT001/RT002 INFO).
- Review fixes: route resolution honours `routing.declared_routes` before
  the `work_type` default (several declared and no `default_route`: stop
  and list them; RT003 INFO when the route in force is not declared).
  ART007 matches a disclosed tool name in both directions (a parenthetical
  is tried on its own and removed) and, even when nothing is disclosed,
  a member full_name against generic AI-tool name patterns
  (`validators/ai_tool_name_patterns.yaml`, no product names). Route data
  files now validate against their schemas and the schema-lint guard
  checks them; the FICTIONAL banner rests on an explicit `fictional: true`
  key; the concept-note route evaluates the S family so its
  `required_fields` are checked (`docs/deviations.md`).
- `build/ACADEMIC_ARTICLE.md` (`spec/output/academic-article.contract.md`,
  `templates/academic_article.md.j2`, `render/article.py`) and
  `build/RESEARCH_CONCEPT_NOTE.md` as a route
  (`spec/output/research-concept-note.contract.md`, `render/concept_note.py`);
  fictional examples `examples/article-fictional/` and
  `examples/both-routes-fictional/` (no real journal named).

### Removed — the router
- Nothing. 0.2 files are read unchanged; `build --concept-note` (never
  implemented) is superseded by the `concept-note` route.

### Added — the AI-use ceiling (GenAI guideline 2569)
- `docs/policy/ai-use-ceiling.md` and `docs/policy/ai-use-ceiling.th.md`:
  the most any AI may do in GrantThai, each line citing the page of the
  National Research Council of Thailand's GenAI guideline for researchers
  (September 2569) and the force of its Thai wording; stage-by-stage limits,
  disclosure, accountability, data rules, record keeping, where GrantThai is
  stricter, human duties GrantThai cannot check, a crosswalk of every
  normative point (N01-N58), and the glosa P20/P06/P10 comparison. The
  guideline is guidance; its binding status is OPEN. `docs/sources.md`
  records it (public URL `NEEDS_VERIFICATION`).
- `authoring.ai_use_declaration` in `project.yaml`, following the sample
  form in the guideline's Appendix A (p.34). Every AI-assisted write
  (`grantthai set --ai`, MCP `grantthai_set_field`, HTTP field writes, the
  skill's `apply`) records the tool, its version and the stage; new options
  `--tool-version` / `--stage`, `tool_version` / `stage`. Adding a tool or
  stage resets `declaration_confirmed_by_human`, which only the researcher
  sets.
- Rules AI001 (declaration missing, incomplete or unconfirmed), AI002
  (AI-drafted data or evidence record; extends X003), AI003
  (personal-data-shaped string in an AI-assisted value) and AI004
  (self-assessed risk of 3; the single level is labelled GrantThai's
  convention, since the guideline gives no rule for combining its five
  example scores). Family AI, REVIEW only; Thai explanations in
  `skills/grantthai/reference/rules-th.md`.
- Output section 4.7, the AI Use Declaration: a GrantThai appendix, never
  an NRIIS field (whether a call asks for one is `NEEDS_VERIFICATION`).
  Frontmatter `authoring.ai_use_declaration`: `none`, `unconfirmed` or
  `confirmed_by_researcher`. Renderer `nriis_submission.md.j2@0.3.0`,
  output contract 0.4.0-draft.
- The personal/confidential-data warning (guideline p.14-16), shown before
  any data is accepted: `grantthai_skill.py warning`, `data_warning` in the
  MCP `grantthai_new_project` result and the HTTP `POST /projects`
  response. The skill keeps team members' personal data out of a public AI
  chat and stops drafting a dual-use topic.
- `src/grantthai/core/pii.py`: one set of personal-data patterns, shared by
  the validator (AI003) and the leak/PII guard.
- `tests/test_ai_use_ceiling.py`.

### Changed — the AI-use ceiling
- The worked example's golden output is re-pinned: renderer version, one
  frontmatter line and section 4.7 ("no AI use recorded") are the only
  changes.
- The fictional demo gains an AI Use Declaration for its simulated persona
  and now shows **REVIEW 3** (FW001, and AI001 twice: no human verification
  yet, not confirmed). `examples/demo-seedbank/NRIIS_SUBMISSION.md` is
  rebuilt with `--as-of 2026-09-25`.

### Added — practice shared by funded work
- `docs/practice/funded-work-patterns.md` (English) and
  `docs/practice/funded-work-patterns.th.md` (Thai): what the 100 funded
  final reports share, with tiers fixed in advance (CORE: at least 70/100
  and at least 50% in each source; CONTEXTUAL: 40–69% or concentrated in
  one source; EMERGING: under 40% but rising across year bands), an
  evidence table of 37 patterns, a close reading of 8 stratified documents
  (cited by corpus id and PDF page), and limits. Six proposal-relevant
  patterns are CORE: background, objectives section, numbered objectives,
  method section, objectives with method, and a reference list.
- `tools/corpus/practice_stats.py`: recomputes the evidence table from
  `docs/demo/corpus-100.csv` alone.
- Rules FW001 (theory or foundations filled, reference list empty; 78/100)
  and FW002 (two or more objectives, objectives narrative not numbered;
  77/100), family FW, REVIEW only. The rule schema allows the source
  `docs/practice/funded-work-patterns.md` and forbids BLOCK for it. This
  implements the rule the corpus key finding below had only proposed.
- `guidance/writing_intent.yaml`: a `practice:` list on 25 fields (32
  entries: pattern id, evidence count, tier, context, advice in English and
  Thai, what not to do, deep-read pages); schema updated. The Thai advice is
  the only filled Thai text in that file, and it sits next to its evidence.
- Skill: `SKILL.md`, `reference/interview.md` (section 3a),
  `reference/writing.md` and `reference/rules-th.md` ask for and explain
  these patterns.
- `tests/test_practice_patterns.py`: negative tests for FW001 and FW002,
  and a check that every count and tier matches the CSV.

### Changed
- The fictional demo now shows **REVIEW 1** (FW001: its theory box has
  content, its reference list is empty). The demo is left unchanged so the
  finding stays visible; `examples/demo-seedbank/NRIIS_SUBMISSION.md` is
  rebuilt with `--as-of 2026-09-25`.
- `docs/demo/comparison.md`: a dated note (2026-09-25) that the e-Library's
  own download path requires a login, that R1, R3 and R4 were reached
  through direct file URLs that may bypass that gate, that the corpus-100
  work therefore excluded the e-Library, and that R1, R3 and R4 stay cited
  by public title and contract only, with no further use pending the
  founder's decision.

### Added — funded-document corpus (n=100)
- `docs/demo/corpus-100.md` (English) and `docs/demo/corpus-100.th.md`
  (Thai): 100 funded Thai research documents that anyone can download
  without an account (83 from the Health Systems Research Institute
  repository, 17 from the Prince of Songkla University repository),
  compared with the fictional demo and the field registry: method, sources
  and terms, metadata for every document, section frequencies, a close
  reading of 8 documents, 14 ranked improvements, and limitations. No
  document text is reproduced and no PDF is committed.
- `docs/demo/corpus-100.csv`: metadata (as each repository records it),
  sha256, page count and structural flags per document.
- `tools/corpus/corpus_extract.py`: the structural extractor (`extract`,
  local PDFs only, never downloads), plus `publish` (builds the CSV) and
  `stats` (recomputes every number in the corpus documents from the CSV).
- Key finding: the demo passes with BLOCK 0 / REVIEW 0 although its
  required theory box cites nothing and its references box is empty; 78% of
  the funded reports have a reference list. The proposed rule is listed,
  not implemented.
- The national research funding agency's e-Library was not used: its own
  download link requires a login. 53 of its records are set aside pending a
  founder decision.

## [0.2.0] — 2026-09-25

Founder scope 2026-09-25: build v0.2, make our own fictional demo proposal
end to end, and compare it with real, funded, publicly available research
reports. Not released; the founder approves any release.

### Added — writing layer
- `guidance/writing_intent.yaml` (`spec/guidance/writing_intent.schema.json`):
  purpose, micro-template, length target with a cited basis, keep-out list
  and quality traits for 76 fields; completeness checklist WC01–WC14.
- Rules W101/W102 (length above/below target), REVIEW only, evaluated on
  every field with a length target. `grantthai explain FIELD_ID`.
- Output section 4.6 "Completeness checklist".
- Sources: core/01, core/02 and SD-4 are not in the public repo, so targets
  citing them are relayed and `NEEDS_VERIFICATION`. The summary cap (at most
  3000 words) and keyword cap (at most 5) were read on SD-5 p3.

### Added — form profiles
- `form_profile` (optional, top level, null = observed form) in
  `project.yaml`; 8 profiles in `mappings/nriis/form_profiles/`
  (`spec/mappings/form_profile.schema.json`), all `NEEDS_VERIFICATION`.
- S001 reads the profile's required set; an unknown profile is a SCHEMA
  BLOCK, never ignored. `grantthai profiles`.
- Output: `form_profile` frontmatter key; subsection 1.8 lists unmapped
  profile items and candidate budget rules (listed, never evaluated).
- New public source SD-5 (FF full-proposal form, 2570 cycle) in
  `docs/sources.md`. Two relayed readings were corrected against its page
  text: the p1 "work being built on" block (prior work, TRL/SRL) applies
  only when focus area 6 is chosen, so it is not required; the p9 20
  percent equipment cap applies to the budget-receiving unit, not to a
  single project. CX-09 gains SD-5's four-part reading; it stays OPEN.

### Added — review, lock and diff
- `grantthai link | review | accept-mapping | reject-mapping | lock | diff`
  (local CLI only; MCP and REST cannot reach them). Named review records
  per gate RG0–RG4 bound to `content_sha256`; self review renders
  AUTHOR_CHECKED; the object LOCK breaks on any authored edit.
- A missing or stale gate never blocks `build`; it adds a hold reason
  (frontmatter `hold_reasons` and section 1).

### Added — demo and comparison
- `examples/demo-seedbank/` (FICTIONAL): an AI-simulated researcher
  interview (`docs/demo/transcript-seedbank.md`, turns T01–T21) run through
  the skill end to end with form profile `ff_full_proposal@nriis-2570`:
  BLOCK 0, REVIEW 0; no value `SOURCE`, nothing above `DRAFT`, every value
  cites its transcript turn. Not an AT-1 pass.
- `docs/demo/comparison.md`: sources R0–R4 (title, first author, contract
  or handle, sha256; no PDF committed), a structural matrix against the
  public FF form and three funded final reports, the D1–D11 rubric, an
  empty score sheet for two independent scorers (the maker does not score),
  and gaps G1–G12 as v0.3 candidates. Licence and terms of R1–R4 are
  relayed and still `OPEN` (to be re-checked by a person before any push);
  R4 is withdrawn as the D7 anchor.
- `docs/demo/scored-reading-draft.md` and `.th.md`: one non-blind AI
  reading with D1–D11 scores (`DRAFT`, not the blind scores). Funded works
  are named only in `comparison.md`'s source table; no score is given from
  a failed search (`OPEN`), and lessons are stated as structure, not as
  flaws of a named work.
- CI guard `tools/ci/check_case_collision.py` (in `run_all_guards.sh`):
  fails when two tracked paths differ only by letter case; its bad fixture
  is generated at run time.
- Skill: answers may carry `markers` (`NEEDS_VERIFICATION`,
  `HOLD_FOR_VERIFICATION`) next to a supplied value, and
  `project.form_profile`; plain-Thai explanations for W101/W102; the
  interview guide now gives the id prefixes for partners, users, outcomes,
  impacts, beneficiaries and outcome process.
- `tests/test_demo.py`.

### Changed — v0.2 fixes
- Package version `0.2.0.dev0` (the frontmatter no longer says 0.1.0 next
  to renderer 0.2.0).
- A build bound to a FICTIONAL fund profile prints a FICTIONAL banner right
  after the notice line and "Submittable to a real call: n/a (fictional
  call)"; the frontmatter `submittable` boolean is unchanged.
- Worksheet section 1.5 gives separate advice for `ai_draft` (rewrite and
  set human, or adopt as `human_ai_assisted`) and `human_ai_assisted`
  (confirm; no relabelling to human). Golden hash in
  `tests/test_form_profiles.py` re-pinned once for these three changes.

### Changed
- Renderer `nriis_submission.md.j2@0.2.0`. The example build
  (`examples/lecturer-no-ai`) is no longer byte-identical to v0.1.0: it
  now carries `form_profile: null`, five gate hold reasons, 11 W102 REVIEW
  findings (the example is deliberately terse) and the checklist. The
  golden hash in `tests/test_form_profiles.py` was re-pinned for this
  deliberate change. `tests/test_engine.py` now allows REVIEW findings on
  the example only from W101/W102.
- INFO lines for catalog rules not evaluated now say "not yet implemented
  in this build" instead of "not evaluated by v0.1".

### Not in this build (OPEN)
- Citizen Mode, concept note, lifecycle, bridge ontology/SHACL, C001–C003
  and the other v0.2 rule families. AT-1 is not passed.

## [0.1.0] — 2026-09-25

Scope set by the founder on 2026-09-25: "เอาแค่ สกิล mcp และ api ที่นักวิจัยใช้เอไอ ดึงไปใช้สร้างไฟล์สำหรับวางภาพรวมได้" ("only the skill, MCP
and API that a researcher's AI can pull in to create the overview file").
The offline web form, launchers, Citizen Mode, review/lock and SHACL are
deferred. See `docs/BUILD_GUIDE.md` and `GOVERNANCE.md`.

### Added — answering the real forms (audit of the design sources, 2026-09-25)

An audit compared the Phase 0 repository with the original handoff package
and the public source documents. Applied before release:

- **Origin per field** (core/02 §2): `origin` + `origin_basis` on every
  registry record; only `NRIIS_NATIVE` fields get an `NRIIS.*` record
  (100 -> 69 at that step; 82 of 122 after the new fields). Research core and
  methodology are `AUTHORING_CORE` and appear in the output appendix with
  the narrative box they feed (`render_from`); the methodology is no longer
  rendered twice. The output's `ORIGIN` column is the registry origin;
  `PROVENANCE` is a separate line. ProposalMeta and Audit are `not_on_tab`.
- **Contradiction register**: `registry/contradictions.yaml` and
  `docs/contradictions.md` (CX-01..CX-10, all OPEN, both readings kept);
  `conflicts` on registry records and on project field records; a defined
  "Conflicts and open contradictions" output section (replacing the
  undefined "conflict log").
- **22 new fields** (100 -> 122), each `NEEDS_VERIFICATION`; public-document
  fields carry `source_status: PUBLIC_DOCUMENT` and `source_document`
  (document id, edition, PDF pages): programme name, sub-projects, past
  performance of a continuing project, ISCED broad/narrow/detailed,
  references, IP check, project risks, entrepreneur information,
  sustainability, team expertise and ongoing projects, team credentials,
  project-lead track record and management experience (fund-profile
  origin), primary/secondary policy pathway, fund objective/KR selection,
  one-sentence alignment statement, theoretical foundations,
  propositions, boundary conditions.
- **Structure**: Need/Problem/Gap/Innovation accept text or core/02
  objects; outputs `kr_ids` + `kr_role`; outcomes `kr_ids` (the chain's
  Outcome -> KR edge) and `outcome_type`; impacts `impact_type`,
  `claim_strength`, `sign`, `directness`, `intended`; partners
  `in_kind_basis`.
- **Rules** (60 -> 72): S009, S010, S011, R008, R009, W005, B007, E009,
  F005 evaluated in v0.1 (REVIEW); C001-C003 classification (v0.2, INFO).
  `validators/crosswalk.yaml` maps all 37 core/02, 41 core/04 and 12
  core/05 validation codes.
- **Candidate options**: "Continuing Project" for the project
  characteristic and the OECD main/sub code lists, accepted with a REVIEW
  finding (S011), never a BLOCK.
- **Candidate Thai labels**: `mappings/nriis/labels@nrct-manual-2566.yaml`
  (field and part labels, OECD lists, budget categories, output/outcome/
  impact typologies), each cited to a public document and PDF page, all
  `NEEDS_VERIFICATION`, shown in the output tagged "candidate"; nothing
  from the screenshot-derived readout (K14).
- `docs/sources.md` records the four excluded public documents as SD-1..SD-4
  (title, issuer and edition as printed on them).
- `ecosystem/positions@2026-09.yaml`: the six core/02 policy lenses and
  eleven ecosystem positions, RELAYED.
- `list_fields` (CLI, Python API, MCP, HTTP) now lists every field: NRIIS
  boxes first, then fields with tab `NOT_ON_TAB`, each with its `origin`.
- Deferred to v0.2 and recorded in `docs/deviations.md`: form profiles for
  the five proposal form types and funding-unit templates, the project
  lifecycle (V-L01-V-L06), the writing layer (core/02 §4A.2, §4B, §4E, §15;
  core/01 §30 checklist).

### Added — AI-facing surfaces (thin wrappers over `grantthai.api_py`)

- `skills/grantthai/`: agent skill (`SKILL.md`, Thai/English interview,
  provenance rules, `answers.yaml` format, Thai rule explanations, a
  prompt packet for chat-only AIs, helper script `grantthai_skill.py`
  with `check`/`apply`/`report`) and `docs/use-with-ai.md`,
  `docs/th/use-with-ai.th.md`.
- `src/grantthai/mcp/`: stdio MCP server `grantthai-mcp` (official SDK
  when installed, built-in JSON-RPC fallback otherwise); six tools and two
  resources; every value written is AI-assisted, capped at `DRAFT`, never
  `SOURCE`. `spec/mcp/tools.schema.json` updated to the built tools;
  `docs/mcp.md`.
- `src/grantthai/api/`: local HTTP API `grantthai-api` (standard-library
  WSGI, binds 127.0.0.1 unless `--allow-remote`), OpenAPI 3.1 at
  `spec/api/openapi.yaml`, `docs/api.md`. Like MCP, every value written
  over HTTP is AI-assisted (`ai_draft`/`INFERENCE`, or
  `human_ai_assisted`/`DECISION` with `researcher_verbatim`), capped at
  `DRAFT`, never `SOURCE`; `actor: human` is refused.
- `pyproject.toml`: extras `mcp`, `api`, `skill`, `all`; console scripts
  `grantthai-mcp`, `grantthai-api`.
- `spec/common/parity.yaml`: one entry per MCP tool / API endpoint / skill,
  each naming its tested human CLI equivalent.
- Tests: `skills/grantthai/scripts/test_grantthai_skill.py`,
  `tests/mcp/`, `tests/api/`.

### Added — engine

- `src/grantthai/core/project.py`: load/save `project.yaml`, schema
  validation through a local `$id` registry of `spec/**/*.schema.json`
  (never fetches a URL), `new_project`, `set_field` under the status hard
  ceiling (never above `DRAFT`; an AI draft is `ai_draft`/`INFERENCE`, never
  `SOURCE`).
- `src/grantthai/validators/engine.py`: report-only validator for the v0.1
  rule families (S, R, W, B, T, CH, F, ELIG); every other catalog rule is
  reported as an explicit INFO "not evaluated" finding (B003, B004, F004 and
  all v0.2 rules). X003 (an AI draft marked `SOURCE`) ships early, checked
  on every record, so a hand- or chat-written `project.yaml` cannot bypass
  the core guard. A status above `DRAFT` typed into `project.yaml` renders
  as self-declared and not backed by any check.
- `src/grantthai/render/submission.py` + `templates/nriis_submission.md.j2`:
  renders exactly one `build/NRIIS_SUBMISSION.md` per the output contract;
  deterministic (byte-identical for the same input and `--as-of` date).
- `src/grantthai/api_py.py`: `new_project`, `set_field`, `validate`,
  `build`, `explain`, `list_fields` — the one surface the skill, MCP server
  and HTTP API wrap.
- CLI `grantthai` (`init`, `set`, `validate`, `explain`, `build`, `fields`).
- `tests/test_engine.py`: end-to-end, determinism, negative cases, hard
  ceiling.

## [0.0.0] — Phase 0

### Added

- Repository tree skeleton (`spec/`, `docs/`, `src/grantthai/`, `funds/`,
  `tests/`, etc.).
- `.githooks/commit-msg` attribution guard, installed as commit #1.
- Governance and policy documents: `GOVERNANCE.md`, `NOTICE`, `PRIVACY.md`,
  `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `CITATION.cff`.
- Licensing: `LICENSE` (Apache-2.0), `LICENSES/` (Apache-2.0, CC BY 4.0
  texts), `REUSE.toml` (founder ruling K13).
- Data-contract drafts (structure only): `spec/common/*.yaml`,
  `spec/profile/`, `spec/project/`, `spec/fund/`, `spec/nriis/`,
  `spec/mcp/tools.schema.json` (contract only), `spec/output/`,
  `spec/contracts/one-input-one-output.md`.
- CI guards with seeded bad fixtures: no-AI-import, no-hardcoded-rules,
  leak/PII scan (maintainer-specific terms loaded from an untracked local
  file), attribution scan, gitleaks, REUSE lint, schema lint with instance
  validation, one-input-one-output, NOTICE constant. The leak/PII and
  gitleaks bad fixtures are generated at test run time.
- Field registry `registry/fields.jsonl` (100 fields derived from the
  handoff package core/05; every Thai label `NEEDS_VERIFICATION`), the
  generated `registry/nriis-fields.jsonl`, `mappings/nriis/section_to_tab.yaml`
  (`NEEDS_VERIFICATION`), and the rule catalog `validators/rules.yaml`
  (56 rules at first, 60 after the additions below), each with its schema.
- `docs/design/PLAN.md` (the founder's design plan, historical record) and
  the founder decisions log in `GOVERNANCE.md` (K1, K13, K14 ruled).
- `docs/sources.md`, `docs/deviations.md`, `docs/lineage.md`,
  `docs/ecosystem.md`, `docs/BUILD_GUIDE.md`.
- `AGENTS.md` (with `CLAUDE.md`/`GEMINI.md` pointers) as the binding entry
  point for any AI builder.
- `ai.json`, `llms.txt`, `llms-full.txt` discovery files (flags ADVISORY).
- `GRANTTHAI_STANDALONE.md` system/architecture guide.

### Added — cold-start contract fixes (round-2 independent review)

- `spec/registry/structured_fields.schema.json`: a machine value contract
  for every registry field of type `array<object>`, `object` or
  `rich_text|object` (46 fields), with key names derived from the handoff
  package core/02 (renames recorded per field and in `docs/deviations.md`),
  per-item ids (`x-grantthai-node`) and annotated references
  (`x-grantthai-ref`). `spec/registry/types.yaml` states the value
  semantics of every registry `type`; `field.schema.json` now enums `type`.
- `spec/common/links-and-sources.md`: the link model (nodes, reference
  resolution, how `project:chain_edges` is derived, causal vs feedback
  edges) and what a resolvable source reference is (offline only).
  `spec/common/source.schema.json` and a top-level `sources` list in
  `project.yaml`; `links` and a `source_ids` pattern on field records.
- Rules: S006 (unresolved reference), S007 (duplicate node id), S008
  (unresolvable source), T002 (exactly one PI); R001–R007, W001–W004,
  B001–B002, T001, CH001, ELIG001, S002 and S004 restated in terms of the
  new keys and `project:chain_edges` (60 rules).
- `spec/common/object-hash.md` v0.2: two hashes. `content_sha256` excludes
  statuses, review records, the lock and mapping acceptance, so a review
  record stays current when it takes effect; `state_sha256` covers the
  whole file. Review records carry `content_sha256`, the lock
  `locked_content_sha256`; output frontmatter and validation reports carry
  both hashes. Reference implementation `src/grantthai/core/object_hash.py`
  (checked against an independent RFC 8785 implementation), golden vectors
  in `tests/golden/object-hash/`.
- `spec/common/status.yaml`: precise `STRUCTURE_CHECKED` and `LOGIC_LINKED`
  criteria, including fields that no link rule reads.
- Output contract: structured fields render as tables; the appendix is
  gate records, source manifest and unresolved references (the undefined
  "conflict log" is removed); the output path is `<dir of project.yaml>/build/`.
- `examples/lecturer-no-ai/project.yaml`: a fully populated FICTIONAL
  worked example; `tests/test_example_project.py` recomputes the v0.1
  link, sum, budget, source and DAG rules on it from the contracts alone.
- `tools/ci/check_schema_lint.py` now enforces the structured-field
  contracts and checks project instances for placement, structured values,
  reference and source resolution, duplicate ids, causal cycles and stale
  review records, with a seeded bad fixture
  (`tests/fixtures/negative/schema_instance/examples/badlinks/`).
- Registry: the `CORE.RESEARCH.INNOVATION` descriptive label is now
  "Innovation / What Is New".

No CLI, renderer, or web-form logic ships in Phase 0. See `docs/deviations.md`
for departures from the original handoff package and `docs/design/PLAN.md`
§I for the full phased roadmap.
