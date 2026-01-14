# TraceKit v0.3.0 Release Checklist

## ✅ Completed

### Code Quality

- [x] All lint checks passed (ruff: 0 errors)
- [x] All format checks passed (ruff format: 1012 files)
- [x] Type checking passed (mypy: 432 files, 0 errors)
- [x] Fixed 21 type errors across 9 automotive files
- [x] Automotive tests: 485/485 passing
- [x] No unintended test skips (4 intentional skips documented)

### Version Management

- [x] Updated pyproject.toml: 0.2.0 → 0.3.0
- [x] Updated CHANGELOG.md with v0.3.0 entry
- [x] Added automotive module section to CHANGELOG
- [x] Updated version comparison links

### Git & GitHub

- [x] Created release commit: `e1443de`
- [x] Created annotated tag: `v0.3.0`
- [x] Pushed to origin/main
- [x] Pushed tag to origin
- [x] Clean git history (no messy commits)

### Package Build

- [x] Built source distribution: `dist/tracekit-0.3.0.tar.gz`
- [x] Built wheel: `dist/tracekit-0.3.0-py3-none-any.whl`
- [x] Validated with twine check: PASSED
- [x] Verified automotive module included in package

### Documentation

- [x] Created PyPI upload instructions
- [x] Created automated publishing script
- [x] Documented all changes in CHANGELOG

## ⏳ Pending (Requires User Action)

### PyPI Publishing

- [ ] Get TestPyPI API token from https://test.pypi.org/manage/account/token/
- [ ] Get PyPI API token from https://pypi.org/manage/account/token/
- [ ] Configure `~/.pypirc` with tokens
- [ ] Upload to TestPyPI: `uv run twine upload --repository testpypi dist/tracekit-0.3.0*`
- [ ] Verify TestPyPI upload at https://test.pypi.org/project/tracekit/0.3.0/
- [ ] Test install from TestPyPI
- [ ] Upload to production PyPI: `uv run twine upload dist/tracekit-0.3.0*`
- [ ] Verify production PyPI at https://pypi.org/project/tracekit/0.3.0/

### Post-Release

- [ ] Create GitHub Release from tag v0.3.0
- [ ] Announce release (social media, mailing lists, etc.)
- [ ] Update project website (if applicable)

## Quick Commands

### Upload to TestPyPI

```bash
uv run twine upload --repository testpypi dist/tracekit-0.3.0*
```

### Upload to Production PyPI

```bash
uv run twine upload dist/tracekit-0.3.0*
```

### Or Use Automated Script

```bash
./scripts/publish-to-pypi.sh
```

## Files Ready for Upload

```
dist/
├── tracekit-0.3.0-py3-none-any.whl  (wheel, universal)
└── tracekit-0.3.0.tar.gz            (source distribution)
```

## Package Metadata

- **Name**: tracekit
- **Version**: 0.3.0
- **Release Date**: 2026-01-13
- **Python**: 3.12+
- **License**: MIT (or as specified in pyproject.toml)
- **GitHub**: https://github.com/lair-click-bats/tracekit
- **Release Tag**: v0.3.0

## What's New in v0.3.0

### Automotive CAN Bus Analysis Suite (485 tests)

Complete reverse engineering framework including:
- File loaders: BLF (Vector), ASC (Vector), MDF (ASAM), CSV
- Discovery API with confidence scoring
- State machine inference (RPNI algorithm)
- Pattern learning (counter, sequence, toggle)
- OBD-II decoder (54 PIDs)
- J1939 decoder (154 PGNs)
- UDS decoder (17 services)
- DTC database (210 codes)
- Checksum detection (XOR, SUM, CRC-8/16/32)

### Standards Compliance

- SAE J1979 (OBD-II)
- SAE J1939 (Heavy-duty vehicles)
- ISO 14229 (UDS)
- SAE J2012 (Diagnostic Trouble Codes)

## Next Steps

1. **Immediate**: Get API tokens and upload to PyPI
2. **After Upload**: Create GitHub Release
3. **Within 24h**: Announce release
4. **Ongoing**: Monitor for bug reports and user feedback

---

**Status**: All development work complete. Ready for PyPI upload pending credentials.
