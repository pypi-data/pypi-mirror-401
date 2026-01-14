#!/usr/bin/env python3
"""Run all TraceKit examples for validation.

This script runs all examples in the examples directory to verify they
execute without errors.

Usage:
    python examples/run_all_examples.py [--section SECTION] [--verbose] [--stop-on-error]

Examples:
    # Run all examples
    python examples/run_all_examples.py

    # Run only basics section
    python examples/run_all_examples.py --section 01_basics

    # Stop on first error
    python examples/run_all_examples.py --stop-on-error
"""
# mypy: disable-error-code="no-untyped-def,no-untyped-call,type-arg,attr-defined,arg-type,union-attr,call-arg,index,no-any-return,override,return-value,var-annotated,func-returns-value,unreachable,assignment,str-bytes-safe,misc,operator,call-overload"

import argparse
import subprocess
import sys
import time
from pathlib import Path

# Example sections in order
SECTIONS = [
    "01_basics",
    "02_digital_analysis",
    "03_spectral_analysis",
    "04_protocol_decoding",
    "05_advanced",
    "06_expert_api",
]

# Files to skip (not runnable examples)
SKIP_FILES = {
    "__init__.py",
    "run_all_examples.py",
    "conftest.py",
}

# Timeout per example (seconds)
EXAMPLE_TIMEOUT = 60


def find_examples(examples_dir: Path, section: str | None = None) -> list[Path]:
    """Find all example files to run."""
    examples = []

    if section:
        sections = [section]
    else:
        sections = SECTIONS

    for sec in sections:
        sec_dir = examples_dir / sec
        if not sec_dir.exists():
            continue

        for py_file in sorted(sec_dir.glob("*.py")):
            if py_file.name in SKIP_FILES:
                continue
            examples.append(py_file)

    return examples


def run_example(example_path: Path, verbose: bool = False) -> tuple[bool, str, float]:
    """Run a single example and return (success, output, duration)."""
    start_time = time.time()

    try:
        result = subprocess.run(
            [sys.executable, str(example_path)],
            check=False,
            capture_output=True,
            text=True,
            timeout=EXAMPLE_TIMEOUT,
            cwd=example_path.parent,
        )
        duration = time.time() - start_time

        if result.returncode == 0:
            return True, result.stdout, duration
        else:
            output = result.stdout + "\n" + result.stderr
            return False, output, duration

    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        return False, f"TIMEOUT after {EXAMPLE_TIMEOUT}s", duration

    except Exception as e:
        duration = time.time() - start_time
        return False, f"ERROR: {e}", duration


def run_all(
    examples_dir: Path,
    section: str | None = None,
    verbose: bool = False,
    stop_on_error: bool = False,
) -> int:
    """Run all examples and report results."""
    print("=" * 60)
    print("TraceKit Examples Runner")
    print("=" * 60)

    examples = find_examples(examples_dir, section)

    if not examples:
        print("\nNo examples found!")
        if section:
            print(f"Section '{section}' may not exist or have no examples.")
        return 1

    print(f"\nFound {len(examples)} examples to run\n")

    results = {
        "passed": [],
        "failed": [],
        "skipped": [],
    }

    for example in examples:
        rel_path = example.relative_to(examples_dir)
        print(f"Running: {rel_path} ... ", end="", flush=True)

        success, output, duration = run_example(example, verbose)

        if success:
            print(f"PASSED ({duration:.2f}s)")
            results["passed"].append((rel_path, duration))
            if verbose and output:
                print(f"  Output: {output[:200]}...")
        else:
            print(f"FAILED ({duration:.2f}s)")
            results["failed"].append((rel_path, output))
            if verbose or stop_on_error:
                print(f"  Error: {output[:500]}")

            if stop_on_error:
                print("\nStopping on first error (--stop-on-error)")
                break

    # Summary
    print("\n" + "=" * 60)
    print("Results Summary")
    print("=" * 60)
    print(f"  Passed:  {len(results['passed'])}")
    print(f"  Failed:  {len(results['failed'])}")
    print(f"  Skipped: {len(results['skipped'])}")

    total_time = sum(d for _, d in results["passed"]) + sum(
        EXAMPLE_TIMEOUT if "TIMEOUT" in o else 0.1 for _, o in results["failed"]
    )
    print(f"  Total time: {total_time:.2f}s")

    if results["failed"]:
        print("\n--- Failed Examples ---")
        for path, error in results["failed"]:
            print(f"  {path}")
            if not verbose:
                # Show brief error
                error_lines = error.strip().split("\n")
                if error_lines:
                    print(f"    {error_lines[-1][:80]}")

        return 1

    print("\nAll examples passed!")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run all TraceKit examples",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Sections available:
  01_basics          - Loading, measurements, plotting, export
  02_digital_analysis - Clock recovery, edges, bus decoding
  03_spectral_analysis - FFT, THD, SNR, spectrograms
  04_protocol_decoding - UART, SPI, I2C, CAN
  05_advanced        - NaN handling, GPU, lazy eval, ensemble
  06_expert_api      - Expert API, tuning, discovery
        """,
    )
    parser.add_argument(
        "--section",
        "-s",
        choices=SECTIONS,
        help="Run only examples in this section",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Show example output")
    parser.add_argument("--stop-on-error", "-x", action="store_true", help="Stop on first error")
    args = parser.parse_args()

    # Find examples directory
    examples_dir = Path(__file__).parent
    if examples_dir.name != "examples":
        # Running from repo root
        examples_dir = Path.cwd() / "examples"

    if not examples_dir.exists():
        print(f"ERROR: Examples directory not found: {examples_dir}")
        sys.exit(1)

    exit_code = run_all(examples_dir, args.section, args.verbose, args.stop_on_error)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
