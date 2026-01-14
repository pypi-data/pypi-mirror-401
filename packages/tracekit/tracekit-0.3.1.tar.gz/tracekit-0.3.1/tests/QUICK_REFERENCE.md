# Test Suite Quick Reference

Quick reference card for common testing tasks in TraceKit.

## Running Tests

### Basic Commands

```bash
# Single module (fastest, recommended for development)
uv run pytest tests/unit/loaders -v

# Specific test file
uv run pytest tests/unit/loaders/test_binary.py -v

# Single test function
uv run pytest tests/unit/loaders/test_binary.py::test_load_packet -v

# All unit tests
uv run pytest tests/unit -v
```

### With Markers

```bash
# By level marker
uv run pytest -m unit                    # Unit tests only
uv run pytest -m integration             # Integration tests
uv run pytest -m compliance              # Compliance tests

# By domain marker
uv run pytest -m loader                  # Loader tests
uv run pytest -m analyzer                # Analyzer tests
uv run pytest -m inference               # Inference tests

# Combined markers
uv run pytest -m "unit and loader"       # Loader unit tests
uv run pytest -m "analyzer and digital"  # Digital analyzer tests

# Exclude markers
uv run pytest -m "not slow"              # Exclude slow tests
uv run pytest -m "unit and not slow"     # Fast unit tests only
```

### With Coverage

```bash
# Single module with coverage
uv run pytest tests/unit/loaders --cov=src/tracekit/loaders --cov-report=term-missing

# HTML coverage report
uv run pytest tests/unit/loaders --cov=src/tracekit/loaders --cov-report=html
open htmlcov/index.html  # View report

# Coverage with markers
uv run pytest -m "unit and loader" --cov=src/tracekit/loaders
```

### Performance Options

```bash
# Parallel execution (4 workers)
uv run pytest tests/unit -n 4

# Stop on first failure
uv run pytest tests/unit -x

# Stop after N failures
uv run pytest tests/unit --maxfail=3

# Show slowest tests
uv run pytest tests/unit --durations=10

# Verbose output with full tracebacks
uv run pytest tests/unit -vv --tb=long
```

## Writing Tests

### Minimal Test Template

```python
import pytest

# Required: Add module-level markers
pytestmark = [pytest.mark.unit, pytest.mark.loader]

def test_something():
    # Test code here
    assert True
```

### With Factory Fixtures

```python
import pytest

pytestmark = [pytest.mark.unit, pytest.mark.analyzer, pytest.mark.digital]

def test_with_signal(signal_factory):
    # Generate test signal
    signal, metadata = signal_factory(
        signal_type="sine",
        frequency=1000,
        sample_rate=10000
    )

    # Test code
    assert len(signal) > 0
    assert metadata['frequency'] == 1000
```

### With Multiple Fixtures

```python
import pytest

pytestmark = [pytest.mark.unit, pytest.mark.loader]

def test_with_factories(signal_factory, packet_factory, tmp_path):
    # Generate signal
    signal, _ = signal_factory(signal_type="square")

    # Generate packets
    packets, truth = packet_factory(count=10)

    # Use tmp_path for files
    test_file = tmp_path / "test.bin"
    test_file.write_bytes(packets)

    # Test code
    assert test_file.exists()
```

### With Mocks

```python
import pytest
from unittest.mock import MagicMock
from tests.utils import mock_optional_module

pytestmark = [pytest.mark.unit, pytest.mark.loader]

def test_with_mock():
    mock_wfm = MagicMock()
    mock_wfm.parse.return_value = {'data': [1, 2, 3]}

    with mock_optional_module('rigol_wfm', mock_wfm):
        # Code that imports rigol_wfm
        result = some_function_that_uses_rigol_wfm()
        assert result is not None
```

## Markers Reference

### Level Markers (Required)

| Marker        | Description                       |
| ------------- | --------------------------------- |
| `unit`        | Unit tests (fast, isolated)       |
| `integration` | Integration tests                 |
| `stress`      | Stress tests (high load)          |
| `performance` | Performance benchmarks            |
| `compliance`  | Standards compliance (IEEE/JEDEC) |
| `validation`  | Ground truth validation           |

### Domain Markers (Required)

| Marker          | Description              |
| --------------- | ------------------------ |
| `loader`        | Loader module tests      |
| `analyzer`      | Analyzer module tests    |
| `inference`     | Inference module tests   |
| `exporter`      | Exporter module tests    |
| `core`          | Core functionality tests |
| `visualization` | Visualization tests      |
| `workflow`      | Workflow-specific tests  |

### Subdomain Markers (Optional)

| Marker        | Description             |
| ------------- | ----------------------- |
| `digital`     | Digital signal analysis |
| `spectral`    | Spectral analysis       |
| `statistical` | Statistical analysis    |
| `protocol`    | Protocol analysis       |
| `pattern`     | Pattern recognition     |
| `power`       | Power analysis          |
| `jitter`      | Jitter measurement      |

### Resource Markers (Optional)

| Marker             | Description            |
| ------------------ | ---------------------- |
| `slow`             | Tests taking >1 second |
| `memory_intensive` | Tests using >100MB RAM |

## Factory Fixtures

### signal_factory

Generate test signals:

```python
# Sine wave
signal, metadata = signal_factory(
    signal_type="sine",
    frequency=1000,        # Hz
    sample_rate=10000,     # Hz
    duration=1.0,          # seconds
    amplitude=1.0,         # V
    noise_level=0.0        # 0.0 = no noise
)

# Square wave
signal, metadata = signal_factory(signal_type="square", frequency=500)

# Sawtooth wave
signal, metadata = signal_factory(signal_type="sawtooth", frequency=100)

# Random noise
signal, metadata = signal_factory(signal_type="noise", duration=1.0)
```

### packet_factory

Generate test packets:

```python
# Basic packets
data, truth = packet_factory(
    count=100,              # Number of packets
    checksum_type="crc16",  # crc16, crc32, xor
    corruption_rate=0.0     # 0.0 = no corruption
)

# Corrupted packets for testing error handling
data, truth = packet_factory(count=50, corruption_rate=0.1)
```

### waveform_factory

Generate waveform structures:

```python
waveform = waveform_factory(
    num_channels=4,
    sample_rate=1e6,
    duration=0.01,
    channel_names=["CH1", "CH2", "CH3", "CH4"]
)
```

## Test Utilities

### Assertions

```python
from tests.utils import (
    assert_signals_equal,
    assert_within_tolerance,
    assert_packet_valid
)

# Compare signals with tolerance
assert_signals_equal(actual, expected, atol=1e-6)

# Check value within relative tolerance
assert_within_tolerance(measured, expected, rtol=0.01)

# Validate packet structure
assert_packet_valid(packet, format_spec)
```

### Mocking

```python
from tests.utils import mock_optional_module, mock_rigol_wfm

# Mock any optional module
with mock_optional_module('module_name', MagicMock()):
    # Code that imports module_name
    pass

# Pre-configured mock for rigol_wfm
with mock_rigol_wfm():
    # Code that uses rigol_wfm
    pass
```

## Domain Fixtures

### Loader Fixtures

From `tests/unit/loaders/conftest.py`:

```python
# Error scenarios
def test_error_handling(loader_error_scenarios):
    for error_type, content in loader_error_scenarios.items():
        # Test each error scenario
        pass

# Create temporary files
def test_with_file(mock_file_handle):
    test_file = mock_file_handle(b"\xaa\x55\x01\x02", "test.bin")
    # Use test_file
    pass

# Binary packets
def test_packet_loading(simple_binary_packet):
    # Use pre-generated packet
    pass

# Malformed packets
def test_error_handling(malformed_packets):
    for error_type, packet in malformed_packets.items():
        # Test each malformed packet
        pass
```

### Built-in Fixtures

```python
# Temporary directory (auto-cleanup)
def test_with_files(tmp_path):
    file1 = tmp_path / "test1.txt"
    file1.write_text("content")
    # tmp_path is cleaned up automatically

# Temporary file
def test_with_file(tmp_path):
    temp_file = tmp_path / "data.bin"
    temp_file.write_bytes(b"\x00\x01\x02")
    assert temp_file.exists()
```

## Quality Gates

### Marker Validation

```bash
# Validate all test files
uv run python scripts/validate_test_markers.py

# Auto-fix missing markers
uv run python scripts/validate_test_markers.py --fix

# Check specific files
uv run python scripts/validate_test_markers.py --files tests/unit/loaders/test_binary.py

# Verbose output
uv run python scripts/validate_test_markers.py -v
```

### Test Isolation

```bash
# Check all tests
uv run python scripts/check_test_isolation.py

# Check specific files
uv run python scripts/check_test_isolation.py --files tests/unit/loaders/test_binary.py

# Verbose output
uv run python scripts/check_test_isolation.py -v
```

### Test Data Verification

```bash
# Verify test data integrity
./scripts/verify_test_data.sh

# Verbose output
./scripts/verify_test_data.sh -v
```

## Pre-commit Hooks

### Install Hooks

```bash
# Install all pre-commit hooks
pre-commit install

# Run on all files (without committing)
pre-commit run --all-files

# Run specific hook
pre-commit run validate-test-markers --all-files
```

### Skip Hooks (Not Recommended)

```bash
# Skip all hooks for single commit
git commit --no-verify -m "message"

# Skip specific hook
SKIP=validate-test-markers git commit -m "message"
```

## Common Workflows

### Adding a New Test

```bash
# 1. Create test file
touch tests/unit/loaders/test_new.py

# 2. Add markers and test code
cat > tests/unit/loaders/test_new.py << 'EOF'
import pytest

pytestmark = [pytest.mark.unit, pytest.mark.loader]

def test_new_feature():
    assert True
EOF

# 3. Validate markers
uv run python scripts/validate_test_markers.py --files tests/unit/loaders/test_new.py

# 4. Run test
uv run pytest tests/unit/loaders/test_new.py -v
```

### Debugging a Failing Test

```bash
# Run with verbose output and full traceback
uv run pytest tests/unit/loaders/test_binary.py::test_failing -vv --tb=long

# Run with pdb debugger
uv run pytest tests/unit/loaders/test_binary.py::test_failing --pdb

# Show local variables on failure
uv run pytest tests/unit/loaders/test_binary.py::test_failing -vv --showlocals

# Capture output (print statements)
uv run pytest tests/unit/loaders/test_binary.py::test_failing -v -s
```

### Measuring Coverage

```bash
# Module coverage
uv run pytest tests/unit/loaders --cov=src/tracekit/loaders --cov-report=term-missing

# Coverage with HTML report
uv run pytest tests/unit/loaders --cov=src/tracekit/loaders --cov-report=html
open htmlcov/index.html

# Coverage for specific files only
uv run pytest tests/unit/loaders --cov=src/tracekit/loaders/binary.py --cov-report=term

# Show uncovered lines
uv run pytest tests/unit/loaders --cov=src/tracekit/loaders --cov-report=term-missing:skip-covered
```

## Environment Setup

### First Time Setup

```bash
# Clone repository
git clone https://github.com/lair-click-bats/tracekit.git
cd tracekit

# Install dependencies
uv sync

# Install pre-commit hooks
pre-commit install

# Verify setup
uv run pytest tests/unit -x --maxfail=5
```

### Daily Development

```bash
# Update dependencies
uv sync

# Run tests before committing
uv run pytest tests/unit/{module} -v

# Validate markers
uv run python scripts/validate_test_markers.py

# Commit (pre-commit hooks run automatically)
git add .
git commit -m "feat: add new feature"
```

## Troubleshooting

### Tests hang or timeout

```bash
# Increase timeout
uv run pytest tests/unit/loaders --timeout=180

# Exclude slow tests
uv run pytest tests/unit -m "not slow"

# Run with timeout disabled (debugging only)
uv run pytest tests/unit/loaders --timeout=0
```

### Import errors

```bash
# Check Python path
uv run python -c "import sys; print(sys.path)"

# Verify src is in path
uv run pytest --collect-only tests/unit/loaders

# Check test can import
uv run python -c "from tracekit.loaders import load_binary"
```

### Marker errors

```bash
# List all available markers
uv run pytest --markers

# Check strict markers
uv run pytest --strict-markers tests/unit/loaders

# Fix missing markers
uv run python scripts/validate_test_markers.py --fix
```

## Documentation

- **Comprehensive Guide**: `.claude/PYTEST_GUIDE.md`
- **Migration Guide**: `tests/MIGRATION_GUIDE.md`
- **Main Documentation**: `CLAUDE.md`
- **Test Utilities**: `tests/utils/` (see module docstrings)

## Cheat Sheet

```bash
# Fast iteration during development
uv run pytest tests/unit/loaders/test_binary.py::test_specific -v

# Before committing
uv run pytest tests/unit/{module} -v
uv run python scripts/validate_test_markers.py

# Full validation (before PR)
uv run pytest tests/unit -v --cov=src/tracekit
uv run python scripts/validate_test_markers.py
uv run python scripts/check_test_isolation.py

# Common pytest flags
-v              # Verbose
-vv             # Very verbose
-x              # Stop on first failure
--maxfail=N     # Stop after N failures
-s              # Show print output
--pdb           # Drop into debugger on failure
--tb=short      # Short traceback
--tb=long       # Long traceback
--durations=N   # Show N slowest tests
-n N            # Parallel execution (N workers)
```
