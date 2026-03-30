---
name: Technical Standards
description: Architecture, DB, API, logging, error handling, performance, UI, security, i18n, testing, deployment
type: feedback
---

## Architecture
- **4-tier** as standard (Presentation, Application/Service, Domain, Data Access)

## Database
- ORM as standard — raw SQL only for complex queries
- Migrations always versioned (Alembic/Flyway/Prisma Migrate etc.)
- Indexing: all foreign keys + frequently filtered fields
- Naming: snake_case, plural (`users`, `user_roles`)
- No `SELECT *` — always explicit fields
- Connection pooling always active

## API Design
- REST as standard — GraphQL only when explicitly justified
- Versioning: URL-based (`/api/v1/`)
- Error response: `{ error, message, details }`
- Pagination always on lists: cursor-based
- Use HTTP status codes correctly
- OpenAPI/Swagger auto-generated

## Logging
- Structured logging (JSON format)
- Log levels: DEBUG / INFO / WARNING / ERROR / CRITICAL
- Always log: request ID, timestamp, user ID (anonymized), duration
- Never log: passwords, tokens, personal data
- Pass correlation ID through all services
- 3 channels: stdout/stderr (CI/CD), rotated file (debugging), DB (audit trail)

## Error Handling
- User-facing: clear message without technical details (i18n-capable)
- Internal: full stack trace in logs
- Error codes: `ERR_NOT_FOUND`, `ERR_UNAUTHORIZED`, `ERR_VALIDATION`, `ERR_TIMEOUT`
- Global error handler per application

## Performance
- API: < 200ms (p95) | UI: < 100ms time-to-interactive | DB: < 50ms
- Bundle size: < 200KB initial (gzipped)
- N+1 queries forbidden | Lazy loading for UI/routes

## Configuration
- All parameters in DB/admin area — not hardcoded, not in local JSON files
- Exception: only when technically impossible (e.g. boot configuration)
- Admin area is mandatory for every application

## UI/Frontend
- Every async operation: loading / error / empty state — always all three
- State management: local where possible, global store only when needed
- Breakpoints: Mobile (< 768px), Tablet (768-1024px), Desktop (> 1024px)
- CSS: Tailwind preferred — alternatively CSS Modules
- Components: separate presentational vs. container
- Accessibility: ARIA labels, keyboard navigation, WCAG AA
- Forms: client AND server-side validation
- No direct DOM manipulation outside the framework
- Theming + light/dark mode as standard
- Health state UI in admin area: service status, start/stop, metrics, log viewer

## Naming Conventions
- Files: kebab-case | Classes: PascalCase | Functions/vars: camelCase (JS) / snake_case (Python)
- Constants/enums: SCREAMING_SNAKE_CASE
- DB: snake_case, plural | API endpoints: kebab-case, plural (`/api/v1/user-profiles`)
- Test files: `*.test.ts` / `test_*.py` next to source file

## Documentation (mandatory set per project/package)
- `README.md`, `docs/install.md`, `docs/admin.md`, `docs/user.md`, `docs/operations.md`
- `CHANGELOG.md` auto-generated | OpenAPI/Swagger auto-generated from code
- Inline comments only where logic is not self-explanatory

## Monitoring & Alerting
- `/health` endpoint mandatory
- Metrics: response time, error rate, DB pool, memory/CPU
- Error rate > 1% → warning | > 5% → critical | p95 > 500ms → warning
- Stack + channel: project-specific

## Backup & Restore
- Automatic: daily + before every release
- Restore test mandatory | Verify backup integrity
- Retention policy: project-specific
- Restore test belongs in release checklist

## Security — Sensitive Data
- Never in: code, config files, .env (committed), Docker images, logs
- Local: OS Keychain | CI/CD: secret management of respective system

## Internationalization (i18n)
- No hardcoded strings in UI or API responses
- Translation keys: `domain.context.key` (e.g. `user.login.button`)
- Preferred: `i18next` (frontend, Node.js) | Python: `babel` + `gettext`

## Testing
- Always real DB — NO mocking at DB level
- Separate test DB instance (test_db vs. production_db)
- Even for POCs: mock data in DB, NOT in UI
- Always run tests with coverage (pytest --cov, vitest --coverage etc.)
- **Target: 90% test coverage — entire codebase** (including refactoring)
- E2E/UI tool: per project (Playwright or Cypress)
- Test types: unit+range, property-based, integration, API, contract, component, E2E, visual regression, accessibility, performance, security, smoke
- Test isolation: no side effects after tests
- Edge cases explicit: None input, empty lists, missing files, timeouts
- Mock correctness: mock at the right level

## Dependency Management
- Automatic vulnerability scans in CI/CD (npm audit, pip audit, dependabot etc.)
- Security patches: apply immediately — tests must be green
- Major updates: planned, normal workflow
- Monthly check for outdated dependencies
- No packages with known CVEs in prod

## GDPR/Data Privacy
- Data minimization: only collect what is needed
- Right to deletion: user data fully deletable (including logs — document)
- Anonymization in logs: hash user IDs, no names/emails in logs
- Retention: logs max 90 days, personal data only as long as needed
- Consent for non-essential data: store documented
- Data breach: 72h notification to authority, define process

## Rate Limiting & DoS Protection
- Rate limiting: per IP + per user (stack-specific middleware/gateway)
- Unauthenticated: 60 req/min | Authenticated: 600 req/min | Login: 10 req/min
- HTTP 429 + `Retry-After` header on exceeded limits
- CORS: whitelist instead of wildcard (`*`)

## Auth & Authorization
- Authentication: JWT (stateless), OAuth2 for third-party — choose stack-specific tool
- Authorization: RBAC as standard
- Tokens: access token (15min) + refresh token (7 days)
- Passwords: bcrypt/argon2 — never MD5/SHA1
- Sessions: server-side for admin, JWT for APIs
- 2FA: architecture must allow it (even if not immediately implemented)

## Admin Debug Mode (MUST — every app)
Activatable for all app admins (role-gated). Toggle via admin menu or shortcut.
- **Element overlay**: ID, type, classes, styles on hover
- **Style copy**: copy CSS of an element
- **Component tree** + layout grid display
- **A/B testing**: layout variants switchable (per admin session)
- **Screenshots**: with metadata (timestamp, user, route, viewport)
- **Error logging**: stack trace + automatic screenshot on every error
- **Claude analysis**: active on errors (webhook optional) or on demand

## Deployment & Migration
- Migration: MUST be patch without breaking changes
- One-click deployment | auto-patching mechanism
- Environment: commit → test deploy → "Deploy to prod?" → user: yes/no → prod
- Rollback: re-deploy last artifact + down-migration if DB affected
- Rollback must always be possible
