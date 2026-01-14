# TraceKit Brand Guidelines

**Version:** 1.0
**Last Updated:** 2026-01-06
**Purpose:** Contributor guidelines for consistent naming and terminology

---

## Name & Capitalization

### Official Name

**TraceKit** (one word, capital T, capital K)

### Package & Import Names

```python
# PyPI package name (lowercase, one word)
uv pip install tracekit

# Python import (lowercase, one word)
import tracekit
import tracekit as tk  # Recommended alias
from tracekit import load, rise_time, fft

# CLI command (lowercase, one word)
tracekit characterize input.wfm
```

### Usage Rules

✅ **CORRECT:**

- TraceKit is a digital waveform analysis framework
- The TraceKit project
- Using TraceKit for signal analysis
- Install `uv pip install tracekit` (in code blocks)
- Import `tracekit` or `import tracekit as tk` (in code)

❌ **INCORRECT:**

- tracekit (no capital T in prose)
- Trace-Kit (hyphen in prose)
- trace-kit (hyphenated)
- Trace Kit (two words)
- TK (too generic, conflicts with Tkinter)

### Context-Specific Forms

| Context            | Form     | Example                              |
| ------------------ | -------- | ------------------------------------ |
| **Marketing copy** | TraceKit | "TraceKit provides..."               |
| **Documentation**  | TraceKit | "Using TraceKit, you can..."         |
| **Package names**  | tracekit | `uv pip install tracekit`            |
| **Python imports** | tracekit | `import tracekit as tk`              |
| **CLI commands**   | tracekit | `tracekit characterize input.wfm`    |
| **File names**     | tracekit | `tracekit-guide.md`                  |
| **URLs**           | tracekit | `github.com/lair-click-bats/tracekit |

---

## Tagline

**Digital Waveform and Protocol Reverse Engineering Toolkit**

Use this tagline consistently in documentation headers and project descriptions.

### Short Description

"Signal analysis framework for oscilloscope and logic analyzer data"

Use for:

- PyPI package description
- GitHub repository description
- Social media summaries

---

## Preferred Terminology

| Use This                  | Not This                                |
| ------------------------- | --------------------------------------- |
| TraceKit                  | Trace Kit, trace-kit, TK                |
| waveform analysis         | trace analysis, signal processing       |
| oscilloscope data         | scope data, o-scope data                |
| logic analyzer            | LA, logic probe                         |
| protocol decoder          | protocol parser, bus decoder            |
| reverse engineering       | RE, reversing                           |
| signal integrity analysis | SI analysis                             |
| eye diagram               | eye pattern                             |
| measurement               | metric, calculation                     |
| trace (noun)              | waveform, signal (context-dependent)    |
| IEEE-compliant            | standards-compliant, IEEE-compatible    |
| load a waveform           | import a trace, read a file             |
| export to CSV             | save as CSV, write CSV                  |
| characterize              | analyze, profile                        |
| unknown signal            | unidentified signal, mystery signal     |
| fuzzy matching            | approximate matching, pattern tolerance |

---

## Domain-Specific Language

Use standard terminology for each domain:

### Oscilloscope/Waveform Analysis

- Rise time, fall time, overshoot, undershoot
- Frequency, period, duty cycle, pulse width
- Amplitude, RMS, peak-to-peak
- Trigger level, threshold, hysteresis

### Digital Signal Processing

- Edge detection, clock recovery, baud rate
- Correlation, convolution, filtering
- FFT, PSD, spectrogram
- THD, SNR, SINAD, ENOB

### Protocol Analysis

- UART, SPI, I2C, CAN, CAN-FD, 1-Wire
- Baud rate, bit rate, frame, packet
- Start bit, stop bit, parity, checksum
- Address, data, acknowledge, arbitration

### Signal Integrity

- Eye diagram, eye opening, eye height
- Jitter (TIE, period, cycle-to-cycle)
- BER, bathtub curve, Q-factor
- S-parameters, de-embedding, equalization

### File Formats

- Tektronix WFM/ISF, Rigol, LeCroy
- Sigrok session, VCD, PCAP
- TDMS, WAV, CSV, HDF5, NPZ

---

## Tone Guidelines

### Documentation

- **Style**: Clear, technical, example-driven
- **Focus**: Explain measurement theory and practical application
- **Examples**: Every function has code example and expected output
- **Assumption**: Reader is electrical engineer or embedded developer

### Community (GitHub, Issues)

- **Style**: Professional, collaborative, helpful
- **Focus**: Debug issues, explain limitations, guide solutions
- **Celebrate**: Contributions, new decoders, test improvements

### Announcements

- **Style**: Technical and precise
- **Focus**: New capabilities, standards compliance, performance improvements
- **Examples**: Concrete measurements over vague claims
- **Voice**: Engineering confidence

---

## Code Examples

### Formatting

- Use proper indentation (4 spaces)
- Include imports at top
- Add comments for context
- Show expected output when helpful
- Use realistic signal names

### Good Example

```python
import tracekit as tk

# Load oscilloscope capture
trace = tk.load("clock_signal.wfm")

# Measure rise time (IEEE 181 compliant)
rise = tk.rise_time(trace)
print(f"Rise time: {rise:.2e} s")  # Expected: 2.5e-9 s

# Detect edges with hysteresis
edges = tk.find_edges(trace, low=0.8, high=2.0)
print(f"Found {len(edges)} edges")
```

### Bad Example

```python
# Missing imports, unclear purpose, no context
trace = load("data.wfm")
result = process(trace)
```

---

## Technical Terms

**First use:** Define it clearly
**Subsequent:** Use directly
**Avoid:** Excessive jargon without context

Examples:

- **Good**: "TraceKit performs rise time measurements following IEEE 181 (10%-90% transition time)..."
- **Bad**: "TraceKit leverages advanced DSP paradigms to facilitate waveform characterization workflows..."

---

## File Naming

### Root Documentation

- `README.md` (not readme.md)
- `CONTRIBUTING.md`
- `CHANGELOG.md`
- `LICENSE` (no extension)
- `SECURITY.md`
- `CLAUDE.md`

### docs/ Documentation

- `docs/contributing/branding.md` (this file)
- `docs/reference/import-paths.md`
- `docs/testing/index.md`

### Code

- `tracekit/` (directory)
- `loaders/` (not Loaders/)
- `analyzers/` (not Analyzers/)
- `test_loaders.py` (test files)

### Examples

- `example_uart_decode.py` (underscored)
- `tutorial-1-loading-waveforms.md` (hyphenated)
- `clock_recovery.py`

---

## Version Naming

Format: `MAJOR.MINOR.PATCH[-PRERELEASE]`

Examples:

- `0.1.0` (initial release)
- `1.0.0` (stable release)
- `1.1.0` (minor feature release)
- `1.0.1` (bugfix patch)
- `2.0.0-alpha.1` (alpha prerelease)

**No code names** - use version numbers only

### Version Strategy

- **MAJOR**: Breaking API changes, major architectural changes
- **MINOR**: New decoders, new measurements, backward-compatible features
- **PATCH**: Bug fixes, documentation improvements, minor optimizations

---

## Error Codes

TraceKit uses structured error codes: `TK-MODULE-###`

Format:

- `TK-`: Prefix for all TraceKit errors
- `MODULE`: Three-letter module code (FILE, MEAS, PROT, etc.)
- `###`: Three-digit error number

Examples:

- `TK-FILE-101`: File not found
- `TK-MEAS-201`: Insufficient data for measurement
- `TK-PROT-301`: Invalid baud rate

See `docs/error-codes.md` for complete reference.

---

## Standards References

When mentioning standards compliance:

- **Full citation first**: "IEEE 181 (Standard for Transitions, Pulses, and Related Waveforms)"
- **Subsequent**: "IEEE 181" or "per IEEE 181"
- **Link when available**: Include DOI or IEEE Xplore link

Examples:

- IEEE 181 (Transition Measurements)
- IEEE 1057 (Digitizing Waveform Recorders)
- IEEE 1241 (ADC Terminology and Testing)
- IEEE 2414 (Jitter and Jitter Testing)
- JEDEC JESD65C (Eye Diagram Measurements)

---

## Legal

### Copyright Notice

```
Copyright (c) 2025-2026 lair-click-bats
Licensed under the MIT License
```

### Disclaimer

> TraceKit provides measurement and analysis tools based on industry standards. Users are responsible for validating measurements for their specific equipment and use case. TraceKit is not certified for safety-critical applications.

---

## Comparison Language

When comparing to other tools:

- **Be factual**: State capabilities, not superiority
- **Be specific**: "Python-native scripting" not "better automation"
- **Be respectful**: "Different approach" not "inferior design"

**Good:**

- "vs sigrok/PulseView: Python-native (scriptable, automatable)"
- "vs MATLAB: Open-source, no licensing costs"

**Bad:**

- "Better than sigrok because..."
- "More powerful than MATLAB..."

---

## Updates

This document is reviewed:

- **Major releases**: Update examples, version numbers
- **Quarterly**: Ensure consistency with actual usage
- **On feedback**: Incorporate community suggestions

**Owner**: Project maintainer
**Contributors**: Open to community input via GitHub issues

---

**Document Version:** 1.0
**Status:** Official - All project materials should follow these guidelines
