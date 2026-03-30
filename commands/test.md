# /test - Test-Suite ausführen

Führt alle Tests aus und gibt einen vollständigen Status-Report aus.

## Ablauf

1. Stack erkennen (package.json / pyproject.toml / etc.)
2. Tests + Linting + Formatting ausführen (stack-spezifische Tools)
3. Coverage-Report generieren
4. Ergebnis als kompakte Tabelle ausgeben

## Test-Reihenfolge
1. Linting + Formatting
2. Unit Tests (mit Coverage)
3. Integration Tests (echte Test-DB)
4. E2E Tests (falls konfiguriert)

## Output-Format

```
| Test-Art        | Status     | Coverage | Dauer  |
|-----------------|------------|----------|--------|
| Linting         | ✓ / ✗      | -        | Xs     |
| Unit Tests      | ✓ / ✗      | XX%      | Xs     |
| Integration     | ✓ / ✗      | XX%      | Xs     |
| E2E             | ✓ / ✗      | -        | Xs     |
| Gesamt Coverage | -          | XX%      | -      |
```

## Bei Fehlern
- Fehlermeldung vollständig zitieren - nicht kürzen
- Ursache identifizieren
- Lösung vorschlagen, aber NICHT automatisch Code ändern

## Coverage-Gate
Wenn Gesamt-Coverage < 90%: fehlende Tests identifizieren und schreiben.
Kein Commit bis Coverage ≥ 90%.

---

## Micro-Loop (für jeden Schritt)
Scan (was existiert?) → Plan (was genau?) → Act → Reflect (funktioniert? sonst: stoppen + melden)
