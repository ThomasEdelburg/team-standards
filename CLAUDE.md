# Claude Global Standards

These standards apply to ALL projects. Detail files are in `~/.claude/memory/`.

## Required: Read these files at session start
- `~/.claude/memory/standards.md` - Technical standards
- `~/.claude/memory/workflow.md` - Workflow, agents, commits, tasks
- `~/.claude/memory/checklists.md` - Review, cleanup, test behavior

---

## Environment
- **Platform:** Windows 11 (Git Bash as shell)
- **Repo strategy:** Mono-repo (all projects/packages in one Git repository)
- **Context:** Corporate environment — no private projects

## Natural Language → Auto-Commands

Detect intent and automatically invoke the matching command — no need for the user to know command names:

| When user says... | Command |
|---|---|
| "plan", "new task", "what do we need to do" / "plane", "neue task", "was müssen wir tun", "lass uns planen" | `/plan` |
| "let's go", "start", "implement", "begin" / "lege los", "starte", "implementiere", "fang an" | `/implement` |
| "test", "run tests", "all green?" / "teste", "tests laufen lassen", "check die tests", "alles grün?" | `/test` |
| "review", "check the code", "is the code ok" / "prüf den code", "ist der code ok" | `/review` |
| "release", "deploy", "publish", "to prod" / "veröffentlichen", "auf prod" | `/release` |

## Core Rules (always active)

### Workflow
- **Coding gate:** Only start coding after planning is complete + user says "lege los"
- **Commit gate:** Code review + tests green + migration tested (no exceptions, including hotfixes)
- **Deployment:** Auto-deploy to test → user approval for prod
- **Task management:** TODO.md in repo, acceptance criteria auto-generated

### Quality
- **Testing:** Always real DB, NO mocking, 90% coverage entire codebase
- **Architecture:** 4-tier (Presentation, Application/Service, Domain, Data Access)
- **Configuration:** All parameters in admin area — never hardcoded
- **Secrets:** OS Keychain (local) / Secret manager (CI/CD) — never in code/config/.env

### Behavior
- **Language:** Always communicate in German with user
- **Context:** Evaluate quality on new topics (sufficient / incomplete / unclear)
- **Don't guess:** Ask targeted questions when context is missing
- **Review checklist:** Run through before every commit (see checklists.md)
- **Cleanup checklist:** Before completing complex tasks (see checklists.md)
- **Error messages:** Quote in full, never truncate
- **Minor violations:** Fix directly without asking
- **Architecture decisions:** Present to user

### Micro-Loop (applies to me AND all agents)
Run implicitly before every significant action — no explicit output needed:
- **Scan:** What actually exists? Don't assume — verify
- **Plan:** Specifically: what exactly, in what order?
- **Act:** Execute
- **Reflect:** Did it work? Is the result correct? → If no: stop and report, don't continue

### Planning (11 points — for larger tasks)
1. Understand the task
2. Gather context (explore)
3. Clarify constraints
4. Check dependencies
5. Ensure deployment & migration (MUST: patch without breaking changes)
6. Communicate plan + user approval
7. Testing strategy
8. Error handling & monitoring
9. Security review
10. Documentation
11. Data migration

**Task size:** Small (1-3 mental) | Medium (explicit, 5+7+9) | Large (EnterPlanMode, all 11)

### Mono-Repo Conventions
- Packages/apps as subdirectories (e.g. `packages/`, `apps/`, `services/`, `libs/`)
- Shared configuration in root (`.gitignore`, `pre-commit`, CI/CD)
- Package-specific CLAUDE.md in respective subdirectory
- Shared dependencies in root, package-specific locally
