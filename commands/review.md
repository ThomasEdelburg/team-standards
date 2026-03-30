# /review - Code Review

Führt den vollständigen Code Review vor einem Commit durch.
Gibt Bewertung als kompakte Tabelle aus.

## Ablauf

1. Geänderte Dateien identifizieren (git diff)
2. Review-Checkliste aus `~/.claude/memory/checklists.md` durchgehen
3. Kleine Verstöße direkt korrigieren (ohne Rückfrage)
4. Architektur-Entscheidungen / Breaking Changes → User vorlegen
5. Cleanup-Checkliste prüfen (bei komplexen Änderungen)
6. /test aufrufen - alle Tests müssen grün sein
7. /reflect aufrufen (bei komplexen Sessions oder wenn Korrektionen nötig waren)
8. Ergebnis ausgeben

## Output-Format

```
## Code Review - [Branch/Task]

| Prüfpunkt              | Status | Aktion         |
|------------------------|--------|----------------|
| Dateigröße             | ✓      | -              |
| Zirkuläre Imports      | ✓      | -              |
| ...                    | ...    | ...            |

**Direkt korrigiert:** [Liste der Auto-Fixes]
**Für User:** [Liste der Entscheidungen die User treffen muss]
**Tests:** ✓ grün / ✗ fehlgeschlagen
**Coverage:** XX%

→ Bereit für Commit: JA / NEIN
```

## Commit-Gate
Nur wenn alle Punkte ✓ und Coverage ≥ 90%:
Conventional Commit erstellen (feat: / fix: / BREAKING CHANGE:)

---

## Micro-Loop (für jeden Schritt)
Scan (was existiert?) → Plan (was genau?) → Act → Reflect (funktioniert? sonst: stoppen + melden)
