#!/usr/bin/env bash
# =============================================================================
# format_markdown.sh - Markdown Formatter
# =============================================================================
# Formats and lints markdown files using prettier and markdownlint
# Usage: ./scripts/format_markdown.sh [--check] [--fix] [path]
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# shellcheck source=lib/common.sh
source "${SCRIPT_DIR}/lib/common.sh"

# Defaults
MODE="format" # format, check, fix
TARGET=""

# =============================================================================
# Argument Parsing
# =============================================================================

while [[ $# -gt 0 ]]; do
  case $1 in
    --check)
      MODE="check"
      shift
      ;;
    --fix)
      MODE="fix"
      shift
      ;;
    --format)
      MODE="format"
      shift
      ;;
    -h | --help)
      echo "Usage: $0 [OPTIONS] [path]"
      echo ""
      echo "Formats and lints markdown files"
      echo ""
      echo "Options:"
      echo "  --check     Check formatting without modifying files"
      echo "  --fix       Fix formatting and lint issues"
      echo "  --format    Run formatting only (default)"
      echo "  -h, --help  Show this help message"
      echo ""
      echo "Path:"
      echo "  Optional path to file or directory (default: entire repo)"
      echo ""
      echo "Examples:"
      echo "  $0                     # Format all markdown files"
      echo "  $0 --check             # Check all files without modifying"
      echo "  $0 --fix README.md     # Fix specific file"
      exit 0
      ;;
    -*)
      echo "Unknown option: $1" >&2
      exit 2
      ;;
    *)
      TARGET="$1"
      shift
      ;;
  esac
done

# Default target
if [[ -z "${TARGET}" ]]; then
  TARGET="${REPO_ROOT}"
fi

# Make target absolute
if [[ ! "${TARGET}" = /* ]]; then
  TARGET="${REPO_ROOT}/${TARGET}"
fi

# =============================================================================
# Main Execution
# =============================================================================

print_header "Markdown Formatter"

case ${MODE} in
  check)
    print_section "Checking markdown formatting"

    # Run prettier check
    "${SCRIPT_DIR}/tools/prettier.sh" --check --md-only "${TARGET}" || exit_code=1

    # Run markdownlint check
    "${SCRIPT_DIR}/tools/markdownlint.sh" --check "${TARGET}" || exit_code=1
    ;;
  format)
    print_section "Formatting markdown"
    "${SCRIPT_DIR}/tools/prettier.sh" --fix --md-only "${TARGET}"
    ;;
  fix)
    print_section "Fixing markdown formatting and lint issues"
    "${SCRIPT_DIR}/tools/prettier.sh" --fix --md-only "${TARGET}"
    "${SCRIPT_DIR}/tools/markdownlint.sh" --fix "${TARGET}"
    ;;
esac

exit "${exit_code:-0}"
