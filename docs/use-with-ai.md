# Using GrantThai with an AI assistant

Thai version: [`docs/th/use-with-ai.th.md`](th/use-with-ai.th.md).

GrantThai works without any AI. This page is for researchers who want an
AI assistant to interview them and prepare the one input file,
`project.yaml`, and the one overview file, `build/NRIIS_SUBMISSION.md`.

Whichever AI you use, the rules do not change:

- **Your information is the source.** What you say is recorded as yours.
  Anything the AI writes is recorded as an AI draft (`ai_draft`,
  `INFERENCE`) that you must confirm. An AI draft can never be marked as
  a source; the engine refuses it.
- **The AI does not validate your knowledge.** GrantThai's checks test
  structure and links only.
- **No invented Thai facts.** Fund rules, deadlines, rates, eligibility,
  NRIIS labels and tab order come from your current call document, or
  stay `NEEDS_VERIFICATION`.
- **Nothing goes above `DRAFT`, and nothing is submitted.** You copy the
  output into NRIIS yourself.

GrantThai is unofficial; see [`NOTICE`](../NOTICE).

## What the AI uses

| Piece | Where | What it is |
|---|---|---|
| The skill | `skills/grantthai/` | `SKILL.md` (instructions any AI can follow), `reference/` (interview questions, provenance rules, Thai rule explanations, answers-file format, prompt packet), `scripts/grantthai_skill.py` (helper) |
| The engine | `src/grantthai/` | `grantthai` command and Python API (`grantthai.api_py`): `init`, `set`, `validate`, `explain`, `build`, `fields` |
| Prompt packet | `skills/grantthai/reference/PROMPT_PACKET.md` | one message to paste into a chat-only AI that cannot run programs |

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

Start a session in your proposal folder and ask, for example,
"ช่วยเตรียมข้อเสนอโครงการสำหรับ NRIIS ด้วย GrantThai". The skill loads from
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

1. The AI checks the engine (`python skills/grantthai/scripts/grantthai_skill.py check`)
   and creates `project.yaml` (`grantthai init project.yaml`).
2. It asks for your call document, then interviews you topic by topic
   (`reference/interview.md`), asking where each factual claim comes from.
3. It writes your answers with `grantthai_skill.py apply answers.yaml`
   (or `grantthai set ...`), marking its own drafts as AI drafts.
4. It runs `grantthai_skill.py report`: validation, a plain-Thai
   explanation of every BLOCK and REVIEW finding, the list of AI-drafted
   fields you still need to confirm, and the build.
5. It hands you `build/NRIIS_SUBMISSION.md` (the only output) and your
   `project.yaml`.

Read the output's readiness summary and the "AI-drafted values (the
researcher must confirm)" section before you use anything in it.

## Commands you can run yourself at any time

```bash
grantthai validate project.yaml            # exit code 1 when there is any BLOCK finding
grantthai explain B002                     # what a rule means
grantthai build project.yaml               # writes build/NRIIS_SUBMISSION.md
grantthai fields --required                # every required field, in NRIIS entry order
```

## Limits of v0.1

- Only one fund profile ships: `example/FICTIONAL_CALL@0.1`, a fictional
  test profile. Ceiling and eligibility checks against it are not checks
  against a real fund.
- Rules B003, B004 and F004 are not evaluated yet; the report says so in
  an INFO line. Check those points against your call document.
- The fund-rule freshness check (F002) depends on the date; the same file
  on a different day can give a different result.
