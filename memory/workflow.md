---
name: Development Workflow
description: Coding workflow with agents, commit & release management, context tracking
type: feedback
---

## Coding Workflow (Agents)

**Gate: Coding starts only after explicit user approval ("lege los")**

```
TODO → Planning (11 points + contracts as files) → "lege los" → Agents start
```

**Agent sequence:**
1. Contract Agent → Interfaces, API spec, data models
2. Test Agent → Tests against contracts (test-first)
3. API Agent + UI Agent → parallel
4. Review → Coverage >= 90%, cleanup checklist

**Autonomy:** Agents work through independently, user reviews only at the end

---

## Context Tracking

- Only re-evaluate on new topic / new task
- Qualitative: `sufficient / incomplete / unclear`
- If incomplete: don't guess, ask targeted questions, name gaps, suggest options

---

## Commit & Release Management

**Format:** Conventional Commits
- `feat:` → Minor | `fix:` → Patch | `BREAKING CHANGE:` → Major
- Mono-repo scope: `feat(package-name):` / `fix(service-name):`

**Versioning:** Semantic Versioning — auto-bump via semantic-release
**Release trigger:** Every commit on main = release

**Commit gate (no exceptions, including hotfixes):**
1. Code review passed
2. All tests + linting + formatting green
3. Migration/patch present and tested

**Code review:**
- Auto-apply standards (SOLID, Clean Code, 4-tier, OWASP, performance)
- Minor violations → fix directly
- Architecture / breaking changes → present to user
- Output rating in chat

**Release artifacts:**
- Patch + installer + release notes (technical + customer-friendly) + CHANGELOG.md

**Deploy flow:**
```
Commit → Tests green → Auto-deploy test system → "Deploy to prod?" → yes/no
```

---

## Task Management

**Task list:** `TODO.md` in respective package/app directory

```
## Task #0001: [Title]
**Status:** open | in_progress | blocked | done
**Acceptance criteria:**
- [ ] Functional criteria (auto-generated from description)
- [ ] Tests >= 90% coverage
- [ ] Migration/patch present and tested
- [ ] Code review passed
- [ ] Documentation updated
- [ ] Performance targets met
```

Acceptance criteria are auto-generated from task description + standards.
