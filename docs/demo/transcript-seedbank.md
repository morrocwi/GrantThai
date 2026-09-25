> **FICTIONAL. สมมติทั้งหมด.** This is an AI-simulated interview. The "researcher", every person, village, district, number and field observation in it is invented. It is not a real proposal and not a real person's knowledge.

GrantThai is an independent, unofficial project; see `NOTICE`.

> **FICTIONAL. สมมติทั้งหมด.** Both sides of this transcript were written by one AI assistant, which played the interviewer (following `skills/grantthai/SKILL.md` and `reference/interview.md`) and a simulated researcher persona. Because of that, **nothing here is a source of knowledge**: in `examples/demo-seedbank/project.yaml` no value is `SOURCE`, every value is `DRAFT` or lower, and the file is marked AI-assisted. It is a test of the tool, not evidence about seed banks.

# Simulated interview: community seed-bank learning network (demo topic 1)

- Persona: **นักวิจัยสมมติ ก.** (Fictional Researcher K), a social-science lecturer at "มหาวิทยาลัยสมมติ" (FICTIONAL University), working with farmers in "อำเภอสมมติ", "จังหวัดสมมติ ก" (a fictional district and province in the south).
- Date of the simulation: 2026-09-25. Language: Thai, with English glosses.
- Form the persona says she is filling: the public FF full-proposal form for the 2570 cycle (SD-5 in `docs/sources.md`). GrantThai ships no real fund profile, so the project is bound to the fictional test call `example/FICTIONAL_CALL@0.1` and uses the form profile `ff_full_proposal@nriis-2570` (`NEEDS_VERIFICATION`).

How to read it:

- **AI** = the interviewer. **ผู้วิจัยสมมติ** = the simulated researcher. The simulated researcher's answers are recorded as `by: researcher` with class `DECISION` (never `SOURCE`).
- **AI draft** = wording the AI wrote. It is recorded as `by: ai` unless the persona explicitly adopts it (then `by: researcher_edited_ai_draft`). The "Recorded" line under each turn says which.
- Each turn has an id (T01, T02 ...). In `project.yaml` every value cites its turn as a source (`SRC-T01` ...), kind `PROJECT_DOCUMENT`.

---

### T01 — before we start

**AI:** มีประกาศทุนหรือเอกสารของแหล่งทุนที่จะยื่นอยู่ในมือไหมคะ และมีร่างข้อเสนอโครงการอยู่แล้วหรือยัง
(Do you have the call document? Do you already have a draft?)

**ผู้วิจัยสมมติ:** มีแค่แบบฟอร์มข้อเสนอฉบับสมบูรณ์ของ FF รอบปี 2570 ที่ดาวน์โหลดมา ยังไม่มีประกาศของหน่วยงานตัวเอง ยังไม่มีร่าง มีแต่บันทึกภาคสนามสองปีที่ผ่านมา
(Only the downloaded FF full-proposal form for the 2570 cycle; no call from my own unit yet; no draft, only two years of field notes.)

**AI:** เข้าใจค่ะ ข้อมูลของแหล่งทุนจะใส่ได้เฉพาะที่อ่านจากเอกสารเท่านั้น ส่วนที่ยืนยันไม่ได้จะเขียนว่า `NEEDS_VERIFICATION`

Recorded: `FUND.CALL.FISCAL_YEAR` = 2570 (read from the form's cover, SD-5 p1; marker `NEEDS_VERIFICATION`). `FUND.CALL.NAME`, `FUND.CALL.AGENCY`: the project is bound to the fictional test call, so these name that fictional call. `FUND.CALL.KEY_RESULTS`: `NEEDS_VERIFICATION` (no call document with key results).

### T02 — focus area and plan

**AI:** แบบฟอร์มหน้าแรกให้เลือกจุดมุ่งเน้นได้ไม่เกิน 2 ข้อ งานนี้อยู่ข้อไหนคะ

**ผู้วิจัยสมมติ:** ข้อ 4 งานวิจัยเพื่อการพัฒนาเชิงพื้นที่ ข้อเดียว ไม่ได้ต่อยอดงานเดิม ไม่เลือกข้อ 6

Recorded: `CORE.GENERAL.RESEARCH_ISSUE` and `CORE.GENERAL.PLAN` = focus area 4 as the persona names it (SD-5 p1; marker `NEEDS_VERIFICATION`: which plan her unit files it under is not confirmed). `CORE.ALIGNMENT.FUND_SELECTION`: `NEEDS_VERIFICATION`. Because focus area 6 is not chosen, the SD-5 "work being built on" block does not apply.

### T03 — title, duration, other funders

**AI:** ชื่อโครงการภาษาไทย ระยะเวลา และเคยยื่นเรื่องนี้กับแหล่งทุนอื่นไหมคะ

**ผู้วิจัยสมมติ:** "เครือข่ายเรียนรู้ธนาคารเมล็ดพันธุ์ข้าวพื้นบ้านโดยชุมชน อำเภอสมมติ จังหวัดสมมติ ก" ทำหนึ่งปี ไม่เคยยื่นที่อื่น เป็นโครงการใหม่

**AI draft (English title, a translation):** "A community-led learning network of local rice seed banks in a fictional southern district"

**ผู้วิจัยสมมติ:** ใช้ได้ค่ะ

Recorded: `TITLE_TH`, `DURATION_Y` = 1, `DURATION_M` = 0, `OTHER_FUNDER` = false, `CHARACTERISTIC` (researcher). `TITLE_EN`: AI draft adopted by the persona (`researcher_edited_ai_draft`).

### T04 — keywords and field

**AI:** คำสำคัญ 3-5 คำ และสาขาวิชาหลัก-รองคะ

**ผู้วิจัยสมมติ:** ธนาคารเมล็ดพันธุ์ชุมชน, ข้าวพื้นบ้าน, การวิจัยเชิงปฏิบัติการแบบมีส่วนร่วม, เครือข่ายเรียนรู้ สาขาหลักสังคมศาสตร์ รองสังคมศาสตร์ (6 และ 6.4 ในรายการ)

**AI draft (English keywords, a translation):** community seed bank; local rice varieties; participatory action research; learning network

**ผู้วิจัยสมมติ:** (ไม่ได้ตอบเรื่องคำภาษาอังกฤษ / did not respond about the English keywords)

Recorded: `KEYWORDS_TH`, `OECD.PRIMARY` = 6, `OECD.SECONDARY` = 6.4 (researcher; candidate codes, `NEEDS_VERIFICATION` per the labels file). `KEYWORDS_EN`: AI draft, **not adopted** (silence is not consent), stays `by: ai`.

### T05 — why it matters (need)

**AI:** เรื่องนี้สำคัญต่อพื้นที่หรือชุมชนอย่างไรคะ ใครได้รับผลกระทบ

**ผู้วิจัยสมมติ:** (สมมติ) ชาวนารายย่อยในอำเภอสมมติต้องซื้อเมล็ดพันธุ์ข้าวทุกฤดู ต้นทุนสูงขึ้น และพันธุ์ข้าวพื้นบ้านที่ปรับตัวกับน้ำท่วมขังค่อย ๆ หายไป ถ้าชุมชนเก็บพันธุ์เองได้อย่างมีระบบ จะลดต้นทุนและรักษาพันธุ์ไว้ได้

Recorded: `CORE.RESEARCH.NATIONAL_NEED` (researcher, `DECISION`, source T05).

### T06 — the problem, and how she knows

**AI:** ปัญหาที่เจอจริงคืออะไรคะ รู้ได้จากไหน

**ผู้วิจัยสมมติ:** (สมมติ) จากบันทึกภาคสนามสองปีในสามหมู่บ้าน ครัวเรือนเก็บเมล็ดพันธุ์กันเอง ไม่มีกติกากลาง เมล็ดที่เก็บไว้งอกไม่ดีหลายครั้ง และสองในสามหมู่บ้านบอกว่าพันธุ์พื้นบ้านบางพันธุ์หายไปแล้ว บันทึกมีชื่อคนอยู่ เปิดเผยไม่ได้

Recorded: `CORE.RESEARCH.PROBLEM` (researcher, `DECISION`; sources T06 and the persona's field notes `SRC-FN1`, `contains_personal_data: true`, so it prints `[private]`). Linked to the need.

### T07 — what is already known

**AI:** ตอนนี้รู้อะไรเกี่ยวกับเรื่องนี้อยู่แล้วบ้างคะ ทั้งประสบการณ์และงานวิจัย

**ผู้วิจัยสมมติ:** (สมมติ) ปีที่แล้วบ้านสมมติหนึ่งเคยจัดงานแลกเปลี่ยนเมล็ดพันธุ์ครั้งเดียว คนมาเยอะแต่ไม่มีใครดูแลต่อ ส่วนงานวิจัยที่เกี่ยวข้อง ฉันรู้ว่ามีงาน PAR เรื่องความเข้มแข็งชุมชนบนฐานการทำนาในภาคใต้ แต่ยังไม่ได้ทบทวนวรรณกรรมอย่างเป็นระบบ

**AI:** งั้นส่วนงานวิจัยที่เกี่ยวข้องจะเว้นไว้เป็น `NEEDS_INPUT` จนกว่าอาจารย์จะทบทวนเองนะคะ ดิฉันจะไม่เติมชื่องานวิจัยให้

Recorded: `CORE.PRIORKNOWLEDGE.PK1` = the one-off exchange event (researcher, `DECISION`, sources T07 and `SRC-FN1`). `CORE.PRIORKNOWLEDGE.PK2` (literature) = `NEEDS_INPUT`. `CORE.NARRATIVE.REFERENCES` = `NEEDS_INPUT`.

### T08 — the gap

**AI draft (gap):** "ยังไม่มีกติกาและกระบวนการที่ชุมชนออกแบบเองสำหรับธนาคารเมล็ดพันธุ์ระดับหมู่บ้านที่เชื่อมกันเป็นเครือข่าย และยังไม่รู้ว่าเงื่อนไขใดทำให้ธนาคารเมล็ดพันธุ์ดำเนินต่อได้หลังโครงการจบ"

**ผู้วิจัยสมมติ:** ใช่ ใช้ตามนี้ แต่เติมคำว่า "ในอำเภอสมมติ" ด้วย

Recorded: `CORE.RESEARCH.GAP` (AI draft edited and adopted: `researcher_edited_ai_draft`, class `INFERENCE`). Linked to PK1 only (PK2 is empty).

### T09 — research questions

**AI:** คำถามหลักที่งานนี้จะตอบคืออะไรคะ มีคำถามรองไหม

**ผู้วิจัยสมมติ:** คำถามหลัก: ธนาคารเมล็ดพันธุ์ที่ชุมชนออกแบบกติกาเองและเชื่อมกันเป็นเครือข่ายสามหมู่บ้าน ช่วยให้ครัวเรือนเข้าถึงเมล็ดพันธุ์ข้าวพื้นบ้านที่งอกดีในฤดูถัดไปได้หรือไม่ ภายใต้เงื่อนไขใด คำถามรอง: (1) ตอนนี้มีพันธุ์อะไรเหลืออยู่ ใครรู้วิธีเก็บ (2) กติกาแบบไหนที่คนยอมทำตามจริง

Recorded: `CORE.RESEARCH.RQ.PRIMARY` (linked to the gap), `CORE.RESEARCH.RQ.SECONDARY` (researcher).

### T10 — objectives

**AI:** ทำโครงการนี้เพื่อให้ได้อะไร เป็นข้อ ๆ ค่ะ แต่ละข้อตอบคำถามไหน

**ผู้วิจัยสมมติ:** 1) สำรวจพันธุ์ข้าวพื้นบ้านและความรู้การเก็บเมล็ดพันธุ์ในสามหมู่บ้าน 2) ออกแบบและทดลองกติกาธนาคารเมล็ดพันธุ์ร่วมกับผู้ร่วมวิจัยชุมชน 3) สร้างเครือข่ายเรียนรู้ข้ามหมู่บ้านและคู่มือ ทุกข้อตอบคำถามหลัก

Recorded: `CORE.RESEARCH.OBJECTIVES` OBJ1–OBJ3 (researcher), `CORE.NARRATIVE.OBJECTIVES` (her sentence).

### T11 — design and phases

**AI:** ใช้การวิจัยแบบไหน แบ่งกี่ขั้นคะ

**ผู้วิจัยสมมติ:** PAR สามวง วางแผน-ลงมือ-สังเกต-สะท้อนคิด วงแรกสำรวจ วงสองตั้งและทดลองธนาคาร วงสามสะท้อนผลและขยายเครือข่าย ใช้ข้อมูลเชิงคุณภาพเป็นหลัก มีตัวเลขง่าย ๆ คืออัตราการงอก จำนวนพันธุ์ จำนวนครัวเรือนที่ยืมและคืนเมล็ด

Recorded: `METHOD.PLAN.DESIGN` with phases MP1–MP3 linked to OBJ1–OBJ3 (researcher).

### T12 — who takes part, instruments

**AI:** เก็บข้อมูลกับใคร กี่คน เลือกอย่างไร ใช้เครื่องมืออะไรคะ

**ผู้วิจัยสมมติ:** สามหมู่บ้าน หมู่บ้านละประมาณ 20 ครัวเรือนที่ทำนาและอยากเข้าร่วม เลือกแบบเจาะจง มีผู้ร่วมวิจัยชุมชนหมู่บ้านละหนึ่งคนเป็นแกนหลัก และผู้อาวุโสที่รู้เรื่องพันธุ์ข้าวหมู่บ้านละ 3-5 คน เครื่องมือ: แบบบันทึกทะเบียนพันธุ์ แบบบันทึกทดสอบความงอก แนวคำถามสัมภาษณ์กึ่งโครงสร้าง และแบบบันทึกเวทีสะท้อนคิด ให้เพื่อนอาจารย์สองคนอ่านตรวจ และลองใช้ในหมู่บ้านเดียวก่อน

Recorded: `METHOD.PLAN.SAMPLE`, `METHOD.PLAN.INSTRUMENTS` INS1–INS4, `METHOD.PLAN.DATA_COLLECTION` DC1–DC3, `METHOD.PLAN.ANALYSIS` (researcher).

### T13 — ethics

**AI:** เกี่ยวกับคนไหมคะ ขอความยินยอมอย่างไร เก็บข้อมูลส่วนบุคคลอย่างไร ยื่นกรรมการจริยธรรมหรือยัง

**ผู้วิจัยสมมติ:** เกี่ยวกับคน ผู้อาวุโสหลายคนอ่านหนังสือไม่คล่อง จะอ่านเอกสารให้ฟังและขอความยินยอมเป็นวาจาต่อหน้าพยาน แล้วลงนามหรือพิมพ์ลายนิ้วมือ ใช้รหัสแทนชื่อ ถอนตัวได้ทุกเมื่อ ยังไม่ได้ยื่นกรรมการจริยธรรมของมหาวิทยาลัย จะยื่นก่อนลงพื้นที่

Recorded: `METHOD.PLAN.ETHICS` (researcher). `COMP.STANDARD.HUMAN` = to be submitted (researcher; the committee route is `NEEDS_VERIFICATION`). `DOC.ATTACHMENTS.DOCUMENTS` ATT1 = ethics approval, not yet supplied.

### T14 — team and partners

**AI:** ใครอยู่ในทีม บทบาท และสัดส่วนงาน (รวม 100) มีหน่วยงานหรือกลุ่มในชุมชนร่วมไหมคะ

**ผู้วิจัยสมมติ:** ฉันเป็นหัวหน้าโครงการ 50% นักวิจัยสมมติ ข. อาจารย์สายพืชศาสตร์ 30% ดูเรื่องทดสอบความงอก ผู้ร่วมวิจัยชุมชนสามคน คนละประมาณ 7% ... ขอเป็น 7, 7, 6 นะ กลุ่มเกษตรกรทำนาสมมติของอำเภอให้ใช้ศาลาเป็นที่ประชุมและเก็บเมล็ด ไม่คิดเงิน

**AI:** ในระบบไม่มีบทบาท "ผู้ร่วมวิจัยชุมชน" ตรง ๆ ขอใช้ `OTHER` แล้วเขียนหน้าที่ไว้นะคะ

**ผู้วิจัยสมมติ:** ได้

Recorded: `PROFILE.TEAM.MEMBERS` TM1–TM5 (researcher; community co-researchers as `OTHER`, a GrantThai gap noted in `docs/demo/comparison.md`). `WORK.PARTNERS.ORGANIZATIONS` P1 with in-kind basis. Names are invented persona labels.

### T15 — workplan and sites

**AI:** ทำอะไรบ้าง เดือนไหน ใครรับผิดชอบ น้ำหนักงานกี่เปอร์เซ็นต์ ลงพื้นที่ที่ไหนคะ

**ผู้วิจัยสมมติ:** เดือน 1-2 เตรียมงาน ขอจริยธรรม ตั้งทีมชุมชน 15% เดือน 2-6 สำรวจพันธุ์และความรู้ 30% เดือน 5-10 ตั้งและทดลองธนาคาร ทดสอบความงอก 35% เดือน 10-12 เวทีสะท้อนคิด งานแลกเปลี่ยนเครือข่าย ทำคู่มือและรายงาน 20% สามหมู่บ้านในอำเภอสมมติ

Recorded: `WORK.PLAN.ACTIVITIES` ACT1–ACT4 (weights sum 100), `GEO.AREA.RESEARCH_SITES` SITE1–SITE3 (researcher).

### T16 — risks

**AI:** อะไรอาจทำให้โครงการไม่สำเร็จ จะป้องกันอย่างไรคะ

**ผู้วิจัยสมมติ:** น้ำท่วมช่วงปลายปีทำให้ลงพื้นที่ไม่ได้ ครัวเรือนยืมเมล็ดแล้วไม่คืน และความรู้ของผู้อาวุโสถูกนำไปใช้โดยไม่ให้เครดิต

Recorded: `WORK.PLAN.RISKS` RSK1–RSK3 (researcher; the mitigations are her words).

### T17 — budget

**AI:** ใช้เงินกับอะไรบ้าง จำนวน กี่คน กี่ครั้ง ราคาต่อหน่วยเท่าไร ใช้ในกิจกรรมไหนคะ ดิฉันจะคูณให้ดูแต่ตัวเลขเป็นของอาจารย์

**ผู้วิจัยสมมติ:** (สมมติ) ผู้ช่วยวิจัยภาคสนาม 1 คน 10 เดือน เดือนละ 12,000; เวทีชุมชน 3 หมู่บ้าน 4 ครั้ง ครั้งละ 15,000; วัสดุทดสอบความงอก 3 หมู่บ้าน ชุดละ 20,000; ค่าเดินทาง 2 คน 12 เดือน เดือนละ 2,500; พิมพ์คู่มือ 300 เล่ม เล่มละ 100; งานแลกเปลี่ยนเครือข่าย 1 ครั้ง 30,000 ไม่มีครุภัณฑ์ ไม่มีค่าตอบแทน

**AI (arithmetic shown):** 120,000 + 180,000 + 60,000 + 60,000 + 30,000 + 30,000 = 480,000

**ผู้วิจัยสมมติ:** ถูกต้อง ขอ 480,000

Recorded: `BUDGET.PLAN.ITEMS` BI1–BI6, `BUDGET.PLAN.YEARS`, `BUDGET.PLAN.TOTAL`, `REQUESTED_BUDGET`, `TOTAL_BUDGET` (researcher; totals `DERIVED`). Budget categories are the persona's words; the FF category rules on SD-5 p9 are listed by the form profile, not checked.

### T18 — outputs, users, change

**AI:** จบโครงการแล้วจะได้อะไรเป็นชิ้น ๆ ใครจะนำไปใช้ และจะเกิดการเปลี่ยนแปลงอะไรคะ

**ผู้วิจัยสมมติ:** ทะเบียนพันธุ์และความรู้การเก็บเมล็ด 1 ชุด กติกาธนาคารเมล็ดพันธุ์ 3 หมู่บ้าน คู่มือ 1 เล่ม และข้อเสนอเชิงนโยบายถึงสำนักงานเกษตรของอำเภอสมมติ คนใช้คือคณะกรรมการธนาคารเมล็ดพันธุ์สามหมู่บ้าน และเจ้าหน้าที่ส่งเสริมการเกษตรของอำเภอ หวังว่าครัวเรือนจะยืมและคืนเมล็ดพันธุ์ตามกติกา ในระยะยาวอาจช่วยรักษาพันธุ์ข้าวพื้นบ้านของอำเภอ แต่ไม่กล้าบอกว่าเป็นผลของโครงการนี้อย่างเดียว

Recorded: `RESULTS.CHAIN.OUTPUTS` OUT1–OUT4, `RESULTS.CHAIN.USERS`, `RESULTS.CHAIN.OUTCOME_PROCESS`, `RESULTS.CHAIN.OUTCOMES`, `RESULTS.CHAIN.IMPACTS` (claim strength `CONTRIBUTORY`, her own caution), `RESULTS.CHAIN.BENEFICIARIES`, `RESULTS.PATHWAY.SUSTAINABILITY` (researcher). A "policy proposal" has no dedicated output type in GrantThai (gap noted). Output types against the form's 10 output types: `NEEDS_VERIFICATION`.

### T19 — evidence and expected claim

**AI:** มีหลักฐานอะไรที่ทำให้เชื่อว่าแนวทางนี้น่าจะได้ผล และคาดว่าจะสรุปได้ว่าอะไรคะ

**ผู้วิจัยสมมติ:** (สมมติ) หลักฐานมีแค่งานแลกเปลี่ยนครั้งเดียวในบ้านสมมติหนึ่งที่คนสนใจมาก ยังอ่อนอยู่ สิ่งที่คาดว่าจะสรุปได้คือ ธนาคารเมล็ดพันธุ์ที่ชุมชนตั้งกติกาเองทำได้จริงในหมู่บ้านแบบนี้ และรู้ว่าเงื่อนไขอะไรช่วยหรือขัดขวาง

Recorded: `CORE.EVIDENCE.E1` (researcher, `DECISION`, claim cap `CONTRIBUTORY`, her own "still weak"), `CORE.CLAIM.C1` (`INFERENCE`).

### T20 — narrative boxes

**AI draft (summary, assembled from T05–T19):** see `CORE.NARRATIVE.SUMMARY` in `project.yaml`.

**AI draft (rationale, assembled from T05–T09):** see `CORE.NARRATIVE.RATIONALE`.

**AI draft (method narrative, assembled from T11–T13):** see `CORE.NARRATIVE.METHOD`.

**ผู้วิจัยสมมติ:** หลักการและเหตุผลกับวิธีวิจัยใช้ได้ ส่วนบทสรุปขอไปเขียนเองทีหลัง กรอบแนวคิดกับทฤษฎีฉันเขียนเอง: "กติกาที่ชุมชนตั้งเอง ทำให้การยืม-คืนเมล็ดพันธุ์คาดการณ์ได้ ทำให้พันธุ์พื้นบ้านถูกปลูกซ้ำทุกฤดู" ทฤษฎีคือแนวคิดการจัดการทรัพยากรร่วมและทุนทางสังคม แต่ยังไม่ได้ใส่อ้างอิง

Recorded: `CORE.NARRATIVE.RATIONALE`, `CORE.NARRATIVE.METHOD`: AI drafts adopted (`researcher_edited_ai_draft`). `CORE.NARRATIVE.SUMMARY`: AI draft **not adopted**, stays `by: ai` (the persona will rewrite it). `CORE.NARRATIVE.FRAMEWORK`, `CORE.NARRATIVE.THEORY`: researcher, with references still `NEEDS_INPUT`. `CORE.NARRATIVE.IP_CHECK`: `NEEDS_INPUT` (not done).

### T21 — hand-back

**AI:** ไฟล์ที่ได้คือ `build/NRIIS_SUBMISSION.md` ไฟล์เดียว ผลตรวจเป็นเรื่องโครงสร้างและการเชื่อมโยงเท่านั้น ไม่ได้บอกว่างานถูกต้องหรือได้ทุน ยังมีช่องที่ต้องยืนยันกับแหล่งทุน (`NEEDS_VERIFICATION`) ช่องที่ยังไม่มีข้อมูล (`NEEDS_INPUT`) และข้อความที่ดิฉันร่างซึ่งอาจารย์ยังไม่ได้ยืนยัน อาจารย์เป็นผู้กรอกและยื่นใน NRIIS เองค่ะ

**ผู้วิจัยสมมติ:** รับทราบ

> **FICTIONAL. สมมติทั้งหมด.** End of the simulated transcript.
