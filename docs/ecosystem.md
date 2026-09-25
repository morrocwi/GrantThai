# The GrantThai ecosystem / ระบบนิเวศของ GrantThai

*(TH + EN. Machine-readable companion: `ecosystem/ecosystem.yaml`. The
English and Thai sections carry the same content.)*

## 1. Two ecosystems, and how they nest

GrantThai sits between two distinct ecosystems. Understanding both, and
where the boundary between them is, is the point of this document.

**Two meanings of "Toledo".** In this document, "the Toledo ecosystem"
means the founder's *conceptual* framework (lived experience ↔ academic
knowledge, human-gated translation). "Toledo" is also the name of a
separate public repository, an equation registry and proof framework that
the founder maintains (section 5). The two are related — the repository is
one of the founder's projects under the same programme — but they are not
the same thing, and **GrantThai contains no Toledo-registered equations and
no proofs**.

In both diagrams below, the stages GrantThai covers are marked (`[GT n]`
in diagram (a), a `[GrantThai: stages 1-4]` box in diagram (b)) with the
four bridge stages:
**①** Problem/Knowledge, **②** Researchable project, **③** Funding-aligned
project (only when the chosen route needs a fund), **④** route-ready
output — an academic article, an NRIIS proposal or a concept note; **NRIIS
is one route** of the router, and the route is chosen by the person, never
by an AI (founder reframe, 2026-09-25). Every diagram also draws the direct
`Person ==(no AI)==> Research core` edge.

### (a) The Toledo Open Research & Knowledge Ecosystem (conceptual, founder's)

The founder's node order is kept unchanged. Nodes marked `[GT n]` are the
ones GrantThai covers (stage n); unmarked nodes are outside GrantThai.

```
 People / Practitioners              Academic knowledge
 (lived experience, Stream A)        (Stream B)
        \                                  /
         v                                v
              Real-world problems                    [GT 1] Problem/Knowledge
                     |
                     v
     TRANSLATION (by people; AI optional, never required)   [GT 2]
                     |
                     v
  Person ==(no AI)==> Research core                   [GT 2] Researchable project
                     |
                     v
  Experts / Universities / Institutions / Research networks
     (GrantThai only records their named reviews, v0.2)
                     |
                     v
              Quality assurance
                     |
                     v
              Verified knowledge
                     |
                     v
              Research project                        [GT 3] Funding-aligned project (NRIIS route)
                     |                                [GT 4] route-ready output, one file per route:
                     |                                       build/ACADEMIC_ARTICLE.md (scholarly record)
                     |                                       build/NRIIS_SUBMISSION.md (one route)
                     |                                       build/RESEARCH_CONCEPT_NOTE.md
                     v
                 Innovation (social or other)
                     |
                     v
                  Outcome
                     |
                     v
                  Impact
                     |
                     `---------(feedback)---------> back to real-world problems
```

### (b) The Thailand Research & Innovation (R&I) ecosystem — national/sector

Time-sensitive Thai facts in this section (agency names, programmes,
funds) are **RELAYED and dated only** (`ecosystem/positions@2026-09.yaml`,
`ecosystem/ecosystem.yaml`). Verify against a current public source before
relying on any specific name or figure — see `docs/sources.md`.

```
 National/sector need  <------------------------------------------+
         |                                                        |
         v                                                        |
 Policy / plan / KR (key result)                                  |
         |                                                        |
         v                                                        |
 Fund / PMU (Program Management Unit) -- publishes a call         |
         |           (read by GrantThai as a dated fund profile)  |
         v                                                        |
 +---------------------------------------------------------+      |
 | [GrantThai: stages 1-4]                                  |      |
 |  (1) Problem/Knowledge                                   |      |
 |  Person ==(no AI)==> Research core                       |      |
 |  (2) Researchable project                                |      |
 |  (3) Funding-aligned project (NRIIS route: bound fund)   |      |
 |  (4) ROUTER, the person chooses (never an AI):           |      |
 |      --route academic-article -> build/ACADEMIC_ARTICLE.md        |      |
 |      --route nriis-proposal   -> build/NRIIS_SUBMISSION.md        |      |
 |      --route concept-note     -> build/RESEARCH_CONCEPT_NOTE.md   |      |
 +---------------------------|-----------------------------+      |
                             v  a person submits (NRIIS route) or   |
                                finishes the manuscript; GrantThai  |
                                never submits                       |
 Research institution / network (endorsement, submission)         |
         |                                                        |
         v                                                        |
       Project (funded)                                           |
         |                                                        |
         v                                                        |
       Output --> User --> Outcome --> Impact ---(feedback)-------+
```

## 2. Where GrantThai sits

GrantThai is the bridge across exactly four stages, and nowhere else:

```
(1) Problem / Knowledge --> (2) Researchable project --> (3) Funding-aligned project --> (4) route-ready output
                                                          (only for routes that need a fund)        |
                                                                                                    v
                        [ one work.yaml IN --> the person picks a route --> exactly one file OUT per route ]
                          academic-article -> ACADEMIC_ARTICLE.md | nriis-proposal -> NRIIS_SUBMISSION.md | concept-note -> RESEARCH_CONCEPT_NOTE.md
```

How the four stages map onto the nodes of each ecosystem (also in
`ecosystem/ecosystem.yaml`, `grantthai_position.stages[].maps_to`):

| Stage | Toledo ecosystem node(s) | Thailand R&I node(s) |
|---|---|---|
| (1) Problem / Knowledge | real-world problems; people/practitioners; academic knowledge | national/sector need (as the person's problem statement) |
| (2) Researchable project | translation; research core | — (before any fund is involved) |
| (3) Funding-aligned project | research project | fund/PMU (read only, as a dated fund profile); policy/plan/KR (as declared positions). Only the NRIIS route needs this stage |
| (4) Route-ready output | research project (rendered); for the article route, the scholarly-record layer of the open-knowledge intake (a manuscript overview the person finishes; preprint is not peer review) | project (NRIIS route, only once a person submits it and it is funded — outside GrantThai); a journal's own process (article route — outside GrantThai) |

```
                 +---------------------------------------------------------------+
                 |                           GrantThai                           |
                 |                                                               |
                 |   Person ==(no AI)==> work.yaml                               |
                 |   spec/ (contracts) -> validators (route-scoped) ->           |
   work.yaml     |   review gates -> ROUTER (routes/, the person chooses) ->     |  exactly one file per route:
   (one input) --+-> render (Jinja2, deterministic, one template per route)      +--> build/ACADEMIC_ARTICLE.md
                 |                                                               |     build/NRIIS_SUBMISSION.md
                 |   AI assist (OPTIONAL, never SOURCE, never above DRAFT,       |     build/RESEARCH_CONCEPT_NOTE.md
                 |   never picks a route)                                        |
                 +---------------------------------------------------------------+
```

**Inside the GrantThai box:** the work object, the rule engine, the
review-gate bookkeeping, the router (a declared, deterministic choice of
output route), one renderer per route, and an optional AI assistant that
can only ever propose, never check, approve, or pick a route.

**Outside the GrantThai box, and never entered by GrantThai:** NRIIS
itself (GrantThai never submits — see `NOTICE`), any journal's or
publisher's submission and review process (GrantThai is not affiliated
with any of them and ships no venue registry), any fund/PMU's internal
review process, any institution's own approval chain, and any human's
final judgment about whether and what to submit.

## 3. Actors

See `ecosystem/ecosystem.yaml` (`actors:`) for the machine-readable form.

| Actor | Brings | GrantThai gives them | AI |
|---|---|---|---|
| Citizen | lived experience | guided questionnaire + concept-note path (v0.2) | optional |
| Practitioner | field knowledge | same as citizen, plus local-terms glossary | optional |
| Civil society | community representation | same as citizen | optional |
| Social entrepreneur | applied problem framing | Expert or Citizen mode | optional |
| Graduate student | partial academic training | Expert Mode guidance | optional |
| Lecturer | academic expertise | the full no-AI Expert path (v0.1) | none required |
| University / independent researcher | academic or applied expertise | the full no-AI Expert path (v0.1) | none required |
| Research administrator | institutional process knowledge | review + lock workflow (v0.2) | none |
| Expert reviewer | independent judgment | named review-record tooling | none |
| Mentor | guidance | review view | none |
| Institution | affiliation record | partner/eligibility context | none |
| Research network | partner matching | directory pointers (v0.5, opt-in) | none |
| Fund / PMU | a dated fund profile | nothing — GrantThai only reads the profile | none |
| NRIIS | one external render target (the `nriis-proposal` route) | nothing — GrantThai never submits to it | none |
| Journal / publisher | another external target (the `academic-article` route) | nothing — GrantThai names no journal and reads no venue rules; the researcher supplies the venue's own document | none |
| User / adopter | downstream use of the output | nothing directly | none |

AI's column is always "optional" or "none" — never "required". This is not
a simplification; it is the enforced ceiling (`spec/common/status_permissions.yaml`).

## 4. Flows

- **Knowledge flow.** Lived experience (Stream A) and academic knowledge
  (Stream B) meet at TRANSLATION. A human can always cross this bridge
  alone; a `Mapping` (LocalTerm → AcademicConcept) records the crossing
  and its provenance (`spec/common/mapping_proposal.schema.json`).
- **Checking flow.** Only deterministic validators set
  `STRUCTURE_CHECKED`/`LOGIC_LINKED`; only a named human review record sets
  `HUMAN_REVIEWED`/`VERIFIED`; only a named human sets `LOCKED`/`SUBMITTED`.
  **AI never sets any status above `DRAFT`** (`spec/common/status_permissions.yaml`).
- **Funding flow.** A dated `funds/<agency>/<call-id>@<ver>/` profile is
  bound at build time; it decides eligibility (`ELIG001`) and rule content.
  GrantThai's core schema holds no eligibility thresholds of its own.
- **Routing flow.** The person declares the route (`routing` in
  `work.yaml`, or `--route`); the tool resolves it deterministically and
  stops when the choice is ambiguous. Choosing a route is not authored
  content: `routing` is outside `content_sha256`, so a route choice never
  makes a review stale.
- **Output → user → outcome → impact flow.** Mirrors both ecosystem
  diagrams above; GrantThai's own responsibility ends at rendering the one
  file of the chosen route — everything from submission, or from the
  manuscript's journey to a journal, onward is a human, and later a
  funder/journal/institution/user, decision.
- **Feedback loop.** Both ecosystem diagrams draw impact feeding back into
  new problems/needs. In the chain contract (`spec/common/chain.yaml`)
  this is modelled explicitly as the `feedback` edges `KR -> Need` and
  `Impact -> KR`, which are allowed to loop (unlike `causal` edges, which
  must form a DAG, rule `CH001`).

## 5. Sibling infrastructure (pointers only — no content copied)

- **Toledo (repository)** — the equation registry and proof framework the
  founder also maintains; related to, but not the same as, the conceptual
  Toledo ecosystem in section 1(a). GrantThai contains none of its content.
  <https://github.com/morrocwi/toledo> — DOI
  [10.5281/zenodo.22537318](https://doi.org/10.5281/zenodo.22537318)
- **glosa** — human-AI knowledge co-production methodology (maker/checker
  discipline, claim cards). <https://github.com/morrocwi/glosa>
- **main.hub** — routing layer across the founder's public Human-AI
  Readout Programme repos. <https://github.com/morrocwi/main.hub>

## 6. Boundaries — what GrantThai does NOT do

- It does not submit anything to NRIIS, ever (`NOTICE`,
  `submission_mode.direct_submit: false`, always), and it does not submit
  to any journal.
- It does not pick a route. The route is the person's declaration; an AI
  surface lists routes and asks.
- It does not write an article. The article route arranges the
  researcher's own records into an overview; section text, citations and
  venue facts are the researcher's (`NEEDS_VERIFICATION` without a
  supplied source).
- It does not decide PI eligibility — that is the bound fund profile's job
  (`ELIG001`).
- It does not grant any certification or official/compatible status. Its
  own output says "checked against GrantThai rules", never "verified" in
  any sense that implies an outside authority signed off
  (`spec/common/status.yaml`).
- Time-sensitive Thai ecosystem facts (funds, PMUs, programmes) appear only
  as dated `RELAYED` entries, carrying `derived_from: core/03@sha256:...`
  lineage — never as settled truth.

---

## ภาษาไทย

### 1. ระบบนิเวศสองชั้นและความสัมพันธ์

GrantThai อยู่ระหว่างระบบนิเวศสองชั้น

**คำว่า "Toledo" มีสองความหมาย** ในเอกสารนี้ "ระบบนิเวศ Toledo" หมายถึงกรอบแนวคิดของผู้ก่อตั้ง
(เชื่อมประสบการณ์ตรงของผู้คนกับความรู้เชิงวิชาการ ผ่านการแปลที่มีมนุษย์เป็นผู้กำกับ) ส่วน
"Toledo" อีกความหมายหนึ่งคือ repository สาธารณะแยกต่างหาก ซึ่งเป็นคลังสมการและกรอบการพิสูจน์
ที่ผู้ก่อตั้งดูแลอยู่ (ข้อ 5) ทั้งสองเกี่ยวข้องกันเพราะอยู่ในโครงการเดียวกันของผู้ก่อตั้ง แต่ไม่ใช่สิ่งเดียวกัน
และ **GrantThai ไม่มีสมการที่ลงทะเบียนใน Toledo และไม่มีบทพิสูจน์ใด ๆ**

ในแผนภาพทั้งสองข้างต้น ขั้นตอนที่ GrantThai ดูแลมีเครื่องหมายกำกับ (`[GT n]` ในแผนภาพ (a)
และกรอบ `[GrantThai: stages 1-4]` ในแผนภาพ (b)) พร้อมหมายเลข
สี่ขั้นของสะพาน ได้แก่ (1) ปัญหา/ความรู้ (2) โครงการที่วิจัยได้ (3) โครงการที่สอดคล้องกับแหล่งทุน (เฉพาะเส้นทางที่ต้องใช้ทุน)
(4) ผลลัพธ์ตามเส้นทางที่เลือก — บทความวิชาการ ข้อเสนอ NRIIS หรือ concept note โดย **NRIIS เป็นเพียงหนึ่งเส้นทางของ router**
และคนเป็นผู้เลือกเส้นทาง ไม่ใช่ AI (ผู้ก่อตั้งปรับกรอบ 2026-09-25) ทุกแผนภาพมีเส้นตรง `บุคคล ==(ไม่ใช้ AI)==> แกนวิจัย` เสมอ

- **(ก) ระบบนิเวศวิจัยและความรู้เปิดของ Toledo (เชิงแนวคิด):** ผู้คน/ผู้ปฏิบัติงาน และความรู้เชิงวิชาการ
  → ปัญหาจริง [GT 1] → การแปล (โดยมนุษย์ AI เป็นทางเลือก ไม่บังคับ) [GT 2] → แกนวิจัย [GT 2]
  → ผู้เชี่ยวชาญ/มหาวิทยาลัย/สถาบัน/เครือข่ายวิจัย → การประกันคุณภาพ → ความรู้ที่ผ่านการตรวจสอบ
  → โครงการวิจัย [GT 3, GT 4] → นวัตกรรม → ผลลัพธ์ → ผลกระทบ → (ย้อนกลับ) ปัญหาจริง
- **(ข) ระบบนิเวศวิจัยและนวัตกรรมของประเทศไทย (ระดับชาติ/ภาคส่วน):** ความต้องการของประเทศ/ภาคส่วน
  → นโยบาย/แผน/KR → แหล่งทุน/หน่วยบริหารจัดการทุน (PMU) → [GrantThai ขั้น 1–4] → สถาบัน/เครือข่ายวิจัย
  → โครงการ → ผลผลิต → ผู้ใช้ → ผลลัพธ์ → ผลกระทบ → (ย้อนกลับ) ความต้องการของประเทศ
  ข้อเท็จจริงที่ผูกกับเวลา เช่น ชื่อหน่วยงาน ทุน หรือโปรแกรม ระบุแบบ RELAYED และมีวันที่กำกับเสมอ
  ไม่ถือเป็นความจริงตายตัว

### 2. ตำแหน่งของ GrantThai

GrantThai เป็นสะพานผ่านสี่ขั้นตอนเท่านั้น: (1) ปัญหา/ความรู้ → (2) โครงการที่วิจัยได้ →
(3) โครงการที่สอดคล้องกับแหล่งทุน (เมื่อเส้นทางต้องใช้ทุน) → (4) ผลลัพธ์ตามเส้นทางที่เลือก โดยมี **input ทางเดียว
(work.yaml) และ output หนึ่งไฟล์ต่อหนึ่งเส้นทาง** (`build/ACADEMIC_ARTICLE.md`, `build/NRIIS_SUBMISSION.md`
หรือ `build/RESEARCH_CONCEPT_NOTE.md`) ไฟล์ `project.yaml` แบบเดิมอ่านได้โดยไม่ต้องแก้และถือเป็นเส้นทาง NRIIS
ตารางในข้อ 2 ภาษาอังกฤษแสดงว่าแต่ละขั้นตรงกับส่วนใดของระบบนิเวศทั้งสอง

### 3. ผู้มีบทบาท (actors)

| ผู้มีบทบาท | สิ่งที่นำมา | สิ่งที่ GrantThai ให้ | AI |
|---|---|---|---|
| ประชาชน | ประสบการณ์ตรง | แบบสอบถามนำทาง + เส้นทางบันทึกแนวคิดโครงการ (v0.2) | เลือกใช้ได้ |
| ผู้ปฏิบัติงาน | ความรู้จากการทำงานจริง | เหมือนประชาชน และมีอภิธานศัพท์ท้องถิ่น | เลือกใช้ได้ |
| ภาคประชาสังคม | การเป็นตัวแทนชุมชน | เหมือนประชาชน | เลือกใช้ได้ |
| ผู้ประกอบการสังคม | การตั้งโจทย์เชิงประยุกต์ | โหมดผู้เชี่ยวชาญหรือโหมดประชาชน | เลือกใช้ได้ |
| นักศึกษาบัณฑิตศึกษา | การฝึกฝนทางวิชาการบางส่วน | คำแนะนำในโหมดผู้เชี่ยวชาญ | เลือกใช้ได้ |
| อาจารย์ | ความเชี่ยวชาญทางวิชาการ | เส้นทางโหมดผู้เชี่ยวชาญเต็มรูปแบบโดยไม่ใช้ AI (v0.1) | ไม่ต้องใช้ |
| นักวิจัยในมหาวิทยาลัย/นักวิจัยอิสระ | ความเชี่ยวชาญทางวิชาการหรือเชิงประยุกต์ | เส้นทางโหมดผู้เชี่ยวชาญเต็มรูปแบบโดยไม่ใช้ AI (v0.1) | ไม่ต้องใช้ |
| ผู้บริหารงานวิจัย | ความรู้ด้านกระบวนการของสถาบัน | ขั้นตอนทบทวนและล็อก (v0.2) | ไม่ใช้ |
| ผู้ทรงคุณวุฒิ | การตัดสินอย่างอิสระ | เครื่องมือบันทึกการทบทวนแบบระบุชื่อ | ไม่ใช้ |
| พี่เลี้ยง | คำแนะนำ | มุมมองสำหรับการทบทวน | ไม่ใช้ |
| สถาบัน | ข้อมูลสังกัด | บริบทหุ้นส่วนและคุณสมบัติ | ไม่ใช้ |
| เครือข่ายวิจัย | การจับคู่หุ้นส่วน | ตัวชี้ไปยังทำเนียบรายชื่อ (v0.5, สมัครใจ) | ไม่ใช้ |
| แหล่งทุน/PMU | โปรไฟล์ทุนที่มีวันที่กำกับ | ไม่มี — GrantThai แค่อ่านโปรไฟล์ | ไม่ใช้ |
| NRIIS | ระบบปลายทางภายนอกหนึ่งทาง (เส้นทาง `nriis-proposal`) | ไม่มี — GrantThai ไม่ส่งข้อมูลเข้าระบบ | ไม่ใช้ |
| วารสาร/สำนักพิมพ์ | ปลายทางภายนอกอีกทาง (เส้นทาง `academic-article`) | ไม่มี — GrantThai ไม่ระบุชื่อวารสารและไม่อ่านกติกาวารสารเอง นักวิจัยเป็นผู้นำเอกสารของวารสารมาเอง | ไม่ใช้ |
| ผู้ใช้/ผู้นำไปใช้ | การนำผลผลิตไปใช้ต่อ | ไม่มีโดยตรง | ไม่ใช้ |

ช่อง AI เป็น "เลือกใช้ได้" หรือ "ไม่ใช้" เสมอ ไม่เคยเป็น "ต้องใช้" และบังคับจริงด้วย
`spec/common/status_permissions.yaml` (AI ตั้งสถานะได้ไม่เกิน DRAFT)

### 4. การไหล (flows)

- **ความรู้:** ประสบการณ์ตรงและความรู้เชิงวิชาการมาพบกันที่ขั้นการแปล มนุษย์ข้ามสะพานนี้เองได้เสมอ
- **การตรวจ:** ตัวตรวจแบบกำหนดแน่นอน (deterministic validator) เท่านั้นที่ตั้งสถานะ STRUCTURE_CHECKED/LOGIC_LINKED
  บันทึกการทบทวนที่ระบุชื่อบุคคลเท่านั้นที่ตั้ง HUMAN_REVIEWED/VERIFIED และ AI ตั้งสถานะได้ไม่เกิน DRAFT
- **ทุน:** โปรไฟล์ทุนที่มีวันที่กำกับถูกผูกตอน build และเป็นผู้ตัดสินคุณสมบัติ (ELIG001)
- **เส้นทาง (routing):** คนเป็นผู้ประกาศเส้นทาง (`routing` ใน work.yaml หรือ `--route`) เครื่องมือแค่ทำตามอย่างแน่นอน
  ถ้ากำกวมจะหยุดและแสดงตัวเลือก การเลือกเส้นทางไม่ใช่เนื้อหา จึงอยู่นอก `content_sha256` และไม่ทำให้การทบทวนใดล้าสมัย
- **ผลผลิต → ผู้ใช้ → ผลลัพธ์ → ผลกระทบ:** หน้าที่ของ GrantThai จบที่การสร้างไฟล์เดียวของเส้นทางที่เลือก
- **วงย้อนกลับ:** ผลกระทบย้อนกลับไปเป็นปัญหา/ความต้องการใหม่ (`feedback` edges ใน `spec/common/chain.yaml`)

### 5. โครงสร้างพื้นฐานพี่น้อง (ตัวชี้เท่านั้น ไม่คัดลอกเนื้อหา)

Toledo (repository คลังสมการ), glosa (ระเบียบวิธีผลิตความรู้ร่วมมนุษย์-AI) และ main.hub
(ชั้นนำทางระหว่าง repository สาธารณะของผู้ก่อตั้ง) — ลิงก์อยู่ในข้อ 5 ภาษาอังกฤษ

### 6. ขอบเขต — สิ่งที่ GrantThai ไม่ทำ

- ไม่ส่งข้อมูลใด ๆ เข้า NRIIS หรือวารสารใดเองเลย (`direct_submit: false` เสมอ)
- ไม่เลือกเส้นทางแทนคน AI บอกได้ว่ามีเส้นทางอะไรบ้างแล้วถาม แต่ไม่ตัดสินให้
- ไม่เขียนบทความให้ เส้นทางบทความแค่จัดเรียงบันทึกของนักวิจัยเองเป็นภาพรวมต้นฉบับ เนื้อหาแต่ละส่วน การอ้างอิง
  และข้อเท็จจริงเรื่องวารสารเป็นของนักวิจัย (ไม่มีแหล่งที่นักวิจัยนำมา = `NEEDS_VERIFICATION`)
- ไม่ตัดสินคุณสมบัติหัวหน้าโครงการ — เป็นหน้าที่ของโปรไฟล์ทุนที่ผูกไว้ (ELIG001)
- ไม่มอบการรับรองหรือสถานะทางการใด ๆ ผลลัพธ์ของ GrantThai บอกเพียงว่า "ตรวจตามกฎของ GrantThai แล้ว"
  ไม่เคยอ้างว่ามีหน่วยงานภายนอกรับรอง
- ข้อเท็จจริงเกี่ยวกับระบบนิเวศของไทยที่ผูกกับเวลา แสดงเป็นรายการ RELAYED ที่มีวันที่กำกับเท่านั้น
  ไม่ถือเป็นความจริงตายตัว

การตัดสินใจสุดท้ายเป็นของมนุษย์เสมอ
