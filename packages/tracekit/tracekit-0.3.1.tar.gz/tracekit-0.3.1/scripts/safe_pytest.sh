#!/usr/bin/env bash
# =============================================================================
# safe_pytest.sh - Safe Test Wrapper for TraceKit
# =============================================================================
# This script sets safe environment variables and resource limits before
# running pytest, preventing crashes in terminal/Claude Code contexts.
#
# USAGE:
#   ./scripts/safe_pytest.sh              # Run all unit tests
#   ./scripts/safe_pytest.sh tests/unit   # Run specific path
#   ./scripts/safe_pytest.sh -v -x        # Pass pytest options
#
# PROBLEM HISTORY:
#   - pytest-xdist options in pyproject.toml caused initialization crashes
#   - Duplicate pytest_addoption hooks caused argument parsing failures
#   - Fork bombs from pytest.main() in test files crashed terminals
#   - Memory exhaustion during large test runs caused OOM kills
#
# This wrapper applies mitigations for all known issues.
# =============================================================================

set -euo pipefail

# =============================================================================
# Color Support Detection (terminal-safe)
# =============================================================================
if [[ -t 1 ]] && [[ -n "${TERM:-}" ]] && [[ "${TERM}" != "dumb" ]]; then
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  YELLOW='\033[1;33m'
  BLUE='\033[0;34m'
  NC='\033[0m'
else
  RED='' GREEN='' YELLOW='' BLUE='' NC=''
fi

# =============================================================================
# Script Configuration
# =============================================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "${SCRIPT_DIR}")"
LOG_DIR="${PROJECT_ROOT}/.claude/hooks"
LOG_FILE="${LOG_DIR}/safe_pytest.log"

# Ensure log directory exists
mkdir -p "${LOG_DIR}"

log() {
  echo "[$(date -Iseconds)] SAFE_PYTEST: $*" >> "${LOG_FILE}"
}

info() {
  echo -e "${BLUE}INFO:${NC} $*"
}

warn() {
  echo -e "${YELLOW}WARNING:${NC} $*"
}

error() {
  echo -e "${RED}ERROR:${NC} $*"
}

success() {
  echo -e "${GREEN}SUCCESS:${NC} $*"
}

# =============================================================================
# Pre-flight Environment Audit
# =============================================================================
audit_environment() {
  log "=== Environment Audit Start ==="

  # Shell info
  local shell_name="${SHELL:-unknown}"
  local shell_version="${BASH_VERSION:-unknown}"
  log "Shell: ${shell_name} (bash ${shell_version})"

  # Terminal info
  local term="${TERM:-dumb}"
  local columns="${COLUMNS:-80}"
  local lines="${LINES:-24}"
  log "Terminal: TERM=${term}, COLUMNS=${columns}, LINES=${lines}"

  # Python/UV info
  local python_version=""
  if command -v python3 &> /dev/null; then
    python_version=$(python3 --version 2>&1)
  fi
  local uv_version=""
  if command -v uv &> /dev/null; then
    uv_version=$(uv --version 2>&1 | head -1)
  fi
  log "Python: ${python_version}"
  log "UV: ${uv_version}"

  # Memory info
  if command -v free &> /dev/null; then
    local mem_total=$(free -m | grep Mem | awk '{print $2}')
    local mem_avail=$(free -m | grep Mem | awk '{print $7}')
    log "Memory: ${mem_avail}MB available of ${mem_total}MB total"

    # Warn if memory is low
    if [[ ${mem_avail} -lt 2000 ]]; then
      warn "Low memory detected: ${mem_avail}MB available"
      warn "Consider using --maxfail=1 to stop early on failures"
    fi
  fi

  # Resource limits
  log "Resource limits:"
  log "  ulimit -n (open files): $(ulimit -n 2> /dev/null || echo 'unknown')"
  log "  ulimit -u (processes): $(ulimit -u 2> /dev/null || echo 'unknown')"
  log "  ulimit -v (virtual memory): $(ulimit -v 2> /dev/null || echo 'unknown')"
  log "  ulimit -s (stack size): $(ulimit -s 2> /dev/null || echo 'unknown')"

  log "=== Environment Audit Complete ==="
}

# =============================================================================
# Set Safe Resource Limits
# =============================================================================
set_safe_limits() {
  log "Setting safe resource limits..."

  # Increase file descriptor limit if possible (needed for many test files)
  local current_files=$(ulimit -n 2> /dev/null || echo "1024")
  if [[ ${current_files} -lt 4096 ]]; then
    ulimit -n 4096 2> /dev/null || true
    log "File descriptor limit: attempted increase to 4096"
  fi

  # Don't set memory limits - let the system handle it naturally
  # Setting hard limits can cause unexpected failures

  # Ensure stack size is reasonable (8MB is typical)
  ulimit -s 8192 2> /dev/null || true
}

# =============================================================================
# Set Safe Environment Variables
# =============================================================================
set_safe_environment() {
  log "Setting safe environment variables..."

  # Disable pytest-xdist parallel execution by default
  # (prevents accidental parallelism that could overwhelm the system)
  export PYTEST_XDIST_AUTO=0

  # Force non-interactive mode for matplotlib
  export MPLBACKEND=Agg

  # Disable interactive prompts
  export DEBIAN_FRONTEND=noninteractive

  # Set safe terminal settings
  export TERM="${TERM:-dumb}"
  export COLUMNS="${COLUMNS:-120}"
  export LINES="${LINES:-50}"

  # Disable color output if terminal doesn't support it
  if [[ "${TERM}" == "dumb" ]] || [[ ! -t 1 ]]; then
    export NO_COLOR=1
    export PYTEST_ADDOPTS="${PYTEST_ADDOPTS:-} --color=no"
  fi

  # Set Python to unbuffered mode for real-time output
  export PYTHONUNBUFFERED=1

  # Limit pytest timeout for individual tests (fallback)
  export PYTEST_TIMEOUT="${PYTEST_TIMEOUT:-60}"

  # Force UTF-8 encoding
  export PYTHONIOENCODING=utf-8
  export LC_ALL="${LC_ALL:-C.UTF-8}"
  export LANG="${LANG:-C.UTF-8}"

  # Disable warnings that clutter output
  export PYTHONWARNINGS="ignore::DeprecationWarning"

  # UV settings
  export UV_NO_PROGRESS=1 # Disable progress bars in non-interactive mode

  log "Environment variables set"
}

# =============================================================================
# Validate pytest Configuration
# =============================================================================
validate_config() {
  log "Validating pytest configuration..."

  local issues=0

  # Check for problematic pyproject.toml settings
  if [[ -f "${PROJECT_ROOT}/pyproject.toml" ]]; then
    # Check for pytest-xdist options in addopts (they cause crashes without -n)
    if grep -E "maxprocesses|max-worker-restart" "${PROJECT_ROOT}/pyproject.toml" 2> /dev/null | grep -v "^#" | grep -v "Use:" > /dev/null; then
      warn "Found pytest-xdist options in pyproject.toml addopts"
      warn "These should only be used with -n flag on command line"
      ((issues++))
    fi
  fi

  # Check for duplicate conftest hooks (pattern only checks for syntax, not semantic duplicates)
  local conftest_count=$(find "${PROJECT_ROOT}/tests" -name "conftest.py" 2> /dev/null | wc -l)
  if [[ ${conftest_count} -gt 5 ]]; then
    log "Note: Found ${conftest_count} conftest.py files"
    log "Ensure pytest_addoption and pytest_configure are only in tests/conftest.py"
  fi

  # Check for pytest.main() in test files (fork bomb risk)
  local bad_files=$(grep -r "pytest\.main\|pytest\.main(" "${PROJECT_ROOT}/tests" --include="*.py" 2> /dev/null | grep -v "# .*pytest.main" | head -5 || true)
  if [[ -n "${bad_files}" ]]; then
    warn "Found pytest.main() calls in test files (fork bomb risk):"
    echo "${bad_files}" | head -3
    warn "Remove these calls - they can cause terminal crashes"
    ((issues++))
  fi

  if [[ ${issues} -gt 0 ]]; then
    warn "Found ${issues} potential configuration issues"
    warn "See docs/TESTING_CRASH_FIX.md for details"
  else
    log "Configuration validation passed"
  fi

  return 0 # Don't fail, just warn
}

# =============================================================================
# Cleanup Function
# =============================================================================
cleanup() {
  local exit_code=$?
  log "Test run completed with exit code: ${exit_code}"

  # Force garbage collection hint (Python will handle this)
  # No need to do anything special here

  exit ${exit_code}
}

trap cleanup EXIT

# =============================================================================
# Show Help
# =============================================================================
show_help() {
  cat << 'EOF'
Safe Pytest Wrapper for TraceKit

USAGE:
    ./scripts/safe_pytest.sh [OPTIONS] [PYTEST_ARGS...]

OPTIONS:
    --audit         Run environment audit only (don't run tests)
    --no-audit      Skip environment audit
    --verbose       Show detailed environment information
    -h, --help      Show this help message

PYTEST_ARGS:
    All other arguments are passed directly to pytest.

EXAMPLES:
    ./scripts/safe_pytest.sh                    # Run all unit tests
    ./scripts/safe_pytest.sh tests/unit -v      # Run unit tests verbosely
    ./scripts/safe_pytest.sh -x --maxfail=1     # Stop on first failure
    ./scripts/safe_pytest.sh --audit            # Just audit environment

SAFETY FEATURES:
    - Sets safe resource limits (file descriptors, stack size)
    - Configures safe environment variables (MPLBACKEND, encodings)
    - Validates pytest configuration (no bad xdist options)
    - Detects low memory conditions
    - Logs all activity for debugging

LOG FILE:
    .claude/hooks/safe_pytest.log
EOF
}

# =============================================================================
# Main Execution
# =============================================================================
main() {
  local audit_only=false
  local skip_audit=false
  local verbose=false
  local pytest_args=()

  # Parse our arguments (before --)
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --audit)
        audit_only=true
        shift
        ;;
      --no-audit)
        skip_audit=true
        shift
        ;;
      --verbose)
        verbose=true
        shift
        ;;
      -h | --help)
        show_help
        exit 0
        ;;
      --)
        shift
        pytest_args+=("$@")
        break
        ;;
      *)
        pytest_args+=("$1")
        shift
        ;;
    esac
  done

  log "=========================================="
  log "Safe pytest wrapper started"
  log "Arguments: ${pytest_args[*]:-none}"
  log "=========================================="

  # Run environment audit
  if [[ "${skip_audit}" != "true" ]]; then
    audit_environment

    if [[ "${verbose}" == "true" ]]; then
      info "Environment audit written to: ${LOG_FILE}"
      tail -30 "${LOG_FILE}"
    fi
  fi

  if [[ "${audit_only}" == "true" ]]; then
    success "Environment audit complete"
    cat << EOF

Environment Summary:
  Shell: ${SHELL:-unknown} (bash ${BASH_VERSION:-unknown})
  Terminal: ${TERM:-dumb}
  Python: $(python3 --version 2>&1 || echo "not found")
  UV: $(uv --version 2>&1 | head -1 || echo "not found")
  Memory: $(free -h 2> /dev/null | grep Mem | awk '{print $7 " available"}' || echo "unknown")
  Open files limit: $(ulimit -n 2> /dev/null || echo "unknown")
  Process limit: $(ulimit -u 2> /dev/null || echo "unknown")

See ${LOG_FILE} for full details.
EOF
    exit 0
  fi

  # Set safe environment
  set_safe_limits
  set_safe_environment

  # Validate configuration
  validate_config

  # Change to project root
  cd "${PROJECT_ROOT}"

  # Default test path if none specified
  if [[ ${#pytest_args[@]} -eq 0 ]] || [[ ! "${pytest_args[0]}" =~ ^tests/ ]]; then
    # Check if first arg looks like a pytest option
    if [[ ${#pytest_args[@]} -eq 0 ]] || [[ "${pytest_args[0]}" =~ ^- ]]; then
      pytest_args=("tests/unit" "${pytest_args[@]}")
    fi
  fi

  info "Running pytest with safe environment..."
  info "Command: uv run pytest ${pytest_args[*]}"
  echo ""

  # Run pytest via uv
  # shellcheck disable=SC2086
  exec uv run pytest "${pytest_args[@]}"
}

# Run main
main "$@"
