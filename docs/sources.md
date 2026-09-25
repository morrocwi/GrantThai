# Sources

This file lists, bibliographically only, every source document that
informed GrantThai's design but is **excluded** from this public
repository (`docs/design/PLAN.md` §H, "Excluded from the public repo"). No
author metadata is recorded here: the publish gate uses a denylist of PDF
author strings, and excluded files are described, not named, where their
file names carry no bibliographic value.

## Handoff package (never committed as-is)

The original build-handoff package supplied by the founder. Its `core/`
files 01–06 are the basis for the `derived_from: core/0N@sha256:<hash>`
lineage tags used throughout this repository. The package itself —
including `00_READ_FIRST_AI_BUILD_BRIEF.md`, `MANIFEST.json`, `README.md`,
and `core/01`–`06` — is never committed.

| File | sha256 |
|---|---|
| `00_READ_FIRST_AI_BUILD_BRIEF.md` | `60283c3d5737b2ef898dc78bfa8358a6024f9c4663069e6d5811bfaad10d2d46` |
| `core/01_OPEN_THAI_RESEARCH_GIT_STANDALONE_ARCHITECTURE.md` | `c177c28034a71bd8dfb65965e5bba81efac9ef68e9e0d5c6ba1ed0f1f2cf8512` |
| `core/02_NRIIS_STANDALONE_v2_POLICY_ALIGNED.md` | `d36e6922a01296bd5001733ca7d5e1d2f6927fbcc08ffebde176d0d2159535a4` |
| `core/03_THAILAND_RI_ECOSYSTEM_STANDALONE_v1.1_UHC.md` | `8bdf055edc0b61d744337bdcbd664a19af581fead6ad335a6c77eb82585d4ef3` |
| `core/04_RESEARCH_PROJECT_LIFECYCLE_TIMELESS_PSEUDO_DAG.md` | `c23217441176d90f129e525248c24103575bcd85841020b2842fd237638d269a` |
| `core/05_NRIIS_RESEARCH_PROPOSAL_MASTER_SCHEMA_PSEUDO.jsonl` | `14e85efafc8633b7f50f792b0a3f71ed7abcd2f27fbea857c90064521004860e` |
| `core/06_NRIIS_RESEARCH_PROPOSAL_DAG_KGGRAPH_PSEUDO.md` | `e0f787dab03ef73c2596e91ca603f2bbdf598774c0f1623bae9e388413365d1d` |

**Rights status: resolved (founder ruling K13, 2026-09-25).** The founder,
Yaoharee Lahtee, owns core 01–06. Files derived from them are licensed
Apache-2.0 (code) and CC BY 4.0 (documentation, specifications and data),
as mapped in `REUSE.toml`. Every derived file keeps its `derived_from`
lineage tag so it stays traceable to its source. See `GOVERNANCE.md`,
"Founder decisions log".

What is derived, concretely:

- `registry/fields.jsonl` — the 100 field records of core/05, re-keyed into
  GrantThai's field-ID namespaces (table in `registry/README.md`).
  `label_en` is core/05's descriptive English label, **not** an official
  NRIIS label; every `label_th` is `NEEDS_VERIFICATION`.
- `mappings/nriis/section_to_tab.yaml` — core/05 sections to NRIIS tabs,
  from core/02's compact field map. It describes one observed form and is
  marked `NEEDS_VERIFICATION` throughout.
- `validators/rules.yaml` — rule ids and wording from core/01 §28, plus the
  rule families in `docs/design/PLAN.md` §E.
- The schemas and YAML contracts under `spec/`, as tagged in each file.

## Excluded source PDFs (SD-1 to SD-4)

These documents informed the ecosystem and fund-rule background (core/03,
core/04) and, since v0.1.0, some registry fields, candidate labels and the
contradiction register. The PDFs themselves are excluded from this
repository. Each has a short id (`SD-n`) that registry records cite
(`source_document`, `derived_from: sourcedoc/SD-n@sha256:...`).

Title, issuer and edition below were **read from each document's own cover
or first page** (not from its file name). They describe the document as
supplied; whether it is the current edition, and its official URL, are
`NEEDS_VERIFICATION`. A public document describes a form edition: nothing
taken from it is declared official or current (founder ruling K14).

| Id | Document (as printed on it) | Issuer (as printed) | Edition | sha256 | Official URL |
|---|---|---|---|---|---|
| SD-1 | คู่มือนักวิจัย ในการขอรับทุนวิจัยและนวัตกรรมจาก สำนักงานการวิจัยแห่งชาติ (วช.) (researcher's manual for research and innovation funding) | สำนักงานการวิจัยแห่งชาติ (วช.), กระทรวงการอุดมศึกษา วิทยาศาสตร์ วิจัยและนวัตกรรม | ฉบับปี 2566 | `98423019ad17f0f0aafc3863840e9d7aaa81007a84f3ddd64a10aab689a4b52e` | NEEDS_VERIFICATION |
| SD-2 | คู่มือในการส่งข้อเสนอโครงการ (proposal submission manual) | หน่วยบริหารและจัดการทุนด้านการเพิ่มความสามารถในการแข่งขันของประเทศ (บพข.) | มีนาคม 2564 | `3382acc8ca922bb39a7ad0f5996b338c992abb76dbb21e10444e2511910a39dc` | NEEDS_VERIFICATION |
| SD-3 | คู่มือการส่งข้อเสนอโครงการ (บพค.) (proposal submission manual) | as printed on PDF p1: หน่วยบริหารจัดการทุนด้านเทคโนโลยีและนวัตกรรมเพื่ออุตสาหกรรมแห่งอนาคต (บพค.) | ฉบับปรับปรุงครั้งที่ 3 (มิถุนายน 2569) | `1df827ce8af160dfb5a37e1b6c7ec3c6cc7f1b368812f73c7caf1801c6498105` | NEEDS_VERIFICATION |
| SD-4 | University lecture slides on writing a research proposal for funding (training session handout) | a university research institute's training programme (lecturer not named here) | session dated 2566 | `29ace18ff6599bef925b254f5d879b9cc267f628b0325d5c0093fa4f49b924dc` | NEEDS_VERIFICATION |

Page numbers cited anywhere in this repository are **PDF page numbers**. In
SD-1 and SD-4 the printed page number equals the PDF page; in SD-3 the
printed number is one lower (PDF p2 = printed p1).

Notes:

- **SD-1 p5 vs SD-3 PDF p1 (contradiction CX-06, OPEN).** SD-1 p5 expands the
  abbreviation บพค. as "หน่วยบริหารและจัดการทุนด้านการพัฒนากำลังคน และทุนด้านการพัฒนา
  สถาบันอุดมศึกษา การวิจัยและการสร้างนวัตกรรม (บพค.)". SD-3 PDF p1 expands the same
  abbreviation as "หน่วยบริหารจัดการทุนด้านเทคโนโลยีและนวัตกรรมเพื่ออุตสาหกรรมแห่งอนาคต
  (บพค.)". GrantThai does not choose between them and names no funding unit in
  its data.
- **SD-4 text extraction.** The text layer of SD-4 drops the Thai vowel sign
  "ำ" (sara am) in many words. Where a candidate label in
  `mappings/nriis/labels@nrct-manual-2566.yaml` comes from SD-4, the sign was
  restored by hand and the entry says so; the restored spelling is itself
  `NEEDS_VERIFICATION`.
- SD-4 quotes a typology from a further, third-party source; that source is
  not cited here and nothing is taken from it beyond what SD-4 prints.

## Excluded AI-derived readout of portal screenshots

One excluded file is an AI-generated readout of three NRIIS portal
screenshots. It is **INFERENCE**, not SOURCE, and is excluded entirely,
together with the screenshots behind it.

**Founder ruling K14 (2026-09-25): labels from this readout are not used.**
Nothing in `registry/`, `mappings/`, `spec/nriis/` or any other file in this
repository was taken from it. NRIIS labels and tab order will come later
from public call or TOR documents; until then they are
`NEEDS_VERIFICATION`.

## Excluded reference image

A Toledo concept reference image (a poster) is excluded. A redraw without
the photo, e-mail address or SDG icons, showing the direct
human-to-research-core edge, is a possible future replacement (K8, open),
and would go through the publish gate first.

## Public sources (informative, not yet independently re-verified)

None cited with a live URL yet in Phase 0. Thai fund-rule facts and NRIIS
field labels will be sourced from public call/TOR documents before any
`funds/` entry moves out of `trust_level: FICTIONAL` — see `funds/README.md`
and `spec/fund/fund-profile.schema.json`.
