# Verification Skill

## 1. What a Verification Skill Does

A verification skill:

- Runs the test suite.
- Reads the diff.
- Checks that no test was weakened just to make things pass.
- Reports pass or fail with the evidence attached.

## 2. Two Parts of a Skill

A skill has two parts:

### Description

The description acts like a conditional state. When the context matches, the skill runs.

Example: `Use after any refactor or code change to verify it.`

### Procedure

The procedure contains fixed steps. The output from teammates follows the same structure.

## 3. Verification Principles

### A Green Test Is Not Enough

Sometimes Claude changes the condition instead of fixing the code, and the test still passes.

**Original:**

```js
expect(total).toBe(150);
```

**AI changed:**

```js
expect(total).toBeGreaterThan(0);
```

### Define What "Done" Means

Verification must be specific:

> Run 42 tests, 42 pass, the type check reports 0 errors, and the tests were not changed.

## 4. Skill Folder Structure

A skill folder has one entry point and two supporting resources:

```text
pre-commit-check/
├── SKILL.md             # entry point, always read first
├── reference.md         # detailed guide, read when SKILL.md says so
└── scripts/
    └── check.sh         # executable check, run when SKILL.md says so
```

### Example: How the Skill Works

The purpose of this skill is to prevent `console.log` from being left in `src/` before a commit.

`SKILL.md` controls the order:

````md
---
name: verify-pre-commit
description: Use before a commit to check that no console.log remains in src/.
---

1. Read `reference.md`.
2. Run `scripts/check.sh`.
3. If the check fails, fix the code and run it again.
4. Run the test suite.
5. Read the diff and check that no test was weakened.
6. Report pass or fail with evidence.

```

```
````

`reference.md` explains the rule:

```md
Do not use `console.log` in `src/`.
Use the application logger instead.
```

`scripts/check.sh` enforces the rule:

```bash
#!/usr/bin/env bash
set -euo pipefail

if grep -Rn "console.log" src/; then
    echo "FAIL"
    exit 1
else
    echo "PASS"
fi
```

### Before and After

Before — `src/login.js`:

```js
console.log(user.password);
```

```text
$ bash scripts/check.sh
src/login.js:5:console.log(user.password);
FAIL
```

After — the same file, `src/login.js`:

```js
logger.info("user logged in");
```

```text
$ bash scripts/check.sh
PASS
```

**Conclusion:** The `console.log` line was removed and replaced with `logger.info`; the check now passes.

## 5. Which Instruction Surface Owns Each Rule?

- **`CLAUDE.md`:** Rules for everywhere, such as naming and where to store files.
- **`SKILL.md`:** Procedures and introductory material for a specific type of work.
- **Hook:** Hard rules that Claude must always follow.

### Rule Strength

- **Introduction and steps:** `CLAUDE.md` for all work + skill files for a specific job. Claude usually follows these rules, but they are not hard enforcement.
- **Hook:** Must be followed.

## 6. Recommended First Skill

A skill is a reusable component. The first skill should be a check or verification skill.
