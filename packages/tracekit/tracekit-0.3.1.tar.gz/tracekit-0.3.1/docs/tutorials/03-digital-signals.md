# Tutorial 3: Digital Signal Analysis

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08 | **Time**: 25 minutes

Learn to analyze digital signals, detect patterns, and extract timing information.

## Prerequisites

- Completed [Tutorial 2: Basic Measurements](02-basic-measurements.md)
- Understanding of digital signal concepts (clock, data, edges)

## Learning Objectives

By the end of this tutorial, you will be able to:

- Convert analog captures to digital representations
- Perform clock recovery
- Analyze bit patterns
- Measure digital timing parameters

## Understanding Digital Traces

TraceKit supports two trace types:

| Type            | Use Case       | Data Type       |
| --------------- | -------------- | --------------- |
| `WaveformTrace` | Analog signals | Float samples   |
| `DigitalTrace`  | Logic signals  | Boolean samples |

```python
import tracekit as tk
from tracekit import DigitalTrace

# Digital traces contain binary data
# Each sample is True (high) or False (low)
```

## Converting Analog to Digital

### Basic Thresholding

```python
import numpy as np

# Generate analog square wave
sample_rate = 100e6
duration = 10e-6
frequency = 1e6
t = np.arange(0, duration, 1/sample_rate)
# Square wave with noise
data = (np.sin(2 * np.pi * frequency * t) > 0).astype(float)
data += np.random.normal(0, 0.1, len(data))  # Add noise
analog = tk.WaveformTrace(data=data, metadata=tk.TraceMetadata(sample_rate=sample_rate))

# Convert to digital using threshold
digital = tk.digitize(analog, threshold=0.5)

print(f"Analog samples: {len(analog.data)}")
print(f"Digital samples: {len(digital.data)}")
```

### Automatic Threshold Detection

```python
# Let TraceKit find the optimal threshold
digital = tk.digitize(analog, threshold="auto")

# Or use histogram-based detection for noisy signals
digital = tk.digitize(analog, threshold="histogram")
```

### Hysteresis Thresholding

For noisy signals, use hysteresis to prevent glitches:

```python
# Two thresholds: high and low
digital = tk.digitize(
    analog,
    threshold_high=0.6,
    threshold_low=0.4
)
# Signal must cross 0.6 to go high, 0.4 to go low
```

## Clock Recovery

Extract clock information from data signals:

```python
# Note: In practice, load real captured UART data
# from a file instead of generating test signals

# Generate UART signal (async serial)
uart = generate_uart_signal(
    baud_rate=115200,
    data=b"Hello",
    sample_rate=10e6
)

# Recover the baud rate
from tracekit.inference import detect_baud_rate

detected_baud = detect_baud_rate(uart)
print(f"Detected baud rate: {detected_baud}")
# Expected: 115200
```

### Clock from Edge Intervals

```python
# Find all edges
edges = tk.find_edges(uart)

# Analyze edge intervals
intervals = []
for i in range(1, len(edges)):
    interval = edges[i][0] - edges[i-1][0]
    intervals.append(interval)

# Minimum interval is approximately bit time
import numpy as np
bit_time = np.min(intervals)
baud_rate = 1.0 / bit_time
print(f"Estimated baud rate: {baud_rate:.0f}")
```

## Pattern Detection

### Finding Bit Patterns

```python
from tracekit.analyzers.patterns import find_pattern

# Define pattern to find (as bits)
pattern = [1, 0, 1, 0, 1, 0, 1, 0]  # 0xAA

# Find all occurrences
matches = find_pattern(digital, pattern)

print(f"Found {len(matches)} matches")
for start_time, end_time in matches[:5]:
    print(f"  Pattern at: {start_time * 1e6:.2f} us")
```

### Preamble Detection

Many protocols use preambles for synchronization:

```python
from tracekit.analyzers.patterns import find_preamble

# Common preambles
preambles = {
    "uart_break": [0] * 10,           # UART break condition
    "spi_sync": [1, 0, 1, 0] * 4,     # Alternating pattern
    "i2c_start": [1, 1, 1, 0],        # I2C start condition
}

# Find UART break
breaks = find_pattern(digital, preambles["uart_break"])
print(f"Found {len(breaks)} break conditions")
```

## Timing Analysis

### Pulse Width Measurement

```python
from tracekit.analyzers.digital import measure_pulse_widths

# Measure all high pulse widths
high_widths = measure_pulse_widths(digital, level="high")
low_widths = measure_pulse_widths(digital, level="low")

print(f"High pulse widths: min={min(high_widths)*1e9:.1f}ns, max={max(high_widths)*1e9:.1f}ns")
print(f"Low pulse widths: min={min(low_widths)*1e9:.1f}ns, max={max(low_widths)*1e9:.1f}ns")
```

### Duty Cycle Analysis

```python
# Calculate duty cycle over time
from tracekit.analyzers.digital import duty_cycle_analysis

analysis = duty_cycle_analysis(digital, window_size=1000)

print(f"Average duty cycle: {analysis.mean * 100:.1f}%")
print(f"Duty cycle variation: {analysis.std * 100:.2f}%")
```

### Setup and Hold Time

For synchronous protocols:

```python
from tracekit.analyzers.digital import measure_setup_hold

# Analyze setup/hold timing between data and clock
# timing = measure_setup_hold(data_signal, clock_signal)
# print(f"Setup time: {timing.setup * 1e9:.1f} ns")
# print(f"Hold time: {timing.hold * 1e9:.1f} ns")
```

## Glitch Detection

Find signal integrity issues:

```python
from tracekit.analyzers.digital import find_glitches

# Find pulses shorter than minimum expected width
min_pulse = 100e-9  # 100 ns minimum valid pulse
glitches = find_glitches(digital, min_width=min_pulse)

print(f"Found {len(glitches)} glitches")
for time, width in glitches[:5]:
    print(f"  Glitch at {time * 1e6:.2f} us, width: {width * 1e9:.1f} ns")
```

## Signal Statistics

### Transition Density

```python
from tracekit.analyzers.digital import transition_density

# Calculate transitions per second
density = transition_density(digital)
print(f"Transition density: {density / 1e6:.2f} MTrans/s")
```

### Run Length Statistics

```python
from tracekit.analyzers.digital import run_length_stats

stats = run_length_stats(digital)

print("Run length statistics:")
print(f"  Shortest run: {stats.min_length} samples")
print(f"  Longest run: {stats.max_length} samples")
print(f"  Average run: {stats.mean_length:.1f} samples")
```

## Complete Analysis Example

```python
import tracekit as tk
# Note: In practice, load real captured UART data
# from a file instead of generating test signals

# Generate test signal
uart = generate_uart_signal(
    baud_rate=9600,
    data=b"Test message\r\n",
    sample_rate=1e6
)

# Full digital analysis
print("=== Digital Signal Analysis ===")
print(f"Sample rate: {uart.metadata.sample_rate / 1e6:.1f} MSa/s")
print(f"Duration: {uart.duration * 1e3:.2f} ms")

# Edge analysis
edges = tk.find_edges(uart)
rising = sum(1 for _, t in edges if t == "rising")
falling = sum(1 for _, t in edges if t == "falling")
print(f"\nEdges: {rising} rising, {falling} falling")

# Baud rate detection
from tracekit.inference import detect_baud_rate
baud = detect_baud_rate(uart)
print(f"Detected baud rate: {baud}")

# Transition density
density = len(edges) / uart.duration
print(f"Transition rate: {density:.0f} edges/sec")
```

## Exercise

Analyze a mixed signal:

```python
# Note: In practice, load real captured SPI data

# Generate SPI signal with clock and data
spi = generate_spi_signal(
    clock_freq=1e6,
    data=bytes([0xAA, 0x55, 0xFF, 0x00]),
    sample_rate=50e6
)

# Tasks:
# 1. Digitize the signal
# 2. Count edges on clock line
# 3. Verify clock frequency from edge timing
# 4. Find the 0xAA pattern in the data

# Your code here...
```

## Next Steps

- [Tutorial 4: Spectral Analysis](04-spectral-analysis.md)
- [Tutorial 5: Protocol Decoding](05-protocol-decoding.md)

## See Also

- [Digital Analysis API](../api/analysis.md#digital-analysis)
- [Edge Detection Guide](../guides/troubleshooting.md#edge-detection)
- [Protocol Decoders Reference](../reference/protocol-decoders.md)
