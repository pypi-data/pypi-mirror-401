# Changelog

All notable changes to TraceKit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.1] - 2026-01-13

### Added

#### Comprehensive Local CI Verification System

- **Pre-Push Verification Script** (`scripts/pre-push.sh`):
  - Mirrors GitHub Actions CI pipeline for local verification
  - Stage 1: Fast checks (pre-commit, ruff lint/format, mypy, config validation)
  - Stage 2: Tests (unit, integration, compliance)
  - Stage 3: Build verification (MkDocs, package build, CLI, docstrings)
  - Modes: `--full` (complete CI, ~10-15m), `--quick` (~2m), `--no-tests` (~3m)
  - Auto-fix mode: `--fix` to auto-correct issues before verification
  - Colored output with detailed failure reporting

- **Git Pre-Push Hook** (`scripts/hooks/pre-push`):
  - Automatic CI verification before push
  - Full verification for protected branches (main, develop)
  - Quick verification for feature branches
  - Blocks push on verification failure
  - Bypass: `git push --no-verify` (use sparingly)

- **Git Hooks Setup Script** (`scripts/setup-git-hooks.sh`):
  - Easy installation: `./scripts/setup-git-hooks.sh`
  - Status check: `./scripts/setup-git-hooks.sh --status`
  - Uninstall: `./scripts/setup-git-hooks.sh --uninstall`

- **Quick Development Verification** (`scripts/verify.sh`):
  - Fast lint/format check for development iterations (~30s)
  - Auto-fix mode: `--fix`
  - Optional test inclusion: `--test`

### Changed

#### Branding and Positioning Updates

- **README.md**: Comprehensive analog + digital signal positioning
  - Updated tagline: "The open-source toolkit for reverse engineering ANY system from captured waveforms—analog or digital"
  - Added analog use cases: audio amplifiers (THD/SNR), power supplies (ripple/efficiency), RF baseband
  - Reorganized Key Capabilities into Analog, Digital, Automotive, and Compliance sections
  - Updated "Why TraceKit?" table with analog examples
  - Updated citation: "Analog and Digital Signal Reverse Engineering Toolkit"

- **pyproject.toml**: Updated description to reflect analog and digital breadth
  - Mentions audio (THD/SNR), power (ripple/efficiency), RF, sensors alongside IoT protocols
  - IEEE standards compliance (181/1241/1459/2414)

- **docs/index.md**: Updated to v0.3.1 with comprehensive scope
  - Version updated to 0.3.1
  - Last updated: 2026-01-13
  - Added analog analysis capabilities alongside digital
  - Automotive section highlighted

- **CLAUDE.md**: Restored full vision statement
  - Complete positioning: analog or digital, simple or complex
  - Detailed use cases and target users

- **project-metadata.yaml**: Updated SSOT description
  - Aligned with comprehensive positioning

- **CONTRIBUTING.md**: Updated with comprehensive verification workflow
  - Git hooks setup instructions
  - Recommended development workflow
  - Verification script comparison table
  - Troubleshooting CI failures guide

### Fixed

- **Test Marker Format** (`tests/unit/inference/test_crc_reverse.py`):
  - Fixed pytestmark to use list format: `[pytest.mark.unit]`
  - Resolves CI quality gate failure

### Infrastructure

- New `scripts/hooks/` directory for custom git hooks
- Pre-push hook mirrors CI to prevent remote failures

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
  - **Anomaly Detection** (`can.anomaly`): Multi-model detection with explainability
  - **Attack Synthesis** (`can.injection`): Safety-bounded fuzzing and replay attacks
  - Comprehensive test suite with 150+ tests
  - Example: `examples/automotive/can_reverse_engineering.py`

#### Streaming Analysis

- **Streaming Correlation Detection** (`src/tracekit/streaming/`):
  - Real-time cross-correlation with adaptive thresholds
  - Periodic pattern detection without full trace storage
  - Memory-efficient sliding window processing
  - Comprehensive test suite: 50+ tests passing

#### Search Capabilities

- **Pattern Search Engine** (`src/tracekit/search/`):
  - Pattern search across multiple traces
  - Boolean query combining (AND, OR, NOT)
  - Time-range filtering
  - Result ranking and scoring

### Changed

- **Documentation Overhaul**:
  - Added comprehensive API reference documentation
  - Updated Getting Started guide with new examples
  - Added Troubleshooting section

### Fixed

- Various bug fixes in protocol decoders
- Memory optimization in large trace handling
- Edge case fixes in IEEE measurement functions

## [0.2.0] - 2025-12-15

### Added

- Protocol decoder framework with UART, SPI, I2C support
- IEEE 181-2011 compliant pulse measurements
- Spectral analysis with FFT, THD, SNR calculations
- Basic trace visualization

### Changed

- Improved loader error messages
- Enhanced type hints throughout codebase

## [0.1.0] - 2025-11-01

### Added

- Initial release
- Core Signal and Trace data types
- VCD file loader
- Basic time-domain measurements
- CLI interface foundation
