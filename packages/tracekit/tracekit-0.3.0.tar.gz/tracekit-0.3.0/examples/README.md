# TraceKit Examples - Complete Learning Path

> **Version**: 1.1.0 | **Last Updated**: 2026-01-12

Welcome to TraceKit examples! This directory contains a comprehensive, structured learning path from basic concepts to advanced analysis techniques with **100% API coverage**.

## Learning Path Structure

```
examples/
    01_basics/            <- Start here: Loading, measurements, export
    02_digital_analysis/  <- Edge detection, clock recovery, quality
    03_spectral_analysis/ <- FFT, THD, SNR, spectrograms
    04_protocol_decoding/ <- UART, SPI, I2C, CAN, auto-detect
    05_filtering/         <- Low/high/band-pass, notch filters
    06_export/            <- Data export formats (CSV, JSON, HDF5, MAT)
    07_math/              <- Arithmetic, calculus operations
    08_triggering/        <- Edge, pulse, glitch detection
    09_power/             <- Power analysis, efficiency, ripple
    10_advanced/          <- NaN handling, lazy eval, GPU, ensembles
    11_comparison/        <- Trace comparison, golden reference
    12_parallel_pipeline/ <- Parallel processing and pipelines
    13_expert_api/        <- Expert API, composition, streaming
    14_real_captures/     <- Real-world capture analysis
    configs/              <- YAML configuration examples
```

## Prerequisites

- Python 3.12+
- TraceKit installed (`uv sync`)
- Sample waveform files (see `test_data/README.md`)

## Estimated Time

| Section              | Duration  | Prerequisites       |
| -------------------- | --------- | ------------------- |
| 01_basics            | 30-45 min | None                |
| 02_digital_analysis  | 45-60 min | 01_basics           |
| 03_spectral_analysis | 30-45 min | 01_basics           |
| 04_protocol_decoding | 60 min    | 02_digital_analysis |
| 05_filtering         | 45 min    | 01_basics           |
| 06_export            | 20 min    | 01_basics           |
| 07_math              | 30 min    | 01_basics           |
| 08_triggering        | 30 min    | 02_digital_analysis |
| 09_power             | 45 min    | 01_basics           |
| 10_advanced          | 60+ min   | Most previous       |
| 11_comparison        | 30 min    | 01_basics           |
| 12_parallel_pipeline | 45 min    | 01_basics           |
| 13_expert_api        | 60+ min   | All previous        |
| 14_real_captures     | 30 min    | 01-04               |

**Total learning path**: 8-10 hours
**Quick start (basics only)**: 30-45 minutes

## Running Examples

Each example is a standalone Python script:

```bash
# Run a single example
uv run python examples/01_basics/01_load_waveform.py

# Run with test data
uv run python examples/01_basics/01_load_waveform.py test_data/sample.wfm
```

### Run All Examples in a Section

```bash
# Run all basics examples
uv run python examples/run_all_examples.py --section 01_basics

# Run all examples (full validation)
uv run python examples/run_all_examples.py

# Stop on first error
uv run python examples/run_all_examples.py --stop-on-error
```

## Quick Start

### 1. Load Your First Waveform

```python
import tracekit as tk

# Load a waveform file
trace = tk.load("capture.wfm")

# Check what we loaded
print(f"Samples: {len(trace.data)}")
print(f"Sample rate: {trace.metadata.sample_rate} Hz")
```

### 2. Make Basic Measurements

```python
# Measure frequency
freq = tk.frequency(trace)
print(f"Frequency: {freq/1e6:.2f} MHz")

# Measure rise time
rise = tk.rise_time(trace)
print(f"Rise time: {rise*1e9:.2f} ns")
```

### 3. Filter a Signal

```python
# Low-pass filter to remove noise
filtered = tk.low_pass(trace, cutoff=1e6)

# Notch filter to remove 60 Hz hum
clean = tk.notch_filter(trace, notch_freq=60, q=30)
```

### 4. Decode a Protocol

```python
# Decode UART data
frames = tk.decode_uart(trace, baud_rate=115200)

for frame in frames:
    print(f"[{frame.timestamp:.6f}s] {frame.data.hex()}")
```

## Section Overview

### 01_basics - Getting Started

**Prerequisites**: None | **Time**: 30-45 minutes

- Loading waveform files (WFM, CSV, VCD, etc.)
- Basic time-domain measurements
- Plotting and visualization
- Exporting data
- Generating reports

### 02_digital_analysis - Digital Signal Processing

**Prerequisites**: 01_basics | **Time**: 45-60 minutes

- Clock recovery from data signals
- Edge detection and timing
- Bus decoding fundamentals
- Signal quality metrics
- Multi-channel analysis

### 03_spectral_analysis - Frequency Domain

**Prerequisites**: 01_basics | **Time**: 30-45 minutes

- FFT computation and plotting
- THD, SNR, SINAD, ENOB measurements
- Harmonic analysis
- Spectrogram generation
- Jitter analysis

### 04_protocol_decoding - Serial Protocols

**Prerequisites**: 02_digital_analysis | **Time**: 60 minutes

- UART/RS-232 decoding
- SPI bus decoding
- I2C bus decoding
- CAN bus decoding
- Automatic protocol detection

### 05_filtering - Signal Filtering

**Prerequisites**: 01_basics | **Time**: 45 minutes

- Low-pass filtering (noise removal)
- High-pass filtering (DC removal)
- Band-pass and band-stop filters
- Notch filters (power line hum)
- Custom filter design

### 06_expert_api - Expert Mode

**Prerequisites**: All previous | **Time**: 60+ minutes

- Pipeline architecture
- Function composition
- Streaming analysis
- Custom measurements
- Plugin system

### 07_math - Math Operations

**Prerequisites**: 01_basics | **Time**: 30 minutes

- Arithmetic (add, subtract, multiply, divide)
- Calculus (differentiate, integrate)
- Scaling and offset
- Interpolation and resampling

### 08_triggering - Event Detection

**Prerequisites**: 02_digital_analysis | **Time**: 30 minutes

- Edge triggering (rising/falling)
- Pulse width triggering
- Glitch and runt detection
- Pattern matching

### 09_power - Power Analysis

**Prerequisites**: 01_basics | **Time**: 45 minutes

- Instantaneous and average power
- Power factor and reactive power
- Efficiency calculations
- Ripple analysis

### 10_signal_integrity - Signal Quality

**Prerequisites**: 03_spectral | **Time**: 45 minutes

- Eye diagram generation
- Eye metrics (height, width)
- Mask testing
- Jitter measurements

### 11_comparison - Trace Comparison

**Prerequisites**: 01_basics | **Time**: 30 minutes

- Correlation and similarity
- Golden waveform comparison
- Limit testing
- Mask testing

### 14_session - Session Management

**Prerequisites**: 01_basics | **Time**: 30 minutes

- Creating analysis sessions
- Adding annotations
- Operation history
- Save and restore state

### configs/ - Configuration Examples

YAML configuration files for:

- Packet format definitions
- Device mappings
- Bus configurations
- Protocol definitions
- Report customization

## API Coverage

This example suite provides **complete coverage** of TraceKit's public API:

| Category     | Coverage | Examples               |
| ------------ | -------- | ---------------------- |
| Loaders      | 95%      | 01_basics, 05_advanced |
| Measurements | 100%     | 01_basics, 02_digital  |
| Spectral     | 100%     | 03_spectral            |
| Digital      | 95%      | 02_digital             |
| Protocols    | 80%      | 04_protocol            |
| Filtering    | 100%     | 05_filtering           |
| Triggering   | 90%      | 08_triggering          |
| Math         | 100%     | 07_math                |
| Power        | 100%     | 09_power               |
| Comparison   | 100%     | 11_comparison          |
| Session      | 100%     | 14_session             |

## Philosophy

TraceKit examples demonstrate **real-world workflows**, not just API coverage.
Each example solves a practical problem you would encounter in signal analysis:

- **Realistic scenarios**: Based on actual use cases
- **Progressive complexity**: Build on previous concepts
- **Self-contained**: Each example runs independently
- **Well-documented**: Clear comments explaining each step
- **Error handling**: Shows how to handle common issues

## Using Test Data

Most examples work with synthetic data or test data in the `test_data/` directory:

```bash
# List available test files
ls test_data/

# Examples auto-detect test data location
uv run python examples/01_basics/01_load_waveform.py
```

Or use your own waveform files:

```bash
uv run python examples/01_basics/01_load_waveform.py /path/to/your/file.wfm
```

## Generating Synthetic Data

For learning without real waveform files:

```python
from tracekit.testing import generate_sine_wave, generate_square_wave

# Generate a test sine wave
trace = generate_sine_wave(
    frequency=1e6,
    sample_rate=100e6,
    duration=1e-3
)

# Generate square wave
square = generate_square_wave(
    frequency=500e3,
    duty_cycle=0.5,
    sample_rate=10e6
)
```

## Troubleshooting

### Example won't run

```bash
# Verify TraceKit is installed
uv run python -c "import tracekit; print(tracekit.__version__)"

# Check for missing dependencies
uv sync
```

### Can't find test data

```bash
# Examples look for test_data/ relative to repo root
cd /path/to/tracekit
uv run python examples/01_basics/01_load_waveform.py
```

### Need more help

- See [Getting Started](../docs/getting-started.md)
- See [User Guide](../docs/user-guide.md)
- See [Troubleshooting](../docs/guides/troubleshooting.md)

## Contributing Examples

We welcome new examples! Guidelines:

1. Follow existing naming convention: `##_descriptive_name.py`
2. Include docstring with purpose and concepts covered
3. Use test data or synthetic generation (no external files)
4. Add error handling for common issues
5. Update section README with new example
6. Run `examples/run_all_examples.py` to verify

## See Also

- [Getting Started](../docs/getting-started.md) - Quick introduction
- [User Guide](../docs/user-guide.md) - Comprehensive guide
- [API Reference](../docs/api/index.md) - Complete documentation
- [Test Data Guide](../test_data/README.md) - About test data
