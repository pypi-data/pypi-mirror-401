# TraceKit Test Strategy

**Last Updated**: 2026-01-11
**Status**: Active
**Owner**: Test Infrastructure Team

---

## Table of Contents

1. [Overview](#overview)
2. [CI Workflow Architecture](#ci-workflow-architecture)
3. [Test Grouping Strategy](#test-grouping-strategy)
4. [Worker Configuration](#worker-configuration)
5. [Test Markers](#test-markers)
6. [Hypothesis Testing](#hypothesis-testing)
7. [Coverage Requirements](#coverage-requirements)
8. [Local Development](#local-development)
9. [Troubleshooting](#troubleshooting)

---

## Overview

TraceKit uses a **multi-tiered CI strategy** with four specialized workflows:

1. **ci.yml** - Primary gating (every PR)
2. **tests-chunked.yml** - Comprehensive nightly testing
3. **test-quality.yml** - Test health monitoring
4. **benchmarks.yml** - Performance tracking

This strategy balances **fast feedback** for PRs with **comprehensive coverage** via nightly runs.

---

## CI Workflow Architecture

### 1. ci.yml - Primary Gating Workflow

**Purpose**: Fast, comprehensive check for all PRs/pushes
**Runs**: Every push/PR to main/develop
**Duration**: ~25 minutes (8 groups × 2 Python versions)
**Fail Behavior**: Blocks PR merge

**Coverage**:

- All unit tests (8 coarse-grained groups)
- Integration tests
- Compliance tests
- Validation tests

**Test Groups**:

```yaml
- analyzers (all subdirectories)
- core-protocols-loaders
- search-filtering-streaming
- cli-ui-reporting
- unit-workflows
- unit-exploratory
- unit-utils
- non-unit-tests (integration/compliance/validation)
```

**Worker Configuration**:

- Memory-intensive groups (analyzers, non-unit): 2 workers
- Standard groups: 4 workers

**Why This Configuration?**
Provides fast feedback (<30 min) while testing all code paths. Coarse-grained grouping minimizes matrix job count.

---

### 2. tests-chunked.yml - Comprehensive Nightly Testing

**Purpose**: Thorough testing with stress/performance checks
**Runs**: Nightly at 2 AM UTC + manual dispatch
**Duration**: ~60 minutes (15 groups + stress + performance)
**Fail Behavior**: Creates issue, doesn't block

**Coverage**:

- All unit tests (15 fine-grained groups)
- Integration tests
- Validation tests
- Stress tests
- Performance tests

**Test Groups** (15 fine-grained):

```yaml
# Analyzer tests (6 groups, memory-intensive, 2 workers each)
- analyzers-digital
- analyzers-power-spectral
- analyzers-statistical-waveform
- analyzers-eye-jitter-packet
- analyzers-protocols-patterns
- analyzers-signal-integrity

# Core functionality (2 workers - I/O intensive)
- core-protocols-loaders-math

# Standard tests (4 workers)
- search-filtering-batch-streaming
- cli-ui-reporting-viz-export
- workflows-pipeline-session-integrations

# CPU-intensive (2 workers)
- inference-discovery-exploratory

# Fast tests (4 workers)
- utils-config-plugins-hooks
- api-dsl-schemas-optimization
- quality-testing-requirements-comparison
- component-jupyter-triggering
```

**Why This Configuration?**
Fine-grained grouping enables:

- Better memory management (analyzer tests isolated)
- Faster parallel execution
- Easier debugging (smaller test groups)
- Comprehensive coverage including stress/performance

**Trigger Changes (2026-01-11)**:
Removed push/PR triggers to eliminate redundancy with ci.yml. Now runs:

- Nightly at 2 AM UTC
- Manual dispatch
- Main branch merges (workflow file changes only)

---

### 3. test-quality.yml - Test Health Monitoring

**Purpose**: Maintain test suite quality
**Runs**: When tests/**change + weekly randomization
**Duration**: ~20 minutes
**Fail Behavior\*\*: Blocks PR if markers invalid

**Coverage**:

- Marker validation (all tests have required markers)
- Test isolation checks (tests don't depend on execution order)
- Randomized order testing (3 runs with different seeds)

**Why This Configuration?**
Catches test quality issues early:

- Missing markers
- Test order dependencies
- Flaky tests

---

### 4. benchmarks.yml - Performance Tracking

**Purpose**: Track performance metrics over time
**Runs**: Weekly + when performance tests change
**Duration**: ~30 minutes
**Fail Behavior**: Creates issue if regression detected

**Coverage**:

- tests/performance/ only
- Benchmark comparisons
- Performance regression detection

---

## Test Grouping Strategy

### Principles

1. **Memory-Intensive Groups Use 2 Workers**
   - Analyzer tests (large signals, FFT operations)
   - Loader tests (file I/O)
   - Inference tests (ML algorithms)

2. **Standard Groups Use 4 Workers**
   - Utils, config, schemas (fast unit tests)
   - UI, reporting, visualization
   - Workflows, pipeline

3. **Group Size Target: 20-40 test files per group**
   - Too small: Overhead from matrix jobs
   - Too large: Unbalanced execution times

### Test Group Mapping

#### Analyzer Tests (Memory-Intensive, 2 workers)

```
analyzers-digital/          → Digital signal analysis (edges, timing)
analyzers-power-spectral/   → Power analysis, FFT, spectrograms
analyzers-statistical-waveform/ → Statistical measures, waveform metrics
analyzers-eye-jitter-packet/ → Eye diagrams, jitter analysis, packet decoding
analyzers-protocols-patterns/ → Protocol analyzers, pattern detection
analyzers-signal-integrity/ → Signal integrity metrics
```

#### Core Tests (I/O-Intensive, 2 workers)

```
core-protocols-loaders-math/ → Core types, protocol decoders, file loaders, math utilities
```

#### Standard Tests (4 workers)

```
search-filtering-batch-streaming/ → Search algorithms, filters, batch processing
cli-ui-reporting-viz-export/ → CLI, UI, reports, visualizations, exporters
workflows-pipeline-session-integrations/ → Workflows, pipelines, sessions, integrations
```

#### CPU-Intensive Tests (2 workers)

```
inference-discovery-exploratory/ → Protocol inference, signal discovery, exploratory analysis
```

#### Fast Tests (4 workers)

```
utils-config-plugins-hooks/ → Utilities, configuration, plugin system
api-dsl-schemas-optimization/ → API, DSL interpreter, schemas, optimization
quality-testing-requirements-comparison/ → Quality metrics, testing utilities, comparison
component-jupyter-triggering/ → Component framework, Jupyter integration
```

---

## Worker Configuration

### Why Different Worker Counts?

**2 Workers** (Memory-Intensive):

- Prevents OOM errors on GitHub Actions runners (7GB RAM)
- Reduces parallel memory allocation
- Longer per-test time but safer

**4 Workers** (Standard/Fast):

- Maximizes parallelism for fast tests
- Reduces total execution time
- Safe for low-memory tests

### How to Choose Worker Count

```python
# Memory usage estimation per test
def choose_workers(test_group):
    if test_group in ['analyzers', 'loaders', 'inference']:
        return 2  # Each test may allocate 100-500MB
    elif test_group in ['utils', 'config', 'schemas']:
        return 4  # Each test allocates <50MB
    else:
        return 4  # Default to parallelism
```

### Pytest Configuration

All CI workflows use:

```bash
pytest -n <workers> --maxprocesses=<workers> --dist loadfile
```

- `-n <workers>`: Number of parallel workers
- `--maxprocesses=<workers>`: Limit spawned processes
- `--dist loadfile`: Group tests by file (better caching)

---

## Test Markers

### Required Markers

Every test must have a **level marker**:

```python
@pytest.mark.unit           # Fast, isolated, no I/O
@pytest.mark.integration    # Multiple components, file I/O
@pytest.mark.performance    # Performance benchmarks
@pytest.mark.stress         # High load, memory intensive
@pytest.mark.validation     # Ground truth validation
```

### Domain Markers

Domain markers help with filtering:

```python
@pytest.mark.analyzer       # Analyzer module
@pytest.mark.loader         # Loader module
@pytest.mark.protocol       # Protocol decoder
@pytest.mark.inference      # Protocol inference
```

### Resource Markers

```python
@pytest.mark.slow                  # Tests taking >1 second
@pytest.mark.memory_intensive      # Tests requiring >100MB
@pytest.mark.requires_data         # Tests requiring test_data/
```

### Marker Validation

Markers are validated by:

- **Pre-commit hook**: `pytest --strict-markers --collect-only`
- **CI**: `test-quality.yml` runs `scripts/validate_test_markers.py`

---

## Hypothesis Testing

### Configuration Profiles

TraceKit uses **Hypothesis** for property-based testing.

**Profiles** (defined in `tests/conftest.py`):

```python
# default: 100 examples, normal verbosity
# fast: 20 examples, 1s deadline (local dev)
# ci: 500 examples, 2s deadline, derandomize (CI)
# debug: 10 examples, verbose output
```

### CI Configuration

All CI workflows use `--hypothesis-profile=ci`:

```bash
pytest --hypothesis-profile=ci
```

**Why 500 examples?**

- Catches edge cases (scientific computing has many corner cases)
- 2s deadline sufficient for FFT, correlation, etc.
- derandomize=True ensures reproducible failures

### Local Development

```bash
# Fast development (20 examples)
pytest --hypothesis-profile=fast

# Production testing (500 examples)
pytest --hypothesis-profile=ci

# Debugging failures
pytest --hypothesis-profile=debug
```

---

## Coverage Requirements

### Aggregate Coverage: 80%

**Enforced by**: `pyproject.toml` + Codecov

```toml
[tool.coverage.report]
fail_under = 80
```

### How It Works

1. Each CI job runs tests with `--cov=src/tracekit`
2. Coverage reports uploaded to Codecov
3. Codecov aggregates coverage across all jobs
4. PR blocked if aggregate coverage <80%

### Individual Job Coverage

Individual jobs may fall below 80% (they test subsets), but **aggregate coverage must meet threshold**.

### Checking Coverage Locally

```bash
# Run all tests with coverage
pytest --cov=src/tracekit --cov-report=html

# Open coverage report
open htmlcov/index.html
```

---

## Local Development

### Running Tests

```bash
# All unit tests
pytest tests/unit -v

# Specific module
pytest tests/unit/analyzers/digital/ -v

# With coverage
pytest tests/unit --cov=src/tracekit --cov-report=term-missing

# Fast mode (skip slow tests)
pytest tests/unit -m "unit and not slow" -v

# With parallelism (4 workers)
pytest tests/unit -n 4 --dist loadfile
```

### Pre-Commit Checks

```bash
# Run all pre-commit hooks
pre-commit run --all-files

# Run specific hook
pre-commit run pytest-smoke-test
```

### Quality Checks

```bash
# Run all checks (lint, format, type, test)
./scripts/check.sh

# Format code
./scripts/format.sh

# Validate test markers
python scripts/validate_test_markers.py
```

---

## Troubleshooting

### Test Failures

**Random test failures**:

```bash
# Get the failing seed
pytest --randomly-seed=1234567890

# Re-run with same seed
pytest --randomly-seed=1234567890
```

**Test order dependencies**:

```bash
# Check isolation (run twice in different orders)
pytest tests/unit/path/to/test.py
pytest tests/unit/path/to/test.py --randomly-seed=different
```

**OOM errors**:

```bash
# Reduce worker count
pytest tests/unit/analyzers/ -n 2

# Run sequentially
pytest tests/unit/analyzers/
```

### CI Failures

**Which workflow failed?**

- **ci.yml**: Blocking issue, fix immediately
- **tests-chunked.yml**: Investigate, may be flaky
- **test-quality.yml**: Test quality issue (markers, isolation)
- **benchmarks.yml**: Performance regression

**Debugging CI-specific failures**:

```bash
# Simulate CI environment
pytest --hypothesis-profile=ci -n 4 --dist loadfile --maxfail=10

# Check if it's a concurrency issue
pytest tests/unit -n 1  # Sequential
pytest tests/unit -n 4  # Parallel
```

### Coverage Issues

**Coverage dropped below 80%**:

1. Check Codecov report for missing lines
2. Add tests for uncovered code
3. Use `# pragma: no cover` for unreachable code

**False coverage failures**:

- Codecov may report spurious failures
- Check individual job coverage reports
- Verify aggregate coverage calculation

---

## Quick Reference

### Test Commands

```bash
# Development (fast)
pytest tests/unit -m "not slow" -n 4

# Pre-commit (smoke test)
pytest tests/unit/core/test_types.py -x --strict-markers -q

# CI simulation
pytest tests/unit -m "unit and not slow" -n 4 --hypothesis-profile=ci --maxfail=10

# Comprehensive (all tests)
pytest tests/ -v
```

### Workflow Triggers

| Workflow          | Trigger                          | Purpose               |
| ----------------- | -------------------------------- | --------------------- |
| ci.yml            | push/PR to main/develop          | Gate PRs              |
| tests-chunked.yml | Nightly 2AM UTC                  | Comprehensive testing |
| test-quality.yml  | tests/\*\* changes, weekly       | Test health           |
| benchmarks.yml    | performance/\*\* changes, weekly | Performance tracking  |

### Worker Configuration

| Test Type    | Workers | Reason                                |
| ------------ | ------- | ------------------------------------- |
| Analyzers    | 2       | Memory-intensive (large signals, FFT) |
| Loaders      | 2       | I/O-intensive (file operations)       |
| Inference    | 2       | CPU/memory-intensive (ML algorithms)  |
| Utils/Config | 4       | Fast, low memory                      |
| UI/Reporting | 4       | Standard                              |

---

## See Also

- Test Fixtures - See `tests/conftest.py` for available fixtures
- Hypothesis Testing - See `tests/conftest.py` for profile configuration
- Writing Tests - See `CONTRIBUTING.md` in repository root
- CI/CD Configuration - See `.github/workflows/` directory
