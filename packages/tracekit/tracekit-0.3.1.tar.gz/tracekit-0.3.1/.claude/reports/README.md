# Claude Code Reports

This directory contains **temporary** analysis reports, summaries, and assessments generated during Claude Code orchestration sessions.

## Purpose

- **Temporary workspace** for analysis documents
- **NOT version controlled** (git-ignored)
- **Auto-archived** after retention period
- **Organized separate** from main project structure

## What Goes Here

### ✅ Temporary Analysis Documents

- Phase assessment reports
- Orchestration analysis summaries
- Code audit reports
- Architecture analysis
- Performance assessments
- Testing reports
- Workflow summaries

### ❌ What Does NOT Go Here

- Permanent project documentation → `docs/`
- User-facing guides → `docs/guides/`
- API documentation → `docs/api/`
- Architecture docs (permanent) → `docs/architecture/`

## Retention Policy

Reports are automatically archived/deleted based on `.claude/config.yaml`:

```yaml
retention:
  reports: 7 # Days before archiving
  reports_archive: 30 # Days in archive before deletion
```

## File Naming Convention

Use ISO date prefix for chronological organization:

```
YYYY-MM-DD-description.md              # General reports
YYYY-MM-DD-SUMMARY-topic.md            # Summary documents
YYYY-MM-DD-ASSESSMENT-area.md          # Assessment reports
YYYY-MM-DD-ANALYSIS-component.md       # Analysis documents
```

**Examples**:

- `2026-01-09-orchestration-analysis.md`
- `2026-01-09-SUMMARY-phase-2-improvements.md`
- `2026-01-09-ASSESSMENT-code-quality.md`

## Lifecycle

1. **Generation**: Agent creates report in this directory
2. **Review**: User reviews during session
3. **Archive**: After 7 days → `.claude/reports/archive/`
4. **Deletion**: After 30 days in archive → removed

## Moving Existing Reports

If you have reports in project root, move them here:

```bash
# Move reports to proper location
mv *REPORT*.md .claude/reports/ 2>/dev/null
mv *SUMMARY*.md .claude/reports/ 2>/dev/null
mv *ASSESSMENT*.md .claude/reports/ 2>/dev/null
mv *ANALYSIS*.md .claude/reports/ 2>/dev/null

# Verify they're git-ignored
git status  # Should not show these files
```

## Version Control Policy

### ✅ Always Tracked (Essential Configuration & Documentation)

**Configuration files**:

- `.claude/config.yaml` - SSOT for all behavioral settings
- `.claude/paths.yaml` - Path definitions
- `.claude/project-metadata.yaml` - Project identity
- `.claude/coding-standards.yaml` - Code quality rules
- `.claude/orchestration-config.yaml` - Orchestration behavior

**Agent definitions**:

- All `.claude/agents/*.md` files - Agent behavior and routing

**Command documentation**:

- All `.claude/commands/*.md` files - Command usage guides

**Hooks**:

- All `.claude/hooks/*.py` files - Runtime enforcement hooks
- `.claude/hooks/shared/*.py` - Shared utilities

**Documentation**:

- All `README.md` files - Documentation
- All `.claude/*.md` guides - User documentation

### ❌ Never Tracked (Temporary Runtime State)

**Reports & analysis** (this directory):

- `.claude/reports/*.md` - Temporary analysis documents
- `.claude/reports/archive/` - Archived reports
- Exception: `.claude/reports/README.md` (tracked)

**Runtime state**:

- `.claude/agent-registry.json` - Agent tracking state
- `.claude/workflow-progress*.json` - Progress tracking
- `.claude/settings.local.json` - Local overrides

**Logs**:

- `.claude/hooks/*.log` - All log files
- `.claude/orchestration.log` - Activity log
- `.claude/hooks/orchestration-metrics.json` - Metrics

**Outputs**:

- `.claude/agent-outputs/*` - Agent outputs (except .gitkeep)
- `.claude/summaries/*` - Summaries (except .gitkeep)

**Coordination**:

- `.coordination/**` - All coordination state (except READMEs and .gitkeep)

### Why This Separation?

**Tracked files** = Essential for collaboration, system behavior, documentation
**Untracked files** = Temporary artifacts, runtime state, session-specific data

This ensures:

- Other contributors can access and use the orchestration system
- Temporary files don't pollute version control
- System configuration is consistent across environments
- Runtime state remains local to each session

## Do NOT Commit Reports

⚠️ **Files in this directory are temporary analysis artifacts and should NEVER be committed to version control.**

They are automatically git-ignored by `.gitignore`
