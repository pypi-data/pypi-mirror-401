# Documentation and Codebase Maintenance Guide

This guide covers the documentation system and codebase organization tools in TraceKit.

## Overview

TraceKit uses a comprehensive set of tools to maintain high-quality documentation and clean codebase organization:

- **Documentation**: MkDocs + mkdocstrings for auto-generated API docs
- **Code Quality**: interrogate, darglint, vulture for code health
- **Architecture**: import-linter for dependency management
- **Visualization**: pydeps, pyreverse for architecture diagrams

---

## Documentation System

### MkDocs + mkdocstrings

TraceKit uses **MkDocs** with the **Material theme** for documentation, combined with **mkdocstrings** for automatic API documentation generation from Python docstrings.

#### Key Features

1. **Single Source of Truth**: API documentation is generated directly from Google-style docstrings in source code
2. **Type Hint Integration**: Type annotations are automatically rendered in documentation
3. **Versioning**: Multiple documentation versions supported via mike plugin
4. **Image Viewing**: Enhanced image viewing with GLightbox plugin
5. **Diagrams**: Support for Mermaid diagrams in markdown

#### Configuration

All documentation settings are in `mkdocs.yml`:

```yaml
plugins:
  - mkdocstrings:
      handlers:
        python:
          options:
            docstring_style: google
            show_source: true
            show_bases: true
            show_signature_annotations: true
            merge_init_into_class: true
```

#### Building Documentation

```bash
# Build documentation locally
uv run mkdocs build

# Serve documentation with live reload
uv run mkdocs serve

# Deploy documentation to GitHub Pages
uv run mkdocs gh-deploy
```

#### Documentation Versioning

TraceKit supports multiple documentation versions using mike:

```bash
# Deploy version 0.1.0 as latest
mike deploy 0.1.0 latest --update-aliases

# Set default version
mike set-default latest

# List all versions
mike list
```

---

## Code Quality Tools

### Interrogate - Docstring Coverage

**Purpose**: Measures what percentage of the codebase has docstrings.

**Threshold**: 95% (configured in `pyproject.toml`)

```bash
# Check docstring coverage
uv run interrogate src/tracekit --fail-under=95

# Generate coverage badge
uv run interrogate src/tracekit --generate-badge docs/badges/
```

**Configuration** (`pyproject.toml`):

```toml
[tool.interrogate]
fail-under = 95
exclude = ["tests", "examples", "scripts"]
ignore-init-method = true
verbose = 2
```

### Darglint - Docstring Validation

**Purpose**: Validates that docstrings match function signatures (all parameters documented, return values match, etc.).

**Integration**: Pre-commit hook (runs automatically on commit)

```bash
# Run manually
uv run darglint src/tracekit --docstring-style=google
```

**Configuration** (`.pre-commit-config.yaml`):

```yaml
- repo: https://github.com/terrencepreilly/darglint
  rev: v1.8.1
  hooks:
    - id: darglint
      args: [--docstring-style=google, --strictness=short]
```

### Vulture - Dead Code Detection

**Purpose**: Finds unused code (variables, functions, imports).

**Confidence Threshold**: 80%

```bash
# Find dead code
uv run vulture src/tracekit --min-confidence 80
```

**Configuration** (`pyproject.toml`):

```toml
[tool.vulture]
exclude = ["tests/", "examples/", "scripts/"]
ignore_decorators = ["@pytest.fixture", "@pytest.mark.*"]
min_confidence = 80
```

**Common False Positives**:

- Exception variables in `__exit__` methods (`exc_val`, `exc_tb`)
- Callback methods (`visit_*`, test methods)
- Public API methods not used internally

---

## Architecture Tools

### Import-Linter - Dependency Management

**Purpose**: Enforces architectural constraints and prevents circular dependencies.

**Configuration**: `.importlinter`

```bash
# Check import architecture
uv run lint-imports
```

#### Configured Contracts

1. **Loaders should not import analyzers** - Loaders load data, don't analyze it
2. **Analyzers should not import loaders** - Analyzers work on data structures, not files
3. **Exporters should not import loaders** - One-way data flow
4. **No circular dependencies** - Core modules are independent
5. **Core should not import high-level modules** - Core is foundational

**Note**: Some pre-existing violations exist and are tracked as informational warnings in CI.

### Radon - Complexity Analysis

**Purpose**: Measures cyclomatic complexity and maintainability.

```bash
# Check complexity
uv run radon cc src/tracekit --min D

# Check maintainability index
uv run radon mi src/tracekit -s
```

**Complexity Ratings**:

- **A**: 1-5 (low complexity)
- **B**: 6-10 (moderate)
- **C**: 11-20 (needs attention)
- **D**: 21-30 (high complexity)
- **E**: 31-40 (very high)
- **F**: 41+ (extremely high)

---

## Architecture Visualization

### Generating Diagrams

TraceKit includes a script to automatically generate architecture diagrams:

```bash
# Generate all diagrams
uv run python scripts/generate_diagrams.py
```

This creates diagrams in `docs/images/architecture/`:

1. **module-dependencies.svg** - Module dependency graph (pydeps)
2. **packages_tracekit.svg** - Package-level UML diagram (pyreverse)
3. **classes_tracekit.svg** - Class-level UML diagram (pyreverse)
4. **classes\_{package}.svg** - Per-package class diagrams

### Tools Used

#### pydeps - Module Dependencies

Visualizes Python package dependencies:

```bash
# Generate module dependency graph
pydeps src/tracekit --max-bacon=3 --cluster -o diagram.svg
```

**Parameters**:

- `--max-bacon`: Limit dependency depth
- `--cluster`: Group by package
- `--exclude`: Exclude patterns

#### pyreverse - UML Diagrams

Part of pylint, generates UML class and package diagrams:

```bash
# Generate UML diagrams
pyreverse -o svg -p tracekit --output-directory docs/images/ src/tracekit/
```

**Output**:

- `classes_*.svg` - Class inheritance diagrams
- `packages_*.svg` - Package dependency diagrams

---

## Codebase Health Check

### Comprehensive Health Script

Run all quality checks at once:

```bash
# Run full health check
uv run python scripts/codebase_health.py
```

This script runs:

1. **Dead Code Detection** (vulture)
2. **Complexity Analysis** (radon)
3. **Test Suite Statistics**
4. **Docstring Coverage** (interrogate)
5. **Dead Fixture Detection** (pytest-deadfixtures)
6. **Duplicate Test Names**

**Example Output**:

```
TraceKit Codebase Health Check
======================================================================

✓ Dead Code Detection (vulture)
No dead code detected!

✓ Complexity Analysis (radon)
Analyzed 385 functions:
  A: 250 functions
  B: 100 functions
  C: 35 functions

✓ Test Suite Statistics
Total tests: 17,130
  unit: 15,000
  integration: 1,500
  compliance: 630

✓ Docstring Coverage (interrogate)
Coverage: 98.3%

Summary:
  ✓ PASS: Dead Code Detection
  ✓ PASS: Complexity Analysis
  ✓ PASS: Test Suite Statistics
  ✓ PASS: Docstring Coverage

Passed: 6/6

✓ All checks passed!
```

---

## CI/CD Integration

### Documentation Validation (docs.yml)

Runs on: Push to main, PRs affecting docs

**Steps**:

1. API documentation validation
2. Documentation link validation
3. Architecture diagram generation
4. MkDocs build (strict mode)
5. Docstring coverage check
6. Spell check

### Code Quality (code-quality.yml)

Runs on: Push to main, PRs affecting code

**Required Checks** (must pass):

- ✅ Docstring coverage ≥95%

**Informational Checks** (warnings only):

- ⚠️ Docstring style (pydocstyle)
- ⚠️ Dead code detection (vulture)
- ⚠️ Complexity analysis (radon)
- ⚠️ Import architecture (import-linter)

---

## Best Practices

### Documentation

1. **Always use Google-style docstrings**:

   ```python
   def analyze_signal(data: NDArray[np.float64], sample_rate: float) -> dict[str, float]:
       """Analyze signal for key metrics.

       Args:
           data: Input signal data
           sample_rate: Sample rate in Hz

       Returns:
           Dictionary of measurement name to value

       Raises:
           ValueError: If data is empty
       """
   ```

2. **Document all public API**: Keep docstring coverage ≥95%

3. **Include examples in docstrings**:

   ```python
   """
   Examples:
       >>> result = analyze_signal(data, 1e6)
       >>> result['frequency']
       1000000.0
   """
   ```

4. **Keep docs synchronized**: Run `validate_api_docs.py` regularly

### Code Organization

1. **Respect architectural boundaries**: Don't violate import-linter contracts
2. **Keep functions simple**: Target complexity rating A or B
3. **Remove dead code**: Run vulture periodically
4. **Avoid circular imports**: Use import-linter to detect

### Testing

1. **Name tests descriptively**: `test_<functionality>_<condition>_<expected>()`
2. **Check for dead fixtures**: Run pytest-deadfixtures
3. **Avoid duplicate test names**: Check codebase health report

---

## Maintenance Schedule

### Weekly

- Run `scripts/codebase_health.py`
- Check for dead code with vulture
- Review complexity warnings

### Per Release

- Generate new architecture diagrams
- Update documentation version with mike
- Run full API documentation validation
- Check import architecture

### Continuous

- Pre-commit hooks run automatically
- CI checks run on every PR
- Documentation builds on every push

---

## Troubleshooting

### MkDocs Build Fails

**Issue**: `mkdocs build` fails with import errors

**Solution**:

```bash
# Ensure all dependencies installed
uv sync --all-extras

# Check mkdocs configuration
uv run mkdocs build --strict --verbose
```

### Architecture Diagrams Don't Generate

**Issue**: `generate_diagrams.py` fails

**Common Causes**:

- Missing graphviz system package
- Circular imports in code
- Very large codebase (can be slow)

**Solution**:

```bash
# Install graphviz (Ubuntu/Debian)
sudo apt-get install graphviz

# Or macOS
brew install graphviz

# Reduce diagram complexity
pydeps src/tracekit --max-bacon=2 --exclude tests
```

### Import-Linter Failures

**Issue**: `lint-imports` reports violations

**Check violations**:

```bash
uv run lint-imports | less
```

**Common violations**:

- Core modules importing high-level modules
- Circular dependencies between packages
- Loaders importing analyzers

**Fix**:

- Refactor imports to respect architectural layers
- Move shared code to core utilities
- Use dependency injection instead of direct imports

### Interrogate Coverage Too Low

**Issue**: Docstring coverage below 95%

**Find missing docstrings**:

```bash
uv run interrogate src/tracekit -vv | grep "MISSING"
```

**Fix**: Add Google-style docstrings to flagged items

---

## Additional Resources

- [MkDocs Documentation](https://www.mkdocs.org/)
- [mkdocstrings Documentation](https://mkdocstrings.github.io/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Import Linter Documentation](https://import-linter.readthedocs.io/)

---

_Last updated: 2026-01-10_
