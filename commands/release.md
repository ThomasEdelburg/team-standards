# /release - Release Workflow

Executes the full release workflow after user approval.

**Trigger words:** "release", "deploy", "veroeffentlichen", "auf prod", "publish", "to prod", "ship it"

## Check Prerequisites
- [ ] All tests green
- [ ] Coverage >= 90%
- [ ] Code review passed
- [ ] Migration/Patch present and tested
- [ ] Rollback strategy in place

## Workflow

### 1. Prepare Release
- Calculate version (Semantic Versioning from commit types)
- Update CHANGELOG.md (automatically from commits)
- Generate release notes:
  - Technical (for developers): all commits, breaking changes, migration steps
  - User-friendly (no jargon): what's new, what was fixed

### 2. Deploy to Test System
- Auto-deploy to test system
- Run smoke tests
- Create backup before deployment
- Output status

### 3. Get User Approval
```
Test deployment successful.
Version: X.X.X
Changes: [Summary]

Deploy to prod? (yes/no)
```

### 4. Prod Deployment (after "yes" / "ja")
- Create backup
- Deploy to prod
- Run smoke tests on prod
- Generate installer + patch artifacts
- Restore test after deployment

### 5. Wrap-Up
- Mark TODO.md tasks as "done"
- Tag release (git tag)
- Update docs if needed

---

## Micro-Loop (for each step)
Scan (what exists?) -> Plan (what exactly?) -> Act -> Reflect (does it work? if not: stop + report)
