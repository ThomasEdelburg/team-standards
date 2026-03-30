# /note - Korrektur manuell loggen

Loggt eine Korrektur oder ein Problem manuell in `~/.claude/logs/corrections.jsonl`.
Wird von `/reflect` ausgewertet.

## Verwendung

```
/note [Beschreibung des Problems]
```

**Beispiele:**
- `/note Review-Checkliste übersprungen`
- `/note Falsches Tool verwendet - Read statt Bash cat`
- `/note Regel aus standards.md ignoriert: kein SELECT *`
- `/note User-Erwartung falsch verstanden bei Deployment`

## Was geloggt wird
- Timestamp
- Session-ID (aus Umgebung)
- Nachricht (User-Input)
- Kontext: aktuelle Aufgabe / letztes Tool

## Ablauf

1. Lese Argument (Text nach `/note`)
2. Erstelle Log-Eintrag als JSON
3. Schreibe in `~/.claude/logs/corrections.jsonl` (append)
4. Bestätige: "Notiert: [Text]"

## Log-Format
```json
{"ts": "2026-03-30T10:30:00", "type": "manual", "session": "abc123", "msg": "Review-Checkliste übersprungen", "context": "nach git commit"}
```

## Hinweis
Auch ohne `/note` werden Tool-Fehler automatisch geloggt via `PostToolUseFailure` Hook.
`/reflect` liest beide Quellen.
