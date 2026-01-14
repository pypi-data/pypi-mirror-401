#!/bin/bash
# ULTRA-ROBUST Memory-Safe Coverage Runner for TraceKit
#
# PROBLEM: Coverage instrumentation causes OOM kills even with directory-level batching
#
# SOLUTION: Run coverage file-by-file with --cov-append, ensuring no single
# batch exceeds memory limits. Accumulate results progressively.
#
# USAGE:
#   ./scripts/run_coverage_robust.sh           # Run all tests
#   ./scripts/run_coverage_robust.sh --resume  # Resume from last successful file

set -e

COVERAGE_FILE=".coverage"
REPORT_JSON="coverage-full.json"
PROGRESS_FILE=".coverage_progress"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Parse arguments
RESUME=0
if [[ "$1" == "--resume" ]]; then
  RESUME=1
fi

# Clean or resume
if [[ ${RESUME} -eq 0 ]]; then
  echo -e "${YELLOW}Starting fresh coverage run...${NC}"
  rm -f "${COVERAGE_FILE}" "${PROGRESS_FILE}" "${REPORT_JSON}"
  echo "0" > "${PROGRESS_FILE}"
else
  echo -e "${YELLOW}Resuming from previous run...${NC}"
fi

# Get all test files
mapfile -t test_files < <(find tests/unit -name "test_*.py" -type f | sort)
total_files=${#test_files[@]}
start_index=$(cat "${PROGRESS_FILE}" 2> /dev/null || echo "0")

echo -e "${GREEN}Total test files: ${total_files}${NC}"
echo -e "${GREEN}Starting from file: ${start_index}${NC}"
echo ""

failed_files=()
passed_count=0
failed_count=0
skipped_count=0

# Process each file
for ((i = start_index; i < total_files; i++)); do
  test_file="${test_files[${i}]}"
  file_num=$((i + 1))

  echo -e "${GREEN}[${file_num}/${total_files}] Processing: ${test_file}${NC}"

  # Run with --cov-append, ignore coverage threshold
  if uv run pytest "${test_file}" \
    --cov=tracekit \
    --cov-append \
    --cov-report= \
    --timeout=0 \
    --tb=line \
    -q \
    --no-cov-on-fail 2>&1 | tee /tmp/pytest_output.txt; then

    # Extract stats
    stats=$(grep -E "passed|failed|skipped" /tmp/pytest_output.txt | tail -1 || echo "")
    echo "  Result: ${stats}"

    # Parse counts
    p=$(echo "${stats}" | grep -oP '\d+(?= passed)' || echo "0")
    f=$(echo "${stats}" | grep -oP '\d+(?= failed)' || echo "0")
    s=$(echo "${stats}" | grep -oP '\d+(?= skipped)' || echo "0")

    passed_count=$((passed_count + p))
    failed_count=$((failed_count + f))
    skipped_count=$((skipped_count + s))
  else
    exit_code=$?
    if [[ ${exit_code} -eq 144 ]]; then
      echo -e "${RED}  ERROR: OOM KILL (exit 144)${NC}"
      echo -e "${RED}  This file is too large to run with coverage!${NC}"
      failed_files+=("${test_file} (OOM)")
    else
      echo -e "${YELLOW}  Warning: Non-zero exit (${exit_code})${NC}"
    fi
  fi

  # Update progress
  echo "$((i + 1))" > "${PROGRESS_FILE}"

  # Memory cleanup delay
  sleep 1

  echo ""
done

echo -e "\n${GREEN}=== Coverage Collection Complete ===${NC}"
echo "Passed:  ${passed_count}"
echo "Failed:  ${failed_count}"
echo "Skipped: ${skipped_count}"

if [[ ${#failed_files[@]} -gt 0 ]]; then
  echo -e "\n${RED}Files that caused OOM:${NC}"
  printf '%s\n' "${failed_files[@]}"
fi

# Generate final report
echo -e "\n${GREEN}=== Generating Final Coverage Report ===${NC}"
uv run coverage report --precision=2 | tee coverage_summary.txt
uv run coverage json -o "${REPORT_JSON}"

# Extract metrics
python3 << 'PYTHON'
import json
data = json.load(open("coverage-full.json"))
total = data["totals"]
print(f"\n{'='*60}")
print(f"Total Statements:  {total['num_statements']:,}")
print(f"Covered:           {total['covered_lines']:,}")
print(f"Missing:           {total['missing_lines']:,}")
print(f"Coverage:          {total['percent_covered']:.2f}%")
print(f"{'='*60}")

if total['percent_covered'] >= 80.0:
    print("\n✓ SUCCESS: Reached 80% coverage target!")
else:
    remaining = 80.0 - total['percent_covered']
    lines_needed = int((total['num_statements'] * 0.80) - total['covered_lines'])
    print(f"\n⚠  Need {remaining:.1f}% more coverage ({lines_needed:,} more lines)")
PYTHON

echo -e "\n${GREEN}Done!${NC}"
rm -f "${PROGRESS_FILE}"
