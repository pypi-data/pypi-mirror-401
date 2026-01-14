.PHONY: help install dev test lint format typecheck security clean docs

help:
	@echo "TraceKit Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  install     Install package"
	@echo "  dev         Install with dev dependencies + pre-commit"
	@echo "  sync        Sync dependencies with lockfile"
	@echo ""
	@echo "Quality:"
	@echo "  test        Run tests"
	@echo "  test-fast   Run tests in parallel"
	@echo "  test-cov    Run tests with coverage report"
	@echo "  lint        Run linter (ruff check)"
	@echo "  format      Format code (ruff format + fix)"
	@echo "  typecheck   Run type checker (mypy)"
	@echo "  security    Run security checks (bandit + safety)"
	@echo "  check       Run all checks (lint, typecheck, security, test)"
	@echo ""
	@echo "Testing:"
	@echo "  test-compliance  Run IEEE/JEDEC compliance tests"
	@echo "  test-benchmark   Run performance benchmarks"
	@echo "  test-unit        Run unit tests only"
	@echo "  test-integration Run integration tests only"
	@echo ""
	@echo "Other:"
	@echo "  clean       Remove build artifacts"
	@echo "  docs        Build documentation"
	@echo "  docs-serve  Serve documentation locally"

# =============================================================================
# Setup
# =============================================================================

install:
	uv pip install -e .

dev:
	uv sync --dev
	uv run pre-commit install --install-hooks

sync:
	uv sync --dev

# =============================================================================
# Quality Checks
# =============================================================================

test:
	uv run pytest tests/ -v

test-fast:
	uv run pytest tests/ -v -n auto

test-cov:
	uv run pytest tests/ -v --cov=src/tracekit --cov-report=html --cov-report=term-missing

test-unit:
	uv run pytest tests/unit/ -v

test-integration:
	uv run pytest tests/integration/ -v

test-compliance:
	uv run pytest tests/compliance/ -v -m compliance

test-benchmark:
	uv run pytest tests/performance/ -v -m benchmark --benchmark-only

lint:
	uv run ruff check src/ tests/

format:
	uv run ruff format src/ tests/
	uv run ruff check --fix src/ tests/

typecheck:
	uv run mypy src/

security:
	uv run bandit -c pyproject.toml -r src/
	uv run safety check || true

check: lint typecheck security test

# =============================================================================
# Documentation
# =============================================================================

docs:
	uv run mkdocs build

docs-serve:
	uv run mkdocs serve

# =============================================================================
# Cleanup
# =============================================================================

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf site/
	rm -rf .coverage coverage.xml
	rm -rf benchmark.json
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

# =============================================================================
# Release (future)
# =============================================================================

build:
	uv build

publish-test:
	uv publish --repository testpypi

publish:
	uv publish
