# Permission Modes

Claude Code has six permission modes:

1. **Manual**: Reads are allowed. Claude asks first for everything else.
2. **Accept edits**: Reads, file edits, and common file system bash commands run without asking. Use this mode to review the changes after they happen.
3. **Plan**: Claude researches and proposes changes without editing anything.
4. **Auto**: Accepts everything. A separate classifier model reviews most actions before they run.
5. **Don't ask**: Allows file reads inside your working directories and pre-approved tools.
6. **Bypass permissions**: Skips all checks. Only run it inside an isolated container or virtual machine.

## Switching Modes

Press `Shift+Tab` to cycle through the visible modes:

`Manual > Accept edits > Plan > Auto`

## Hidden Modes

### Don't Ask

Set it at startup or in `settings.json`:

```bash
claude --permission-mode dontAsk
```

```json
{ "permissions": { "defaultMode": "dontAsk" } }
```

### Bypass Permissions

```bash
claude --dangerously-skip-permissions
```

## Auto Mode in Detail

Auto mode is for hands-off work. Claude can work independently, but guardrails stop it from doing the following:

- Deploying to production or running database migrations
- Force pushing, or piping downloaded code straight into a shell
- Sending sensitive data (such as `.env` files or tokens) to external endpoints
- Irreversibly deleting files that existed before the session

It suits:

- CI pipelines
- Scheduled jobs
- Overnight batches

### Key Takeaway

The guardrails let Claude finish tasks that can be restored, but block actions that are hard or impossible to undo, such as database changes.

The classifier checks the **intent** of an action, not the exact code. So add a **stop hook** that runs after Claude finishes to verify the result.
