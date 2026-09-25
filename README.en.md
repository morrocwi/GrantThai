# GrantThai

**Status: v0.1.0 (not yet released to a package index).** The engine works:
one `project.yaml` in, one `build/NRIIS_SUBMISSION.md` out, through the
`grantthai` command, a Python API, an agent **skill**, an **MCP** server and
a local **HTTP API**. The offline web form, the launchers and Citizen Mode
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
`NEEDS_VERIFICATION`). Every value it writes stays `DRAFT` and is listed in
the output for you to confirm. Works with any AI vendor or a local model.
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

ทั้งสามทางได้ไฟล์เดียวกันเพียงไฟล์เดียว: `build/NRIIS_SUBMISSION.md` คุณเป็นผู้ตรวจ
ตัดสินใจ และส่งเองเสมอ

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
4. Open `build/NRIIS_SUBMISSION.md`. It is one file: a readiness summary at
   the top (anything still missing, in plain language) followed by every
   field, grouped by NRIIS tab, ready to copy and paste. The tab names and
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

GrantThai's entire purpose is one pipeline:

```
ONE INPUT                    ONE COMMAND                 ONE OUTPUT
project.yaml  ------------>  grantthai build  --------->  build/NRIIS_SUBMISSION.md
(the only canonical input)                                (a single, self-contained,
                                                             ready-to-copy-paste file)
```

- **One input.** `project.yaml` is the only input `grantthai build` reads.
  The offline web form, the Markdown forms, the Citizen/Expert
  questionnaires, `grantthai init`, and any optional AI assistant are all
  just *editors* of that one file. Your name, team and institution used in
  the submission are stored in `project.yaml` too (`PROFILE.*` fields); an
  optional local `profile.yaml` can pre-fill them while you edit, but
  `build` never reads it. The fund profile is a bound reference named inside
  `project.yaml`, not a second input.
- **One command.** `grantthai build <project.yaml>`.
- **One output.** `build/NRIIS_SUBMISSION.md` — one self-contained file
  containing every field grouped by NRIIS tab, plus a readiness summary
  (`BLOCK` / `REVIEW` / `INFO` findings, `NEEDS_INPUT`,
  `NEEDS_VERIFICATION`) at the top. No second GrantThai-generated file is
  needed to enter data into NRIIS; supporting documents for the attachments
  tab are your own files, listed with their status. (Citizen Mode's
  optional `--concept-note` output is a *separate*, clearly optional
  artifact for people who are not yet build-ready for NRIIS at all — it is
  never part of the NRIIS entry path itself.)

The full contract is written down in
[`spec/contracts/one-input-one-output.md`](./spec/contracts/one-input-one-output.md)
and is guarded by `tools/ci/check_one_output.py` (structural checks, plus
a renderer-output check that runs `grantthai build` on the shipped
FICTIONAL worked example).

### Commands

Working in v0.1.0 (`grantthai --help`):

| Command | Purpose |
|---|---|
| `grantthai init [PATH] [--project-id ID] [--fund ID]` | write a blank `project.yaml` (refuses to overwrite) |
| `grantthai set FIELD_ID VALUE [--ai --tool NAME]` | set one field; the result is always `DRAFT` (an AI value is `ai_draft`/`INFERENCE`) |
| `grantthai fields [--tab TAB] [--required]` | list the fields in NRIIS order |
| `grantthai validate [PATH] [--json] [--as-of DATE]` | run the rules (BLOCK/REVIEW/INFO report); exit 1 on any BLOCK |
| `grantthai explain RULE_ID` | plain-language explanation of a rule |
| `grantthai build [PATH] [--out DIR] [--as-of DATE]` | render the one output `build/NRIIS_SUBMISSION.md` |
| `grantthai-mcp --root DIR` | MCP server over the same functions |
| `grantthai-api [--port N]` | local HTTP API over the same functions |

Deferred (founder scope, 2026-09-25): `fill --interactive`, `import-form`,
`fund check`/`fund stale` as separate commands, `export`, `doctor`, and the
Citizen Mode, review and lock commands (`interview`, `review`,
`accept-mapping`/`reject-mapping`, `build --concept-note`, `lock`, `diff`).

---

## Ecosystem at a glance

GrantThai bridges exactly four stages: **Problem/Knowledge → Researchable
project → Funding-aligned project → NRIIS-ready project**, with the one
canonical `project.yaml` in and the one canonical
`build/NRIIS_SUBMISSION.md` out. It sits between two larger ecosystems —
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
| handoff package | `NRIIS_SUBMISSION.md` (the one output); `GRANTTHAI_STANDALONE.md` is reference documentation |
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
web form logic and launchers are deferred. See `GRANTTHAI_STANDALONE.md` for the full
system/architecture description, `docs/design/PLAN.md` for the design plan
(historical record), and `docs/deviations.md` for where this scaffold
intentionally departs from the original handoff package.

## Repository map

- `spec/` — JSON Schema and YAML contracts.
- `registry/`, `mappings/`, `validators/` — field registry, section-to-tab
  table, rule catalog (data).
- `docs/th/`, `docs/en/` — role-specific guides (stubs in v0.1.0).
- `docs/design/PLAN.md` — the founder's design plan (historical record).
- `docs/demo/` — the fictional demo's comparisons with funded public work:
  `comparison.md` (3 reports) and `corpus-100.md` / `corpus-100.th.md`
  (100 funded Thai research documents, metadata and structural statistics
  only, no PDFs; data in `corpus-100.csv`, extractor in `tools/corpus/`).
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
