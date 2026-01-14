# NaN Handling Guide

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08

Understanding and handling NaN (Not a Number) results in TraceKit measurements.

## Why Measurements Return NaN

TraceKit returns `float('nan')` when a measurement cannot be computed meaningfully. This is **by design** - it's better to indicate "no valid result" than to return an incorrect value.

### Common Causes

| Measurement            | NaN Cause                   |
| ---------------------- | --------------------------- |
| `measure_frequency()`  | DC signal (no transitions)  |
| `measure_rise_time()`  | No rising edge found        |
| `measure_duty_cycle()` | No complete cycles          |
| `measure_period()`     | Fewer than 2 edges detected |
| `measure_snr()`        | Signal frequency not found  |
| `measure_thd()`        | No fundamental detected     |

## Checking for NaN

### Using math.isnan()

```python
import math
import tracekit as tk

trace = tk.load("capture.wfm")
freq = tk.measure_frequency(trace)

if math.isnan(freq):
    print("Frequency measurement returned NaN")
else:
    print(f"Frequency: {freq / 1e6:.3f} MHz")
```

### Using numpy.isnan()

```python
import numpy as np

freq = tk.measure_frequency(trace)
if np.isnan(freq):
    print("No valid frequency")
```

## Handling Strategies

### Strategy 1: Provide Default Value

```python
def safe_measure_frequency(trace, default=0.0):
    """Measure frequency with default fallback."""
    freq = tk.measure_frequency(trace)
    return default if math.isnan(freq) else freq

freq = safe_measure_frequency(trace, default=0.0)
```

### Strategy 2: Raise Exception

```python
def strict_measure_frequency(trace):
    """Measure frequency, raise if invalid."""
    freq = tk.measure_frequency(trace)
    if math.isnan(freq):
        raise ValueError("Cannot measure frequency: signal may be DC or too noisy")
    return freq

try:
    freq = strict_measure_frequency(trace)
except ValueError as e:
    print(f"Measurement failed: {e}")
```

### Strategy 3: Try Alternative Methods

```python
def robust_measure_frequency(trace):
    """Try multiple methods to measure frequency."""
    # Method 1: Standard measurement
    freq = tk.measure_frequency(trace)
    if not math.isnan(freq):
        return freq

    # Method 2: FFT-based
    from tracekit.analyzers.spectral import compute_fft
    spectrum = compute_fft(trace)
    peak_idx = spectrum.magnitude_db.argmax()
    freq = spectrum.frequencies[peak_idx]
    if freq > 0:
        return freq

    # Method 3: Edge-based
    edges = tk.find_edges(trace)
    rising = [(t, typ) for t, typ in edges if typ == "rising"]
    if len(rising) >= 2:
        period = rising[1][0] - rising[0][0]
        return 1.0 / period

    return float("nan")
```

### Strategy 4: Diagnose the Issue

```python
def diagnose_frequency_nan(trace):
    """Explain why frequency measurement failed."""
    freq = tk.measure_frequency(trace)
    if not math.isnan(freq):
        return f"Frequency: {freq / 1e6:.3f} MHz"

    # Check for DC signal
    stats = tk.analyze_amplitude(trace)
    if stats.peak_to_peak < 0.01:  # Less than 10mV
        return "NaN: Signal appears to be DC (no amplitude variation)"

    # Check for edges
    edges = tk.find_edges(trace)
    if len(edges) == 0:
        return "NaN: No edges detected (threshold may need adjustment)"
    if len(edges) == 1:
        return "NaN: Only one edge detected (need at least 2 for period)"

    # Check edge timing
    rising = [t for t, typ in edges if typ == "rising"]
    if len(rising) < 2:
        return "NaN: No complete period (need 2+ rising edges)"

    # If edges exist but frequency still NaN
    return "NaN: Unknown cause - edges exist but period calculation failed"

result = diagnose_frequency_nan(trace)
print(result)
```

## Per-Measurement Guidance

### Frequency Measurement

**Returns NaN when:**

- Signal is DC (constant value)
- Threshold doesn't produce valid crossings
- Signal period exceeds capture duration

**Solutions:**

```python
# 1. Check signal has variation
stats = tk.analyze_amplitude(trace)
if stats.peak_to_peak > 0.1:  # At least 100mV swing
    freq = tk.measure_frequency(trace)

# 2. Adjust threshold
freq = tk.measure_frequency(trace, threshold=0.3)

# 3. Use FFT for noisy signals
from tracekit.analyzers.spectral import compute_fft
spectrum = compute_fft(trace)
peak_freq = spectrum.frequencies[spectrum.magnitude_db.argmax()]
```

### Rise Time Measurement

**Returns NaN when:**

- No rising edges in signal
- Signal is DC or falling only
- Rise is too fast for sample rate

**Solutions:**

```python
# 1. Verify signal type
edges = tk.find_edges(trace)
rising_edges = [e for e in edges if e[1] == "rising"]
if rising_edges:
    rise = tk.measure_rise_time(trace)

# 2. Adjust threshold levels
rise = tk.measure_rise_time(trace, low=0.2, high=0.8)

# 3. Verify sample rate is adequate
# Rise time needs >5 samples to measure accurately
min_rise = 5 / trace.metadata.sample_rate
print(f"Minimum measurable rise time: {min_rise * 1e9:.1f} ns")
```

### Duty Cycle Measurement

**Returns NaN when:**

- No complete cycles captured
- Signal is DC
- Threshold doesn't produce valid crossings

**Solutions:**

```python
# 1. Check for complete cycles
duration = trace.duration
expected_period = 1e-6  # Expected 1 MHz = 1 us period
if duration > 2 * expected_period:
    duty = tk.measure_duty_cycle(trace)

# 2. Verify edges exist
edges = tk.find_edges(trace)
if len(edges) >= 3:  # Need at least rise-fall-rise
    duty = tk.measure_duty_cycle(trace)
```

### SNR Measurement

**Returns NaN when:**

- Signal frequency not specified or detected
- Signal amplitude too low
- Noise floor higher than signal

**Solutions:**

```python
# 1. Specify signal frequency explicitly
snr = tk.measure_snr(trace, signal_freq=1e6)

# 2. Find fundamental first
spectrum = compute_fft(trace)
fundamental = spectrum.frequencies[spectrum.magnitude_db.argmax()]
snr = tk.measure_snr(trace, signal_freq=fundamental)
```

## Batch Processing with NaN Handling

When processing multiple files, track NaN results:

```python
from pathlib import Path
import math

results = []
nan_files = []

for file_path in Path("captures/").glob("*.wfm"):
    trace = tk.load(file_path)
    freq = tk.measure_frequency(trace)

    if math.isnan(freq):
        nan_files.append(file_path.name)
        results.append({"file": file_path.name, "frequency": None, "status": "NaN"})
    else:
        results.append({"file": file_path.name, "frequency": freq, "status": "OK"})

print(f"Processed {len(results)} files")
print(f"NaN results: {len(nan_files)}")
if nan_files:
    print("Files with NaN:")
    for f in nan_files:
        print(f"  - {f}")
```

## NaN-Safe Analysis Functions

TraceKit provides NaN-safe variants for common workflows:

```python
from tracekit.analyzers import safe_measure_all

# Returns dict with None instead of NaN
results = safe_measure_all(trace)
# {
#     "frequency": 1000000.0,  # or None if NaN
#     "amplitude": 2.5,
#     "rise_time": None,       # Was NaN
#     "duty_cycle": 0.5,
# }

# Check which measurements succeeded
for name, value in results.items():
    if value is not None:
        print(f"{name}: {value}")
    else:
        print(f"{name}: Could not measure")
```

## Reporting NaN in Results

When generating reports, handle NaN appropriately:

```python
from tracekit.reporting import generate_report

# Reports automatically handle NaN
report = generate_report(trace)
# NaN measurements shown as "N/A" or "--" in report

# Or exclude NaN measurements
from tracekit.reporting import ReportConfig

config = ReportConfig(
    exclude_nan_measurements=True  # Don't show NaN results
)
report = generate_report(trace, config=config)
```

## Debugging NaN Issues

### Enable Verbose Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

import tracekit as tk
trace = tk.load("problematic.wfm")
freq = tk.measure_frequency(trace)
# Debug logs show why measurement returned NaN
```

### Signal Inspection

```python
def inspect_signal(trace):
    """Print signal characteristics to debug NaN."""
    print("=== Signal Inspection ===")
    print(f"Samples: {len(trace.data)}")
    print(f"Sample rate: {trace.metadata.sample_rate / 1e6:.1f} MSa/s")
    print(f"Duration: {trace.duration * 1e6:.1f} us")

    stats = tk.analyze_amplitude(trace)
    print(f"\nAmplitude stats:")
    print(f"  Min: {stats.minimum:.3f} V")
    print(f"  Max: {stats.maximum:.3f} V")
    print(f"  P-P: {stats.peak_to_peak:.3f} V")
    print(f"  Mean: {stats.mean:.3f} V")
    print(f"  RMS: {stats.rms:.3f} V")

    edges = tk.find_edges(trace)
    print(f"\nEdge detection:")
    print(f"  Total edges: {len(edges)}")
    rising = sum(1 for _, t in edges if t == "rising")
    falling = sum(1 for _, t in edges if t == "falling")
    print(f"  Rising: {rising}")
    print(f"  Falling: {falling}")

inspect_signal(trace)
```

## See Also

- [Troubleshooting Guide](troubleshooting.md)
- [Tutorial 2: Basic Measurements](../tutorials/02-basic-measurements.md)
- [Error Codes Reference](../error-codes.md)

---

<!-- Content merged from docs/NAN_RESULTS_GUIDE.md -->

# NaN Results Guide

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08

## Overview

TraceKit measurement functions return `np.nan` (Not-a-Number) when a measurement cannot be computed due to signal characteristics, insufficient data, or incompatible signal types. This guide explains when and why measurements return NaN, how to handle these cases, and how to choose appropriate measurements for your signals.

## Table of Contents

- [Understanding NaN Results](#understanding-nan-results)
- [Signal Compatibility Matrix](#signal-compatibility-matrix)
- [Measurement-Specific NaN Conditions](#measurement-specific-nan-conditions)
- [Troubleshooting Guide](#troubleshooting-guide)
- [Best Practices](#best-practices)
- [Code Examples](#code-examples)

## Understanding NaN Results

NaN results indicate that a measurement is **not applicable** or **cannot be computed** for the given signal. This is not an error - it's TraceKit's way of telling you that the measurement doesn't make sense for your particular signal.

### Why NaN Instead of Exceptions?

TraceKit uses NaN for incompatible measurements rather than raising exceptions because:

1. **Batch processing**: When analyzing multiple signals, you can continue processing even if some measurements fail
2. **Discovery mode**: You can run all measurements and see which ones apply to your signal
3. **Flexibility**: NaN is a standard IEEE 754 value that integrates well with NumPy and scientific computing workflows

### Common Reasons for NaN Results

1. **Insufficient edges**: Digital timing measurements need edges (transitions)
2. **Non-periodic signals**: Frequency/period measurements need repeating patterns
3. **DC signals**: AC measurements (frequency, duty cycle) don't apply to constant signals
4. **Insufficient data**: Statistical measurements need minimum sample counts
5. **Signal type mismatch**: Applying digital measurements to analog noise, or vice versa

## Signal Compatibility Matrix

Use this matrix to quickly determine which measurements apply to your signal type:

| Measurement           | Periodic Digital | Aperiodic Digital | DC Signal | Analog AC | Noisy/Random |
| --------------------- | ---------------- | ----------------- | --------- | --------- | ------------ |
| `rise_time()`         | ✓                | ✓                 | ✗         | ✓         | ✗            |
| `fall_time()`         | ✓                | ✓                 | ✗         | ✓         | ✗            |
| `period()`            | ✓                | ✗                 | ✗         | ✓         | ✗            |
| `frequency()`         | ✓                | ✗                 | ✗         | ✓         | ✗            |
| `duty_cycle()`        | ✓                | ✗                 | ✗         | ✗         | ✗            |
| `pulse_width()`       | ✓                | ✓ (single)        | ✗         | ✗         | ✗            |
| `amplitude()`         | ✓                | ✓                 | ✓         | ✓         | ✓            |
| `rms()`               | ✓                | ✓                 | ✓         | ✓         | ✓            |
| `mean()`              | ✓                | ✓                 | ✓         | ✓         | ✓            |
| `overshoot()`         | ✓                | ✓                 | ✗         | ✓         | Maybe        |
| `undershoot()`        | ✓                | ✓                 | ✗         | ✓         | Maybe        |
| `slew_rate()`         | ✓                | ✓                 | ✗         | ✓         | ✗            |
| `propagation_delay()` | ✓                | ✓                 | ✗         | ✓         | ✗            |
| `setup_time()`        | ✓                | ✓                 | ✗         | ✗         | ✗            |
| `hold_time()`         | ✓                | ✓                 | ✗         | ✗         | ✗            |
| `phase()`             | ✓                | ✗                 | ✗         | ✓         | ✗            |
| `rms_jitter()`        | ✓                | ✗                 | ✗         | ✗         | ✗            |
| `eye_height()`        | ✓ (high-speed)   | ✗                 | ✗         | ✗         | ✗            |
| `eye_width()`         | ✓ (high-speed)   | ✗                 | ✗         | ✗         | ✗            |

**Legend:**

- ✓ = Measurement typically succeeds
- ✗ = Returns NaN (not applicable)
- Maybe = May return NaN depending on signal quality

## Measurement-Specific NaN Conditions

### Waveform Measurements

#### `rise_time(trace)`

**Returns NaN when:**

- No rising edges detected (DC signal, noise, or all falling edges)
- Insufficient samples (< 3 samples)
- Signal amplitude is zero or negative (flat line)
- Signal never crosses both reference levels (e.g., 10% and 90%)

**Typical causes:**

```python
# DC signal - no transitions
dc_signal = np.ones(1000) * 3.3  # Returns NaN

# Noise without clear edges
noise = np.random.randn(1000) * 0.1  # Returns NaN

# Signal with only falling edges
falling_only = np.array([3.3, 3.3, 0, 0, 3.3, 3.3, 0, 0])  # Returns NaN
```

**Suitable signals:**

- Square waves, clock signals, digital pulses
- Analog signals with clear rising transitions
- PWM signals

---

#### `fall_time(trace)`

**Returns NaN when:**

- No falling edges detected
- Insufficient samples (< 3 samples)
- Signal amplitude is zero or negative
- Signal never crosses both reference levels

**Typical causes:** Same as `rise_time()` but for falling edges

---

#### `period(trace)` and `frequency(trace)`

**Returns NaN when:**

- Fewer than 2 edges detected (non-periodic signal)
- DC signal (no transitions)
- Period is zero or negative (calculation error)
- Aperiodic/single-shot signals

**Typical causes:**

```python
# DC signal
dc = np.ones(1000) * 5.0  # Returns NaN

# Single pulse (aperiodic)
single_pulse = np.array([0]*100 + [1]*50 + [0]*100)  # Returns NaN

# Insufficient sample rate for high-frequency signal
# Nyquist violation: signal frequency > sample_rate/2
```

**Suitable signals:**

- Periodic square waves
- Clock signals
- Sine waves (with method="fft")
- PWM with constant frequency

**Special notes:**

- `frequency(method="edge")`: Needs at least 2 edges (1 complete period)
- `frequency(method="fft")`: Needs at least 16 samples, may return incorrect frequency for non-sinusoidal signals

---

#### `duty_cycle(trace)`

**Returns NaN when:**

- `pulse_width()` returns NaN (no pulses detected)
- `period()` returns NaN (non-periodic signal)
- Period is zero or negative
- No complete pulse cycles detected

**Typical causes:**

```python
# DC signal
dc_high = np.ones(1000) * 5.0  # Returns NaN

# Aperiodic signal
aperiodic = np.random.randint(0, 2, 1000)  # Returns NaN

# Insufficient edges for both period and pulse width
```

**Suitable signals:**

- Periodic PWM signals
- Clock signals
- Regular digital patterns

**Not suitable for:**

- DC signals
- Aperiodic digital patterns
- Single pulses

---

#### `pulse_width(trace)`

**Returns NaN when:**

- No rising edges found (for positive polarity)
- No falling edges found (for negative polarity)
- No complete pulses detected (edge without corresponding opposite edge)
- Signal never returns to baseline

**Typical causes:**

```python
# DC signal
dc = np.ones(1000) * 3.3  # Returns NaN

# Missing falling edge
incomplete_pulse = np.array([0]*100 + [1]*100)  # Returns NaN

# For negative pulses, needs falling then rising edges
```

---

#### `overshoot(trace)` and `undershoot(trace)`

**Returns NaN when:**

- Insufficient samples (< 3 samples)
- Signal amplitude is zero or negative
- Cannot determine high/low levels

**Returns 0.0 when:**

- No overshoot/undershoot present (normal condition)

**Typical causes for NaN:**

```python
# DC signal with no variation
dc = np.ones(1000) * 5.0  # Returns NaN (amplitude = 0)

# Completely flat signal
flat = np.zeros(1000)  # Returns NaN
```

---

#### `amplitude(trace)`, `rms(trace)`, `mean(trace)`

These rarely return NaN:

- `amplitude()`: Returns NaN only if < 2 samples
- `rms()`: Returns NaN only if 0 samples
- `mean()`: Returns NaN only if 0 samples

---

### Digital Timing Measurements

#### `propagation_delay(input_trace, output_trace)`

**Returns NaN when:**

- No edges found in input trace
- No edges found in output trace
- No output edge follows any input edge (incorrect edge matching)
- Edges present but no valid pairs detected

**Raises InsufficientDataError when:**

- Zero edges in either trace (before attempting calculation)

**Typical causes:**

```python
# DC signals
input_dc = np.ones(1000) * 0.0
output_dc = np.ones(1000) * 0.0  # Raises InsufficientDataError

# Output transitions before all input transitions
# (negative delay - no valid subsequent edges)
```

---

#### `setup_time(data_trace, clock_trace)` and `hold_time(data_trace, clock_trace)`

**Returns NaN when:**

- No clock edges detected
- No data edges detected
- No data edge precedes any clock edge (setup_time)
- No data edge follows any clock edge (hold_time)

**Typical causes:**

```python
# DC clock
dc_clock = np.ones(1000) * 3.3  # Returns NaN

# DC data
dc_data = np.ones(1000) * 3.3  # Returns NaN

# Incorrect timing relationship between signals
```

---

#### `slew_rate(trace)`

**Returns NaN when:**

- Insufficient samples (< 3)
- Signal amplitude is zero or negative
- No transitions found between reference levels
- No valid edges of specified type

---

#### `phase(trace1, trace2)`

**Returns NaN when (method="edge"):**

- Fewer than 2 edges in either trace
- Period is zero or negative
- Cannot match edges between traces

**Returns NaN when (method="fft"):**

- Fewer than 16 samples
- Signals don't share a common frequency component

**Typical causes:**

```python
# DC signals
dc1 = np.ones(1000) * 1.0
dc2 = np.ones(1000) * 2.0  # Returns NaN

# Different frequencies (edge method)
# Single pulses vs periodic signals
```

---

#### `rms_jitter(trace)` and `peak_to_peak_jitter(trace)`

**Returns NaN when:**

- Fewer than 3 edges detected
- Fewer than 2 periods calculated
- Non-periodic signal

**Typical causes:**

```python
# DC signal
dc = np.ones(1000) * 5.0  # Returns NaN

# Single pulse
single_pulse = np.array([0]*100 + [1]*50 + [0]*100)  # Returns NaN

# Aperiodic signal
random_edges = np.random.randint(0, 2, 1000)  # Returns NaN
```

---

#### `skew(traces)`

**Returns NaN for individual traces when:**

- No edges detected in that specific trace
- Cannot match edges to reference trace

**Returns NaN in results dict when:**

- No valid skew values calculated
- Reference trace has no edges

---

#### `recover_clock_fft(trace)` and `recover_clock_edge(trace)`

**Returns ClockRecoveryResult with NaN when:**

- Insufficient samples (< 16 for FFT, < 3 edges for edge method)
- No valid frequency peak found in specified range (FFT)
- No periods calculated (edge method)

---

### Eye Diagram Measurements

#### `eye_height(eye)` and `eye_width(eye)`

**Returns NaN when:**

- No eye opening detected (all transitions overlap)
- Cannot separate logic high from logic low levels
- Insufficient data to determine distributions

**Typical causes:**

- Excessive jitter (closed eye)
- Low-quality signal (no clear separation)
- Incorrect eye diagram parameters

---

### Power Analysis Measurements

#### `ripple_percentage(trace)`

**Returns (NaN, NaN) when:**

- DC level is exactly zero (division by zero)

**Typical causes:**

```python
# Signal centered at zero
centered = np.sin(np.linspace(0, 10*np.pi, 1000))  # Returns (NaN, NaN)
```

---

## Troubleshooting Guide

### Step-by-Step Diagnostic Process

When you get an unexpected NaN result, follow this process:

#### 1. Check Your Signal Type

```python
import numpy as np
import tracekit as tk

# Visualize your signal first
import matplotlib.pyplot as plt
plt.plot(trace.data)
plt.title("Signal Overview")
plt.show()

# Check basic statistics
print(f"Min: {np.min(trace.data)}")
print(f"Max: {np.max(trace.data)}")
print(f"Mean: {np.mean(trace.data)}")
print(f"Std: {np.std(trace.data)}")
print(f"Samples: {len(trace.data)}")
```

**Decision tree:**

- Is min ≈ max? → **DC signal** - use `mean()`, `rms()` only
- Is std very small? → **Near-DC signal** - frequency/period won't work
- Are there clear high/low levels? → **Digital signal** - try edge-based measurements
- Is it continuous variation? → **Analog signal** - try FFT-based measurements
- Is std very large relative to mean? → **Noise** - limited measurements available

#### 2. Check for Edges

```python
from tracekit.analyzers.waveform.measurements import _find_levels, _find_edges

# Check if edges can be detected
data = trace.data
low, high = _find_levels(data)
print(f"Low level: {low}, High level: {high}")
print(f"Amplitude: {high - low}")

# Try to find edges
edges = _find_edges(trace, "rising")
print(f"Rising edges found: {len(edges)}")
edges = _find_edges(trace, "falling")
print(f"Falling edges found: {len(edges)}")
```

**What to look for:**

- **0 edges**: Signal is DC or pure noise - can't use timing measurements
- **1 edge**: Single transition - can use rise/fall time but not period
- **2-3 edges**: One complete cycle - period may be calculable, but jitter measurements won't work
- **Many edges**: Most measurements should work

#### 3. Check Sample Rate vs Signal Frequency

```python
sample_rate = trace.metadata.sample_rate
signal_duration = len(trace.data) / sample_rate

print(f"Sample rate: {sample_rate:.3e} Hz")
print(f"Duration: {signal_duration:.3e} s")
print(f"Nyquist frequency: {sample_rate/2:.3e} Hz")

# Estimate signal frequency from edges
edges = _find_edges(trace, "rising")
if len(edges) >= 2:
    periods = np.diff(edges)
    est_freq = 1.0 / np.mean(periods)
    print(f"Estimated signal frequency: {est_freq:.3e} Hz")
    print(f"Samples per period: {sample_rate / est_freq:.1f}")
```

**Rules of thumb:**

- Need at least **10-20 samples per period** for accurate timing measurements
- Signal frequency must be < Nyquist frequency (sample_rate / 2)
- For rise time: need at least **5-10 samples** across the transition

#### 4. Try Alternative Measurement Methods

```python
# If edge-based frequency fails, try FFT
freq_edge = tk.frequency(trace, method="edge")
if np.isnan(freq_edge):
    freq_fft = tk.frequency(trace, method="fft")
    if not np.isnan(freq_fft):
        print(f"FFT method succeeded: {freq_fft:.3e} Hz")
    else:
        print("Signal is not periodic")
```

#### 5. Check Data Length

```python
print(f"Data points: {len(trace.data)}")

if len(trace.data) < 16:
    print("⚠ Insufficient data for FFT-based measurements (need >= 16)")
if len(trace.data) < 3:
    print("⚠ Insufficient data for most measurements (need >= 3)")
```

### Common Scenarios and Solutions

#### Scenario 1: "My PWM signal returns NaN for duty_cycle()"

**Possible causes:**

1. Signal is not periodic (variable duty cycle or frequency)
2. Insufficient edges detected
3. Sample rate too low

**Solution:**

```python
# Check if signal is periodic
periods = tk.period(trace, return_all=True)
if len(periods) > 0:
    print(f"Period variation: {np.std(periods) / np.mean(periods) * 100:.1f}%")
    if np.std(periods) / np.mean(periods) > 0.1:
        print("⚠ Signal has variable period (> 10% variation)")
        print("Try measuring individual pulses instead:")
        pw = tk.pulse_width(trace, return_all=True)
        print(f"Pulse widths: {pw}")
else:
    print("No periods detected - signal is not periodic")
```

---

#### Scenario 2: "frequency() returns NaN on my sine wave"

**Possible causes:**

1. DC offset makes edge detection fail
2. Sample rate too low
3. Using wrong method

**Solution:**

```python
# Try FFT method for sine waves
freq_fft = tk.frequency(trace, method="fft")
if not np.isnan(freq_fft):
    print(f"Frequency (FFT): {freq_fft:.3e} Hz")
else:
    # Check if signal is actually varying
    if np.std(trace.data) < 1e-6:
        print("Signal is effectively DC")
    else:
        # Try edge method with more data
        print("Try collecting more cycles or increasing sample rate")
```

---

#### Scenario 3: "propagation_delay() returns NaN"

**Possible causes:**

1. Output edge occurs before input edge (wrong signal assignment)
2. Delay is longer than capture window
3. Edge types don't match

**Solution:**

```python
# Check edge counts
from tracekit.analyzers.digital.timing import _get_edge_timestamps

input_edges = _get_edge_timestamps(input_trace, "rising", 0.5)
output_edges = _get_edge_timestamps(output_trace, "rising", 0.5)

print(f"Input edges: {len(input_edges)}")
print(f"Output edges: {len(output_edges)}")

if len(input_edges) > 0 and len(output_edges) > 0:
    print(f"First input edge: {input_edges[0]:.6e} s")
    print(f"First output edge: {output_edges[0]:.6e} s")

    if output_edges[0] < input_edges[0]:
        print("⚠ Output edge before input edge - signals may be swapped")
        # Try swapping
        delay = tk.propagation_delay(output_trace, input_trace)
        print(f"Reversed delay: {delay:.6e} s")
```

---

#### Scenario 4: "rise_time() returns NaN on square wave"

**Possible causes:**

1. Insufficient sample rate (too few points across transition)
2. No rising edges in capture
3. Signal doesn't cross both reference levels

**Solution:**

```python
# Calculate how many samples are in the transition
sample_rate = trace.metadata.sample_rate
data = trace.data

# Find edges manually
low, high = _find_levels(data)
mid = (low + high) / 2
rising_indices = np.where((data[:-1] < mid) & (data[1:] >= mid))[0]

if len(rising_indices) > 0:
    # Check samples across transition (10% to 90%)
    idx = rising_indices[0]
    low_ref = low + 0.1 * (high - low)
    high_ref = low + 0.9 * (high - low)

    # Find samples between 10% and 90%
    transition_region = (data >= low_ref) & (data <= high_ref)
    samples_in_transition = np.sum(transition_region)

    print(f"Samples in transition: {samples_in_transition}")
    if samples_in_transition < 3:
        print("⚠ Insufficient samples in transition")
        print(f"Recommendation: Increase sample rate by {10 / samples_in_transition:.0f}x")
else:
    print("No rising edges found")
    # Check for falling edges
    falling_indices = np.where((data[:-1] >= mid) & (data[1:] < mid))[0]
    print(f"Falling edges: {len(falling_indices)}")
```

---

## Best Practices

### 1. Always Check for NaN

Never assume a measurement will succeed:

```python
import numpy as np

# ❌ BAD - will crash if NaN
freq = tk.frequency(trace)
print(f"Period: {1/freq} s")  # Division by zero if NaN

# ✓ GOOD - explicit check
freq = tk.frequency(trace)
if not np.isnan(freq):
    print(f"Frequency: {freq:.3e} Hz")
    print(f"Period: {1/freq:.3e} s")
else:
    print("Frequency measurement not applicable for this signal")
```

### 2. Use the measure() Function for Discovery

The `measure()` function computes multiple measurements and handles NaN gracefully:

```python
# Get all applicable measurements
results = tk.measure(trace, include_units=True)

# Filter out NaN results
valid_results = {k: v for k, v in results.items()
                 if not np.isnan(v['value'])}

print(f"Valid measurements: {len(valid_results)}/{len(results)}")
for name, data in valid_results.items():
    print(f"  {name}: {data['value']:.3e} {data['unit']}")
```

### 3. Provide User Feedback

When building applications, give users actionable feedback:

```python
def measure_with_feedback(trace, measurement_name):
    """Measure with user-friendly error messages."""
    measurement_func = getattr(tk, measurement_name)
    result = measurement_func(trace)

    if np.isnan(result):
        # Provide specific guidance
        if measurement_name in ['frequency', 'period']:
            return None, "Signal is not periodic. Try single-pulse measurements."
        elif measurement_name in ['rise_time', 'fall_time']:
            return None, "No clear transitions detected. Check signal type and sample rate."
        elif measurement_name == 'duty_cycle':
            return None, "Requires periodic square wave. Signal may be aperiodic or DC."
        else:
            return None, f"{measurement_name} not applicable for this signal."

    return result, None

# Usage
result, error = measure_with_feedback(trace, 'frequency')
if error:
    print(f"Error: {error}")
else:
    print(f"Frequency: {result:.3e} Hz")
```

### 4. Pre-validate Signals

Check signal characteristics before attempting measurements:

```python
def analyze_signal_characteristics(trace):
    """Determine what measurements are applicable."""
    data = trace.data

    # Basic checks
    n_samples = len(data)
    amplitude = np.max(data) - np.min(data)
    variation = np.std(data)

    characteristics = {
        'sufficient_samples': n_samples >= 16,
        'has_amplitude': amplitude > 1e-9,
        'has_variation': variation > 1e-9,
    }

    # Edge detection
    if characteristics['has_amplitude']:
        from tracekit.analyzers.waveform.measurements import _find_edges
        rising_edges = _find_edges(trace, "rising")
        falling_edges = _find_edges(trace, "falling")

        characteristics['has_edges'] = len(rising_edges) > 0 or len(falling_edges) > 0
        characteristics['is_periodic'] = len(rising_edges) >= 2 and len(falling_edges) >= 2
        characteristics['edge_count'] = len(rising_edges) + len(falling_edges)
    else:
        characteristics['has_edges'] = False
        characteristics['is_periodic'] = False
        characteristics['edge_count'] = 0

    # Recommend measurements
    recommended = []

    if characteristics['is_periodic']:
        recommended.extend(['frequency', 'period', 'duty_cycle', 'rise_time', 'fall_time'])
    elif characteristics['has_edges']:
        recommended.extend(['rise_time', 'fall_time', 'pulse_width'])

    # These almost always work
    if characteristics['sufficient_samples']:
        recommended.extend(['amplitude', 'rms', 'mean'])

    characteristics['recommended_measurements'] = recommended

    return characteristics

# Usage
chars = analyze_signal_characteristics(trace)
print(f"Signal characteristics:")
print(f"  Periodic: {chars['is_periodic']}")
print(f"  Edges: {chars['edge_count']}")
print(f"  Recommended measurements: {', '.join(chars['recommended_measurements'])}")
```

### 5. Handle Batch Processing

When analyzing multiple traces:

```python
def batch_analyze(traces, measurement_name):
    """Analyze multiple traces, handling NaN gracefully."""
    results = []
    failures = []

    for i, trace in enumerate(traces):
        measurement_func = getattr(tk, measurement_name)
        result = measurement_func(trace)

        if np.isnan(result):
            failures.append(i)
        else:
            results.append(result)

    if results:
        print(f"{measurement_name}:")
        print(f"  Successful: {len(results)}/{len(traces)}")
        print(f"  Mean: {np.mean(results):.3e}")
        print(f"  Std: {np.std(results):.3e}")

    if failures:
        print(f"  Failed traces: {failures}")

    return results, failures
```

---

## Code Examples

### Example 1: Robust Single Measurement

```python
import numpy as np
import tracekit as tk

def measure_frequency_robust(trace):
    """
    Attempt to measure frequency with fallback strategies.
    Returns (frequency, method, confidence) or (None, None, None)
    """
    # Strategy 1: Edge-based (most accurate for digital signals)
    freq = tk.frequency(trace, method="edge")
    if not np.isnan(freq):
        return freq, "edge", "high"

    # Strategy 2: FFT-based (good for analog signals)
    freq = tk.frequency(trace, method="fft")
    if not np.isnan(freq):
        return freq, "fft", "medium"

    # Strategy 3: Check if single period exists
    periods = tk.period(trace, return_all=True)
    if len(periods) > 0:
        freq = 1.0 / np.mean(periods)
        return freq, "period", "low"

    # No frequency detectable
    return None, None, None

# Usage
trace = tk.load("signal.wfm")
freq, method, confidence = measure_frequency_robust(trace)

if freq is not None:
    print(f"Frequency: {freq:.3e} Hz (method: {method}, confidence: {confidence})")
else:
    print("Signal is not periodic or has insufficient transitions")
```

### Example 2: Signal Type Detection

```python
import numpy as np
import tracekit as tk
from tracekit.analyzers.waveform.measurements import _find_edges

def detect_signal_type(trace):
    """
    Classify signal type based on characteristics.
    Returns one of: 'dc', 'periodic_digital', 'aperiodic_digital',
                    'periodic_analog', 'noise'
    """
    data = trace.data

    # Check for DC
    if np.std(data) < 1e-9 * (np.max(np.abs(data)) + 1e-12):
        return 'dc'

    # Check for edges
    rising = _find_edges(trace, "rising")
    falling = _find_edges(trace, "falling")
    total_edges = len(rising) + len(falling)

    if total_edges == 0:
        # No edges - either analog or noise
        # Check if mostly sinusoidal
        from scipy import signal
        f, psd = signal.periodogram(data, trace.metadata.sample_rate)
        peak_power = np.max(psd[1:])  # Exclude DC
        avg_power = np.mean(psd[1:])

        if peak_power > 10 * avg_power:
            return 'periodic_analog'
        else:
            return 'noise'

    # Has edges - check periodicity
    if total_edges >= 4:
        # Check period consistency
        if len(rising) >= 2:
            periods = np.diff(_get_edge_timestamps(trace, "rising", 0.5))
            cv = np.std(periods) / np.mean(periods)

            if cv < 0.1:  # Less than 10% variation
                return 'periodic_digital'

    return 'aperiodic_digital'

# Usage
trace = tk.load("unknown_signal.wfm")
signal_type = detect_signal_type(trace)

print(f"Signal type: {signal_type}")

# Choose appropriate measurements based on type
if signal_type == 'periodic_digital':
    results = tk.measure(trace, parameters=[
        'frequency', 'duty_cycle', 'rise_time', 'fall_time'
    ])
elif signal_type == 'aperiodic_digital':
    results = tk.measure(trace, parameters=[
        'rise_time', 'fall_time', 'pulse_width_pos'
    ])
elif signal_type == 'dc':
    results = tk.measure(trace, parameters=['mean', 'rms'])
else:
    results = tk.measure(trace, parameters=['amplitude', 'rms', 'mean'])

# Display results
for name, value in results.items():
    if isinstance(value, dict):
        val = value['value']
        unit = value['unit']
    else:
        val = value
        unit = ''

    if not np.isnan(val):
        print(f"  {name}: {val:.3e} {unit}")
```

### Example 3: Comprehensive Signal Report

```python
import numpy as np
import tracekit as tk

def generate_signal_report(trace):
    """Generate comprehensive signal analysis report."""
    print("=" * 60)
    print("SIGNAL ANALYSIS REPORT")
    print("=" * 60)

    # Basic info
    print(f"\nBasic Information:")
    print(f"  Samples: {len(trace.data)}")
    print(f"  Sample rate: {trace.metadata.sample_rate:.3e} Hz")
    print(f"  Duration: {len(trace.data) / trace.metadata.sample_rate:.3e} s")

    # Statistical summary
    print(f"\nStatistical Summary:")
    print(f"  Min: {np.min(trace.data):.3e}")
    print(f"  Max: {np.max(trace.data):.3e}")
    print(f"  Mean: {np.mean(trace.data):.3e}")
    print(f"  RMS: {np.sqrt(np.mean(trace.data**2)):.3e}")
    print(f"  Std Dev: {np.std(trace.data):.3e}")

    # Attempt all measurements
    all_measurements = tk.measure(trace, include_units=True)

    successful = {}
    failed = {}

    for name, data in all_measurements.items():
        if np.isnan(data['value']):
            failed[name] = data
        else:
            successful[name] = data

    # Display successful measurements
    print(f"\nSuccessful Measurements ({len(successful)}):")
    for name, data in successful.items():
        print(f"  {name}: {data['value']:.3e} {data['unit']}")

    # Display failed measurements
    print(f"\nNot Applicable ({len(failed)}):")
    for name in failed.keys():
        print(f"  {name}")

    # Interpretation
    print(f"\nSignal Interpretation:")

    if 'frequency' in successful:
        freq = successful['frequency']['value']
        print(f"  ✓ Periodic signal at {freq:.3e} Hz")

        if 'duty_cycle' in successful:
            dc = successful['duty_cycle']['value']
            print(f"  ✓ Square wave with {dc:.1f}% duty cycle")
    else:
        print(f"  ⨯ Non-periodic signal")

    if 'rise_time' in successful or 'fall_time' in successful:
        print(f"  ✓ Has measurable transitions")
    else:
        print(f"  ⨯ No clear transitions (DC or noise)")

    print("=" * 60)

# Usage
trace = tk.load("my_signal.wfm")
generate_signal_report(trace)
```

### Example 4: Helper Function for Signal Validation

```python
import numpy as np
import tracekit as tk
from tracekit.analyzers.waveform.measurements import _find_edges

def is_suitable_for_measurement(trace, measurement_name):
    """
    Check if a trace is suitable for a specific measurement.

    Returns:
        (bool, str): (is_suitable, reason)
    """
    data = trace.data
    n = len(data)

    # Check minimum samples
    if n < 3:
        return False, f"Insufficient samples ({n} < 3)"

    # Check amplitude
    amplitude = np.max(data) - np.min(data)
    if amplitude < 1e-12:
        if measurement_name not in ['mean', 'rms']:
            return False, "Signal has no variation (DC)"

    # Measurement-specific checks
    if measurement_name in ['frequency', 'period']:
        edges = _find_edges(trace, "rising")
        if len(edges) < 2:
            return False, "Need at least 2 edges for periodic measurements"

        # Check period consistency
        periods = np.diff([e * trace.metadata.sample_rate for e in edges])
        if len(periods) > 1:
            cv = np.std(periods) / np.mean(periods)
            if cv > 0.2:
                return False, f"Non-periodic signal (period variation: {cv*100:.1f}%)"

    elif measurement_name == 'duty_cycle':
        rising = _find_edges(trace, "rising")
        falling = _find_edges(trace, "falling")

        if len(rising) < 1 or len(falling) < 1:
            return False, "Need both rising and falling edges"

        if len(rising) < 2:
            return False, "Need periodic signal for duty cycle"

    elif measurement_name in ['rise_time', 'fall_time']:
        edge_type = "rising" if measurement_name == 'rise_time' else "falling"
        edges = _find_edges(trace, edge_type)

        if len(edges) < 1:
            return False, f"No {edge_type} edges detected"

    elif measurement_name == 'pulse_width':
        rising = _find_edges(trace, "rising")
        falling = _find_edges(trace, "falling")

        if len(rising) == 0 or len(falling) == 0:
            return False, "Need both rising and falling edges for pulse width"

    return True, "Signal is suitable"

# Usage
trace = tk.load("signal.wfm")

measurements_to_try = ['frequency', 'duty_cycle', 'rise_time', 'amplitude']

print("Measurement Suitability Check:")
for meas in measurements_to_try:
    suitable, reason = is_suitable_for_measurement(trace, meas)
    status = "✓" if suitable else "⨯"
    print(f"  {status} {meas}: {reason}")

    if suitable:
        result = getattr(tk, meas)(trace)
        if not np.isnan(result):
            print(f"      Result: {result:.3e}")
```

### Example 5: Adaptive Measurement Strategy

```python
import numpy as np
import tracekit as tk

def smart_measure(trace):
    """
    Intelligently choose and perform measurements based on signal characteristics.
    Returns dictionary of all applicable measurements.
    """
    results = {}

    # Try basic measurements (almost always work)
    results['amplitude'] = tk.amplitude(trace)
    results['mean'] = tk.mean(trace)
    results['rms'] = tk.rms(trace)

    # Try edge-based measurements
    rise = tk.rise_time(trace)
    if not np.isnan(rise):
        results['rise_time'] = rise

        # If rise time works, try fall time
        fall = tk.fall_time(trace)
        if not np.isnan(fall):
            results['fall_time'] = fall

    # Try frequency (both methods)
    freq_edge = tk.frequency(trace, method="edge")
    if not np.isnan(freq_edge):
        results['frequency'] = freq_edge
        results['frequency_method'] = 'edge'

        # Periodic signal - try more measurements
        duty = tk.duty_cycle(trace, percentage=True)
        if not np.isnan(duty):
            results['duty_cycle'] = duty

        period = tk.period(trace)
        if not np.isnan(period):
            results['period'] = period
    else:
        # Try FFT method
        freq_fft = tk.frequency(trace, method="fft")
        if not np.isnan(freq_fft):
            results['frequency'] = freq_fft
            results['frequency_method'] = 'fft'

    # Try pulse width if no frequency
    if 'frequency' not in results:
        pw = tk.pulse_width(trace, polarity="positive")
        if not np.isnan(pw):
            results['pulse_width'] = pw

    # Try overshoot/undershoot
    over = tk.overshoot(trace)
    if not np.isnan(over) and over > 0:
        results['overshoot'] = over

    under = tk.undershoot(trace)
    if not np.isnan(under) and under > 0:
        results['undershoot'] = under

    return results

# Usage
trace = tk.load("signal.wfm")
results = smart_measure(trace)

print("Measurement Results:")
for name, value in results.items():
    if isinstance(value, str):
        print(f"  {name}: {value}")
    else:
        print(f"  {name}: {value:.3e}")
```

---

## Quick Reference

### When to Use Each Measurement

**For Clock/Square Wave Signals:**

- `frequency()`, `period()`, `duty_cycle()`
- `rise_time()`, `fall_time()`
- `rms_jitter()`, `peak_to_peak_jitter()`

**For Single Pulse/Aperiodic Digital:**

- `rise_time()`, `fall_time()`
- `pulse_width()`
- `overshoot()`, `undershoot()`

**For DC Signals:**

- `mean()`, `rms()`, `amplitude()`
- `ripple()` (power analysis)

**For Analog Periodic (Sine Wave):**

- `frequency(method="fft")`
- `amplitude()`, `rms()`, `mean()`

**For Two Signal Comparisons:**

- `propagation_delay()` (input → output)
- `setup_time()`, `hold_time()` (data vs clock)
- `phase()` (two periodic signals)
- `skew()` (multiple signals)

**For High-Speed Serial:**

- `eye_height()`, `eye_width()`
- `q_factor()` (eye diagram quality)

---

## Additional Resources

- [API Reference](../api/index.md) - Detailed function signatures
- [Tutorials](../tutorials/index.md) - Step-by-step guides
- [Best Practices](best-practices.md) - Coding best practices

---

## Summary

NaN results are a normal part of signal analysis. By understanding when and why measurements return NaN, you can:

1. Choose appropriate measurements for your signal type
2. Debug measurement failures quickly
3. Build robust analysis workflows
4. Provide better user feedback in applications

**Key takeaways:**

- Always check for NaN before using measurement results
- Use `measure()` to discover which measurements apply
- Visualize your signal first to understand its characteristics
- Pre-validate signals with helper functions
- Provide fallback strategies for critical measurements

---

<!-- Content merged from docs/TROUBLESHOOTING_NAN_RESULTS.md -->

# Troubleshooting NaN Results - Quick Reference

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08

## Quick Decision Tree

```
Got NaN result?
    │
    ├─→ Check signal basics
    │   │
    │   ├─→ Plot signal visually
    │   │   └─→ See any variation?
    │   │       ├─→ NO  → DC signal → Use mean(), rms() only
    │   │       └─→ YES → Continue to next check
    │   │
    │   └─→ Check sample count
    │       └─→ < 3 samples?
    │           ├─→ YES → Insufficient data error
    │           └─→ NO  → Continue
    │
    ├─→ For frequency/period measurements:
    │   │
    │   ├─→ Check for edges
    │   │   └─→ Use _find_edges() to count
    │   │       ├─→ 0-1 edges → Not periodic → Try single-pulse measurements
    │   │       └─→ 2+ edges → Check periodicity
    │   │
    │   ├─→ Check periodicity
    │   │   └─→ Calculate period variation
    │   │       ├─→ > 20% variation → Aperiodic → Can't measure frequency
    │   │       └─→ < 20% variation → Periodic → Check sample rate
    │   │
    │   └─→ Check sample rate
    │       └─→ Samples per period
    │           ├─→ < 10 samples → Too low → Increase sample rate
    │           └─→ 10+ samples → Should work → Check method
    │
    ├─→ For rise_time/fall_time measurements:
    │   │
    │   ├─→ Check for edges of correct type
    │   │   ├─→ No rising edges → Can't measure rise_time
    │   │   └─→ No falling edges → Can't measure fall_time
    │   │
    │   ├─→ Check amplitude
    │   │   └─→ High - Low ≤ 0?
    │   │       ├─→ YES → Flat signal → Can't measure
    │   │       └─→ NO  → Continue
    │   │
    │   └─→ Check transition sampling
    │       └─→ Count samples across 10%-90%
    │           ├─→ < 3 samples → Insufficient → Increase sample rate
    │           └─→ 3+ samples → Should work
    │
    ├─→ For duty_cycle measurement:
    │   │
    │   ├─→ Check frequency works
    │   │   └─→ frequency() returns NaN?
    │   │       ├─→ YES → Not periodic → Can't measure duty cycle
    │   │       └─→ NO  → Check edges
    │   │
    │   └─→ Check both edge types
    │       └─→ Has rising AND falling?
    │           ├─→ NO  → Incomplete cycles → Can't measure
    │           └─→ YES → Should work
    │
    └─→ For jitter measurements:
        │
        ├─→ Check edge count
        │   └─→ < 3 edges?
        │       ├─→ YES → Insufficient → Need more cycles
        │       └─→ NO  → Check periodicity
        │
        └─→ Check periodicity
            └─→ frequency() works?
                ├─→ NO  → Not periodic → Can't measure jitter
                └─→ YES → Should work
```

## Common NaN Scenarios - Quick Solutions

### Scenario: "All timing measurements return NaN"

**Likely cause:** DC signal (no transitions)

**Quick check:**

```python
import numpy as np
print(f"Std deviation: {np.std(trace.data):.3e}")
print(f"Amplitude: {np.max(trace.data) - np.min(trace.data):.3e}")
```

**Solution:**

- If std ≈ 0: Signal is DC, use `mean()` and `rms()` only
- If amplitude > 0 but no edges: Check if signal is pure noise

---

### Scenario: "frequency() returns NaN but signal is clearly periodic"

**Likely cause:** Insufficient sample rate or using wrong method

**Quick check:**

```python
from tracekit.analyzers.waveform.measurements import _find_edges

edges = _find_edges(trace, "rising")
print(f"Edges found: {len(edges)}")

if len(edges) >= 2:
    periods = np.diff(edges)
    samples_per_period = np.mean(periods) * trace.metadata.sample_rate
    print(f"Samples per period: {samples_per_period:.1f}")
```

**Solution:**

- If edges < 2: Signal may not be periodic in this capture window
- If samples per period < 10: Increase sample rate
- For sine waves: Try `frequency(method="fft")` instead

---

### Scenario: "duty_cycle() returns NaN on PWM signal"

**Likely cause:** Signal is not periodic (variable frequency or duty cycle)

**Quick check:**

```python
periods = tk.period(trace, return_all=True)
if len(periods) > 1:
    variation = np.std(periods) / np.mean(periods) * 100
    print(f"Period variation: {variation:.1f}%")
```

**Solution:**

- If variation > 20%: Signal is aperiodic
- Use `pulse_width(return_all=True)` to measure individual pulses
- Check if you're capturing multiple different signals

---

### Scenario: "rise_time() returns NaN on square wave"

**Likely cause:** Insufficient sample rate across transition

**Quick check:**

```python
# Estimate transition time
from tracekit.analyzers.waveform.measurements import _find_levels

low, high = _find_levels(trace.data)
mid = (low + high) / 2
transitions = np.where((trace.data[:-1] < mid) & (trace.data[1:] >= mid))[0]

if len(transitions) > 0:
    idx = transitions[0]
    # Count samples in transition region
    low_ref = low + 0.1 * (high - low)
    high_ref = low + 0.9 * (high - low)

    transition_samples = np.sum((trace.data[idx:idx+20] >= low_ref) &
                                 (trace.data[idx:idx+20] <= high_ref))
    print(f"Samples in transition: {transition_samples}")
```

**Solution:**

- If < 3 samples: Increase sample rate by 10x
- If no transitions found: Signal may be all high or all low in this window

---

### Scenario: "propagation_delay() returns NaN"

**Likely cause:** Signals swapped or delay outside capture window

**Quick check:**

```python
from tracekit.analyzers.digital.timing import _get_edge_timestamps

input_edges = _get_edge_timestamps(input_trace, "rising", 0.5)
output_edges = _get_edge_timestamps(output_trace, "rising", 0.5)

print(f"Input edges: {len(input_edges)}")
print(f"Output edges: {len(output_edges)}")

if len(input_edges) > 0 and len(output_edges) > 0:
    print(f"First input edge: {input_edges[0]:.6e} s")
    print(f"First output edge: {output_edges[0]:.6e} s")
```

**Solution:**

- If output edge < input edge: Signals are swapped, reverse them
- If no overlapping edges: Delay is longer than capture window
- Check edge_type parameter matches your signals

---

### Scenario: "Jitter measurements return NaN"

**Likely cause:** Non-periodic signal or too few edges

**Quick check:**

```python
from tracekit.analyzers.waveform.measurements import _find_edges

edges = _find_edges(trace, "rising")
print(f"Edges: {len(edges)}")

if len(edges) >= 2:
    periods = np.diff(edges)
    print(f"Periods: {len(periods)}")
    print(f"Period std/mean: {np.std(periods)/np.mean(periods)*100:.1f}%")
```

**Solution:**

- If edges < 3: Capture more cycles
- If period variation > 20%: Signal is not clock-like
- Jitter measurements need clean periodic signals

---

## Measurement Compatibility Quick Reference

| Signal Type              | Working Measurements                                    | NaN Measurements                                                |
| ------------------------ | ------------------------------------------------------- | --------------------------------------------------------------- |
| **DC (constant)**        | mean, rms, amplitude                                    | frequency, period, duty_cycle, rise_time, fall_time, all jitter |
| **Single pulse**         | rise_time, fall_time, pulse_width, amplitude, mean, rms | frequency, period, duty_cycle, jitter                           |
| **Periodic square wave** | ALL MEASUREMENTS                                        | (none if properly sampled)                                      |
| **Sine wave**            | frequency(fft), amplitude, mean, rms                    | frequency(edge), duty_cycle, rise_time, fall_time               |
| **Noise**                | mean, rms, amplitude                                    | frequency, period, duty_cycle, rise_time, fall_time             |
| **Aperiodic digital**    | rise_time, fall_time, pulse_width, amplitude, mean, rms | frequency, period, duty_cycle, jitter                           |

## Debug Checklist

When you get NaN, work through this checklist:

### 1. Basic Signal Checks

- [ ] Signal has variation (std > 0)
- [ ] Signal has amplitude (max - min > 0)
- [ ] At least 3 samples in data
- [ ] Signal is not clipped or saturated

### 2. For Edge-Based Measurements

- [ ] Signal crosses threshold level
- [ ] At least one edge detected
- [ ] Sufficient samples across transitions (5-10 minimum)
- [ ] Sample rate > 2x signal frequency (Nyquist)

### 3. For Periodic Measurements

- [ ] At least 2 complete cycles captured
- [ ] Period variation < 20%
- [ ] At least 10-20 samples per period
- [ ] Signal doesn't drift significantly

### 4. For Two-Signal Measurements

- [ ] Both signals have edges
- [ ] Signals are time-aligned (same time base)
- [ ] Edge types match (both rising or both falling)
- [ ] Expected timing relationship is present

## Validation Workflow

Recommended workflow to avoid NaN surprises:

```python
import numpy as np
import tracekit as tk
from tracekit.analyzers.validation import (
    analyze_signal_characteristics,
    get_valid_measurements,
)

# 1. Visualize (if possible)
import matplotlib.pyplot as plt
plt.plot(trace.data)
plt.title("Signal Overview")
plt.show()

# 2. Analyze characteristics
chars = analyze_signal_characteristics(trace)
print(f"Signal type: {chars['signal_type']}")
print(f"Periodic: {chars['is_periodic']}")
print(f"Edges: {chars['edge_count']}")

# 3. Get valid measurements
valid = get_valid_measurements(trace)
print(f"Applicable: {', '.join(valid)}")

# 4. Only attempt valid measurements
for meas_name in valid:
    func = getattr(tk, meas_name)
    result = func(trace)
    if not np.isnan(result):
        print(f"{meas_name}: {result:.3e}")
```

## Getting Help

If you're still getting unexpected NaN results:

1. **Check the signal:**

   ```python
   print(f"Samples: {len(trace.data)}")
   print(f"Min: {np.min(trace.data):.3e}")
   print(f"Max: {np.max(trace.data):.3e}")
   print(f"Mean: {np.mean(trace.data):.3e}")
   print(f"Std: {np.std(trace.data):.3e}")
   ```

2. **Check sample rate:**

   ```python
   print(f"Sample rate: {trace.metadata.sample_rate:.3e} Hz")
   print(f"Duration: {len(trace.data)/trace.metadata.sample_rate:.3e} s")
   ```

3. **Try the simplest measurements first:**

   ```python
   # These almost never return NaN
   print(f"Mean: {tk.mean(trace):.3e}")
   print(f"RMS: {tk.rms(trace):.3e}")
   print(f"Amplitude: {tk.amplitude(trace):.3e}")
   ```

4. **Check edge detection:**

   ```python
   from tracekit.analyzers.waveform.measurements import _find_edges

   rising = _find_edges(trace, "rising")
   falling = _find_edges(trace, "falling")

   print(f"Rising edges: {len(rising)}")
   print(f"Falling edges: {len(falling)}")
   ```

## See Also

- [API Reference](../api/index.md) - Function signatures and parameters
- [Troubleshooting Guide](troubleshooting.md) - General troubleshooting
- [Tutorial 02: Basic Measurements](../tutorials/02-basic-measurements.md) - Hands-on tutorial
- [NaN Handling Example](../examples-reference.md#05-advanced) - Code demonstrations
