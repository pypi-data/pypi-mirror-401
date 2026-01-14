# TraceKit Examples - Learning Path

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08

Welcome to TraceKit examples! This directory contains a structured learning path
from basic concepts to advanced analysis techniques.

## Learning Path Structure

```
examples/
    01_basics/           <- Start here
    02_digital_analysis/ <- Clock recovery, edge detection
    03_spectral_analysis/ <- FFT, THD, spectrograms
    04_protocol_decoding/ <- UART, SPI, I2C, CAN
    05_advanced/         <- NaN handling, GPU, ensemble
    06_expert_api/       <- Expert mode, discovery
    configs/             <- YAML configuration examples
```

## Prerequisites

- Python 3.12+
- TraceKit installed (`uv sync`)
- Sample waveform files (see `#prerequisites`)

## Estimated Time

| Section              | Duration  | Prerequisites       |
| -------------------- | --------- | ------------------- |
| 01_basics            | 30-45 min | None                |
| 02_digital_analysis  | 45-60 min | 01_basics           |
| 03_spectral_analysis | 30-45 min | 01_basics           |
| 04_protocol_decoding | 60 min    | 02_digital_analysis |
| 05_advanced          | 45-60 min | 01-04               |
| 06_expert_api        | 60+ min   | All previous        |

**Total learning path**: 4-6 hours
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
freq = tk.measure_frequency(trace)
print(f"Frequency: {freq/1e6:.2f} MHz")

# Measure rise time
rise_time = tk.measure_rise_time(trace)
print(f"Rise time: {rise_time*1e9:.2f} ns")
```

### 3. Decode a Protocol

```python
from tracekit.protocols import UARTDecoder

decoder = UARTDecoder(baud_rate=115200)
messages = decoder.decode(trace)

for msg in messages:
    print(f"[{msg.timestamp:.6f}s] {msg.data.hex()}")
```

## Section Overview

<a id="01-basics"></a>

### 01_basics - Getting Started

**Prerequisites**: None
**Time**: 30-45 minutes

Learn fundamental TraceKit operations:

- Loading waveform files
- Basic time-domain measurements
- Plotting and visualization
- Exporting data
- Generating reports

Start here: See the examples above.

### 02_digital_analysis - Digital Signal Processing

**Prerequisites**: 01_basics
**Time**: 45-60 minutes

Digital signal analysis techniques:

- Clock recovery from data signals
- Edge detection and timing
- Bus decoding fundamentals
- Signal quality metrics
- Multi-channel analysis

### 03_spectral_analysis - Frequency Domain

**Prerequisites**: 01_basics
**Time**: 30-45 minutes

Spectral and frequency analysis:

- FFT computation and plotting
- THD and SNR measurements
- Harmonic analysis
- Spectrogram generation
- Jitter analysis

### 04_protocol_decoding - Serial Protocols

**Prerequisites**: 02_digital_analysis
**Time**: 60 minutes

Decode common serial protocols:

- UART/RS-232 decoding
- SPI bus decoding
- I2C bus decoding
- CAN bus decoding
- Automatic protocol detection

<a id="05-advanced"></a>

### 05_advanced - Advanced Topics

**Prerequisites**: 01-04
**Time**: 45-60 minutes

Advanced analysis techniques:

- Handling NaN results
- Lazy loading for large files
- GPU acceleration
- Ensemble analysis
- Cross-domain correlation
- Eye diagram analysis
- Batch processing

### 06_expert_api - Expert Mode

**Prerequisites**: All previous
**Time**: 60+ minutes

Power user features:

- Expert API usage
- Advanced configuration
- Adaptive parameter tuning
- Audit trail tracking
- Discovery mode for exploration

### configs/ - Configuration Examples

YAML configuration files for:

- Packet format definitions
- Device mappings
- Bus configurations
- Protocol definitions
- Report customization

## Philosophy

TraceKit examples demonstrate **real-world workflows**, not just API coverage.
Each example solves a practical problem you would encounter in signal analysis:

- **Realistic scenarios**: Based on actual use cases
- **Progressive complexity**: Build on previous concepts
- **Self-contained**: Each example runs independently
- **Well-documented**: Clear comments explaining each step
- **Error handling**: Shows how to handle common issues

## Using Test Data

Most examples work with test data in the `test_data/` directory:

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
from tracekit.testing import generate_sine_wave, generate_uart_signal

# Generate a test sine wave
trace = generate_sine_wave(
    frequency=1e6,
    sample_rate=100e6,
    duration=1e-3
)

# Generate UART test signal
uart_trace = generate_uart_signal(
    message=b"Hello, World!",
    baud_rate=115200,
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

- See [Getting Started](./getting-started.md)
- See [User Guide](./user-guide.md)
- See [Troubleshooting](./guides/troubleshooting.md)

## Contributing Examples

We welcome new examples! Guidelines:

1. Follow existing naming convention: `##_descriptive_name.py`
2. Include docstring with purpose and concepts covered
3. Use test data or synthetic generation (no external files)
4. Add error handling for common issues
5. Update section README with new example
6. Run `examples/run_all_examples.py` to verify

## See Also

- [Getting Started](./getting-started.md) - Quick introduction
- [User Guide](./user-guide.md) - Comprehensive guide
- [API Reference](./api/index.md) - Complete documentation
- [Test Data Guide](../#prerequisites) - About test data
