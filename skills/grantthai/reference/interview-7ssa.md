# Interview guide, 7SSA track (route `academic-article` with a structure profile)

Use this track after the researcher chose the `academic-article` route
(step 0) **and** a 7SSA structure profile (step 0a): `7ssa-world`,
`7ssa-thai-7`, `7ssa-thai-5` or `7ssa-thai-4`
(`grantthai route profiles work.yaml`). 7SSA (Seven-Section Scholarly
Architecture) comes from the founder-authored 7SSA master schema v1.0; the
data GrantThai uses is in `routes/academic-article/profiles/INDEX.yaml`.

The general rules of `reference/interview.md` and
`reference/interview-article.md` apply unchanged: ask in the researcher's
language, two or three questions per turn, `by: researcher` for their words
and `by: ai` for yours, a source for every factual claim, "don't know yet"
stays `NEEDS_INPUT`, no journal facts, you are never an author.

Rules specific to this track:

- **Every sector is the researcher's text.** Each answer becomes one item of
  `ARTICLE.BODY.SECTIONS` with `ssa_sector` (S1-S7) and `ssa_slot` (the
  slot names below), or a key of `ARTICLE.SSA.GAP`,
  `ARTICLE.SSA.CONTRIBUTION` or `ARTICLE.SSA.BEFORE_AFTER`. Never write a
  sector for them and never write "bridging" sentences when sections merge.
- **The source's quality conditions are questions, not verdicts.** "Is the
  gap real?", "is the contribution new?", "is the framework just a list?"
  are things to ask the researcher. Never tell them their gap is weak or
  their contribution is not new; GrantThai judges no knowledge.
- **No quartile gate.** Never tell the researcher an article is or is not
  "Q1 quality". A target system is their own declaration.
- **Objections to their own draft are advisory only.** You may help them
  think of the strongest objection to their own argument (Sector 6); that is
  their draft, never a review record.

## 0. Article type

| Field id | Ask (TH) | Ask (EN) | Notes |
|---|---|---|---|
| `ARTICLE.SSA.ARTICLE_TYPE` | บทความนี้เป็นประเภทไหน: เชิงแนวคิด ทฤษฎี ปรัชญา กฎหมาย การทบทวนเชิงบูรณาการ เชิงรูปนัย SoK หรือเชิงนโยบาย | Which type is this article: conceptual, theory, philosophical, legal, integrative review, formal/mathematical conceptual, CS SoK/survey, or policy/governance? | enum; it picks the English section headings (7SSA v1 §15) and extra S2 slots |

## Writing order

Ask in the suggested writing order 5 -> 4 -> 3 -> 6 -> 2 -> 1 -> 7 (7SSA v1
§22). The reading order in the output stays S1 to S7.

## S5 New contribution (ask first)

| Slot / field | Ask (TH) | Ask (EN) |
|---|---|---|
| `ARTICLE.SSA.CONTRIBUTION.one_sentence` | ข้อเสนอใหม่ของบทความนี้ในประโยคเดียวคืออะไร | What does this article add, in one sentence? |
| `.object_name`, `.contribution_type` | สิ่งที่เสนอชื่ออะไร เป็นแนวคิด กรอบ แบบจำลอง หลักการ หรืออย่างอื่น | What is it called, and what kind of object is it (construct, framework, model, principle ...)? |
| `.nearest_prior`, `.difference_from_prior` | งานเดิมที่ใกล้ที่สุดคืออะไร และต่างกันตรงไหน | What is the nearest existing work, and how does yours differ? |
| items S5 `components`, `relationships`, `mechanism`, `propositions` | ข้อเสนอนี้มีองค์ประกอบอะไร เชื่อมกันอย่างไร | What are its parts and how do they connect? |

## S4 Problem in existing knowledge

| Slot / field | Ask (TH) | Ask (EN) |
|---|---|---|
| `ARTICLE.SSA.GAP.gap_type` | ปัญหาเป็นแบบไหน เช่น แนวคิดคลุมเครือ ข้อขัดแย้ง ขาดกลไก ขาดการจัดประเภท | What kind of problem is it (ambiguity, contradiction, missing mechanism, classification gap ...)? |
| `.unresolved_problem`, `.why_existing_knowledge_fails` | องค์ความรู้เดิมยังตอบอะไรไม่ได้ และเพราะอะไร | What can existing knowledge not answer, and why? |
| `.consequence_if_unresolved` | ถ้าไม่แก้ปัญหานี้ วงวิชาการจะอธิบายหรือตัดสินอะไรไม่ได้ | If it stays unresolved, what can the field not explain or decide? |
| `.strongest_prior_attempt` | งานที่พยายามแก้ปัญหานี้ได้ดีที่สุดคืออะไร | What is the strongest existing attempt? |

## S3 Existing knowledge

| Slot | Ask (TH) | Ask (EN) |
|---|---|---|
| `canonical_sources`, `recent_sources` | งานหลักดั้งเดิมและงานล่าสุดที่ต้องอ้างถึงคืออะไร (ขอแหล่งที่มา) | Which classic and recent works must be cited? (ask for the sources) |
| `competing_literatures` | มีสำนักคิดหรืองานที่เห็นต่างไหม | Which literatures disagree with this view? |
| `constructs`, `theories`, `debates` | แนวคิดและทฤษฎีหลักที่ใช้คืออะไร | Which constructs and theories does the article use? |

## S6 Critical evaluation

| Slot | Ask (TH) | Ask (EN) |
|---|---|---|
| `strongest_objection`, `response` | ใครจะแย้งข้อเสนอนี้อย่างหนักที่สุด และคุณตอบอย่างไร | What is the strongest objection, and your reply? |
| `alternative_explanation`, `counterexample` | มีคำอธิบายทางเลือกหรือกรณีที่ข้อเสนอใช้ไม่ได้ไหม | Is there a rival explanation or a counterexample? |
| `boundary_conditions`, `limitations` | ข้อเสนอนี้ใช้ได้ที่ไหน ใช้ไม่ได้ที่ไหน และมีข้อจำกัดอะไร | Where does it apply, where not, and what are its limits? |
| `theoretical_implications`, `practical_implications`, `future_research` | ถ้ายอมรับข้อเสนอนี้ อะไรเปลี่ยนไป และควรศึกษาอะไรต่อ | What changes if it is accepted, and what should be studied next? |

## S2 Approach, scope and knowledge base

| Slot | Ask (TH) | Ask (EN) |
|---|---|---|
| `methodology` (+ type slots) | บทความนี้ใช้วิธีวิเคราะห์แบบไหน | How does the article reason (its method)? |
| `source_base`, `inclusion_logic`, `exclusions` | ใช้แหล่งความรู้อะไร เลือกอย่างไร ตัดอะไรออก | Which sources, chosen how, and what is excluded? |
| `scope` | ขอบเขตของบทความคืออะไร | What is the scope? |
| review / SoK: `corpus_method`, `synthesis_method` | รวบรวมเอกสารอย่างไร และสังเคราะห์อย่างไร (อย่าเรียกว่า systematic ถ้าไม่มีโปรโตคอล) | How was the corpus built and synthesised? (never call it systematic without a protocol) |
| legal: `legal_sources`, `jurisdiction_scope`, `doctrinal_or_normative_method` | ใช้กฎหมายหรือคำพิพากษาใด เขตอำนาจใด วิธีวิเคราะห์แบบใด | Which legal sources, which jurisdiction, which method? |
| formal: `definitions`, `assumptions`, `formal_system` | นิยาม สมมติฐาน และระบบรูปนัยที่ใช้คืออะไร | Which definitions, assumptions and formal system? |

## S1 Introduction (ask after S2-S6)

| Slot | Ask (TH) | Ask (EN) |
|---|---|---|
| `phenomenon`, `importance` | ปรากฏการณ์หรือปัญหาคืออะไร และสำคัญอย่างไร | What is the phenomenon, and why does it matter? |
| `scholarly_conversation`, `gap_preview` | อยู่ในบทสนทนาทางวิชาการเรื่องใด และยังขาดอะไร | Which scholarly conversation, and what is missing? |
| `central_argument`, `contributions`, `roadmap` | บทความนี้เสนออะไร และจะเดินเรื่องอย่างไร | What does the article argue, and how is it organised? |

## S7 Conclusion (ask last)

| Slot / field | Ask (TH) | Ask (EN) |
|---|---|---|
| item S7 `answer_to_problem` | คำตอบต่อปัญหาในบทนำคืออะไร | What is the answer to the problem posed in the introduction? |
| `ARTICLE.SSA.BEFORE_AFTER.before_state`, `.after_state` | ก่อนบทความนี้วงวิชาการเข้าใจอย่างไร หลังจากนี้ทำอะไรได้เพิ่ม | What did the field understand before, and what can it do after? |
| `.non_claims` | บทความนี้ไม่ได้อ้างอะไรบ้าง | What does the article explicitly not claim? |
| item S7 `next_frontier` | ประเด็นที่ควรศึกษาต่อคืออะไร | What is the next frontier? |

## After the interview

```bash
python scripts/grantthai_skill.py apply answers.yaml --project work.yaml   # project.route + project.structure_profile
python scripts/grantthai_skill.py report --project work.yaml --route academic-article
grantthai build work.yaml --structure-profile 7ssa-thai-4    # the same sectors in four Thai sections
grantthai build work.yaml --format tex                       # English LaTeX draft, build/ACADEMIC_ARTICLE.tex
```

Explain every 7SSA finding with `reference/rules-th.md`. They say only that
a sector or slot is empty or out of order; never turn them into a judgement
of the article.
