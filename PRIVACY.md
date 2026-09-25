# Privacy (PDPA)

## English

GrantThai (v0.x) runs entirely on your own computer. There is no server, no
account system, and no telemetry. GrantThai does not collect, transmit, or
store any personal data anywhere outside your own device.

- Your project data lives in a `project.yaml` file and a private
  `workspaces/` folder you control, outside this repository. Personal data
  used in a submission (names, team, institution) is stored in
  `project.yaml` (`PROFILE.*` fields); an optional local `profile.yaml` only
  pre-fills those fields while you edit. `.gitignore` excludes
  `profile.yaml`, `build/` and `workspaces/`.
- `grantthai export` excludes personal data (PII) by default. Use
  `--include-private` to opt in explicitly, and you will see a warning when
  you do.
- ORCID is optional and typed by hand; NRIIS credentials are never stored
  by GrantThai (there is no NRIIS API integration in v0.x).
- All examples in this repository (`examples/`, `funds/example/`) use
  obviously synthetic names and checksum-invalid ID numbers, and carry a
  `FICTIONAL` banner. No example combines a real place name with a real
  institution name.
- A CI check scans for Thai national ID numbers (with checksum
  validation), phone numbers, and email addresses (see
  `tools/ci/check_leak_pii.py`, run by `.github/workflows/ci.yml` and
  `leak-scan.yml`). The guard's own failing test input is generated at test
  run time with synthetic values (a checksum-valid number that starts with
  0, which no real Thai ID does; an unissuable phone number; a reserved
  `.test` e-mail domain), so no PII-shaped value is committed.
- A future hosted service (not part of this repository's scope) would
  require a Data Protection Impact Assessment (DPIA) and a named PDPA data
  controller before launch — this is decision K2 in the plan, and is not
  started.

If you believe personal data has leaked into this repository, see
`SECURITY.md` for how to report it.

## ภาษาไทย

GrantThai (v0.x) ทำงานบนเครื่องของคุณเองทั้งหมด ไม่มีเซิร์ฟเวอร์ ไม่มีระบบบัญชีผู้ใช้
และไม่มีการส่งข้อมูลการใช้งานกลับไปที่ใด ๆ GrantThai ไม่เก็บ ไม่ส่ง และไม่บันทึกข้อมูล
ส่วนบุคคลใด ๆ ออกนอกเครื่องของคุณ

- ข้อมูลโครงการของคุณอยู่ในไฟล์ `project.yaml` และพื้นที่ทำงานส่วนตัว (`workspaces/`)
  ที่คุณควบคุมเอง นอก repository นี้ ข้อมูลส่วนบุคคลที่ใช้ในการยื่น (ชื่อ ทีม สถาบัน)
  เก็บอยู่ใน `project.yaml` (ฟิลด์ `PROFILE.*`) ส่วนไฟล์ `profile.yaml` (ถ้ามี)
  ใช้แค่ช่วยกรอกล่วงหน้าระหว่างแก้ไข
- คำสั่ง `grantthai export` จะไม่รวมข้อมูลส่วนบุคคลโดยค่าเริ่มต้น ต้องใช้
  `--include-private` เพื่อเลือกรวมเอง และจะมีคำเตือนแสดงขึ้น
- ORCID เป็นทางเลือกและพิมพ์เองได้ ไม่มีการเก็บรหัสผ่านหรือบัญชี NRIIS ใด ๆ
- ตัวอย่างทั้งหมดในโครงการนี้ใช้ชื่อสมมติที่ชัดเจนและเลขบัตรที่ไม่ผ่าน checksum จริง
  พร้อมป้าย FICTIONAL กำกับเสมอ
- มีการตรวจใน CI สำหรับเลขบัตรประชาชนไทย (ตรวจ checksum) เบอร์โทร และอีเมล
  ข้อมูลทดสอบที่ใช้ตรวจว่าตัวตรวจทำงานจะถูกสร้างขึ้นตอนรันทดสอบด้วยค่าสมมติเท่านั้น
  (เลข 13 หลักที่ขึ้นต้นด้วย 0 ซึ่งไม่มีบัตรจริงใดขึ้นต้นเช่นนี้ เบอร์โทรที่ออกให้ใครไม่ได้
  และโดเมนอีเมล `.test` ที่สงวนไว้) จึงไม่มีข้อมูลที่ดูเหมือนข้อมูลส่วนบุคคลถูก commit
- บริการแบบมีศูนย์กลาง (hosted) ในอนาคตต้องมี DPIA และผู้ควบคุมข้อมูลตาม PDPA
  ที่ระบุชื่อไว้ก่อนเปิดใช้งาน — เป็นประเด็นที่ยังไม่ตัดสิน (K2) และยังไม่เริ่มทำ
