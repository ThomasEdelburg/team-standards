# /reflect - Session Analysis & Standards Improvement

Analyzes the current session for forgotten/ignored rules and proposes concrete
improvements to CLAUDE.md, memory/*.md, or commands/*.md.

## When to Invoke
- Before a commit after complex or problematic sessions
- When the user had to make corrections ("nicht so" / "not like that", "das war falsch" / "that was wrong", "vergessen" / "forgot")
- Optionally at the end of any session as a learning step

## Workflow

### 1. Read Correction Log
Read `~/.claude/logs/corrections.jsonl` (if present) - contains automatically
logged tool errors and manually logged corrections via `/note`.

### 2. Analyze Session
Reflect on this session:
- Which rules from CLAUDE.md / memory/*.md were forgotten or ignored?
- Where did the user have to correct?
- What misunderstandings occurred?
- Which expectations were not met?

### 3. Identify Patterns
Categorize problems:
| Category | Example |
|----------|---------|
| Rule forgotten | Review checklist skipped |
| Rule unclear | "Admin Debug Mode" - unclear when active |
| Rule missing | Behavior not defined for situation X |
| Rule contradictory | Standard A vs. Standard B |
| Tool error | Tool permission, file not read, etc. |

### 4. Propose Improvements

For each problem: concrete improvement proposal with target file and change.

**Output Format:**
```
## Session Analysis

### Problems This Session
| # | Problem | Category | Frequency |
|---|---------|----------|-----------|
| 1 | Review checklist skipped | Rule forgotten | 2x |
| 2 | ... | ... | ... |

### Proposed Improvements
**[1] ~/.claude/CLAUDE.md - Line X**
Old: "..."
New: "..."
Reason: ...

**[2] ~/.claude/memory/standards.md**
Add after "## UI/Frontend":
"..."

### Tool Errors (from corrections.jsonl)
- [Timestamp] Tool: X, Error: Y

-> Apply changes? (yes / "ja" / only #X,Y / "nur Nr. X,Y" / no / "nein")
```

### 5. Apply After User Approval
- On "yes" / "ja": apply all changes directly
- On "only #X,Y" / "nur Nr. X,Y": apply only the listed ones
- Archive correction log after analysis (rename with date)

---

## Micro-Loop (for each step)
Scan -> Plan -> Act -> Reflect (does it work? if not: stop + report)
