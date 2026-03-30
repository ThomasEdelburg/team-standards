# /implement - Implementierung starten

Startet den vollständigen Implementierungs-Workflow mit parallelen Agents.
Nur ausführen wenn Planung abgeschlossen und User-Freigabe erteilt wurde.

## Voraussetzungen prüfen
- [ ] TODO.md enthält fertige Planung mit Abnahmekriterien
- [ ] Contracts/Interfaces als Dateien definiert (oder Contract Agent ausführen)
- [ ] User hat explizit "lege los" oder /implement aufgerufen

## Phase 1 - Contract Agent (sequenziell, blockiert Phase 2)

Starte Agent mit Fokus:
- DB-Schema + Migrations definieren
- API-Spec (OpenAPI) erstellen
- Interfaces/Types/Contracts als Dateien ablegen
- Worktree: `feature/[task-id]-contracts`

Warte auf Abschluss bevor Phase 2 startet.

## Phase 2 - Agent Teams parallel (3 Teammates)

Agent Teams nutzen (CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1):
Teammates kommunizieren direkt miteinander über geteilte Task-Liste.

**Backend Teammate** (Worktree: `feature/[task-id]-backend`):
- Zuständigkeit: DB-Layer + API-Endpoints
- Implementiert gegen Contracts aus Phase 1
- Standards: 4-Tier, ORM, REST, Error Handling, Logging
- Meldet an Frontend Teammate wenn API-Endpoints bereit

**Frontend Teammate** (Worktree: `feature/[task-id]-frontend`):
- Zuständigkeit: UI-Komponenten + State Management
- Wartet auf API-Bereitschaft vom Backend Teammate
- Standards: Tailwind, Loading/Error/Empty States, i18n, WCAG AA

**Unit-Test Teammate** (Worktree: `feature/[task-id]-unit-tests`):
- Zuständigkeit: Unit + Range/Boundary Tests gegen Contracts
- Arbeitet parallel zu Backend/Frontend gegen Interfaces
- Ziel: 90% Coverage der Business Logic

## Phase 3 - Agent Teams parallel (nach Phase 2)

**Integration-Test Teammate** (Worktree: `feature/[task-id]-integration-tests`):
- API + DB Integration Tests mit echter Test-DB
- Keine Mocks auf DB-Ebene

**E2E-Test Teammate** (Worktree: `feature/[task-id]-e2e-tests`):
- Komplette Workflows im Browser (Playwright oder Cypress)
- Visual Regression, Accessibility Tests

## Abschluss
Nach allen Agents: /review aufrufen

---

## Micro-Loop (für jeden Schritt)
Scan (was existiert?) → Plan (was genau?) → Act → Reflect (funktioniert? sonst: stoppen + melden)
