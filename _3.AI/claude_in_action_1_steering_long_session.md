# Claude Code in Action

## 1. Steering Long Sessions

### Scope the Work First with Plan Mode

1. Lay out a plan.
2. Read the code without editing it.
3. Create a plan to review.
4. Read the plan carefully.
5. Check if something is off or missing.
6. Ask Claude to add what is needed.

### While Claude Works

#### 1. `Compact`

Summarize the conversation and create a new context window, then check all the information.

- Run `/compact` with instructions on how to summarize.
- **Example:**
  - `/compact Focus on the --version flag implementation`
- `/compact` creates a context window with the main outlines in a summary.
- For more detail, use:
  - `/compact Focus on the API integration in the frontend`

#### 2. Rewind

Load a save. There are two ways to create a checkpoint:

- **Auto-save:** Every time you send a prompt, it saves.
- **Manual:** Use Git.

**Menu options:**

- **Restore code and conversation:** Roll back both together.
- **Restore conversation:** Restore only the chat.
- **Restore code:** Restore the files.
- **Summarize from here:** Summarize everything after the checkpoint until now, when you want to create a side chat.
- **Summarize up to here:** Summarize everything before the checkpoint, when you want to compress a long setup phase but keep the implementation parts intact.

#### 3. Goal

The goal sets a completion condition. Define what "done" means.

> Specific, measurable, and clear.

`/goal All tests in src/billing pass, and the type checker reports zero errors`

**Everything should be based on output.**

To cancel: `/goal clear`

#### 4. Loop

Repeat actions at an interval between turns, either fixed or self-paced.

> Use this when doing something external, such as CI, deployment, or state changes.

**Stop:** Press `Escape` while it waits for the next turn. A loop on a fixed interval keeps running until you ask Claude to cancel it or seven days pass.

#### 5. Run Parallel Work with Worktrees

- The steering metaphor is only one at a time.
- When we have multiple agents on the same codebase, we should use worktrees.
- When a session exits, a clean worktree is automatically removed.
- Location: `root (repo) -> .worktreeinclude`

So, `.worktreeinclude` will create multiple versions of the source tree. We do not need to worry about conflicts because they will be removed after finishing.

All versions will have the same `.gitignore` file, so `.env` will not be pushed.

## Summary

1. Scope the work and steer it.
2. Compact with a summary.
3. Rewind when needed.
4. Set specific goals (identify when it is done).
5. Run parallel work with worktrees.
