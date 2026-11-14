# Hooks

Claude > Read hook > do something
-> It will never do over rules from hooks
There are some hooks we need to know:

1. PreToolUse: fires before a tool call.
2. PostToolUse: fires after a successful tool call (auto-formatting)
3. Stop fires when Claude wants to end its turn. Combine with SubagentStop when a sub-agent finishes. Use it to make sure job is DONE BY OUR Difination.
4. PreCompact and Post compact: fire before and after compaction.
5. InstructionsLoaded fires when a CLAUDE.md or rule file loads. Put Claude into a context.
6. SessinStart: fires at the start and primes the environment. Use `startup` source if you only want it on fresh starts.

## 1. PreToolUse: returning a decision as JSON

It can stop/block a tool call before it runs.

`permissionDecision` has three common values:

- `allow`
- `deny`
- `ask`
- `defer` (rarely use it for non-interactive -`p` run, pause then resume)

### One Context, Three Decisions

**Context:** Claude wants to run:

```bash
git push origin main
```

The hook can return three different decisions:

**1. Allow — run the command immediately**

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow"
  }
}
```

**2. Ask — pause and ask the user first**

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "ask",
    "permissionDecisionReason": "Confirm before pushing to main."
  }
}
```

**3. Deny — block the command**

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Don't push to main. Open a pull request instead."
  }
}
```

The same command is used in all three cases; only the hook's decision changes.

`allow` or `ask` with `updatedInput`

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "ask",
    "updatedInput": {
      "command": "..."
    }
  }
}
```

IMPORTANT: There are some notices:

1. **redact a secret and still let it run**
   Instead of denying whole command, hook will replace the command
   Example: replace key by REDACTED:
   Original:

```bash
curl -H "Authorization: sk_live_abc123" https://api.stripe.com/...
```

Hook Replace:

```bash
curl -H "Authorization: REDACTED" https://api.stripe.com/...
```

2. `updatedInput`

original data:

```json
{
  "command": "curl -H 'Authorization: sk_live_abc123' ...",
  "description": "Call Stripe API",
  "timeout": 60000
}
```

> `updatedInput` edits all object

So, we need to combine all edit parts also others

Wrong: -> lose timeout and description

```json
"updatedInput": {
  "command": "curl -H 'Authorization: REDACTED' ..."
}
```

RIGHT:

```json
"updatedInput": {
  "command": "curl -H 'Authorization: REDACTED' ...",
  "description": "Call Stripe API",
  "timeout": 60000
}
```

-> Script to run:

```bash
updatedInput: (.tool_input | .command |= gsub("sk_live_\\w+"; "REDACTED"))
```

## Exit codes, for hooks that don't return JSON

The hook's exit code controls what happens to the tool call:

| Exit code | Hook result | Does `git push origin main` run? |
|---|---|---|
| `0` | Success | Yes |
| `2` | Blocking error | No |
| Any other code, such as `1` | Non-blocking error | Yes |

For most hook events, plain text written to `stdout` is ignored. Error text
written to `stderr` is sent back to Claude for exit code `2`; for other
non-zero codes, it is logged and Claude continues. `SessionStart`,
`UserPromptSubmit`, and `UserPromptExpansion` can use plain text as context.

### One Simple Example

**One context:** Claude wants to run:

```bash
git push origin main
```

The following are three alternative versions of the same file:
`.claude/hooks/pre-tool-use.sh`.

The filename is not fixed; the hook configuration defines the path. Only one
case would be used in the file at a time.

**Case 1: Allow the command**

```bash
# .claude/hooks/pre-tool-use.sh
if [[ "$COMMAND" == "git push origin main" ]]; then
    echo "Command allowed."
    exit 0  # Success: Claude continues.
fi
```

Hook output:

```text
Command allowed.
```

Result: Claude continues, so the push runs and can reach `main`.

**Case 2: Block the command**

```bash
# .claude/hooks/pre-tool-use.sh
if [[ "$COMMAND" == "git push origin main" ]]; then
    echo "Blocked: open a pull request instead." >&2
    exit 2  # Blocking error: Claude stops.
fi
```

Hook output:

```text
Blocked: open a pull request instead.
```

Result: Claude stops, so the push does not run.

**Case 3: Report a non-blocking error**

```bash
# .claude/hooks/pre-tool-use.sh
if [[ "$COMMAND" == "git push origin main" ]]; then
    echo "Warning: the branch was not checked." >&2
    exit 1  # Non-blocking error: Claude continues.
fi
```

Hook output:

```text
Warning: the branch was not checked.
```

Result: Claude continues, so the push can still run and reach `main`.

### A real guardrail: readact instead of block

We have a hook PreToolUse for Bash. we will:

1. Register the file in setting with path `.claude/settings.json` -> push it to our team:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(curl *)", // field on the hook can narrow it to a specific command
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/redact-secrets.sh" // run this command
          }
        ]
      }
    ]
  }
}
```

- matcher: Bash (environment) / tool
- This will deny by default but we have `command` run in `.claude/hooks/redact-secrets.sh` to fix by replacing secret:

`.claude/hooks/redact-secrets.sh` content:

```bash
jq 'if (.tool_input.command // "" | test("sk_live_\\w+")) then {
  hookSpecificOutput: {
    hookEventName: "PreToolUse",
    permissionDecision: "ask",
    permissionDecisionReason: "Replaced a live key with a placeholder",
    updatedInput: (.tool_input | .command |= gsub("sk_live_\\w+"; "REDACTED"))
  }
} else empty end'
```

exmplain:
.tool*input.command // "": get command Claude wanna run or "" for no showing err
test("sk_live*\\w+"): check the format command `sk_live_`
permissionDecision: "ask" -> ask before running
permissionDecisionReason: reason to show this
updatedInput: keep all command `tool_input` bur replace `key` by `REDACTED`

> Notice: we might need to install `jq` (JSON request)
>
> ```bashbrew install jq        # Mac
> sudo apt install jq    # Ubuntu/Linux
> ```
>
> and provide permission by `chmod +x`
>
> ```
> `chmod +x .claude/hooks/redact-secrets.sh`
> ```

### Preserving state across a compact

this hook for combining `SessionStart` with matcher `compact` run after compress:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [{ "type": "command", "command": "git status --short" }]
      }
    ]
  }
}
```

example:

```bash
M  src/api/payment.ts
M  src/components/Checkout.tsx
?? src/utils/currency.ts
```
