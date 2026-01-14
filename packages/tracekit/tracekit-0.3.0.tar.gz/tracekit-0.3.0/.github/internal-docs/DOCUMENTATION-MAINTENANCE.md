# Documentation Maintenance Best Practices

> How to keep TraceKit's API documentation accurate, complete, and up-to-date

## Overview

This guide explains the systems and practices in place to ensure TraceKit's documentation stays synchronized with the codebase, and how to maintain it going forward.

## Automated Validation

### 1. API Documentation Validator

**Script**: `scripts/validate_api_docs.py`

This script automatically checks:

- ✅ All public functions in `src/tracekit/__init__.py` are documented
- ✅ No "phantom" documentation (documenting functions that don't exist)
- ✅ All code examples in docs have valid Python syntax
- ✅ Example code in `examples/` directory is syntactically valid

**Usage**:

```bash
# Run validation
python scripts/validate_api_docs.py

# With verbose output
python scripts/validate_api_docs.py --verbose

# In CI/CD (exits with non-zero on failure)
python scripts/validate_api_docs.py
```

**What it catches**:

```
❌ Undocumented API (3 items)
  - new_function() - function
    Signature: (trace, threshold=0.5)

⚠️  Phantom Documentation (2 items)
  - old_function() - Documented but doesn't exist in actual API

❌ Syntax Errors (1 items)
  - docs/api/analysis.md:45
    Invalid Python syntax: unexpected EOF while parsing
```

### 2. Link Validator

**Script**: `scripts/validate_docs.py`

Checks for:

- ✅ Broken internal links between documentation files
- ✅ Missing required documentation structure
- ✅ Missing category READMEs

**Usage**:

```bash
# Check all links
python scripts/validate_docs.py

# Show fix suggestions
python scripts/validate_docs.py --fix-suggestions
```

### 3. CI/CD Integration

**Workflow**: `.github/workflows/docs.yml`

Runs automatically on:

- Every push to `main` branch
- Every pull request modifying `docs/**` or `src/**/*.py`
- Manual trigger

**What it does**:

1. **Docstring Coverage** - Checks docstring coverage with `interrogate`
2. **Build Test** - Builds documentation with MkDocs in strict mode
3. **Doctests** - Runs all doctest examples in source code
4. **Docstring Lint** - Checks docstring style with ruff
5. **Spell Check** - Runs cSpell on all documentation
6. **Deploy** - Deploys to GitHub Pages (on main branch only)

## Manual Maintenance Checklist

### When Adding New Functions

**Before committing code:**

1. **Add to `__init__.py` exports**:

   ```python
   # src/tracekit/__init__.py
   from tracekit.analyzers.power import instantaneous_power

   __all__ = [
       # ... existing exports ...
       "instantaneous_power",
   ]
   ```

2. **Write comprehensive docstring**:

   ```python
   def instantaneous_power(voltage: WaveformTrace, current: WaveformTrace) -> WaveformTrace:
       """Calculate instantaneous power P(t) = V(t) × I(t).

       Parameters
       ----------
       voltage : WaveformTrace
           Voltage waveform
       current : WaveformTrace
           Current waveform

       Returns
       -------
       WaveformTrace
           Instantaneous power waveform

       Examples
       --------
       >>> power = tk.instantaneous_power(voltage, current)
       >>> avg_power = np.mean(power.data)

       See Also
       --------
       average_power : Calculate average power over time
       """
   ```

3. **Add to API documentation** (`docs/api/`):
   - Find the appropriate API doc file (e.g., `docs/api/power-analysis.md`)
   - Add function signature, parameters, return values
   - Include 2-3 practical examples
   - Add "See Also" links to related functions

4. **Update API index** (`docs/api/index.md`):
   - Add to Quick Links if it's a major category
   - Add to API Overview with example code
   - Add to Module Reference table

5. **Add to guides** (if applicable):
   - Update relevant task-focused guide (e.g., `docs/guides/power-analysis-guide.md`)
   - Include in workflow examples

6. **Run validators**:

   ```bash
   # Check API coverage
   python scripts/validate_api_docs.py

   # Check links
   python scripts/validate_docs.py

   # Build docs locally
   mkdocs serve
   ```

### When Renaming/Removing Functions

**Critical: This breaks backward compatibility!**

1. **Update all documentation files**:

   ```bash
   # Find all references
   grep -r "old_function_name" docs/

   # Update each file
   # docs/api/analysis.md
   # docs/getting-started.md
   # docs/tutorials/*.md
   ```

2. **Update examples**:

   ```bash
   grep -r "old_function_name" examples/
   ```

3. **Add deprecation notice** (before removing):

   ```python
   import warnings

   def old_function_name(*args, **kwargs):
       """Deprecated: Use new_function_name instead."""
       warnings.warn(
           "old_function_name is deprecated, use new_function_name instead",
           DeprecationWarning,
           stacklevel=2
       )
       return new_function_name(*args, **kwargs)
   ```

4. **Update CHANGELOG.md**:

   ```markdown
   ## [Unreleased]

   ### Changed

   - Renamed `old_function_name()` to `new_function_name()` for clarity

   ### Deprecated

   - `old_function_name()` - Use `new_function_name()` instead
   ```

5. **Run validators**:

   ```bash
   python scripts/validate_api_docs.py
   python scripts/validate_docs.py
   ```

### When Changing Function Signatures

**Example: Adding a new parameter**

1. **Use backward-compatible defaults**:

   ```python
   # GOOD - backward compatible
   def analyze(trace, method="auto", new_param=None):
       pass

   # BAD - breaks existing code
   def analyze(trace, method, new_param):
       pass
   ```

2. **Update all documentation examples**:

   ```bash
   # Find all usage examples
   grep -r "analyze(" docs/ examples/
   ```

3. **Update docstring with new parameter**:

   ```python
   """
   Parameters
   ----------
   trace : WaveformTrace
       Input waveform
   method : str, default="auto"
       Analysis method
   new_param : float, optional
       New parameter for advanced analysis
   """
   ```

4. **Add migration guide** (if major change):

   ````markdown
   # docs/guides/migration-guide.md

   ## Migrating to v0.2.0

   ### analyze() function

   The `analyze()` function now supports a `new_param` parameter:

   **Before:**

   ```python
   result = tk.analyze(trace, method="fft")
   ```
   ````

   **After:**

   ```python
   result = tk.analyze(trace, method="fft", new_param=1.5)
   ```

   ```

   ```

## Automated Testing of Documentation

### Doctests

All docstrings with `>>>` examples are automatically tested:

```python
def frequency(trace: WaveformTrace) -> float:
    """Measure signal frequency.

    Examples
    --------
    >>> import numpy as np
    >>> import tracekit as tk
    >>> # Create 1 MHz sine wave
    >>> t = np.linspace(0, 1e-6, 1000)
    >>> data = np.sin(2 * np.pi * 1e6 * t)
    >>> trace = tk.WaveformTrace(data, metadata=tk.TraceMetadata(sample_rate=1e9))
    >>> freq = tk.frequency(trace)
    >>> abs(freq - 1e6) < 1000  # Within 1 kHz
    True
    """
```

**Run doctests**:

```bash
pytest --doctest-modules src/tracekit/
```

### Example Code Testing

All example scripts are syntax-checked and optionally run:

```bash
# Syntax check all examples
python -m py_compile examples/**/*.py

# Run all examples (with test data)
python examples/run_all_examples.py
```

## Documentation Quality Standards

### Function Documentation Template

Use this template for all new functions:

```python
def function_name(
    param1: Type1,
    param2: Type2,
    optional_param: Type3 = default_value,
) -> ReturnType:
    """One-line summary (imperative mood).

    More detailed description explaining what the function does,
    when to use it, and any important caveats.

    Parameters
    ----------
    param1 : Type1
        Description of param1
    param2 : Type2
        Description of param2
    optional_param : Type3, default=default_value
        Description of optional_param

    Returns
    -------
    ReturnType
        Description of return value

    Raises
    ------
    ValueError
        When param1 is negative
    TypeError
        When param2 is not a WaveformTrace

    Examples
    --------
    Basic usage:

    >>> result = function_name(value1, value2)
    >>> print(result)
    42

    Advanced usage with optional parameter:

    >>> result = function_name(value1, value2, optional_param=100)

    See Also
    --------
    related_function : Brief description
    other_function : Brief description

    Notes
    -----
    Implementation notes, algorithm details, references to papers or
    standards (IEEE, IEC, etc.).

    References
    ----------
    .. [1] Smith et al. "Paper Title", Journal, 2020.
    """
```

### Markdown Documentation Template

For API docs (`docs/api/*.md`):

```markdown
# Module Name API

> **Version**: 0.1.0 | **Last Updated**: YYYY-MM-DD

Brief description of what this module provides.

## Quick Start

\`\`\`python
import tracekit as tk

# Basic usage example

result = tk.function_name(input_data)
\`\`\`

## Functions

### function_name()

Description of what it does and when to use it.

**Signature**:
\`\`\`python
tk.function_name(param1, param2, optional=default) -> ReturnType
\`\`\`

**Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `param1` | `Type1` | required | Description |
| `param2` | `Type2` | required | Description |
| `optional` | `Type3` | `default` | Description |

**Returns**:

- `ReturnType` - Description of return value

**Example**:
\`\`\`python
result = tk.function_name(value1, value2)
print(result)
\`\`\`

**See Also**:

- `related_function()` - Brief description

## Best Practices

- Tip 1
- Tip 2

## Common Pitfalls

- Issue 1 and how to avoid it
- Issue 2 and how to avoid it
```

## Version Management

### Documentation Versioning

1. **Update version in all docs when releasing**:

   ```bash
   # Find all version headers
   grep -r "Version.*:" docs/

   # Update with sed or manually
   find docs -name "*.md" -exec sed -i 's/Version: 0.1.0/Version: 0.2.0/g' {} \;
   ```

2. **Update dates**:

   ```bash
   find docs -name "*.md" -exec sed -i "s/Last Updated: .*/Last Updated: $(date +%Y-%m-%d)/g" {} \;
   ```

3. **Version-specific documentation**:
   - Keep old versions in `docs/versions/v0.1/`
   - Current version always at `docs/`
   - MkDocs can serve multiple versions

## Pre-Commit Hooks

**Recommended**: Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: validate-api-docs
        name: Validate API Documentation
        entry: python scripts/validate_api_docs.py
        language: system
        pass_filenames: false
        files: \.(py|md)$

      - id: validate-doc-links
        name: Validate Documentation Links
        entry: python scripts/validate_docs.py
        language: system
        pass_filenames: false
        files: \.md$
```

**Install**:

```bash
pip install pre-commit
pre-commit install
```

Now validations run automatically before every commit!

## Continuous Monitoring

### GitHub Actions Badges

Add to `README.md`:

```markdown
![Docs](https://github.com/your-org/tracekit/workflows/Documentation/badge.svg)
![API Coverage](https://img.shields.io/badge/API%20Coverage-100%25-brightgreen)
```

### Regular Audits

**Monthly**:

- [ ] Run full validation suite
- [ ] Check for outdated screenshots/diagrams
- [ ] Review and update tutorials with latest best practices
- [ ] Update external links (they may have changed)

**Per Release**:

- [ ] Update all version numbers
- [ ] Update all "Last Updated" dates
- [ ] Run `scripts/validate_api_docs.py`
- [ ] Run `scripts/validate_docs.py`
- [ ] Build and review documentation site locally
- [ ] Check CHANGELOG.md is complete

## Troubleshooting

### "Undocumented API" Errors

**Problem**: New function shows as undocumented

**Solution**:

1. Check function is in `src/tracekit/__init__.py` `__all__` list
2. Add to appropriate API doc file in `docs/api/`
3. Use function name exactly as it appears in code

### "Phantom Documentation" Warnings

**Problem**: Documentation references function that doesn't exist

**Causes**:

- Function was renamed/removed but docs not updated
- Typo in function name
- Wrong module path

**Solution**:

1. Find all references: `grep -r "function_name" docs/`
2. Update or remove references
3. Add redirect/deprecation notice if needed

### Code Example Syntax Errors

**Problem**: Code examples don't parse

**Common causes**:

- Incomplete imports
- Undefined variables
- Mixing example styles (full script vs. snippet)

**Solution**:

```python
# GOOD - Complete example
import tracekit as tk
trace = tk.load("file.wfm")
freq = tk.frequency(trace)

# GOOD - Clear placeholder
# Load your trace file
trace = tk.load("your_file.wfm")

# BAD - Incomplete
freq = tk.frequency(trace)  # Where does 'trace' come from?
```

## Summary

**Key Practices**:

1. ✅ **Always update docs when changing API** - Documentation and code changes go in the same commit
2. ✅ **Run validators before committing** - `scripts/validate_api_docs.py`
3. ✅ **Write docstrings with examples** - They're automatically tested
4. ✅ **Keep examples runnable** - Use real code, not pseudocode
5. ✅ **Version everything** - Update versions and dates with each release
6. ✅ **Use CI/CD** - Let automation catch issues early
7. ✅ **Review docs in PRs** - Documentation review is as important as code review

**Tools**:

- `scripts/validate_api_docs.py` - API completeness checker
- `scripts/validate_docs.py` - Link validator
- `.github/workflows/docs.yml` - CI/CD automation
- `mkdocs serve` - Local preview
- `interrogate` - Docstring coverage

**Remember**: Good documentation is maintained alongside code, not as an afterthought!
