#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Yaoharee Lahtee and ARAYA NIKAH SOCIAL ENTERPRISE CO.
# SPDX-License-Identifier: Apache-2.0
"""tools/corpus/corpus_extract.py

Structural extractor for the funded-report comparison corpus
(docs/demo/corpus-100.md).

It reads PDFs that YOU downloaded into a local directory of your choice. It
never downloads anything, and neither the PDFs nor their extracted text
belong in this repository.

Subcommands
-----------
extract   pdftotext -layout -> heading detection (Thai/English patterns,
          tolerant of the broken sara-am / dropped-vowel output that legacy
          Thai PDF fonts give) -> per-section presence and size, reference /
          table / figure counts, objective and RQ counts, keyword mentions,
          funder names -> mapping of each detected section to GrantThai
          field_ids (registry/fields.jsonl). Writes a structure CSV and one
          JSON per document. No report text is written: only flags, counts,
          page numbers and section keys.

publish   Joins a metadata catalogue with the structure CSV into the public
          metadata + structural-flags CSV (docs/demo/corpus-100.csv).

stats     Prints the aggregate tables used in docs/demo/corpus-100.md from
          the public CSV, so every number there can be recomputed without
          the PDFs.

Examples
--------
  python tools/corpus/corpus_extract.py extract --pdf-dir DIR --catalogue cat.csv \
      --registry registry/fields.jsonl --out-dir OUT [--txt-dir TXT] [--ids-from fetch_log.jsonl]
  python tools/corpus/corpus_extract.py publish --catalogue cat.csv \
      --structure OUT/corpus_structure.csv --out docs/demo/corpus-100.csv
  python tools/corpus/corpus_extract.py stats --csv docs/demo/corpus-100.csv

Needs the `pdftotext` program (poppler-utils) for `extract` only.
"""
import argparse
import csv
import json
import os
import re
import statistics as st
import subprocess
import sys
import unicodedata
from collections import Counter, OrderedDict

# ---------------------------------------------------------------- normalisation
THAI_DIGITS = str.maketrans("๐๑๒๓๔๕๖๗๘๙", "".join(map(str, range(10))))
# marks that legacy Thai fonts drop, duplicate or re-order in extracted text
_DROP = dict.fromkeys(map(ord, "่้๊๋็์ุูํ​‌‍﻿"), None)

# some Thai PDF fonts map tone marks / thanthakhat to ASCII glyphs (e.g. "ข^อมูล", "กลุQม", "วัตถุประสงค`")
_ARTIFACT = re.compile(r"(?<=[ก-๏])[!#$%&*+<=>?@\[\]^_`{|}~A-Za-z0-9Ÿ](?=[ก-๏])"
                       r"|(?<=[ก-๏])[`^OQ>](?=\s|$)")


def unglitch(s):
    return _ARTIFACT.sub("", s)


def norm(s, pattern=False):
    s = unicodedata.normalize("NFC", s)
    s = (s if pattern else unglitch(s)).translate(THAI_DIGITS)
    s = s.replace("ํา", "า").replace("ำ", "า")  # sara am -> sara aa
    s = s.translate(_DROP)
    return re.sub(r"\s+", "", s).lower()


def lite(s, pattern=False):
    """norm() without whitespace removal / lower-casing: for running text and its regexes."""
    s = unicodedata.normalize("NFC", s)
    s = (s if pattern else unglitch(s)).translate(THAI_DIGITS)
    s = s.replace("\u0e4d\u0e32", "\u0e32").replace("\u0e33", "\u0e32")
    return s.translate(_DROP)

# ---------------------------------------------------------------- section taxonomy
# (key, regex applied to norm(heading text after numbering is stripped))
# order matters: first match wins.
def R(p):
    return re.compile("^(?:" + norm(p, pattern=True) + ")")

SECTIONS = [
    ("abstract_th",      R("บทคัดย่อ|บทคัดย่อภาษาไทย")),
    ("abstract_en",      R("abstract|summary(?!of)")),
    ("executive_summary", R("บทสรุปผู้บริหาร|บทสรุปสาหรับผู้บริหาร|บทสรุป$|executivesummary")),
    ("acknowledgement",  R("กิตติกรรมประกาศ|acknowledg")),
    ("keywords",         R("คาสาคัญ|คาหลัก|keywords?")),
    ("policy_recommendations", R("ข้อเสนอเชิงนโยบาย|ข้อเสนอแนะเชิงนโยบาย|policyrecommendation|policyimplication")),
    ("recommendations",  R("ข้อเสนอแนะ|ข้อเสนอ|recommendation|suggestion")),
    ("rq",               R("คาถาม(?:ของ)?(?:การ)?วิจัย|คาถามการศึกษา|researchquestion")),
    ("hypothesis",       R("สมมติฐาน|สมมุติฐาน|hypothes")),
    ("objectives",       R("วัตถ.?ประสงค์|จุดประสงค์|objective|aim")),
    ("alignment",        R("เป้าหมายเชิงยุทธศาสตร์|ความสอดคล้อง(?:กับ)?(?:ยุทธศาสตร์|นโยบาย|แผน)|ความเชื่อมโยง(?:กับ)?(?:ยุทธศาสตร์|นโยบาย|แผน)|alignment")),
    ("scope",            R("ขอบเขต|scope")),
    ("framework",        R("กรอบ(?:แนวคิด|ความคิด|การวิจัย|การศึกษา)|conceptualframework|researchframework")),
    ("definitions",      R("นิยามศัพท์|นิยามปฏิบัติการ|คานิยาม|definition")),
    ("users_section",    R("หน่วยงาน(?:ผู้)?(?:ที่)?(?:นา.{0,20})?ใช้ประโยชน์|ผู้ใช้ประโยชน์|กลุ่มผู้ใช้|ผู้ใช้ผล|researchusers?|endusers?")),
    ("beneficiaries_section", R("ผู้(?:ได้)?รับประโยชน์|กลุ่มผู้(?:ได้)?รับประโยชน์|beneficiar")),
    ("expected_benefit", R("ประโยชน์ที่(?:คาดว่าจะ)?ได้รับ|ประโยชน์(?:ของ|จาก)(?:การ|งาน|โครงการ)|expectedbenefit|significance")),
    ("utilization",      R("การนา.{0,20}ไปใช้(?:ประโยชน์)?|การใช้ประโยชน์|utili[sz]ation")),
    ("outputs",          R("ผลผลิต|ผลลัพธ์|ผลกระทบ|ผลที่คาดว่าจะได้รับ|ผลงาน(?:วิจัย)?ที่ได้|output|outcome|impact")),
    ("lit_review",       R("ทบทวน(?:วรรณกรรม|เอกสาร)|การทบทวน|เอกสาร(?:และ|,)?งานวิจัยที่เกี่ยวข้อง|งานวิจัยที่เกี่ยวข้อง|"
                           "แนวคิด.{0,30}ทฤษฎี|ทฤษฎี.{0,30}(?:ที่เกี่ยวข้อง|งานวิจัย)|การตรวจเอกสาร|วรรณกรรมที่เกี่ยวข้อง|"
                           "literaturereview|reviewofliterature|relatedwork|theoreticalbackground")),
    ("background",       R("ความเป็นมา|ที่มา|ความสาคัญ|หลักการและเหตุผล|บทนา|สภาพ(?:และความสาคัญของ)?ปัญหา|"
                           "introduction|background|rationale")),
    ("population",       R("ประชากร|กลุ่มตัวอย่าง|กลุ่มเป้าหมาย|ผู้ให้ข้อมูล|population|participants|samplesize|studypopulation")),
    ("instruments",      R("เครื่องมือ(?:ที่ใช้)?(?:ใน)?(?:การ)?(?:วิจัย|เก็บ|ศึกษา)|เครื่องมือ|instrument")),
    ("data_collection",  R("การ(?:เก็บ|รวบรวม)(?:รวบรวม)?ข้อมูล|วิธีการเก็บ|datacollection")),
    ("analysis",         R("การวิเคราะห์ข้อมูล|การวิเคราะห์ทางสถิติ|สถิติที่ใช้|dataanalysis|statisticalanalys")),
    ("ethics",           R("จริยธรรม|การพิทักษ์สิทธิ|ข้อพิจารณาทางจริยธรรม|ethic")),
    ("budget",           R("งบประมาณ|budget")),
    ("workplan",         R("แผนการ(?:ดาเนิน|ทา)งาน|ระยะเวลา(?:การ|ใน|ที่ใช้|ดาเนิน)|ขั้นตอนการดาเนิน|workplan|timeline|ganttchart")),
    ("methods",          R("วิธี(?:การ)?ดาเนิน|วิธีการวิจัย|วิธีวิจัย|ระเบียบวิธี|วิธีการศึกษา|วิธีการทดลอง|วัสดุ.{0,20}วิธี|"
                           "รูปแบบการวิจัย|การออกแบบการวิจัย|methodology|methods?|materialsandmethods|researchdesign|studydesign")),
    ("results",          R("ผล(?:การ)?(?:วิจัย|ศึกษา|ทดลอง|ดาเนิน(?:งาน|โครงการ|การ)|วิเคราะห์|การศึกษา|ประเมิน)|results?|findings")),
    ("discussion_conclusion", R("สรุป|อภิปราย|วิจารณ์|conclusion|discussion")),
    ("references",       R("เอกสารอ้างอิง|บรรณานุกรม|รายการอ้างอิง|เอกสารประกอบ$|references?$|referencelist|bibliography|literaturecited")),
    ("appendix",         R("ภาคผนวก|appendi")),
]
SECTION_KEYS = [k for k, _ in SECTIONS]

# section -> GrantThai field_ids. "exact" = same purpose; "nearest" = closest
# proposal-side counterpart of a report-side section; [] = report-only.
FIELD_MAP = {
    "abstract_th": ("exact", ["CORE.NARRATIVE.SUMMARY"]),
    "abstract_en": ("exact", ["CORE.NARRATIVE.SUMMARY"]),
    "executive_summary": ("exact", ["CORE.NARRATIVE.SUMMARY"]),
    "keywords": ("exact", ["CORE.GENERAL.KEYWORDS_TH", "CORE.GENERAL.KEYWORDS_EN"]),
    "background": ("exact", ["CORE.NARRATIVE.RATIONALE", "CORE.RESEARCH.PROBLEM", "CORE.RESEARCH.NATIONAL_NEED"]),
    "objectives": ("exact", ["CORE.RESEARCH.OBJECTIVES", "CORE.NARRATIVE.OBJECTIVES"]),
    "rq": ("exact", ["CORE.RESEARCH.RQ.PRIMARY", "CORE.RESEARCH.RQ.SECONDARY"]),
    "hypothesis": ("exact", ["CORE.RESEARCH.HYPOTHESES"]),
    "scope": ("nearest", ["CORE.RESEARCH.BOUNDARY_CONDITIONS"]),
    "alignment": ("exact", ["CORE.ALIGNMENT.STATEMENT", "CORE.ALIGNMENT.POLICY_PATHWAY"]),
    "framework": ("exact", ["CORE.NARRATIVE.FRAMEWORK", "CORE.RESEARCH.CONSTRUCTS", "CORE.RESEARCH.RELATIONSHIPS"]),
    "definitions": ("nearest", ["METHOD.PLAN.VARIABLES"]),
    "lit_review": ("exact", ["CORE.RESEARCH.THEORETICAL_FOUNDATIONS", "CORE.NARRATIVE.THEORY", "CORE.RESEARCH.GAP"]),
    "methods": ("exact", ["CORE.NARRATIVE.METHOD", "METHOD.PLAN.DESIGN"]),
    "population": ("exact", ["METHOD.PLAN.POPULATION", "METHOD.PLAN.SAMPLE"]),
    "instruments": ("exact", ["METHOD.PLAN.INSTRUMENTS"]),
    "data_collection": ("exact", ["METHOD.PLAN.DATA_COLLECTION"]),
    "analysis": ("exact", ["METHOD.PLAN.ANALYSIS"]),
    "ethics": ("exact", ["METHOD.PLAN.ETHICS", "COMP.STANDARD.RESEARCH_ETHICS"]),
    "users_section": ("exact", ["RESULTS.CHAIN.USERS", "GEO.AREA.RESEARCH_USERS"]),
    "beneficiaries_section": ("exact", ["RESULTS.CHAIN.BENEFICIARIES"]),
    "expected_benefit": ("exact", ["RESULTS.CHAIN.BENEFIT_SUMMARY"]),
    "utilization": ("exact", ["RESULTS.CHAIN.UTILIZATION_DESC", "RESULTS.CHAIN.UTILIZATION_DOMAIN"]),
    "outputs": ("exact", ["RESULTS.CHAIN.OUTPUTS", "RESULTS.CHAIN.OUTCOMES", "RESULTS.CHAIN.IMPACTS"]),
    "budget": ("exact", ["BUDGET.PLAN.ITEMS", "BUDGET.PLAN.TOTAL"]),
    "workplan": ("exact", ["WORK.PLAN.ACTIVITIES"]),
    "references": ("exact", ["CORE.NARRATIVE.REFERENCES"]),
    "appendix": ("nearest", ["DOC.ATTACHMENTS.DOCUMENTS"]),
    "recommendations": ("nearest", ["RESULTS.CHAIN.UTILIZATION_DESC"]),
    "policy_recommendations": ("nearest", ["RESULTS.CHAIN.UTILIZATION_DESC", "CORE.ALIGNMENT.POLICY_PATHWAY"]),
    "acknowledgement": ("nearest", ["FUND.CALL.AGENCY"]),
    "results": ("report_only", []),
    "discussion_conclusion": ("report_only", []),
}

MENTIONS = OrderedDict([
    ("kr", (r"\bKR\s?\d|\bOKRs?\b|key\s*results?|ผลลัพธ์สำคัญ", ["FUND.CALL.KEY_RESULTS", "CORE.ALIGNMENT.FUND_SELECTION"])),
    ("strategy", (r"ยุทธศาสตร์", ["CORE.ALIGNMENT.POLICY_PATHWAY"])),
    ("wwn_plan", (r"ววน|แผนด้านวิทยาศาสตร์\s*วิจัย\s*และนวัตกรรม|วิทยาศาสตร์\s*วิจัย\s*และนวัตกรรม", ["CORE.GENERAL.MASTER_PLAN", "CORE.ALIGNMENT.POLICY_PATHWAY"])),
    ("trl", (r"\bTRL\b|technology\s+readiness|ระดับความพร้อม(?:ทาง|ของ)?เทคโนโลยี", ["READY.TRL.CURRENT", "READY.TRL.TARGET"])),
    ("srl", (r"\bSRL\b|societal\s+readiness|ระดับความพร้อม(?:ทาง|ของ)?สังคม", ["READY.SRL.CURRENT", "READY.SRL.TARGET"])),
    ("users", (r"ผู้ใช้ประโยชน์|ผู้ใช้ผล(?:งาน|การ)วิจัย|research\s+users?|end[\s-]users?", ["RESULTS.CHAIN.USERS"])),
    ("beneficiaries", (r"ผู้ได้รับประโยชน์|ผู้รับประโยชน์|beneficiar", ["RESULTS.CHAIN.BENEFICIARIES"])),
    ("policy_rec", (r"ข้อเสนอ(?:แนะ)?เชิงนโยบาย|policy\s+recommendation", ["RESULTS.CHAIN.UTILIZATION_DESC"])),
    ("ethics_approval", (r"คณะกรรมการ(?:พิจารณา)?จริยธรรม|ethics\s+committee|institutional\s+review\s+board|\bIRB\b", ["METHOD.PLAN.ETHICS", "COMP.STANDARD.HUMAN"])),
    ("sample_size_basis", (r"ขนาด(?:ของ)?กลุ่มตัวอย่าง|sample\s*size|Cochran|Yamane|ยามาเน่|Krejcie|G\s?\*\s?Power", ["METHOD.PLAN.SAMPLE"])),
    ("informed_consent", (r"ยินยอม(?:เข้าร่วม|ให้ข้อมูล|ในการเข้าร่วม)|หนังสือแสดงความยินยอม|informed\s+consent", ["METHOD.PLAN.ETHICS"])),
    ("expert_validation", (r"ผู้ทรงคุณวุฒิ|expert\s+(?:panel|review|seminar|consultation)|ประชาพิจารณ์|public\s+hearing", ["METHOD.PLAN.QUALITY"])),
    ("limitations", (r"ข้อจำกัด(?:ของ|ใน)?(?:การ)?(?:วิจัย|ศึกษา)|limitations?\s+of\s+(?:the|this)\s+(?:study|research)|study\s+limitations?", ["METHOD.PLAN.QUALITY"])),
    ("triangulation", (r"triangulat|สามเส้า", ["METHOD.PLAN.QUALITY"])),
    ("budget_amount",(r"งบประมาณ[^\n]{0,40}\d[\d,]*\s*บาท|\d[\d,]{3,}\s*บาท", ["CORE.GENERAL.TOTAL_BUDGET", "BUDGET.PLAN.TOTAL"])),
])

# Funder names are matched by their full Thai / English names only. Short
# agency acronyms are deliberately not listed: this repository keeps them out
# of code and docs (tools/ci/check_no_hardcoded_rules.py), and a full name is
# the stronger evidence anyway. Codes are this tool's own labels.
FUNDER_PATTERNS = OrderedDict([
    ("HSRI", r"สถาบันวิจัยระบบสาธารณสุข|\(?สวรส\.?\)?|Health Systems Research Institute|\bHSRI\b"),
    ("TRF_SRI", r"สำนักงานการวิจัยแห่งชาติ\s*\(?สกว|สำนักงานกองทุนสนับสนุนการวิจัย|สกว\.|สำนักงานคณะกรรมการส่งเสริมวิทยาศาสตร์\s*วิจัยและนวัตกรรม|Thailand Research Fund|Thailand Science Research and Innovation|\bTRF\b"),
    ("NRC", r"สำนักงานคณะกรรมการวิจัยแห่งชาติ|สำนักงานการวิจัยแห่งชาติ|National Research Council of Thailand"),
    ("GOV_BUDGET", r"งบประมาณแผ่นดิน|งบประมาณ(?:ประจำ)?ปี(?:งบประมาณ)?\s*(?:พ\.ศ\.\s*)?25\d\d|government budget|national budget"),
    ("UNIV_INCOME", r"เงินรายได้|ทุนอุดหนุนการวิจัย(?:จาก)?มหาวิทยาลัย|(?:ทุน|งบประมาณ)[^\n]{0,60}(?:มหาวิทยาลัยสงขลานครินทร์|Prince of Songkla University)|(?:มหาวิทยาลัยสงขลานครินทร์|Prince of Songkla University)[^\n]{0,80}(?:ทุน|สนับสนุน|support|grant)"),
    ("THAIHEALTH", r"สำนักงานกองทุนสนับสนุนการสร้างเสริมสุขภาพ|\(?สสส\.?\)?|Thai Health Promotion Foundation"),
    ("NIEMS", r"สถาบันการแพทย์ฉุกเฉินแห่งชาติ|สำนักงานการแพทย์ฉุกเฉิน|\bสพฉ\.?"),
    ("NHSO", r"สำนักงานหลักประกันสุขภาพแห่งชาติ|\(?สปสช\.?\)?"),
    ("FUND_UNIT", r"หน่วยบริหารและจัดการทุน|หน่วยบริหารจัดการทุน"),
    ("OTHER_FUND", r"ทุนสนับสนุน|research grant|grant no|funded by|supported by"),
])
FUNDING_ACK = re.compile(
    r"(ได้(?:รับ)?(?:การ)?(?:สนับสนุน)?(?:ทุน|งบประมาณ|การสนับสนุน|เงินทุน)|ให้(?:การ)?(?:สนับสนุน)?ทุน|ทุนอุดหนุน|ทุนวิจัย|สนับสนุนงบประมาณ|"
    r"สนับสนุนทุน|financial(?:ly)? support|funded by|supported by|grant(?:ed)? (?:from|by|no))", re.I)

# ---------------------------------------------------------------- line helpers
NUM_PREFIX = re.compile(
    r"^\s*(?:บทที่\s*[0-9๐-๙IVXivx]+\s*[:.\-–]?|chapter\s*[0-9IVX]+\s*[:.\-–]?|part\s*[0-9IVX]+\s*[:.\-–]?|"
    r"ส่วนที่\s*[0-9๐-๙]+\s*[:.\-–]?|[0-9๐-๙]{1,2}(?:\.[0-9๐-๙]{1,2}){0,4}\.?\)?|\(?[0-9๐-๙]{1,2}\)|"
    r"[ก-ฮ]\.|[A-Za-z]\.|[IVX]{1,4}\.)\s*", re.I)
CHAPTER_ONLY = re.compile(r"^\s*(?:บทที่|chapter)\s*[0-9๐-๙IVXivx]+\s*$", re.I)
TOC_LEADER = re.compile(r"(?:\.\s?){4,}\s*[0-9๐-๙ivxlcdmIVXLCDMก-ฮ\-]*\s*$|…{2,}")
CAPTION_TABLE = re.compile(r"^\s*(?:ตารางที่|ตาราง|Table)\s*([0-9๐-๙]+(?:[.\-–][0-9๐-๙]+)*|[ก-ฮ][.\-][0-9]+)", re.I)
CAPTION_FIG = re.compile(r"^\s*(?:ภาพที่|รูปที่|แผนภาพที่|แผนภูมิที่|ภาพ|รูป|Figure|Fig\.)\s*([0-9๐-๙]+(?:[.\-–][0-9๐-๙]+)*|[ก-ฮ][.\-][0-9]+)", re.I)
YEAR = re.compile(r"(?:19|20)\d\d|25[0-6]\d")
ITEM = re.compile(r"^\s*(?:\(?[0-9๐-๙]{1,2}(?:\.[0-9๐-๙]{1,2}){0,3}[.)]|\(?[0-9๐-๙]{1,2}\)|[ก-ฮ][.)]|[•\-–▪●○◦]|ข้อที่\s*[0-9๐-๙])\s*\S")


def classify(text):
    n = norm(text)
    if not n:
        return None
    for key, rx in SECTIONS:
        if rx.match(n):
            return key
    return None


def page_split(raw):
    return raw.split("\f")


def is_toc_page(lines):
    return sum(1 for l in lines if TOC_LEADER.search(l)) >= 4 or any(
        norm(l).startswith(("สารบัญ", "contents", "tableofcontents", "listoffig", "listoftab", "listofillus"))
        and len(norm(l)) <= 20 for l in lines[:12])


def detect(raw):
    """Return (toc_hits, headings) where headings = [(line_index, page, key|None, text)]."""
    pages = page_split(raw)
    lines, page_of = [], []
    for pi, p in enumerate(pages):
        for l in p.split("\n"):
            lines.append(l); page_of.append(pi + 1)
    toc_pages = {pi + 1 for pi, p in enumerate(pages) if pi < max(25, len(pages) // 4) and is_toc_page(p.split("\n"))}
    page_width = {}
    for x, l in enumerate(lines):
        page_width[page_of[x]] = max(page_width.get(page_of[x], 0), len(l.rstrip()))
    toc_hits, heads = Counter(), []
    i = 0
    while i < len(lines):
        l = lines[i]; s = l.strip()
        if not s:
            i += 1; continue
        pg = page_of[i]
        if pg in toc_pages or TOC_LEADER.search(s):
            t = TOC_LEADER.sub("", s)
            t2 = NUM_PREFIX.sub("", t, count=1)
            k = classify(t2) or (classify(t) if CHAPTER_ONLY.match(t) is None else None)
            if k and len(norm(t2)) <= 80:
                toc_hits[k] += 1
            i += 1; continue
        # "บทที่ 3" on its own line: title is the next non-empty line
        if CHAPTER_ONLY.match(s):
            j = i + 1
            while j < len(lines) and not lines[j].strip() and j - i < 4:
                j += 1
            title = lines[j].strip() if j < len(lines) else ""
            heads.append((i, pg, classify(title) if len(norm(title)) <= 70 else None, "CHAPTER " + title[:60], 0))
            i = j + 1; continue
        m = NUM_PREFIX.match(s)
        has_num = bool(m and m.group(0).strip())
        body = s[m.end():] if has_num else s
        trailing = re.search(r"\s{3,}(.*)$", body) if has_num else None
        table_row = bool(trailing and len(trailing.group(1).split()) >= 2)  # numbered table row with columns
        body = re.sub(r"\s{3,}.*$", "", body) if has_num else body  # drop trailing page no./columns
        pref = m.group(0).strip() if has_num else ""
        if re.match(r"^(?:บทที่|chapter|part|ส่วนที่)", pref, re.I):
            lvl = 0
        elif re.match(r"^[0-9๐-๙]", pref):
            lvl = len(re.findall(r"[0-9๐-๙]+", pref))
        elif pref:
            lvl = 4
        else:
            lvl = 1
        nb = norm(body)
        prev_blank = i == 0 or not lines[i - 1].strip()
        short = len(nb) <= 45
        plausible = (has_num and len(nb) <= 70) or (short and prev_blank) or (len(nb) <= 25)
        multicol = (not has_num) and any(re.search(r"\S\s{3,}\S", lines[x].strip()) for x in range(max(0, i - 4), min(len(lines), i + 5))
                                            if page_of[x] == pg)  # table rows nearby
        prose = re.search(r"พบว่า|ดังนี้$|ได้แก่|เท่ากับ|ร้อยละ|เช่น|ของท่าน|ประกอบด้วย|คือ(?:\s|$)|[?:;]\s*\S", body)
        indent = len(l) - len(l.lstrip())
        pw = page_width.get(pg, 100)
        off_centre = abs(indent - (pw - len(s)) / 2) > 12
        cell = (not has_num) and indent >= 12 and off_centre  # narrow table-column cell, not a heading
        if plausible and nb and not multicol and not prose and not table_row and not cell:
            k = classify(body)
            if k and not s.rstrip().endswith((",", "และ")):
                heads.append((i, pg, k, body[:80], lvl))
            elif has_num and re.match(r"^\s*(?:[0-9๐-๙]{1,2}\.[0-9๐-๙]|บทที่)", s) and len(nb) <= 60:
                heads.append((i, pg, None, body[:80], lvl))  # generic numbered heading = boundary
        i += 1
    # context: proposal-component words inside a results chapter are result
    # sub-headings (e.g. "the framework we produced"), and a "summary" inside a
    # literature-review chapter is that chapter's wrap-up, not the report's conclusion
    PROPOSAL_KEYS = {"framework", "instruments", "population", "scope", "objectives", "hypothesis", "rq",
                     "definitions", "workplan", "budget", "ethics", "lit_review", "data_collection", "analysis",
                     "methods", "background"}
    chap, fixed = None, []
    for h in heads:
        if h[4] == 0:
            chap = h[2]
        elif chap == "results" and h[2] in PROPOSAL_KEYS:
            h = (h[0], h[1], None, h[3], h[4])
        elif chap == "lit_review" and h[2] == "discussion_conclusion":
            h = (h[0], h[1], None, h[3], h[4])
        fixed.append(h)
    heads = fixed
    # back matter: once a body "appendix" heading appears past 40% of the pages,
    # later keyed headings (questionnaires, forms) are appendix content
    n_pages = len(pages)
    cut = next((h[0] for h in heads if h[2] == "appendix" and h[1] > 0.4 * n_pages), None)
    if cut is not None:
        refs_before = any(h[2] == "references" and h[0] < cut for h in heads)
        keep = ("appendix",) if refs_before else ("appendix", "references")
        heads = [h if h[0] <= cut or h[2] in keep else (h[0], h[1], None, h[3], max(h[4], 1)) for h in heads]
    return lines, page_of, toc_hits, heads, toc_pages


def seg_chars(seg_lines):
    """Section size as non-whitespace characters (deterministic for Thai,
    which has no spaces between words)."""
    return len(re.sub(r"\s", "", "\n".join(seg_lines)))


def count_items(seg_lines):
    n = 0
    for l in seg_lines:
        if ITEM.match(l):
            n += 1
    return n


def count_refs(seg_lines):
    body = [l for l in seg_lines if l.strip()]
    if not body:
        return 0, "none"
    numbered = [l for l in body if re.match(r"^\s*(?:\[[0-9]{1,3}\]|[0-9]{1,3}[.)]\s)", l)]
    if len(numbered) >= 5:
        return len(numbered), "numbered"
    indents = Counter(len(l) - len(l.lstrip()) for l in body)
    base = min(indents)
    starts, cur_has_year, n = 0, False, 0
    for l in body:
        ind = len(l) - len(l.lstrip())
        if ind <= base + 1:
            if starts and cur_has_year:
                n += 1
            starts += 1; cur_has_year = bool(YEAR.search(l))
        else:
            cur_has_year = cur_has_year or bool(YEAR.search(l))
    if starts and cur_has_year:
        n += 1
    return n, "hanging-indent-estimate"




def pdf_pages(pdf, raw):
    try:
        out = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True, timeout=60).stdout
        m = re.search(r"^Pages:\s+(\d+)", out, re.M)
        if m:
            return int(m.group(1))
    except (OSError, subprocess.SubprocessError):
        pass
    return raw.count("\f") or 1


def sha256_file(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def extract(doc_id, pdf, txt_path, title, registry_ids):
    """Structure of one PDF. Returns a dict of flags, counts and section keys only."""
    if txt_path and os.path.exists(txt_path):
        raw = open(txt_path, encoding="utf-8", errors="replace").read()
    else:
        raw = subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", pdf, "-"],
                             capture_output=True, timeout=300).stdout.decode("utf-8", "replace")
        if txt_path:
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(raw)
    lines, page_of, toc_hits, heads, toc_pages = detect(raw)

    # section segments: every body line gets one owner. A chapter heading owns
    # its chapter; a keyed sub-heading at numbering depth L owns lines until the
    # next keyed heading or the next heading at depth <= L (deeper generic
    # headings stay inside it).
    owner = [None] * len(lines)
    for idx, (li, pg, key, text, lvl) in enumerate(heads):
        if lvl != 0:
            continue
        nxt = [h[0] for h in heads[idx + 1:] if h[4] == 0]
        end = nxt[0] if nxt else len(lines)
        for j in range(li, end):
            owner[j] = key
    for idx, (li, pg, key, text, lvl) in enumerate(heads):
        if lvl == 0 or not key:
            continue
        nxt = [h[0] for h in heads[idx + 1:] if h[2] or h[4] <= lvl]
        end = nxt[0] if nxt else len(lines)
        for j in range(li, end):
            owner[j] = key
    sections = OrderedDict()
    for (li, pg, key, text, lvl) in heads:
        if key:
            s = sections.setdefault(key, {"n_headings": 0, "first_page": pg, "lines": []})
            s["n_headings"] += 1
    for j, l in enumerate(lines):
        k = owner[j]
        if k and k in sections and l.strip() and page_of[j] not in toc_pages:
            sections[k]["lines"].append(l)
    # inline "Keywords: ..." / "คำสำคัญ: ..." lines are not stand-alone headings
    if "keywords" not in sections:
        for j, l in enumerate(lines):
            if page_of[j] in toc_pages:
                continue
            if re.match(r"^\s*(?:คาสาคัญ|คาหลัก|key\s*words?|index\s*terms)\s*[:：]?\s*\S", lite(l), re.I):
                s = sections.setdefault("keywords", {"n_headings": 0, "first_page": page_of[j], "lines": []})
                s["n_headings"] += 1
                s["lines"].append(l)

    obj_items = count_items(sections["objectives"]["lines"][:60]) if "objectives" in sections else 0
    rq_items = 0
    if "rq" in sections:
        rq_lines = sections["rq"]["lines"][:60]
        rq_items = max(count_items(rq_lines), sum(1 for l in rq_lines if "?" in l or l.rstrip().endswith("หรือไม่")))
    refs, ref_method = count_refs(sections["references"]["lines"]) if "references" in sections else (0, "none")

    body_lines = [l for l, p in zip(lines, page_of) if p not in toc_pages and not TOC_LEADER.search(l)]
    tables = {norm(m.group(1)) for l in body_lines for m in [CAPTION_TABLE.match(l)] if m}
    figs = {norm(m.group(1)) for l in body_lines for m in [CAPTION_FIG.match(l)] if m}
    body_lite = lite("\n".join(body_lines))
    mentions = {k: len(re.findall(lite(p, True), body_lite, re.I)) for k, (p, _) in MENTIONS.items()}

    # funding statement: acknowledgement section plus the first 400 body lines
    fund_src = "\n".join(sections["acknowledgement"]["lines"]) if "acknowledgement" in sections else ""
    probe = lite(fund_src + "\n" + "\n".join(body_lines[:400]))
    ack_m = re.compile(lite(FUNDING_ACK.pattern, True), re.I).search(probe)
    funders = []
    if ack_m:
        wide = re.sub(r"\s+", " ", probe[max(0, ack_m.start() - 200):ack_m.end() + 400])
        wide_ns = re.sub(r"\s+", "", wide)
        funders = [k for k, p in FUNDER_PATTERNS.items()
                   if re.search(lite(p, True), wide, re.I) or re.search(lite(p, True).replace(" ", ""), wide_ns, re.I)]
        if len(funders) > 1 and "OTHER_FUND" in funders:
            funders.remove("OTHER_FUND")
    # a funding body named anywhere on the first 20 pages (cover, preface, acknowledgement)
    front20 = lite("\f".join(page_split(raw)[:20]))
    front20_ns = re.sub(r"\s+", "", front20)
    funders_front = [k for k, p in FUNDER_PATTERNS.items() if k not in ("OTHER_FUND", "GOV_BUDGET", "UNIV_INCOME")
                     and (re.search(lite(p, True), front20, re.I) or re.search(lite(p, True).replace(" ", ""), front20_ns, re.I))]
    # is the catalogue title (its Thai part) on the first 3 pages?
    first_pages = norm("\f".join(page_split(raw)[:3]))
    tnorm = norm(re.split(r"\s+[A-Z]", title or "", maxsplit=1)[0])[:40]
    title_found = bool(tnorm) and tnorm in first_pages

    detected = sorted(set(sections) | set(toc_hits))
    fmap = {}
    for k in detected:
        kind, ids = FIELD_MAP.get(k, ("report_only", []))
        bad = [x for x in ids if x not in registry_ids]
        if bad:
            raise SystemExit(f"field_id not in registry: {bad}")
        fmap[k] = {"match": kind, "field_ids": ids,
                   "source": ("body+toc" if k in sections and k in toc_hits else "body" if k in sections else "toc_only")}
    covered = sorted({f for v in fmap.values() if v["match"] in ("exact", "nearest") for f in v["field_ids"]}
                     | {f for k, v in mentions.items() if v for f in MENTIONS[k][1]})
    return OrderedDict(
        id=doc_id, pages=pdf_pages(pdf, raw), sha256=sha256_file(pdf),
        total_chars=len(re.sub(r"\s", "", raw)), toc_pages=sorted(toc_pages), title_found_on_first_pages=title_found,
        funding_statement_found=bool(ack_m), funders_in_funding_statement=funders, funders_named_first20pages=funders_front,
        sections=OrderedDict((k, {"n_headings": v["n_headings"], "first_page": v["first_page"],
                                  "chars": seg_chars(v["lines"])}) for k, v in sections.items()),
        toc_sections=dict(toc_hits),
        objectives_items=obj_items, rq_count=rq_items, references_count=refs, references_method=ref_method,
        tables_distinct=len(tables), figures_distinct=len(figs), mentions=mentions, field_map=fmap,
        grantthai_fields_covered=covered,
        # page, section key and numbering level only: heading wording is not stored
        headings_detected=[(pg, k, lv) for (_, pg, k, _t, lv) in heads if k],
    )


def cmd_extract(a):
    registry_ids = {json.loads(l)["field_id"] for l in open(a.registry, encoding="utf-8") if l.strip()}
    cat = {r["id"]: r for r in csv.DictReader(open(a.catalogue, encoding="utf-8"))} if a.catalogue else {}
    if a.ids_from:
        ids = [r["id"] for r in (json.loads(l) for l in open(a.ids_from, encoding="utf-8") if l.strip()) if r.get("usable")]
    else:
        ids = sorted(f[:-4] for f in os.listdir(a.pdf_dir) if f.lower().endswith(".pdf"))
    os.makedirs(os.path.join(a.out_dir, "docs"), exist_ok=True)
    if a.txt_dir:
        os.makedirs(a.txt_dir, exist_ok=True)
    rows = []
    for doc_id in ids:
        pdf = os.path.join(a.pdf_dir, doc_id + ".pdf")
        txt = os.path.join(a.txt_dir, doc_id + ".txt") if a.txt_dir else None
        doc = extract(doc_id, pdf, txt, cat.get(doc_id, {}).get("title", ""), registry_ids)
        with open(os.path.join(a.out_dir, "docs", doc_id + ".json"), "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=1)
        row = OrderedDict((k, doc[k]) for k in ("id", "pages", "sha256", "total_chars", "title_found_on_first_pages",
                                                 "funding_statement_found"))
        row["funders_in_funding_statement"] = ";".join(doc["funders_in_funding_statement"])
        row["funders_named_first20pages"] = ";".join(doc["funders_named_first20pages"])
        for k in SECTION_KEYS:
            s = doc["sections"].get(k)
            row[f"has_{k}"] = int(bool(s) or k in doc["toc_sections"])
            row[f"chars_{k}"] = s["chars"] if s else 0
        for k in ("objectives_items", "rq_count", "references_count", "references_method",
                  "tables_distinct", "figures_distinct"):
            row[k] = doc[k]
        for k, v in doc["mentions"].items():
            row[f"mention_{k}"] = int(v > 0)
        row["grantthai_fields_covered"] = ";".join(doc["grantthai_fields_covered"])
        rows.append(row)
        print(doc_id, len(doc["sections"]), len(doc["grantthai_fields_covered"]), flush=True)
    with open(os.path.join(a.out_dir, "corpus_structure.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print("rows", len(rows))


# ---------------------------------------------------------------- publish
META_COLS = ["id", "source_repository", "title_repository_record", "title_found_on_first_pages",
             "first_author_repository_record", "institution_repository_record", "funder_repository_record",
             "funding_statement_found", "funders_in_funding_statement", "funders_named_first20pages",
             "contract_or_handle", "year_be", "doc_type_repository_record", "pages", "sha256", "record_url"]
NOT_RECORDED = "not in repository record"


def _clean_meta(v):
    v = (v or "").strip()
    if not v or v.upper().startswith("NOT IN METADATA") or v.startswith("(not"):
        return NOT_RECORDED
    return re.sub(r"\s*\((?:per repository|by repository)[^)]*\)\s*$", "", re.split(r"\s+-\s+by repository", v)[0]).strip()


def cmd_publish(a):
    cat = {r["id"]: r for r in csv.DictReader(open(a.catalogue, encoding="utf-8"))}
    rows = list(csv.DictReader(open(a.structure, encoding="utf-8")))
    struct_cols = [c for c in rows[0] if c.startswith(("has_", "chars_", "mention_"))] + [
        "objectives_items", "rq_count", "references_count", "references_method", "tables_distinct", "figures_distinct",
        "grantthai_fields_covered"]
    out = []
    for r in rows:
        c = cat[r["id"]]
        m = OrderedDict()
        m["id"] = r["id"]
        m["source_repository"] = c.get("source_repo", "")
        m["title_repository_record"] = re.sub(r"\s+", " ", c.get("title", "")).strip()
        m["title_found_on_first_pages"] = int(r["title_found_on_first_pages"] == "True")
        m["first_author_repository_record"] = _clean_meta(c.get("first_author"))
        m["institution_repository_record"] = _clean_meta(c.get("institution"))
        m["funder_repository_record"] = _clean_meta(c.get("funder"))
        m["funding_statement_found"] = int(r["funding_statement_found"] == "True")
        m["funders_in_funding_statement"] = r["funders_in_funding_statement"]
        m["funders_named_first20pages"] = r["funders_named_first20pages"]
        m["contract_or_handle"] = re.sub(r";\s*contract\s*;", ";", c.get("contract_or_handle", "")).strip("; ")
        m["year_be"] = c.get("year", "")
        m["doc_type_repository_record"] = c.get("doc_type", "")
        m["pages"] = r["pages"]
        m["sha256"] = r["sha256"]
        # the record (landing) page, not the file link: file links carry
        # repository-internal identifiers and the record page names the terms
        m["record_url"] = c.get("item_page") or c.get("url", "")
        for k in struct_cols:
            m[k] = r[k]
        out.append(m)
    with open(a.out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    print("wrote", len(out), "rows to", a.out)


# ---------------------------------------------------------------- stats
def _pct(rs, col):
    return round(100 * sum(int(r[col]) for r in rs) / len(rs)) if rs else 0


def _band(y):
    y = int(y or 0)
    return "<=2559" if y <= 2559 else ("2560-62" if y <= 2562 else "2563-68")


def _med(v):
    return st.median(v) if v else 0


def _iqr(v):
    q = st.quantiles(v, n=4) if len(v) > 1 else [0, 0, 0]
    return f"{q[0]:g}-{q[2]:g}"


def cmd_stats(a):
    rows = list(csv.DictReader(open(a.csv, encoding="utf-8")))
    n = len(rows)
    groups = OrderedDict([("all", rows)])
    for src in sorted({r["source_repository"] for r in rows}):
        groups[src] = [r for r in rows if r["source_repository"] == src]
    for b in ("<=2559", "2560-62", "2563-68"):
        groups[b] = [r for r in rows if _band(r["year_be"]) == b]
    groups["Technical Report only"] = [r for r in rows if r["doc_type_repository_record"] == "Technical Report"]
    print(f"n = {n}")
    print("\n## Section presence (% of documents; heading detected in body or table of contents)\n")
    print("| section | " + " | ".join(f"{g} ({len(v)})" for g, v in groups.items()) + " |")
    print("|---|" + "---|" * len(groups))
    keys = [c[4:] for c in rows[0] if c.startswith("has_")]
    for k in sorted(keys, key=lambda k: -_pct(rows, "has_" + k)):
        print(f"| {k} | " + " | ".join(str(_pct(v, "has_" + k)) for v in groups.values()) + " |")
    print("\n## Text markers (% of documents)\n")
    for c in [c for c in rows[0] if c.startswith("mention_")]:
        print(f"- {c[8:]}: {_pct(rows, c)}")
    ip = [r for r in rows if int(r["mention_users"]) or int(r["has_users_section"])]
    ip = [r for r in ip if int(r["has_outputs"]) or int(r["has_utilization"]) or int(r["has_expected_benefit"])]
    ip = [r for r in ip if int(r["has_policy_recommendations"]) or int(r["has_recommendations"]) or int(r["mention_policy_rec"])]
    print(f"- impact-pathway proxy (users + outputs/utilization/benefit + recommendations): {len(ip)}")
    print("\n## Counts\n")
    for g in ("all",) + tuple(k for k in groups if k != "all"):
        v = [int(r["pages"]) for r in groups[g]]
        print(f"- pages [{g}]: median {_med(v):g}, IQR {_iqr(v)}, min {min(v)}, max {max(v)}")
    refs = [int(r["references_count"]) for r in rows if int(r["references_count"]) > 0]
    print(f"- references counted in {len(refs)} documents: median {_med(refs):g}, IQR {_iqr(refs)}, "
          f"max {max(refs)}, >100: {sum(x > 100 for x in refs)}; method {dict(Counter(r['references_method'] for r in rows))}")
    obj = [int(r["objectives_items"]) for r in rows if int(r["has_objectives"])]
    print(f"- objective items where an objectives section exists (n={len(obj)}): median {_med(obj):g}, "
          f"1-5: {sum(1 <= x <= 5 for x in obj)}, >5: {sum(x > 5 for x in obj)}, 0: {sum(x == 0 for x in obj)}")
    for c in ("tables_distinct", "figures_distinct"):
        v = [int(r[c]) for r in rows]
        print(f"- {c}: median {_med(v):g}, IQR {_iqr(v)}")
    sizes = {k: [int(r["chars_" + k]) for r in rows if int(r.get("chars_" + k) or 0) > 0]
             for k in keys if "chars_" + k in rows[0]}
    print("- section size, median non-whitespace characters where the section body was measured:",
          {k: f"{_med(v):g} (n={len(v)})" for k, v in sizes.items() if v})
    print("\n## Funders\n")
    fs = Counter()
    for r in rows:
        for x in set((r["funders_in_funding_statement"] + ";" + r["funders_named_first20pages"]).split(";")) - {""}:
            fs[x] += 1
    print("- documents naming each funder code (funding statement or first 20 pages):", dict(fs.most_common()))
    print("- funding statement found:", sum(int(r["funding_statement_found"]) for r in rows))
    named = [r for r in rows if r["funders_in_funding_statement"] or r["funders_named_first20pages"]]
    print("- some funder code found in the file:", len(named),
          "; none found:", [r["id"] for r in rows if r not in named])
    print("- HSRI named in file:", sum("HSRI" in (r["funders_in_funding_statement"] + r["funders_named_first20pages"]) for r in rows))
    print("- repository-record funder:", dict(Counter(r["funder_repository_record"][:40] for r in rows).most_common(6)))
    print("\n## GrantThai field_ids a detected section or marker maps to (documents)\n")
    fc = Counter(x for r in rows for x in r.get("grantthai_fields_covered", "").split(";") if x)
    for k, v in sorted(fc.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"- {k}: {v}")
    print("\n## Other\n")
    print("- years:", dict(sorted(Counter(r["year_be"] for r in rows).items())))
    print("- doc types:", dict(Counter(r["doc_type_repository_record"] for r in rows)))
    print("- title found on first 3 pages:", sum(int(r["title_found_on_first_pages"]) for r in rows))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("extract", help="extract structure from local PDFs")
    e.add_argument("--pdf-dir", required=True, help="directory of <id>.pdf files you downloaded")
    e.add_argument("--registry", required=True, help="registry/fields.jsonl")
    e.add_argument("--out-dir", required=True, help="where corpus_structure.csv and docs/<id>.json go")
    e.add_argument("--catalogue", help="catalogue CSV with id,title (used to check the title on the first pages)")
    e.add_argument("--txt-dir", help="optional cache for pdftotext output (keep it outside the repository)")
    e.add_argument("--ids-from", help="optional JSONL; only rows with usable=true are processed")
    e.set_defaults(func=cmd_extract)
    pb = sub.add_parser("publish", help="join catalogue + structure into the public CSV")
    pb.add_argument("--catalogue", required=True)
    pb.add_argument("--structure", required=True)
    pb.add_argument("--out", required=True)
    pb.set_defaults(func=cmd_publish)
    s = sub.add_parser("stats", help="aggregate tables from the public CSV")
    s.add_argument("--csv", required=True)
    s.set_defaults(func=cmd_stats)
    a = p.parse_args(argv)
    a.func(a)


if __name__ == "__main__":
    sys.exit(main())
