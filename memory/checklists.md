---
name: Checklists
description: Review checklist (before commit), cleanup checklist (before completion), test behavior
type: feedback
---

## Review Checklist (before every commit)

| Check | Rule |
|---|---|
| File size business logic | max 300 lines |
| File size UI components | max 200 lines |
| File size tests | max 500 lines |
| Generated code | no limit |
| Circular imports | not allowed |
| Mutable state | thread-safe |
| Async | no synchronous calls blocking event loop |
| Public APIs | fully typed, no Any |
| Magic strings | forbidden → enums/constants |
| Catch-all exceptions | forbidden → specific, log + re-raise unexpected |
| Obsolescence scan | remove unused files/functions/imports |
| Cross-reference | no `_private` access from outside |
| Data format | keys, column names, delimiters consistent |
| Parameter signatures | names + types identical in call and definition |
| Return types | function returns what caller expects |
| Schema ↔ handler | required fields identical in schema and handler |
| Null/None guards | no code paths that crash on None |
| Resource leaks | connections/file handles closed even on errors |
| Side effects constructor | `__init__()` no files/directories/network |
| N+1 queries | forbidden |
| Rollback possible | migration backwards-compatible |

## Cleanup Checklist (before completing complex tasks)

| Check | Action |
|---|---|
| Replaced modules | Remove/mark old module |
| Orphaned files | Dead code analysis (grep on filename) |
| Outdated docs | Update or mark as DEPRECATED |
| Stale dependencies | Remove packages no longer imported |
| Coverage >= 90% | Check coverage report, write missing tests |
| Unused config | Remove settings/env vars/schema fields without evaluation |
| Migration compatibility | If B replaces module A: can B read A's data? |
| Restore test | Verify backup after release |

## Test Behavior

- Testing = tests + linting + formatting (stack-specific)
- Quote error messages in full — never truncate
- Test isolation: no side effects (files, env vars, DB entries)
- Edge cases: None input, empty lists, missing files, timeouts
- Mock correctness: mock at the right level

## Bash Commands (mandatory rules)

**Never nested quotes** — triggers security check:
- WRONG: `grep -A 5 "FAILED\|Error"` | RIGHT: `grep -A 5 'FAILED\|Error'`
- WRONG: `python -c "import json"` | RIGHT: `python -c 'import json'`

**Integration tests with external models:**
- Skip condition when model not locally cached: `pytest.mark.skipif(not model_cached, ...)`
- Prevents errors from failed downloads in CI/tests
