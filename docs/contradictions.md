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
