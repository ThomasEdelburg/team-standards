# /reflect - Session-Analyse & Standards-Verbesserung

Analysiert die aktuelle Session auf vergessene/ignorierte Regeln und schlägt konkrete
Verbesserungen an CLAUDE.md, memory/*.md oder commands/*.md vor.

## Wann aufrufen
- Vor einem Commit nach komplexen oder problematischen Sessions
- Wenn User Korrektionen machen musste ("nicht so", "das war falsch", "vergessen")
- Optional am Ende jeder Session als Lernschritt

## Ablauf

### 1. Korrektions-Log lesen
Lese `~/.claude/logs/corrections.jsonl` (falls vorhanden) - enthält automatisch
geloggte Tool-Fehler und manuell geloggte Korrektionen via `/note`.

### 2. Session analysieren
Reflektiere über diese Session:
- Welche Regeln aus CLAUDE.md / memory/*.md wurden vergessen oder ignoriert?
- Wo musste der User korrigieren?
- Welche Missverständnisse gab es?
- Welche Erwartungen wurden nicht erfüllt?

### 3. Muster identifizieren
Kategorisiere Probleme:
| Kategorie | Beispiel |
|-----------|---------|
| Regel vergessen | Review-Checkliste übersprungen |
| Regel unklar | "Admin Debug Mode" - unklar wann aktiv |
| Regel fehlend | Verhalten nicht definiert für Situation X |
| Regel widersprüchlich | Standard A vs. Standard B |
| Werkzeug-Fehler | Tool-Permission, File not read etc. |

### 4. Verbesserungen vorschlagen

Für jedes Problem: konkreter Verbesserungsvorschlag mit Zieldatei und Änderung.

**Output-Format:**
```
## Session-Analyse

### Probleme diese Session
| # | Problem | Kategorie | Häufigkeit |
|---|---------|-----------|------------|
| 1 | Review-Checkliste übersprungen | Regel vergessen | 2x |
| 2 | ... | ... | ... |

### Vorgeschlagene Verbesserungen
**[1] ~/.claude/CLAUDE.md - Zeile X**
Alt: "..."
Neu: "..."
Begründung: ...

**[2] ~/.claude/memory/standards.md**
Ergänzen nach "## UI/Frontend":
"..."

### Tool-Fehler (aus corrections.jsonl)
- [Timestamp] Tool: X, Fehler: Y

→ Änderungen anwenden? (ja / nur Nr. X,Y / nein)
```

### 5. Anwenden nach User-Freigabe
- Bei "ja": alle Änderungen direkt anwenden
- Bei "nur Nr. X,Y": nur die genannten anwenden
- Korrektions-Log nach Analyse archivieren (umbenennen mit Datum)

---

## Micro-Loop (für jeden Schritt)
Scan → Plan → Act → Reflect (funktioniert? sonst: stoppen + melden)
