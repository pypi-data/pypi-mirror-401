# Getting Started with TraceKit

> **Version**: 0.2.0 | **Last Updated**: 2026-01-12 | **Applies to**: TraceKit 0.2.x

Welcome to TraceKit! This guide will have you analyzing waveforms in under 5 minutes.

## What is TraceKit?

TraceKit is a Python toolkit for digital waveform and protocol reverse engineering. It provides:

- **Multi-format Loading** - Support for Tektronix, Rigol, Sigrok, and more
- **Signal Analysis** - Frequency, timing, spectral, and statistical analysis
- **Protocol Decoding** - 16+ protocols including UART, SPI, I2C, CAN
- **Protocol Inference** - Automatic protocol detection and field discovery
- **Report Generation** - PDF, HTML, and PowerPoint output

## Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)

## Quick Installation

```bash
# Clone the repository
git clone https://github.com/your-org/tracekit.git
cd tracekit

# Install dependencies
uv sync

# Verify installation
uv run python -c "import tracekit; print(tracekit.__version__)"
```

For detailed installation options, see [Installation Guide](installation.md).

## Your First Analysis (5 Minutes)

### Step 1: Load a Waveform

```python
import tracekit as tk

# Load a waveform file (auto-detects format)
trace = tk.load("capture.wfm")

# Check what we loaded
print(f"Samples: {len(trace.data)}")
print(f"Sample rate: {trace.metadata.sample_rate} Hz")
print(f"Duration: {trace.duration:.3f} s")
```

### Step 2: Basic Measurements

```python
# Measure frequency
freq = tk.frequency(trace)
print(f"Frequency: {freq:.2f} Hz")

# Measure rise time
rise_time = tk.rise_time(trace)
print(f"Rise time: {rise_time * 1e9:.2f} ns")

# Get amplitude statistics
amplitude = tk.amplitude(trace)
print(f"Amplitude: {amplitude:.3f} V")
```

### Step 3: Visualize

```python
# Quick plot
tk.plot_waveform(trace, title="My First Waveform")

# Or export to file
tk.plot_waveform(trace, output="waveform.png")
```

### Step 4: Export Results

```python
# Export to CSV
tk.export_csv(trace, "results.csv")

# Or to HDF5 for large datasets
tk.export_hdf5(trace, "results.h5")
```

## CLI Quick Start

TraceKit also provides a command-line interface:

```bash
# Analyze a waveform file
uv run tracekit analyze capture.wfm

# Decode a protocol
uv run tracekit decode capture.wfm --protocol uart --baud 115200

# Generate a report
uv run tracekit report capture.wfm -o report.pdf
```

## Understanding the Output

### WaveformTrace Objects

When you load a waveform, you get a `WaveformTrace` object:

```python
trace = tk.load("capture.wfm")

# Access the raw data (NumPy array)
trace.data  # Shape: (num_samples,)

# Access metadata
trace.metadata.sample_rate    # Samples per second
trace.metadata.source_file    # Original filename
trace.metadata.channel_name   # Channel identifier
trace.metadata.vertical_scale # Vertical scale in V/div (if available)

# Computed properties
trace.duration               # Total capture duration in seconds
trace.time_vector            # Time values for each sample
```

### Digital Traces

For digital captures:

```python
from tracekit import DigitalTrace

trace = tk.load("digital_capture.wfm")

if isinstance(trace, DigitalTrace):
    # Boolean data (True = high, False = low)
    print(f"Duty cycle: {trace.data.mean() * 100:.1f}%")

    # Edge information
    if trace.edges:
        print(f"Edges detected: {len(trace.edges)}")
```

## Common Tasks

### Multi-Channel Loading

```python
# Load all channels at once
channels = tk.load_all_channels("multi_channel.wfm")

for name, trace in channels.items():
    print(f"{name}: {len(trace.data)} samples")
```

### Protocol Decoding

```python
import tracekit as tk

# Using convenience function
messages = tk.decode_uart(trace, baudrate=115200)

for msg in messages:
    print(f"[{msg.timestamp:.6f}s] {msg.data.hex()}")
```

### Spectral Analysis

```python
import numpy as np

# Compute FFT - returns (frequencies, magnitudes_db) tuple
freq, mag = tk.fft(trace, window="hann")

# Compute power spectral density
psd_freq, psd_mag = tk.psd(trace, window="hann")

# Find dominant frequency (peak in FFT magnitude)
peak_idx = np.argmax(mag)
peak_freq = freq[peak_idx]
print(f"Peak at {peak_freq/1e6:.2f} MHz: {mag[peak_idx]:.1f} dB")
```

## Next Steps

Now that you have the basics, explore these topics:

### Tutorials (Step-by-Step)

1. [Loading Data](tutorials/01-loading-data.md) - File formats and options
2. [Basic Measurements](tutorials/02-basic-measurements.md) - Timing and amplitude
3. [Spectral Analysis](tutorials/04-spectral-analysis.md) - FFT and harmonics
4. [Protocol Decoding](tutorials/05-protocol-decoding.md) - Decode serial protocols

### Examples (Hands-On)

Start with the [examples](examples-reference.md) for practical code you can run immediately.

### Guides (Task-Focused)

- [Loading Waveforms](guides/loading-waveforms.md) - Detailed loading options
- [NaN Handling](guides/nan-handling.md) - Dealing with invalid measurements
- [GPU Acceleration](guides/gpu-acceleration.md) - Speed up large analyses

### Reference

- [API Reference](api/index.md) - Complete function documentation
- [CLI Reference](cli.md) - Command-line options
- [Supported Formats](reference/supported-formats.md) - File format details

## Getting Help

- **Examples**: See `examples/` directory
- **API Docs**: Each function has comprehensive docstrings
- **Issues**: Report bugs on GitHub

## Common Questions

**Q: What file formats are supported?**

A: TraceKit supports Tektronix WFM, Rigol WFM, Sigrok SR, LeCroy TRC, CSV, NPZ, HDF5, and more. See [Supported Formats](reference/supported-formats.md).

**Q: How do I handle large files?**

A: Use lazy loading for files over 100MB:

```python
trace = tk.load("huge_capture.wfm", lazy=True)
chunk = trace.data[0:10000]  # Only loads what you need
```

**Q: My measurement returns NaN - what's wrong?**

A: This usually means the signal doesn't meet the measurement requirements (e.g., measuring frequency on DC, or analog measurements on digital signals). See [NaN Handling Guide](guides/nan-handling.md).

**Q: How do I decode an unknown protocol?**

A: Use the inference module:

```python
from tracekit.inference import detect_protocol

result = detect_protocol(trace)
print(f"Detected: {result.protocol_type}")
print(f"Confidence: {result.confidence:.1%}")
```

---

Ready to dive deeper? Start with the [tutorials](tutorials/index.md) or explore the [examples](examples-reference.md).
