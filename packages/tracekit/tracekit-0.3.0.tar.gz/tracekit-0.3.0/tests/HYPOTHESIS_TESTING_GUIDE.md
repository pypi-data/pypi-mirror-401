# Hypothesis Property-Based Testing Guide

This guide explains how to use Hypothesis for property-based testing in the TraceKit project.

## Table of Contents

- [What is Property-Based Testing?](#what-is-property-based-testing)
- [When to Use Hypothesis](#when-to-use-hypothesis)
- [Available Custom Strategies](#available-custom-strategies)
- [Writing Good Properties](#writing-good-properties)
- [Common Patterns](#common-patterns)
- [Examples from the Codebase](#examples-from-the-codebase)
- [Running Hypothesis Tests](#running-hypothesis-tests)
- [Troubleshooting](#troubleshooting)

## What is Property-Based Testing?

Property-based testing automatically generates test cases to verify that properties (invariants) hold for a wide range of inputs. Instead of writing specific test cases like:

```python
def test_reverse_specific():
    assert reverse([1, 2, 3]) == [3, 2, 1]
```

You write properties that should always be true:

```python
@given(lst=st.lists(st.integers()))
def test_reverse_involutive(lst):
    """Property: Reversing twice returns original list."""
    assert reverse(reverse(lst)) == lst
```

Hypothesis automatically generates hundreds of different lists to test this property.

## When to Use Hypothesis

Use Hypothesis when testing:

- **Algorithms**: Sorting, searching, parsing, encoding/decoding
- **Mathematical properties**: Commutativity, associativity, identity elements
- **Invariants**: Data structure properties that must always hold
- **Edge cases**: Automatically discover boundary conditions
- **Roundtrip properties**: Serialize/deserialize, encode/decode
- **Idempotence**: Operations that can be applied multiple times without changing result

## Available Custom Strategies

TraceKit provides custom strategies in `tests/hypothesis_strategies.py`:

### Signal Generation

```python
from tests.hypothesis_strategies import digital_signals, analog_waveforms

@given(signal=digital_signals(min_length=100, max_length=1000))
def test_signal_processing(signal):
    # Test with generated digital signals
    pass
```

Available signal strategies:

- `digital_signals()` - Digital (0/3.3V) signals with optional noise
- `analog_waveforms()` - Continuous analog waveforms
- `edge_lists()` - Sorted lists of edge timestamps
- `clock_signals()` - Clock-like periodic signals
- `noisy_digital_signal()` - Digital signals with added noise

### Protocol Messages

```python
from tests.hypothesis_strategies import protocol_messages, message_streams

@given(msg=protocol_messages(header_size=(2,4), payload_size=(1,64)))
def test_packet_parsing(msg):
    # Test with generated protocol messages
    pass
```

Available protocol strategies:

- `protocol_messages()` - Single messages with header and payload
- `message_streams()` - Multiple messages concatenated
- `checksum_data()` - Data for checksum testing
- `packet_data()` - Network packet data
- `framing_data()` - Framed data with delimiters

### Inference and Analysis

```python
from tests.hypothesis_strategies import (
    state_machine_samples,
    alignment_sequences,
    clustering_data
)
```

Available analysis strategies:

- `state_machine_samples()` - Sequences for state machine learning
- `alignment_sequences()` - Pairs of sequences for alignment
- `clustering_data()` - Multi-dimensional data points
- `entropy_data()` - Data for entropy calculation
- `ngram_sequences()` - Sequences for n-gram analysis
- `pattern_sequences()` - Sequences for pattern detection
- `repetitive_sequences()` - Sequences with repeated patterns

### Frequency and Spectral

```python
from tests.hypothesis_strategies import frequency_data, jitter_samples
```

Available spectral strategies:

- `frequency_data()` - Frequency domain data (frequencies, magnitudes)
- `jitter_samples()` - Timing jitter measurements
- `power_traces()` - Power consumption traces

### Metadata and Configuration

```python
from tests.hypothesis_strategies import waveform_metadata, timing_parameters
```

Available metadata strategies:

- `waveform_metadata()` - Realistic waveform metadata dictionaries
- `timing_parameters()` - Timing analysis parameters

## Writing Good Properties

### 1. Think in Terms of Invariants

Good properties express invariants that must always hold:

```python
@given(data=entropy_data())
def test_entropy_bounded(data):
    """Property: Entropy is always between 0 and 8 bits."""
    entropy = calculate_entropy(data)
    assert 0.0 <= entropy <= 8.0
```

### 2. Use Assume to Filter Invalid Inputs

Use `assume()` to skip invalid test cases:

```python
@given(
    seq_a=st.binary(min_size=1, max_size=100),
    seq_b=st.binary(min_size=1, max_size=100)
)
def test_alignment_commutative(seq_a, seq_b):
    """Property: align(A,B) and align(B,A) have same score."""
    assume(len(seq_a) >= 5 and len(seq_b) >= 5)  # Skip too-short sequences

    result_ab = align_global(seq_a, seq_b)
    result_ba = align_global(seq_b, seq_a)

    assert result_ab.score == pytest.approx(result_ba.score)
```

### 3. Test Mathematical Properties

Common mathematical properties to test:

**Identity**: `f(identity) = identity`

```python
@given(signal=digital_signals())
def test_filter_with_identity(signal):
    """Property: Filtering with identity kernel returns original."""
    identity_filter = [1.0]
    filtered = apply_filter(signal, identity_filter)
    assert np.allclose(signal, filtered)
```

**Commutativity**: `f(a, b) = f(b, a)`

```python
@given(a=st.floats(...), b=st.floats(...))
def test_addition_commutative(a, b):
    assert a + b == pytest.approx(b + a)
```

**Associativity**: `f(f(a, b), c) = f(a, f(b, c))`

**Idempotence**: `f(f(x)) = f(x)`

```python
@given(data=st.binary())
def test_normalization_idempotent(data):
    """Property: Normalizing twice = normalizing once."""
    normalized_once = normalize(data)
    normalized_twice = normalize(normalized_once)
    assert normalized_once == normalized_twice
```

**Inverse**: `f(f_inverse(x)) = x`

```python
@given(signal=analog_waveforms())
def test_fft_roundtrip(signal):
    """Property: IFFT(FFT(signal)) = signal."""
    fft_result = np.fft.fft(signal)
    recovered = np.fft.ifft(fft_result)
    assert np.allclose(signal, recovered.real)
```

### 4. Test Boundary Conditions

Hypothesis automatically finds edge cases, but you can guide it:

```python
@given(length=st.integers(min_value=0, max_value=10000))
def test_handles_empty_and_large(length):
    """Property: Function handles empty and large inputs."""
    data = bytes([0] * length)
    result = process(data)

    if length == 0:
        assert result is not None  # Empty input handled
    else:
        assert len(result) > 0  # Non-empty produces output
```

### 5. Use Deterministic Assertions

Avoid assertions that can randomly fail:

```python
# BAD - can fail due to randomness
@given(data=st.binary())
def test_random_bad(data):
    result = random_process(data)
    assert result > 0  # Might randomly be 0!

# GOOD - deterministic assertion
@given(data=st.binary())
def test_deterministic_good(data):
    result1 = hash_function(data)
    result2 = hash_function(data)
    assert result1 == result2  # Deterministic
```

## Common Patterns

### Pattern 1: Roundtrip Testing

Test that encode/decode or save/load preserves data:

```python
@given(data=st.binary())
def test_roundtrip(data):
    """Property: Decode(encode(data)) = data."""
    encoded = encode(data)
    decoded = decode(encoded)
    assert data == decoded
```

### Pattern 2: Bounds Checking

Ensure outputs are within valid ranges:

```python
@given(signal=digital_signals())
def test_correlation_bounded(signal):
    """Property: Correlation coefficient is between -1 and 1."""
    corr = np.corrcoef(signal, signal)[0, 1]
    assert -1.0 <= corr <= 1.0
```

### Pattern 3: Consistency Across Representations

Test that different input formats produce same results:

```python
@given(data=st.binary())
def test_accepts_bytes_and_arrays(data):
    """Property: Function handles both bytes and arrays."""
    result_bytes = process(data)
    result_array = process(np.frombuffer(data, dtype=np.uint8))
    assert result_bytes == result_array
```

### Pattern 4: Comparative Properties

Compare with a simpler (but slower) reference implementation:

```python
@given(data=st.lists(st.integers()))
def test_optimized_vs_simple(data):
    """Property: Optimized version matches simple version."""
    result_fast = fast_sort(data)
    result_simple = sorted(data)  # Python's built-in
    assert result_fast == result_simple
```

### Pattern 5: Monotonicity

Test that outputs preserve ordering:

```python
@given(
    threshold1=st.floats(min_value=0, max_value=5),
    threshold2=st.floats(min_value=0, max_value=5)
)
def test_threshold_monotonic(threshold1, threshold2):
    """Property: Higher threshold means fewer detections."""
    assume(threshold1 < threshold2)

    edges1 = detect_edges(signal, threshold=threshold1)
    edges2 = detect_edges(signal, threshold=threshold2)

    assert len(edges1) >= len(edges2)
```

## Examples from the Codebase

### Example 1: Message Format Inference

```python
# File: tests/unit/inference/test_message_format_hypothesis.py

@given(
    num_messages=st.integers(min_value=10, max_value=50),
    msg_length=st.integers(min_value=10, max_value=100),
)
@settings(max_examples=50, deadline=None)
def test_inferred_schema_total_size_matches_input(
    num_messages: int, msg_length: int
) -> None:
    """Property: Inferred schema total_size equals input message length."""
    rng = np.random.default_rng(42)
    messages = [
        rng.integers(0, 256, msg_length, dtype=np.uint8).tobytes()
        for _ in range(num_messages)
    ]

    schema = infer_format(messages, min_samples=10)

    assert schema.total_size == msg_length
```

### Example 2: Entropy Calculation

```python
# File: tests/unit/analyzers/statistical/test_entropy_hypothesis.py

@given(length=st.integers(min_value=100, max_value=1000))
@settings(max_examples=50, deadline=None)
def test_constant_data_zero_entropy(length: int) -> None:
    """Property: Constant data has zero entropy."""
    data = bytes([42] * length)
    entropy = calculate_entropy(data)
    assert entropy == pytest.approx(0.0, abs=1e-6)
```

### Example 3: Alignment Properties

```python
# File: tests/unit/inference/test_alignment_hypothesis.py

@given(seq_len=st.integers(min_value=5, max_value=50))
@settings(max_examples=50, deadline=None)
def test_identical_sequences_perfect_alignment(seq_len: int) -> None:
    """Property: Identical sequences have 100% identity."""
    rng = np.random.default_rng(42)
    seq = rng.integers(0, 256, seq_len, dtype=np.uint8).tobytes()

    result = align_global(seq, seq)

    assert result.identity == pytest.approx(1.0, abs=0.01)
    assert result.similarity >= 0.99
    assert result.gaps == 0
```

## Running Hypothesis Tests

### Run All Hypothesis Tests

```bash
# Run all tests marked with hypothesis
uv run pytest -m hypothesis -v

# With coverage
uv run pytest -m hypothesis --cov=src/tracekit --cov-report=term-missing
```

### Run Specific Test Files

```bash
# Run specific hypothesis test file
uv run pytest tests/unit/inference/test_message_format_hypothesis.py -v

# Run specific test
uv run pytest tests/unit/inference/test_message_format_hypothesis.py::TestMessageFormatInferenceProperties::test_entropy_values_within_bounds -v
```

### Using Different Profiles

Hypothesis profiles are registered in `tests/conftest.py`:

```bash
# Fast profile (20 examples)
uv run pytest -m hypothesis --hypothesis-profile=fast

# CI profile (500 examples, deterministic)
uv run pytest -m hypothesis --hypothesis-profile=ci

# Debug profile (verbose output)
uv run pytest -m hypothesis --hypothesis-profile=debug
```

### CI Integration

Hypothesis tests are integrated into the CI/CD pipeline with optimized settings:

#### Profile Configuration

Hypothesis profiles are registered in `tests/conftest.py` using the `pytest_configure` hook:

- **default**: 100 examples, normal verbosity (local development)
- **fast**: 20 examples with 1s deadline (quick feedback)
- **ci**: 500 examples, optimized for CI (see details below)
- **debug**: 10 examples with verbose output (debugging)

**CI Profile Optimizations** (500 examples, scientificcomputing-optimized):

- `derandomize=True` - Reproducible test failures
- `deadline=2000` - 2 seconds per example (sufficient for FFT, correlation, signal processing)
- `database=None` - Disabled for parallel execution safety (no file locking conflicts)
- `print_blob=True` - Better failure reproduction information
- `suppress_health_check=[too_slow]` - 500 examples legitimately take time
- Full shrinking enabled - Minimal failing examples for easier debugging

The CI pipeline automatically uses the `ci` profile for thorough testing with optimized parallel execution:

```yaml
# .github/workflows/ci.yml
# Memory-aware worker allocation:
# - analyzers group: 2 workers (large signal arrays)
# - non-unit-tests: 2 workers (real capture files)
# - other groups: 4 workers (standard memory usage)

uv run pytest tests/ \
-n 4 \
--maxprocesses=4 \
--dist loadfile \
--hypothesis-profile=ci \
--benchmark-disable \
--cov-fail-under=75 \
--durations=10
```

#### Example Database Behavior

The `.hypothesis/` directory contains the example database - a cache of previously discovered failing test cases.

**Local Development:**

- Database is **enabled** by default
- Stores failing examples for replay
- Automatically created in `.hypothesis/examples/`
- Gitignored (in `.gitignore` line 186)

**CI Environment:**

- Database is **disabled** (`database=None` in CI profile)
- Rationale: Avoids file locking conflicts with parallel execution (`-n 4`)
- Trade-off: No example caching, but ensures consistent parallel performance
- GitHub Actions cache still stores `.hypothesis/` directory for potential future use

#### Running Tests Locally vs CI

```bash
# Local development (100 examples)
uv run pytest -m hypothesis -v

# Quick feedback (20 examples)
uv run pytest -m hypothesis --hypothesis-profile=fast

# CI simulation (500 examples, deterministic)
uv run pytest -m hypothesis --hypothesis-profile=ci

# Debug with verbose output (10 examples)
uv run pytest -m hypothesis --hypothesis-profile=debug
```

### Reproducing Failures

Hypothesis prints a seed when a test fails:

```
Falsifying example: test_something(data=...)
You can reproduce this example by temporarily adding @reproduce_failure('6.148.8', b'AXJbVA==') as a decorator
```

Add the decorator to reproduce:

```python
from hypothesis import reproduce_failure

@reproduce_failure('6.148.8', b'AXJbVA==')
@given(data=st.binary())
def test_something(data):
    ...
```

## Troubleshooting

### Tests Taking Too Long

Reduce number of examples:

```python
@given(data=st.binary())
@settings(max_examples=10)  # Default is 100
def test_slow_operation(data):
    ...
```

Or disable deadline:

```python
@given(data=st.binary())
@settings(deadline=None)  # No time limit per test
def test_complex_operation(data):
    ...
```

### Too Many Invalid Examples

If Hypothesis skips many examples due to `assume()`:

```python
# BAD - skips too many
@given(x=st.integers(min_value=0, max_value=1000))
def test_primes(x):
    assume(is_prime(x))  # Skips most numbers
    ...

# GOOD - generate primes directly
@given(x=st.sampled_from([2, 3, 5, 7, 11, 13, 17, 19, 23, 29]))
def test_primes(x):
    ...
```

### Flaky Tests

If tests pass sometimes and fail other times:

1. Use `derandomize=True` in settings
2. Fix any non-deterministic code
3. Use `@seed()` decorator to fix randomness

```python
@given(data=st.binary())
@settings(derandomize=True)
def test_deterministic(data):
    ...
```

### Health Checks

Disable health checks if needed:

```python
from hypothesis import settings, HealthCheck

@given(data=st.binary())
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_legitimately_slow(data):
    ...
```

## Best Practices

1. **Start Simple**: Begin with simple properties, add complexity gradually
2. **One Property Per Test**: Each test should verify one specific property
3. **Use Descriptive Names**: Test names should describe the property being tested
4. **Document Properties**: Use docstrings to explain what property is being tested
5. **Combine with Unit Tests**: Use both property-based and example-based tests
6. **Run in CI**: Include hypothesis tests in continuous integration
7. **Monitor Performance**: Keep track of test execution time
8. **Share Strategies**: Reuse custom strategies across tests

## Further Reading

- [Hypothesis Documentation](https://hypothesis.readthedocs.io/)
- [Property-Based Testing with Hypothesis (Tutorial)](https://hypothesis.works/articles/getting-started-with-hypothesis/)
- [What is Property Based Testing?](https://hypothesis.works/articles/what-is-property-based-testing/)
- [Choosing Properties for Property-Based Testing](https://fsharpforfunandprofit.com/posts/property-based-testing-2/)

## Getting Help

- Check existing hypothesis tests in `tests/unit/*/test_*_hypothesis.py`
- Review custom strategies in `tests/hypothesis_strategies.py`
- Consult the Hypothesis documentation
- Ask in project discussions or issues
