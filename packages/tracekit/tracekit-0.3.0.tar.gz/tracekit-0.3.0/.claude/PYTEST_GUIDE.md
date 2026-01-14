# TraceKit Pytest Testing Guide

**Status**: AUTHORITATIVE - Single Source of Truth for Test Execution

## TL;DR - Quick Commands

```bash
# Development: Test single module (RECOMMENDED)
uv run pytest tests/unit/{module} -v --tb=short

# CI/CD: Run all tests safely (use optimized test runner)
scripts/test.sh

# Coverage: Measure module coverage
uv run pytest tests/unit/{module} --cov=src/tracekit/{module} --cov-report=term-missing

# With markers
uv run pytest -m "unit and loader" -v

# Using test utilities
from tests.utils import SignalFactory, PacketFactory
```

## Quick Start (New Contributors)

### Running Tests

```bash
# Single module (RECOMMENDED)
uv run pytest tests/unit/loaders -v --tb=short

# With markers
uv run pytest -m "unit and loader" -v

# Exclude slow tests
uv run pytest -m "not slow" -v

# Specific test file
uv run pytest tests/unit/loaders/test_binary.py -v
```

### Test Organization

- `tests/unit/` - Unit tests (fast, isolated)
- `tests/integration/` - Integration tests
- `tests/compliance/` - Standards compliance (IEEE/JEDEC)
- `tests/performance/` - Performance benchmarks
- `tests/validation/` - Ground truth validation
- `tests/utils/` - Shared test utilities

### Using Test Utilities

```python
from tests.utils import SignalFactory, PacketFactory, mock_optional_module

def test_signal_processing(signal_factory):
    signal, metadata = signal_factory(signal_type="sine", frequency=1000)
    # ... test code

def test_with_mock():
    with mock_optional_module('rigol_wfm', Mock()):
        # ... test code
```

## Test Suite Overview

- **Full Runtime**: 15-20 minutes (if batched correctly)
- **Largest Module**: analyzers (8-10 min)
- **Critical Constraint**: Individual pytest runs >10min will timeout

## Critical Rules

### DO

- Test modules individually: `pytest tests/unit/{module}`
- Use timeouts: `--timeout=90` or `--timeout=180` for large modules
- Batch large test runs: See Strategy 2 below
- Exclude problem tests: `--ignore=tests/unit/search/test_performance.py`

### DO NOT

- Run full suite with single command: `pytest tests/` (WILL TIMEOUT)
- Run without timeout limits (hangs can crash terminal)
- Include `test_performance.py` in coverage runs (hangs indefinitely)
- Run coverage on full suite without batching

## Optimal Strategies

### Strategy 1: Module-by-Module (Development)

**Best for**: Daily development, debugging, targeted testing

```bash
# Test single module
uv run pytest tests/unit/analyzers -v --tb=short --timeout=180

# With coverage
uv run pytest tests/unit/inference \
  --cov=src/tracekit/inference \
  --cov-report=term-missing \
  --timeout=90
```

**Execution Time**: 30s - 10min per module
**Memory Usage**: Low (<500MB)
**Risk**: None

### Strategy 2: Batched Execution (CI/CD)

**Best for**: Full validation, coverage measurement, releases

```bash
# Batch 1: Large modules (sequential, 180s timeout each)
uv run pytest tests/unit/analyzers --timeout=180 -q
uv run pytest tests/unit/inference --timeout=90 -q
uv run pytest tests/unit/loaders --timeout=90 -q

# Batch 2: Medium modules (can run together, 90s timeout)
uv run pytest tests/unit/{visualization,core,search} \
  --ignore=tests/unit/search/test_performance.py \
  --timeout=90 -q

# Batch 3: Small modules (60s timeout)
uv run pytest tests/unit/{onboarding,plugins,reporting,dsl,config} \
  --timeout=60 -q

# Batch 4: Remaining
uv run pytest tests/unit \
  --ignore=tests/unit/analyzers \
  --ignore=tests/unit/inference \
  --ignore=tests/unit/loaders \
  --ignore=tests/unit/visualization \
  --ignore=tests/unit/core \
  --ignore=tests/unit/search \
  --ignore=tests/unit/onboarding \
  --ignore=tests/unit/plugins \
  --ignore=tests/unit/reporting \
  --ignore=tests/unit/dsl \
  --ignore=tests/unit/config \
  --timeout=60 -q
```

**Execution Time**: 15-20min total (parallelizable)
**Memory Usage**: Moderate (~1-2GB peak)
**Risk**: Low if timeouts set correctly

### Strategy 3: Quick Validation (Pre-commit)

```bash
# Fast tests only
uv run pytest -m "not slow and not performance" --timeout=30 -q

# Specific test file
uv run pytest tests/unit/core/test_trace.py -v

# Pattern matching
uv run pytest -k "test_basic" -v --timeout=30
```

## Module Testing Matrix

| Module        | Runtime | Timeout | Priority |
| ------------- | ------- | ------- | -------- |
| analyzers     | 8-10min | 180s    | CRITICAL |
| inference     | 3-5min  | 90s     | CRITICAL |
| loaders       | 2-4min  | 90s     | CRITICAL |
| visualization | 2-3min  | 90s     | HIGH     |
| core          | 1-2min  | 60s     | CRITICAL |
| search        | 1-2min  | 90s     | HIGH     |
| onboarding    | 30-60s  | 60s     | MEDIUM   |
| plugins       | 30s     | 60s     | MEDIUM   |
| reporting     | 30-60s  | 60s     | MEDIUM   |
| dsl           | 30s     | 60s     | MEDIUM   |
| config        | 10s     | 60s     | HIGH     |

**Note**: Exclude `tests/unit/search/test_performance.py` - it hangs on large datasets

## Coverage Measurement

### Module Coverage (Safe)

```bash
# Single module
uv run pytest tests/unit/analyzers \
  --cov=src/tracekit/analyzers \
  --cov-report=term-missing:skip-covered \
  --cov-report=json \
  --timeout=180 \
  -q
```

### Incremental Coverage (Recommended)

```bash
# Measure critical modules
for module in analyzers inference loaders core; do
  echo "=== $module ==="
  uv run pytest tests/unit/$module \
    --cov=src/tracekit/$module \
    --cov-report=term-missing:skip-covered \
    --timeout=180 -q | tail -20
done
```

### Full Coverage (Use with Caution)

```bash
# Exclude problematic tests, use high timeout
uv run pytest tests/unit \
  --ignore=tests/unit/search/test_performance.py \
  --cov=src/tracekit \
  --cov-report=term-missing:skip-covered \
  --cov-report=html \
  --timeout=300 \
  -q

# View HTML report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

**Warning**: Full coverage takes 15-20min and may timeout. Prefer batched approach.

## Troubleshooting

### Tests Hang/Timeout

**Symptoms**: No output, terminal freezes

**Fix**:

1. `Ctrl+C` to kill
2. Check if running `test_performance.py` - Exclude it
3. Increase timeout: `--timeout=180`
4. Run smaller batches

### Memory Issues

**Symptoms**: System slowdown, swap usage

**Fix**:

1. Run modules individually
2. Exclude memory tests: `-m "not memory_intensive"`
3. Close other applications
4. Monitor: `watch -n 1 free -h`

### Collection Errors

**Symptoms**: `ERROR collecting tests/...`

**Fix**:

```bash
# Check for unregistered marks
uv run pytest --collect-only --strict-markers

# Fix: Remove unregistered @pytest.mark.{name} decorators
# Or add marks to pyproject.toml [tool.pytest.ini_options] markers

# Verify collection works
uv run pytest tests/unit/{module} --collect-only
```

## Available Test Scripts

### Optimized Test Runner

Use `scripts/test.sh` for parallel test execution with coverage:

```bash
# Run all tests with parallel execution (pytest-xdist)
./scripts/test.sh

# Run with custom worker count
./scripts/test.sh --workers 4

# Run with coverage
./scripts/test.sh --coverage
```

**Features**: Parallel execution, extended timeout (300s), coverage reports, ~10 min runtime.

### Safe Test Wrapper

Use `scripts/safe_pytest.sh` for Claude Code/terminal-safe execution:

```bash
# Run all unit tests safely
./scripts/safe_pytest.sh

# Run specific path
./scripts/safe_pytest.sh tests/unit/{module}

# Pass pytest options
./scripts/safe_pytest.sh -v -x
```

**Features**: Safe environment variables, resource limits, prevents terminal crashes.

### Coverage Measurement

Use `scripts/measure_coverage.py` for detailed coverage analysis:

```bash
# Measure coverage for all modules
uv run python scripts/measure_coverage.py

# Measure specific modules
uv run python scripts/measure_coverage.py --modules analyzers inference loaders
```

## Test Markers

### Required Markers

Every test file MUST have module-level markers:

```python
import pytest

pytestmark = [pytest.mark.unit, pytest.mark.loader]

# Tests go here...
```

### Marker Categories

**Level Markers** (required):

- `unit` - Unit tests (fast, isolated, no I/O)
- `integration` - Integration tests (slower, multiple components)
- `stress` - Stress tests (high load, memory intensive)
- `performance` - Performance benchmark tests
- `compliance` - Standards compliance tests (IEEE, JEDEC)
- `validation` - Ground truth validation tests

**Domain Markers** (required):

- `loader` - Loader module tests
- `analyzer` - Analyzer module tests
- `inference` - Protocol inference tests
- `exporter` - Exporter module tests
- `core` - Core functionality tests
- `visualization` - Visualization tests
- `workflow` - Workflow-specific tests

**Subdomain Markers** (optional):

- `digital` - Digital signal analysis
- `spectral` - Spectral analysis
- `statistical` - Statistical analysis
- `protocol` - Protocol analysis
- `pattern` - Pattern recognition/detection

**Resource Markers** (optional):

- `slow` - Tests taking >1 second to run
- `memory_intensive` - Tests requiring significant memory (>100MB)

### Running by Marker

```bash
# All unit tests
uv run pytest -m unit

# Loader unit tests only
uv run pytest -m "unit and loader"

# Exclude slow tests
uv run pytest -m "not slow"

# Digital analysis tests
uv run pytest -m "analyzer and digital"

# Compliance tests only
uv run pytest -m compliance
```

### Validation

```bash
# Validate markers in your test files
uv run python scripts/validate_test_markers.py

# Auto-fix missing markers
uv run python scripts/validate_test_markers.py --fix

# Check specific files
uv run python scripts/validate_test_markers.py --files tests/unit/loaders/test_binary.py
```

## Fixtures

### Domain-Specific Fixtures

Fixtures are organized by domain:

- `tests/conftest.py` - Global fixtures (paths, cleanup)
- `tests/unit/loaders/conftest.py` - Loader fixtures
- `tests/unit/analyzers/conftest.py` - Analyzer fixtures
- `tests/unit/inference/conftest.py` - Inference fixtures
- `tests/performance/conftest.py` - Performance fixtures

### Factory Fixtures

Use factory fixtures for flexible test data generation:

```python
def test_with_factory(signal_factory, packet_factory):
    # Generate custom signal
    signal, metadata = signal_factory(
        signal_type="square",
        frequency=5000,
        noise_level=0.1
    )

    # Generate custom packets
    data, truth = packet_factory(
        count=100,
        checksum_type="crc16",
        corruption_rate=0.05
    )
```

### Available Factories

From `tests.utils`:

- `signal_factory` - Generate test signals (sine, square, sawtooth, etc.)
- `packet_factory` - Generate test packets with checksums
- `waveform_factory` - Generate waveform structures

### Domain Fixtures

From domain-specific conftest files:

- `loader_error_scenarios` - Common loader error cases
- `mock_file_handle` - Create temporary test files
- `simple_binary_packet` - Basic packet for testing
- `malformed_packets` - Invalid packets for error handling
- `packet_format_config` - Configurable packet formats

See domain conftest files for complete fixture list.

## Quality Gates

### Pre-commit Hooks

Install pre-commit hooks to catch issues early:

```bash
pre-commit install
```

Hooks run automatically on commit:

- Marker validation
- Code formatting (ruff)
- Linting (ruff, mypy)
- Shellcheck for scripts

### Manual Checks

```bash
# Validate markers
uv run python scripts/validate_test_markers.py

# Check test isolation (verify tests don't share state)
uv run python scripts/check_test_isolation.py

# Verify test data integrity
./scripts/verify_test_data.sh
```

### CI/CD Quality Gates

All quality gates run in CI:

- Marker validation (blocks PR if missing markers)
- Test isolation check (warning only)
- Coverage requirements (blocks PR if <80%)
- Code formatting and linting

## Pytest Configuration

File: `pyproject.toml`

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
addopts = ["--import-mode=importlib", "-ra", "--strict-markers", "--strict-config", "--timeout=60"]
timeout = 60
timeout_method = "thread"
markers = [
    "slow: marks tests as slow running",
    "unit: marks unit tests",
    "integration: marks integration tests",
    "performance: marks performance benchmarks",
    "memory_intensive: marks tests using >100MB",
    # ... see pyproject.toml for full list of 40+ markers
]
```

## Summary

**Safe Default**:

```bash
uv run pytest tests/unit/{module} -v --tb=short --timeout=90
```

**Full Suite**:
Use batched execution strategy (see scripts above)

**Coverage**:
Measure module-by-module, combine results

**When in Doubt**:
Test one module at a time with explicit timeout

---

## See Also

- **tests/QUICK_REFERENCE.md** - Quick reference card for common testing tasks
- **tests/MIGRATION_GUIDE.md** - Migration guide for updating existing tests
- **CLAUDE.md** - Main project instructions and development workflow
- **scripts/README.md** - Comprehensive script documentation
- **docs/testing/index.md** - Detailed testing philosophy and patterns

---

**Maintenance**: Update when adding significant tests to any module
