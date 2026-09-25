# Using GrantThai with an AI assistant

Thai version: [`docs/th/use-with-ai.th.md`](th/use-with-ai.th.md).

GrantThai works without any AI. This page is for researchers who want an
AI assistant to interview them and prepare the one input file
(`work.yaml`; an older `project.yaml` still works unchanged) and exactly
one overview file per **output route you choose**:
`build/NRIIS_SUBMISSION.md` (a research proposal to enter into NRIIS by
hand), `build/ACADEMIC_ARTICLE.md` (a manuscript overview) or
`build/RESEARCH_CONCEPT_NOTE.md` (a concept note). Since v0.3 entering
NRIIS is one route of the router, no longer the core.

Whichever AI you use, the rules do not change:

- **Your information is the source.** What you say is recorded as yours.
  Anything the AI writes is recorded as an AI draft (`ai_draft`,
  `INFERENCE`) that you must confirm. An AI draft can never be marked as
  a source; the engine refuses it.
- **The AI does not validate your knowledge.** GrantThai's checks test
  structure and links only.
- **No invented Thai or journal facts.** Fund rules, deadlines, rates,
  eligibility, NRIIS labels and tab order come from your current call
  document; a journal's scope, indexing, word limits, fees and review
  time come from the venue's own current author guidelines that you
  supply. Otherwise they stay `NEEDS_VERIFICATION`.
- **You choose the route; the AI never does.** The AI lists the routes
  and asks. When nothing you declared decides the route, GrantThai stops
  and lists the candidates instead of guessing.
- **Nothing goes above `DRAFT`, and nothing is submitted.** You copy the
  output into NRIIS, or send the manuscript to the journal, yourself.

GrantThai is unofficial; see [`NOTICE`](../NOTICE).

## What the AI uses

| Piece | Where | What it is |
|---|---|---|
| The skill | `skills/grantthai/` | `SKILL.md` (instructions any AI can follow; step 0 is "ask which route"), `reference/` (routes, interview questions for the proposal and the article track, provenance rules, Thai rule explanations, answers-file format, prompt packet), `scripts/grantthai_skill.py` (helper) |
| The engine | `src/grantthai/` | `grantthai` command and Python API (`grantthai.api_py`): `init`, `set`, `validate`, `explain`, `build --route`, `fields --route`, `route list|check|build`, `migrate` |
| Prompt packet | `skills/grantthai/reference/PROMPT_PACKET.md` | one message to paste into a chat-only AI that cannot run programs (proposal variant, plus an article variant) |

The MCP server and HTTP API are other thin wrappers over the same Python
API. They follow the same rules and produce the same one file.

## Step 1: install the engine (for any AI that can run commands)

Python 3.10 or newer. From a GrantThai checkout:

```bash
pip install -e .
grantthai --version
```

Use the editable install (`-e`): in v0.1 the engine reads `spec/`,
`registry/`, `templates/` and the other data folders from the checkout.
If you install another way, set `GRANTTHAI_HOME` to the checkout folder.
Nothing is downloaded while GrantThai runs.

## Step 2: give the skill to your AI

### Claude Code

Copy the skill folder into your skills folder (for yourself), or into the
project you are working in (for that project only):

```bash
cp -r skills/grantthai ~/.claude/skills/grantthai          # personal
cp -r skills/grantthai .claude/skills/grantthai            # one project
```

Start a session in your work folder and ask, for example,
"ช่วยเตรียมข้อเสนอโครงการสำหรับ NRIIS ด้วย GrantThai" or
"ช่วยเตรียมภาพรวมต้นฉบับบทความวิชาการด้วย GrantThai". The skill loads from
its description. You can also place the folder inside a plugin's `skills/`
directory if you distribute skills as a plugin.

### Codex CLI and other agents that read `AGENTS.md`

Put the skill folder next to your proposal and add an `AGENTS.md` to that
folder:

```markdown
# AGENTS.md
When I ask for help with a research proposal, NRIIS or GrantThai, read
skills/grantthai/SKILL.md and follow it exactly, including every file it
points to under skills/grantthai/reference/.
```

If your version supports a skills folder, you can copy
`skills/grantthai` there instead.

### Gemini CLI

Same as above, with a `GEMINI.md` file in your proposal folder containing
the same instruction.

### ChatGPT, Gemini or Claude in a web or desktop chat

- **Projects, custom assistants, or similar features with instructions and
  files:** upload `SKILL.md` and the files in `reference/`, and use the
  instruction "Follow SKILL.md". The assistant can only run the GrantThai
  checks if it can run Python with GrantThai available; otherwise it
  should follow the prompt-packet route below.
- **Plain chat:** paste the text between the `=====` lines of
  `reference/PROMPT_PACKET.md` as your first message.

### Local models and any other AI

- If the AI can run shell commands: give it `SKILL.md` as its instructions
  (system prompt) and let it run `grantthai` and
  `skills/grantthai/scripts/grantthai_skill.py`.
- If it cannot: use `reference/PROMPT_PACKET.md`, save the YAML it gives
  you as `project.yaml`, and run `grantthai build project.yaml` yourself.

## Step 3: what a session looks like

0. The AI lists the output routes (`grantthai route list`) and asks which
   one you want now: NRIIS proposal, academic article or concept note. It
   records your answer (`--route`, or `project.route` in its answers
   file); it never picks one. You can ask for a second route from the same
   file later.
1. The AI checks the engine (`python skills/grantthai/scripts/grantthai_skill.py check`)
   and creates `work.yaml` (`grantthai init work.yaml --work-type ...`).
2. Before asking for any data it shows you the data warning
   (`grantthai_skill.py warning`): do not give a public AI personal data
   that identifies anyone, participants' records, confidential,
   unpublished or pre-patent material, or dual-use information; enter team
   members' names yourself. It records its own name and version for your
   AI Use Declaration (`docs/policy/ai-use-ceiling.md`).
3. It asks for your call document (proposal route) or the venue's author
   guidelines (article route), then interviews you topic by topic
   (`reference/interview.md`, or `reference/interview-article.md` for an
   article), asking where each factual claim comes from. On the article
   route your results stay yours: the AI arranges, it never writes them.
4. It writes your answers with `grantthai_skill.py apply answers.yaml`
   (or `grantthai set ...`), marking its own drafts as AI drafts.
5. It runs `grantthai_skill.py report --route ID`: route-scoped
   validation, a plain-Thai explanation of every BLOCK and REVIEW finding,
   the list of AI-drafted fields you still need to confirm, and the build.
6. It hands you that route's one file (`build/NRIIS_SUBMISSION.md`,
   `build/ACADEMIC_ARTICLE.md` or `build/RESEARCH_CONCEPT_NOTE.md`) and
   your `work.yaml`. For an article, `manuscript_ready` means only that no
   BLOCK is open, never accepted or publishable.

For a conceptual, theory, philosophical, legal, review, formal, SoK or
policy article the AI may also show you the 7SSA structure profiles
(`grantthai route profiles work.yaml`: seven English sections, or seven,
five or four Thai sections) and ask which one you want; it never picks one.
With a profile it interviews you sector by sector
(`reference/interview-7ssa.md`, in the suggested writing order 5 -> 4 -> 3
-> 6 -> 2 -> 1 -> 7). Every sector is your own text; merging sections never
drops a sector (each keeps its `[S#]` marker).

Read the output's readiness summary and the "AI-drafted values (the
researcher must confirm)" section before you use anything in it. Then read
section 4.7, the AI Use Declaration (a GrantThai appendix, not an NRIIS
field). If it is true and complete, set `declaration_confirmed_by_human:
true` in `project.yaml` yourself; the AI never sets it.

## Commands you can run yourself at any time

```bash
grantthai route list                                   # the output routes
grantthai route check --route academic-article work.yaml   # report for one route
grantthai validate work.yaml --route nriis-proposal    # exit code 1 when there is any BLOCK finding
grantthai explain B002                                 # what a rule means
grantthai build work.yaml --route nriis-proposal       # writes build/NRIIS_SUBMISSION.md
grantthai build work.yaml --route academic-article     # writes build/ACADEMIC_ARTICLE.md
grantthai fields --required --route academic-article   # the article route's fields, in placement order
grantthai route profiles work.yaml                     # 7SSA structure profiles and the candidates (you choose)
grantthai build work.yaml --structure-profile 7ssa-thai-5   # the article body in five Thai sections
grantthai build work.yaml --format tex                 # build/ACADEMIC_ARTICLE.tex instead (needs a 7SSA profile)
grantthai migrate project.yaml --dry-run               # what upgrading to work.yaml would make stale
```

An older `project.yaml` builds exactly as before: `grantthai build
project.yaml` still writes `build/NRIIS_SUBMISSION.md`, byte for byte.

## Limits

- Only one fund profile ships: `example/FICTIONAL_CALL@0.1`, a fictional
  test profile. Ceiling and eligibility checks against it are not checks
  against a real fund.
- Rules B003, B004 and F004 are not evaluated yet; the report says so in
  an INFO line. Check those points against your call document.
- The fund-rule freshness check (F002) depends on the date; the same file
  on a different day can give a different result.
- The article route's sub-profiles (`thai-journal`, `international-journal`)
  are GrantThai defaults, not journal profiles; everything in them is
  `NEEDS_VERIFICATION` until you supply a named venue's author guidelines.
