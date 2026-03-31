# /implement - Start Implementation

Starts the full implementation workflow with parallel agents.
Only execute when planning is complete and user approval has been granted.

**Trigger words:** "lege los", "starte", "implementiere", "fang an", "let's go", "start", "implement", "begin"

## Check Prerequisites
- [ ] TODO.md contains completed planning with acceptance criteria
- [ ] Contracts/Interfaces defined as files (or run Contract Agent)
- [ ] User has explicitly said "lege los" / "let's go" or invoked /implement

## Phase 1 - Contract Agent (sequential, blocks Phase 2)

Start agent with focus:
- Define DB schema + migrations
- Create API spec (OpenAPI)
- Store interfaces/types/contracts as files
- Worktree: `feature/[task-id]-contracts`

Wait for completion before Phase 2 starts.

## Phase 2 - Agent Teams in Parallel (3 Teammates)

Use Agent Teams (CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1):
Teammates communicate directly with each other via shared task list.

**Backend Teammate** (Worktree: `feature/[task-id]-backend`):
- Responsibility: DB layer + API endpoints
- Implements against contracts from Phase 1
- Standards: 4-tier, ORM, REST, error handling, logging
- Notifies Frontend Teammate when API endpoints are ready

**Frontend Teammate** (Worktree: `feature/[task-id]-frontend`):
- Responsibility: UI components + state management
- Waits for API readiness from Backend Teammate
- Standards: Tailwind, loading/error/empty states, i18n, WCAG AA

**Unit Test Teammate** (Worktree: `feature/[task-id]-unit-tests`):
- Responsibility: Unit + range/boundary tests against contracts
- Works in parallel with Backend/Frontend against interfaces
- Goal: 90% Coverage of business logic

## Phase 3 - Agent Teams in Parallel (after Phase 2)

**Integration Test Teammate** (Worktree: `feature/[task-id]-integration-tests`):
- API + DB integration tests with real test DB
- No mocks at DB level

**E2E Test Teammate** (Worktree: `feature/[task-id]-e2e-tests`):
- Complete workflows in browser (Playwright or Cypress)
- Visual regression, accessibility tests

## Completion
After all agents finish: invoke /review

---

## Micro-Loop (for each step)
Scan (what exists?) -> Plan (what exactly?) -> Act -> Reflect (does it work? if not: stop + report)
