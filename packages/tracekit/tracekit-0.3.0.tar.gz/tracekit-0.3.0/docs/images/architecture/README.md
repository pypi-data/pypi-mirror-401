# Architecture Diagrams

This directory contains auto-generated architecture diagrams for TraceKit.

## ⚠️ Important: Diagrams are NOT Version Controlled

These diagrams are **generated automatically** and should **not be committed to git**. They are:

- Generated during CI/CD pipeline (docs workflow)
- Available in deployed documentation (GitHub Pages)
- Can be generated locally when needed

## 🔄 Generating Diagrams Locally

To generate diagrams on your local machine:

```bash
# Generate all architecture diagrams
uv run python scripts/generate_diagrams.py
```

This creates:

- `module-dependencies.svg` - Module dependency graph
- `classes_*.svg` - UML class diagrams per package
- `packages_*.svg` - Package structure diagrams
- `index.md` - Index page for all diagrams

## 📊 Diagram Types

### Module Dependencies (pydeps)

Shows how Python modules import each other across the codebase.

**Timeout:** 120 seconds
**Tools:** pydeps

### UML Class Diagrams (pyreverse)

Shows class inheritance and relationships within each package.

**Timeout:** 30-60 seconds per package
**Tools:** pyreverse (from pylint)

### Package Architecture (pyreverse)

Shows high-level package structure and dependencies.

**Timeout:** 90 seconds
**Tools:** pyreverse (from pylint)

## ⏱️ Generation Time

- **Quick packages** (loaders, inference): ~10-30 seconds
- **Medium packages** (reporting, analyzers): ~30-60 seconds
- **Full codebase** (top-level): ~60-120 seconds (may timeout)

**Note:** Some diagrams may timeout on large codebases - this is expected behavior. Essential diagrams still generate successfully.

## 🔧 Troubleshooting

### Timeout Issues

If diagram generation times out:

1. **Increase timeout** in `scripts/generate_diagrams.py`:

   ```python
   timeout=120  # Increase as needed
   ```

2. **Reduce complexity**:

   ```python
   "--max-bacon=1",  # Reduce dependency depth
   "--max-color-depth=1",  # Simplify diagrams
   ```

3. **Generate specific diagrams only**: Edit the `packages` list in `generate_diagrams.py`

### Missing Dependencies

If you see "not found" errors:

```bash
# Install diagram generation tools
uv sync --all-extras

# Verify installation
uv run pydeps --version
uv run pyreverse --version
```

### System Dependencies

Some systems require graphviz:

```bash
# Ubuntu/Debian
sudo apt-get install graphviz

# macOS
brew install graphviz

# Windows
choco install graphviz
```

## 📝 CI/CD Integration

Diagrams are automatically generated during documentation builds in the GitHub Actions workflow (`.github/workflows/docs.yml`).

The workflow:

1. Generates all architecture diagrams
2. Builds MkDocs documentation (includes diagrams)
3. Deploys to GitHub Pages

**Important:** Diagram generation failures don't block doc deployment - essential content is still published.

## 🎨 Customizing Diagrams

To customize diagram appearance, edit `scripts/generate_diagrams.py`:

**pydeps options:**

- `--max-bacon`: Dependency depth (1-3)
- `--cluster`: Group by package
- `--no-show`: Don't open browser

**pyreverse options:**

- `--max-color-depth`: Color complexity (1-3)
- `--only-classnames`: Simplified diagrams
- `--colorized`: Use colors

See tool documentation:

- [pydeps documentation](https://github.com/thebjorn/pydeps)
- [pyreverse documentation](https://pylint.readthedocs.io/en/latest/pyreverse.html)

---

_Last updated: 2026-01-10_
