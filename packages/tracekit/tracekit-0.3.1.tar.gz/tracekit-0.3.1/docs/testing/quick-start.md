# Quick Start Guide for Testing

> **Version**: 0.2.0 | **Last Updated**: 2026-01-11

A beginner-friendly introduction to testing in TraceKit. Start here if you're new to the project or testing in general.

## Table of Contents

- [Getting Started](#getting-started)
- [Running Your First Test](#running-your-first-test)
- [Common pytest Commands](#common-pytest-commands)
- [Debugging Tests](#debugging-tests)
- [Understanding Test Markers](#understanding-test-markers)
- [Best Practices](#best-practices)
- [Next Steps](#next-steps)

## Getting Started

### Prerequisites

Make sure you have TraceKit installed with development dependencies:

```bash
# Install all dependencies including test tools
uv sync --all-extras

# Verify installation
uv run pytest --version
```

You should see output like `pytest 9.0.2`.

### Your Development Environment

TraceKit works great with VS Code. If you're using it:

1. Open the TraceKit folder in VS Code
2. The Python extension should auto-detect the test framework
3. Look for the Testing icon in the sidebar (flask icon)
4. Tests will auto-discover and appear in the Test Explorer

## Running Your First Test

### Option 1: Command Line (Recommended for Learning)

Let's run a simple test to verify everything works:

```bash
# Run all unit tests (may take a few minutes first time)
pytest tests/unit

# Run just one test file to start
pytest tests/unit/core/test_signal.py -v
```

The `-v` flag means "verbose" and shows each test as it runs.

**What you'll see:**

```
tests/unit/core/test_signal.py::TestSignal::test_create_signal PASSED     [ 25%]
tests/unit/core/test_signal.py::TestSignal::test_add_channel PASSED       [ 50%]
tests/unit/core/test_signal.py::TestSignal::test_sample_rate PASSED       [ 75%]
tests/unit/core/test_signal.py::TestSignal::test_timestamps PASSED        [100%]

======================== 4 passed in 0.23s =========================
```

**Success!** You just ran your first tests.

### Option 2: VS Code Test Explorer

1. Click the Testing icon in the sidebar (flask/beaker icon)
2. You'll see a tree of all tests organized by file
3. Click the play button next to any test to run it
4. Green checkmark = passed, red X = failed

### Option 3: VS Code Debugger (For Deep Debugging)

1. Open any test file (e.g., `tests/unit/core/test_signal.py`)
2. Press **F5** (or Run > Start Debugging)
3. Select "Debug Current Test File"
4. Watch the tests run with debugger attached

## Common pytest Commands

Here are the essential commands you'll use daily:

### Running Tests

```bash
# Run all unit tests
pytest tests/unit

# Run a specific test file
pytest tests/unit/analyzers/test_digital.py

# Run a specific test class
pytest tests/unit/analyzers/test_digital.py::TestFrequencyAnalysis

# Run a specific test function
pytest tests/unit/analyzers/test_digital.py::TestFrequencyAnalysis::test_basic_frequency

# Run tests matching a pattern
pytest tests/unit -k "frequency"  # Runs all tests with "frequency" in name
```

### Faster Testing with Incremental Mode

**Incremental testing** only runs tests affected by your changes:

```bash
# First run: builds dependency graph
pytest --testmon

# Make changes to code...

# Second run: only runs affected tests (much faster!)
pytest --testmon
```

This is **perfect for TDD** (Test-Driven Development) and rapid iteration.

### Useful Flags

```bash
# Stop at first failure (fast feedback)
pytest -x

# Show print statements (debug output)
pytest -s

# Run in parallel (4 workers = 4x faster)
pytest -n 4

# Show detailed output for failures
pytest -v

# Combine flags
pytest tests/unit -v -x -s
```

### Coverage Reports

See which code is tested:

```bash
# Run tests with coverage
pytest tests/unit --cov=src/tracekit

# Generate HTML coverage report
pytest tests/unit --cov=src/tracekit --cov-report=html

# Open the report in your browser
open htmlcov/index.html
```

## Debugging Tests

### When a Test Fails

When a test fails, pytest shows helpful information:

```
FAILED tests/unit/core/test_signal.py::test_sample_rate - AssertionError: assert 44100 == 48000
```

This tells you:

- **File**: `tests/unit/core/test_signal.py`
- **Test**: `test_sample_rate`
- **Error**: Expected 48000 but got 44100

### Debugging Methods

**Method 1: Print Debugging** (Simplest)

```python
def test_sample_rate():
    signal = create_signal(sample_rate=48000)
    print(f"Signal sample rate: {signal.sample_rate}")  # Debug output
    assert signal.sample_rate == 48000
```

Run with `-s` to see prints:

```bash
pytest tests/unit/core/test_signal.py::test_sample_rate -s
```

**Method 2: VS Code Debugger** (Most Powerful)

1. Open the test file
2. Click left of line number to set a breakpoint (red dot appears)
3. Press **F5** and select "Debug Current Test File"
4. Execution stops at breakpoint
5. Hover over variables to see values
6. Use Debug Console to evaluate expressions

**Keyboard shortcuts while debugging:**

- **F10** - Step over (next line)
- **F11** - Step into (enter function)
- **Shift+F11** - Step out (exit function)
- **F5** - Continue to next breakpoint
- **Shift+F5** - Stop debugging

**Method 3: Drop into pdb** (Command Line Debugger)

Add this line where you want to pause:

```python
import pdb; pdb.set_trace()
```

Run the test:

```bash
pytest tests/unit/core/test_signal.py::test_sample_rate -s
```

Useful pdb commands:

- `l` - List code around current line
- `n` - Next line
- `s` - Step into function
- `c` - Continue execution
- `p variable_name` - Print variable value
- `q` - Quit debugger

### Debugging Tips

1. **Start simple**: Use print statements first
2. **Isolate the problem**: Run just one test at a time
3. **Check the data**: Print inputs and outputs
4. **Read the error carefully**: pytest tells you exactly what failed
5. **Use VS Code debugger**: Set breakpoints and inspect state

## Understanding Test Markers

**Markers** are tags that categorize tests. They help you run specific groups of tests.

### Common Markers

```python
import pytest

@pytest.mark.unit
def test_basic():
    """Unit test - fast, isolated."""
    pass

@pytest.mark.slow
def test_long_running():
    """Test that takes >1 second."""
    pass

@pytest.mark.memory_intensive
def test_large_data():
    """Test that uses >100MB memory."""
    pass

@pytest.mark.integration
def test_workflow():
    """Integration test - multiple components."""
    pass
```

### Running Specific Markers

```bash
# Run only unit tests
pytest -m unit

# Skip slow tests (faster feedback)
pytest -m "not slow"

# Skip slow AND memory-intensive tests
pytest -m "not slow and not memory_intensive"

# Run only analyzer tests
pytest -m analyzer

# Combine conditions
pytest -m "analyzer and not slow"
```

### Why Use Markers?

- **Speed**: Run only fast tests during development
- **Focus**: Test specific components you're working on
- **CI/CD**: Different markers for different pipeline stages
- **Organization**: Group related tests together

### List All Markers

```bash
# See all available markers and their descriptions
pytest --markers
```

## Best Practices

### 1. Run Tests Before Committing

Always run tests before pushing code:

```bash
# Quick check (fast tests only)
pytest -m "not slow and not memory_intensive" -x

# Full check (all tests)
pytest tests/unit
```

### 2. Use Incremental Testing During Development

Speed up your workflow with testmon:

```bash
# Run only tests affected by your changes
pytest --testmon
```

This is **much faster** than running all tests every time.

### 3. Write Clear Test Names

**Good test names** describe what they test:

```python
# Good: Describes what's being tested
def test_signal_with_zero_sample_rate_raises_error():
    with pytest.raises(ValueError):
        Signal(sample_rate=0)

# Bad: Unclear what this tests
def test_signal1():
    Signal(sample_rate=0)
```

### 4. Keep Tests Independent

Each test should work on its own:

```python
# Good: Test creates its own data
def test_frequency_measurement():
    signal = generate_sine_wave(frequency=1000)
    measured = measure_frequency(signal)
    assert measured == 1000

# Bad: Depends on global state
GLOBAL_SIGNAL = None

def test_create_signal():
    global GLOBAL_SIGNAL
    GLOBAL_SIGNAL = generate_sine_wave(frequency=1000)

def test_measure():  # Fails if test_create_signal didn't run!
    measured = measure_frequency(GLOBAL_SIGNAL)
    assert measured == 1000
```

### 5. Use Fixtures for Shared Setup

Instead of duplicating setup code:

```python
import pytest

@pytest.fixture
def sine_signal():
    """Create a 1kHz sine wave for testing."""
    return generate_sine_wave(frequency=1000, duration=1.0)

def test_frequency(sine_signal):
    """Test uses fixture automatically."""
    freq = measure_frequency(sine_signal)
    assert freq == 1000

def test_amplitude(sine_signal):
    """Different test, same fixture."""
    amp = measure_amplitude(sine_signal)
    assert amp > 0
```

### 6. Mark Slow Tests

Help others (and CI) skip slow tests:

```python
@pytest.mark.slow
def test_large_dataset():
    """This takes 10 seconds."""
    signal = generate_signal(duration=3600)  # 1 hour of data
    result = process(signal)
    assert result is not None
```

Run without slow tests:

```bash
pytest -m "not slow"  # Much faster!
```

### 7. Check Test Isolation

Before pushing, verify tests don't depend on each other:

```bash
# Check isolation for sample of test files
python scripts/check_test_isolation.py --sample 5
```

If this fails, your tests share state and need fixing.

### 8. Write Docstrings

Explain what each test verifies:

```python
def test_uart_decoder_with_parity():
    """Test UART decoder correctly handles even parity bit.

    Verifies that decoder detects parity errors when
    even parity is enabled and bit is corrupted.
    """
    # Test implementation...
```

## Next Steps

### Congratulations!

You now know the basics of testing in TraceKit. Here's what to explore next:

**For more testing details:**

- [Full Testing Guide](./index.md) - Comprehensive testing documentation
- [OOM Prevention](./oom-prevention.md) - Memory management in tests
- [Hypothesis Testing Guide](https://github.com/lair-click-bats/tracekit/blob/main/tests/HYPOTHESIS_TESTING_GUIDE.md) - Property-based testing

**For writing tests:**

- Look at existing tests in `tests/unit/` for examples
- Read [pytest documentation](https://docs.pytest.org/) for advanced features
- Study fixtures in `tests/conftest.py`

**For debugging:**

- Practice using VS Code debugger (it's powerful!)
- Learn [pytest debugging flags](https://docs.pytest.org/en/stable/how-to/failures.html)
- Check out [pdb tutorial](https://docs.python.org/3/library/pdb.html)

### Quick Reference Card

**Essential Commands:**

```bash
# Run tests
pytest tests/unit                      # All unit tests
pytest tests/unit -v                   # Verbose output
pytest tests/unit -x                   # Stop at first failure
pytest tests/unit -k "pattern"         # Run tests matching pattern

# Incremental testing (faster)
pytest --testmon                       # Only run affected tests

# Debugging
pytest tests/unit -s                   # Show print statements
pytest tests/unit --pdb               # Drop into debugger on failure
pytest tests/unit -v --tb=short       # Short traceback

# Coverage
pytest tests/unit --cov=src/tracekit  # Coverage report

# Markers
pytest -m unit                         # Run unit tests only
pytest -m "not slow"                   # Skip slow tests
pytest --markers                       # List all markers

# Parallel execution
pytest tests/unit -n 4                 # Use 4 workers
pytest tests/unit -n auto              # Auto-detect CPUs
```

**VS Code Shortcuts:**

- **F5** - Start debugging current test file
- **F9** - Toggle breakpoint
- **F10** - Step over (during debugging)
- **F11** - Step into (during debugging)
- **Shift+F5** - Stop debugging

### Getting Help

- **Documentation**: Check [testing documentation](./index.md) for detailed guides
- **Examples**: Look at existing tests in `tests/unit/`
- **pytest docs**: https://docs.pytest.org/
- **VS Code testing**: https://code.visualstudio.com/docs/python/testing

### Common Gotchas

**Problem: Tests pass alone but fail together**

**Solution**: Tests share state. Use fixtures to isolate data.

```bash
# Check isolation
python scripts/check_test_isolation.py --sample 5
```

**Problem: Tests are slow**

**Solution**: Use incremental testing or skip slow tests.

```bash
# Incremental testing
pytest --testmon

# Skip slow tests
pytest -m "not slow"
```

**Problem: Can't see print output**

**Solution**: Use `-s` flag.

```bash
pytest tests/unit -s
```

**Problem: Coverage seems wrong**

**Solution**: Make sure you're testing the right path.

```bash
# Specify source explicitly
pytest tests/unit --cov=src/tracekit --cov-report=term-missing
```

**Problem: Tests hang or timeout**

**Solution**: Add timeout or check for infinite loops.

```bash
# Run with 10 second timeout
pytest tests/unit --timeout=10
```

---

**Ready to write your first test?** Start by copying an existing test file as a template, then modify it for your needs. Happy testing!
