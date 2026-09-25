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

## Excluded source PDFs

These documents informed the ecosystem and fund-rule background (core/03,
core/04) but are excluded entirely. Only a sha256 fingerprint and what is
known about each is recorded. Titles, issuers and editions are
`NEEDS_VERIFICATION`: they will be recorded from the public documents
themselves, not from file names.

| Document | Issuer | Edition | sha256 | Official URL |
|---|---|---|---|---|
| Excluded source document 1 (PDF, title NEEDS_VERIFICATION) | NEEDS_VERIFICATION | NEEDS_VERIFICATION | `98423019ad17f0f0aafc3863840e9d7aaa81007a84f3ddd64a10aab689a4b52e` | NEEDS_VERIFICATION |
| Excluded source document 2 (PDF, title NEEDS_VERIFICATION) | NEEDS_VERIFICATION | NEEDS_VERIFICATION | `3382acc8ca922bb39a7ad0f5996b338c992abb76dbb21e10444e2511910a39dc` | NEEDS_VERIFICATION |
| Excluded source document 3 (PDF, title NEEDS_VERIFICATION) | NEEDS_VERIFICATION | NEEDS_VERIFICATION | `1df827ce8af160dfb5a37e1b6c7ec3c6cc7f1b368812f73c7caf1801c6498105` | NEEDS_VERIFICATION |
| University lecture slides on writing a research proposal | NEEDS_VERIFICATION | NEEDS_VERIFICATION | `29ace18ff6599bef925b254f5d879b9cc267f628b0325d5c0093fa4f49b924dc` | NEEDS_VERIFICATION |

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
