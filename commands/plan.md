# /plan - Planungsphase

Führe die vollständige Planungsphase für die aktuelle oder angegebene Task durch.

## Ablauf

1. Lies `~/.claude/memory/standards.md`, `~/.claude/memory/workflow.md`, `~/.claude/memory/checklists.md`
2. Lies die aktuelle `TODO.md` im Projektverzeichnis (falls vorhanden)
3. Führe die 11 Planungspunkte durch (aus CLAUDE.md)
4. Generiere automatisch Abnahmekriterien für die Task
5. Erstelle oder aktualisiere den Task-Eintrag in `TODO.md`
6. Warte auf explizite User-Freigabe ("lege los") bevor du mit Coding beginnst

## Task-Format in TODO.md

```
## Task #XXXX: [Titel]
**Status:** open
**Abnahmekriterien:**
- [ ] [Funktionale Kriterien - aus Beschreibung abgeleitet]
- [ ] Tests ≥ 90% Coverage
- [ ] Migration/Patch vorhanden und getestet
- [ ] Code-Review bestanden
- [ ] Dokumentation aktualisiert
- [ ] Performance-Ziele erfüllt
```

## Kontext-Check
Bewerte ob der Kontext ausreichend/lückenhaft/unklar ist.
Bei lückenhaft: gezielt nachfragen bevor du planst.
