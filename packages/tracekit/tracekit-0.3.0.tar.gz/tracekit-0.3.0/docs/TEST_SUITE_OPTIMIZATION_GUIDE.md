# Test Suite Optimization Guide for Large Python Projects

## Executive Summary

This document provides comprehensive analysis and best practices for managing and optimizing large Python test suites, specifically tailored for TraceKit's test infrastructure with **17,524 test functions across 408 files**.

### Current State Analysis

| Metric                               | Value                                                          |
| ------------------------------------ | -------------------------------------------------------------- |
| Total Test Functions                 | 17,524                                                         |
| Test Files                           | 408                                                            |
| Fixtures Defined                     | 692                                                            |
| Marked as slow/memory_intensive/skip | 176                                                            |
| Test Categories                      | unit, integration, stress, performance, compliance, validation |
| Primary Dependencies                 | numpy, scipy, matplotlib, pywt, pandas                         |

---

## 1. Most Frequent Points of Failure in Large Test Suites

### 1.1 Exit Code 137 - OOM Killer

**Root Cause:** Linux kernel's OOM (Out-of-Memory) killer terminates processes when system memory is exhausted.

**Why It Happens in TraceKit:**

- Heavy scientific computing dependencies (numpy, scipy)
- Large signal arrays (10M+ sample fixtures)
- Parallel test execution with pytest-xdist
- Matplotlib figure accumulation
- Fixture caching across session scope

**Detection Strategies:**

```bash
# Check system logs for OOM events
dmesg | grep -i "killed process"

# Monitor memory during test runs
pytest tests/ -v --tb=short 2>&1 | tee test.log &
watch -n 1 'free -h && ps aux --sort=-%mem | head -10'
```

**Mitigation (Already Implemented in conftest.py):**

```python
@pytest.fixture(autouse=True, scope="function")
def memory_cleanup():
    """Force garbage collection after each test."""
    yield
    import gc
    gc.collect()

@pytest.fixture(autouse=True)
def cleanup_matplotlib():
    """Close matplotlib figures to prevent memory accumulation."""
    yield
    try:
        import matplotlib.pyplot as plt
        plt.close("all")
    except ImportError:
        pass
```

### 1.2 Test Collection Problems

**Symptoms:**

- Slow collection phase (>30 seconds for 17K+ tests)
- Import errors during collection
- Circular import issues
- Missing module dependencies

**Common Causes:**

1. Heavy imports at module level
2. Fixture code running during collection
3. Complex conftest.py hierarchies
4. Dynamic test generation

**Best Practices:**

```python
# BAD: Heavy import at module level
import scipy.signal  # Loaded during collection

# GOOD: Lazy import inside test
def test_signal_processing():
    import scipy.signal
    # use scipy.signal
```

### 1.3 Flaky Tests and Race Conditions

**Common Patterns in Signal Processing Suites:**

1. **Timing-dependent tests** - Tests that assume specific timing
2. **Order-dependent tests** - Tests that rely on execution order
3. **Resource contention** - File handles, matplotlib backends
4. **Random data without seeds** - Non-reproducible failures

**Detection:**

```bash
# Run tests multiple times to detect flakiness
for i in {1..10}; do
    pytest tests/unit/inference/ -x --tb=line 2>&1 | tee run_$i.log
done

# Use pytest-repeat plugin
pytest tests/unit/inference/ --count=5 -x
```

**Mitigation:**

```python
# Always use seeded random generators
rng = np.random.default_rng(42)  # Reproducible

# Avoid time.sleep() - use mocking instead
from unittest.mock import patch

@patch('time.time', return_value=1000.0)
def test_timing_logic(mock_time):
    pass
```

### 1.4 Dependency Conflicts

**High-Risk Dependencies in TraceKit:**

| Package    | Risk Level | Common Issues                     |
| ---------- | ---------- | --------------------------------- |
| numpy      | Medium     | ABI incompatibility with scipy    |
| scipy      | High       | Memory-intensive operations       |
| matplotlib | High       | Backend conflicts, display issues |
| pywt       | Medium     | Version-specific API changes      |
| h5py       | Medium     | HDF5 library version conflicts    |

**Best Practice:** Pin specific versions in `uv.lock` and use virtual environments.

### 1.5 Fixture Explosion and Scope Issues

**Problem:** 692 fixtures across 134 files can create complex dependency graphs.

**Anti-patterns:**

```python
# BAD: Function-scoped expensive fixture
@pytest.fixture
def large_signal():
    return np.random.randn(10_000_000)  # Created for every test

# GOOD: Session-scoped with proper caching
@pytest.fixture(scope="session")
def large_signal():
    return np.random.default_rng(42).standard_normal(10_000_000)
```

**Fixture Scope Guidelines:**

| Scope    | Use Case                              | TraceKit Examples                            |
| -------- | ------------------------------------- | -------------------------------------------- |
| session  | Read-only data, paths, global configs | `project_root`, `test_data_dir`, `wfm_files` |
| module   | Expensive shared data within file     | `loaded_wfm_data`, `large_signal`            |
| function | Mutable state, temporary resources    | `tmp_output_dir`, `memory_cleanup`           |

---

## 2. Best Practices for Test Suite Optimization

### 2.1 Optimal Test Organization

**Recommended Structure (Already Implemented):**

```
tests/
+-- conftest.py              # Root fixtures, hooks (SSOT)
+-- hypothesis_strategies.py # Property-based test strategies
+-- utils/                   # Test utilities
|   +-- factories.py
|   +-- generators.py
|   +-- mocking.py
|   +-- assertions.py
+-- unit/                    # Fast, isolated tests
|   +-- analyzers/
|   +-- loaders/
|   +-- inference/
|   +-- ...
+-- integration/             # Multi-component tests
+-- stress/                  # High-load tests
+-- performance/             # Benchmarks
+-- compliance/              # Standards tests
+-- validation/              # Ground truth validation
```

**Key Principles:**

1. **Single Source of Truth (SSOT)** - All pytest hooks in root `conftest.py`
2. **Marker-Based Categorization** - Use markers for test filtering
3. **Fixture Hierarchy** - Session > Module > Function scoping
4. **Factory Patterns** - Use factories for parameterized data

### 2.2 Parallel Execution Strategies

**pytest-xdist Configuration:**

```bash
# Optimal for 8-core machine with 16GB RAM
pytest tests/unit/ -n 4 --dist loadscope

# Memory-constrained environments
pytest tests/unit/ -n 2 --max-worker-restart 2

# Disable for debugging
pytest tests/unit/ -n 0
```

**Distribution Modes:**

| Mode        | Best For               | TraceKit Recommendation |
| ----------- | ---------------------- | ----------------------- |
| `loadscope` | Module-heavy fixtures  | **Recommended**         |
| `loadfile`  | File-level parallelism | Good for unit tests     |
| `loadgroup` | Custom grouping        | Complex scenarios       |
| `each`      | Fully parallel         | Small, fast tests only  |

**Memory-Safe Parallel Execution:**

```python
# In pyproject.toml or pytest command
# -n 4: 4 worker processes
# --maxprocesses=4: Hard limit on workers
# --max-worker-restart=2: Restart crashed workers (OOM recovery)
```

**Worker Count Guidelines:**

| System RAM | Recommended Workers | Notes                |
| ---------- | ------------------- | -------------------- |
| 8 GB       | 2                   | Conservative, safe   |
| 16 GB      | 4                   | Standard development |
| 32 GB      | 8                   | CI/CD runners        |
| 64 GB+     | 16                  | Heavy compute nodes  |

### 2.3 Test Selection and Filtering

**Marker-Based Selection:**

```bash
# Run only fast unit tests
pytest tests/unit/ -m "unit and not slow and not memory_intensive"

# Run specific domain
pytest -m "analyzer and digital"

# Skip expensive tests
pytest -m "not stress and not performance"
```

**Keyword-Based Selection:**

```bash
# Run tests matching pattern
pytest -k "test_edge_detection" tests/

# Exclude patterns
pytest -k "not hypothesis and not stress"
```

**Directory-Based Selection:**

```bash
# Run specific module tests
pytest tests/unit/analyzers/digital/

# Run by file pattern
pytest tests/unit/**/test_*_basic.py
```

**Changed-File Selection (CI/CD):**

```bash
# Run tests for changed files only
git diff --name-only HEAD~1 | \
    grep -E '^src/.*\.py$' | \
    xargs -I {} pytest tests/ --collect-only -q 2>/dev/null | \
    head -100
```

### 2.4 Fixture Optimization

**Current State Assessment:**

- 58 fixtures in root `conftest.py`
- 692 total fixtures across test files
- Good use of session/module scoping

**Optimization Strategies:**

**1. Lazy Loading Pattern:**

```python
@pytest.fixture(scope="session")
def heavy_data():
    """Lazy load only when first accessed."""
    def _load():
        return expensive_operation()
    return _load
```

**2. Factory Fixtures (Already Implemented):**

```python
@pytest.fixture
def signal_factory():
    """Create signals on demand with configurable parameters."""
    def _create_signal(signal_type="sine", frequency=1000.0, ...):
        # Generate signal
        return signal, metadata
    return _create_signal
```

**3. Fixture Caching:**

```python
@pytest.fixture(scope="module")
def loaded_wfm_data(wfm_files):
    """Cache loaded WFM files for module reuse."""
    cache = {}
    for wfm_file in wfm_files[:5]:  # Limit to 5 files
        cache[str(wfm_file.name)] = load_tektronix_wfm(wfm_file)
    return cache
```

### 2.5 Resource Management

**Memory Monitoring Fixture:**

```python
@pytest.fixture
def memory_monitor():
    """Track peak memory usage during test."""
    import tracemalloc

    class Monitor:
        def __init__(self):
            self.peak_mb = 0

        def __enter__(self):
            tracemalloc.start()
            return self

        def __exit__(self, *args):
            _, peak = tracemalloc.get_traced_memory()
            self.peak_mb = peak / (1024 * 1024)
            tracemalloc.stop()

    return Monitor
```

**Timeout Configuration:**

```python
# In pyproject.toml
[tool.pytest.ini_options]
timeout = 90                    # Default test timeout
timeout_method = "thread"       # Thread-based timeout
timeout_func_only = false       # Include fixture time
```

**Per-Test Timeouts:**

```python
import pytest

@pytest.mark.timeout(30)
def test_quick_operation():
    pass

@pytest.mark.timeout(300)
def test_slow_operation():
    pass
```

---

## 3. CI/CD Configuration Best Practices

### 3.1 GitHub Actions - Optimized Configuration

**Current State:** Good multi-stage pipeline with chunked tests workflow.

**Recommended Enhancements:**

**Tiered Test Strategy:**

```yaml
# .github/workflows/ci.yml (enhanced)
jobs:
  # Stage 1: Fast Checks (< 2 min)
  fast-checks:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
      - name: Lint and Format
        run: |
          uv sync --all-extras
          uv run ruff check src/ tests/
          uv run ruff format --check src/ tests/
      - name: Type Check
        run: uv run mypy src/

  # Stage 2: Core Unit Tests (< 10 min)
  unit-fast:
    needs: fast-checks
    runs-on: ubuntu-latest
    timeout-minutes: 15
    strategy:
      matrix:
        shard: [1, 2, 3, 4] # Split tests across 4 shards
    steps:
      - uses: actions/checkout@v4
      - name: Run shard
        run: |
          uv run pytest tests/unit/ \
            -m "unit and not slow and not memory_intensive" \
            -n 4 \
            --dist loadfile \
            --splits 4 \
            --group ${{ matrix.shard }} \
            --benchmark-disable

  # Stage 3: Memory-Intensive Tests (sequential)
  unit-memory:
    needs: unit-fast
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - name: Run memory tests
        run: |
          uv run pytest tests/unit/ \
            -m "memory_intensive" \
            -n 2 \
            --tb=short

  # Stage 4: Integration Tests
  integration:
    needs: unit-fast
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - name: Run integration
        run: |
          uv run pytest tests/integration/ \
            -m integration \
            -n 2

  # Stage 5: Extended Tests (main branch only)
  extended:
    needs: [unit-fast, integration]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    timeout-minutes: 60
    steps:
      - name: Run stress and performance
        run: |
          uv run pytest tests/stress/ tests/performance/ \
            -m "stress or performance" \
            --tb=short
```

### 3.2 Test Sharding and Matrix Strategies

**pytest-split for Sharding:**

```bash
# Install pytest-split
pip install pytest-split

# Run specific shard
pytest tests/ --splits 4 --group 1
pytest tests/ --splits 4 --group 2
pytest tests/ --splits 4 --group 3
pytest tests/ --splits 4 --group 4
```

**Duration-Based Sharding:**

```yaml
# Store test durations
- name: Store test durations
  run: |
    pytest tests/unit/ --store-durations --durations-path=.test_durations

- name: Upload durations
  uses: actions/upload-artifact@v4
  with:
    name: test-durations
    path: .test_durations

# Use in subsequent runs
- name: Run balanced shards
  run: |
    pytest tests/unit/ \
      --splits 4 \
      --group ${{ matrix.shard }} \
      --durations-path=.test_durations
```

**Matrix Configuration for Different Test Types:**

```yaml
strategy:
  fail-fast: false
  matrix:
    include:
      # Fast unit tests - more parallelism
      - test_type: unit-fast
        path: tests/unit/
        markers: 'unit and not slow'
        workers: 4
        timeout: 15

      # Memory-intensive - less parallelism
      - test_type: unit-memory
        path: tests/unit/
        markers: 'memory_intensive'
        workers: 2
        timeout: 30

      # Integration - moderate parallelism
      - test_type: integration
        path: tests/integration/
        markers: 'integration'
        workers: 2
        timeout: 30
```

### 3.3 Caching Strategies

**Comprehensive Caching Configuration:**

```yaml
env:
  UV_CACHE_DIR: /tmp/.uv-cache

jobs:
  test:
    steps:
      # UV dependency cache
      - name: Cache UV dependencies
        uses: actions/cache@v4
        with:
          path: |
            ${{ env.UV_CACHE_DIR }}
            ~/.cache/uv
          key: uv-${{ runner.os }}-${{ hashFiles('uv.lock') }}
          restore-keys: |
            uv-${{ runner.os }}-

      # pytest cache (test results, durations)
      - name: Cache pytest
        uses: actions/cache@v4
        with:
          path: .pytest_cache
          key: pytest-${{ runner.os }}-${{ hashFiles('pyproject.toml') }}
          restore-keys: |
            pytest-${{ runner.os }}-

      # mypy cache
      - name: Cache mypy
        uses: actions/cache@v4
        with:
          path: .mypy_cache
          key: mypy-${{ runner.os }}-${{ hashFiles('pyproject.toml') }}

      # Test data cache (if generated)
      - name: Cache test data
        uses: actions/cache@v4
        with:
          path: test_data/generated/
          key: testdata-${{ hashFiles('scripts/generate_comprehensive_test_data.py') }}
```

**Pre-commit Cache:**

```yaml
- name: Cache pre-commit
  uses: actions/cache@v4
  with:
    path: ~/.cache/pre-commit
    key: pre-commit-${{ runner.os }}-${{ hashFiles('.pre-commit-config.yaml') }}
```

### 3.4 Timeout Configurations

**Recommended Timeouts by Test Type:**

| Test Type     | Job Timeout | Per-Test Timeout | Notes                    |
| ------------- | ----------- | ---------------- | ------------------------ |
| Lint/Format   | 10 min      | N/A              | Fast, no timeout needed  |
| Type Check    | 15 min      | N/A              | Depends on codebase size |
| Unit (Fast)   | 15 min      | 30 sec           | Most tests < 1 sec       |
| Unit (Memory) | 30 min      | 90 sec           | Allow for GC             |
| Integration   | 30 min      | 120 sec          | Multi-component          |
| Stress        | 60 min      | 300 sec          | Intentionally slow       |
| Performance   | 30 min      | 60 sec           | Benchmarks               |

**Implementing Timeouts:**

```yaml
jobs:
  unit-fast:
    timeout-minutes: 15
    steps:
      - name: Run tests
        run: |
          uv run pytest tests/unit/ \
            --timeout=30 \
            --timeout-method=thread
```

### 3.5 Resource Limits and Allocation

**GitHub Actions Runner Specs:**

| Runner           | vCPUs | RAM   | Disk  | Best For         |
| ---------------- | ----- | ----- | ----- | ---------------- |
| ubuntu-latest    | 4     | 16 GB | 14 GB | Standard tests   |
| ubuntu-latest-8  | 8     | 32 GB | 28 GB | Memory-intensive |
| ubuntu-latest-16 | 16    | 64 GB | 56 GB | Stress tests     |

**Memory Management in CI:**

```yaml
- name: Set memory limits
  run: |
    # Limit Python memory allocation
    export PYTHONMALLOC=malloc

    # Set numpy memory limits
    export NPY_MEM_POLICY=smallest

    # Run tests with memory monitoring
    uv run pytest tests/ \
      -n 4 \
      --tb=short \
      -p no:cacheprovider
```

### 3.6 Fail-Fast vs Complete Run Strategies

**Fail-Fast (Default for PRs):**

```yaml
strategy:
  fail-fast: true # Stop on first failure
```

- **Pros:** Fast feedback, saves CI minutes
- **Cons:** May miss multiple independent failures

**Complete Run (Main Branch):**

```yaml
strategy:
  fail-fast: false # Run all jobs
```

- **Pros:** Complete picture of test health
- **Cons:** Longer runs, more CI minutes

**Hybrid Approach (Recommended):**

```yaml
jobs:
  unit:
    strategy:
      fail-fast: ${{ github.event_name == 'pull_request' }}
```

**--maxfail Configuration:**

```bash
# For PRs: Stop after 10 failures
pytest tests/ --maxfail=10

# For main branch: Run all
pytest tests/ --maxfail=0
```

---

## 4. Specific Recommendations for TraceKit

### 4.1 Current Strengths

1. **Excellent Test Organization**
   - Clear separation: unit/integration/stress/performance/compliance
   - Comprehensive markers defined in pyproject.toml
   - Factory fixtures for flexible test data generation

2. **Good Memory Management**
   - `memory_cleanup` fixture with GC
   - `cleanup_matplotlib` for figure cleanup
   - Session-scoped expensive fixtures

3. **Solid CI/CD Foundation**
   - Multi-stage pipeline in ci.yml
   - Chunked tests workflow
   - Concurrency management

### 4.2 Identified Issues and Solutions

**Issue 1: Full Test Runs Being Killed (Exit 137)**

**Root Cause Analysis:**

- 17,524 tests with heavy scipy/numpy operations
- Parallel execution with insufficient memory
- Large fixture arrays (10M samples)

**Solutions:**

**A. Reduce Parallel Workers:**

```yaml
# In tests-chunked.yml
- name: Run unit tests
  run: |
    uv run pytest tests/unit \
      -n 2 \  # Reduced from -n 4
      --max-worker-restart=3 \
      -m "unit and not memory_intensive"
```

**B. Split Memory-Intensive Tests:**

```yaml
# New job: unit-memory-intensive
unit-memory-intensive:
  runs-on: ubuntu-latest
  timeout-minutes: 60
  steps:
    - name: Run memory tests sequentially
      run: |
        uv run pytest tests/unit \
          -n 1 \  # Sequential
          -m "memory_intensive" \
          --tb=short
```

**C. Implement Test Sharding:**

```yaml
strategy:
  matrix:
    shard: [1, 2, 3, 4, 5, 6, 7, 8] # 8 shards

steps:
  - name: Run test shard
    run: |
      uv run pytest tests/unit \
        --splits 8 \
        --group ${{ matrix.shard }} \
        -n 2
```

**Issue 2: Test Collection Time**

With 17K+ tests, collection can take significant time.

**Solutions:**

**A. Use `--collect-only` for Validation:**

```bash
# Quick validation that all tests collect
pytest tests/ --collect-only -q --tb=no
```

**B. Pre-generate Test IDs:**

```bash
# Store test IDs
pytest tests/ --collect-only -q > .test_ids

# Run subset by IDs
pytest $(head -100 .test_ids)
```

**Issue 3: Fixture Overhead**

692 fixtures with complex dependency graphs.

**Solutions:**

**A. Audit Fixture Dependencies:**

```python
# Add to conftest.py for debugging
def pytest_fixture_setup(fixturedef, request):
    import time
    start = time.perf_counter()
    yield
    duration = time.perf_counter() - start
    if duration > 1.0:
        print(f"SLOW FIXTURE: {fixturedef.argname} took {duration:.2f}s")
```

**B. Reduce Session-Scoped Data:**

```python
# Current: Load 5 WFM files
@pytest.fixture(scope="module")
def loaded_wfm_data(wfm_files):
    cache = {}
    for wfm_file in wfm_files[:5]:  # Limit memory
        cache[str(wfm_file.name)] = load_tektronix_wfm(wfm_file)
    return cache

# Better: Load on-demand
@pytest.fixture(scope="module")
def wfm_loader(wfm_files):
    cache = {}
    def _load(name):
        if name not in cache:
            for f in wfm_files:
                if f.name == name:
                    cache[name] = load_tektronix_wfm(f)
                    break
        return cache.get(name)
    return _load
```

### 4.3 Recommended CI/CD Configuration

**Enhanced tests-chunked.yml:**

```yaml
name: Test Suite (Chunked)

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  workflow_dispatch:
  schedule:
    - cron: '0 2 * * *' # Nightly

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:
  PYTHON_VERSION: '3.12'
  UV_CACHE_DIR: /tmp/.uv-cache
  # Memory management
  PYTHONMALLOC: malloc
  MALLOC_TRIM_THRESHOLD_: 100000

jobs:
  # Determine test scope based on trigger
  setup:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    outputs:
      python-versions: ${{ steps.config.outputs.python-versions }}
      run-extended: ${{ steps.config.outputs.run-extended }}
      parallelism: ${{ steps.config.outputs.parallelism }}
      shards: ${{ steps.config.outputs.shards }}
    steps:
      - id: config
        run: |
          if [[ "${{ github.event_name }}" == "schedule" ]]; then
            echo 'python-versions=["3.12", "3.13"]' >> $GITHUB_OUTPUT
            echo "run-extended=true" >> $GITHUB_OUTPUT
            echo "parallelism=4" >> $GITHUB_OUTPUT
            echo "shards=8" >> $GITHUB_OUTPUT
          elif [[ "${{ github.ref }}" == "refs/heads/main" ]]; then
            echo 'python-versions=["3.12", "3.13"]' >> $GITHUB_OUTPUT
            echo "run-extended=true" >> $GITHUB_OUTPUT
            echo "parallelism=2" >> $GITHUB_OUTPUT
            echo "shards=4" >> $GITHUB_OUTPUT
          else
            echo 'python-versions=["3.12"]' >> $GITHUB_OUTPUT
            echo "run-extended=false" >> $GITHUB_OUTPUT
            echo "parallelism=2" >> $GITHUB_OUTPUT
            echo "shards=2" >> $GITHUB_OUTPUT
          fi

  # Unit tests - sharded for speed
  unit-sharded:
    needs: setup
    runs-on: ubuntu-latest
    timeout-minutes: 20
    strategy:
      fail-fast: ${{ github.event_name == 'pull_request' }}
      matrix:
        python: ${{ fromJson(needs.setup.outputs.python-versions) }}
        shard: [1, 2, 3, 4]
    steps:
      - uses: actions/checkout@v4

      - name: Setup UV
        uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true

      - name: Setup Python
        run: uv python install ${{ matrix.python }}

      - name: Install dependencies
        run: uv sync --all-extras

      - name: Run test shard
        run: |
          uv run pytest tests/unit/ \
            -m "unit and not slow and not memory_intensive" \
            -n ${{ needs.setup.outputs.parallelism }} \
            --dist loadfile \
            --splits 4 \
            --group ${{ matrix.shard }} \
            --benchmark-disable \
            --tb=short \
            --maxfail=20 \
            --junit-xml=results-shard-${{ matrix.shard }}-py${{ matrix.python }}.xml

      - name: Upload results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: results-shard-${{ matrix.shard }}-py${{ matrix.python }}
          path: results-*.xml

  # Memory-intensive tests - sequential
  unit-memory:
    needs: [setup, unit-sharded]
    runs-on: ubuntu-latest
    timeout-minutes: 45
    strategy:
      fail-fast: false
      matrix:
        python: ${{ fromJson(needs.setup.outputs.python-versions) }}
    steps:
      - uses: actions/checkout@v4

      - name: Setup
        uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true

      - run: uv python install ${{ matrix.python }}
      - run: uv sync --all-extras

      - name: Run memory-intensive tests
        run: |
          uv run pytest tests/unit/ \
            -m "memory_intensive" \
            -n 1 \
            --tb=short \
            --maxfail=10 \
            --junit-xml=results-memory-py${{ matrix.python }}.xml

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: results-memory-py${{ matrix.python }}
          path: results-*.xml

  # Integration tests
  integration:
    needs: [setup, unit-sharded]
    runs-on: ubuntu-latest
    timeout-minutes: 30
    strategy:
      fail-fast: false
      matrix:
        python: ${{ fromJson(needs.setup.outputs.python-versions) }}
    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true

      - run: uv python install ${{ matrix.python }}
      - run: uv sync --all-extras

      - name: Run integration tests
        run: |
          uv run pytest tests/integration/ \
            -m integration \
            -n 2 \
            --tb=short \
            --maxfail=10

  # Extended tests (main/scheduled only)
  extended:
    needs: [setup, unit-sharded, unit-memory]
    if: needs.setup.outputs.run-extended == 'true'
    runs-on: ubuntu-latest
    timeout-minutes: 90
    strategy:
      fail-fast: false
      matrix:
        test_type:
          - name: stress
            path: tests/stress/
            markers: stress
            workers: 1
            timeout: 60
          - name: performance
            path: tests/performance/
            markers: 'performance or benchmark'
            workers: 2
            timeout: 45
          - name: compliance
            path: tests/compliance/
            markers: compliance
            workers: 2
            timeout: 30
    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true

      - run: uv python install ${{ env.PYTHON_VERSION }}
      - run: uv sync --all-extras

      - name: Run ${{ matrix.test_type.name }} tests
        timeout-minutes: ${{ matrix.test_type.timeout }}
        run: |
          uv run pytest ${{ matrix.test_type.path }} \
            -m "${{ matrix.test_type.markers }}" \
            -n ${{ matrix.test_type.workers }} \
            --tb=short

  # Summary job
  summary:
    needs: [unit-sharded, unit-memory, integration]
    if: always()
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - name: Download all results
        uses: actions/download-artifact@v4
        with:
          path: results
        continue-on-error: true

      - name: Generate summary
        run: |
          echo "# Test Results Summary" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "| Job | Status |" >> $GITHUB_STEP_SUMMARY
          echo "|-----|--------|" >> $GITHUB_STEP_SUMMARY
          echo "| Unit (Sharded) | ${{ needs.unit-sharded.result }} |" >> $GITHUB_STEP_SUMMARY
          echo "| Unit (Memory) | ${{ needs.unit-memory.result }} |" >> $GITHUB_STEP_SUMMARY
          echo "| Integration | ${{ needs.integration.result }} |" >> $GITHUB_STEP_SUMMARY

      - name: Check required jobs
        run: |
          if [[ "${{ needs.unit-sharded.result }}" != "success" ]]; then
            echo "::error::Unit tests failed"
            exit 1
          fi
```

### 4.4 Quick Wins for Immediate Implementation

**1. Add pytest-split for Sharding:**

```toml
# In pyproject.toml [dependency-groups]
dev = [
    # ... existing deps
    "pytest-split>=0.8.2",
]
```

**2. Add Memory Marker to Heavy Tests:**

```python
# Find and mark heavy tests
@pytest.mark.memory_intensive
def test_large_fft():
    signal = np.random.randn(10_000_000)
    np.fft.fft(signal)
```

**3. Add Test Duration Tracking:**

```bash
# Generate duration data
pytest tests/unit/ --durations=100 --durations-min=1.0 -q

# Output: slowest tests to optimize
```

**4. Implement Gradual Execution:**

```bash
# For local development - run fast tests first
pytest tests/unit/ -m "unit and not slow" --ff -x

# Then run slower tests
pytest tests/unit/ -m "slow" --ff
```

### 4.5 Monitoring and Metrics

**CI Metrics to Track:**

- Test execution time by category
- Memory usage peak per job
- Flaky test rate
- Cache hit rate
- Test count growth over time

**Dashboard Configuration:**

```yaml
# Add to CI for metrics collection
- name: Collect metrics
  run: |
    echo "::set-output name=test_count::$(pytest --collect-only -q 2>/dev/null | tail -1)"
    echo "::set-output name=duration::$SECONDS"
```

---

## 5. Appendix: Command Reference

### Common pytest Commands

```bash
# Run all tests with coverage
pytest tests/ --cov=src/tracekit --cov-report=html

# Run fast tests only
pytest tests/ -m "not slow and not memory_intensive" -n 4

# Run with verbose failure output
pytest tests/ -v --tb=long -x

# Run and re-run failed tests
pytest tests/ --lf  # Last failed
pytest tests/ --ff  # Failed first

# Run with profiling
pytest tests/unit/analyzers/ --profile --profile-svg

# Collect without running
pytest tests/ --collect-only -q

# Run specific test by ID
pytest "tests/unit/analyzers/test_digital.py::TestEdgeDetection::test_rising_edges"

# Run tests matching pattern
pytest -k "edge and detection"

# Generate JUnit XML report
pytest tests/ --junit-xml=results.xml
```

### Memory Debugging

```bash
# Run with memory tracking
pytest tests/unit/ -n 1 --memray

# Find memory leaks
pytest tests/unit/analyzers/ --memray --memray-bin-path=memray.bin
memray flamegraph memray.bin

# Set memory limit (Linux)
ulimit -v 8000000  # 8GB virtual memory limit
pytest tests/
```

### CI/CD Debugging

```bash
# Test GitHub Actions locally with act
act -j unit-fast -P ubuntu-latest=nektos/act-environments-ubuntu:22.04

# Dry run workflow
act -n

# Debug specific job
act -j unit-sharded -v
```

---

## 6. References

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-xdist Documentation](https://pytest-xdist.readthedocs.io/)
- [pytest-split Documentation](https://github.com/jerry-git/pytest-split)
- [GitHub Actions Best Practices](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Python Memory Management](https://docs.python.org/3/c-api/memory.html)
- [NumPy Memory Policy](https://numpy.org/doc/stable/reference/routines.ctypeslib.html)

---

_Document Version: 1.0_
_Last Updated: 2026-01-08_
_TraceKit Test Suite: 17,524 tests across 408 files_
