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

`permissionDecision` has one of 3 values:

- `allow`
- `deny`
- `ask`
- `defer` (rarely use it for non-interactive -`p` run, pause then resume)

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Don't push to main. Open a pull request instead."
  }
}
```

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
