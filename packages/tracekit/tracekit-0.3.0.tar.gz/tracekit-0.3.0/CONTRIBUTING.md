# Contributing to TraceKit

First off, thank you for considering contributing to TraceKit! It's people like you that make TraceKit such a great tool.

## Versioning and Compatibility

TraceKit follows [Semantic Versioning](https://semver.org/) (SemVer):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

**Stability Commitment:**

- Backwards compatibility - Maintained within major versions
- Deprecation warnings - Added before removing features
- Migration guides - Provided for major version upgrades
- Semantic versioning - Strictly followed for all releases

## Code of Conduct

This project and everyone participating in it is governed by the [TraceKit Code of Conduct](code-of-conduct.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (code snippets, waveform files, etc.)
- **Describe the behavior you observed and what you expected**
- **Include your environment details** (Python version, OS, TraceKit version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List any alternatives you've considered**

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the test suite (`uv run pytest tests/unit -v`)
5. Run linting (`uv run ruff check src/ tests/`)
6. Commit your changes using [conventional commits](https://www.conventionalcommits.org/)
7. Push to your branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Development Setup

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/tracekit.git
cd tracekit

# Install dependencies
uv sync

# Verify setup
uv run pytest tests/unit -x --maxfail=5
```

### Development Commands

#### Running Tests

For comprehensive test documentation, see **[TESTING_GUIDELINES.md](testing/index.md)**.

Quick reference:

```bash
# Run unit tests (recommended)
uv run pytest tests/unit -v --timeout=90

# Run tests with coverage
uv run pytest tests/unit --cov=src/tracekit --cov-report=term-missing

# Run specific module tests
uv run pytest tests/unit/analyzers -v
uv run pytest tests/unit/protocols -v

# Run in parallel
uv run pytest tests/unit -n 4
```

#### Other Commands

```bash
# Lint code
uv run ruff check src/ tests/

# Format code
uv run ruff format src/ tests/

# Type check
uv run mypy src/
```

## Coding Standards

### Style Guide

- Follow PEP 8 (enforced by ruff)
- Use type hints for all function signatures
- Write docstrings for all public functions and classes
- Keep functions focused and small

### Commit Messages

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, missing semi-colons, etc.)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding missing tests
- `chore`: Maintenance tasks

**Examples:**

```
feat(protocols): add FlexRay decoder support
fix(loaders): correct Tektronix WFM channel parsing
docs(api): add spectral analysis examples
test(analyzers): increase rise time test coverage
```

### Testing

- Write tests for all new features
- Maintain or improve test coverage
- Use descriptive test names that explain the scenario
- Follow the existing test structure

### Documentation

- Update documentation for any user-facing changes
- Add docstrings to all public functions
- Include code examples where helpful
- Keep README.md up to date

## IEEE Compliance Guidelines

When implementing measurement functions, follow IEEE standards:

- **IEEE 181-2011**: Pulse measurements (rise/fall time, slew rate)
- **IEEE 1241-2010**: ADC testing (SNR, SINAD, ENOB)
- **IEEE 2414-2020**: Jitter measurements (TIE, period jitter)

Include references to specific standard sections in docstrings:

```python
def rise_time(trace: TraceData, low: float = 0.1, high: float = 0.9) -> float:
    """Calculate rise time per IEEE 181-2011 Section 5.2.

    The rise time is the interval between the reference level instants
    when the signal crosses the specified low and high percentage levels.

    Args:
        trace: Input waveform trace.
        low: Low reference level (0-1). Default 10%.
        high: High reference level (0-1). Default 90%.

    Returns:
        Rise time in seconds.

    References:
        IEEE 181-2011 Section 5.2 "Rise Time and Fall Time"
    """
```

## Documentation Checklist

Before submitting a PR that includes new code, ensure:

- [ ] All new public functions have docstrings
- [ ] Docstrings follow NumPy style format
- [ ] Args section lists all parameters with descriptions
- [ ] Returns section describes the return value
- [ ] Raises section documents all exceptions (if applicable)
- [ ] Examples are included for complex functionality
- [ ] User-facing docs updated if behavior changes
- [ ] CHANGELOG.md updated for user-visible changes
- [ ] **IEEE references included** for measurement functions

### Docstring Format

Use NumPy-style docstrings:

```python
def example_function(param1: str, param2: int = 0) -> bool:
    """Brief one-line description.

    Extended description if needed. Can span multiple lines
    and provide additional context.

    Parameters
    ----------
    param1 : str
        Description of first parameter.
    param2 : int, optional
        Description of second parameter. Default is 0.

    Returns
    -------
    bool
        Description of return value.

    Raises
    ------
    ValueError
        When param1 is empty.
    TypeError
        When param2 is not an integer.

    Examples
    --------
    >>> example_function("value", 10)
    True

    Notes
    -----
    Additional implementation notes if needed.

    References
    ----------
    IEEE 181-2011 Section X.X (if applicable)
    """
```

## Project Structure

```
tracekit/
├── docs/                   # Documentation
│   ├── TESTING_GUIDELINES.md    # Testing approach
│   └── api/                     # API reference
├── examples/               # Usage examples
├── src/tracekit/           # Source code
│   ├── core/               # Data types, exceptions, configuration
│   ├── loaders/            # File format loaders
│   ├── analyzers/          # Signal analysis modules
│   │   ├── digital/        # Digital signal processing
│   │   ├── spectral/       # Spectral analysis
│   │   ├── statistical/    # Statistical analysis
│   │   └── patterns/       # Pattern detection
│   ├── protocols/          # Protocol decoders
│   ├── inference/          # Protocol inference
│   ├── exporters/          # Data export formats
│   └── visualization/      # Plotting utilities
└── tests/                  # Test suite
    ├── unit/               # Unit tests
    ├── integration/        # Integration tests
    ├── validation/         # IEEE compliance tests
    └── performance/        # Benchmark tests
```

## Getting Help

- **GitHub Discussions**: For questions and discussions
- **GitHub Issues**: For bugs and feature requests

## Recognition

Contributors are recognized in:

- The CHANGELOG.md for significant contributions
- The GitHub contributors page
- Special thanks in release notes for major features

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to TraceKit!
