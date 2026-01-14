# TraceKit - AI Project Context

**Project**: Digital waveform and protocol analysis toolkit
**Python**: 3.12+
**Key Tech**: numpy, pytest, ruff, uv, hypothesis

---

## What is TraceKit

TraceKit is the open-source toolkit for reverse engineering ANY system from captured waveforms—analog or digital, simple or complex. Four core capabilities: (1) signal characterization (waveform, spectral, power analysis), (2) behavior inference (circuits, protocols, patterns), (3) protocol reverse engineering (decode + infer), (4) compliance validation (IEEE, EMC, power quality).

**Analog**: Audio amplifiers (THD, SNR), power supplies (ripple, efficiency), RF baseband (spectral analysis), sensors, control systems, EMC compliance
**Digital**: Logic circuits (state machines, patterns), IoT protocols (UART, SPI, I2C, CAN + 16 more), timing analysis, protocol inference
**Both**: Spectral analysis, signal integrity, IEEE-compliant measurements (181, 1241, 1459, 2414), mixed-signal validation

**Core capabilities**: Signal characterization, spectral analysis (FFT, THD, SNR), power analysis (AC/DC, efficiency, ripple), protocol analysis (16+ transport decoders + message inference), CRC reverse engineering, state machine learning, timing correlation, Wireshark dissector generation, IEEE compliance validation.

**Primary use cases**: Analog circuit analysis (audio, power, RF baseband, sensors), digital circuit reverse engineering, protocol reverse engineering (transport + message), hardware security research, embedded debugging, signal integrity validation, EMC compliance testing, mixed-signal validation.

**Target users**: Hardware reverse engineers, audio engineers, power electronics engineers, RF engineers, security researchers, embedded engineers, test & validation engineers, vintage computing enthusiasts, automotive security specialists, IoT researchers, academic researchers.

---

## Essential Project Knowledge

### Project Structure

```
src/tracekit/          # Source code (loader, analyzers, protocols, etc.)
tests/                 # Test suite (unit, integration, compliance)
docs/                  # User-facing documentation
examples/              # Working code examples
scripts/               # Development utilities
.claude/               # Claude configuration and agents
```

### Core Abstractions

- **Signal**: Time-series container with channels, sample rate, metadata
- **Loader**: Parse file formats → Signal objects
- **Analyzer**: Signal → Measurements (dict of named values)
- **Protocol Decoder**: Signal → Frame objects (decoded data)

**Pattern**: Inherit from base classes, implement required methods. See existing implementations for patterns.

### Where Things Live

| Need               | Look Here                                                  |
| ------------------ | ---------------------------------------------------------- |
| Add loader         | `src/tracekit/loaders/` + pattern from vcd.py              |
| Add analyzer       | `src/tracekit/analyzers/` + tests                          |
| Add protocol       | `src/tracekit/analyzers/protocols/` + pattern from uart.py |
| Usage examples     | `examples/` (organized by category)                        |
| User documentation | `docs/` (getting-started, guides, API ref)                 |
| Testing strategy   | `docs/testing/index.md`                                    |
| Coding standards   | `.claude/coding-standards.yaml` (SSOT)                     |

---

## Development Workflow

### 1. Setup

```bash
uv sync                           # Install dependencies
uv run pytest tests/unit -x      # Verify installation
```

### 2. Make Changes

- Read existing code for patterns before adding new features
- Use fixtures from `tests/conftest.py` for synthetic test data
- Keep test files <100KB (use synthetic data only)
- Follow IEEE standards where applicable (see table below)

### 3. Quality Checks

```bash
uv run ruff check src/ tests/     # Lint
uv run ruff format src/ tests/    # Format
uv run mypy src/                  # Type check
pytest tests/unit -v              # Test
```

Or use: `scripts/check.sh` (runs all checks)

### 4. Commit

- Use [conventional commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `refactor:`, etc.
- **MUST update CHANGELOG.md** under `[Unreleased]` (see protocol below)
- Pre-commit hooks run automatically (lint, format, type check)

### 5. Create PR

- Follow template in `.github/PULL_REQUEST_TEMPLATE.md`
- All CI checks must pass (tests, lint, docs, coverage)
- See `CONTRIBUTING.md` for full PR workflow

---

## Changelog and Versioning Protocol

**CRITICAL**: Follow this for ALL development work.

### Version Management

- **Current version**: Check `pyproject.toml` [project.version]
- **Scheme**: Semantic Versioning (MAJOR.MINOR.PATCH)
  - MAJOR: Breaking API changes
  - MINOR: New features (backward compatible)
  - PATCH: Bug fixes only
- **DO NOT bump version per PR** - accumulate in [Unreleased]
- **Bump only when releasing** (separate commit + git tag)

### CHANGELOG.md Update (Required)

Every PR must update CHANGELOG.md under `## [Unreleased]`:

**Sections**: Added | Changed | Fixed | Removed | Infrastructure

**Entry format**:

```markdown
- **Feature Name** (`path/to/file.py`):
  - Brief description of what it does
  - Key capabilities (bullets if needed)
  - Test count: X/X passing
  - Example: `examples/category/example.py` (if applicable)
```

**Document**: New features, API changes, bug fixes, CI/CD changes
**Skip**: Minor refactoring, comments, test-only changes

**Release process**:

1. Rename `[Unreleased]` → `[X.Y.Z] - YYYY-MM-DD`
2. Bump version in `pyproject.toml`
3. Create git tag `vX.Y.Z`
4. Push tag (triggers release workflow)

---

## Standards and Conventions

### IEEE Standards Compliance

| Standard       | Scope                      | Examples                  |
| -------------- | -------------------------- | ------------------------- |
| IEEE 181-2011  | Pulse measurements         | Rise/fall time, slew rate |
| IEEE 1057-2017 | Digitizer characterization | Timing analysis           |
| IEEE 1241-2010 | ADC testing                | SNR, SINAD, ENOB          |
| IEEE 2414-2020 | Jitter measurements        | TIE, period jitter        |

Document standard compliance in docstrings.

### Naming Conventions

- Files/modules: `snake_case.py`
- Classes: `PascalCase`
- Functions: `snake_case()`
- Constants: `SCREAMING_SNAKE_CASE`
- Private: `_leading_underscore()`
- Tests: `test_<module>.py` / `test_<functionality>_<condition>_<expected>()`

### Test Data

- Use synthetic data only (not vendor captures)
- Generate with `scripts/generate_comprehensive_test_data.py`
- Store in `test_data/synthetic/`
- Keep files <100KB

---

## Reference Hierarchy

**Check in this order**:

1. **CLAUDE.md** (this file) - How to work in the repo
2. `.claude/coding-standards.yaml` - Style rules (SSOT)
3. `CONTRIBUTING.md` - Git workflow, PR process
4. `docs/testing/index.md` - Testing strategy
5. `examples/` - Working code examples
6. Existing code - Examine similar implementations

### Key Files

- `pyproject.toml` - Dependencies, build config, version
- `.claude/project-metadata.yaml` - Project identity (SSOT)
- `.claude/orchestration-config.yaml` - Agent behavior
- `.pre-commit-config.yaml` - Pre-commit hooks
- `CHANGELOG.md` - Version history (Keep a Changelog format)

---

## Quick Lookups

| Task                 | Action                                           |
| -------------------- | ------------------------------------------------ |
| Add file format      | Check `src/tracekit/loaders/vcd.py`              |
| Add analyzer         | Check `examples/03_analysis/`                    |
| Add protocol decoder | Check `src/tracekit/analyzers/protocols/uart.py` |
| Write tests          | Use fixtures from `tests/conftest.py`            |
| Check code style     | See `.claude/coding-standards.yaml`              |
| Commit format        | See `CONTRIBUTING.md`                            |
| Update CHANGELOG     | See "Changelog Protocol" section above           |
| Run quality checks   | Run `scripts/check.sh`                           |

---

## Performance Notes

- Files >100MB: Use chunked reading
- Signals >10M samples: Consider downsampling
- Prefer numpy vectorized operations over loops
- Memory-mapped loading available for large files

---

## Error Handling

- Validate at API boundaries (user-facing functions)
- Raise descriptive errors with context
- Trust internal code (no defensive checks between internals)

---

## Additional Resources

- **User docs**: `docs/` (getting-started, guides, tutorials, API reference)
- **Examples**: `examples/` (organized by feature area)
- **Testing**: `docs/testing/index.md`
- **Development**: `CONTRIBUTING.md`
- **Issues/PRs**: [GitHub repository](https://github.com/lair-click-bats/tracekit)

When uncertain about implementation, **examine existing similar code** in `src/tracekit/` for established patterns.
