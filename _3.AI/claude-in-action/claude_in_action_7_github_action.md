# GitHub Actions and Code Review

## 1. Code Review with the Claude GitHub App

The Claude GitHub app reviews pull requests.

> Organization enables from Claude Code admin settings - allow code review at the setup
> Decid:
>
> - repo
> - when

### 1.1 When a Review Runs

After the app is installed and linked, contributors can choose:

- Once when a PR opens
- One every push to the PR
- Only when someone comments @claude review.

-> Clear explanation + suggested fix.

it deduplicates and ranks the findings -> We have a handful of real issues worth your attention.

### 1.2 What Code Review Does and Does Not Do

- never approves or blocks the PR -> flag > You decide
- No pushing fixes, posts findings only
- Available on Team and Enterprise plans.

Your turn: Fix the code and push.

## 2. The Do-It-Yourself Path: GitHub Actions

### 2.1 Workflow 1: Review When Someone Mentions `@claude`

```yaml
# File: .github/workflows/claude.yaml
name: Claude Code # Workflow name shown in the Actions tab

on: # Events that start this workflow
  issue_comment: # A comment on an issue or on a PR conversation
    types: [created] # Only new comments, not edited or deleted ones
  pull_request_review_comment: # A comment on a specific line of code in a PR
    types: [created]

jobs:
  claude: # Job name
    if: contains(github.event.comment.body, '@claude') # Run only if the comment contains "@claude"
    runs-on: ubuntu-latest # GitHub lends a fresh Linux machine

    permissions: # What this job is allowed to do
      contents: write # Push commits
      pull-requests: write # Comment on PRs
      issues: write # Comment on issues
      id-token: write # Sign in as the Claude GitHub app
      actions: read # Read results of other workflow runs

    steps: # Steps run in order
      - uses: actions/checkout@v6 # Step 1: download the repo code
        with:
          fetch-depth: 1 # Only the latest commit, which is faster

      - uses: anthropics/claude-code-action@v1 # Step 2: run Claude
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }} # Key read from the repo secrets
          claude_args: "--max-turns 5 --model claude-sonnet-5" # Max 5 steps, use the Sonnet model
          # No "prompt" here, so Claude waits until someone writes "@claude"
```

### 2.2 Workflow 2: Generate a Daily Report

```yaml
# File: .github/workflows/daily-report.yaml
name: Daily report # Workflow name shown in the Actions tab

on:
  schedule: # Run on a timer
    - cron: "0 9 * * *" # minute=0 hour=9 every day → 9:00 UTC (4:00 AM Toronto in winter)
  workflow_dispatch: # Adds a "Run workflow" button to start it by hand

jobs:
  report:
    runs-on: ubuntu-latest # Fresh Linux machine

    permissions: # Read only, cannot change anything
      contents: read # Read code and commits
      issues: read # Read issues
      id-token: write # Sign in as the Claude GitHub app

    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}

          # Has a "prompt", so Claude runs right away without waiting for "@claude"
          prompt: "Generate a summary of yesterday's commits and open issues"

          # "|" lets you write the value on several lines
          # Claude may only list commits and list issues, nothing else
          # Do NOT put "#" comments inside this block
          claude_args: |
            --allowedTools "mcp__github__list_commits,mcp__github__list_issues"

# Note: this run does NOT post a comment. Read the report in the run log:
# Actions tab → click this run.
```
