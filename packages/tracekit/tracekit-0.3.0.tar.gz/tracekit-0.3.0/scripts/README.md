# Scripts Reference

Development automation scripts for the TraceKit project.

## Quick Reference

| Script      | Purpose                                     | When to Use                               |
| ----------- | ------------------------------------------- | ----------------------------------------- |
| `check.sh`  | Quick quality check (lint + format --check) | Before commits, after significant changes |
| `lint.sh`   | Run all configured linters                  | When checking for issues                  |
| `format.sh` | Format all code files                       | When formatting is needed                 |
| `clean.sh`  | Clean build artifacts and caches            | When builds are stale                     |
| `doctor.sh` | Environment health check                    | When tools seem broken                    |
| `fix.sh`    | Auto-fix common issues                      | After lint failures                       |
| `test.sh`   | **Full test suite (recommended)**           | **Before releases, in CI pipelines**      |

## Directory Structure

```
scripts/
  lib/              # Shared shell function library
  tools/            # Individual linting/formatting tool wrappers
  *.sh              # Core workflow scripts
  *.py              # Python automation scripts
```

## Quality Scripts

### check.sh

Quick quality check combining lint and format verification.

```bash
./scripts/check.sh           # Run all checks
./scripts/check.sh --json    # Machine-readable output
./scripts/check.sh -v        # Verbose output
```

### lint.sh

Run all linters across the codebase.

```bash
./scripts/lint.sh            # Run all linters
./scripts/lint.sh --json     # JSON output
./scripts/lint.sh -v         # Verbose output
./scripts/lint.sh --python   # Python only
./scripts/lint.sh --shell    # Shell only
```

### format.sh

Run all formatters.

```bash
./scripts/format.sh          # Format all files
./scripts/format.sh --check  # Check only, don't modify
./scripts/format.sh --json   # JSON output
```

### fix.sh

Auto-fix common issues.

```bash
./scripts/fix.sh             # Auto-fix all files
./scripts/fix.sh --json      # JSON output
./scripts/fix.sh -v          # Verbose output
```

### doctor.sh

Check development environment setup.

```bash
./scripts/doctor.sh          # Check tool availability
./scripts/doctor.sh -v       # Verbose output
./scripts/doctor.sh --json   # Machine-readable output
```

Checks:

- Core tools (git, bash)
- Python tools (python3, uv, ruff, mypy)
- JS tools (node, npm, prettier, markdownlint)
- Shell tools (shellcheck, shfmt)
- YAML tools (yamllint)
- Configuration files presence

## Clean Scripts

### clean.sh

**`clean.sh`** removes:

- Python caches (`__pycache__`, `.mypy_cache`, `.pytest_cache`)
- Build artifacts (`dist/`, `build/`, `*.egg-info`)
- Coverage data (`.coverage`, `htmlcov/`)
- Editor backup files (`*.bak`, `*~`, `*.swp`, `*.swo`)
- With `--all`: virtual environments and `node_modules`

## Test Scripts

| Script    | Purpose                                                           | Speed   |
| --------- | ----------------------------------------------------------------- | ------- |
| `test.sh` | **RECOMMENDED** - Optimized parallel test execution with coverage | ~10 min |

### Optimized Test Execution

The `test.sh` script provides the **fastest, most reliable** way to run tests:

```bash
# RECOMMENDED: Full test suite with coverage (~10 minutes)
./scripts/test.sh

# Quick test without coverage (~5-7 minutes)
./scripts/test.sh --fast

# With specific options
./scripts/test.sh --verbose     # Verbose output
./scripts/test.sh --parallel 4  # Use 4 workers
```

**Key Features**:

- Auto-detects optimal worker count
- Configurable timeouts
- Generates coverage reports
- Full coverage report in `htmlcov/index.html`

### Coverage

For memory-safe coverage runs on large test suites:

```bash
./scripts/run_coverage.sh              # Run all batches
./scripts/run_coverage.sh --batch 1    # Run specific batch only
./scripts/run_coverage.sh --quick      # Run quick subset for CI
```

## Tool Wrappers

Located in `scripts/tools/`:

### Python Tools

| Script    | Tool | Purpose               |
| --------- | ---- | --------------------- |
| `ruff.sh` | Ruff | Python linting/format |
| `mypy.sh` | Mypy | Python type checking  |

### Universal Tools

| Script            | Tool         | Purpose                 |
| ----------------- | ------------ | ----------------------- |
| `markdownlint.sh` | markdownlint | Markdown linting        |
| `prettier.sh`     | Prettier     | Multi-format formatting |
| `shellcheck.sh`   | ShellCheck   | Shell script linting    |
| `shfmt.sh`        | shfmt        | Shell script formatting |
| `yamllint.sh`     | yamllint     | YAML linting            |
| `jsonc.sh`        | Custom       | JSON/JSONC validation   |
| `xmllint.sh`      | xmllint      | XML validation          |

### Other Tool Scripts

| Script                 | Purpose                               |
| ---------------------- | ------------------------------------- |
| `check_links.sh`       | Check broken links in documentation   |
| `vscode_extensions.sh` | Verify recommended VS Code extensions |

## Test Data Scripts

Located in `scripts/`:

### Test Data Generation Scripts

| Script                                | Purpose                                                          |
| ------------------------------------- | ---------------------------------------------------------------- |
| `generate_comprehensive_test_data.py` | **RECOMMENDED** - Complete test data for all 14 analysis domains |
| `generate_synthetic_wfm.py`           | Generate synthetic Tektronix WFM files with custom parameters    |
| `generate_all_reports.py`             | Generate analysis reports from existing test data files          |

### Utility Scripts

| Script                          | Purpose                        |
| ------------------------------- | ------------------------------ |
| `categorize_wfm_files.py`       | Categorize WFM files           |
| `prepare_real_captures.py`      | Prepare real capture data      |
| `verify_synthetic_test_data.py` | Verify synthetic test data     |
| `download_test_data.sh`         | Download test data from remote |
| `validate_test_markers.py`      | Validate pytest markers        |

### Usage Examples

```bash
# Generate comprehensive test suite (RECOMMENDED)
uv run python scripts/generate_comprehensive_test_data.py test_data/comprehensive/

# Generate custom WFM file
python scripts/generate_synthetic_wfm.py --signal sine --frequency 10000 --output test.wfm

# Generate all reports from test data
python scripts/generate_all_reports.py
```

## Common Library

`scripts/lib/common.sh` provides shared functions:

### Color Output

- `print_header "text"` - Blue header box
- `print_section "text"` - Section heading
- `print_tool "text"` - Tool name display
- `print_pass "text"` - Green checkmark
- `print_fail "text"` - Red X mark
- `print_skip "text"` - Yellow skip marker
- `print_info "text"` - Info message

### Tool Detection

- `has_tool "name"` - Check if tool exists
- `require_tool "name" "install hint"` - Check tool, show hint if missing
- `has_uv` - Check if uv is available
- `run_py_tool "args"` - Run Python tool via uv

### Counter Management

- `reset_counters` - Reset all counters
- `increment_passed` - Increment passed counter
- `increment_failed` - Increment failed counter
- `increment_skipped` - Increment skipped counter

### JSON Output

- `enable_json` - Switch to JSON output mode
- `is_json_mode` - Check if JSON mode is enabled
- `json_result tool status message` - Output JSON object

### Configuration

- `find_config "filename"` - Find config file (check current dir, then repo root)

## Environment Variables

| Variable      | Purpose                         |
| ------------- | ------------------------------- |
| `REPO_ROOT`   | Repository root (auto-detected) |
| `JSON_OUTPUT` | Enable JSON mode                |

## Exit Codes

| Code | Meaning                         |
| ---- | ------------------------------- |
| 0    | Success (or gracefully skipped) |
| 1    | Failures found                  |
| 2    | Tool/configuration error        |

## Usage Examples

```bash
# Quick check before commit
./scripts/check.sh

# Fix all auto-fixable issues
./scripts/fix.sh

# Diagnose setup problems
./scripts/doctor.sh

# Clean everything including caches
./scripts/clean.sh --all

# Run tests with parallel execution (recommended)
./scripts/test.sh

# Quick test without coverage
./scripts/test.sh --fast

# Check dependencies
./scripts/check_dependencies.sh -v
```

## Best Practices

1. **Always use `uv run`** for Python scripts
2. **Source `lib/common.sh`** for consistent output in shell scripts
3. **Support `--json` flag** for CI/automation
4. **Exit codes**: 0 = success, 1 = failure, 2 = bad arguments
5. **Use absolute paths** when called from different directories
6. **Add `# shellcheck source=` directive** when sourcing files
7. **Use `${var}` style** for all variable references (consistent quoting)
8. **Use 2-space indentation** for shell scripts (per .editorconfig)

## Adding New Scripts

1. Place in appropriate subdirectory
2. Add executable bit: `chmod +x script.sh`
3. Source `lib/common.sh` for shell scripts
4. Add `# shellcheck source=lib/common.sh` directive
5. Use 2-space indentation
6. Add entry to this README
7. Use conventional commit when adding: `feat(scripts): add new-script.sh`

## Integration

### Pre-commit

Scripts are invoked by pre-commit hooks defined in `.pre-commit-config.yaml`.

### CI

The `check.sh` script runs in CI via `.github/workflows/ci.yml`.

### Claude Code

Scripts are referenced in `CLAUDE.md` for quality workflows.
