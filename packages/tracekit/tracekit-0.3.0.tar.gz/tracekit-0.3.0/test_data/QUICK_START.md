# Synthetic Test Data - Quick Start

## TL;DR

```bash
# Generate all test files (29 files, 2.5 MB)
python scripts/generate_synthetic_wfm.py --generate-suite

# Generate custom signal
python scripts/generate_synthetic_wfm.py --signal sine --frequency 10000 --output test.wfm

# Verify system
python scripts/verify_synthetic_test_data.py

# Use in code
from tracekit.loaders.tektronix import load_tektronix_wfm
trace = load_tektronix_wfm("test_data/waveforms/synthetic/basic/sine_1khz.wfm")
```

## What You Get

**29 test files** (2.5 MB) covering:

- Basic signals (sine, square, triangle, sawtooth, pulse)
- Edge cases (DC, noise, extreme values)
- Size variations (100 to 1M samples)
- Frequency variations (10 Hz to 100 kHz)
- Advanced signals (chirp, PWM, damped, etc.)

## Why Use This?

✓ **Legally safe** - No proprietary data
✓ **Reproducible** - Same every time
✓ **Fast** - Small files, quick generation
✓ **Comprehensive** - All test scenarios covered
✓ **Version controlled** - Commit to git

## Common Commands

### Generate Test Suite

```bash
python scripts/generate_synthetic_wfm.py --generate-suite
```

### Generate Specific Signals

```bash
# 1 kHz sine
python scripts/generate_synthetic_wfm.py --signal sine --frequency 1000 --output sine.wfm

# Square wave with noise
python scripts/generate_synthetic_wfm.py --signal square --snr 30 --output noisy.wfm

# Large file (1M samples)
python scripts/generate_synthetic_wfm.py --signal sine --samples 1000000 --output large.wfm
```

### Verify Installation

```bash
python scripts/verify_synthetic_test_data.py
```

## File Locations

```
test_data/waveforms/synthetic/
├── basic/              # 5 standard waveforms
├── edge_cases/         # 8 edge cases
├── sizes/              # 4 size variations
├── frequencies/        # 5 frequency tests
└── advanced/           # 7 advanced signals
```

## Available Signal Types

- `sine` - Pure sinusoid
- `square` - Square wave
- `triangle` - Triangle wave
- `sawtooth` - Sawtooth wave
- `pulse` - Pulse train (configurable duty cycle)
- `dc` - Constant voltage
- `noisy` - White noise
- `mixed` - Multiple harmonics
- `chirp` - Frequency sweep
- `pwm` - Pulse width modulation
- `exponential` - Exponential decay
- `damped_sine` - Damped oscillation

## Parameters

```bash
--frequency HZ          Signal frequency (default: 1000)
--amplitude V           Signal amplitude (default: 1.0)
--sample-rate SA/S      Sample rate (default: 1e6)
--samples N             Number of samples
--duty-cycle RATIO      Pulse duty cycle (default: 0.5)
--snr DB                Add noise with specified SNR
--offset V              DC offset (default: 0.0)
```

## Help

```bash
# Full help
python scripts/generate_synthetic_wfm.py --help

# Documentation
cat docs/guides/synthetic_test_data.md
cat test_data/README.md
cat SYNTHETIC_TEST_DATA_SUMMARY.md
```

## Dependencies

```bash
pip install tm_data_types numpy
```

## Next Steps

1. **Generate test suite**: `python scripts/generate_synthetic_wfm.py --generate-suite`
2. **Verify**: `python scripts/verify_synthetic_test_data.py`
3. **Read full guide**: `docs/guides/synthetic_test_data.md`
4. **Migrate from legacy data**: `docs/guides/test_data_migration.md`

## Status

✓ Production ready
✓ 29/29 files validated
✓ 100% legal compliance
✓ Full documentation

---

For questions: See [test_data/README.md](README.md) or [SYNTHETIC_TEST_DATA_SUMMARY.md](../SYNTHETIC_TEST_DATA_SUMMARY.md)
