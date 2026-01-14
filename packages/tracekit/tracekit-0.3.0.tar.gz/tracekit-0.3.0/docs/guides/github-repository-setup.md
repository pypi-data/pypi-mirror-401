# GitHub Repository Settings Setup Guide

This guide provides step-by-step instructions for configuring all GitHub repository settings for TraceKit.

All file-based configurations (`.github/` directory) are already in place. This guide covers settings that must be configured through the GitHub web interface.

---

## Quick Navigation

1. [Branch Protection Rules](#1-branch-protection-rules)
2. [General Repository Settings](#2-general-repository-settings)
3. [Security Settings](#3-security-settings)
4. [Actions & Automation](#4-actions-automation)
5. [Environments](#5-environments)
6. [Tag Protection](#6-tag-protection)
7. [Repository Labels](#7-repository-labels)
8. [Repository Topics](#8-repository-topics)
9. [Verification Checklist](#verification-checklist)

---

## 1. Branch Protection Rules

Navigate to: **Settings → Branches → Add branch protection rule**

### Configuration

| Setting                 | Value  | Notes                    |
| ----------------------- | ------ | ------------------------ |
| **Branch name pattern** | `main` | Protects the main branch |

### Pull Request Settings

- ☑ **Require a pull request before merging**
  - ☑ **Require approvals**: `1`
  - ☑ **Dismiss stale pull request approvals when new commits are pushed**
  - ☑ **Require review from Code Owners** (if team grows)
  - ☐ **Restrict who can dismiss pull request reviews** (leave unchecked)
  - ☑ **Allow specified actors to bypass required pull requests**
    - Add: GitHub Actions bot (for automated updates)

### Status Checks

- ☑ **Require status checks to pass before merging**
  - ☑ **Require branches to be up to date before merging**
  - **Add required status checks** (after CI runs at least once):
    - `ci / test (3.12)` (or your test job name)
    - `ci / test (3.13)` (or your test job name)
    - `ci / lint`
    - `ci / type-check`
    - `security / security-scan` (if applicable)

### Additional Settings

- ☑ **Require conversation resolution before merging**
- ☐ **Require signed commits** (optional - enable if desired)
- ☑ **Require linear history** (cleaner git history)
- ☑ **Require deployments to succeed before merging** (for release environment)

### Rules Applied To

- ☑ **Include administrators**
- ☑ **Restrict who can push to matching branches**
  - Add: Repository maintainers only
  - Add: GitHub Actions (for automated workflows)
- ☐ **Allow force pushes** (must be DISABLED)
- ☐ **Allow deletions** (must be DISABLED)

**Click "Create" to save the branch protection rule.**

---

## 2. General Repository Settings

Navigate to: **Settings → General**

### Repository Name and Description

- **Description**: "Python library for loading, analyzing, and reporting on high-speed digital waveforms and signal integrity measurements"
- **Website**: (leave blank or add your project documentation URL)
- ☑ **Include in the home page**

### Features

| Feature                      | Status     | Reason                            |
| ---------------------------- | ---------- | --------------------------------- |
| **Wikis**                    | ☐ Disabled | Use `docs/` directory instead     |
| **Issues**                   | ☑ Enabled  | Bug tracking and feature requests |
| **Sponsorships**             | ☑ Enabled  | If accepting sponsorships         |
| **Preserve this repository** | ☑ Enabled  | Archive code long-term            |
| **Discussions**              | ☑ Enabled  | Q&A and community                 |
| **Projects**                 | ☑ Enabled  | Project management                |

### Pull Requests

- ☐ **Allow merge commits**
  - Reason: Prefer squash for cleaner history
- ☑ **Allow squash merging** (Default)
  - ☑ **Default to pull request title and commit details**
- ☑ **Allow rebase merging**
- ☑ **Always suggest updating pull request branches**
- ☑ **Allow auto-merge**
- ☑ **Automatically delete head branches**

### Archives

- ☐ **Include Git LFS objects in archives** (unless using LFS)

### Pushes

- ☐ **Limit how many branches and tags can be updated in a single push**: Leave at default (5)

---

## 3. Security Settings

Navigate to: **Settings → Code security and analysis**

### Dependency Graph

- ☑ **Dependency graph**
  - Automatically enabled for public repositories

### Dependabot

- ☑ **Dependabot alerts**
  - Sends alerts for vulnerable dependencies
- ☑ **Dependabot security updates**
  - Automatically creates PRs to fix vulnerabilities
- ☑ **Grouped security updates** (if available)

**Note**: Dependabot version updates are already configured in `.github/dependabot.yml`

### Code Scanning

- ☑ **CodeQL analysis**
  - Click "Set up" → "Default" (or use existing `.github/workflows/security.yml`)
  - Languages: Python
  - Query suites: Default + Security extended

### Secret Scanning

- ☑ **Secret scanning**
  - Scans for exposed secrets
- ☑ **Push protection**
  - **Critical**: Prevents pushing commits with secrets
- ☑ **Validity checks** (if available)
- ☑ **Non-provider patterns** (if available)

### Private Vulnerability Reporting

- ☑ **Enable private vulnerability reporting**
  - Allows security researchers to report vulnerabilities privately
  - Already configured in `SECURITY.md`

---

## 4. Actions & Automation

Navigate to: **Settings → Actions → General**

### Actions Permissions

- ☑ **Allow select actions and reusable workflows**
  - ☑ **Allow actions created by GitHub**
  - ☑ **Allow actions by Marketplace verified creators**
  - ☐ **Allow specified actions and reusable workflows**

### Workflow Permissions

- ☑ **Read repository contents and packages permissions**
  - Least privilege by default
- ☑ **Allow GitHub Actions to create and approve pull requests**
  - Required for Dependabot and automated PRs

### Fork Pull Request Workflows

- ☑ **Require approval for first-time contributors**
  - Security measure for fork PRs
- ☐ **Require approval for all outside collaborators**

### Workflow Run Approval

- ☑ **Require approval for fork pull request workflows from outside collaborators**

---

## 5. Environments

Navigate to: **Settings → Environments → New environment**

### Create `pypi` Environment

1. Click "New environment"
2. **Name**: `pypi`
3. **Deployment protection rules**:
   - ☑ **Required reviewers**: Add yourself (allenjd) as reviewer
   - ☑ **Wait timer**: 0 minutes
   - ☑ **Deployment branches and tags**: Selected branches and tags only
     - Add rule: `main` branch only
     - Add rule: `v*` tags only
4. **Environment secrets**:
   - Add secret: `PYPI_API_TOKEN`
     - Value: Your PyPI API token (if not using Trusted Publishing)
     - **Note**: For Trusted Publishing (OIDC), no token needed - configure on PyPI instead

**Trusted Publishing Setup (Recommended)**:

1. Go to https://pypi.org/manage/account/publishing/
2. Add a new publisher:
   - **PyPI Project Name**: `tracekit`
   - **Owner**: `lair-click-bats` (or your org)
   - **Repository name**: `tracekit`
   - **Workflow name**: `release.yml`
   - **Environment name**: `pypi`

---

## 6. Tag Protection

Navigate to: **Settings → Tags → New rule**

### Create Tag Protection Rule

1. Click "New rule"
2. **Tag name pattern**: `v*`
3. ☑ **Add tag protection rule**

This prevents unauthorized tag creation and deletion.

**Additional Configuration** (if available):

- ☑ **Restrict who can create matching tags**
  - Add: Repository maintainers only

---

## 7. Repository Labels

Navigate to: **Issues → Labels**

The following labels should already exist. If not, create them:

### Bug Tracking

| Label          | Color     | Description                    |
| -------------- | --------- | ------------------------------ |
| `bug`          | `#d73a4a` | Something isn't working        |
| `needs-triage` | `#ffffff` | Needs initial review           |
| `confirmed`    | `#0e8a16` | Bug confirmed and reproducible |
| `wontfix`      | `#666666` | Will not be fixed              |

### Features & Enhancements

| Label              | Color     | Description                   |
| ------------------ | --------- | ----------------------------- |
| `enhancement`      | `#a2eeef` | New feature or request        |
| `good first issue` | `#7057ff` | Good for newcomers            |
| `help wanted`      | `#008672` | Extra attention needed        |
| `question`         | `#d876e3` | Further information requested |

### Documentation

| Label           | Color     | Description                |
| --------------- | --------- | -------------------------- |
| `documentation` | `#0075ca` | Documentation improvements |
| `examples`      | `#0075ca` | Example code or tutorials  |

### Dependencies & CI

| Label            | Color     | Description               |
| ---------------- | --------- | ------------------------- |
| `dependencies`   | `#0366d6` | Dependency updates        |
| `python`         | `#3572A5` | Python dependency updates |
| `github-actions` | `#000000` | GitHub Actions updates    |
| `ci`             | `#000000` | CI/CD pipeline changes    |

### Security

| Label           | Color     | Description             |
| --------------- | --------- | ----------------------- |
| `security`      | `#b60205` | Security-related issues |
| `vulnerability` | `#b60205` | Security vulnerability  |

### Priority

| Label                | Color     | Description       |
| -------------------- | --------- | ----------------- |
| `priority: critical` | `#b60205` | Critical priority |
| `priority: high`     | `#d93f0b` | High priority     |
| `priority: medium`   | `#fbca04` | Medium priority   |
| `priority: low`      | `#0e8a16` | Low priority      |

### Breaking Changes

| Label      | Color     | Description                     |
| ---------- | --------- | ------------------------------- |
| `breaking` | `#b60205` | Breaking changes (semver major) |

---

## 8. Repository Topics

Navigate to: **Repository home page → ⚙️ (gear icon) next to About**

Add the following topics:

```
python
signal-integrity
waveform-analysis
test-automation
hardware-testing
oscilloscope
measurement
debugging
developer-tools
observability
ieee-181
jedec
high-speed-digital
```

**How to add**:

1. Click the gear icon ⚙️ next to "About" on the main repo page
2. In the "Topics" field, add topics separated by spaces or commas
3. Topics will auto-suggest as you type
4. Click "Save changes"

---

## 9. Social Preview

Navigate to: **Settings → General → Social Preview**

**Create a social preview image** (1280x640px recommended):

1. Click "Upload an image"
2. Use a preview image showing:
   - TraceKit logo
   - Tagline: "Python library for signal integrity analysis"
   - Key features or example waveform
3. This image appears when sharing the repo on social media

---

## Verification Checklist

After completing the setup, verify:

### Branch Protection

- [ ] Navigate to `main` branch and try to push directly (should be blocked)
- [ ] Create a test PR and verify:
  - [ ] At least 1 approval required
  - [ ] Status checks must pass
  - [ ] Conversations must be resolved
  - [ ] Force push disabled

### Security

- [ ] Visit **Security → Dependabot** and verify alerts are enabled
- [ ] Visit **Security → Code scanning** and verify CodeQL is running
- [ ] Visit **Security → Secret scanning** and verify it's enabled
- [ ] Try to push a test secret (should be blocked by push protection)

### Actions

- [ ] Visit **Actions** tab and verify workflows are visible
- [ ] Check that fork PR workflows require approval
- [ ] Verify `pypi` environment appears in **Settings → Environments**

### Tags

- [ ] Try to create a tag `v9.9.9` manually (should require proper permissions)
- [ ] Verify `v*` pattern is protected

### Release Process

- [ ] Create a test branch
- [ ] Open a PR and verify:
  - [ ] PR template appears with all sections
  - [ ] Required status checks are listed
  - [ ] At least 1 approval needed
- [ ] Test the release workflow:
  - [ ] Tag a test version (or use workflow_dispatch)
  - [ ] Verify GitHub release is created
  - [ ] Verify PyPI publish works (if configured)

---

## Post-Setup Recommendations

### 1. Enable Repository Rulesets (Beta)

GitHub is migrating to "Rulesets" as a more powerful alternative to branch protection. Once generally available:

- Navigate to **Settings → Rules → Rulesets**
- Create a ruleset that combines branch protection, tag protection, and push rules

### 2. Configure Status Checks

After your first CI run:

1. Go back to **Settings → Branches → Edit protection rule for `main`**
2. Under "Status checks", search for and add:
   - All test jobs
   - Lint jobs
   - Type checking jobs
   - Security scanning jobs

### 3. Set Up Webhooks (Optional)

If integrating with external services:

- Navigate to **Settings → Webhooks**
- Add webhooks for CI/CD, notifications, or monitoring services

### 4. Configure Notifications

- **Settings → Notifications**
  - Watch: All activity
  - Subscribe to: Releases only (for users)

### 5. Enable Discussions Categories

- Navigate to **Discussions** tab
- Configure categories:
  - Announcements
  - Q&A
  - Show and Tell
  - Feature Requests

---

## Troubleshooting

### Status Checks Not Appearing

**Problem**: Required status checks don't appear in the dropdown

**Solution**:

1. Run your CI workflow at least once on the `main` branch
2. Wait for the workflow to complete
3. Refresh the branch protection settings page
4. The status checks should now appear

### Unable to Push to Main

**Problem**: Accidentally locked yourself out

**Solution**:

1. Go to **Settings → Branches → Edit protection for `main`**
2. Temporarily disable "Include administrators"
3. Make your change
4. Re-enable "Include administrators"

### Dependabot Not Creating PRs

**Problem**: Dependabot is enabled but no PRs

**Solution**:

1. Check `.github/dependabot.yml` is valid YAML
2. Verify the schedule hasn't passed (it runs weekly on Monday)
3. Manually trigger: **Insights → Dependency graph → Dependabot → Check for updates**

### Release Workflow Failing

**Problem**: Release workflow fails to publish to PyPI

**Solution**:

1. Verify `pypi` environment exists
2. Check that `PYPI_API_TOKEN` is set (or Trusted Publishing configured)
3. Verify the `release.yml` workflow has correct environment name
4. Check PyPI API token permissions (should allow uploads)

---

## References

- [GitHub Branch Protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Environments](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
- [Dependabot Configuration](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file)
- [CodeQL Setup](https://docs.github.com/en/code-security/code-scanning/automatically-scanning-your-code-for-vulnerabilities-and-errors/configuring-code-scanning)
- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)

---

## Support

If you encounter issues with this setup:

1. Check the [GitHub Documentation](https://docs.github.com)
2. Open a discussion in the repository
3. Contact the maintainer: @lair-click-bats

---

**Setup Date**: 2026-01-07
**TraceKit Version**: v0.1.0
**Last Updated**: 2026-01-07
