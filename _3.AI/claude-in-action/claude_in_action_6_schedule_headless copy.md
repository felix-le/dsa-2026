# Scheduled Tasks and Headless Mode

## 1. Cloud Scheduled Tasks

### 1.1 What a Scheduled Task Is

A scheduled task is a saved prompt that runs in the cloud for repeating work.

There are three things:

- A prompt
- The respository (work on)
- Any connectors it needs
- A Trigger(s)

There are some kinds of triggers:

- A cron schedule, like every morning at 9 am
- An HTTP POST to its API endpoint
- A GitHub event like a new pull request.
- OR a Sentry tickets to figure out what's most urgent.

> A prompt + repo + connectors + trigger

### 1.2 How to Create a Scheduled Task

`claude.ai/code/routines` with:

- Name
- What: instruction describing: what Claude should do (pick a respository)
- When: a trigger

OR
`Terminal`

`/schedule daily dependency audit at 9am`

### 1.3 Limits

- Cloud scheduled tasks are research preview: Behavior and limits will keep moving -> change/update all time.
- A recurring schedule runs at most hourly: do not use for more frequent tasks.
- Run start from a fresh clone of your default branch and push to a `claude/` branch, unless your prompt namees another branch.

### 1.4 Example: A PR-Triggered Task

```md
### Step by step

1. **Laura opens a PR**
   Laura creates the branch `fix/readme-name` and changes `README.md`:
   `Project Alpha` → `Project Beta`
   Laura opens PR #7: merge `fix/readme-name` into `main`.

2. **The task starts automatically**
   GitHub reports a new PR, so Claude starts running.

3. **Claude gets the code**
   Because a PR triggered the run, Claude copies the latest commit of `fix/readme-name`, not `main`.
   This way it sees exactly what Laura changed.

4. **Claude does the work**
   It reads the change and finds a typo: `Projetc Beta` → fixes it to `Project Beta`.

5. **Claude pushes the result**
   The prompt does not name a branch, so Claude pushes to a new branch: `claude/fix-typo-readme`.
   Laura's branch is not changed. `main` is not changed.

6. **Humans review**
   If the fix looks good, merge it. If not, ignore it.

### Pushing directly to the PR branch

Add this to the prompt:

> "...and push the fix to the pull request's branch."

Then step 5 pushes straight to `fix/readme-name`.
```

## 2. Headless Mode

### 2.1 When to Use Headless Mode

The docs call non-interactive mode `Headless mode`. Use it when you want to use
your own environment or wrap logic around a Claude run.

core: `-p`

example:
`claude -p "summarize the changes in this diff"`

Notice: `-p` will load same context and an interactive session would, hooks, skills, plugins, MCP servers and also CLAUDE.md. To skip add `--bare`

### 2.2 Getting Structured Output

`structured_output`

`pipe` - output step 1 is input step 2

```bash
claude -p "Extract the exported function names from src/core/style.js" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}}}' \
  | jq '.structured_output.functions'
```

#### 2.2.1 Line by Line

- `claude -p "..."`: run Claude headless with this prompt.
- `--output-format json`: return the result as JSON.
- `--json-schema '...'`: the required shape: an object with a `functions` field that is an array of strings.
- `| jq '.structured_output.functions'`: pull out just the array.

#### 2.2.2 JSON Returned by Claude (Shortened)

```json
{
  "result": "...",
  "session_id": "abc123",
  "structured_output": {
    "functions": ["applyTheme", "getColor", "resetStyles"]
  }
}
```

#### 2.2.3 Output After `jq`

```json
["applyTheme", "getColor", "resetStyles"]
```

A clean array you can hand to a database or another script.

### 2.3 Multi-Step Automation with Sessions

For work with several steps, don't cram everything into one command.
Save the **session ID** from the JSON output and resume the session later.

```bash
claude --resume "$(jq -r .session_id /tmp/plan.json)"
```

#### 2.3.1 Line by Line

- `jq -r .session_id /tmp/plan.json`: read the saved JSON file and get the session ID. `-r` (raw) removes the quotes.
- `$(...)`: run the command inside and insert its result here.
- `claude --resume abc123`: reopen that exact session with full context.

#### 2.3.2 Example Flow

```bash
# Step 1: make a plan and save the JSON
claude -p "Plan how to add dark mode" --output-format json > /tmp/plan.json

# Step 2 (later): resume the session and carry out the plan
claude --resume "$(jq -r .session_id /tmp/plan.json)"
```

One script starts the work. Another script resumes it later with full context.
Useful when the first pass makes a plan and the second pass carries it out.

## 3. Consistent Runs for CI and the Agent SDK

### 3.1 Abbreviations

- **CI** (Continuous Integration): a system that automatically runs tests and builds every time new code is pushed. Example: GitHub Actions.
- **CLI** (Command Line Interface): a program you use by typing commands in the terminal.
- **SDK** (Software Development Kit): a library that lets your own code use a tool.
- **JSON** (JavaScript Object Notation): a data format like `{ "key": "value" }`.
- **API key** (Application Programming Interface key): a secret password that lets a program use a service.
- **MCP** (Model Context Protocol): a way to plug extra tools into Claude.
- **PR** (Pull Request): a request to merge code from one branch into another.

### 3.2 `--bare` for Consistent CI Runs

#### 3.2.1 The Problem

Normally Claude Code automatically loads everything it finds on the machine:

- your personal `~/.claude/CLAUDE.md`
- your hooks and skills
- your plugins and MCP servers

Your laptop has these. The CI machine doesn't, or has different ones.
So **the same command can behave differently on each machine**.
In CI that's bad: when something fails, you can't tell if it's the code or the machine setup.

#### 3.2.2 The Fix

`--bare` skips all auto-loading. Claude starts with only 3 tools:

- Bash
- read files
- edit files

Anything else, you add **on purpose** with flags like `--settings` or `--mcp-config`.

Result: every machine starts from the **exact same setup**, and startup is faster.

#### 3.2.3 Important

Bare mode does NOT use your subscription login. Set an API key first:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

#### 3.2.4 Example: Inside a CI Job

```bash
export ANTHROPIC_API_KEY=$CLAUDE_KEY_FROM_CI_SECRETS

claude --bare -p "Run the tests and list any failures" \
  --settings ./ci/claude-settings.json \
  --output-format json \
  --json-schema '{"type":"object","properties":{"pass":{"type":"boolean"},"failures":{"type":"array","items":{"type":"string"}}}}' \
  | jq '.structured_output'
```

Line by line:

- `export ANTHROPIC_API_KEY=...`: log in with an API key (read from CI secrets, never written in code).
- `--bare`: start clean, load nothing automatically.
- `-p "..."`: run headless with this task.
- `--settings ./ci/claude-settings.json`: add only the settings you chose, stored in the repo.
- `--output-format json` + `--json-schema`: answer must have `pass` (true/false) and a `failures` list.
- `| jq '.structured_output'`: pull out just that answer.

Output:

```json
{ "pass": false, "failures": ["login.test.js: wrong password not rejected"] }
```

The CI pipeline reads `"pass": false` and blocks the merge.

#### 3.2.5 Analogy

An exam room: every student enters with empty hands and gets the same allowed tools.
Nobody brings personal notes, so results are fair and comparable.

### 3.3 Agent SDK: Claude Code Inside Your Own App

#### 3.3.1 What It Is

A library for **TypeScript** or **Python** that puts Claude Code inside your own program.
Same engine as the CLI, but your code calls it instead of you typing.

#### 3.3.2 Main Parts

- `query(...)`: send Claude a task.
- `allowedTools`: limit what Claude can do.
- system prompt: give Claude a role and rules.
- permission mode: how much Claude can do without asking.

Claude **streams** messages back (sends them one by one as it works). Your app handles each one.

#### 3.3.3 Example: Python

```python
from claude_agent_sdk import query, ClaudeAgentOptions

async for message in query(
    prompt="Find and fix the bug in auth.py",
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Edit"],
        system_prompt="You are a careful code reviewer.",
        permission_mode="acceptEdits",
    ),
):
    print(message)
```

Line by line:

- `query(prompt=...)`: the task.
- `allowed_tools=["Read", "Edit"]`: Claude can read and edit files, but can NOT run terminal commands.
- `system_prompt`: Claude's role.
- `permission_mode="acceptEdits"`: edits happen without asking.
- `async for message`: handle each message as it arrives (show it in your UI, save it to a database, etc.).

#### 3.3.4 Real Use Case

You build a web app with a button: "Fix this bug for me."
When a user clicks it, your backend calls the SDK, and Claude does the work behind the scenes.

#### 3.3.5 Analogy

CLI = hiring a worker who comes to your house.
SDK = installing the worker's engine inside your own machine, so your machine controls it.

## 4. Which One Should I Use?

Think of it as a ladder, from easiest to most control:

| Option               | Who runs the machine | How much control | Effort  |
| -------------------- | -------------------- | ---------------- | ------- |
| Cloud scheduled task | Anthropic            | Low              | Easiest |
| Headless mode (`-p`) | You                  | Medium           | Easy    |
| `--bare`             | You (CI)             | High             | Medium  |
| Agent SDK            | You (your app)       | Highest          | Hardest |

Ask these questions in order:

1. **Is it repeat work that doesn't need my own system?**
   → Cloud scheduled task (runs on Anthropic's servers, nothing to host)
2. **Does it need to be part of my script or pipeline, passing data along?**
   → Headless mode (`-p`)
3. **Is it in CI, and must it behave the same on every machine?**
   → `--bare` (plus `-p`)
4. **Does it need to live inside my own product?**
   → Agent SDK

### 4.1 Quick Examples

| Task                                                                | Best choice                 |
| ------------------------------------------------------------------- | --------------------------- |
| Every morning, summarize new PRs                                    | Cloud scheduled task        |
| A script that lists exported functions and saves them to a database | Headless `-p` + JSON schema |
| GitHub Actions reviews every PR the same way                        | `--bare` + `-p`             |
| A "Fix with AI" button in your web app                              | Agent SDK                   |

**Rule:** start with cloud scheduled tasks. Go down the ladder only when the job needs more control.

## 5. Remember

- CI needs **sameness**: use `--bare` and an API key.
- Your own product: use the **Agent SDK**.
- Pick the **simplest option that still does the job**. Each step down costs more setup and maintenance.
