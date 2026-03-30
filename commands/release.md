# /release - Release-Workflow

Führt den vollständigen Release-Workflow aus nach User-Freigabe.

## Voraussetzungen prüfen
- [ ] Alle Tests grün
- [ ] Coverage ≥ 90%
- [ ] Code Review bestanden
- [ ] Migration/Patch vorhanden und getestet
- [ ] Rollback-Strategie vorhanden

## Ablauf

### 1. Release vorbereiten
- Version berechnen (Semantic Versioning aus Commit-Types)
- CHANGELOG.md aktualisieren (automatisch aus Commits)
- Release Notes generieren:
  - Technisch (für Entwickler): alle Commits, Breaking Changes, Migration Steps
  - Kundenfreundlich (ohne Jargon): Was ist neu, was wurde behoben

### 2. Test-System deployen
- Auto-Deploy auf Test-System
- Smoke Tests ausführen
- Backup vor Deployment erstellen
- Status ausgeben

### 3. User-Freigabe einholen
```
Test-Deployment erfolgreich.
Version: X.X.X
Änderungen: [Zusammenfassung]

Auf Prod deployen? (ja/nein)
```

### 4. Prod-Deployment (nach "ja")
- Backup erstellen
- Deploy auf Prod
- Smoke Tests auf Prod
- Installer + Patch-Artefakte generieren
- Restore-Test nach Deployment

### 5. Abschluss
- TODO.md Tasks als "done" markieren
- Release taggen (git tag)
- Docs aktualisieren falls nötig

---

## Micro-Loop (für jeden Schritt)
Scan (was existiert?) → Plan (was genau?) → Act → Reflect (funktioniert? sonst: stoppen + melden)
