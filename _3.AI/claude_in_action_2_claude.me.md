# A `CLAUDE.md` That Follows

## 1. `CLAUDE.md` Rules

There are two types of rules: guidance and hard rules that must never be crossed.

You can write a rule such as "Never push to main" in `CLAUDE.md`, but sometimes Claude may still do it. Therefore, you need a hard rule.

**Hooks** belong in a `PreToolUse` hook. Claude reads the hook before letting an action proceed, and it can block actions that we want to stop.

## 2. Locations

- **Managed policy:** Organization-level rules shared across teams.
- **User:** Personal preferences shared across projects.
- **Project:** Rules shared with the team and checked into the repository.
- **Local:** Rules ignored by Git and used for personal notes in one repository only.

> `Managed policy > Local > Project > User`

```text
Question: Which package manager should Claude use?

Managed: Only use npm.
Local: Use pnpm. // CLAUDE.local.md in your repo; do not push to GitHub. It is only for this repo.
Project: Use yarn.
User: Use bun. // ~/.claude/CLAUDE.md on your computer for all projects.

Who wins?

Managed → Claude uses npm. Local, Project, and User are all overridden.
```

## 3. Split Up a Big File with Imports

Organize a large file with imports:

```text
@.claude/conventions/code-style.md
@.claude/conventions/testing.md
@.claude/conventions/workflow.md
```

## 4. Phrasing

- Be specific and checkable.

  > `Put new API routes in src/api/handlers, one per file`

- Name the replacement.

  > `Use named exports, not default exports.`

- Word it plainly instead of shouting.

  > `Rule can't bend -> make it a hook. Claude gets lost -> make the file shorter.`

- Keep the file under revision.

  > `Update CLAUDE.md every time you have issues -> let Claude fix it.`

> Move hard rules to hooks, where they're actually enforced.  
> Organize long files with imports (just remember they don't reduce context).  
> Make every rule specific and checkable, and name the replacement.  
> Word rules plainly instead of adding emphasis.  
> Keep revising the file whenever Claude gets something wrong.
