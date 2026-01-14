# Synthetic Test Data Generation Guide

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08

## Overview

TraceKit uses synthetic test data to ensure legal compliance and reproducibility. This guide explains how to generate, manage, and use synthetic Tektronix WFM files for testing.

## Why Synthetic Data?

### Legal Compliance

- **No proprietary data**: All files generated programmatically
- **No IP concerns**: Uses open-source tm_data_types library
- **Safe distribution**: Can be included in public repositories
- **Clear provenance**: Fully documented generation process

### Technical Benefits

- **Reproducible**: Same inputs always produce same outputs
- **Customizable**: Generate exactly the signal types needed
- **Comprehensive**: Cover all edge cases systematically
- **Version controlled**: Small files suitable for git
- **CI/CD friendly**: Fast generation in automated pipelines

## Quick Start

### Generate Test Suite

Generate the complete synthetic test suite with one command:

```bash
python scripts/generate_synthetic_wfm.py --generate-suite
```

This creates 29 test files covering:

- Basic waveforms (sine, square, triangle, sawtooth, pulse)
- Edge cases (DC, noise, extreme amplitudes)
- Size variations (100 samples to 1M samples)
- Frequency variations (10 Hz to 100 kHz)
- Advanced signals (chirp, PWM, damped oscillations)

### Generate Custom Signal

Generate a specific signal type:

```bash
# 10 kHz sine wave, 3.3V amplitude
python scripts/generate_synthetic_wfm.py \
    --signal sine \
    --frequency 10000 \
    --amplitude 3.3 \
    --output my_signal.wfm

# Square wave with 25% duty cycle
python scripts/generate_synthetic_wfm.py \
    --signal pulse \
    --frequency 5000 \
    --duty-cycle 0.25 \
    --output square_25pct.wfm

# Noisy signal (SNR = 30 dB)
python scripts/generate_synthetic_wfm.py \
    --signal sine \
    --frequency 1000 \
    --snr 30 \
    --output noisy_sine.wfm
```

## Signal Types

### Basic Waveforms

#### Sine Wave

```bash
python scripts/generate_synthetic_wfm.py \
    --signal sine \
    --frequency 1000 \
    --amplitude 2.0 \
    --phase 0 \
    --output sine.wfm
```

Pure sinusoidal signal. Parameters:

- `frequency`: Frequency in Hz
- `amplitude`: Peak amplitude in V
- `phase`: Phase offset in radians

#### Square Wave

```bash
python scripts/generate_synthetic_wfm.py \
    --signal square \
    --frequency 5000 \
    --amplitude 3.3 \
    --output square.wfm
```

Square wave using Fourier series approximation (20 harmonics).

#### Triangle Wave

```bash
python scripts/generate_synthetic_wfm.py \
    --signal triangle \
    --frequency 2000 \
    --output triangle.wfm
```

Linear ramp up and down.

#### Sawtooth Wave

```bash
python scripts/generate_synthetic_wfm.py \
    --signal sawtooth \
    --frequency 3000 \
    --output sawtooth.wfm
```

Linear ramp with sharp reset.

#### Pulse Train

```bash
python scripts/generate_synthetic_wfm.py \
    --signal pulse \
    --frequency 10000 \
    --duty-cycle 0.3 \
    --output pulse_30pct.wfm
```

Pulse train with configurable duty cycle (0.0 to 1.0).

### Advanced Signals

#### Chirp (Frequency Sweep)

```bash
python scripts/generate_synthetic_wfm.py \
    --signal chirp \
    --output chirp.wfm
```

Linear frequency sweep from 100 Hz to 10 kHz. Useful for frequency response testing.

#### PWM (Pulse Width Modulation)

```bash
python scripts/generate_synthetic_wfm.py \
    --signal pwm \
    --output pwm.wfm
```

Pulse train with sinusoidally varying duty cycle (10% to 90%).

#### Damped Oscillation

```bash
python scripts/generate_synthetic_wfm.py \
    --signal damped_sine \
    --frequency 1000 \
    --output damped.wfm
```

Exponentially decaying sine wave. Simulates RLC circuit response.

#### Exponential Decay

```bash
python scripts/generate_synthetic_wfm.py \
    --signal exponential \
    --output decay.wfm
```

Pure exponential decay. Useful for RC circuit testing.

#### Mixed Signal

```bash
python scripts/generate_synthetic_wfm.py \
    --signal mixed \
    --output harmonics.wfm
```

Combination of multiple frequency components with decreasing amplitudes.

### Special Cases

#### DC Signal

```bash
python scripts/generate_synthetic_wfm.py \
    --signal dc \
    --amplitude 2.5 \
    --output dc_2v5.wfm
```

Constant voltage level.

#### White Noise

```bash
python scripts/generate_synthetic_wfm.py \
    --signal noisy \
    --amplitude 1.0 \
    --output noise.wfm
```

Random Gaussian noise.

#### Signal with DC Offset

```bash
python scripts/generate_synthetic_wfm.py \
    --signal sine \
    --frequency 1000 \
    --amplitude 1.0 \
    --offset 2.5 \
    --output sine_offset.wfm
```

Any signal can have a DC offset applied.

#### Signal with Noise

```bash
python scripts/generate_synthetic_wfm.py \
    --signal sine \
    --frequency 1000 \
    --snr 40 \
    --output sine_noisy.wfm
```

Add white Gaussian noise to any signal (SNR in dB).

## Advanced Options

### Sample Rate and Duration

```bash
# High sample rate (10 MSa/s)
python scripts/generate_synthetic_wfm.py \
    --signal sine \
    --frequency 1000 \
    --sample-rate 10e6 \
    --duration 0.001 \
    --output high_sr.wfm

# Low sample rate (100 kSa/s)
python scripts/generate_synthetic_wfm.py \
    --signal sine \
    --frequency 1000 \
    --sample-rate 100e3 \
    --duration 0.01 \
    --output low_sr.wfm

# Specific number of samples
python scripts/generate_synthetic_wfm.py \
    --signal sine \
    --frequency 1000 \
    --samples 100000 \
    --output 100k_samples.wfm
```

### File Sizes

Control file size through sample count:

```bash
# Small file (~1 KB)
python scripts/generate_synthetic_wfm.py \
    --signal sine --samples 100 --output small.wfm

# Medium file (~20 KB)
python scripts/generate_synthetic_wfm.py \
    --signal sine --samples 10000 --output medium.wfm

# Large file (~2 MB)
python scripts/generate_synthetic_wfm.py \
    --signal sine --samples 1000000 --output large.wfm
```

### Channel Names

```bash
python scripts/generate_synthetic_wfm.py \
    --signal sine \
    --channel CH2 \
    --output ch2_signal.wfm
```

## Integration with Testing

### Pytest Fixtures

```python
# tests/conftest.py
import pytest
from pathlib import Path

@pytest.fixture
def synthetic_wfm_files():
    """Provide all synthetic WFM test files."""
    return list(Path("test_data/synthetic").glob("**/*.wfm"))

@pytest.fixture
def basic_wfm_files():
    """Provide basic signal WFM files."""
    return list(Path("test_data/synthetic/basic").glob("*.wfm"))

# tests/test_wfm_loading.py
def test_load_all_synthetic_files(synthetic_wfm_files):
    """Test loading all synthetic WFM files."""
    from tracekit.loaders.tektronix import load_tektronix_wfm

    for wfm_file in synthetic_wfm_files:
        trace = load_tektronix_wfm(wfm_file)
        assert trace.data is not None
        assert len(trace.data) > 0
        assert trace.metadata.sample_rate > 0
```

### Parametric Testing

```python
import pytest
from pathlib import Path

SYNTHETIC_DIR = Path("test_data/synthetic")

@pytest.mark.parametrize("wfm_file", SYNTHETIC_DIR.glob("**/*.wfm"))
def test_wfm_file(wfm_file):
    """Parametric test for each WFM file."""
    from tracekit.loaders.tektronix import load_tektronix_wfm

    trace = load_tektronix_wfm(wfm_file)
    assert trace.data is not None
```

### CI/CD Pipeline

```yaml
# .github/workflows/test.yml
name: Test with Synthetic Data

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install -e .
          pip install tm_data_types numpy pytest

      - name: Generate synthetic test data
        run: |
          python scripts/generate_synthetic_wfm.py --generate-suite

      - name: Run tests
        run: |
          pytest tests/ -v
```

## File Format Details

### WFM#003 Format

Generated files use the Tektronix WFM#003 format:

- **Magic bytes**: `:WFM#003` at file start
- **Header**: ~858 bytes of metadata
- **Data**: 16-bit signed integer samples
- **Scaling**: Y = (raw_value \* y_spacing) + y_offset

### Metadata

Each file contains:

- Sample rate (X axis spacing)
- Time units (typically seconds)
- Voltage units (typically volts)
- Y-axis offset and scaling
- Source channel name

### Verification

Verify generated files:

```python
from tm_data_types import read_file
import numpy as np

wf = read_file("test.wfm")
print(f"Samples: {wf.record_length}")
print(f"Sample rate: {1.0 / wf.x_axis_spacing} Sa/s")
print(f"Duration: {wf.record_length * wf.x_axis_spacing} s")

# Reconstruct voltage values
y_raw = np.array(wf.y_axis_values)
y_volts = y_raw * wf.y_axis_spacing + wf.y_axis_offset
print(f"Voltage range: [{y_volts.min():.3f}, {y_volts.max():.3f}] V")
```

## Best Practices

### For Testing

1. **Use test suite**: Start with `--generate-suite` for comprehensive coverage
2. **Generate on demand**: Create in CI/CD rather than committing to repo
3. **Version control generator**: Commit `generate_synthetic_wfm.py`, not output files
4. **Document requirements**: Clearly state which files tests need

### For Development

1. **Custom scenarios**: Generate specific signals for debugging
2. **Edge cases**: Test extreme values (0V, high frequency, large files)
3. **Reproducibility**: Use same parameters for consistent results
4. **Performance testing**: Use large files for memory/speed tests

### For Documentation

1. **Example data**: Use synthetic files in tutorials
2. **Screenshots**: Generate known signals for visualization examples
3. **API examples**: Demonstrate with reproducible data

## Troubleshooting

### Import Error: tm_data_types

```bash
pip install tm_data_types
```

### Generator Not Found

```bash
# Make sure you're in the TraceKit root directory
python scripts/generate_synthetic_wfm.py --help
```

### File Too Large

Reduce sample count:

```bash
python scripts/generate_synthetic_wfm.py \
    --signal sine \
    --samples 1000 \
    --output small.wfm
```

### Invalid Signal Type

Check available types:

```bash
python scripts/generate_synthetic_wfm.py --help
```

Available: sine, square, triangle, sawtooth, pulse, dc, noisy, mixed, chirp, pwm, exponential, damped_sine

## Reference

### Command-Line Options

```
usage: generate_synthetic_wfm.py [--generate-suite | --signal TYPE] [options]

Required (choose one):
  --generate-suite        Generate complete test suite
  --signal TYPE           Signal type to generate

Output:
  -o, --output PATH       Output file path (single file mode)
  --output-dir DIR        Output directory (suite mode)

Signal parameters:
  -f, --frequency HZ      Signal frequency (default: 1000)
  -a, --amplitude V       Signal amplitude (default: 1.0)
  -r, --sample-rate SA/S  Sample rate (default: 1e6)
  -d, --duration S        Signal duration (default: 0.001)
  -n, --samples N         Number of samples (overrides duration)
  --offset V              DC offset (default: 0.0)
  --phase RAD             Phase in radians (default: 0.0)
  --duty-cycle RATIO      Duty cycle for pulse/PWM (default: 0.5)
  --snr DB                Signal-to-noise ratio in dB
  --channel NAME          Channel name (default: CH1)

Other:
  -v, --verbose           Verbose output
  -h, --help             Show help message
```

### Dependencies

- **Python**: 3.9+
- **tm_data_types**: 0.3.0+
- **numpy**: Any recent version

### Related Documentation

- [Test Data Strategy](../getting-started.md#prerequisites)
- [WFM File Format](https://download.tek.com/manual/Waveform-File-Format-Manual-077022011.pdf)
- [tm_data_types Documentation](https://tm-data-types.readthedocs.io)

## Support

For issues or questions:

1. Check generator help: `python scripts/generate_synthetic_wfm.py --help`
2. Review test data README: `../getting-started.md#prerequisites`
3. Consult tm_data_types documentation
4. File issue on GitHub
