# /test - Run Test Suite

Runs all tests and outputs a full status report.

**Trigger words:** "teste", "tests laufen lassen", "check die tests", "alles gruen?", "test", "run tests", "check tests", "all green?"

## Workflow

1. Detect stack (package.json / pyproject.toml / etc.)
2. Run tests + linting + formatting (stack-specific tools)
3. Generate Coverage report
4. Output result as compact table

## Test Order
1. Linting + Formatting
2. Unit Tests (with Coverage)
3. Integration Tests (real test DB)
4. E2E Tests (if configured)

## Output Format

```
| Test Type       | Status     | Coverage | Duration |
|-----------------|------------|----------|----------|
| Linting         | pass/fail  | -        | Xs       |
| Unit Tests      | pass/fail  | XX%      | Xs       |
| Integration     | pass/fail  | XX%      | Xs       |
| E2E             | pass/fail  | -        | Xs       |
| Total Coverage  | -          | XX%      | -        |
```

## On Errors
- Quote error messages in full - never truncate
- Identify root cause
- Suggest a fix, but do NOT automatically change code

## Coverage Gate
If total Coverage < 90%: identify missing tests and write them.
No commit until Coverage >= 90%.

---

## Micro-Loop (for each step)
Scan (what exists?) -> Plan (what exactly?) -> Act -> Reflect (does it work? if not: stop + report)
