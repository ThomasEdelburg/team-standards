# Claude Code Team Standards

Shared Claude Code configuration for the team. Clone directly as your `~/.claude/` directory.

## Quick Setup (new team member)

```bash
# If you already have ~/.claude/ — back it up first
mv ~/.claude ~/.claude-backup

# Clone this repo as your ~/.claude/
git clone https://github.com/ThomasEdelburg/team-standards.git ~/.claude

# Done! Start Claude Code — everything works immediately.
```

## What's included

| File/Dir | Purpose |
|----------|---------|
| `CLAUDE.md` | Global standards (loaded every session) |
| `memory/standards.md` | Technical standards (architecture, DB, API, security, testing) |
| `memory/workflow.md` | Workflow, commit rules, TODO/checklist format |
| `memory/checklists.md` | Review checklist (before commit), cleanup checklist |
| `settings.json` | Team permissions, hooks (auto-lint, error logging) |
| `scripts/session-start.py` | SessionStart hook (loads memory, runs techstack check) |
| `scripts/commit-gate-hook.py` | Pre-commit quality gate |
| `scripts/techstack-check.py` | Weekly toolchain health check |
| `commands/*.md` | Slash commands (/plan, /implement, /review, /test, /release, etc.) |
| `templates/project/` | Project template for `/new-project` (CLAUDE.md, CI/CD, docs, Makefile, TODO) |

## What's NOT included (personal, stays local)

These are auto-created locally and ignored by `.gitignore`:

- `.credentials.json` — your auth tokens
- `settings.local.json` — your personal overrides (e.g. `bypassPermissions`)
- `history.jsonl` — your conversation history
- `sessions/` — session data
- `projects/` — per-project personal memory
- `logs/` — local log files
- `cache/`, `plugins/`, `ide/` — runtime data

## Personal overrides

To override team settings without affecting the repo, create `settings.local.json`:

```json
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  }
}
```

This file is gitignored — your personal preferences stay local.

## Updating

```bash
cd ~/.claude
git pull
```

## Contributing

1. Make changes to the shared files
2. Test locally
3. Commit and push — all team members get updates on next `git pull`

## Future: Plugin

A Claude Code plugin version of these standards is planned (see `TODO.md` in ReadingRoom repo).
This will enable automatic installation and updates without manual git operations.
