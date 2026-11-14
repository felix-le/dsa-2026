# Verifying Unsupervised Runs

## 1. The Big Idea

Claude ran a task unsupervised and said "Done!" Before using the result, you
must verify what it actually did.

> The less you watched -> the more you verify.

## 2. Choose a Safe Permission Mode

- Auto mode: a classifier check most action for danger before they run - Only for dangerous NOT for is this code correct?
- Bypass permission: no checks at all.

## 3. Start with the Diff, Not the Summary

- Summary = what Claude says it did.
- Diff = What Claude actually changed, line by line.

```bash
git diff --stat:
  src/components/LoginButton.tsx   | 2 +-
  src/config/database.ts           | 5 +++--    <- Why is this here?!
  tests/login.test.ts              | 3 +--      <- Why did tests change?!

```

### 3.1 How to Check

1. Run /code-review: Claude walks through the changes and flags issues
2. Run git diff: read it with your own eyes
3. Read the files in the plan first
4. The look for anything outside the plan

## 4. Turn Tests into a Gate, Not a Promise

- Promise: Claude says tests passed -> need to check again as it migh weakened a test
- Gate = Code forces the tests to run -> Claude can't skip (with hooks)

### 4.1 Stop Hook: Run Tests Before Claude Stops

Use this when Claude wants to end its turn even the test fail/ refuses

`.claude/settings.json:`

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": ".claude/hooks/run-tests.sh" }
        ]
      }
    ]
  }
}
```

`.claude/hooks/run-tests.sh:`

```bash
#!/bin/bash
# Run the tests. If they fail, block Claude from stopping.
if ! npm test > /tmp/test-output.txt 2>&1; then
  echo "Tests failed. Fix them before finishing:" >&2
  tail -n 20 /tmp/test-output.txt >&2
  exit 2   # exit 2 = block, and send this message back to Claude
fi
exit 0     # exit 0 = tests passed, Claude may stop
```

### 4.2 PostToolUse Hook: Check After Editing

`.claude/settings.json:`

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/lint-and-typecheck.sh"
          }
        ]
      }
    ]
  }
}
```

`.claude/hooks/lint-and-typecheck.sh:`

```bash
#!/bin/bash
# After each edit, check code style and types.
if ! npx eslint . > /tmp/lint.txt 2>&1; then
  echo "Lint errors found:" >&2
  cat /tmp/lint.txt >&2
  exit 2
fi
if ! npx tsc --noEmit > /tmp/types.txt 2>&1; then
  echo "Type errors found:" >&2
  cat /tmp/types.txt >&2
  exit 2
fi
exit 0
```

### 4.3 Exit Codes

- 0 OK, continue
- 2 Block and send the error message to Claude
- 1 NOT blocking, just logged. Common mistake

### 4.4 Full Verification Flow

```md
1. Claude edits login.ts
2. PostToolUse hook -> type check fails -> exit 2
3. Claude reads "Type error on line 12" -> fixes it
4. Claude says "I'm done"
5. Stop hook -> runs tests -> 1 test fails -> exit 2
6. Claude reads the failure -> fixes the code
7. Claude says "I'm done" again
8. Stop hook -> all tests pass -> exit 0
9. Claude really stops
```

## 5. Get a Cold Second Opinion

Cold here means no memory of how the code was built.

Session A (wrote the code):
"I skipped input validation because the frontend already checks it."

Session B (fresh, no memory), reviewing the diff:
"The API accepts user input with no validation.
Anyone can call this endpoint directly and skip the frontend.
This is a security risk."

-> Conclusion: you need to use 2 different agents to write and check.

## 6. Verify Headless Runs by JSON Result and Exit Code

For headless runs (claude `-p`), don’t read prose. Check the exit code and the JSON result.

```bash
claude -p "Fix the failing tests in src/billing" \
  --output-format json > result.json

# 1. Did the command itself succeed?
if [ $? -ne 0 ]; then
  echo "Claude run failed"
  exit 1
fi

# 2. Did the run end with an error?
if [ "$(jq -r .is_error result.json)" = "true" ]; then
  echo "Claude reported an error"
  exit 1
fi
# 3. Don't trust the words. Run the tests yourself.
npm test

```

Verify by your own tests, not Claude's words.

## 7. Putting It Together

Make the verification as serious as the unsupervised run was:

| Step | What to do                                | Why                                     |
| ---- | ----------------------------------------- | --------------------------------------- |
| 1    | Read the diff yourself                    | The summary can hide surprises.         |
| 2    | Turn tests into a Stop hook gate          | Claude cannot skip or fake tests.       |
| 3    | Check headless runs by JSON and exit code | Machines read data, not prose.          |
| 4    | Get a cold second opinion                 | Fresh eyes catch rationalized mistakes. |
| 5    | Test by your test cases                   | make suere it work                      |
