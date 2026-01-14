# Tutorial 2: Basic Measurements

> **Version**: 0.2.0 | **Last Updated**: 2026-01-12 | **Time**: 20 minutes

Learn to perform fundamental waveform measurements with TraceKit.

## Prerequisites

- Completed [Tutorial 1: Loading Data](01-loading-data.md)
- Understanding of basic signal concepts

## Learning Objectives

By the end of this tutorial, you will be able to:

- Measure frequency and period
- Calculate amplitude and RMS values
- Analyze rise and fall times
- Handle measurement edge cases (NaN results)

## Creating Test Data

Let's start with a known signal for measurement validation:

```python
from tracekit.testing import generate_sine_wave, generate_square_wave
import tracekit as tk

# Generate a 1 MHz sine wave using testing utilities
sine = generate_sine_wave(
    frequency=1e6,      # 1 MHz
    amplitude=1.0,      # 1V peak
    sample_rate=100e6,  # 100 MSa/s
    duration=10e-6      # 10 microseconds
)
print(f"Generated sine wave: {len(sine.data)} samples")
```

## Time-Domain Measurements

### Frequency and Period

```python
# Measure frequency
freq = tk.frequency(sine)
print(f"Frequency: {freq / 1e6:.3f} MHz")

# Measure period
period = tk.period(sine)
print(f"Period: {period * 1e9:.1f} ns")

# Expected: 1.000 MHz, 1000.0 ns
```

### Duty Cycle

```python
# Generate a square wave with 30% duty cycle
square = generate_square_wave(
    frequency=1e6,
    duty_cycle=0.3,     # 30%
    sample_rate=100e6,
    duration=10e-6
)

duty = tk.duty_cycle(square)
print(f"Duty cycle: {duty * 100:.1f}%")
# Expected: ~30%
```

## Amplitude Measurements

### Basic Amplitude

```python
# Measure peak-to-peak amplitude
amp = tk.amplitude(sine)
print(f"Amplitude: {amp:.3f} V")

# Measure RMS voltage
rms = tk.rms(sine)
print(f"RMS: {rms:.3f} V")
# For a sine wave: RMS = peak / sqrt(2) ~ 0.707 * peak
```

### Complete Amplitude Analysis

```python
# Get all amplitude statistics at once using basic_stats
stats = tk.basic_stats(sine)

print(f"Minimum: {stats['min']:.3f} V")
print(f"Maximum: {stats['max']:.3f} V")
print(f"Peak-to-peak: {stats['range']:.3f} V")
print(f"Mean (DC): {stats['mean']:.3f} V")
print(f"Std Dev: {stats['std']:.3f} V")
```

## Rise and Fall Time

Rise and fall times are measured according to IEEE 181-2011:

```python
from tracekit.testing import generate_pulse

# Generate a pulse for rise time measurement
pulse = generate_pulse(
    width=50e-9,          # 50 ns pulse width
    rise_time=10e-9,      # 10 ns rise time
    fall_time=10e-9,      # 10 ns fall time
    sample_rate=1e9,      # 1 GSa/s for adequate resolution
    duration=100e-9
)

# Measure rise time (10% to 90% by default)
rise = tk.rise_time(pulse)
print(f"Rise time: {rise * 1e9:.1f} ns")

# Measure fall time (90% to 10%)
fall = tk.fall_time(pulse)
print(f"Fall time: {fall * 1e9:.1f} ns")
```

### Custom Thresholds

```python
# Use different thresholds (20% to 80%)
# ref_levels is a tuple of (low, high) reference levels as fractions
rise_20_80 = tk.rise_time(pulse, ref_levels=(0.2, 0.8))
print(f"Rise time (20-80%): {rise_20_80 * 1e9:.1f} ns")
```

## Overshoot and Undershoot

```python
# Generate pulse with overshoot
pulse_overshoot = generate_pulse(
    width=50e-9,
    rise_time=5e-9,
    fall_time=5e-9,
    sample_rate=1e9,
    duration=100e-9,
    overshoot=0.15       # 15% overshoot
)

overshoot = tk.overshoot(pulse_overshoot)
print(f"Overshoot: {overshoot * 100:.1f}%")
```

## Edge Detection

Find all rising and falling edges:

```python
# Find rising edges
rising_edges = tk.find_rising_edges(square)
falling_edges = tk.find_falling_edges(square)

print(f"Found {len(rising_edges)} rising edges")
print(f"Found {len(falling_edges)} falling edges")

print("\nFirst 5 rising edge times:")
for i, time in enumerate(rising_edges[:5]):
    print(f"  Edge {i+1}: {time * 1e9:.1f} ns")
```

**Output:**

```
Found 10 rising edges
Found 10 falling edges

First 5 rising edge times:
  Edge 1: 0.0 ns
  Edge 2: 1000.0 ns
  Edge 3: 2000.0 ns
  ...
```

## Handling NaN Results

Measurements return `NaN` when they cannot be computed:

```python
import math
from tracekit.testing import generate_dc

# DC signal has no frequency
dc_signal = generate_dc(level=1.5, sample_rate=100e6, duration=10e-6)
freq = tk.frequency(dc_signal)

if math.isnan(freq):
    print("Frequency measurement returned NaN")
    print("Reason: Signal has no transitions")
```

### Robust Measurement Pattern

```python
def safe_measure_frequency(trace, default=0.0):
    """Measure frequency with fallback."""
    freq = tk.frequency(trace)

    if not math.isnan(freq):
        return freq

    # Fallback: try edge-based measurement
    rising_edges = tk.find_rising_edges(trace)
    if len(rising_edges) >= 2:
        period = rising_edges[1] - rising_edges[0]
        return 1.0 / period

    return default

freq = safe_measure_frequency(sine)
print(f"Frequency: {freq / 1e6:.3f} MHz")
```

## Measurement Summary

Get all measurements at once:

```python
import math

# Comprehensive measurement report
def measure_all(trace):
    """Perform all standard measurements."""
    return {
        "frequency": tk.frequency(trace),
        "period": tk.period(trace),
        "amplitude": tk.amplitude(trace),
        "rms": tk.rms(trace),
        "duty_cycle": tk.duty_cycle(trace),
    }

results = measure_all(square)
for name, value in results.items():
    if not math.isnan(value):
        print(f"{name}: {value}")
```

## Exercise

Create and measure a custom waveform:

```python
from tracekit.testing import generate_sine_wave

# Generate a 500 kHz sine wave with DC offset
test_signal = generate_sine_wave(
    frequency=500e3,
    amplitude=2.0,       # 2V peak amplitude
    sample_rate=50e6,
    duration=20e-6,
    offset=0.5           # 0.5V DC offset
)

# Measure and verify:
# 1. Frequency should be ~500 kHz
# 2. Amplitude should be ~4V (peak-to-peak)
# 3. Mean should be ~0.5V

freq = tk.frequency(test_signal)
amp = tk.amplitude(test_signal)
stats = tk.basic_stats(test_signal)

print(f"Frequency: {freq / 1e3:.1f} kHz (expected: 500 kHz)")
print(f"Amplitude: {amp:.2f} V (expected: 4.0 V)")
print(f"DC offset: {stats['mean']:.2f} V (expected: 0.5 V)")
```

## Next Steps

- [Tutorial 3: Digital Signal Analysis](03-digital-signals.md)
- [Tutorial 4: Spectral Analysis](04-spectral-analysis.md)

## See Also

- [NaN Handling Guide](../guides/nan-handling.md)
- [IEEE 181-2011 Compliance](../reference/standards-compliance.md)
- [API Reference: Measurements](../api/analysis.md)
