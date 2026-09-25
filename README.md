<p align="center">
  <img src="docs/assets/ai-civic-knowledge-logo.png" width="300" alt="ศูนย์ความรู้พลเมืองปัญญาประดิษฐ์ · Center for AI Civic Knowledge">
</p>

<h1 align="center">GrantThai</h1>

<p align="center"><strong>งานความรู้หนึ่งชิ้น หลายเส้นทาง: บทความ &nbsp;·&nbsp; ข้อเสนอ NRIIS &nbsp;·&nbsp; concept note</strong></p>

<p align="center">
  <img alt="ทำในประเทศไทย" src="https://img.shields.io/badge/%F0%9F%87%B9%F0%9F%87%AD-%E0%B8%97%E0%B8%B3%E0%B9%83%E0%B8%99%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B9%80%E0%B8%97%E0%B8%A8%E0%B9%84%E0%B8%97%E0%B8%A2-1B2A4A?style=for-the-badge">
  <img alt="เวอร์ชัน 0.1.0" src="https://img.shields.io/badge/%E0%B9%80%E0%B8%A7%E0%B8%AD%E0%B8%A3%E0%B9%8C%E0%B8%8A%E0%B8%B1%E0%B8%99-0.1.0-B08D57?style=for-the-badge">
  <img alt="โค้ด Apache-2.0 · เอกสาร CC BY 4.0" src="https://img.shields.io/badge/%E0%B9%82%E0%B8%84%E0%B9%89%E0%B8%94%20Apache--2.0%20%C2%B7%20%E0%B9%80%E0%B8%AD%E0%B8%81%E0%B8%AA%E0%B8%B2%E0%B8%A3%20CC%20BY%204.0-1B2A4A?style=for-the-badge">
  <img alt="โครงการอิสระ ไม่เป็นทางการ" src="https://img.shields.io/badge/%E0%B9%82%E0%B8%84%E0%B8%A3%E0%B8%87%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%AD%E0%B8%B4%E0%B8%AA%E0%B8%A3%E0%B8%B0-%E0%B9%84%E0%B8%A1%E0%B9%88%E0%B9%80%E0%B8%9B%E0%B9%87%E0%B8%99%E0%B8%97%E0%B8%B2%E0%B8%87%E0%B8%81%E0%B8%B2%E0%B8%A3-B08D57?style=for-the-badge">
</p>

<p align="center">
  <a href="README.en.md"><b>English</b></a> &nbsp;·&nbsp;
  <a href="AGENTS.md">สำหรับ AI ผู้ช่วย</a> &nbsp;·&nbsp;
  <a href="docs/th/">คู่มือภาษาไทย</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/-%20-A51931?style=flat-square" height="6" alt="">
  <img src="https://img.shields.io/badge/-%20-F4F5F8?style=flat-square" height="6" alt="">
  <img src="https://img.shields.io/badge/-%20-2D2A4A?style=flat-square" height="6" alt="">
  <img src="https://img.shields.io/badge/-%20-F4F5F8?style=flat-square" height="6" alt="">
  <img src="https://img.shields.io/badge/-%20-A51931?style=flat-square" height="6" alt="">
</p>

## GrantThai คืออะไร

เครื่องมือเปิดที่ช่วยเปลี่ยน **ปัญหาจริงที่คุณรู้ดี** ให้เป็น **งานความรู้หนึ่งชิ้น** ที่คุณเก็บไว้ในไฟล์เดียว (`work.yaml`) แล้วเลือกเองว่าจะให้ออกมาเป็นอะไร: ร่างบทความวิชาการ ร่างข้อเสนอโครงการสำหรับกรอก NRIIS หรือ concept note แต่ละเส้นทางให้ไฟล์เดียว เพื่อให้คุณตรวจทาน แล้วนำไปใช้ต่อด้วยตนเอง

```
                                  ┌─ --route academic-article ─►  build/ACADEMIC_ARTICLE.md
work.yaml  ──►  grantthai build ──┼─ --route nriis-proposal   ─►  build/NRIIS_SUBMISSION.md
(ข้อมูลของคุณ ไฟล์เดียว)             └─ --route concept-note     ─►  build/RESEARCH_CONCEPT_NOTE.md
                                  (คุณเป็นคนเลือกเส้นทาง ไม่ใช่ AI · หนึ่งครั้ง = หนึ่งไฟล์)
```

การลงระบบ NRIIS ไม่ใช่แกนหลักอีกต่อไป แต่เป็นหนึ่งเส้นทางของ **router** — ในที่นี้ router หมายถึงเส้นทางผลลัพธ์ที่ **คน** เป็นผู้เลือกอย่างชัดเจน ไม่ใช่ AI ตัดสินให้ ไฟล์ `project.yaml` แบบเดิมยังใช้ได้โดยไม่ต้องแก้ (ระบบอ่านเป็นเส้นทาง NRIIS ให้อัตโนมัติ)

- **ความรู้เป็นของคุณ** ประสบการณ์ ข้อมูล และดุลยพินิจของนักวิจัยคือต้นทาง
- **AI เป็นเพียงผู้ช่วยเรียบเรียง** ถามคุณ ร่างให้ ตรวจโครงสร้าง แต่ไม่รับรองความรู้ และไม่แต่งข้อเท็จจริงเรื่องทุน
- **ทุกช่องตรวจสอบย้อนกลับได้** อะไรยังขาด ระบบบอกว่า `NEEDS_INPUT` อะไรยังไม่ยืนยันกับเอกสารทางการ ระบบบอกว่า `NEEDS_VERIFICATION`
- **ไม่แต่งข้อเท็จจริงเรื่องวารสาร** GrantThai ไม่มีทะเบียนวารสาร ไม่ผูกพันกับวารสารหรือสำนักพิมพ์ใด ข้อกำหนดของวารสารเป็นสิ่งที่คุณต้องยืนยันจากคู่มือผู้เขียนของวารสารนั้นเอง

> **GrantThai ลดกำแพงในการเข้าสู่งานวิจัย ไม่ได้ลดมาตรฐานของงานวิจัย**

## เริ่มใช้ใน 3 นาที

```bash
pip install -e .                                   # ติดตั้งครั้งเดียว
grantthai init work.yaml --work-id MY-001 --work-type academic_article   # เริ่มงานใหม่ (หรือ research_proposal / concept_note)
grantthai set CORE.GENERAL.TITLE_TH "ชื่องาน"                              # กรอกข้อมูลทีละช่อง
grantthai route list                                                     # ดูว่ามีเส้นทางอะไรบ้าง
grantthai route check --route academic-article work.yaml                 # ตรวจตามเส้นทางที่เลือก
grantthai build work.yaml --route academic-article                       # ได้ build/ACADEMIC_ARTICLE.md
grantthai build work.yaml --route nriis-proposal                         # งานเดียวกัน ได้ build/NRIIS_SUBMISSION.md
grantthai migrate project.yaml --dry-run                                 # มี project.yaml เดิม? ดูก่อนว่าการย้ายเป็น work.yaml กระทบอะไร
```

## ใช้ร่วมกับ AI ของคุณ

ให้ AI ที่คุณใช้อยู่แล้ว ไม่ว่าค่ายไหน เป็นคนสัมภาษณ์และกรอกให้ ส่วนคุณเป็นคนยืนยัน

| ช่องทาง | เหมาะกับ | เริ่มที่ |
|---|---|---|
| **สกิล** | Claude Code, Codex, Gemini CLI และ AI แชททั่วไป | [`skills/grantthai/SKILL.md`](skills/grantthai/SKILL.md) |
| **MCP** | โปรแกรม AI ที่รองรับ MCP เช่น Claude Desktop | [`docs/mcp.md`](docs/mcp.md) |
| **API** | ChatGPT Actions และระบบอัตโนมัติ | [`docs/api.md`](docs/api.md) |

ทุกช่องทางให้ผลลัพธ์เดียวกัน คือไฟล์เดียวกันแบบไบต์ต่อไบต์ต่อหนึ่งเส้นทาง และทุกค่าที่ AI ร่างจะถูกระบุว่าเป็นร่างของ AI รอคุณยืนยันเสมอ AI ทำได้แค่บอกว่ามีเส้นทางอะไรบ้างแล้วถามคุณ ไม่เคยเลือกเส้นทางแทนคุณ

AI ทุกตัวทำงานภายใต้ [เพดานการใช้ AI](docs/policy/ai-use-ceiling.th.md) ที่อิงแนวทางการใช้ GenAI อย่างมีจริยธรรมสำหรับนักวิจัย
(กันยายน 2569): ก่อนรับข้อมูลต้องเตือนเรื่องข้อมูลส่วนบุคคลและข้อมูลลับ และไฟล์ผลลัพธ์มีแบบแจ้งการใช้ AI ให้คุณตรวจและยืนยันเอง

## ระบบนิเวศที่ GrantThai อยู่

```
ประสบการณ์จริงของผู้คน ──► แปลงเป็นโจทย์วิจัย ──► ออกแบบวิธีวิจัย ──► (จัดให้ตรงทุน) ──► ผลลัพธ์ตามเส้นทางที่คุณเลือก
                                        └────────────── GrantThai ทำส่วนนี้ ──────────────┘   บทความ · ข้อเสนอ NRIIS · concept note
```

รายละเอียดทั้งระบบ ผู้เกี่ยวข้อง และขอบเขตที่ GrantThai **ไม่ทำ** อยู่ที่ [`docs/ecosystem.md`](docs/ecosystem.md)

## ผู้พัฒนา

<table>
<tr>
<td width="140" align="center"><img src="docs/assets/ai-civic-knowledge-logo.png" width="120" alt=""></td>
<td>
<b>เยาฮารี หละตี</b> (Yaoharee Lahtee) · ORCID <a href="https://orcid.org/0009-0005-3861-0626">0009-0005-3861-0626</a><br>
<b>อารยานิกะห์ วิสาหกิจเพื่อสังคม</b> · ARAYA NIKAH SOCIAL ENTERPRISE CO.<br>
ผลงานร่วมกับ <b>ศูนย์ความรู้พลเมืองปัญญาประดิษฐ์</b> (Center for AI Civic Knowledge) ซึ่งเป็นศูนย์ของอารยานิกะห์ วิสาหกิจเพื่อสังคม<br><br>
<i>พัฒนาเพื่อให้เป็นประโยชน์กับคนไทยทุกคนในการพัฒนาความรู้</i>
</td>
</tr>
</table>

โค้ดใช้สัญญาอนุญาต Apache-2.0 เอกสารใช้ CC BY 4.0 · **โลโก้สงวนสิทธิ์** ไม่อยู่ภายใต้สัญญาอนุญาตทั้งสอง · รายละเอียดใน [`LICENSE`](LICENSE) และ [`NOTICE`](NOTICE)

## ประกาศ

GrantThai is an independent, unofficial project. It is NOT affiliated with, endorsed by, sponsored by, or officially connected to NRCT, TSRI, any PMU, or NRIIS. / GrantThai เป็นโครงการอิสระ ไม่เป็นทางการ และไม่ผูกพันกับ วช. สกสว. หน่วยบริหารจัดการทุน (PMU) ใด ๆ หรือระบบ NRIIS

ชื่อช่องและลำดับหน้าจอของ NRIIS ในระบบนี้ยังเป็น **ตัวเลือกที่รอยืนยันกับเอกสารทางการ** ทั้งหมด โปรดตรวจกับประกาศทุนฉบับปัจจุบันก่อนยื่นทุกครั้ง

<p align="center">
  <img src="https://img.shields.io/badge/-%20-A51931?style=flat-square" height="6" alt="">
  <img src="https://img.shields.io/badge/-%20-F4F5F8?style=flat-square" height="6" alt="">
  <img src="https://img.shields.io/badge/-%20-2D2A4A?style=flat-square" height="6" alt="">
  <img src="https://img.shields.io/badge/-%20-F4F5F8?style=flat-square" height="6" alt="">
  <img src="https://img.shields.io/badge/-%20-A51931?style=flat-square" height="6" alt="">
</p>

---

<details>
<summary><b>รายละเอียดเชิงเทคนิค</b> (เวอร์ชัน, แผนที่คลัง, การกำกับดูแล, สัญญาอนุญาต, การเปิดเผยบทบาท AI)</summary>

### Philosophy

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

### The one-input, one-output contract

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

### Ecosystem at a glance

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

### ผู้พัฒนา / Developer

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

### AI is optional everywhere (parity table)

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

### What this repository is (v0.1.0)

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

### Repository map

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

### Governance and status vocabulary

See `GOVERNANCE.md`, `spec/common/status.yaml`, `spec/common/review_gates.yaml`.
In short: a "checked" or "verified" status always states *who* checked it
and *how independent* they were. Self-review renders as `AUTHOR_CHECKED`,
never as `VERIFIED`. Humans decide everything; AI proposes, never proves.

### Licensing

- Code (`src/`, `tools/`, `tests/`, `.githooks/`, `.github/`, `webform/`,
  `launchers/`, `pyproject.toml`, `.gitignore`): Apache-2.0.
- Everything else — documentation, specifications, ontology, templates and
  data (registry, mappings, rule catalog, fund profiles, ecosystem files):
  CC BY 4.0.

`REUSE.toml` is the authoritative per-path mapping, and `reuse lint` runs in
CI. See `LICENSE` and `LICENSES/`.

### Contact

See `SECURITY.md` and `CODE_OF_CONDUCT.md` (contact address: `NEEDS_INPUT`,
pending a founder-supplied non-personal address, decision K9).

---

### Core Epistemic Structure (role disclosure)

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


</details>
