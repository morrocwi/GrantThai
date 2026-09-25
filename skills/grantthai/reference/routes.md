# Output routes (v0.3 router)

Since v0.3 GrantThai is a router: one work object (`work.yaml`, or a
legacy `project.yaml`) can be built through several **output routes**,
and each build writes exactly one file. Entering NRIIS is one route among
several, no longer the core.

"Router" here means a deterministic output route **chosen by a person**.
It never means an AI choosing. You (the AI) list the routes and ask; you
never pick one, and GrantThai never picks one for you: when nothing the
researcher declared decides the route, the engine stops and lists the
candidates.

## The routes

| Route id | Output file (`build/`) | For | Ready flag | Needs a fund profile |
|---|---|---|---|---|
| `nriis-proposal` | `NRIIS_SUBMISSION.md` | a research proposal the researcher copies into NRIIS by hand (unchanged from v0.1/v0.2) | `submittable` (against the bound fund profile only) | yes |
| `academic-article` | `ACADEMIC_ARTICLE.md` | a manuscript overview arranged from the researcher's own records; sub-profiles `thai-journal`, `international-journal` (both `NEEDS_VERIFICATION`) | `manuscript_ready` = no BLOCK open; **never** "accepted" or "publishable" | no |
| `concept-note` | `RESEARCH_CONCEPT_NOTE.md` | a pre-proposal working document (the old "one exception") | always a HOLD; enters no system | no |

`grantthai route list` prints the live list (id, status, output file,
accepted work types, title). A route whose file fails its contract is
still listed, with an error; building it fails, nothing is written.

## How the route is resolved

In this order, and only from what a person declared:

1. `--route ID` on the command line (or the `route` argument of the MCP /
   HTTP / Python call);
2. `routing.default_route` in `work.yaml`;
3. a legacy `project.yaml` (schema 0.2) is always `nriis-proposal`;
4. exactly one route names the file's `work_type` in its
   `default_for_work_types`;
5. otherwise the engine stops with exit 2 (the skill's `report` prints the
   candidates; MCP and HTTP return them). **Nobody picks.**

`work_type` sets defaults only. Any route can build from any object; a
route not designed for the work type gives one INFO finding (RT001), and
the rules outside the route's scope are counted in one INFO line (RT002).

## Step 0 of every session: ask

Show the researcher the table above (or `grantthai route list`) and ask,
in their language, which output they want now, for example:

- "ตอนนี้จะให้เตรียมไฟล์แบบไหน: ข้อเสนอโครงการสำหรับ NRIIS, ภาพรวมต้นฉบับบทความวิชาการ,
  หรือ concept note"
- "Which output do you want now: an NRIIS proposal overview, a manuscript
  overview, or a concept note?"

Record the answer:

- in `answers.yaml` as `project.route` (and `project.sub_profile` if they
  named one), applied with `grantthai_skill.py apply`; or
- with `grantthai_skill.py apply answers.yaml --route ID`; or
- by passing `--route ID` to every `report` / `grantthai build` call and
  writing nothing into the file.

All three record only what the researcher said. `routing` is outside
`content_sha256`, so recording a route does not make review records or a
lock stale. A legacy `project.yaml` has no `routing` block: build it with
`--route`, or run `grantthai migrate --rename` (a person's decision; it
changes the content hash) to get a `work.yaml`.

One object, several outputs: the researcher may ask for more than one
route. Build each one separately; each build writes its own file and
leaves the other route's file byte-identical.

## What changes per route

| | `nriis-proposal` | `academic-article` | `concept-note` |
|---|---|---|---|
| interview track | `reference/interview.md` | `reference/interview-article.md` (kind, venue with source, authors and roles, IMRaD from the researcher's own results, ethics, AI-use placement, data-bearing figures) | `reference/interview.md` sections 2-5 (title, keywords, team, need, problem, gap, RQ, objectives, method, ethics), no budget |
| required (BLOCK) set | registry flags + form profile | `ARTICLE.META.KIND`, `ARTICLE.FRONT.AUTHORS` | `CORE.GENERAL.TITLE_TH`, `CORE.RESEARCH.PROBLEM`, `CORE.RESEARCH.RQ.PRIMARY` |
| rule families | all | SCHEMA, S, R, CH, X, AI, FW, ART, OK, E (no budget, workplan, team or fund rules) | SCHEMA, R, CH, X, AI, FW |
| fields to ask for | `grantthai fields` | `grantthai fields --route academic-article` | `grantthai fields --route concept-note` |
| extra notice line | none | "GrantThai is not affiliated with any journal or publisher ..." under the NOTICE | "A concept note is a pre-proposal working document ..." |
| no-invention rule adds | fund, NRIIS, institutional facts | **journal facts**: scope, indexing, word limits, fees, review time, template (all `NEEDS_VERIFICATION` unless the researcher supplies the venue's own document) | as nriis-proposal |

The NOTICE constant itself is unchanged and stays line 1 of every route's
output. Nothing here submits anything anywhere: not to NRIIS, not to a
fund, not to a journal.
