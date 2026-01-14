# 🚀 TestPyPI Upload - Step-by-Step Instructions

## Current Status: ✅ Everything Ready Except Token

Your package is fully prepared and validated:
- ✅ Version 0.3.0 built and validated
- ✅ All quality checks passed
- ✅ Git tagged and pushed
- ✅ Scripts created for automated upload

**You just need to configure your TestPyPI token!**

---

## Quick Start (3 Steps)

### Step 1: Get Your TestPyPI Token

1. Open in browser: https://test.pypi.org/manage/account/token/
2. Click **"Add API token"**
3. Fill in:
   - **Token name**: `TraceKit Upload`
   - **Scope**: `Entire account (all projects)`
4. Click **"Add token"**
5. **Copy the token** immediately (it starts with `pypi-`)
   - You can only see it once!
   - Keep it secure

### Step 2: Configure the Token

**Option A - Automated Setup (Recommended):**

```bash
./scripts/setup-testpypi-token.sh
```

- Run the script
- Paste your token when prompted (input is hidden)
- Done!

**Option B - Manual Setup:**

```bash
# Create the file
nano ~/.pypirc

# Paste this content and replace YOUR_TOKEN with your actual token:
[distutils]
index-servers =
    testpypi

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TOKEN_HERE

# Save and secure it
chmod 600 ~/.pypirc
```

### Step 3: Upload to TestPyPI

```bash
# Verify setup is correct
./scripts/verify-pypi-setup.sh

# Upload to TestPyPI
uv run twine upload --repository testpypi dist/tracekit-0.3.0*
```

---

## Expected Upload Output

When successful, you'll see:

```
Uploading distributions to https://test.pypi.org/legacy/
Uploading tracekit-0.3.0-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Uploading tracekit-0.3.0.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

View at:
https://test.pypi.org/project/tracekit/0.3.0/
```

---

## After Upload - Verification

### 1. Check TestPyPI Page

Visit: https://test.pypi.org/project/tracekit/0.3.0/

Should show:
- ✅ Version 0.3.0
- ✅ Package description
- ✅ Download files (wheel + source)

### 2. Test Installation

Create a test environment and install from TestPyPI:

```bash
# Create temporary test environment
python3 -m venv /tmp/test-tracekit
source /tmp/test-tracekit/bin/activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple \
            tracekit==0.3.0

# Verify it works
python -c "import tracekit; print(f'✅ TraceKit {tracekit.__version__}')"

# Test automotive module
python -c "import tracekit.automotive; print('✅ Automotive module loaded')"

# Cleanup
deactivate
rm -rf /tmp/test-tracekit
```

### 3. All Good? Upload to Production PyPI!

Once TestPyPI upload is verified:

1. Get production PyPI token: https://pypi.org/manage/account/token/
2. Add to `~/.pypirc` under `[pypi]` section
3. Upload: `uv run twine upload dist/tracekit-0.3.0*`
4. Verify: https://pypi.org/project/tracekit/0.3.0/

---

## Troubleshooting

### "Invalid or non-existent authentication information"

- ❌ Token incorrect or missing
- ✅ Check token starts with `pypi-`
- ✅ Verify no extra spaces in `~/.pypirc`
- ✅ Run: `./scripts/verify-pypi-setup.sh`

### "403 Forbidden"

- ❌ Token doesn't have permission
- ✅ Regenerate token with "Entire account" scope
- ✅ Check you're logged into correct TestPyPI account

### "400 Bad Request" or "File already exists"

- ❌ Version 0.3.0 already on TestPyPI
- ✅ Delete old version from TestPyPI
- ✅ OR bump version to 0.3.1 if needed

### "Connection timeout"

- ❌ Network issue
- ✅ Check internet connection
- ✅ Try again in a few minutes

---

## Scripts Available

| Script | Purpose |
|--------|---------|
| `./scripts/setup-testpypi-token.sh` | Interactive token setup |
| `./scripts/verify-pypi-setup.sh` | Verify configuration |
| `./scripts/publish-to-pypi.sh` | Full automated upload (TestPyPI + PyPI) |

---

## Need Help?

**Check configuration:**

```bash
./scripts/verify-pypi-setup.sh
```

**View full instructions:**

```bash
cat /tmp/testpypi-setup-options.md
```

**Re-read this file:**

```bash
cat TESTPYPI_UPLOAD_INSTRUCTIONS.md
```

---

## Summary

✅ **Your package is ready**  
⏳ **Get token**: https://test.pypi.org/manage/account/token/  
⏳ **Configure**: `./scripts/setup-testpypi-token.sh`  
⏳ **Upload**: `uv run twine upload --repository testpypi dist/tracekit-0.3.0*`  
⏳ **Verify**: https://test.pypi.org/project/tracekit/0.3.0/  

Let's get TraceKit v0.3.0 published! 🎉
