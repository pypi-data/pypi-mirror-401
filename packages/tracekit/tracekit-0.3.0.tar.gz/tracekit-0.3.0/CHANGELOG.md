# Changelog

All notable changes to TraceKit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2026-01-13

### Added

#### Examples Restructuring and Expansion

- **New Example Sections** (`examples/`):
  - `05_filtering/`: Complete signal filtering examples
    - `01_low_pass.py`: Low-pass filtering for noise removal
    - `02_high_pass.py`: High-pass filtering and DC removal
    - `03_band_filters.py`: Band-pass, band-stop, and notch filters
  - `07_math/`: Mathematical operations on traces
    - `01_arithmetic.py`: Add, subtract, multiply, divide traces
    - `02_calculus.py`: Differentiate and integrate for slew rate and energy
  - `08_triggering/`: Event detection and triggering
    - `01_edge_trigger.py`: Rising/falling edge detection with timing analysis
  - `09_power/`: Power analysis capabilities
    - `01_basic_power.py`: Instantaneous, average power and energy calculations
  - `11_comparison/`: Trace comparison and limit testing
    - `01_compare_traces.py`: Correlation, similarity, difference analysis
  - `14_session/`: Session management
    - `01_basic_session.py`: Creating, saving, and loading analysis sessions
  - Comprehensive README.md files for each new section
  - Test count: All examples executable without errors

- **Examples Audit Report** (`.claude/reports/examples-audit-report.md`):
  - Complete API surface mapping (200+ functions)
  - Coverage gap analysis identifying 35% missing coverage
  - Redundancy identification (5 duplicate examples)
  - Recommended restructuring plan

#### Testing Utilities

- **Signal Generator Functions** (`src/tracekit/testing/synthetic.py`):
  - `generate_sine_wave()`: Create sine wave WaveformTrace with configurable frequency, amplitude, sample rate, duration, offset, phase, and noise level
  - `generate_square_wave()`: Create square wave with configurable duty cycle, logic levels
  - `generate_dc()`: Create DC (constant) signal for testing edge cases
  - `generate_multi_tone()`: Create sum of multiple sine waves for spectral analysis testing
  - `generate_pulse()`: Create single pulse with configurable rise/fall times and overshoot
  - All functions return `WaveformTrace` objects ready for analysis
  - Example: `examples/01_basics/02_basic_measurements.py`

#### Protocol Reverse Engineering Suite

- **CRC Polynomial Reverse Engineering** (`src/tracekit/inference/crc_reverse.py`):
  - XOR differential technique (Greg Ewing method) for polynomial recovery
  - Automatic reflection detection (refin/refout) for reflected CRCs
  - Support for CRC-8, CRC-16, CRC-32, and CRC-64 with common polynomials
  - Handles both same-length and variable-length message sets
  - `CRCReverser` class with `reverse()` method returning `CRCParameters`
  - Comprehensive test suite: 20/20 tests passing

- **L\* Active Learning Algorithm** (`src/tracekit/inference/active_learning/`):
  - Angluin's L\* algorithm for DFA (Deterministic Finite Automaton) learning
  - `ObservationTable` implementation with closure and consistency checking
  - `Oracle` interface for membership and equivalence queries
  - `SimulatorTeacher` for protocol learning from traffic traces
  - Automatic protocol state machine inference from network captures
  - Comprehensive test suite: 27/27 tests passing
  - Example: `examples/lstar_demo.py`

- **Wireshark Lua Dissector Export** (`src/tracekit/export/wireshark/`):
  - Automatic Wireshark dissector generation from protocol definitions
  - Support for TCP/UDP port registration
  - Variable-length field handling with size field references
  - Enum value mapping for decoded field display
  - Big/little endian support
  - Lua syntax validation with `luac` (when available)
  - Generated dissectors compatible with Wireshark 3.x+
  - Comprehensive test suite: 34/34 tests passing (with luac installed)
  - Example: `examples/05_export/wireshark_dissector_example.py`

- **Enhanced Field Boundary Detection** (`src/tracekit/inference/message_format.py`):
  - Voting expert ensemble with 5 detection strategies:
    - Entropy-based boundary detection
    - Smith-Waterman sequence alignment
    - Statistical variance analysis
    - Byte distribution change detection
    - N-gram frequency analysis
  - IPART-style confidence scoring for field boundaries
  - `detect_boundaries_voting()` method with configurable thresholds
  - `infer_format_ensemble()` for complete message format inference
  - Comprehensive test suite: 100/100 tests passing
  - Example: `examples/ensemble_inference_example.py`

#### Automotive CAN Bus Analysis Suite

- **Complete CAN Bus Reverse Engineering** (`src/tracekit/automotive/`):
  - **File Loaders** (4 formats): BLF (Vector), ASC (Vector), MDF (ASAM), CSV
  - **Discovery API** (`can.discovery`): Automatic message/signal discovery with confidence scoring
  - **State Machine Inference** (`can.state_machine`): RPNI algorithm with hypothesis testing
  - **Pattern Learning** (`can.patterns`): Counter, sequence, toggle detection with 95%+ confidence
  - **Stimulus-Response Analysis** (`can.stimulus_response`): Multi-hop causality, temporal correlation
  - **Checksum Detection** (`can.checksum`): XOR, SUM, CRC-8/16/32 reverse engineering
  - **OBD-II Decoder** (`obd.decoder`): 54 PIDs (Mode 01), freeze frame support
  - **J1939 Decoder** (`j1939.decoder`): 154 PGNs with SPN extraction
  - **UDS Decoder** (`uds.decoder`): 17 diagnostic services (ISO 14229)
  - **DTC Database** (`dtc.database`): 210 diagnostic trouble codes (SAE J2012)
  - **DBC Parser/Generator** (`dbc.parser`, `dbc.generator`): Import/export industry standard format
  - **Session Management** (`can.session`): Save/restore .tkcan format with annotations
  - **Signal Correlation** (`can.correlation`): Cross-message relationship discovery
  - Test count: 485/485 passing
  - Standards: SAE J1979, J1939, ISO 14229, SAE J2012
  - Examples: `examples/automotive/` (5 examples)

### Changed

- **Examples Main README** (`examples/README.md`):
  - Updated to reflect new 12-section structure
  - Added API coverage matrix showing ~95% coverage
  - Expanded estimated time table
  - Added filtering and session sections to quick start

### Fixed

#### Documentation API Consistency

- **Examples Fixed** (`examples/`):
  - `01_basics/02_basic_measurements.py`: Updated to use `tk.frequency()`, `tk.basic_stats()`, `tk.find_rising_edges()` instead of non-existent method calls
  - `02_digital_analysis/01_edge_detection.py`: Fixed to use `tk.find_rising_edges()`, `tk.find_falling_edges()` with correct parameters (`level`, `hysteresis`)
  - `03_spectral_analysis/01_fft_basics.py`: Fixed to use `tk.fft()` returning tuple `(frequencies, magnitudes_db)` instead of non-existent `compute_fft()`
  - `03_spectral_analysis/02_signal_quality.py`: Fixed to use `tk.snr()`, `tk.thd()`, `tk.sinad()`, `tk.enob()`, `tk.sfdr()` instead of non-existent `measure_*()` functions

- **Tutorial Corrections** (`docs/tutorials/02-basic-measurements.md`):
  - Changed all method-style API calls to function-style: `trace.frequency()` -> `tk.frequency(trace)`
  - Updated `analyze_amplitude()` to use `tk.basic_stats()` which returns dict with keys `min`, `max`, `mean`, `range`, `std`
  - Fixed rise_time parameter from `low=0.2, high=0.8` to `ref_levels=(0.2, 0.8)` (tuple of 2 floats)
  - Fixed edge detection to use `tk.find_rising_edges()` and `tk.find_falling_edges()`
  - Added examples using `tracekit.testing` signal generators

- **Getting Started Guide** (`docs/getting-started.md`):
  - Updated version references to 0.2.0
  - Clarified FFT return value is tuple `(frequencies, magnitudes_db)`
  - Fixed CLI verification command

#### CI Workflow Optimization

- **CI Workflow Optimization** (`.github/workflows/ci.yml`):
  - **Performance**: Eliminated redundant test execution in diff-coverage job
    - Test jobs now upload .coverage database files as artifacts
    - Diff-coverage merges existing coverage instead of re-running 17,000+ tests
    - Reduces diff-coverage time from 15+ minutes to ~2 minutes (87% faster)
  - **Permissions**: Added `pull-requests: write` to diff-coverage job
    - Fixes "Resource not accessible by integration" error when posting coverage comments
  - **Artifact Upload**: Added `include-hidden-files: true` to upload-artifact action
    - Ensures .coverage files (hidden files starting with dot) are uploaded
    - Fixes "No coverage files found!" error in diff-coverage merge step
  - **Reliability**: Adjusted timeout to 10 minutes (sufficient for merge-only workflow)
  - Maintains minimal read-only permissions for all other jobs

### Infrastructure

- **CI/CD**: All workflows passing on main branch with zero errors
- **Test Coverage**: 17,313 tests, 99%+ passing rate
- **Dependencies**: Added `luac` (Lua 5.3) for Wireshark dissector validation
- **Examples Coverage**: Improved from 35% to ~95% API coverage

## [0.1.1] - 2026-01-10

### Added

#### Code Quality Infrastructure

- **Documentation Coverage Tool** (`interrogate`): Automated docstring coverage tracking with 98% threshold
  - Enforced in pre-commit hooks and CI/CD pipeline
  - Badge generation for documentation site
  - Baseline: 98.3% coverage achieved

- **Code Quality Tools**:
  - `pydocstyle`: Google-style docstring validation
  - `vulture`: Dead code detection (min confidence 80%)
  - `radon`: Cyclomatic complexity and maintainability index analysis
  - `darglint`: Docstring argument validation
  - `linkchecker`: Documentation link validation

- **Pre-commit Hook Framework**: Local quality enforcement before commits
  - Automated code formatting (ruff)
  - Linting with auto-fix capabilities
  - Docstring coverage validation
  - YAML, JSON, TOML syntax validation
  - Markdown linting with markdownlint
  - Shell script validation with shellcheck
  - Secret detection
  - Comprehensive documentation in `docs/development/pre-commit-setup.md`

- **CI/CD Quality Gates** (`.github/workflows/code-quality.yml`):
  - Docstring coverage check (required, blocks merges)
  - Docstring style analysis (informational)
  - Dead code detection (informational)
  - Complexity analysis (informational)
  - Badge artifact generation

- **Documentation**:
  - Pre-commit hooks setup guide
  - Documentation maintenance best practices guide
  - Quality metrics tracking

### Changed

- **PyPI Metadata**: Enhanced project discoverability with comprehensive keywords and classifiers
  - Added 30+ relevant keywords (oscilloscope, protocol-analysis, signal-processing, etc.)
  - Complete classifier set for Python versions, license, audience, and topics

### Fixed

- **Dead Code Removal**: Cleaned up 32 unused items identified by vulture analysis
  - Removed 13 unused parameters across multiple modules
  - Added Python 3.11+ compatibility comments for required exception handler parameters
  - Improved code maintainability without breaking backward compatibility
  - Files affected: `jupyter/display.py`, `comparison/mask.py`, `core/logging.py`, `exploratory/legacy.py`, `inference/bayesian.py`, `inference/signal_intelligence.py`, `loaders/vcd.py`, `reporting/comparison.py`, `ui/formatters.py`, `visualization/eye.py`, `visualization/interactive.py`, `visualization/spectral.py`, and various memory management modules

- **CI/CD**: Fixed `docs/badges` directory structure (was accidentally a file instead of directory)

### Infrastructure

- **Quality Baseline Established**:
  - Docstring coverage: 98.3% (PASSING)
  - Docstring style: 283 violations (informational)
  - Dead code: 32 items (cleaned up)
  - High complexity: 355 functions (monitored)
  - Critical files: 2 (tracked for refactoring)

- **Two-Tier Quality System**:
  - Local: Pre-commit hooks for instant feedback
  - Remote: GitHub Actions for comprehensive validation
  - Only docstring coverage blocks builds; other metrics are informational

## [0.1.0] - 2026-01-07

### Added

#### Core Framework

- **Data Types**: Unified signal representation with `TraceData`, `WaveformTrace`, and `DigitalTrace`
- **Configuration System**: YAML-based configuration with JSON Schema validation
- **Exception Hierarchy**: Comprehensive error types with clear error codes (TK-XXX-###)
- **CLI**: Command-line interface with `characterize`, `decode`, `compare`, and `batch` commands
- **Session Management**: Save and restore analysis sessions with annotations

#### Loaders

Support for multiple waveform and packet capture formats:

- **Tektronix WFM**: Native oscilloscope file format
- **PCAP/PCAPNG**: Network packet captures
- **Sigrok**: Logic analyzer sessions (605+ device types)
- **Configurable Binary**: Schema-driven custom packet formats
- **Standard Formats**: NumPy arrays, CSV, HDF5, WAV, VCD

#### Analyzers

**Waveform Measurements**

- Rise/fall time (IEEE 181 compliant)
- Frequency, period, and duty cycle
- Amplitude, overshoot, and undershoot
- Pulse width analysis

**Digital Signal Processing**

- Edge detection with configurable hysteresis
- Clock recovery and baud rate detection
- Multi-channel correlation
- Parallel bus decoding

**Spectral Analysis**

- FFT with multiple windowing functions
- Power Spectral Density (PSD)
- THD, SNR, SINAD, ENOB (IEEE 1241 compliant)
- Memory-efficient chunked processing

**Protocol Decoders**

- **Serial**: UART, SPI, I2C, 1-Wire, Manchester
- **Automotive**: CAN/CAN-FD, LIN, FlexRay
- **Debug**: JTAG, SWD
- **Audio**: I2S
- **Other**: HDLC, USB
- Auto-detection and configuration

**Statistical Analysis**

- Shannon entropy and byte distribution
- N-gram frequency analysis
- Checksum detection (CRC-8/16/32, XOR, modular sum)
- Data classification and correlation

**Pattern Analysis**

- Periodic signal detection
- Motif discovery
- Anomaly detection
- Pattern clustering

**Protocol Inference**

- Message format inference with field boundary detection
- State machine inference (RPNI algorithm)
- Sequence alignment (Needleman-Wunsch, Smith-Waterman)
- Protocol DSL for custom decoders

#### Signal Integrity

- Eye diagram generation and analysis
- Jitter measurements (TIE, period, cycle-to-cycle)
- Jitter decomposition (RJ, DJ, DDJ, PJ)
- BER estimation and bathtub curves
- S-parameter analysis
- Channel equalization (FFE, DFE)

#### Power Analysis

- AC/DC power measurements
- Switching loss analysis
- Safe Operating Area (SOA) validation
- Efficiency calculations
- Ripple measurement

#### Comparison and Compliance

- Golden waveform comparison
- Mask testing (IEEE 2414)
- Limit testing with pass/fail criteria
- Trace differencing

#### Visualization and Export

- Multi-channel waveform plotting
- Eye diagrams and jitter histograms
- Protocol decode annotations
- PDF report generation
- PowerPoint export
- CSV/JSON/HDF5 export
- Interactive HTML (Plotly, Bokeh)

### Standards Compliance

- IEEE 181 (Transition Measurements)
- IEEE 1057 (Digitizing Waveform Recorders)
- IEEE 1241 (ADC Terminology and Testing)
- IEEE 2414 (Jitter Testing)
- JEDEC JESD65C (Eye Diagrams)

### Infrastructure

- Python 3.12+ with full type hints
- mypy strict mode
- Comprehensive test suite (16,000+ tests)
- GitHub Actions CI/CD
- Documentation and tutorials

---

[Unreleased]: https://github.com/lair-click-bats/tracekit/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/lair-click-bats/tracekit/compare/v0.1.1...v0.3.0
[0.1.1]: https://github.com/lair-click-bats/tracekit/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/lair-click-bats/tracekit/releases/tag/v0.1.0
