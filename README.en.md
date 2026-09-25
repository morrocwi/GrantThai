# GrantThai

**One work object, many routes: academic article, research proposal
(NRIIS), concept note.** One `work.yaml` in; you choose the route; exactly
one file out per route (`build/ACADEMIC_ARTICLE.md`,
`build/NRIIS_SUBMISSION.md` or `build/RESEARCH_CONCEPT_NOTE.md`). Entering
NRIIS is no longer the core of GrantThai but one route of a **router** — a
deterministic output route chosen by a person, never by an AI (founder
reframe, 2026-09-25). GrantThai is not affiliated with any journal or
publisher and ships no venue registry; every journal fact is
`NEEDS_VERIFICATION` unless you supply the venue's own document.

**Status: v0.1.0 (not yet released to a package index); the v0.3 router is
unreleased (`CHANGELOG.md`).** The engine works through the `grantthai`
command, a Python API, an agent **skill**, an **MCP** server and
a local **HTTP API**. A legacy `project.yaml` is read unchanged as the
NRIIS route. The offline web form, the launchers and Citizen Mode
are deferred (founder scope, 2026-09-25; see `docs/BUILD_GUIDE.md`). Every
Thai label and NRIIS tab name is still `NEEDS_VERIFICATION`.

> GrantThai is an independent, unofficial project. It is NOT affiliated with, endorsed by, sponsored by, or officially connected to NRCT, TSRI, any PMU, or NRIIS. / GrantThai เป็นโครงการอิสระ ไม่เป็นทางการ และไม่ผูกพันกับ วช. สกสว. หน่วยบริหารจัดการทุน (PMU) ใด ๆ หรือระบบ NRIIS
>
> See [`NOTICE`](./NOTICE) for the full statement, which applies everywhere
> in this repository.

---

## Use GrantThai with your AI: Skill / MCP / API

Your own information is the source. The AI only interviews you and writes
drafts; it never validates knowledge, never marks its own wording as
`SOURCE`, and never invents a Thai fund or NRIIS fact (those stay
`NEEDS_VERIFICATION`). It lists the routes and asks you which one to build;
it never chooses a route. Every value it writes stays `DRAFT` and is listed
in the output for you to confirm. Works with any AI vendor or a local model.
Install once: `pip install -e ".[mcp]"` from a copy of this repository.

**1. Skill** (Claude Code, Codex/`AGENTS.md` readers, Gemini CLI, or any
chat AI via `skills/grantthai/reference/PROMPT_PACKET.md`):
```
cp -r skills/grantthai ~/.claude/skills/grantthai   # or point AGENTS.md / GEMINI.md at SKILL.md
grantthai init project.yaml --project-id MY-PROJECT-001
python skills/grantthai/scripts/grantthai_skill.py report --project project.yaml
```
Details: [`docs/use-with-ai.md`](./docs/use-with-ai.md).

**2. MCP server** (stdio; six tools, each capped at `DRAFT`):
```
grantthai-mcp --root /path/to/proposal
# .mcp.json: {"mcpServers":{"grantthai":{"command":"grantthai-mcp","args":["--root","."]}}}
```
Details: [`docs/mcp.md`](./docs/mcp.md).

**3. HTTP API** (local, 127.0.0.1 only by default; OpenAPI 3.1 in
`spec/api/openapi.yaml`):
```
grantthai-api --port 8765
curl -s -X POST 127.0.0.1:8765/projects -d '{"project_id":"my-grant"}'
curl -s -X POST 127.0.0.1:8765/projects/my-grant/build > NRIIS_SUBMISSION.md
```
Details: [`docs/api.md`](./docs/api.md).

**AI-use ceiling.** Every surface works under
[`docs/policy/ai-use-ceiling.md`](./docs/policy/ai-use-ceiling.md) (Thai:
[`ai-use-ceiling.th.md`](./docs/policy/ai-use-ceiling.th.md)), built on the
National Research Council of Thailand's GenAI guideline for researchers
(September 2569; guidance, binding status OPEN; `docs/sources.md`). Before
any data is accepted, the AI shows a personal/confidential-data warning.
Each AI-assisted write records the tool and version in
`authoring.ai_use_declaration`, which the output renders as section 4.7, an
AI Use Declaration (a GrantThai appendix, not an NRIIS field) that only the
researcher confirms. Rules AI001-AI004 are REVIEW only.

## ใช้ GrantThai กับ AI ของคุณ: Skill / MCP / API

ข้อมูลของนักวิจัยเองคือแหล่งที่มา AI ทำหน้าที่สัมภาษณ์และร่างข้อความเท่านั้น
ไม่รับรองความรู้ ไม่ติดป้าย `SOURCE` ให้ข้อความที่ตัวเองเขียน และไม่แต่งข้อเท็จจริง
เรื่องทุนหรือ NRIIS ขึ้นเอง (ส่วนนั้นคงเป็น `NEEDS_VERIFICATION`) ทุกค่าที่ AI เขียนมีสถานะไม่เกิน
`DRAFT` และถูกระบุในไฟล์ผลลัพธ์ให้นักวิจัยยืนยันเอง ใช้ได้กับ AI ทุกค่ายหรือโมเดลในเครื่อง
ติดตั้งครั้งเดียว: `pip install -e ".[mcp]"` จากสำเนาของโครงการนี้

1. **Skill** — คัดลอก `skills/grantthai` ไปไว้ในโฟลเดอร์สกิลของ AI (หรือให้ `AGENTS.md` /
   `GEMINI.md` ชี้ไปที่ `SKILL.md`) ถ้าใช้ AI แบบแชตอย่างเดียว ให้วาง
   `skills/grantthai/reference/PROMPT_PACKET.md` ลงในแชต ดู [`docs/th/use-with-ai.th.md`](./docs/th/use-with-ai.th.md)
2. **MCP** — `grantthai-mcp --root /path/to/proposal` แล้วเพิ่มในค่าตั้ง MCP ของโปรแกรม AI
   ดู [`docs/mcp.md`](./docs/mcp.md)
3. **HTTP API** — `grantthai-api` (ฟังเฉพาะ 127.0.0.1) แล้วเรียก `POST /projects`,
   `PATCH /projects/{id}/fields`, `POST /projects/{id}/build` ดู [`docs/api.md`](./docs/api.md)

ทั้งสามทางได้ไฟล์เดียวกันต่อหนึ่งเส้นทางที่คุณเลือก (`build/ACADEMIC_ARTICLE.md`,
`build/NRIIS_SUBMISSION.md` หรือ `build/RESEARCH_CONCEPT_NOTE.md`) AI บอกได้ว่ามีเส้นทางอะไรบ้าง
แต่คุณเป็นผู้เลือกเส้นทาง ตรวจ ตัดสินใจ และส่งเองเสมอ

ทุกช่องทางอยู่ใต้ [เพดานการใช้ AI](./docs/policy/ai-use-ceiling.th.md) ซึ่งอิงแนวทางการใช้ GenAI
อย่างมีจริยธรรมสำหรับนักวิจัยของสำนักงานการวิจัยแห่งชาติ (กันยายน 2569) ก่อนรับข้อมูล AI ต้องแสดงคำเตือนเรื่องข้อมูลส่วนบุคคลและข้อมูลลับ
ชื่อและเวอร์ชันของเครื่องมือ AI ถูกบันทึกในแบบแจ้งการใช้ AI (หัวข้อ 4.7 ของไฟล์ผลลัพธ์ เป็นภาคผนวกของ GrantThai
ไม่ใช่ช่องของ NRIIS) และนักวิจัยเท่านั้นเป็นผู้ยืนยันแบบแจ้งนี้

---

## Quickstart 1: a lecturer with no AI, no account, no internet (the web form and launchers are deferred)

This is deliberately the **first thing** in this README, because GrantThai's
first principle is that every core task must be doable by a human alone.
**Caveat:** the `grantthai` command works today (steps 3–5). The web form
(steps 1–2) is still a placeholder without an Export button and the
launchers only print a message; both are deferred. Use a text editor or
`grantthai init` + `grantthai set` to write `project.yaml` meanwhile.

1. Open `webform/index.html` in any browser (double-click it — it needs no
   server and no network connection). Fill in the fields.
2. Click "Export" to save a `project.yaml` file to your computer.
   (Prefer a text editor or the CLI? See `forms/*.md` or
   `grantthai fill --interactive` — same result, same file.)
3. Run the platform launcher for your OS in `launchers/` (or, from a
   terminal: `grantthai validate project.yaml` then
   `grantthai build project.yaml`).
4. Open `build/NRIIS_SUBMISSION.md` (a `project.yaml` builds the NRIIS
   route by default; pass `--route academic-article` or `--route
   concept-note` to build another route from the same object). It is one
   file: a readiness summary at the top (anything still missing, in plain
   language) followed by every field, grouped by NRIIS tab, ready to copy
   and paste. The tab names and
   their order follow one observed form and are `NEEDS_VERIFICATION`. For
   the attachments tab, the file lists which documents are needed and their
   status; you upload your own files.
5. You decide what to submit, and you submit it yourself. GrantThai never
   submits anything on your behalf.

No AI model is required at any step above. No internet connection is
required after you have downloaded the repository once.

## Quickstart (คำแนะนำฉบับย่อ): อาจารย์ที่ไม่ใช้ AI ไม่ต้องมีบัญชี ไม่ต้องต่อเน็ต (แบบฟอร์มเว็บและ launcher ยังเลื่อนออกไป)

นี่คือหัวข้อแรกโดยตั้งใจ เพราะหลักการข้อแรกของ GrantThai คือ ทุกงานหลักต้องทำเองได้
โดยมนุษย์ล้วน ไม่ต้องพึ่ง AI
**ข้อควรทราบ:** คำสั่ง `grantthai` ใช้งานได้แล้ว (ขั้นที่ 3–5) แต่แบบฟอร์มเว็บ (ขั้นที่ 1–2)
ยังเป็นหน้าตัวอย่างที่ไม่มีปุ่ม Export และ launcher แค่แสดงข้อความ ทั้งสองส่วนเลื่อนออกไปก่อน
ระหว่างนี้ใช้โปรแกรมแก้ไขข้อความ หรือ `grantthai init` กับ `grantthai set` เขียน `project.yaml`

1. (เป้าหมาย v0.1) เปิดไฟล์ `webform/index.html` ด้วยเบราว์เซอร์ใดก็ได้ (ดับเบิลคลิกได้เลย
   ไม่ต้องมีเซิร์ฟเวอร์หรืออินเทอร์เน็ต) แล้วกรอกข้อมูล
2. กด "Export" เพื่อบันทึกไฟล์ `project.yaml` ลงเครื่อง (จะใช้โปรแกรมแก้ไขข้อความ
   หรือคำสั่ง `grantthai fill --interactive` แทนก็ได้ ผลลัพธ์เป็นไฟล์เดียวกัน)
3. รันตัวเปิดโปรแกรม (launcher) สำหรับระบบปฏิบัติการของคุณใน `launchers/`
   (หรือใช้เทอร์มินัล: `grantthai validate project.yaml` แล้ว `grantthai build project.yaml`)
4. เปิดไฟล์ `build/NRIIS_SUBMISSION.md` เป็นไฟล์เดียว มีสรุปความพร้อม (สิ่งที่ยังขาด
   อธิบายด้วยภาษาที่เข้าใจง่าย) อยู่ด้านบนสุด ตามด้วยทุกฟิลด์จัดกลุ่มตามแท็บของ NRIIS
   พร้อมคัดลอกไปวาง ชื่อแท็บและลำดับแท็บอ้างอิงจากแบบฟอร์มที่สังเกตได้เพียงแบบเดียว
   จึงยังต้องตรวจสอบ (NEEDS_VERIFICATION) ส่วนแท็บเอกสารแนบ ไฟล์จะบอกว่าต้องแนบเอกสารใด
   และสถานะเป็นอย่างไร ผู้ใช้อัปโหลดไฟล์ของตนเอง
5. คุณเป็นผู้ตัดสินใจและส่งเองเสมอ GrantThai ไม่ส่งข้อมูลแทนคุณ

ทุกขั้นตอนข้างต้นไม่ต้องใช้โมเดล AI เลย และไม่ต้องต่ออินเทอร์เน็ตหลังดาวน์โหลดโครงการแล้ว

---

## Philosophy

1. "GrantThai lowers the entry barrier to research, not the standard of research."
2. "Toledo connects lived experience with academic knowledge through
   translation — by people, and optionally with AI assistance — while
   evidence, methodology, and human expertise remain the gates to
   verifiable knowledge."
   *(Sentence 2 wording: founder ruling K1, 2026-09-25; see
   `GOVERNANCE.md`, "Founder decisions log". Translation may always be done
   by a person alone; AI assistance is optional at every step.)*

**GrantThai contains no Toledo-registered equations and no proofs.** "Toledo"
here refers only to the conceptual framework (lived experience ↔ academic
knowledge, human-gated). See `docs/lineage.md` for pointers to the public
Toledo and glosa repositories. No Toledo content is copied into this
repository.

---

## The one-input, one-output contract

GrantThai's entire purpose is one pipeline, restated per route in v0.3:

```
ONE INPUT              ONE COMMAND PER ROUTE                       ONE OUTPUT PER ROUTE
work.yaml  --------->  grantthai build --route academic-article -->  build/ACADEMIC_ARTICLE.md
(the only canonical    grantthai build --route nriis-proposal   -->  build/NRIIS_SUBMISSION.md
 input; a legacy       grantthai build --route concept-note     -->  build/RESEARCH_CONCEPT_NOTE.md
 project.yaml is       (the route is chosen by a person, never by AI; each invocation writes
 read unchanged)        exactly one file and leaves the other routes' files byte-identical)
```

- **One input.** `work.yaml` (0.3, a superset of `project.yaml` 0.2) is
  the only input `grantthai build` reads. The Markdown forms, the
  questionnaires, `grantthai init`/`set`, and any optional AI assistant are
  all just *editors* of that one file. Your name, team and institution are
  stored in it too (`PROFILE.*`, `ARTICLE.FRONT.AUTHORS`); an optional local
  `profile.yaml` can pre-fill them while you edit, but `build` never reads
  it. The fund profile is a bound reference named inside the file, needed
  only by routes that declare `needs_fund_binding` (the NRIIS route). If a
  directory holds both `work.yaml` and `project.yaml`, `build` stops
  (exit 2).
- **One command per route.** `grantthai build <work.yaml> --route <id>`
  (or `route build`). With no `--route`, the object's declared default
  route is used; a legacy `project.yaml` means `nriis-proposal`; when the
  choice is ambiguous the tool lists the candidates and stops — it never
  picks.
- **One output per route.** `build/NRIIS_SUBMISSION.md` (every field by
  NRIIS tab, `submittable` against the bound fund profile only),
  `build/ACADEMIC_ARTICLE.md` (a manuscript overview of your own records,
  `manuscript_ready` = no BLOCK, never "accepted"), or
  `build/RESEARCH_CONCEPT_NOTE.md` (never submittable). Each carries a
  readiness summary at the top and the NOTICE on body line 1; the article
  route adds its own line: GrantThai is not affiliated with any journal or
  publisher. No second GrantThai-generated file is needed to use a route's
  output.
- **7SSA structure profiles (academic-article).** For conceptual,
  theory, philosophical, legal, integrative-review, formal, SoK and policy
  articles, the article route offers four body layouts from the founder's
  7SSA (seven-sector scholarly article) schema: `7ssa-world` (seven English
  headings) and `7ssa-thai-7`, `7ssa-thai-5`, `7ssa-thai-4` (Thai headings).
  The seven sectors are your own text; merging into five or four visible
  sections is deterministic, keeps an `[S#]` marker per sector and drops
  nothing. The tool lists candidates (INFO RT004) but **you select** the
  profile (`routing.structure_profiles` in `work.yaml`, or
  `--structure-profile`); with none selected the overview is unchanged.
  `grantthai build --format tex` writes `build/ACADEMIC_ARTICLE.tex`
  instead, from a sha256-pinned copy of the glosa GLOSA-7SSA LaTeX template
  (English only; unfilled slots print `NEEDS_INPUT`). Example:
  `examples/article-7ssa-fictional/`.

The full contract is written down in
[`spec/contracts/one-input-one-output.md`](./spec/contracts/one-input-one-output.md)
(0.3.0-draft) and is guarded by `tools/ci/check_one_output.py` (one
template and one unique output filename per route, contract
cross-references, plus a renderer-output check that builds every route the
shipped FICTIONAL examples declare and checks the other routes' files stay
byte-identical).

### Commands

Working in v0.1.0 (`grantthai --help`):

| Command | Purpose |
|---|---|
| `grantthai init [PATH] [--work-id ID] [--work-type T] [--fund ID]` | write a blank `work.yaml` 0.3 (refuses to overwrite); `--project-id` still accepted |
| `grantthai migrate [PATH] [--rename] [--dry-run]` | rewrite a legacy `project.yaml` as `work.yaml` 0.3; prints which review gates go stale |
| `grantthai set FIELD_ID VALUE [--ai --tool NAME]` | set one field; the result is always `DRAFT` (an AI value is `ai_draft`/`INFERENCE`) |
| `grantthai route list` | every route: id, title, output filename, accepted work types, status |
| `grantthai route check --route ID [PATH] [--sub-profile SP] [--json]` | route-scoped validation, report-only |
| `grantthai fields [--tab TAB] [--required] [--route ID]` | list the fields in NRIIS order, or in a route's placement order |
| `grantthai validate [PATH] [--route ID] [--json] [--as-of DATE]` | run the rules in scope for one route (BLOCK/REVIEW/INFO report); exit 1 on any BLOCK |
| `grantthai explain RULE_ID` | plain-language explanation of a rule |
| `grantthai build [PATH] [--route ID] [--sub-profile SP] [--out DIR] [--as-of DATE]` | render exactly one `build/<route output file>` (same as `route build`) |
| `grantthai-mcp --root DIR` | MCP server over the same functions |
| `grantthai-api [--port N]` | local HTTP API over the same functions |

Deferred (founder scope, 2026-09-25): `fill --interactive`, `import-form`,
`fund check`/`fund stale` as separate commands, `export`, `doctor`, and the
Citizen Mode `interview` command. The former `build --concept-note` flag is
replaced by the `concept-note` route.

---

## Ecosystem at a glance

GrantThai bridges exactly four stages: **Problem/Knowledge → Researchable
project → Funding-aligned project (when a route needs a fund) →
route-ready output** (an academic article, an NRIIS proposal or a concept
note; NRIIS is one route), with the one canonical `work.yaml` in and one
file per chosen route out. It sits between two larger ecosystems —
the founder's conceptual Toledo Open Research & Knowledge Ecosystem
(lived experience ↔ academic knowledge, human-gated translation) and the
national/sector Thailand Research & Innovation ecosystem (need → policy →
fund/PMU → project → output → user → outcome → impact). GrantThai never
submits to NRIIS, never decides eligibility, and never grants any
official status — those stay with humans, the bound fund profile, and
NRIIS itself. Full diagrams (with GrantThai's box and its four stages
marked in both ecosystems), the actor table, flows, and
sibling-infrastructure pointers (Toledo, glosa, main.hub) are in
[`docs/ecosystem.md`](./docs/ecosystem.md) (TH+EN) and the machine-readable
[`ecosystem/ecosystem.yaml`](./ecosystem/ecosystem.yaml).

---

## ผู้พัฒนา / Developer

- **Developer / maintainer:** Yaoharee Lahtee (เยาฮารี หละตี), ORCID
  [0009-0005-3861-0626](https://orcid.org/0009-0005-3861-0626)
- **Developing organisation:** ARAYA NIKAH SOCIAL ENTERPRISE CO.
  (อารยานิกะห์ วิสาหกิจเพื่อสังคม)
- **Purpose:** "พัฒนาเพื่อให้เป็นประโยชน์กับคนไทยทุกคนในการพัฒนาความรู้" /
  "Developed to benefit every Thai person in developing knowledge."
- **Joint work:** ผลงานร่วมกับ ศูนย์ความรู้พลเมืองปัญญาประดิษฐ์ ซึ่งเป็นศูนย์ของ
  อารยานิกะห์ วิสาหกิจเพื่อสังคม (a joint work with
  ศูนย์ความรู้พลเมืองปัญญาประดิษฐ์, a centre of ARAYA NIKAH SOCIAL
  ENTERPRISE CO.).

This developer/organisation statement is a statement of who builds and
maintains GrantThai. It does **not** imply any affiliation with, or
endorsement by, NRCT, TSRI, any PMU, or NRIIS — see `NOTICE`.

---

## AI is optional everywhere (parity table)

Every AI-assisted convenience has a human-only equivalent that ships in the
same or an earlier version. See `spec/common/parity.yaml` for the
machine-readable version (populated from v0.3 onward; empty in v0.1.0).

| AI feature (v0.3+) | Human-only equivalent (ships v0.1/v0.2) |
|---|---|
| intake assistant | Citizen questionnaire + `citizen_to_core.yaml` |
| field drafting | `webform/`, `forms/*.md`, `grantthai fill --interactive`, `guidance{th,en}` |
| LocalTerm → AcademicConcept proposal | glossary lookup + human `proposesMapping`, or "own words + CONCEPT NEEDS_INPUT" |
| critique | `grantthai validate` + a named expert review record |
| fund-fit check | `grantthai fund check` |
| handoff package | one file per chosen route (`NRIIS_SUBMISSION.md` / `ACADEMIC_ARTICLE.md` / `RESEARCH_CONCEPT_NOTE.md`); `GRANTTHAI_STANDALONE.md` is reference documentation |
| MCP (v0.1.0) / browser-assist (v0.4) | human copy/paste |

AI output is never `SOURCE` and never moves a field above `DRAFT` on its
own. AI critique is never recorded as an independent review of a research
project. See `spec/common/status.yaml` and
`spec/common/status_permissions.yaml`.

---

## What this repository is (v0.1.0)

On top of the initial scaffold (directory layout, governance and policy
documents, data contracts (JSON Schema and YAML), the field registry
derived from the handoff package (`registry/fields.jsonl`, every Thai label
`NEEDS_VERIFICATION`), the validation rule catalog as data
(`validators/rules.yaml`), CI guards with seeded failing fixtures, and
documentation), v0.1.0 adds the working engine (`src/grantthai/core`,
`validators`, `render`, `api_py.py`, `cli`) and three AI-facing wrappers:
the agent skill (`skills/grantthai/`), the MCP server
(`src/grantthai/mcp/`) and the local HTTP API (`src/grantthai/api/`). The
unreleased v0.3 router adds `work.yaml`, `routes/` (three routes: NRIIS
proposal, academic article, concept note), the `route` commands, `migrate`,
the `ARTICLE.*` fields and the ART rule family (`CHANGELOG.md`). The
web form logic and launchers are deferred. See `GRANTTHAI_STANDALONE.md` for the full
system/architecture description, `docs/design/PLAN.md` for the design plan
(historical record), and `docs/deviations.md` for where this scaffold
intentionally departs from the original handoff package.

## Repository map

- `spec/` — JSON Schema and YAML contracts.
- `registry/`, `mappings/`, `validators/` — field registry, section-to-tab
  table, rule catalog (data).
- `routes/` — the router: `INDEX.yaml` plus one `route.yaml` per output
  route (`nriis-proposal`, `academic-article`, `concept-note`), each naming
  exactly one template, one output filename and one contract; the article
  route's placement and its two `NEEDS_VERIFICATION` sub-profiles.
- `docs/th/`, `docs/en/` — role-specific guides (stubs in v0.1.0).
- `docs/design/PLAN.md` — the founder's design plan (historical record).
- `docs/demo/` — the fictional demo's comparisons with funded public work:
  `comparison.md` (3 reports) and `corpus-100.md` / `corpus-100.th.md`
  (100 funded Thai research documents, metadata and structural statistics
  only, no PDFs; data in `corpus-100.csv`, extractor in `tools/corpus/`).
- `docs/policy/` — the AI-use ceiling (English and Thai), built on the
  GenAI guideline 2569, with a crosswalk of every normative point.
- `skills/grantthai/` — the agent skill (SKILL.md, references, helper script).
- `src/grantthai/` — the library (`api_py.py` is the one Python surface); `core`, `validators`, `review`,
  `fund`, `mapping`, `render`, `interview`, `cli` are AI-free by construction
  (CI enforces this — see `.github/workflows/ci.yml`, no-AI-import guard).
  `assist`, `mcp`, `api` are optional and never load in the core path.
- `funds/` — dated, sourced fund-call profiles. `funds/example/` ships a
  clearly `FICTIONAL` profile for testing; never a real one in v0.1.0.
- `tests/` — positive/negative fixtures, guard tests, and (from v0.1)
  golden files, and one negative fixture per BLOCK rule v0.1 evaluates
  (`tests/fixtures/negative/<rule_id>/`, run by `tests/test_negative_fixtures.py`).
- `.githooks/commit-msg` — rejects AI/vendor attribution trailers in commit
  messages. Run `git config core.hooksPath .githooks` after cloning.

## Governance and status vocabulary

See `GOVERNANCE.md`, `spec/common/status.yaml`, `spec/common/review_gates.yaml`.
In short: a "checked" or "verified" status always states *who* checked it
and *how independent* they were. Self-review renders as `AUTHOR_CHECKED`,
never as `VERIFIED`. Humans decide everything; AI proposes, never proves.

## Licensing

- Code (`src/`, `tools/`, `tests/`, `.githooks/`, `.github/`, `webform/`,
  `launchers/`, `pyproject.toml`, `.gitignore`): Apache-2.0.
- Everything else — documentation, specifications, ontology, templates and
  data (registry, mappings, rule catalog, fund profiles, ecosystem files):
  CC BY 4.0.

`REUSE.toml` is the authoritative per-path mapping, and `reuse lint` runs in
CI. See `LICENSE` and `LICENSES/`.

## Contact

See `SECURITY.md` and `CODE_OF_CONDUCT.md` (contact address: `NEEDS_INPUT`,
pending a founder-supplied non-personal address, decision K9).

---

## Core Epistemic Structure (role disclosure)

- **Core respondent / experience-based expert:** Yaoharee Lahtee.
- **Interactional expert:** None.
- **AI model(s) used (role only, not authorship):**
  - GPT-5.6-sol (OpenAI, via Codex) — co-drafting of the handoff package
    and overall picture with the author.
  - Claude Opus 5.5 — planning meeting chair/seats, adversarial gate
    review, drafting fixes.
  - Claude Sonnet 5 — scaffolding and verification.

  This footer and `docs/lineage.md` are the only places an AI model is
  named as having been used in producing this repository (other mentions
  are guard patterns, SDK package names in import-ban lists, tooling file
  names or guard-test fixtures). It is a role disclosure, not an
  authorship or credit line.
