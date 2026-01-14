# Test Data Migration Guide

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08

## Overview

This guide explains how to migrate from legacy test data (Data_Capture/) to synthetic test data for legal compliance and sustainability.

## Why Migrate?

### Legal Issues with Legacy Data

The `test_data/Data_Capture/` directory (954 MB) contains waveform files with potential legal issues:

- **Source**: Military/defense systems
- **Copyright**: Unclear provenance and ownership
- **IP concerns**: May contain proprietary information
- **Distribution risk**: Cannot be safely shared publicly
- **Compliance**: Does not meet open-source legal standards

### Benefits of Synthetic Data

- **Legal safety**: No proprietary or sensitive source material
- **Reproducible**: Can be regenerated at any time
- **Version controlled**: Small enough to commit to git
- **Comprehensive**: Covers all test scenarios systematically
- **CI/CD friendly**: Fast generation in automated pipelines

## Migration Process

### Phase 1: Assess Current Usage

#### Step 1.1: Identify Dependencies

Find all code that references legacy test data:

```bash
# Search for references to Data_Capture
grep -r "Data_Capture" tests/ examples/ docs/

# Search for specific file references
grep -r "\.wfm" tests/ | grep -v synthetic
```

#### Step 1.2: Catalog Test Scenarios

Document what each legacy file is used for:

```python
# Create inventory of legacy files
import json
from pathlib import Path

legacy_files = list(Path("test_data/Data_Capture").glob("**/*.wfm"))
inventory = {}

for f in legacy_files:
    inventory[f.name] = {
        "path": str(f),
        "size": f.stat().st_size,
        "used_in": [],  # Add test files that use this
        "purpose": "",  # Document what it tests
        "replacement": None  # Will be filled in Phase 2
    }

with open("legacy_inventory.json", "w") as fp:
    json.dump(inventory, fp, indent=2)
```

### Phase 2: Generate Replacements

#### Step 2.1: Generate Test Suite

Generate the complete synthetic test suite:

```bash
python scripts/generate_synthetic_wfm.py --generate-suite --output-dir test_data/synthetic/
```

This creates 29 files covering:

- Basic waveforms
- Edge cases
- Size variations
- Frequency variations
- Advanced signal types

#### Step 2.2: Create Custom Replacements

For specific test scenarios not covered by the suite, generate custom files:

```bash
# Example: Replace a specific legacy file
python scripts/generate_synthetic_wfm.py \
    --signal sine \
    --frequency 1000 \
    --amplitude 2.5 \
    --samples 50000 \
    --output test_data/synthetic/custom/replacement_file.wfm
```

#### Step 2.3: Match Legacy Characteristics

If you need to match specific characteristics of legacy files:

```python
from tm_data_types import read_file
from pathlib import Path

# Analyze legacy file
legacy = read_file("test_data/Data_Capture/legacy_file.wfm")
print(f"Record length: {legacy.record_length}")
print(f"Sample rate: {1.0 / legacy.x_axis_spacing} Sa/s")

# Generate matching synthetic file
# python scripts/generate_synthetic_wfm.py \
#     --signal sine \
#     --samples <record_length> \
#     --sample-rate <sample_rate> \
#     --output test_data/synthetic/custom/matched_file.wfm
```

### Phase 3: Update Test Code

#### Step 3.1: Update File Paths

Replace legacy paths with synthetic paths:

```python
# Before
test_file = "test_data/Data_Capture/01_Top/TestParR_RMC_ch1.wfm"

# After
test_file = "test_data/synthetic/basic/sine_1khz.wfm"
```

#### Step 3.2: Update Test Fixtures

Modernize pytest fixtures:

```python
# Before
@pytest.fixture
def test_wfm():
    return "test_data/Data_Capture/01_Top/Buffer4_uknowncommand_ch1.wfm"

# After
@pytest.fixture
def test_wfm():
    return "test_data/synthetic/basic/sine_1khz.wfm"

# Better: Use parametric fixtures for comprehensive testing
@pytest.fixture(params=list(Path("test_data/synthetic").glob("**/*.wfm")))
def all_synthetic_wfms(request):
    return request.param
```

#### Step 3.3: Update Example Code

Update documentation examples:

```python
# Before (in examples/basic_usage.py)
from tracekit.loaders.tektronix import load_tektronix_wfm

trace = load_tektronix_wfm("test_data/Data_Capture/01_Top/TestParR_RMC_ch1.wfm")

# After
trace = load_tektronix_wfm("test_data/synthetic/basic/sine_1khz.wfm")
```

### Phase 4: Validation

#### Step 4.1: Run Existing Tests

Verify tests pass with synthetic data:

```bash
# Run all tests
pytest tests/ -v

# Run specific test module
pytest tests/unit/test_loaders.py -v

# Run with coverage
pytest tests/ --cov=tracekit --cov-report=html
```

#### Step 4.2: Compare Results

Verify synthetic data produces equivalent results:

```python
import numpy as np
from tracekit.loaders.tektronix import load_tektronix_wfm

# Load both versions
legacy = load_tektronix_wfm("test_data/Data_Capture/legacy.wfm")
synthetic = load_tektronix_wfm("test_data/synthetic/replacement.wfm")

# Compare characteristics (not exact values)
assert len(legacy.data) == len(synthetic.data)
assert abs(legacy.metadata.sample_rate - synthetic.metadata.sample_rate) < 1e-6

# Test that analysis functions work on both
from tracekit.analyzers.waveform.measurements import measure_frequency

freq_legacy = measure_frequency(legacy)
freq_synthetic = measure_frequency(synthetic)
# Both should produce valid results (values will differ)
assert freq_legacy > 0
assert freq_synthetic > 0
```

#### Step 4.3: Performance Testing

Verify performance with synthetic data:

```python
import time
from tracekit.loaders.tektronix import load_tektronix_wfm

# Test loading speed
synthetic_files = list(Path("test_data/synthetic").glob("**/*.wfm"))

start = time.time()
for f in synthetic_files:
    trace = load_tektronix_wfm(f)
    assert trace.data is not None
elapsed = time.time() - start

print(f"Loaded {len(synthetic_files)} files in {elapsed:.2f}s")
print(f"Average: {elapsed/len(synthetic_files):.3f}s per file")
```

### Phase 5: Update Documentation

#### Step 5.1: Update README

Update main README to reference synthetic data:

````markdown
## Quick Start

```python
from tracekit.loaders.tektronix import load_tektronix_wfm

# Load a test file (synthetic data for legal compliance)
trace = load_tektronix_wfm("test_data/synthetic/basic/sine_1khz.wfm")
print(f"Loaded {len(trace.data)} samples")
```
````

#### Step 5.2: Update Examples

Update all example scripts:

```bash
# Find all Python files with test data references
find examples/ -name "*.py" -exec grep -l "test_data" {} \;

# Update each one to use synthetic data
```

#### Step 5.3: Update API Documentation

Update docstrings with synthetic data examples:

```python
def load_tektronix_wfm(path):
    """Load a Tektronix WFM file.

    Example:
        >>> # Use synthetic test data
        >>> trace = load_tektronix_wfm("test_data/synthetic/basic/sine_1khz.wfm")
        >>> print(len(trace.data))
        1000
    """
```

### Phase 6: Remove Legacy Data

#### Step 6.1: Backup (Optional)

If you want to keep a backup:

```bash
# Create archive (not for distribution)
tar czf legacy_test_data_backup.tar.gz test_data/Data_Capture/

# Move to secure location
mv legacy_test_data_backup.tar.gz ~/secure_backup/
```

#### Step 6.2: Update .gitignore

Ensure legacy data is excluded:

```gitignore
# .gitignore
test_data/Data_Capture/
test_data/*.zip
*.tar.gz

# Include synthetic data
!test_data/synthetic/
!../getting-started.md#prerequisites
```

#### Step 6.3: Remove from Repository

```bash
# Remove from working directory
rm -rf test_data/Data_Capture/

# If previously committed, remove from git history (optional, advanced)
# WARNING: This rewrites history
git filter-branch --tree-filter 'rm -rf test_data/Data_Capture' HEAD
```

### Phase 7: CI/CD Integration

#### Step 7.1: Update CI Configuration

Update GitHub Actions or other CI to generate synthetic data:

```yaml
# .github/workflows/test.yml
name: Test

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
          pytest tests/ -v --cov=tracekit
```

#### Step 7.2: Test in Clean Environment

Verify tests work from scratch:

```bash
# Clone into fresh directory
git clone <repo-url> test-migration
cd test-migration

# Set up environment
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install tm_data_types numpy pytest

# Generate test data
python scripts/generate_synthetic_wfm.py --generate-suite

# Run tests
pytest tests/ -v
```

## Migration Checklist

Use this checklist to track migration progress:

- [ ] Phase 1: Assess Current Usage
  - [ ] Identify all legacy data dependencies
  - [ ] Catalog test scenarios
  - [ ] Document current test coverage

- [ ] Phase 2: Generate Replacements
  - [ ] Generate test suite
  - [ ] Create custom replacements
  - [ ] Verify file characteristics

- [ ] Phase 3: Update Code
  - [ ] Update test file paths
  - [ ] Modernize test fixtures
  - [ ] Update examples

- [ ] Phase 4: Validation
  - [ ] Run existing tests
  - [ ] Compare results
  - [ ] Performance testing

- [ ] Phase 5: Documentation
  - [ ] Update README
  - [ ] Update examples
  - [ ] Update API docs

- [ ] Phase 6: Cleanup
  - [ ] Create backup (optional)
  - [ ] Update .gitignore
  - [ ] Remove legacy data

- [ ] Phase 7: CI/CD
  - [ ] Update CI configuration
  - [ ] Test in clean environment
  - [ ] Verify automated builds

## Troubleshooting

### Tests Fail with Synthetic Data

If tests expect specific data values:

```python
# Bad: Testing specific values
assert trace.data[0] == 4180  # Fails with synthetic data

# Good: Testing properties
assert len(trace.data) > 0
assert trace.data.dtype == np.float64
assert trace.metadata.sample_rate > 0
```

### Performance Degradation

If synthetic generation is slow in CI:

```bash
# Cache generated files
- uses: actions/cache@v3
  with:
    path: test_data/synthetic
    key: synthetic-data-${{ hashFiles('scripts/generate_synthetic_wfm.py') }}
```

### Missing Test Scenarios

If synthetic data doesn't cover a scenario:

```bash
# Generate custom file
python scripts/generate_synthetic_wfm.py \
    --signal <type> \
    --frequency <freq> \
    --amplitude <amp> \
    --output test_data/synthetic/custom/scenario.wfm
```

## Best Practices

1. **Version control generator**: Commit `generate_synthetic_wfm.py`, not output
2. **Document scenarios**: Clearly state what each test file is for
3. **Test properties, not values**: Focus on correctness, not exact numbers
4. **Generate on demand**: Create in CI rather than committing files
5. **Keep it simple**: Use test suite when possible, custom files when needed

## Support

For migration assistance:

1. Review [Test Data Strategy](../getting-started.md#prerequisites)
2. Check [Synthetic Data Guide](synthetic-test-data.md)
3. Run generator help: `python scripts/generate_synthetic_wfm.py --help`
4. File issue on GitHub

## Timeline Estimate

Typical migration timeline:

- **Small project** (< 10 test files): 1-2 days
- **Medium project** (10-50 test files): 1 week
- **Large project** (> 50 test files): 2-3 weeks

Most time is spent on:

- Identifying dependencies (30%)
- Updating tests (40%)
- Validation (20%)
- Documentation (10%)
