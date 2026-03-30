# /new-project - Neues Package/App im Mono-Repo anlegen

Legt ein neues Package oder eine App als Unterverzeichnis im Mono-Repo an.

## Ablauf

1. Package-Name und Typ erfragen falls nicht angegeben (app / service / package / lib)
2. Zielverzeichnis bestimmen:
   - Apps: `apps/[name]`
   - Services: `services/[name]`
   - Packages/Libs: `packages/[name]`
3. Template kopieren von `~/.claude/templates/project/`
4. Platzhalter `{{PROJECT_NAME}}` und `{{DATE}}` ersetzen
5. Package-spezifische `.claude/CLAUDE.md` anlegen mit Stack-Informationen
6. Pre-commit Hooks prüfen (sollten bereits im Root aktiv sein)
7. `TODO.md` im Package anlegen
8. Ersten Commit erstellen: `feat([name]): initial package structure`

## Mono-Repo Struktur
```
repo-root/
├── .github/workflows/     # Gemeinsame CI/CD
├── .gitignore             # Gemeinsam
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

## GitHub Actions Secrets (einmalig pro Repo setzen)
```bash
gh secret set TEST_DATABASE_URL --body "postgresql://..." --repo [repo]
gh secret set TEST_APP_URL      --body "https://test.example.com" --repo [repo]
gh secret set DEPLOY_KEY        --body "..." --repo [repo]
```

## Nächste Schritte nach Erstellung
1. Stack in `[package]/.claude/CLAUDE.md` eintragen
2. Erste Task in `[package]/TODO.md` anlegen (`/plan`)
3. Entwicklung starten wenn Planung fertig (`/implement`)
