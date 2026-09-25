# Interview guide: questions mapped to field ids

Ask in the researcher's language (Thai first by default). The Thai
questions below are GrantThai's own plain wording. They are **not** NRIIS
field labels; never present them as official labels.

How to run the interview:

- One topic at a time, two or three questions per turn. Let the researcher
  answer in their own words, even in bullet points or voice notes.
- Record answers as `by: researcher`. If you rephrase, summarise, translate
  or suggest, record that as `by: ai` and show it to the researcher
  (`provenance.md`).
- For every factual claim, ask "รู้เรื่องนี้จากไหน / where does this come
  from?" and record the answer as a source. Lived experience and fieldwork
  count (`LIVED_EXPERIENCE_ACCOUNT`, `PRACTITIONER_KNOWLEDGE`,
  `PRIMARY_DATA`).
- "Don't know yet" is a valid answer: leave `NEEDS_INPUT`. A fund or NRIIS
  detail nobody can confirm from the current call document is
  `NEEDS_VERIFICATION`.
- Mark (R) = required in v0.1. The authoritative list, types and allowed
  values are `grantthai fields` and `registry/fields.jsonl`.
- Item ids have a fixed prefix per field plus a number (`OBJ1`, `ACT2`).
  Ids must be unique in the whole file.

## 0. Before you start

| Ask (TH) | Ask (EN) | Why |
|---|---|---|
| มีประกาศทุนหรือเอกสารของแหล่งทุนที่จะยื่นอยู่ในมือไหม ขอดูได้ไหม | Do you have the call announcement or fund document? Can you share it? | Fund facts come only from that document. Without it, fund fields are `NEEDS_VERIFICATION`. |
| ตอนนี้มีข้อเสนอโครงการฉบับร่างอยู่แล้วหรือยัง | Do you already have a draft proposal? | If yes, extract from it field by field (`by: researcher`, the draft is theirs) and ask only for what is missing. |

## 1. The fund call (from the call document only)

| Field id | Ask (TH) | Ask (EN) | Notes |
|---|---|---|---|
| `FUND.CALL.FISCAL_YEAR` (R) | ทุนนี้เป็นของปีงบประมาณไหน | Which fiscal year is this call for? | integer |
| `FUND.CALL.NAME` (R) | ชื่อประกาศทุนตามเอกสารคืออะไร | What is the call's name, as written in the document? | copy exactly |
| `FUND.CALL.AGENCY` (R) | หน่วยงานไหนเป็นผู้ให้ทุน | Which agency funds it? | |
| `FUND.CALL.PLAN.NAME`, `FUND.CALL.PROGRAM.NAME` | ประกาศระบุแผนหรือแผนงานย่อยไว้ไหม | Does the call name a plan or programme? | optional |
| `FUND.CALL.KEY_RESULTS` | ประกาศมีผลลัพธ์สำคัญ (Key Results) ที่โครงการต้องตอบไหม | Does the call list key results to address? | items `KR1..`: `code`, `statement`, `numeric_target`, `target_unit`, `target_period`; stored in chain node KR |
| `CORE.GENERAL.RESEARCH_ISSUE` (R), `CORE.GENERAL.PLAN` (R) | จะยื่นในประเด็นหรือแผนไหนของทุนนี้ | Which issue/plan of the call are you applying under? | copy from the call; otherwise `NEEDS_VERIFICATION` |
| `CORE.ALIGNMENT.FUND_SELECTION` | งานนี้ตอบวัตถุประสงค์ข้อไหนของทุน และ Key Result หลักคือข้อไหน | Which call objectives does this serve, and which is the one primary key result? | `objective_ids`, `primary_kr_id`, `secondary_kr_ids` (ids from the call's items) |
| `CORE.ALIGNMENT.STATEMENT` | สรุปในประโยคเดียวว่างานนี้ช่วยเป้าหมายของทุนอย่างไร | One sentence: how does this project serve the call? | formula: contributes to [KR] by [mechanism], producing [output] for use by [user] |
| `CORE.ALIGNMENT.POLICY_PATHWAY` | ถ้าเลือกมุมนโยบายได้หนึ่งมุม งานนี้อยู่มุมไหน | If you pick one policy lens, which is it? | one code from `ecosystem/positions@2026-09.yaml` lenses (RELAYED); optional, never forced |

## 2. General information

| Field id | Ask (TH) | Ask (EN) | Notes |
|---|---|---|---|
| `CORE.GENERAL.TITLE_TH` (R) | ชื่อโครงการภาษาไทย | Project title in Thai | |
| `CORE.GENERAL.TITLE_EN` (R) | ชื่อโครงการภาษาอังกฤษ | Project title in English | if you translate it: `by: ai` |
| `CORE.GENERAL.DURATION_Y` (R), `CORE.GENERAL.DURATION_M` (R) | โครงการใช้เวลากี่ปี กี่เดือน | How many years and months? | integers |
| `CORE.GENERAL.OTHER_FUNDER` (R) | เคยยื่นโครงการนี้หรือโครงการใกล้เคียงกับแหล่งทุนอื่นไหม | Submitted this or a similar project to another funder? | boolean; if true also `...OTHER_FUNDER.AGENCY`, `.TITLE`, `.DIFF` (rule S005) |
| `CORE.GENERAL.KEYWORDS_TH` (R), `CORE.GENERAL.KEYWORDS_EN` (R) | คำสำคัญ 3-5 คำ ภาษาไทยและอังกฤษ | 3-5 keywords, Thai and English | lists of strings |
| `CORE.GENERAL.OECD.PRIMARY` (R), `CORE.GENERAL.OECD.SECONDARY` (R) | สาขาวิชาหลักและรองของงานนี้คืออะไร | Primary and secondary research field? | candidate codes (main group `6`, sub-field `6.4` ...) are in `mappings/nriis/labels@nrct-manual-2566.yaml` from a public manual: still `NEEDS_VERIFICATION`; a value outside the list gets REVIEW S011 |
| `CORE.GENERAL.ISCED.BROAD`, `.NARROW`, `.DETAILED` | สาขาตาม ISCED (กว้าง แคบ ละเอียด) | ISCED broad, narrow and detailed field? | option list `NEEDS_VERIFICATION` |
| `CORE.GENERAL.CHARACTERISTIC`, `CORE.GENERAL.PAST_PERFORMANCE` | เป็นโครงการใหม่หรือโครงการต่อเนื่อง ถ้าต่อเนื่อง ผลงานปีก่อน ๆ เป็นอย่างไร | New or continuing project? If continuing, past years' results? | `Continuing Project` is a candidate value (REVIEW S011, CX-05); then items `PP1..`: `fiscal_year`, `performance_vs_plan_percent`, `budget_allocated`, `budget_used`, `budget_used_percent` (S005) |
| `CORE.GENERAL.PROGRAMME_NAME`, `CORE.GENERAL.SUBPROJECTS` | โครงการนี้อยู่ในชุดโครงการไหม มีโครงการย่อยไหม | Part of a programme? Any sub-projects? | items `SUB1..`: `title_th`, `title_en`, `lead_person_id`, `contribution_to_shared_goal` |
| `CORE.GENERAL.REQUESTED_BUDGET` (R), `CORE.GENERAL.TOTAL_BUDGET` (R) | ขอทุนเท่าไร งบรวมทั้งโครงการเท่าไร | Requested amount and total project budget? | must equal the sum of budget lines (B002); ask after section 8 |

## 3. Team (`PROFILE.TEAM.MEMBERS`, R)

| Ask (TH) | Ask (EN) |
|---|---|
| ใครอยู่ในทีมบ้าง ชื่อ หน่วยงาน บทบาท | Who is on the team: name, organisation, role? |
| ใครเป็นหัวหน้าโครงการ (มีได้คนเดียว) | Who is the PI (exactly one)? |
| แต่ละคนมีส่วนร่วมกี่เปอร์เซ็นต์ (รวมกันต้องได้ 100) | Each person's contribution %, summing to 100? |
| แต่ละคนรับผิดชอบงานอะไร | What is each person responsible for? |

Items `TM1..`: `full_name`, `organization`, `project_role` (`PI`, `CO_PI`,
`CO_RESEARCHER`, `ADVISOR`, `RESEARCH_ASSISTANT`, `OTHER`; these are GrantThai
codes, the official NRIIS role labels are `NEEDS_VERIFICATION`), `contribution_percent`,
`registration_status`, `orcid`, `responsibilities` (list),
`eligibility_facts` (only facts the researcher states; the fund profile
decides eligibility, rule ELIG001). Rules T001, T002.

Related, optional: `PROFILE.TEAM.EXPERTISE` (items `TEX1..`: `person_id`,
`position`, `expertise`, `special_interests`, `ongoing_projects`: ask
"ตอนนี้แต่ละคนทำโครงการอื่นอะไรอยู่บ้าง"), `PROFILE.TEAM.CREDENTIALS` (items
`CRD1..`: ethics, human-research and laboratory training), and, only when
the bound call asks for them, `PROFILE.TEAM.PI_TRACK_RECORD` (items
`PTR1..`, the lead's relevant work in the last five years) and
`PROFILE.TEAM.PI_MANAGEMENT_EXPERIENCE`. Write only what the researcher
states.

Never add yourself (the AI) as a team member.

## 3a. What funded work usually has: ask for it

The 100 funded final reports in the GrantThai corpus
(`docs/practice/funded-work-patterns.md`) share a few parts. Ask for them
during sections 4 to 9 below. They are **practice, not fund rules**: say
the count when it helps ("77 of 100 funded reports number their
objectives"), never "the fund requires it". The researcher decides.

| Pattern (tier, evidence) | Ask (TH) | Ask (EN) | Field ids |
|---|---|---|---|
| Numbered objectives, each tied to a method (CORE, 77/100; FW002) | วัตถุประสงค์มีกี่ข้อ ขอเป็นข้อ 1) 2) 3) ข้อละหนึ่งเป้าหมาย แต่ละข้อจะตอบด้วยวิธีการหรือขั้นตอนไหน | How many objectives? Please give them as 1) 2) 3), one aim each. Which method step answers each one? | `CORE.RESEARCH.OBJECTIVES` (`method_ids`), `CORE.NARRATIVE.OBJECTIVES` |
| A reference list behind the theory (CORE, 78/100; FW001) | แนวคิดหรือผลการศึกษาเดิมที่ใช้ มาจากเอกสารเรื่องไหนบ้าง ขอรายการอ้างอิง | Which works do the concepts and prior findings come from? Please list the references. | `CORE.NARRATIVE.REFERENCES`, `CORE.NARRATIVE.THEORY` |
| Literature scope as a topic list ending in related studies (CONTEXTUAL, 64/100, rising) | จะทบทวนวรรณกรรมเรื่องอะไรบ้าง เรียงตามวัตถุประสงค์ได้ไหม งานวิจัยใกล้เคียงที่สุดมีเรื่องไหน | Which topics will the review cover, in objective order? Which earlier studies are closest to this one? | `CORE.RESEARCH.THEORETICAL_FOUNDATIONS`, `CORE.PRIORKNOWLEDGE.*`, `CORE.RESEARCH.GAP` |
| Population, sample basis, instruments, analysis (CONTEXTUAL, 66/100; sample basis EMERGING, 35/100) | ประชากรคือใคร ขนาดตัวอย่างคิดจากอะไร (สูตร ค่าที่ใช้ แหล่งที่มา) ใช้เครื่องมืออะไร ตรวจคุณภาพอย่างไร วิเคราะห์แต่ละวัตถุประสงค์ด้วยวิธีใด | Who is the population? What is the sample-size basis (method, parameters, source)? Which instruments, checked how? Which analysis answers each objective? | `METHOD.PLAN.POPULATION`, `.SAMPLE`, `.INSTRUMENTS`, `.QUALITY`, `.ANALYSIS` |
| Ethics written inside the method (EMERGING, 29/100; undercounted) | ขอความยินยอมอย่างไร ผู้ร่วมถอนตัวได้ไหม เก็บรักษาข้อมูลนานเท่าไร จะยื่นคณะกรรมการจริยธรรมที่ไหน | How is consent obtained? Can participants withdraw? How long are data kept? Which ethics committee will review it? | `METHOD.PLAN.ETHICS`, `COMP.STANDARD.HUMAN` |
| Who receives the recommendations (CONTEXTUAL, 59/100, concentrated in health-systems work; users named EMERGING, 16/100) | ถ้าผลนำไปสู่ข้อเสนอแนะ หน่วยงานหรือระดับไหนควรนำไปใช้ และจะใช้เรื่องอะไร | If the results lead to recommendations, which agency or level should act, and on what? | `RESULTS.CHAIN.USERS`, `RESULTS.CHAIN.UTILIZATION_DESC` |
| Known limitations of data and design (EMERGING, 15/100) | แหล่งข้อมูลหรือแบบการวิจัยมีข้อจำกัดอะไรที่รู้อยู่แล้ว จะจัดการอย่างไร | What known limits do the data sources or design have, and how will you handle them? | `METHOD.PLAN.QUALITY` |

`grantthai explain <FIELD_ID>` shows the full practice entry (advice in
English and Thai, what not to do, and the deep-read report pages).

## 4. The research chain (Need to RQ to Objectives)

This is the heart of the file. Each step links to the one before it.

| Field id | Chain node | Ask (TH) | Ask (EN) | Links |
|---|---|---|---|---|
| `CORE.RESEARCH.NATIONAL_NEED` (R) | Need | ปัญหานี้สำคัญต่อประเทศ พื้นที่ หรือชุมชนอย่างไร | Why does this matter for the country, area or community? | |
| `CORE.RESEARCH.PROBLEM` (R) | Problem | ปัญหาที่เจอจริงคืออะไร รู้ได้อย่างไร มีข้อมูลหรือเอกสารอะไรยืนยัน | What exactly is the problem, and how do you know? | `links.need_ids`; ask for a source (R001) |
| `CORE.PRIORKNOWLEDGE.PK1..` | PriorKnowledge | ตอนนี้รู้อะไรเกี่ยวกับเรื่องนี้อยู่แล้ว มีงานวิจัย รายงาน หรือประสบการณ์อะไรบ้าง | What is already known: studies, reports, experience? | `chain_node: PriorKnowledge`, `links.problem_ids`, a source each (R002) |
| `CORE.RESEARCH.GAP` (R) | Gap | สิ่งที่ยังไม่มีใครรู้ หรือยังทำไม่ได้ คืออะไร | What is still unknown or not yet possible? | `links.prior_knowledge_ids` (R002) |
| `CORE.RESEARCH.RQ.PRIMARY` (R) | RQ | คำถามหลักที่งานนี้จะตอบคืออะไร | What main question will this project answer? | `links.gap_ids` (R003) |
| `CORE.RESEARCH.RQ.SECONDARY` | | มีคำถามรองไหม | Any secondary questions? | list of text |
| `CORE.RESEARCH.OBJECTIVES` (R) | Objective | ทำโครงการนี้เพื่อให้ได้อะไร เป็นข้อ ๆ | What will the project achieve, point by point? | items `OBJ1..`: `statement`, `rq_ids` (R004), `method_ids` (R005), `output_ids`, `kr_ids` |
| `CORE.RESEARCH.INNOVATION` | | อะไรใหม่ในงานนี้ | What is new here? | optional; text, or an object `what_is_new`, `compared_with`, `scientific_contribution`, `practical_contribution`, `policy_or_system_contribution` |
| `CORE.RESEARCH.THEORETICAL_FOUNDATIONS`, `CORE.RESEARCH.BOUNDARY_CONDITIONS` | Framework | งานนี้ตั้งอยู่บนทฤษฎีอะไร และกรอบนี้ใช้ได้ในขอบเขตไหน | Which theories does it rest on, and where does the framework hold? | lists of text; optional |
| `CORE.RESEARCH.HYPOTHESES`, `CORE.RESEARCH.PROPOSITIONS` | Hypothesis | มีสมมติฐาน (จะทดสอบอย่างไร) หรือข้อเสนอที่จะสำรวจไหม | Hypotheses (and how each is tested) or propositions to explore? | hypothesis items `HYP1..` need `proposed_test` (R009); propositions are a list of text |

Need, Problem and Gap may be plain text, or an object with the keys
`statement`, `context`, `evidence` ... (spec/registry/structured_fields.schema.json;
contradiction CX-02).

## 5. Method

| Field id | Chain node | Ask (TH) | Ask (EN) | Keys / links |
|---|---|---|---|---|
| `METHOD.PLAN.DESIGN` (R) | Method | ใช้การวิจัยแบบไหน เชิงปริมาณ เชิงคุณภาพ หรือผสม แบ่งเป็นกี่ขั้น | Which design and approach? What phases? | `paradigm`, `design_type`, `approach`, `quantitative_component`, `qualitative_component`, `phases` (items `MP1..`: `name`, `description`, `objective_ids`) |
| `METHOD.PLAN.SAMPLE` (R) | Method | เก็บข้อมูลกับใคร กี่คน เลือกอย่างไร ทำไมจำนวนนี้พอ | Who, how many, how chosen, why enough? | `sampling_method`, `groups` (items `SG1..`: `description`, `target_n`), `sample_size_justification` |
| `METHOD.PLAN.POPULATION` | | ประชากรเป้าหมายคือใคร เกณฑ์คัดเข้าคัดออก | Target population, inclusion/exclusion? | optional |
| `METHOD.PLAN.INSTRUMENTS` (R) | Method | ใช้เครื่องมืออะไรเก็บข้อมูล ตรวจคุณภาพเครื่องมืออย่างไร | Which instruments, and how are they checked? | items `INS1..`: `name`, `purpose`, `construct_ids` or `construct_measured` (R008), `instrument_type`, `validity_method`, `reliability_method` |
| `METHOD.PLAN.DATA_COLLECTION` (R) | Data | เก็บข้อมูลอะไร จากใคร เมื่อไร ใครเก็บ | What data, from whom, when, by whom? | items `DC1..`: `source`, `collection_method`, `timing`, `method_ids` (R006), `instrument_ids`, `activity_ids`, `responsible_person_ids` |
| `METHOD.PLAN.ANALYSIS` (R) | Analysis | จะวิเคราะห์ข้อมูลอย่างไร ใช้โปรแกรมอะไร | How will you analyse the data, with what tools? | `quantitative_methods` (list), `qualitative_method`, `software_or_tools` (list), `data_ids` (R007) |

## 6. Ethics

| Field id | Chain node | Ask (TH) | Ask (EN) | Keys |
|---|---|---|---|---|
| `METHOD.PLAN.ETHICS` (R) | EthicsRequirement | งานนี้เกี่ยวกับคนไหม ขอความยินยอมอย่างไร เก็บข้อมูลส่วนบุคคลอย่างไร ผู้ร่วมถอนตัวได้ไหม มีความเสี่ยงอะไร | Human participants? Consent, privacy, withdrawal, risks? | `human_participants`, `informed_consent`, `privacy`, `confidentiality`, `withdrawal`, `compensation`, `risk_level`, `risk_management`, `vulnerable_groups`, `conflict_of_interest` |
| `COMP.STANDARD.HUMAN` | | ยื่นคณะกรรมการจริยธรรมแล้วหรือยัง ที่ไหน | Ethics committee submission status? | `applicable`, `status`, `committee`, `protocol_number`, `approval_date`, `attachment_ids` |

## 7. Workplan and sites

| Field id | Chain node | Ask (TH) | Ask (EN) | Keys / links |
|---|---|---|---|---|
| `WORK.PLAN.ACTIVITIES` (R) | Activity | ทำอะไรบ้าง เดือนไหน ใครรับผิดชอบ แต่ละกิจกรรมคิดเป็นน้ำหนักงานกี่เปอร์เซ็นต์ | Which activities, which months, who, what weight %? | items `ACT1..`: `year`, `name`, `months` (list), `weight_percent` (sum 100, W003), `objective_ids`/`method_ids` (W001), `output_ids` (W004), `budget_item_ids` (B001), `depends_on_activity_ids` (no cycles, CH001), `responsible_person_ids` (W002) |
| `GEO.AREA.RESEARCH_SITES` (R) | | ลงพื้นที่ที่ไหน | Where is the fieldwork? | items `SITE1..`: `location_type`, `country`, `province`, `place_name`, `site_role`, `activity_ids` |
| `WORK.PARTNERS.ORGANIZATIONS` | | มีหน่วยงาน ชุมชน หรือเอกชนร่วมไหม ร่วมทำอะไร สนับสนุนเงินหรือสิ่งของมูลค่าเท่าไร | Partner organisations, their role, cash and in-kind support? | optional; items `PTN1..`; `collaboration_role` (W005); in-kind needs `in_kind_basis` or a supporting attachment (B007) |
| `WORK.PLAN.RISKS` | | อะไรอาจทำให้โครงการไม่สำเร็จ รวมถึงเรื่องลิขสิทธิ์และผลกระทบต่อสังคม จะป้องกันหรือแก้อย่างไร | What could make the project fail (incl. copyright and social risks), and how will you prevent or handle it? | items `RSK1..`: `risk`, `risk_type`, `likelihood`, `impact`, `mitigation`, `activity_ids`; the top 3-6 risks |

## 8. Budget

Ask the researcher for every number. You may do the arithmetic and show it,
but the numbers written are the ones the researcher accepts.

| Field id | Chain node | Ask (TH) | Ask (EN) | Keys / links |
|---|---|---|---|---|
| `BUDGET.PLAN.ITEMS` (R) | BudgetItem | ใช้เงินกับอะไรบ้าง จำนวน กี่คน กี่ครั้งหรือกี่เดือน ราคาต่อหน่วยเท่าไร ใช้ในกิจกรรมไหน | Each cost: quantity, persons/items, times/months, unit price, which activity? | items `BI1..`: `year`, `budget_type`, `category`, `item_label`, `description`, `quantity`, `unit`, `persons_or_items`, `times_or_months`, `unit_price`, `line_total` (= product of the four, B002), `activity_ids` (B001), `justification` |
| `BUDGET.PLAN.YEARS` (R) | | แบ่งงบเป็นรายปีอย่างไร | Budget per project year? | items `BY1..`: `year`, `planned_total` |
| `BUDGET.PLAN.TOTAL` (R) | | | | the sum of `line_total`; must equal both budget fields in section 2 (B002) |
| `BUDGET.PLAN.EQUIPMENT` | | ต้องซื้อครุภัณฑ์ไหม ทำไมจำเป็น | Any equipment? Why needed? | items `EQ1..`: `name`, `specification`, `quantity`, `unit_price`, `total`, `justification`, `existing_equipment_check`, `budget_item_ids`; rule B005 |

Budget categories, rates and ceilings are fund rules: take them from the
call document or write `NEEDS_VERIFICATION`.

## 9. Outputs, evidence and expected claim

| Field id | Chain node | Ask (TH) | Ask (EN) | Keys / links |
|---|---|---|---|---|
| `RESULTS.CHAIN.OUTPUTS` (R) | Output | จบโครงการแล้วจะได้อะไรออกมาเป็นชิ้น ๆ เช่น รายงาน คู่มือ บทความ | Concrete outputs at the end? | items `OUT1..`: `output_type`, `quantity`, `unit`, `description`, `objective_ids`, `activity_ids` (W004), `kr_ids` + `kr_role` (`primary`/`secondary`: which KR the output answers) |
| `CORE.EVIDENCE.E1..` | Evidence | มีหลักฐานอะไรบ้างที่ทำให้เชื่อว่าแนวทางนี้น่าจะได้ผล | What evidence suggests this approach can work? | `chain_node: Evidence`, a source, `supports_claim_id`, `claim_strength_cap` |
| `CORE.CLAIM.C1..` | Claim | คาดว่าจะสรุปได้ว่าอะไร | What do you expect to be able to conclude? | `chain_node: Claim`, `provenance_class: INFERENCE`, `links.output_ids` |
| `RESULTS.CHAIN.OUTCOMES`, `.IMPACTS`, `.USERS`, `.BENEFICIARIES` | | ใครจะนำผลไปใช้ จะเกิดการเปลี่ยนแปลงอะไร | Who uses the results, what changes? | optional; item ids `USR1..`, `OC1..`, `IMP1..`, `BEN1..` (outcome process `PW1..`); outcomes `kr_ids` (Outcome -> KR); impacts `claim_strength` (`DIRECT` / `CONTRIBUTORY` / `ASPIRATIONAL`: use CONTRIBUTORY for most national-level impacts), `impact_type`, `sign`, `directness` |
| `RESULTS.PATHWAY.SUSTAINABILITY` | | หลังจบโครงการ ใครจะดูแลต่อ ทำเป็นกิจวัตรอย่างไร ใช้ทรัพยากรอะไร | After the project: who keeps it going, how, with what resources? | `owner`, `routine`, `resources_required`, `platform_or_network`, `continuity_mechanism`, `user_ids` |
| `RESULTS.ENTREPRENEUR.PROFILE` | | ถ้าเป็นสตาร์ทอัพหรือบริษัทสปินออฟ รูปแบบธุรกิจคืออะไร สำนักงานอยู่ที่ไหน | Startup or spin-off: business model, office location? | only if applicable |

## 10. Narrative sections (R)

`CORE.NARRATIVE.SUMMARY`, `.RATIONALE`, `.OBJECTIVES`, `.FRAMEWORK`,
`.THEORY`, `.METHOD` are the prose boxes. Prefer the researcher's own text.
If you assemble them from the records above, record them as `by: ai` (or
`provenance_class: DERIVED` with `by: researcher` only if the researcher
wrote the pieces and just asked you to join them verbatim), then ask the
researcher to read and confirm.

Also on the project part: `CORE.NARRATIVE.REFERENCES` (the reference list,
one style throughout) and `CORE.NARRATIVE.IP_CHECK` (was a check of related
patents or IP done, where, and what was found; if the project will use
someone's IP, `permission_status`, rule E009). Research-core and method
records are not NRIIS boxes: the output lists them in its appendix with the
narrative box each one feeds (`render_from`).

## 11. Attachments

`DOC.ATTACHMENTS.DOCUMENTS`: items `ATT1..`: `file_name`, `document_type`,
`file_type`, `related_section`, `required_status` (use `UNKNOWN` unless the
call says), `supplied` (true only when the researcher has the file).
