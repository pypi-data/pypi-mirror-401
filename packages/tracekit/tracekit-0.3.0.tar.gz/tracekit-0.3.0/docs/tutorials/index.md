# Tutorials

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08

Step-by-step tutorials for learning TraceKit, from basics to advanced topics.

## Learning Path

Complete these tutorials in order for a comprehensive understanding:

| #   | Tutorial                                         | Time   | Prerequisites |
| --- | ------------------------------------------------ | ------ | ------------- |
| 1   | [Loading Data](01-loading-data.md)               | 15 min | Python basics |
| 2   | [Basic Measurements](02-basic-measurements.md)   | 20 min | Tutorial 1    |
| 3   | [Digital Signal Analysis](03-digital-signals.md) | 25 min | Tutorial 2    |
| 4   | [Spectral Analysis](04-spectral-analysis.md)     | 30 min | Tutorial 2    |
| 5   | [Protocol Decoding](05-protocol-decoding.md)     | 35 min | Tutorial 3    |
| 6   | [Report Generation](06-report-generation.md)     | 20 min | Tutorials 1-5 |

**Total time**: Approximately 2.5 hours

## Tutorial Descriptions

### Tutorial 1: Loading Data

Learn to load waveform data from various file formats.

**Topics covered:**

- Loading from oscilloscope formats (Tektronix, Rigol)
- Loading from generic formats (CSV, HDF5, NumPy)
- Understanding WaveformTrace structure
- Working with metadata
- Handling large files

**What you'll build:**

- Load and inspect a waveform file
- Extract timing and channel information

### Tutorial 2: Basic Measurements

Perform fundamental waveform measurements.

**Topics covered:**

- Frequency and period measurement
- Amplitude and RMS calculation
- Rise and fall time (IEEE 181-2011)
- Edge detection
- Handling NaN results

**What you'll build:**

- Complete measurement suite for a test signal
- NaN-safe measurement wrapper

### Tutorial 3: Digital Signal Analysis

Analyze digital signals and extract timing information.

**Topics covered:**

- Converting analog to digital
- Clock recovery
- Pattern detection
- Pulse width analysis
- Glitch detection

**What you'll build:**

- Digital signal analyzer with timing report

### Tutorial 4: Spectral Analysis

Analyze signals in the frequency domain.

**Topics covered:**

- FFT computation and windowing
- Power spectral density
- THD, SNR, SINAD measurements
- Harmonic analysis
- GPU acceleration

**What you'll build:**

- Signal quality analyzer with spectral plots

### Tutorial 5: Protocol Decoding

Decode serial communication protocols.

**Topics covered:**

- UART/RS-232 decoding
- SPI bus analysis
- I2C bus analysis
- Auto-detection of protocol parameters
- Error handling

**What you'll build:**

- Multi-protocol decoder with auto-detection

### Tutorial 6: Report Generation

Generate professional analysis reports.

**Topics covered:**

- Report configuration
- Multiple export formats (PDF, HTML, JSON)
- Custom sections and plots
- Pass/fail specifications
- Batch processing

**What you'll build:**

- Automated test report generator

## Quick Start

If you're short on time, start with these essential tutorials:

1. **[Loading Data](01-loading-data.md)** (15 min) - Required for everything
2. **[Basic Measurements](02-basic-measurements.md)** (20 min) - Core functionality

Then pick based on your needs:

- Analyzing digital/logic signals: [Tutorial 3](03-digital-signals.md)
- Signal quality metrics: [Tutorial 4](04-spectral-analysis.md)
- Protocol reverse engineering: [Tutorial 5](05-protocol-decoding.md)

## Prerequisites

Before starting the tutorials:

1. **Install TraceKit**:

   ```bash
   uv sync
   ```

2. **Verify installation**:

   ```python
   import tracekit as tk
   print(tk.__version__)
   ```

3. **Optional**: Install visualization dependencies:

   ```bash
   uv sync --extra viz
   ```

## Tutorials vs Examples vs Guides

| Resource  | Purpose                             | Format          |
| --------- | ----------------------------------- | --------------- |
| Tutorials | Learn concepts step-by-step         | Sequential path |
| Examples  | See working code for specific tasks | Standalone code |
| Guides    | Solve specific problems             | Task-focused    |

**Tutorials** teach you concepts progressively.
**Examples** show you code you can copy and adapt.
**Guides** help you solve specific problems.

## Next Steps After Tutorials

Once you've completed the tutorials:

- **[Examples](../examples-reference.md)** - Real-world code examples
- **[User Guide](../user-guide.md)** - Comprehensive reference
- **[API Reference](../api/index.md)** - Complete API documentation

## See Also

- [Getting Started](../getting-started.md) - Quick 5-minute introduction
- [Examples](../examples-reference.md) - Working code examples
- [Guides](../guides/index.md) - Task-focused how-to guides
