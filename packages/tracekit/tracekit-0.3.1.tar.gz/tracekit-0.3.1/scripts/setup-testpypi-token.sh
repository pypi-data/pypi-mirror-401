#!/bin/bash
# Setup TestPyPI credentials for TraceKit upload

set -e

echo "🔐 TestPyPI Token Setup for TraceKit"
echo "====================================="
echo ""

# Check if .pypirc already exists
if [ -f ~/.pypirc ]; then
    echo "⚠️  ~/.pypirc already exists"
    read -p "Do you want to back it up and create a new one? (yes/no): " backup
    if [ "$backup" == "yes" ]; then
        cp ~/.pypirc ~/.pypirc.backup."$(date +%s)"
        echo "✅ Backed up to ~/.pypirc.backup.*"
    else
        echo "Aborted. Please edit ~/.pypirc manually."
        exit 0
    fi
fi

echo ""
echo "Please paste your TestPyPI token below."
echo "It should start with 'pypi-'"
echo ""
read -s -p "TestPyPI Token: " TESTPYPI_TOKEN
echo ""

# Validate token format
if [[ ! $TESTPYPI_TOKEN =~ ^pypi- ]]; then
    echo "❌ Error: Token should start with 'pypi-'"
    exit 1
fi

echo ""
echo "Creating ~/.pypirc..."

cat > ~/.pypirc << PYPIRC_EOF
[distutils]
index-servers =
    testpypi
    pypi

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = $TESTPYPI_TOKEN

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = # Add your production PyPI token here when ready
PYPIRC_EOF

# Secure the file
chmod 600 ~/.pypirc

echo "✅ ~/.pypirc created and secured (permissions: 600)"
echo ""
echo "Testing configuration..."

# Test the token format
if uv run twine check dist/tracekit-0.3.0* > /dev/null 2>&1; then
    echo "✅ Package validation passed"
else
    echo "⚠️  Warning: Package validation had issues"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Upload to TestPyPI: uv run twine upload --repository testpypi dist/tracekit-0.3.0*"
echo "2. Verify upload: https://test.pypi.org/project/tracekit/0.3.0/"
echo ""
