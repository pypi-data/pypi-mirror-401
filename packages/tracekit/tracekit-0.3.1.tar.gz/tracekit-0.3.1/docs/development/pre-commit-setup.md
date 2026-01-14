# Pre-Commit Hooks Setup

This document explains the pre-commit hook configuration for TraceKit and how to use it effectively.

## Overview

Pre-commit hooks automatically run quality checks **before each commit**, catching issues early and maintaining code quality. This prevents polluting the git history with "fix linting" commits and provides instant feedback.

## Installation

Pre-commit is already configured as a dev dependency. Set it up once:

```bash
# Install dependencies (includes pre-commit)
uv sync --all-extras

# Install git hooks
uv run pre-commit install

# Verify installation
uv run pre-commit --version
```

## What Gets Checked

### Automatic (Fast Checks - Run on Every Commit)

| Hook                    | What It Does                    | Auto-Fix            |
| ----------------------- | ------------------------------- | ------------------- |
| **check-yaml**          | Validate YAML syntax            | No                  |
| **check-json**          | Validate JSON syntax            | No                  |
| **check-toml**          | Validate TOML syntax            | No                  |
| **fix-end-of-files**    | Ensure files end with newline   | Yes                 |
| **trailing-whitespace** | Remove trailing whitespace      | Yes                 |
| **mixed-line-ending**   | Enforce LF line endings         | Yes                 |
| **detect-private-key**  | Prevent committing secrets      | No                  |
| **ruff check**          | Lint Python code                | Yes (when possible) |
| **ruff format**         | Format Python code              | Yes                 |
| **interrogate**         | Check docstring coverage (≥98%) | No                  |
| **shellcheck**          | Lint shell scripts              | No                  |
| **yamllint**            | Lint YAML files                 | No                  |
| **markdownlint**        | Lint Markdown files             | Yes                 |

### On-Demand (Slower Checks - Run Manually)

These tools are available but run in CI, not on every commit:

- **pydocstyle**: Docstring style checking (283 violations to fix)
- **vulture**: Dead code detection (32 items found)
- **radon**: Complexity analysis (355 functions need review)
- **mypy**: Type checking

## Usage

### Normal Commits (Hooks Run Automatically)

```bash
# Make changes
vim src/tracekit/myfile.py

# Stage changes
git add src/tracekit/myfile.py

# Commit (hooks run automatically)
git commit -m "feat: add new feature"

# If hooks fail:
# - Auto-fixable issues (formatting) are fixed automatically
# - You'll see what needs manual fixing
# - Fix issues and try again
```

### Skipping Hooks (Emergency/WIP Only)

```bash
# Skip hooks for work-in-progress commits
git commit --no-verify -m "WIP: temporary work"

# ⚠️ WARNING: Only use --no-verify for:
# - WIP commits on feature branches
# - Emergency hotfixes (but run hooks before pushing!)
# Never use --no-verify on commits to main branch!
```

### Running Hooks Manually

```bash
# Run all hooks on all files
uv run pre-commit run --all-files

# Run specific hook
uv run pre-commit run ruff --all-files
uv run pre-commit run interrogate --all-files

# Run on specific files
uv run pre-commit run --files src/tracekit/myfile.py

# Update hook versions
uv run pre-commit autoupdate
```

## Hook Behavior

### Auto-Fix Hooks

These hooks **automatically fix** issues:

- `ruff format` - Formats code
- `ruff check --fix` - Fixes simple linting issues
- `trailing-whitespace` - Removes trailing spaces
- `end-of-file-fixer` - Adds newline at EOF
- `markdownlint` - Fixes Markdown formatting

**What happens:**

1. You commit
2. Hook finds issues and fixes them
3. Commit is blocked
4. You see: `Files were modified by this hook`
5. You run `git add .` to stage fixes
6. You commit again (now passes)

### Validation Hooks

These hooks **check but don't fix**:

- `interrogate` - Docstring coverage must be ≥98%
- `shellcheck` - Shell script issues
- `yamllint` - YAML formatting issues
- `detect-private-key` - Security check

**What happens:**

1. You commit
2. Hook finds issues
3. Commit is blocked with error message
4. You manually fix issues
5. You commit again

## Common Scenarios

### Scenario 1: Formatting Issues

```bash
git commit -m "feat: new feature"

# Output:
# ruff format..........Failed
# - files were modified by this hook

# Fix: Re-stage and commit
git add .
git commit -m "feat: new feature"
# ✓ Now passes
```

### Scenario 2: Docstring Coverage Below 98%

```bash
git commit -m "feat: add function without docstring"

# Output:
# interrogate..........Failed
# - RESULT: FAILED (minimum: 98.0%, actual: 97.8%)

# Fix: Add docstring to new code
vim src/tracekit/myfile.py  # Add docstring
git add src/tracekit/myfile.py
git commit -m "feat: add function with docstring"
# ✓ Now passes
```

### Scenario 3: Linting Errors

```bash
git commit -m "feat: add code with issues"

# Output:
# ruff.................Failed
# src/tracekit/myfile.py:10:5: F841 Local variable 'x' is assigned but never used

# Fix: Remove unused variable
vim src/tracekit/myfile.py  # Fix issue
git add src/tracekit/myfile.py
git commit -m "feat: add clean code"
# ✓ Now passes
```

## CI Integration

Pre-commit hooks run **twice** for safety:

1. **Local (your machine)**: Before commit (instant feedback)
2. **CI (GitHub)**: On push (safety net)

If hooks pass locally, they'll pass in CI. This ensures:

- No surprises after pushing
- Fast feedback loop
- Clean git history

## Configuration Files

### `.pre-commit-config.yaml`

Main configuration file defining all hooks:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.14.11
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: https://github.com/econchick/interrogate
    rev: 1.7.0
    hooks:
      - id: interrogate
        args: [--fail-under=98, --verbose, --quiet, --color]
        exclude: ^(tests|examples|scripts)/
```

### `pyproject.toml`

Tool-specific configurations:

```toml
[tool.interrogate]
fail-under = 98
exclude = ["tests", "examples", "scripts"]

[tool.ruff]
line-length = 100
target-version = "py312"
```

## Troubleshooting

### Hooks Not Running

```bash
# Check if installed
ls -la .git/hooks/pre-commit

# Reinstall
uv run pre-commit install

# Verify
uv run pre-commit run --all-files
```

### Hooks Taking Too Long

```bash
# Skip slow hooks temporarily
SKIP=interrogate git commit -m "WIP: quick commit"

# Or disable temporarily
uv run pre-commit uninstall
# ...do your work...
uv run pre-commit install
```

### Node.js Version Issues (markdownlint)

If you see `Unsupported engine` errors:

```bash
# Check Node version
node --version

# markdownlint requires Node.js >= 18
# If you have an older version, skip markdownlint:
SKIP=markdownlint git commit -m "your message"
```

### Cache Issues

```bash
# Clear pre-commit cache
uv run pre-commit clean

# Reinstall environments
uv run pre-commit install-hooks
```

## Best Practices

### DO ✅

- Run hooks on every commit (keep them enabled)
- Fix issues locally before pushing
- Add docstrings to all new code
- Keep commits small and focused
- Run `pre-commit run --all-files` after pulling main

### DON'T ❌

- Don't use `--no-verify` except for WIP commits
- Don't commit with failing hooks to main branch
- Don't disable hooks permanently
- Don't commit large generated files
- Don't bypass docstring coverage checks

## Quality Metrics

Current codebase health:

| Metric                 | Status         | Threshold        |
| ---------------------- | -------------- | ---------------- |
| **Docstring Coverage** | 98.3%          | ≥ 98% ✅         |
| **Docstring Style**    | 283 violations | Informational ⚠️ |
| **Dead Code**          | 32 items       | Informational ⚠️ |
| **High Complexity**    | 355 functions  | Informational ⚠️ |

Pre-commit enforces:

- ✅ Docstring coverage (REQUIRED - blocks commits)
- ✅ Code formatting (auto-fixes)
- ✅ Basic linting (auto-fixes when possible)

CI monitors (informational):

- ⚠️ Docstring style violations
- ⚠️ Dead code
- ⚠️ Complexity metrics

## Getting Help

If you encounter issues:

1. Check this documentation
2. Run `uv run pre-commit run --all-files --verbose`
3. Check `.pre-commit-config.yaml` for hook configuration
4. Check `pyproject.toml` for tool settings
5. Ask in GitHub Discussions

## References

- [Pre-commit Documentation](https://pre-commit.com/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Interrogate Documentation](https://interrogate.readthedocs.io/)
- TraceKit Coding Standards: `.claude/coding-standards.yaml`
- Contributing Guide: `CONTRIBUTING.md`
