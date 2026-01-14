# TraceKit

[![Version](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Flair-click-bats%2Ftracekit%2Fmain%2Fpyproject.toml&query=%24.project.version&label=version&color=blue)](https://github.com/lair-click-bats/tracekit/releases)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![IEEE](https://img.shields.io/badge/IEEE-compliant-informational.svg)](docs/)

**The open-source toolkit for reverse engineering ANY system from captured waveforms—analog or digital, simple or complex**

TraceKit provides comprehensive signal analysis across analog and digital domains. Analyze audio amplifiers (THD, SNR), power supplies (ripple, efficiency), RF baseband, sensors, control systems, logic circuits, IoT protocols (UART, SPI, I2C, CAN + 16 more), and mixed-signal systems. Features include IEEE-compliant measurements (181, 1241, 1459, 2414), spectral analysis (FFT, PSD, wavelets), power analysis (AC/DC, efficiency), protocol decoding and reverse engineering (state machine inference, CRC recovery), and compliance validation (EMC, power quality).

---

## Why TraceKit?

| Challenge                             | TraceKit Solution                                         |
| ------------------------------------- | --------------------------------------------------------- |
| Analyzing audio amplifier distortion  | **THD, SNR, SINAD** with IEEE 1241 compliance             |
| Characterizing power supply ripple    | **AC/DC power analysis**, efficiency, ripple metrics      |
| Unknown protocol on captured waveform | **Protocol inference** with automatic parameter detection |
| Analyzing proprietary bus protocols   | **State machine learning** from captured traffic          |
| Validating signal integrity           | **IEEE-compliant measurements** (181, 1241, 2414)         |
| Debugging embedded systems            | **16+ protocol decoders** (UART, SPI, I2C, CAN, JTAG...)  |
| EMC pre-compliance testing            | **CISPR/FCC limit mask testing** with reports             |
| RF baseband spectral analysis         | **FFT, PSD, spectrograms** with windowing options         |

---

## Key Capabilities

### Analog Signal Analysis

- **Audio Analysis** - THD, SNR, SINAD, ENOB, harmonic distortion (IEEE 1241-2010)
- **Power Analysis** - AC/DC power, efficiency, ripple, power factor (IEEE 1459), SOA testing
- **RF/Spectral** - FFT, PSD, spectrograms, wavelets, frequency-domain characterization
- **Waveform Measurements** - Rise/fall time, frequency, duty cycle, overshoot (IEEE 181-2011)

### Digital Signal Analysis

- **Protocol Decoders** - UART, SPI, I2C, CAN, CAN-FD, 1-Wire, LIN, JTAG, SWD, I2S, USB, HDLC, Manchester, FlexRay
- **Protocol Inference** - CRC reverse engineering, L\* active learning, state machine learning, field boundary detection
- **Signal Integrity** - Jitter decomposition, eye diagrams, S-parameter analysis, TDR (IEEE 2414-2020)

### Automotive Protocols

- **CAN Bus Reverse Engineering** - Message discovery, signal extraction, DBC generation, checksum detection
- **Automotive Decoders** - OBD-II (54 PIDs), J1939 (154 PGNs), UDS (17 services), DTC database (210 codes)

### Compliance & Validation

- **EMC Compliance** - CISPR/FCC/CE limit mask testing with automated reporting
- **File Format Support** - Tektronix WFM, Rigol, Sigrok, VCD, PCAP, TDMS, WAV, CSV, HDF5, Touchstone, BLF, ASC, MDF

---

## Quick Start

### Installation

```bash
# Using pip
pip install tracekit

# From source
git clone https://github.com/lair-click-bats/tracekit.git
cd tracekit
pip install -e ".[dev]"
```

### 30-Second Example

```python
import tracekit as tk

# Load waveform (auto-detects format)
trace = tk.load("capture.wfm")

# Make measurements
print(f"Rise time: {tk.rise_time(trace):.2e} s")
print(f"Frequency: {tk.frequency(trace):.2f} Hz")

# Decode protocol
uart = tk.decode_uart(trace, baudrate=115200)
for frame in uart:
    print(f"UART: {frame.data.hex()}")
```

**→ See [docs/getting-started.md](docs/getting-started.md) for complete introduction**

**→ See [examples/](examples/) for 50+ working code examples**

---

## Documentation

### For Users

- **[Getting Started](docs/getting-started.md)** - 5-minute introduction with examples
- **[User Guide](docs/user-guide.md)** - Comprehensive usage guide
- **[API Reference](docs/api/index.md)** - Complete Python API documentation
- **[Tutorials](docs/tutorials/index.md)** - Step-by-step learning path
- **[Examples](examples/)** - 50+ working examples organized by category
- **[Guides](docs/guides/index.md)** - Task-focused how-to guides

### For Developers

- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Development workflow, PR process, commit format
- **[Testing Guide](docs/testing/index.md)** - Running and writing tests
- **[CLAUDE.md](CLAUDE.md)** - AI context: how to work effectively in this repo
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and release notes

---

## Core Features

### Signal Analysis

IEEE-compliant measurements for characterization and validation. TraceKit implements standards IEEE 181-2011 (pulse), IEEE 1241-2010 (ADC), IEEE 2414-2020 (jitter).

**→ See [docs/api/analysis.md](docs/api/analysis.md) for full measurement API**

### Protocol Decoding

Decode embedded protocols directly from waveforms. Supports 16+ protocols including serial (UART, SPI, I2C), automotive (CAN, LIN, FlexRay), and debug (JTAG, SWD).

**→ See [docs/reference/protocol-decoders.md](docs/reference/protocol-decoders.md) for protocol list**

**→ See [examples/04_protocol_decoding/](examples/04_protocol_decoding/) for examples**

### Spectral Analysis

Frequency-domain analysis with IEEE 1241-2010 compliance. FFT, PSD, ADC quality metrics (SNR, THD, SINAD, ENOB, SFDR), time-frequency analysis.

**→ See [docs/tutorials/04-spectral-analysis.md](docs/tutorials/04-spectral-analysis.md)**

### Signal Integrity

High-speed digital validation: jitter measurements (IEEE 2414-2020), eye diagrams, S-parameters, TDR, channel equalization.

**→ See [docs/guides/signal-integrity.md](docs/guides/signal-intelligence.md)**

### Protocol Reverse Engineering

Analyze unknown protocols with:

- **CRC Polynomial Reverse Engineering** - Recover CRC parameters from samples
- **L\* Active Learning** - Infer protocol state machines from traffic
- **Field Boundary Detection** - Automatically detect binary field boundaries
- **Wireshark Dissector Export** - Generate Wireshark dissectors from definitions

**→ See [CHANGELOG.md](CHANGELOG.md) [Unreleased] section for latest features**

**→ See [examples/05_export/](examples/05_export/) for Wireshark export examples**

---

## File Formats

| Format        | Extensions           | Description                 |
| ------------- | -------------------- | --------------------------- |
| Tektronix WFM | `.wfm`               | Tektronix oscilloscopes     |
| Rigol WFM     | `.wfm`               | Rigol oscilloscopes         |
| Sigrok        | `.sr`                | Sigrok/PulseView captures   |
| VCD           | `.vcd`               | Value Change Dump (digital) |
| PCAP          | `.pcap`, `.pcapng`   | Network packet captures     |
| TDMS          | `.tdms`              | NI LabVIEW                  |
| Touchstone    | `.s1p`, `.s2p`, etc. | S-parameter data            |
| WAV           | `.wav`               | Audio waveforms             |
| CSV           | `.csv`               | Generic time-series         |
| HDF5          | `.h5`, `.hdf5`       | Scientific data             |
| NumPy         | `.npz`               | NumPy arrays                |

**→ See [docs/guides/loading-waveforms.md](docs/guides/loading-waveforms.md) for format details**

---

## IEEE Standards Compliance

TraceKit implements measurements according to industry standards:

| Standard       | Domain                     | Measurements                |
| -------------- | -------------------------- | --------------------------- |
| IEEE 181-2011  | Pulse measurements         | Rise/fall time, slew rate   |
| IEEE 1057-2017 | Digitizer characterization | Timing analysis             |
| IEEE 1241-2010 | ADC testing                | SNR, SINAD, ENOB, THD, SFDR |
| IEEE 2414-2020 | Jitter measurements        | TIE, period jitter, RJ/DJ   |
| IEEE 1459      | Power measurements         | Power quality analysis      |
| IEC 61000-4-7  | Power quality              | Harmonics analysis          |

**→ See [docs/reference/standards-compliance.md](docs/reference/standards-compliance.md)**

---

## Development

### Quick Start

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/unit -v

# Quality checks
ruff check src/ tests/
ruff format src/ tests/
mypy src/
```

**→ See [CONTRIBUTING.md](CONTRIBUTING.md) for complete development guide**

**→ See [docs/testing/index.md](docs/testing/index.md) for testing strategy**

---

## Project Structure

```
tracekit/
├── src/tracekit/       # Source code
│   ├── loaders/        # File format parsers
│   ├── analyzers/      # Signal analysis (waveform, digital, spectral, jitter, protocols)
│   ├── inference/      # Protocol reverse engineering
│   ├── export/         # Wireshark dissectors, data export
│   └── reporting/      # Report generation
├── tests/              # Test suite (17,000+ tests)
│   ├── unit/           # Unit tests
│   ├── integration/    # Integration tests
│   └── compliance/     # Standards compliance tests
├── docs/               # Documentation
├── examples/           # 50+ working code examples
└── scripts/            # Development utilities
```

**→ See [docs/index.md](docs/index.md) for documentation structure**

---

## Links

- **Documentation**: [docs/index.md](docs/index.md)
- **Repository**: [github.com/lair-click-bats/tracekit](https://github.com/lair-click-bats/tracekit)
- **Issues**: [github.com/lair-click-bats/tracekit/issues](https://github.com/lair-click-bats/tracekit/issues)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **License**: [MIT](LICENSE)

---

## Citation

If you use TraceKit in your research, please cite:

```bibtex
@software{tracekit2026,
  title = {TraceKit: Analog and Digital Signal Reverse Engineering Toolkit},
  author = {TraceKit Contributors},
  year = {2026},
  url = {https://github.com/lair-click-bats/tracekit}
}
```
