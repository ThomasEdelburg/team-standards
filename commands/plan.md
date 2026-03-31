# /plan - Planning Phase

Execute the full planning phase for the current or specified task.

**Trigger words:** "plane", "neue task", "was muessen wir tun", "lass uns planen", "plan", "new task", "what do we need to do", "let's plan"

## Workflow

1. Read `~/.claude/memory/standards.md`, `~/.claude/memory/workflow.md`, `~/.claude/memory/checklists.md`
2. Read the current `TODO.md` in the project directory (if present)
3. Execute the 11 planning points (from CLAUDE.md)
4. Auto-generate acceptance criteria for the task
5. Create or update the task entry in `TODO.md`
6. Wait for explicit user approval ("lege los" / "let's go" / "start implementing") before starting to code

## Task Format in TODO.md

```
## Task #XXXX: [Title]
**Status:** open
**Acceptance Criteria:**
- [ ] [Functional criteria - derived from description]
- [ ] Tests >= 90% Coverage
- [ ] Migration/Patch present and tested
- [ ] Code review passed
- [ ] Documentation updated
- [ ] Performance goals met
```

## Context Check
Evaluate whether the context is sufficient / incomplete / unclear.
If incomplete: ask targeted questions before planning.
