#!/bin/bash
# TraceKit v0.3.0 PyPI Publishing Script
# Run this after setting up credentials in ~/.pypirc

set -e

echo "🚀 TraceKit v0.3.0 PyPI Publishing"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if .pypirc exists
if [ ! -f ~/.pypirc ]; then
    echo -e "${RED}❌ Error: ~/.pypirc not found${NC}"
    echo ""
    echo "Please create ~/.pypirc with your API tokens."
    echo "See: /tmp/pypi-upload-instructions.md"
    exit 1
fi

# Check dist files exist
if [ ! -f dist/tracekit-0.3.0.tar.gz ] || [ ! -f dist/tracekit-0.3.0-py3-none-any.whl ]; then
    echo -e "${RED}❌ Error: Distribution files not found${NC}"
    echo "Run: uv build"
    exit 1
fi

echo "✅ Found distribution files"
echo ""

# Step 1: Upload to TestPyPI
echo -e "${YELLOW}Step 1: Uploading to TestPyPI...${NC}"
uv run twine upload --repository testpypi dist/tracekit-0.3.0*

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Successfully uploaded to TestPyPI${NC}"
    echo ""
    echo "View at: https://test.pypi.org/project/tracekit/0.3.0/"
    echo ""
else
    echo -e "${RED}❌ TestPyPI upload failed${NC}"
    exit 1
fi

# Step 2: Test installation from TestPyPI
echo -e "${YELLOW}Step 2: Testing installation from TestPyPI...${NC}"
echo "This will test install in a temporary environment"
read -p "Press Enter to continue or Ctrl+C to abort..."

# Create temp venv for testing
TEMP_VENV=$(mktemp -d)/test-install
python3 -m venv "$TEMP_VENV"
source "$TEMP_VENV/bin/activate"

pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple tracekit==0.3.0

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Test installation successful${NC}"
    python -c "import tracekit; print(f'TraceKit version: {tracekit.__version__}')"
    deactivate
    rm -rf "$(dirname $TEMP_VENV)"
else
    echo -e "${RED}❌ Test installation failed${NC}"
    deactivate
    rm -rf "$(dirname $TEMP_VENV)"
    exit 1
fi

echo ""
echo -e "${YELLOW}Step 3: Ready to upload to production PyPI${NC}"
echo "⚠️  This will publish TraceKit v0.3.0 to the public PyPI."
echo ""
read -p "Are you sure you want to proceed? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 0
fi

echo ""
echo -e "${YELLOW}Uploading to production PyPI...${NC}"
uv run twine upload dist/tracekit-0.3.0*

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 Successfully published TraceKit v0.3.0 to PyPI!${NC}"
    echo ""
    echo "📦 Package: https://pypi.org/project/tracekit/0.3.0/"
    echo "📚 GitHub: https://github.com/lair-click-bats/tracekit/releases/tag/v0.3.0"
    echo ""
    echo "Install with: pip install tracekit==0.3.0"
else
    echo -e "${RED}❌ Production PyPI upload failed${NC}"
    exit 1
fi
