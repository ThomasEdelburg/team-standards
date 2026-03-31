# /review - Code Review

Executes the full code review before a commit.
Outputs the assessment as a compact table.

**Trigger words:** "review", "pruef den code", "ist der code ok", "check the code", "is the code ok"

## Workflow

1. Identify changed files (git diff)
2. Go through the review checklist from `~/.claude/memory/checklists.md`
3. Fix minor violations directly (without asking)
4. Present architecture decisions / breaking changes to user
5. Check cleanup checklist (for complex changes)
6. Invoke /test - all tests must be green
7. Invoke /reflect (for complex sessions or when corrections were needed)
8. Output result

## Output Format

```
## Code Review - [Branch/Task]

| Check Point              | Status | Action         |
|--------------------------|--------|----------------|
| File size                | pass   | -              |
| Circular imports         | pass   | -              |
| ...                      | ...    | ...            |

**Auto-fixed:** [List of auto-fixes]
**For user:** [List of decisions the user must make]
**Tests:** pass / fail
**Coverage:** XX%

-> Ready for commit: YES / NO
```

## Commit Gate
Only when all checks pass and Coverage >= 90%:
Create Conventional Commit (feat: / fix: / BREAKING CHANGE:)

---

## Micro-Loop (for each step)
Scan (what exists?) -> Plan (what exactly?) -> Act -> Reflect (does it work? if not: stop + report)
