# Interview guide, article track (route `academic-article`)

Use this track after the researcher chose the `academic-article` route in
step 0 (`reference/routes.md`). It produces the ARTICLE.* records of a
`work.yaml` (`work_type: academic_article`) that
`grantthai build work.yaml --route academic-article` turns into one file,
`build/ACADEMIC_ARTICLE.md`: a manuscript **overview** arranged from the
researcher's own records. GrantThai never composes section text, never
reformats citations and never judges whether a manuscript is publishable.

The general rules of `reference/interview.md` apply unchanged (ask in the
researcher's language, two or three questions per turn, `by: researcher`
for their words and `by: ai` for yours, a source for every factual claim,
"don't know yet" stays `NEEDS_INPUT`). The field ids below are the
registry's; `grantthai fields --route academic-article` lists them in
placement order. Thai labels of ARTICLE fields are `NEEDS_VERIFICATION`.

Three rules specific to this track:

- **The results are the researcher's.** Never write, extend or "improve"
  results, data, figures or evidence. You may restate what they told you
  as an `ai_draft` they must confirm; that is all.
- **No journal facts.** Scope, indexing (TCI, Scopus or any other), word
  or page limits, fees, review time, template and reference style come
  only from the venue's own current author guidelines that the researcher
  supplies (a `sources` entry). Otherwise `NEEDS_VERIFICATION`. Hosting on
  a platform is not indexing (rule OK003).
- **You are not an author.** Never appear in `ARTICLE.FRONT.AUTHORS` or
  `ARTICLE.FRONT.CONTRIBUTIONS` (rule ART007 is a BLOCK). AI use is
  disclosed in `authoring.ai_use_declaration` and in the
  researcher-written `ARTICLE.STATEMENT.AI_USE`.

Shared fields (title, keywords, references, team, research core,
methodology) are the same records as in the proposal track: if the
researcher already has a `work.yaml` from a proposal, do not re-ask them.

## 1. Kind and language

| Field id | Ask (TH) | Ask (EN) | Notes |
|---|---|---|---|
| `ARTICLE.META.KIND` (R) | บทความนี้เป็นแบบไหน: งานวิจัยเชิงประจักษ์ บทความปริทัศน์ บทความเชิงแนวคิด กรณีศึกษา รายงานสั้น หรืออื่น ๆ | Which kind: empirical research, review, conceptual, case study, short communication, other? | enum; GrantThai's own descriptive list, not any journal's. Decides which sections ART003 expects |
| `ARTICLE.META.LANGUAGE` | ต้นฉบับเขียนภาษาไทย อังกฤษ หรือสองภาษา | Thai, English or both? | `th`, `en`, `th+en` |
| `ARTICLE.META.TITLE_TH`, `ARTICLE.META.TITLE_EN` | ชื่อบทความภาษาไทย / ภาษาอังกฤษ | Article title, Thai / English | falls back to `CORE.GENERAL.TITLE_*` by copy; a translation you make is `by: ai` |
| `ARTICLE.META.REFERENCE_STYLE` | ใช้รูปแบบการอ้างอิงแบบไหน | Which reference style do you use? | the researcher's declared label, as typed; GrantThai never reformats citations |

## 2. Venue, with its source

| Field id | Ask (TH) | Ask (EN) | Notes |
|---|---|---|---|
| `ARTICLE.VENUE.TARGET` | ตั้งใจส่งวารสารไหน มีคำแนะนำผู้เขียน (author guidelines) ฉบับปัจจุบันของวารสารนั้นไหม ขอดูได้ไหม | Which venue do you intend? Do you have its current author guidelines? Can you share them? | object `{name_as_typed, sub_profile, source_ids, stated_requirements: [{item, value, source_id}]}`. **Every stated requirement needs a `source_id`** the researcher supplied; a name with no source at all is REVIEW ART010 |
| sub-profile | ต้นฉบับเป็นแบบวารสารไทย/สองภาษา หรือวารสารนานาชาติ | Thai or bilingual journal, or international journal? | `thai-journal` (bilingual title, abstract, keywords as GrantThai's proposed defaults) or `international-journal`; both `NEEDS_VERIFICATION`. Record as `project.sub_profile` in `answers.yaml` or `--sub-profile` |

Ask for the guidelines as a source (`kind: OFFICIAL_DOCUMENT` or as the
researcher describes it, `citation` exactly as they give it, `accessed`
date). Word limits, keyword counts and required statements they read from
it go into `stated_requirements` with that `source_id`; ART002 then uses a
sourced keyword band instead of the default 3-6.

## 3. Authors and roles

Names, affiliations and ORCID are personal data: the same rule as for team
members applies (SKILL.md non-negotiable 7). In a public AI, leave names
`NEEDS_INPUT` for the researcher to fill in with `grantthai set` (no
`--ai`) or by editing the file.

| Field id | Ask (TH) | Ask (EN) | Notes |
|---|---|---|---|
| `ARTICLE.FRONT.AUTHORS` (R) | ผู้แต่งมีใครบ้าง เรียงลำดับอย่างไร ใครเป็น corresponding author สังกัดเขียนอย่างไร | Who are the authors, in what order? Who is corresponding? Affiliation as it should appear? | items `{member_ref -> PROFILE.TEAM.MEMBERS, order, corresponding, affiliation_as_typed}`; identifiers come by reference, no lookup |
| `ARTICLE.FRONT.CONTRIBUTIONS` | แต่ละคนมีส่วนร่วมอะไรบ้าง | What did each author contribute? | items `{member_ref, roles[]}`; more than one author with no contributions, or an author with no role, is REVIEW ART006. Role vocabulary follows CRediT (`NEEDS_VERIFICATION`) |

Never list an AI tool here (BLOCK ART007).

## 4. Keywords and abstracts

| Field id | Ask (TH) | Ask (EN) | Notes |
|---|---|---|---|
| `CORE.GENERAL.KEYWORDS_TH`, `CORE.GENERAL.KEYWORDS_EN` | คำสำคัญ (ไทย / อังกฤษ) | Keywords, Thai / English | shared fields; 3-6 is a `proposed_default` (`NEEDS_VERIFICATION`), overridden by a sourced venue requirement (ART002) |
| `ARTICLE.FRONT.ABSTRACT_TH`, `ARTICLE.FRONT.ABSTRACT_EN` | บทคัดย่อ (ไทย / อังกฤษ) เขียนเองแล้วหรือยัง หรือจะให้ช่วยเรียบเรียงจากผลที่มีอยู่ | Abstract, Thai / English: do you have one, or shall I arrange one from your results for you to rewrite? | rich text, or structured `{background, methods, results, conclusion}`. Anything you arrange is `by: ai`. `thai-journal` expects both languages (ART001, a default, `NEEDS_VERIFICATION`) |

## 5. Sections from the researcher's own results

For `empirical_research` (IMRaD): ask for each section in the researcher's
words. The `render_from` links tell the reader which chain records each
section rests on; they never generate text.

| Field id | Ask (TH) | Ask (EN) | Rests on (`render_from`) |
|---|---|---|---|
| `ARTICLE.SECTION.INTRODUCTION` | บทนำ: ปัญหา สิ่งที่รู้อยู่แล้ว ช่องว่าง | Introduction: problem, what is known, the gap | Problem, PriorKnowledge, Gap (`CORE.RESEARCH.PROBLEM`, `CORE.PRIORKNOWLEDGE.*`, `CORE.RESEARCH.GAP`) |
| `ARTICLE.SECTION.METHODS` | วิธีการ: แบบการวิจัย ข้อมูล การวิเคราะห์ | Methods: design, data, analysis | Method, Data, Analysis (`METHOD.PLAN.*`) |
| `ARTICLE.SECTION.RESULTS` | ผลการศึกษา ตามที่ได้จริง | Results, as found | Evidence records (`CORE.EVIDENCE.*`) |
| `ARTICLE.SECTION.DISCUSSION` | อภิปรายผล เทียบกับสิ่งที่รู้อยู่แล้ว | Discussion against prior knowledge | Claim + PriorKnowledge |
| `ARTICLE.SECTION.CONCLUSION` | สรุป | Conclusion | Claim |
| `ARTICLE.SECTION.LIMITATIONS` | ข้อจำกัดของงาน | Limitations | optional |

Any of Introduction, Methods, Results, Discussion empty on an
`empirical_research` kind is REVIEW ART003.

For every other kind (`review`, `conceptual`, `case_study`,
`short_communication`, `other`): `ARTICLE.BODY.SECTIONS`, items
`{heading, text, render_from}` in the researcher's order. Empty is REVIEW
ART003.

Ask for the reference list (`CORE.NARRATIVE.REFERENCES`) as soon as any
section has text (REVIEW ART004). Never supply a reference from memory.

## 6. Statements

| Field id | Ask (TH) | Ask (EN) | Notes |
|---|---|---|---|
| `ARTICLE.STATEMENT.ETHICS` | ถ้างานเกี่ยวกับคน ยื่นคณะกรรมการจริยธรรมที่ไหน เลขที่รับรองอะไร | If human participants: which ethics committee, which approval identifier? | as typed by the researcher; the committee name is theirs. Human-participant signals without this statement are REVIEW ART008 |
| `ARTICLE.STATEMENT.AI_USE` | จะแจ้งการใช้ AI ว่าอย่างไร (เครื่องมือ ขั้นตอน วัตถุประสงค์ อิทธิพลต่อผล การตรวจสอบ) และจะวางไว้ในส่วนวิธีการหรือกิตติกรรมประกาศ | How will you state your AI use (tool, stage, purpose, influence, checking), and where: methods or acknowledgements? | object `{text, placement: methods \| acknowledgements}`, researcher-written. AI use recorded but no statement or no placement is REVIEW ART005 (GenAI guideline 2569; check the journal's own policy first) |
| `ARTICLE.STATEMENT.DATA_AVAILABILITY` | ข้อมูลเข้าถึงได้อย่างไร | Data availability | optional |
| `ARTICLE.STATEMENT.CONFLICT_OF_INTEREST` | มีผลประโยชน์ทับซ้อนไหม | Conflict of interest | optional |
| `ARTICLE.STATEMENT.FUNDING` | ได้ทุนจากไหน | Funding | optional; as the researcher states it |
| `ARTICLE.BACK.ACKNOWLEDGEMENTS` | กิตติกรรมประกาศ | Acknowledgements | optional; never add yourself |

## 7. Figures and tables

| Field id | Ask (TH) | Ask (EN) | Notes |
|---|---|---|---|
| `ARTICLE.BODY.FIGURES_TABLES` | มีรูปหรือตารางอะไรบ้าง รูปไหนแสดงข้อมูลจริง รูปไหนเป็นภาพประกอบที่สร้างด้วย AI | Which figures and tables? Which show data? Which are AI-generated illustrations? | items `{id, kind, caption, data_bearing, ai_generated_illustration, source_ids}`. `data_bearing: true` together with `ai_generated_illustration: true` is REVIEW ART009 (no AI-generated data or factual images); an AI-generated illustration whose caption has no disclosure is REVIEW ART011 |

## 8. Check and hand back

```bash
grantthai route check --route academic-article work.yaml
python scripts/grantthai_skill.py report --route academic-article [--sub-profile thai-journal]
grantthai build work.yaml --route academic-article       # writes build/ACADEMIC_ARTICLE.md
```

Hand back `build/ACADEMIC_ARTICLE.md` (this route's only output) and
`work.yaml`. Summarise in Thai: BLOCK/REVIEW counts, every venue fact still
`NEEDS_VERIFICATION`, AI-drafted values awaiting confirmation, and that
`manuscript_ready` means only "no BLOCK open", never accepted or
publishable. The researcher submits to the journal themselves; GrantThai
and you submit nothing.
