# Best Practices Guide

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08

Tips and best practices for optimal TraceKit usage across common workflows.

## Overview

This guide covers best practices for:

- Efficient data loading and memory management
- Optimal analysis workflows
- Performance optimization
- Code organization patterns

## Data Loading Best Practices

### Use Lazy Loading for Large Files

For files larger than available RAM:

```python
import tracekit as tk

# Lazy loading - metadata available immediately, data loaded on access
trace = tk.load("huge_capture.wfm", lazy=True)

# Check metadata without loading data
print(f"Duration: {trace.metadata.duration}")
print(f"Sample rate: {trace.metadata.sample_rate}")

# Data loaded only when accessed
segment = trace[0:10000]  # Loads only this segment
```

### Process Large Files in Chunks

```python
import tracekit as tk
import numpy as np

# Process in chunks to avoid memory issues
trace = tk.load("large_file.wfm", lazy=True)
chunk_size = 100000
results = []

for i in range(0, len(trace.data), chunk_size):
    chunk = trace[i:i + chunk_size]
    # Process chunk
    result = tk.measure_frequency(chunk)
    if not np.isnan(result):
        results.append(result)

print(f"Average frequency: {np.mean(results):.2f} Hz")
```

### Cache Loaded Data

When analyzing the same trace multiple times:

```python
import tracekit as tk

# Load once
trace = tk.load("signal.wfm")

# Reuse for multiple analyses
freq = tk.frequency(trace)
rise = tk.rise_time(trace)
amp = tk.amplitude(trace)

# Don't reload for each measurement
# BAD:
# freq = tk.frequency(tk.load("signal.wfm"))
# rise = tk.rise_time(tk.load("signal.wfm"))
```

## Analysis Best Practices

### Check Signal Suitability Before Measuring

```python
import tracekit as tk
import numpy as np

trace = tk.load("signal.wfm")

# Check if measurement is appropriate
suitability = tk.check_measurement_suitability(trace, "frequency")

if suitability['suitable']:
    freq = tk.frequency(trace)
    print(f"Frequency: {freq:.2f} Hz")
else:
    print(f"Warning: {suitability['warnings']}")
    print(f"Suggestions: {suitability['suggestions']}")
```

### Handle NaN Results Gracefully

```python
import tracekit as tk
import math

trace = tk.load("signal.wfm")

# Always check for NaN
freq = tk.frequency(trace)

if math.isnan(freq):
    # Signal may not be periodic - try alternatives
    classification = tk.classify_signal(trace)
    print(f"Signal type: {classification['signal_type']}")

    if not classification['is_periodic']:
        print("Signal is not periodic, frequency measurement not applicable")
else:
    print(f"Frequency: {freq / 1e6:.3f} MHz")
```

See the [NaN Handling Guide](nan-handling.md) for comprehensive NaN handling strategies.

### Use Appropriate Methods for Signal Types

```python
import tracekit as tk

trace = tk.load("signal.wfm")

# Classify first
info = tk.classify_signal(trace)

if info['signal_type'] == 'digital':
    # Use edge-based measurements
    freq = tk.frequency(trace, method='edge')
    rise = tk.rise_time(trace)
    duty = tk.duty_cycle(trace)

elif info['signal_type'] == 'analog':
    # Use FFT-based measurements
    freq = tk.frequency(trace, method='fft')
    thd = tk.thd(trace)
    snr = tk.snr(trace)
```

### Batch Processing Patterns

```python
import tracekit as tk
from pathlib import Path
import numpy as np

def batch_analyze(directory, pattern="*.wfm"):
    """Analyze all matching files in directory."""
    results = []
    errors = []

    for file_path in Path(directory).glob(pattern):
        try:
            trace = tk.load(file_path)
            freq = tk.frequency(trace)

            if not np.isnan(freq):
                results.append({
                    'file': file_path.name,
                    'frequency': freq,
                    'amplitude': tk.amplitude(trace),
                })
            else:
                errors.append((file_path.name, "Non-periodic signal"))

        except Exception as e:
            errors.append((file_path.name, str(e)))

    return results, errors

# Usage
results, errors = batch_analyze("captures/")
print(f"Analyzed {len(results)} files, {len(errors)} errors")
```

## Performance Best Practices

### Pre-compute FFT for Multiple Spectral Measurements

```python
import tracekit as tk
from tracekit.analyzers.spectral import (
    compute_fft,
    measure_snr,
    measure_thd,
)

trace = tk.load("signal.wfm")

# Compute FFT once
spectrum = compute_fft(trace, window="hanning")

# Reuse for multiple measurements
thd = measure_thd(trace, spectrum=spectrum)
snr = measure_snr(trace, signal_freq=1e6, spectrum=spectrum)

# Much faster than recomputing FFT each time
```

### Use GPU Acceleration When Available

```python
import tracekit as tk
from tracekit.analyzers.spectral import compute_fft

trace = tk.load("large_signal.wfm")

# Check and use GPU if available
if tk.gpu_available():
    spectrum = compute_fft(trace, use_gpu=True)
    print("Using GPU acceleration")
else:
    spectrum = compute_fft(trace)
    print("Using CPU")
```

### Optimize Sample Rates

```python
import tracekit as tk

# Only use the sample rate you need
# Over-sampling wastes memory and processing time

trace = tk.load("signal.wfm")

# Decimate if sample rate is excessive
if trace.metadata.sample_rate > 10 * expected_max_freq:
    # Use scipy decimation or TraceKit's built-in
    decimated = tk.decimate(trace, factor=10)
    result = tk.frequency(decimated)
```

## Code Organization Best Practices

### Create Reusable Analysis Functions

```python
import tracekit as tk
import numpy as np
from dataclasses import dataclass

@dataclass
class AnalysisResult:
    """Standard result container."""
    frequency: float
    amplitude: float
    rise_time: float
    signal_type: str
    quality_metrics: dict

def analyze_signal(trace_path: str) -> AnalysisResult:
    """Standard signal analysis workflow."""
    trace = tk.load(trace_path)

    # Classify signal
    info = tk.classify_signal(trace)

    # Basic measurements
    freq = tk.frequency(trace)
    amp = tk.amplitude(trace)
    rise = tk.rise_time(trace)

    # Quality metrics
    quality = tk.assess_signal_quality(trace)

    return AnalysisResult(
        frequency=freq if not np.isnan(freq) else 0.0,
        amplitude=amp,
        rise_time=rise if not np.isnan(rise) else 0.0,
        signal_type=info['signal_type'],
        quality_metrics=quality,
    )
```

### Use Configuration Objects

```python
from dataclasses import dataclass

@dataclass
class AnalysisConfig:
    """Analysis configuration."""
    frequency_method: str = "auto"
    window: str = "hanning"
    fft_size: int = 4096
    threshold: float = 0.5
    include_spectral: bool = True
    include_timing: bool = True

def analyze_with_config(trace_path: str, config: AnalysisConfig):
    """Configurable analysis."""
    trace = tk.load(trace_path)
    results = {}

    # Basic measurements
    results['frequency'] = tk.frequency(trace, method=config.frequency_method)
    results['amplitude'] = tk.amplitude(trace)

    if config.include_spectral:
        from tracekit.analyzers.spectral import compute_fft, measure_thd
        spectrum = compute_fft(trace, window=config.window, nfft=config.fft_size)
        results['thd'] = measure_thd(trace, spectrum=spectrum)

    if config.include_timing:
        results['rise_time'] = tk.rise_time(trace)
        results['fall_time'] = tk.fall_time(trace)

    return results
```

### Structured Error Handling

```python
import tracekit as tk
from tracekit.core.exceptions import LoaderError, MeasurementError

def safe_analyze(trace_path: str):
    """Analysis with comprehensive error handling."""
    try:
        trace = tk.load(trace_path)
    except FileNotFoundError:
        return {"error": "File not found", "file": trace_path}
    except LoaderError as e:
        return {"error": f"Load error: {e.message}", "hint": e.fix_hint}

    try:
        freq = tk.frequency(trace)
        rise = tk.rise_time(trace)

        return {
            "success": True,
            "frequency": freq,
            "rise_time": rise,
        }
    except MeasurementError as e:
        return {"error": f"Measurement error: {e.message}"}
```

## Memory Management Best Practices

### Release Large Objects When Done

```python
import tracekit as tk
import gc

def process_many_files(file_list):
    """Process files with memory management."""
    results = []

    for file_path in file_list:
        trace = tk.load(file_path)
        result = tk.frequency(trace)
        results.append(result)

        # Release memory
        del trace

        # Force garbage collection periodically
        if len(results) % 100 == 0:
            gc.collect()

    return results
```

### Use Context Managers for Resources

```python
import tracekit as tk

# For file operations that need cleanup
with tk.open_trace("signal.wfm") as trace:
    freq = tk.frequency(trace)
    amp = tk.amplitude(trace)
# Trace automatically closed/released
```

## Testing Best Practices

### Use Synthetic Data for Unit Tests

```python
import tracekit as tk
from tracekit.testing import generate_square_wave

def test_frequency_measurement():
    """Test frequency measurement with known signal."""
    # Generate signal with known frequency
    expected_freq = 1e6
    trace = generate_square_wave(
        frequency=expected_freq,
        sample_rate=100e6,
        duration=100e-6
    )

    # Measure
    measured_freq = tk.frequency(trace)

    # Verify within tolerance
    assert abs(measured_freq - expected_freq) / expected_freq < 0.01
```

### Test Edge Cases

```python
import tracekit as tk
from tracekit.testing import generate_dc_signal
import numpy as np

def test_frequency_dc_signal():
    """Verify NaN returned for DC signals."""
    dc = generate_dc_signal(level=1.0, sample_rate=1e6, duration=1e-3)
    freq = tk.frequency(dc)
    assert np.isnan(freq), "DC signal should return NaN for frequency"
```

## Common Anti-Patterns to Avoid

### Don't Reload Files Repeatedly

```python
# BAD - reloads file for each measurement
freq = tk.frequency(tk.load("signal.wfm"))
rise = tk.rise_time(tk.load("signal.wfm"))
amp = tk.amplitude(tk.load("signal.wfm"))

# GOOD - load once, reuse
trace = tk.load("signal.wfm")
freq = tk.frequency(trace)
rise = tk.rise_time(trace)
amp = tk.amplitude(trace)
```

### Don't Ignore NaN Results

```python
# BAD - ignores potential NaN
freq = tk.frequency(trace)
period = 1.0 / freq  # Crashes if freq is NaN

# GOOD - check for NaN
freq = tk.frequency(trace)
if not np.isnan(freq):
    period = 1.0 / freq
else:
    period = None
```

### Don't Use Wrong Methods for Signal Types

```python
# BAD - using edge method for noisy analog signal
freq = tk.frequency(noisy_analog, method='edge')  # May return NaN

# GOOD - use appropriate method
info = tk.classify_signal(noisy_analog)
if info['signal_type'] == 'analog':
    freq = tk.frequency(noisy_analog, method='fft')
```

### Don't Process Full Traces When Subsets Suffice

```python
# BAD - loads entire huge file for quick check
trace = tk.load("10GB_capture.wfm")
freq = tk.frequency(trace)

# GOOD - use lazy loading and take a subset
trace = tk.load("10GB_capture.wfm", lazy=True)
subset = trace[0:1000000]  # First million samples
freq = tk.frequency(subset)
```

## See Also

- [NaN Handling Guide](nan-handling.md) - Handling NaN measurement results
- [GPU Acceleration Guide](gpu-acceleration.md) - Performance optimization with GPU
- [Troubleshooting Guide](troubleshooting.md) - Common issues and solutions
- [Loading Waveforms Guide](loading-waveforms.md) - Data loading details
- [API Reference](../api/index.md) - Complete API documentation
