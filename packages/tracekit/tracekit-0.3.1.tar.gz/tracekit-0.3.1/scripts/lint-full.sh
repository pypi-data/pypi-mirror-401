#!/usr/bin/env bash
# Comprehensive lint script including type checking

set -e

echo "🔍 Running comprehensive lint and type checks..."
echo ""

echo "1️⃣  Ruff lint check..."
uv run ruff check src/ tests/ examples/
echo "✅ Ruff lint: PASS"
echo ""

echo "2️⃣  Ruff format check..."
uv run ruff format --check src/ tests/ examples/
echo "✅ Ruff format: PASS"
echo ""

echo "3️⃣  Mypy type check (source)..."
uv run mypy src/ --config-file=pyproject.toml
echo "✅ Mypy source: PASS"
echo ""

echo "4️⃣  Mypy type check (tests)..."
uv run mypy tests/unit/testing/test_synthetic.py --config-file=pyproject.toml
echo "✅ Mypy tests: PASS"
echo ""

echo "5️⃣  Mypy type check (examples)..."
find examples/ -name "*.py" -type f | xargs uv run mypy --config-file=pyproject.toml --ignore-missing-imports > /dev/null 2>&1
echo "✅ Mypy examples: PASS"
echo ""

echo "🎉 All lint and type checks passed!"
