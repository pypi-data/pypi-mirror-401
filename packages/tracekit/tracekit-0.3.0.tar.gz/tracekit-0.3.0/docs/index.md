# TraceKit Documentation

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08

Welcome to the TraceKit documentation - your guide to digital waveform and protocol analysis.

## Quick Navigation

| Getting Started                       | Learn                             | Reference                     |
| ------------------------------------- | --------------------------------- | ----------------------------- |
| [Getting Started](getting-started.md) | [Tutorials](tutorials/index.md)   | [API Reference](api/index.md) |
| [Installation](installation.md)       | [Examples](examples-reference.md) | [CLI Reference](cli.md)       |
| [User Guide](user-guide.md)           | [Guides](guides/index.md)         | [Error Codes](error-codes.md) |

## What is TraceKit?

TraceKit is a comprehensive Python toolkit for digital waveform and protocol reverse engineering:

- **Multi-format Loading** - Tektronix, Rigol, Sigrok, LeCroy, CSV, HDF5, and more
- **Signal Analysis** - Frequency, timing, spectral, and statistical measurements
- **Protocol Decoding** - 16+ protocols (UART, SPI, I2C, CAN, and more)
- **Protocol Inference** - Automatic protocol detection and parameter discovery
- **Report Generation** - Professional PDF, HTML, and PowerPoint reports

## 5-Minute Quick Start

```python
import tracekit as tk

# Load a waveform (auto-detects format)
trace = tk.load("capture.wfm")

# Make measurements
freq = tk.frequency(trace)
rise_time = tk.rise_time(trace)

print(f"Frequency: {freq/1e6:.2f} MHz")
print(f"Rise time: {rise_time*1e9:.2f} ns")

# Decode protocol
from tracekit.protocols import UARTDecoder
decoder = UARTDecoder(baud_rate=115200)
messages = decoder.decode(trace)
```

See [Getting Started](getting-started.md) for a complete introduction.

## Documentation Sections

### Getting Started

- **[Getting Started](getting-started.md)** - 5-minute introduction to TraceKit
- **[Installation](installation.md)** - Installation options and setup
- **[User Guide](user-guide.md)** - Comprehensive usage guide

### Learning Resources

- **[Tutorials](tutorials/index.md)** - Step-by-step learning path
- **[Examples](examples-reference.md)** - Hands-on code examples (4-6 hour path)
- **[Guides](guides/index.md)** - Task-focused how-to guides

### Reference

- **[API Reference](api/index.md)** - Complete Python API documentation
- **[CLI Reference](cli.md)** - Command-line interface
- **[Error Codes](error-codes.md)** - Error handling reference
- **[Technical Reference](reference/index.md)** - Standards, formats, protocols

### Testing & Development

- **[Testing Guide](testing/index.md)** - Running and writing tests
- **[Contributing](contributing.md)** - Contribution guidelines

## Module Overview

| Module                        | Description                                   |
| ----------------------------- | --------------------------------------------- |
| `tracekit.core`               | Core data types and configuration             |
| `tracekit.loaders`            | File format loaders                           |
| `tracekit.pipeline`           | Pipeline composition & functional programming |
| `tracekit.analyzers.waveform` | Waveform measurements                         |
| `tracekit.analyzers.digital`  | Digital signal analysis                       |
| `tracekit.analyzers.spectral` | FFT, PSD, spectral metrics                    |
| `tracekit.analyzers.jitter`   | Jitter measurements                           |
| `tracekit.protocols`          | Protocol decoders (16+)                       |
| `tracekit.inference`          | Protocol reverse engineering                  |
| `tracekit.exporters`          | Data export (CSV, HDF5, etc.)                 |
| `tracekit.reporting`          | Report generation                             |
| `tracekit.visualization`      | Plotting utilities                            |

## Standards Compliance

TraceKit implements measurements according to industry standards:

- **IEEE 181-2011** - Pulse measurements (rise/fall time, overshoot)
- **IEEE 1057-2017** - Digitizer characterization
- **IEEE 1241-2010** - ADC testing (SNR, SINAD, ENOB)
- **IEEE 2414-2020** - Jitter measurements
- **JEDEC** - Timing specifications

## Common Tasks

### Load and Measure

```python
import tracekit as tk

trace = tk.load("capture.wfm")
freq = tk.frequency(trace)
```

### Decode Protocol

```python
from tracekit.protocols import UARTDecoder

decoder = UARTDecoder(baud_rate=115200)
messages = decoder.decode(trace)
```

### Generate Report

```python
from tracekit.reporting import generate_report, save_pdf_report

report = generate_report(trace, title="Analysis Report")
save_pdf_report(report, "report.pdf")
```

### Use CLI

```bash
# Analyze waveform
uv run tracekit analyze capture.wfm

# Decode protocol
uv run tracekit decode capture.wfm -p uart --baud 115200

# Generate report
uv run tracekit report capture.wfm -o report.pdf
```

## Getting Help

- **[Troubleshooting Guide](guides/troubleshooting.md)** - Common issues and solutions
- **[NaN Handling Guide](guides/nan-handling.md)** - Understanding NaN results
- **[Error Codes](error-codes.md)** - Complete error reference
- **GitHub Issues** - Report bugs or request features

## What's New

See [CHANGELOG.md](changelog.md) for version history and release notes.
