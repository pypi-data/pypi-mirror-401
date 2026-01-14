# Installation Guide

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08 | **Applies to**: TraceKit 0.1.x

This guide covers installing TraceKit for development and production use.

## Requirements

- **Python**: 3.12 or higher
- **Package Manager**: [uv](https://docs.astral.sh/uv/) (recommended) or pip
- **OS**: Linux, macOS, or Windows

## Quick Installation

### Using uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/lair-click-bats/tracekit.git
cd tracekit

# Install all dependencies
uv sync

# Verify installation
uv run tracekit --version
uv run python -c "import tracekit; print(tracekit.__version__)"
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/lair-click-bats/tracekit.git
cd tracekit

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package
pip install -e .

# Verify installation
tracekit --version
python -c "import tracekit; print(tracekit.__version__)"
```

## Optional Dependencies

TraceKit uses optional dependency groups for specialized features:

### GPU Acceleration

For CUDA-accelerated FFT and signal processing:

```bash
# Using uv
uv sync --extra gpu

# Using pip
pip install -e ".[gpu]"
```

Requires:

- NVIDIA GPU with compute capability 3.5+
- CUDA Toolkit 11.0+
- cupy package

### Visualization

For interactive plotting and report generation:

```bash
# Using uv
uv sync --extra viz

# Using pip
pip install -e ".[viz]"
```

Includes: matplotlib, plotly, reportlab

### Full Installation

Install everything:

```bash
# Using uv
uv sync --all-extras

# Using pip
pip install -e ".[all]"
```

## Development Installation

For contributing to TraceKit:

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/tracekit.git  # Replace YOUR-USERNAME with your GitHub username
cd tracekit

# Install with dev dependencies
uv sync --dev

# This includes:
# - pytest (testing)
# - ruff (linting/formatting)
# - mypy (type checking)
# - pre-commit (git hooks)

# Install pre-commit hooks
uv run pre-commit install
```

### Verify Development Setup

```bash
# Run quick tests
uv run pytest tests/unit -x --maxfail=5

# Run linter
uv run ruff check src/

# Run type checker
uv run mypy src/
```

## Platform-Specific Notes

### Linux

No special requirements. Ensure Python 3.12+ is available:

```bash
python3 --version
# Python 3.12.x

# On Ubuntu/Debian, install if needed:
sudo apt update
sudo apt install python3.12 python3.12-venv
```

### macOS

Install Python via Homebrew if needed:

```bash
brew install python@3.12

# Verify
python3.12 --version
```

### Windows

Install Python from [python.org](https://www.python.org/downloads/) or Microsoft Store.

Use PowerShell for commands:

```powershell
# Verify Python
python --version

# Use uv
uv run tracekit --version
```

**Note**: Some features (e.g., Sigrok integration) may have limited Windows support.

## Environment Configuration

### CLI Configuration

Create a configuration file for persistent settings:

```bash
# Initialize config
uv run tracekit config --init

# View current config
uv run tracekit config --show
```

This creates `~/.config/tracekit/config.yaml`:

```yaml
# TraceKit Configuration
default_sample_rate: 1e9
output_format: csv
plot_style: default
gpu_enabled: false
```

### Environment Variables

TraceKit respects these environment variables:

| Variable             | Description             | Default                          |
| -------------------- | ----------------------- | -------------------------------- |
| `TRACEKIT_CONFIG`    | Config file path        | `~/.config/tracekit/config.yaml` |
| `TRACEKIT_DATA_DIR`  | Test data directory     | `./test_data`                    |
| `TRACEKIT_GPU`       | Enable GPU acceleration | `false`                          |
| `TRACEKIT_LOG_LEVEL` | Logging verbosity       | `WARNING`                        |

Example:

```bash
export TRACEKIT_GPU=true
export TRACEKIT_LOG_LEVEL=DEBUG
uv run tracekit analyze capture.wfm
```

## Verifying Installation

### Quick Check

```bash
# CLI check
uv run tracekit --version
uv run tracekit --help

# Python check
uv run python -c "
import tracekit as tk
print(f'TraceKit {tk.__version__}')
print(f'Supported formats: {tk.get_supported_formats()}')
"
```

### Test with Sample Data

```bash
# Run example
uv run python examples/01_basics/01_load_waveform.py

# Or use built-in test data
uv run python -c "
import tracekit as tk
from tracekit.testing import generate_sine_wave

# Generate synthetic test signal
trace = generate_sine_wave(frequency=1e6, sample_rate=100e6, duration=1e-3)
print(f'Generated: {len(trace.data)} samples')

# Analyze
freq = tk.measure_frequency(trace)
print(f'Measured frequency: {freq/1e6:.2f} MHz')
"
```

### Run Test Suite

```bash
# Quick validation (recommended for first install)
uv run pytest tests/unit -x --maxfail=5

# Full unit tests (takes longer)
uv run pytest tests/unit -v

# With coverage
uv run pytest tests/unit --cov=src/tracekit --cov-report=term
```

## Troubleshooting

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'tracekit'`

**Solution**: Ensure package is installed in development mode:

```bash
uv pip install -e .
# Or
pip install -e .
```

### Version Conflicts

**Problem**: Dependency version conflicts

**Solution**: Use uv for reliable dependency resolution:

```bash
# Remove old environment
rm -rf .venv

# Fresh install with uv
uv sync
```

### GPU Not Detected

**Problem**: GPU features not available after installing `[gpu]` extra

**Solution**: Verify CUDA setup:

```bash
# Check CUDA
nvcc --version

# Check cupy
uv run python -c "import cupy; print(cupy.cuda.runtime.getDeviceCount())"
```

### Permission Issues

**Problem**: Permission denied errors on Linux/macOS

**Solution**: Use user installation:

```bash
pip install --user -e .

# Or use virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Path Issues

**Problem**: `tracekit: command not found`

**Solution**: Ensure scripts are in PATH:

```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"

# Or use uv run
uv run tracekit --help
```

## Updating

### Update to Latest

```bash
# Pull latest changes
git pull origin main

# Update dependencies
uv sync
```

### Upgrade Dependencies

```bash
# Check for updates
uv pip list --outdated

# Update all
uv lock --upgrade
uv sync
```

## Uninstalling

```bash
# Remove package
pip uninstall tracekit

# Remove virtual environment
rm -rf .venv

# Remove config (optional)
rm -rf ~/.config/tracekit
```

## Next Steps

After installation:

1. Read the [Getting Started](getting-started.md) guide
2. Try the [examples](examples-reference.md)
3. Review the [API Reference](api/index.md)

For development:

1. Read [CONTRIBUTING.md](contributing.md)
2. Review [Testing Guidelines](testing/index.md)
3. Set up your IDE with ruff and mypy integration
