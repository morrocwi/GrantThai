# Contradiction register

This file lists every contradiction GrantThai has found between the files of
the original handoff package (`core/01`–`06`) and the public source documents
`SD-1`–`SD-4` (described in `docs/sources.md`), where it touches GrantThai's
data. The machine-readable copy is `registry/contradictions.yaml`;
`tests/test_contradictions.py` keeps the two in step.

Rules for this register:

- **Nothing here is resolved.** Every entry keeps both readings and says how
  GrantThai behaves today. The behaviour is a working default, not a ruling.
  Every entry is `OPEN` until a person with the authority to decide records a
  decision (see `GOVERNANCE.md`).
- **Contradictions are surfaced, never merged.** A field touched by an entry
  lists its id under `conflicts` in `registry/fields.jsonl`, and the output
  file prints every open entry that touches the project's fields in its
  "Conflicts and open contradictions" section
  (`spec/output/nriis-submission.contract.md`).
- A project can record its own conflicts (for example, two sources that
  disagree about a number) in a field record's `conflicts` list
  (`spec/common/field_record.schema.json`). Those are printed in the same
  section.
- Page numbers are PDF page numbers. In SD-1 and SD-4 the printed page number
  is the same; in SD-3 the printed number is one lower.

| Id | Topic | Reading A | Reading B | GrantThai today |
|---|---|---|---|---|
| CX-01 | Research Core and Methodology: authoring fields or observed NRIIS fields? | core/02 §1 R4 and §5 04/05: `AUTHORING_CORE`, never presented as NRIIS fields; they reach NRIIS through the narrative renderer (§6) | core/05: every `CORE.*` and `METHOD.*` record has `source_status: OBSERVED` | `origin: AUTHORING_CORE`, not placed on a tab; `source_status` kept as core/05 wrote it; narrative boxes carry `render_from` |
| CX-02 | Need, Problem, Gap, Innovation: text or objects? | core/05: `type: text` | core/02 §5 04.01–04.03, 04.08: objects with named keys | type `rich_text\|object`: either form is valid |
| CX-03 | Direction of Budget–Activity and Ethics–Method edges | core/06 §3 and core/02 §11: Budget → Activities, Ethics → Methodology | core/06 §4 and §12: Activity → Budget item, Methodology → Ethics requirement | `spec/common/chain.yaml` follows core/06 §4/§12; sites and partners are attribute links |
| CX-04 | Impact after Beneficiary, or both after Outcome? | core/06 §3: Outcomes → Beneficiaries → Impacts → KR | core/02 §11 and core/06 §4: Outcome → Beneficiary and Outcome → Impact | `chain.yaml` fans out from Outcome |
| CX-05 | Project characteristic: new only, or new or continuing? | core/05: `allowed_values: ["New Project"]` | SD-1 (2566) p15 part 1 item 3: new, or continuing from an earlier fiscal year, with a past-performance table | `"New Project"` allowed; `"Continuing Project"` is a candidate (`NEEDS_VERIFICATION`) accepted with REVIEW finding S011; table in `CORE.GENERAL.PAST_PERFORMANCE` |
| CX-06 | Two full names for one funding-unit abbreviation | SD-1 (2566) p5 | SD-3 (revision 3, 2569) PDF p1 | Not resolved; exact strings are in `docs/sources.md` only; GrantThai's data names no funding unit |
| CX-07 | Expert connections and stakeholder engagement: which tab? | core/02 §9: Utilization | SD-1 (2566) p17 part 3 item 9 (the plan part), with post-project continuation | Kept on `UTILIZATION`, `NEEDS_VERIFICATION` |
| CX-08 | Expected outcomes: form item or extension? | core/02 §5 09.04: `RECOMMENDED_EXTENSION`; core/05: `INFERRED_SCHEMA_EXTENSION` | SD-1 (2566) p18 part 5 item 4: a numbered form item | `origin: NRIIS_NATIVE` (placed on `UTILIZATION`), `NEEDS_VERIFICATION` |
| CX-09 | How many form parts, in what order? | core/02 §9: five (General, Project, Workplan, Utilization, Attachments/Validation) | SD-1 (2566) p15–18: parts 1–5 incl. part 4 entrepreneur information; SD-4 p164 and p166: attachments and a validation page as parts 5 and 6; SD-5 (FF 2570) p1/p3/p6/p12: four parts (general, project, workplan, outputs/outcomes/impacts) | Five tabs kept (`NEEDS_VERIFICATION`); entrepreneur information on `UTILIZATION`; validation page not modelled; form profiles shipped in v0.2, none overrides the tab order (SD-5's reading recorded, not applied) |
| CX-10 | OECD primary/secondary or main/sub? | core/05: primary and secondary field, no list | SD-1 (2566) p15 item 6 and p20: main/sub field with a list | `PRIMARY` takes a main-group candidate code, `SECONDARY` a sub-field code; outside the candidate list = REVIEW (S011), never BLOCK |
| CX-7SSA-01 | 7SSA: two Thai names for each sector | 7SSA master schema v1.0 (founder-authored; sha256 1c8989c0...f980) §1: master Thai sector names, e.g. S2 'แนวทาง ขอบเขต และฐานความรู้', S3 'ฐานแนวคิดและองค์ความรู้เดิม'. | 7SSA master schema v1.0 (founder-authored; sha256 1c8989c0...f980) §5.1 (and the Thai-renderer comments of the LaTeX template): Thai-7 visible headings, e.g. S2 'แนวทางและขอบเขตการวิเคราะห์', S3 'แนวคิด ทฤษฎี และองค์ความรู้ที่เกี่ยวข้อง'. | The §1 names are the sector ids and print in the [S#] markers; the §5 headings print as the visible headings of the Thai profiles. Neither is changed. |
| CX-7SSA-02 | 7SSA: which English heading for each sector | 7SSA master schema v1.0 (founder-authored; sha256 1c8989c0...f980) §4: world renderer headings, e.g. S4 'The Unresolved Problem', S5 'Theory / Framework / New Contribution'. | GLOSA-7SSA LaTeX template (templates/tex/glosa_7ssa_v1.tex, vendored): section titles, e.g. S4 'Problem in Existing Knowledge', S5 'New Contribution'.; 7SSA master schema v1.0 (founder-authored; sha256 1c8989c0...f980) §15: per article type, e.g. philosophical S6 'Objections and Replies', legal S6 'Counterauthority / Consequences / Limits'. | The article-type overlay (§15) wins when ARTICLE.SSA.ARTICLE_TYPE is set; otherwise the §4 headings. The LaTeX export uses the same resolver and rewrites the template's section titles (INSTINCT precedence, recorded here). |
| CX-7SSA-03 | 7SSA: how many abstract slots | 7SSA master schema v1.0 (founder-authored; sha256 1c8989c0...f980) §13.2: five functional slots: problem, gap, approach, contribution, implication. | 7SSA master schema v1.0 (founder-authored; sha256 1c8989c0...f980) §13.3: the Thai abstract has four: problem, approach, proposal, contribution.; GLOSA-7SSA LaTeX template (templates/tex/glosa_7ssa_v1.tex, vendored): adds a boundary/limitation slot and '150-250 words'. | No abstract structure is imposed; the abstracts print as the researcher wrote them. The word range is not imported (a venue fact, NEEDS_VERIFICATION). |
| CX-7SSA-04 | 7SSA: the expansion rule matches neither compression map | 7SSA master schema v1.0 (founder-authored; sha256 1c8989c0...f980) §17: moving a Thai article to the world form splits Thai Sector 3 into world 3+4 and Thai Sector 4 into world 5+6. | 7SSA master schema v1.0 (founder-authored; sha256 1c8989c0...f980) §5.2, §5.3, §18, §35: the Thai compressions merge S2+S3 and S5+S6 (five) or S4+S5+S6 (four); none maps a Thai 'Sector 3' onto world 3+4. | Only §5/§18/§35 drive the deterministic compression; §17 is guidance for the researcher and is not applied. |
| CX-7SSA-05 | 7SSA: where the core epistemic roles go | GLOSA-7SSA LaTeX template, the founder's first version: the core roles (plus a fourth, the accountable approver) only inside the switchable audit appendix. | glosa P20 (Core Epistemic Structure): a three-role block near the top of every draft, always on. | GrantThai vendors the glosa-registered copy, which adds the always-on front block and keeps the fourth role as an accountability line in the appendix. The Markdown overview prints its own role block (section 4.8). |
| CX-7SSA-06 | 7SSA: Thai script and the LaTeX export | 7SSA master schema v1.0 (founder-authored; sha256 1c8989c0...f980) §5: Thai headings and a Thai abstract for Thai targets. | GLOSA-7SSA LaTeX template (templates/tex/glosa_7ssa_v1.tex, vendored): a portable pdflatex master; Thai text kept in comments; Thai script needs a XeLaTeX/LuaLaTeX derivative. | The tex export is English-only: every Thai value prints as a NEEDS_INPUT note and a Thai-heading profile adds one NEEDS_INPUT note that the Thai layout is not exported. Recorded in docs/deviations.md. |
| CX-7SSA-07 | 7SSA: a quartile as a quality gate | 7SSA master schema v1.0 (founder-authored; sha256 1c8989c0...f980) §26, §36: a 'Q1 world quality gate' and a current-Q1 check before submission. | GrantThai AGENTS.md non-negotiables; the academic-article route: no BLOCK or readiness input rests on a venue fact; every venue fact is NEEDS_VERIFICATION until the researcher supplies the venue's document. | Not imported as a gate. 'Q1' appears only as the source's name for a renderer and as the researcher's own declared target_system. The source's own §27 keeps Thai journals first-class. |
| CX-7SSA-08 | 7SSA: integrity and verification as stored booleans | 7SSA master schema v1.0 (founder-authored; sha256 1c8989c0...f980) §19, §30: integrity booleans (citations_verified, all_claims_traceable ...) and human_verified: true on claims. | GrantThai review records (spec/common/object-hash.md, grantthai review): review state lives in named review records tied to content_sha256; a self-set boolean is not a check. | Not imported. The overview prints review gates from review records only. |
| CX-7SSA-09 | 7SSA: AI simulation used as review | 7SSA master schema v1.0 (founder-authored; sha256 1c8989c0...f980) §29, §36: AI red-team, desk-reject simulation and analysis of recent journal articles as part of the workflow. | GrantThai AI-use ceiling (docs/policy/ai-use-ceiling.md); glosa independence ladder: an AI never validates; an AI reading of one's own draft is advisory at most and never a review record. | Not imported. The skill may help the researcher think through objections to their own draft (advisory only); nothing is recorded as a review. |
| CX-7SSA-10 | 7SSA: every sector VERIFIED vs GrantThai's DRAFT ceiling | 7SSA master schema v1.0 (founder-authored; sha256 1c8989c0...f980) §33: an article is complete when all sectors S1-S7 are VERIFIED. | GrantThai status model (spec/common/status_permissions.yaml): the tool never sets a status above DRAFT; higher states come only from named human review records. | Sector status is a readout of what is filled (the sector map), never a stored status. |
| CX-7SSA-11 | 7SSA: article types vs ARTICLE.META.KIND | 7SSA master schema v1.0 (founder-authored; sha256 1c8989c0...f980) §15: eight article types: conceptual, theory, philosophical, legal, integrative review, formal/mathematical conceptual, CS SoK/survey, policy/governance. | GrantThai ARTICLE.META.KIND (router 2026-09-25): six kinds: empirical_research, review, conceptual, case_study, short_communication, other. | A separate field, ARTICLE.SSA.ARTICLE_TYPE (RECOMMENDED_EXTENSION), carries the eight types; KIND is unchanged. KIND empirical_research with a 7SSA profile is INFO 7SSA-08. |
| CX-7SSA-12 | 7SSA: one output template per route vs a LaTeX export | spec/routes/route.schema.json (router v0.3): exactly one .md.j2 template and one .md file per route. | GLOSA-7SSA LaTeX template (templates/tex/glosa_7ssa_v1.tex, vendored): a journal-facing LaTeX manuscript built from the same seven sectors. | The route keeps one Markdown template (the 7SSA body is an included partial) and gains an optional `exports` list; `build --format tex` writes exactly one .tex file instead of the Markdown file. |

## Notes per entry

**CX-01.** The audit of `main@09d4475` found this reconciled silently: the
first registry followed core/05 and rendered every research-core and
methodology record as its own box on the
Project tab (28 boxes there), so the methodology appeared twice. Since v0.1.0 the registry has an
`origin` per record (core/02 §2) and only `NRIIS_NATIVE` records are placed on
a tab. The research-core records still appear in the output, in the appendix
"Project records not placed on any NRIIS tab", with the narrative box each one
feeds.

**CX-03 and CX-04.** The package draws these edges both ways in different
sections. Earlier drafts of `chain.yaml` called the choice a "direction
choice"; it is recorded here as a contradiction instead. Changing a direction
changes which links a person writes and which rules fire, so it needs a
decision, not a silent edit.

**CX-05.** The candidate value text `Continuing Project` is GrantThai's
English wording. The official option text is `NEEDS_VERIFICATION`.

**CX-08.** GrantThai follows the public document for placement because the
goal of v0.1 is to answer the real form as completely as the sources allow.
The package's reading is kept here, not dropped.

**CX-10.** The p20 list is carried as candidate values in
`mappings/nriis/labels@nrct-manual-2566.yaml`; see that file for the codes.

**CX-7SSA-01 to CX-7SSA-12.** Found while registering the 7SSA structure
profiles (the founder-authored 7SSA master schema v1.0 and its LaTeX
template) on the academic-article route. Readings are cited by section of
the source; the source text is not reproduced here. Several of these record
what GrantThai deliberately does NOT import (a quartile as a gate, stored
verification booleans, AI simulation as review, per-sector VERIFIED status),
so that the decision is visible instead of silent.
