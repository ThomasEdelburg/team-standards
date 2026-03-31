# /note - Manually Log a Correction

Logs a correction or problem manually to `~/.claude/logs/corrections.jsonl`.
Evaluated by `/reflect`.

## Usage

```
/note [Description of the problem]
```

**Examples:**
- `/note Review checklist skipped`
- `/note Wrong tool used - Read instead of Bash cat`
- `/note Rule from standards.md ignored: no SELECT *`
- `/note User expectation misunderstood during deployment`
- `/note Review-Checkliste uebersprungen` (German also works)

## What Gets Logged
- Timestamp
- Session ID (from environment)
- Message (user input)
- Context: current task / last tool

## Workflow

1. Read argument (text after `/note`)
2. Create log entry as JSON
3. Write to `~/.claude/logs/corrections.jsonl` (append)
4. Confirm: "Noted: [Text]" / "Notiert: [Text]"

## Log Format
```json
{"ts": "2026-03-30T10:30:00", "type": "manual", "session": "abc123", "msg": "Review checklist skipped", "context": "after git commit"}
```

## Note
Even without `/note`, tool errors are automatically logged via `PostToolUseFailure` hook.
`/reflect` reads both sources.
