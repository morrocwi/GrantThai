"""grantthai.core.pii — personal-data patterns shared by the engine and CI.

One copy of the patterns: `tools/ci/check_leak_pii.py` (the repository
leak/PII guard) imports them from here, and the validator uses them for
rule AI003 (personal-data-shaped strings in a value written with AI
assistance; docs/policy/ai-use-ceiling.md, guideline p.14).

What is detected: a checksum-valid 13-digit Thai national ID, a Thai
phone-number shape and an e-mail address (placeholder domains such as
example.com, and dated file names that look like addresses, are ignored).
What is NOT detected: names, addresses, health details, or anything that
needs meaning rather than shape. A clean scan never means "no personal
data"; it means none of these shapes was found.
"""
from __future__ import annotations

import re

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
# Thai mobile/landline-ish patterns: 0X-XXX-XXXX or 0XXXXXXXXX (10 digits
# starting with 0), optionally hyphenated.
PHONE_RE = re.compile(r"\b0\d{1,2}-?\d{3}-?\d{3,4}\b")
THAI_ID_RE = re.compile(r"\b\d{13}\b")

# Emails that are clearly placeholders/examples and must not be flagged.
EMAIL_ALLOWLIST_DOMAINS = {"example.invalid", "example.com", "example.org", "example.net"}
FICTIONAL_EMAIL_DOMAIN_HINT = "@example."

# Dated filenames like "positions@2026-09.yaml" look like emails to a
# naive regex; exclude common non-email file extensions as the "TLD".
NON_EMAIL_FILE_EXTENSIONS = {
    "yaml", "yml", "json", "md", "py", "txt", "jsonl", "html", "j2",
    "cff", "toml", "sh", "bat", "command", "jpg", "pdf",
}


def thai_id_checksum_valid(digits: str) -> bool:
    if len(digits) != 13 or not digits.isdigit():
        return False
    d = [int(c) for c in digits]
    total = sum(d[i] * (13 - i) for i in range(12))
    check = (11 - (total % 11)) % 10
    return check == d[12]


def is_real_email(email: str) -> bool:
    """False for placeholder domains and file-name look-alikes."""
    domain = email.split("@", 1)[1].lower()
    tld = domain.rsplit(".", 1)[-1]
    if domain in EMAIL_ALLOWLIST_DOMAINS or FICTIONAL_EMAIL_DOMAIN_HINT in email.lower():
        return False
    return tld not in NON_EMAIL_FILE_EXTENSIONS


def find(text: str) -> list[tuple[str, str]]:
    """Every personal-data-shaped match in `text`, as (kind, matched text).
    kind is one of thai_national_id, phone, email."""
    out: list[tuple[str, str]] = []
    for m in THAI_ID_RE.finditer(text):
        if thai_id_checksum_valid(m.group(0)):
            out.append(("thai_national_id", m.group(0)))
    for m in PHONE_RE.finditer(text):
        out.append(("phone", m.group(0)))
    for m in EMAIL_RE.finditer(text):
        if is_real_email(m.group(0)):
            out.append(("email", m.group(0)))
    return out


def find_in_value(value) -> list[tuple[str, str]]:
    """find() over every string inside a value (strings, lists, objects)."""
    out: list[tuple[str, str]] = []
    if isinstance(value, str):
        out.extend(find(value))
    elif isinstance(value, list):
        for x in value:
            out.extend(find_in_value(x))
    elif isinstance(value, dict):
        for x in value.values():
            out.extend(find_in_value(x))
    return out


# The warning an AI operator shows the researcher BEFORE accepting any
# research data (docs/policy/ai-use-ceiling.md, section 5; the guideline's
# p.14-16). GrantThai's ceiling is stricter than the guideline for
# confidential, unpublished and pre-patent material (the guideline says
# "take care", p.15): the policy says so. One copy, used by the MCP server,
# the HTTP API and the skill script.
GUIDELINE_SHORT_EN = "national GenAI research-ethics guideline for researchers (September 2569)"
GUIDELINE_SHORT_TH = "แนวทางการประยุกต์ใช้ Generative AI อย่างมีจริยธรรมสำหรับนักวิจัย (กันยายน 2569)"

DATA_WARNING_EN = (
    "Before you share research data: anything typed into a public AI service is sent to a third party. "
    "Do not give it personal data that identifies anyone (names, national ID numbers, health data), "
    "participants' records, confidential project material, contracts, trade secrets, unpublished data, "
    "material you plan to patent, or dual-use information. If you must, use a closed or local system, with "
    "approval and a recorded reason. Describe data by its type instead. The AI tool and its version are "
    "recorded in authoring.ai_use_declaration. (" + GUIDELINE_SHORT_EN + ", p.14-16; "
    "docs/policy/ai-use-ceiling.md)"
)
DATA_WARNING_TH = (
    "ก่อนให้ข้อมูลวิจัย: ข้อมูลที่พิมพ์ลงบริการ AI สาธารณะเท่ากับส่งให้บุคคลที่สาม "
    "อย่าให้ข้อมูลส่วนบุคคลที่ระบุตัวตนได้ (ชื่อ เลขบัตรประชาชน ข้อมูลสุขภาพ) ข้อมูลของผู้เข้าร่วมวิจัย "
    "เอกสารลับของโครงการ สัญญา ความลับทางการค้า ข้อมูลที่ยังไม่ตีพิมพ์ สิ่งที่จะยื่นจดสิทธิบัตร "
    "หรือข้อมูลที่ใช้ได้สองทาง (dual-use) ถ้าจำเป็นจริงให้ใช้ระบบปิดหรือระบบในเครื่อง โดยมีการอนุมัติและบันทึกเหตุผล "
    "ให้บอกเพียงประเภทของข้อมูลแทนตัวข้อมูล ชื่อและเวอร์ชันของเครื่องมือ AI จะถูกบันทึกไว้ใน "
    "authoring.ai_use_declaration (" + GUIDELINE_SHORT_TH + " หน้า 14–16; docs/policy/ai-use-ceiling.th.md)"
)
