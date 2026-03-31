# /new-project - Create New Package/App in the Mono-Repo

Creates a new package or app as a subdirectory in the mono-repo.

**Trigger words:** "neues Projekt", "neues Package", "neue App", "new project", "new package", "new app", "create project"

## Workflow

1. Ask for package name and type if not provided (app / service / package / lib)
2. Determine target directory:
   - Apps: `apps/[name]`
   - Services: `services/[name]`
   - Packages/Libs: `packages/[name]`
3. Copy template from `~/.claude/templates/project/`
4. Replace placeholders `{{PROJECT_NAME}}` and `{{DATE}}`
5. Create package-specific `.claude/CLAUDE.md` with stack information
6. Check pre-commit hooks (should already be active in root)
7. Create `TODO.md` in the package
8. Create initial commit: `feat([name]): initial package structure`

## Mono-Repo Structure
```
repo-root/
├── .github/workflows/     # Shared CI/CD
├── .gitignore             # Shared
├── .pre-commit-config.yaml
├── apps/
│   └── [name]/
│       ├── .claude/CLAUDE.md
│       ├── docs/
│       ├── src/
│       └── TODO.md
├── packages/
│   └── [name]/
├── services/
│   └── [name]/
└── libs/
    └── [name]/
```

## GitHub Actions Secrets (set once per repo)
```bash
gh secret set TEST_DATABASE_URL --body "postgresql://..." --repo [repo]
gh secret set TEST_APP_URL      --body "https://test.example.com" --repo [repo]
gh secret set DEPLOY_KEY        --body "..." --repo [repo]
```

## Next Steps After Creation
1. Enter stack in `[package]/.claude/CLAUDE.md`
2. Create first task in `[package]/TODO.md` (`/plan`)
3. Start development when planning is complete (`/implement`)
