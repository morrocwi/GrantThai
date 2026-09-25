# Deviations from the original handoff package

`docs/design/PLAN.md` is the design plan this scaffold follows (a
historical record; where it and `spec/` differ, `spec/` wins). Several of its
provisions intentionally depart from the original AI handoff package
(`00_READ_FIRST_AI_BUILD_BRIEF.md`, `core/01`–`06`). This file is the single
place those departures are recorded, per plan section E ("These names
deliberately depart from 01:626-636 ... The departure is recorded in
`docs/deviations.md`") and section I ("Recorded deviations from the
package").

| Deviation | Original (package) | GrantThai (this repo) | Why | Where decided |
|---|---|---|---|---|
| MCP implementation timing | v0.1 (B:134, B:194) | v0.4; only the contract (`spec/mcp/tools.schema.json`) ships early | v0.1 scope held to the lecturer no-AI path (P3); MCP is an optional interface layer, never required for a human to finish a project | plan §D, §G, §I |
| SHACL timing | v0.1 (01 §63 item 6) | v0.2; generated from `spec/common/chain.yaml`, never hand-maintained | Reduces validation engines from three to two in v0.1; a founder sign-off (K15) is requested for this deferral | plan §E "Validation engines", §K15 |
| AI routing timing | v0.2 (01 §64) | v0.3, after the no-AI citizen path ships | The no-AI citizen path (v0.2) must exist and be tested before any AI-assisted routing is introduced, per the amended version order | plan §I |
| `ai_assisted_fill` default | `true` (01:558-563) | `false`; becomes `true` only on explicit user opt-in | Prevents AI-assisted browser fill from being silently on by default | plan §F |
| Status name `SOURCE_CHECKED`/`METHOD_CHECKED` | let AI set these "checked" states (01:626-636) | renamed `STRUCTURE_CHECKED` ("schema-valid; source reference present and resolvable" — does not mean the source supports the value) and `LOGIC_LINKED` ("required chain links exist" — does not mean the method fits); only a deterministic validator pass sets either | Prevents status overclaim; a "checked" status must never imply more confidence than a schema/logic pass actually gives | plan §E |
| `VERIFIED` on self-review | allowed VERIFIED to render as-is regardless of who checked it | `VERIFIED` with `independence: self` renders as `AUTHOR_CHECKED`; only `VERIFIED(independent: <role>, <date>)` renders as written | Prevents self-review from reading as independent verification | plan §E, critic-parity finding 6/7 |
| "AI-SUPPORTED TRANSLATION" / "AI is a translator, scaffold, router" (brief B:12-25) | AI positioned as the headline of the canonical chain | Person-first translation; AI-assisted is explicitly optional; the word "router" is dropped from all repo prose | AI must never become the de facto requirement in practice (P3); the founder ruled the neutral philosophy wording on 2026-09-25 (K1) | plan §A |
| Version/phase order | (implicit) AI-assisted features earlier, citizen features later | AI-free Expert → AI-free Citizen → AI → interfaces → real funds | Founder amendment: AI is optional at every step, so every core path must be proven AI-free before any AI-assisted feature ships | plan §I, §L "Other chair changes" |
| AT-1 acceptance test placement | implicitly tied to v0.1 in the draft | moved to v0.2 (Citizen Mode) | AT-1 as written concerns the citizen/no-PI path, which ships in v0.2, not v0.1 | plan §L |
| Review-gate prefix | package/letter used "G0-G4" | renamed to `RG0`-`RG4` | Avoids a naming clash with the G001-G003 geography validation rule family | plan §E, critic-feasible finding 5 |
| "Signed" review records | letter referred to "signed" records | renamed "named review records"; there is no cryptographic signing in v0.x | Overclaim correction — nothing is cryptographically signed yet | plan §E, critic-publish finding 14 |
| Founder's term "verified project object" | used freely | kept only in `docs/lineage.md`; public prose says "checked against GrantThai rules" instead | Prevents implied third-party verification/endorsement | plan §E |
| Thai NRIIS field labels | implicitly sourced from the screenshot-derived analysis file | `LABEL_TH: NEEDS_VERIFICATION` until captured from a public call/TOR document | Founder ruling K14 (2026-09-25): labels from the screenshot-derived readout are not used; labels and tab order come from public documents later | plan §E, §H, §K14 |
| `direct_submit` | not explicitly fixed as always false in the package | always `false`; `human_final_approval_required` always `true` | P9 "Humans decide" — GrantThai never submits on a person's behalf | plan §A (P9), §F |
| Cold-read acceptance check | "two equal acceptance checks: a human cold read and an AI cold read" (plan §F, B:215) | release QA only: a human cold read is required; an AI cold read is optional and additional. No cold read is ever a condition for a user to trust or use their own file | Founder ruling 2026-09-25: AI stays optional everywhere, so no check may require an AI | `GOVERNANCE.md` founder decisions log |
| `profile.yaml` as an architecture input | plan §C draws Profile as an arrow into the research core | `profile.yaml` is an editor convenience only; identity/team data used in the submission lives in `project.yaml` (`PROFILE.*`); `grantthai build` never reads `profile.yaml` | Keeps the one-input contract exact | `spec/contracts/one-input-one-output.md` |
| Independent check for releases | plan §H step 4: "AI review never counts as the independent check" | a checker distinct from the maker (a different person or a different, fresh AI agent) plus the human founder's approval of every public release | Founder ruling 2026-09-25 | `GOVERNANCE.md` |
| Public status wording | "validated against GrantThai rules" (plan §E) | "checked against GrantThai rules" / "structure-checked" | Avoids overclaim: nothing is validated by an outside party | `spec/common/status.yaml` |

See also `GOVERNANCE.md` "Recorded dissent" for decisions where a critic
finding was only partly applied, and `docs/design/PLAN.md` §L for the
full change log against the original draft plan.
