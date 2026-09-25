# The one-input, one-output contract (0.3.0-draft: one output per route)

**Founder's reframe (verbatim, 2026-09-25):** "ปรับรูปแบบ การลงใน NRIIS
ไม่ใช่แกนหลักอีกต่อไป แต่เป็นแค่ทางเลือกหนึ่งของ router เพราะเราจะเปิดให้ตั้งแต่การทำ
บทความวิชาการด้วย ไม่ใช่แค่วิจัย" — entering NRIIS is no longer the core; it
is one option of a router, because GrantThai opens to academic articles as
well, not only research proposals.

**Founder's earlier core goal (verbatim, 2026-09-25, kept as history):**
"อย่าลืมนะ เป้าหมายคือ input เข้าทางเดียว แล้ว ออกมาเป็นรายงานที่พร้อมเข้าระบบลงทะเบียน
NRIIS ได้เลยเป็นไฟล์เดียว" — one input path in, one file out that is ready
to enter into NRIIS. That goal is unchanged for the NRIIS route; the reframe
makes it one route among several.

This is the headline contract for the whole system. Every other design
choice in this repository (forms, questionnaires, optional AI assist,
review gates, fund binding, routes) exists to feed exactly one input and,
per route, produce exactly one output.

## The word "router"

"Router" here means a **deterministic output route chosen by a person**:
the researcher declares the route in `work.yaml` (`routing`) or on the
command line (`--route`). No AI and no tool ever picks a route; when the
choice is ambiguous the tool stops and lists the candidates. This is the
opposite of the older sense "AI as router" (an AI deciding where a person's
work goes), which stays dropped (`docs/deviations.md`, decision K-R1).

## ONE INPUT

`work.yaml` (`spec/work/work.schema.json`, `0.3.0-draft`) is the **only
file `grantthai build` reads** apart from the bound fund profile (below,
and only for routes that need one) and GrantThai's own shipped data
(registry, routes, mappings, rules, templates).

- A legacy `project.yaml` (`spec/project/project.schema.json`,
  `0.2.0-draft`) is read unchanged: in memory it is a `work.yaml` with
  `work_type: research_proposal` and `routing.default_route:
  nriis-proposal`, its `form_profile` becoming the NRIIS route's
  sub-profile. Its bytes and its `content_sha256` do not change, so
  existing review records stay current. `grantthai migrate [--rename]`
  rewrites it to 0.3 explicitly; nothing rewrites it implicitly.
- `grantthai build [PATH]` with a directory or no path looks for
  `work.yaml`, then `project.yaml`. **If both exist in the same directory
  the command stops with exit 2** ("two canonical inputs; keep one"). The
  one-input rule is enforced, not assumed.
- The Markdown forms (`forms/*.md`), the questionnaires
  (`interview/*.yaml`), `grantthai init`, `grantthai set`, the deferred
  offline web form, and any optional AI-assisted feature
  (`src/grantthai/assist`, the skill, MCP, HTTP) are all **editors** of
  this one file. Editors are never separate inputs, and their outputs are
  never silently merged at build time.
- **Identity and team data.** Everything about people that an output uses
  (names, roles, institutions, ORCID, contribution percentages, article
  author order) lives **in `work.yaml`**, in `PROFILE.*` and `ARTICLE.*`
  fields. A local `profile.yaml` (`spec/profile/profile.schema.json`) is
  only an **editor convenience**: `grantthai init` and the web form may
  read it to pre-fill `PROFILE.*` fields, and the values are then *copied*
  into `work.yaml`. `grantthai build` — and every other command that
  produces output — **never reads `profile.yaml`**.
- **Fund profile = bound reference, not a second input.** It is named by
  `fund_binding.fund_profile_id` inside `work.yaml` and resolves to exactly
  one path, `funds/<fund_profile_id>/fund-profile.yaml`. In 0.3
  `fund_binding` is optional at the object level and required only by
  routes whose `needs_fund_binding` is true (today: `nriis-proposal`).
- **Routing is a declaration, not content.** `routing` (declared routes,
  default route, sub-profiles) is excluded from `content_sha256`
  (`spec/common/object-hash.md`): choosing where to send a piece of work
  does not make a review record or the lock stale. `work_type` stays
  inside the hash.

## ONE COMMAND PER ROUTE

```
grantthai build [PATH] --route <route-id>          # same as: grantthai route build --route <route-id>
grantthai build [PATH]                              # the object's declared default route, or the legacy route
```

The route is resolved in this order, and the tool never chooses between
routes:

1. `--route` on the command line;
2. `routing.default_route` in the object;
3. a legacy 0.2 `project.yaml` → `nriis-proposal`;
4. exactly one route lists the object's `work_type` in
   `default_for_work_types` → that route;
5. otherwise exit 2, listing the candidates (the Python API raises
   `AmbiguousRoute`; MCP and HTTP return the candidate list).

No other command produces a route's output. The full command list (see
`grantthai --help` for what is implemented):

| Command | Reads | Writes | Route output? |
|---|---|---|---|
| `init [PATH] [--work-type T] [--fund ID]` | — | a blank `work.yaml` (refuses to overwrite) | no |
| `migrate [PATH] [--rename] [--dry-run]` | `project.yaml` | `work.yaml` 0.3 (`--rename` removes `project.yaml`); prints which review gates go stale | no |
| `set <FIELD_ID>` | `work.yaml` | `work.yaml` | no |
| `route list` | `routes/INDEX.yaml` | a list (id, title, output filename, accepted work types, status) | no |
| `route check --route ID [--sub-profile SP]` | `work.yaml`, the route, a bound fund profile if the route needs one | a route-scoped validation report (report-only) | no |
| `validate [--route ID]` | same | a validation report; may persist validator statuses | no |
| `fields [--route ID]` | registry, route placement | a list | no |
| `explain <RULE_ID>` | `validators/rules.yaml` | — | no |
| `build [--route ID] [--sub-profile SP] [--out DIR]` | `work.yaml`, the route, a bound fund profile if the route needs one | `build/<route output filename>` | **yes — the one output of that route** |
| `route build --route ID ...` | same | same | **yes — identical to `build --route`** |
| `review`, `accept-mapping`, `reject-mapping`, `lock`, `diff`, `link` | `work.yaml` | `work.yaml` or a report | no |

## ONE OUTPUT PER ROUTE

Each invocation of `build` writes **exactly one file**,
`<directory of work.yaml>/build/<route output filename>` (or under `--out`),
and touches no other file. Several routes may be built from the same
object, one invocation each; building route B next to route A's output
leaves A's file byte-identical.

| Route (`routes/<id>/route.yaml`) | Output | Ready flag in the frontmatter | Needs a fund profile |
|---|---|---|---|
| `nriis-proposal` | `build/NRIIS_SUBMISSION.md` (`spec/output/nriis-submission.contract.md`, unchanged) | `submittable` — against the bound fund profile only; never "accepted" | yes |
| `academic-article` | `build/ACADEMIC_ARTICLE.md` (`spec/output/academic-article.contract.md`) | `manuscript_ready` — BLOCK = 0; never "accepted" or "publishable" | no |
| `concept-note` | `build/RESEARCH_CONCEPT_NOTE.md` (`spec/output/research-concept-note.contract.md`) | `submittable: false` always, with a HOLD: a concept note enters no system | no |

Every output is a single, self-contained file with a readiness summary at
the top (`BLOCK` / `REVIEW` / `INFO` findings, `NEEDS_INPUT`,
`NEEDS_VERIFICATION`, holds) followed by the researcher's own values in
the route's placement order, ready for copy/paste. **No second
GrantThai-generated file is needed to use a route's output.** Supporting
documents (attachments, figures, data files) are the person's own files:
the output lists which ones are needed and their status, and never
generates them.

- The NRIIS route is what it was: every field grouped by NRIIS tab in the
  observed-form order (tab names and order `NEEDS_VERIFICATION`); a 0.2
  file built with no route gives today's output byte for byte (acceptance
  AT-R1, golden snapshot in `tests/golden/routes/`).
- The article route arranges the researcher's own records into a
  manuscript **overview**. GrantThai never composes section text, never
  reformats citations, and ships no venue registry: every journal fact is
  `NEEDS_VERIFICATION` unless the researcher supplied the venue's own
  document (rule ART010). Both shipped sub-profiles (`thai-journal`,
  `international-journal`) are GrantThai defaults, `NEEDS_VERIFICATION`,
  not venue profiles.
- The concept note, formerly "the one exception" of this contract, is now
  an ordinary route. It is never submittable and never replaces the NRIIS
  route.

### Disclosure lines

The NOTICE constant (`spec/output/notice_constant.txt`) is unchanged and
is line 1 of every route's body. A route may add its own notice line under
it (`route_notice_en` in `route.yaml`; the article route's line says
GrantThai is not affiliated with any journal or publisher). Whether
journals and publishers should join the constant itself is decision K-R6,
open.

## CI guard

`tools/ci/check_one_output.py` asserts, on every run:

1. Every route in `routes/INDEX.yaml` names exactly one template, tagged
   `output_kind: route_output` and `route: <id>` (the NRIIS template keeps
   its `primary_submission` tag and the concept-note template its
   `secondary_optional` tag as accepted aliases, so those templates stay
   byte-identical). No template is claimed by two routes; no template
   tagged for route output is left without a route; at most one template
   is tagged `primary_submission`.
2. Output filenames are unique across routes.
3. Every route's contract (`output.contract`) exists and names this file,
   and this file names every route's contract: `spec/output/nriis-submission.contract.md`,
   `spec/output/academic-article.contract.md`,
   `spec/output/research-concept-note.contract.md`.
4. Runtime, for every shipped example under `examples/`: building each
   route the example declares into an empty directory produces exactly one
   new file with the declared name per build, and every file an earlier
   build wrote in the same directory stays byte-identical. A route with no
   shipped example is reported as not runtime-checked.

Seeded bad fixtures, each of which makes the guard fail:
`tests/fixtures/negative/one_output_dup_filename/` (two routes, one
filename), `one_output_two_templates/` (one route claimed by two
templates), `one_output_orphan_template/` (a `route_output` template no
route names). `tools/ci/check_notice.py` checks every route template for
the NOTICE on body line 1 and, where a route declares `route_notice_en`,
the route notice on line 2.
