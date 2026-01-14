# PR Merge Procedure

## Proper Workflow for Merging Pull Requests

### Standard Merge Process (Preferred)

1. **Create feature branch**

   ```bash
   git checkout -b feature/description
   ```

2. **Make changes and commit**

   ```bash
   # Make your changes
   git add .
   git commit -m "type: description"
   ```

3. **Push branch**

   ```bash
   git push -u origin feature/description
   ```

4. **Create Pull Request**

   ```bash
   gh pr create --title "Title" --body "Description"
   ```

5. **Wait for CI/CD checks**
   - Pre-Commit Hooks must pass
   - Lint must pass
   - Type Check must pass
   - Config Validation must pass
   - Test (Python 3.12) must pass

6. **Get approval**
   - Cannot approve your own PR
   - Requires 1 approving review (per branch protection)

7. **Merge via GitHub CLI**
   ```bash
   gh pr merge <number> --squash --delete-branch
   ```

### Emergency Bypass (Use Sparingly)

Only when you need to merge your own PR and cannot get approval:

1. **Disable branch protection**

   ```bash
   gh api -X DELETE repos/lair-click-bats/tracekit/branches/main/protection
   ```

2. **Merge the PR**

   ```bash
   gh pr merge <number> --squash --delete-branch
   ```

3. **Re-enable branch protection immediately**
   ```bash
   gh api -X PUT repos/lair-click-bats/tracekit/branches/main/protection \
     --input - <<'EOF'
   {
     "required_status_checks": {
       "strict": true,
       "contexts": ["Pre-Commit Hooks", "Lint", "Type Check", "Config Validation", "Test (Python 3.12)"]
     },
     "enforce_admins": false,
     "required_pull_request_reviews": {
       "dismiss_stale_reviews": false,
       "require_code_owner_reviews": false,
       "required_approving_review_count": 1
     },
     "restrictions": null,
     "required_linear_history": false,
     "allow_force_pushes": false,
     "allow_deletions": false
   }
   EOF
   ```

### Anti-Patterns (Never Do This)

- **Never push directly to main** while branch protection is disabled without creating a PR first
- **Never leave branch protection disabled** after merging
- **Never skip CI/CD checks** by merging before they complete
- **Never commit temporary audit files** (e.g., `*_AUDIT_*.md`, `*_SUMMARY.md`, `*_RESULTS.*`)

### Best Practices

1. **Small, focused PRs** - One logical change per PR
2. **Descriptive commit messages** - Follow conventional commits format
3. **Clean up branches** - Delete branches after merging
4. **Run pre-commit locally** - Before pushing: `pre-commit run --all-files`
5. **Test locally** - Before creating PR: `uv run pytest tests/unit/<module> -v`

### CI/CD Status Checks

Required checks that must pass:

- Pre-Commit Hooks
- Lint
- Type Check
- Config Validation
- Test (Python 3.12)

Optional checks (may be skipped):

- Test (Python 3.13)
- Integration Tests
- IEEE/JEDEC Compliance
- Build Package
- Performance Benchmarks

### Branch Protection Settings

Current configuration:

- Require status checks: Yes (5 required checks)
- Require approving reviews: Yes (1 review)
- Enforce for administrators: No (allows emergency bypass)
- Require linear history: No
- Allow force pushes: No
- Allow deletions: No

### Verification Commands

Check branch protection status:

```bash
gh api repos/lair-click-bats/tracekit/branches/main/protection \
  --jq '{required_status_checks: .required_status_checks.contexts, required_reviews: .required_pull_request_reviews.required_approving_review_count}'
```

Check PR status:

```bash
gh pr view <number> --json statusCheckRollup \
  --jq '.statusCheckRollup[] | {name, status, conclusion}'
```

List all PRs:

```bash
gh pr list --state all --limit 10
```

## Historical Note

This procedure was established after PR #9 (2026-01-07) to formalize the process and avoid bypassing the PR workflow with direct commits to main.
