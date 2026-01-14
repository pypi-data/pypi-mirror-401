#!/usr/bin/env python3
"""Example 07: Batch Processing.

This example demonstrates batch processing of multiple waveform files
with parallel execution, result aggregation, and progress tracking.

Time: 20 minutes
Prerequisites: Basic TraceKit measurements

Run:
    uv run python examples/05_advanced/07_batch_processing.py
"""
# mypy: disable-error-code="no-untyped-def,no-untyped-call,type-arg,attr-defined,arg-type,union-attr,call-arg,index,no-any-return,override,return-value,var-annotated,func-returns-value,unreachable,assignment,str-bytes-safe,misc,operator,call-overload"

import tempfile
from pathlib import Path

import numpy as np

from tracekit.batch import (
    AdvancedBatchProcessor,
    BatchConfig,
    BatchLogger,
    aggregate_results,
    batch_analyze,
    get_batch_stats,
)
from tracekit.core.types import TraceMetadata, WaveformTrace


def main() -> None:
    """Demonstrate batch processing capabilities."""
    print("=" * 60)
    print("TraceKit Example: Batch Processing")
    print("=" * 60)

    # Create temporary directory for demo files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # --- Generate Test Files ---
        print("\n--- Generating Test Files ---")

        test_files = generate_test_files(temp_path)

        # --- Basic Batch Analysis ---
        print("\n--- Basic Batch Analysis ---")

        demo_basic_batch(test_files)

        # --- Advanced Batch Processing ---
        print("\n--- Advanced Batch Processing ---")

        demo_advanced_batch(test_files, temp_path)

        # --- Result Aggregation ---
        print("\n--- Result Aggregation ---")

        demo_aggregation(test_files)

        # --- Batch Statistics ---
        print("\n--- Batch Statistics ---")

        demo_batch_stats(test_files)

        # --- Checkpointing ---
        print("\n--- Checkpointing and Resume ---")

        demo_checkpointing(test_files, temp_path)

    # --- Summary ---
    print("\n" + "=" * 60)
    print("Key Points:")
    print("  1. batch_analyze() processes multiple files efficiently")
    print("  2. AdvancedBatchProcessor provides fine-grained control")
    print("  3. aggregate_results() combines per-file results")
    print("  4. Checkpointing enables resume after interruption")
    print("  5. BatchLogger tracks progress and performance")
    print("=" * 60)


def generate_test_files(output_dir: Path) -> list[Path]:
    """Generate synthetic test files for batch processing demo."""
    sample_rate = 100e6  # 100 MHz
    duration = 1e-3  # 1 ms
    n_samples = int(sample_rate * duration)

    files = []

    # Generate signals with different characteristics
    signal_configs = [
        {"name": "clean_1mhz", "freq": 1e6, "noise": 0.01},
        {"name": "clean_5mhz", "freq": 5e6, "noise": 0.01},
        {"name": "noisy_1mhz", "freq": 1e6, "noise": 0.1},
        {"name": "noisy_5mhz", "freq": 5e6, "noise": 0.1},
        {"name": "clean_10mhz", "freq": 10e6, "noise": 0.02},
        {"name": "distorted_1mhz", "freq": 1e6, "noise": 0.05},
    ]

    t = np.arange(n_samples) / sample_rate

    for config in signal_configs:
        # Generate signal
        signal = np.sin(2 * np.pi * config["freq"] * t)

        # Add harmonics for "distorted" signal
        if "distorted" in config["name"]:
            signal += 0.2 * np.sin(2 * np.pi * 2 * config["freq"] * t)
            signal += 0.1 * np.sin(2 * np.pi * 3 * config["freq"] * t)

        # Add noise
        signal += np.random.randn(n_samples) * config["noise"]

        # Save as numpy file
        file_path = output_dir / f"{config['name']}.npy"
        np.save(file_path, signal)
        files.append(file_path)

        print(f"  Created: {config['name']}.npy")

    print(f"\nGenerated {len(files)} test files")
    return files


def demo_basic_batch(files: list[Path]) -> None:
    """Demonstrate basic batch analysis."""
    print("Processing files with basic batch_analyze()...")

    # Define analysis function
    def analyze_signal(file_path: Path) -> dict:
        """Analyze a single signal file."""
        data = np.load(file_path)
        sample_rate = 100e6  # Known from generation

        metadata = TraceMetadata(sample_rate=sample_rate, channel_name=file_path.stem)
        trace = WaveformTrace(data=data, metadata=metadata)

        # Basic measurements
        import tracekit as tk

        return {
            "file": file_path.name,
            "frequency_hz": tk.frequency(trace),
            "amplitude": tk.amplitude(trace),
            "rms": tk.rms(trace),
            "thd_db": tk.thd(trace),
            "snr_db": tk.snr(trace),
        }

    # Run batch analysis
    results = batch_analyze(
        files=files,
        analyze_func=analyze_signal,
        max_workers=2,  # Parallel processing
    )

    print(f"\nBatch results ({len(results)} files):")
    print("-" * 70)
    print(f"{'File':<20} {'Freq (MHz)':>12} {'Amplitude':>10} {'THD (dB)':>10} {'SNR (dB)':>10}")
    print("-" * 70)

    for result in results:
        print(
            f"{result['file']:<20} "
            f"{result['frequency_hz'] / 1e6:>12.3f} "
            f"{result['amplitude']:>10.3f} "
            f"{result['thd_db']:>10.1f} "
            f"{result['snr_db']:>10.1f}"
        )


def demo_advanced_batch(files: list[Path], work_dir: Path) -> None:
    """Demonstrate advanced batch processing with configuration."""
    print("Using AdvancedBatchProcessor for fine-grained control...")

    # Configure batch processing
    config = BatchConfig(
        max_workers=2,
        timeout_per_file=30.0,
        retry_count=2,
        checkpoint_interval=3,  # Checkpoint every 3 files
        output_dir=work_dir / "results",
    )

    # Create processor
    processor = AdvancedBatchProcessor(config)

    # Define analysis with error handling
    def robust_analyze(file_path: Path) -> dict:
        """Analyze with error handling."""
        try:
            data = np.load(file_path)
            sample_rate = 100e6

            metadata = TraceMetadata(sample_rate=sample_rate, channel_name=file_path.stem)
            trace = WaveformTrace(data=data, metadata=metadata)

            import tracekit as tk

            return {
                "status": "success",
                "file": file_path.name,
                "frequency_hz": tk.frequency(trace),
                "rms": tk.rms(trace),
                "samples": len(data),
            }
        except Exception as e:
            return {
                "status": "error",
                "file": file_path.name,
                "error": str(e),
            }

    # Process with progress callback
    def progress_callback(completed: int, total: int, current_file: str) -> None:
        pct = completed / total * 100
        print(f"  Progress: {completed}/{total} ({pct:.0f}%) - {current_file}")

    results = processor.process(
        files=files,
        analyze_func=robust_analyze,
        progress_callback=progress_callback,
    )

    # Summary
    successful = sum(1 for r in results if r.get("status") == "success")
    failed = sum(1 for r in results if r.get("status") == "error")

    print("\nAdvanced batch complete:")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")


def demo_aggregation(files: list[Path]) -> None:
    """Demonstrate result aggregation across files."""
    print("Aggregating results across files...")

    # Analyze all files
    def analyze_for_aggregation(file_path: Path) -> dict:
        data = np.load(file_path)
        sample_rate = 100e6

        metadata = TraceMetadata(sample_rate=sample_rate, channel_name=file_path.stem)
        trace = WaveformTrace(data=data, metadata=metadata)

        import tracekit as tk

        return {
            "file": file_path.name,
            "frequency_hz": tk.frequency(trace),
            "amplitude": tk.amplitude(trace),
            "rms": tk.rms(trace),
            "thd_db": tk.thd(trace),
            "snr_db": tk.snr(trace),
        }

    results = batch_analyze(files, analyze_for_aggregation)

    # Aggregate results
    aggregated = aggregate_results(
        results,
        metrics=["frequency_hz", "amplitude", "rms", "thd_db", "snr_db"],
        group_by=None,  # Aggregate all files together
    )

    print("\nAggregated statistics:")
    print("-" * 50)

    for metric, stats in aggregated.items():
        if metric == "count":
            continue
        print(f"\n{metric}:")
        print(f"  Mean: {stats['mean']:.3f}")
        print(f"  Std:  {stats['std']:.3f}")
        print(f"  Min:  {stats['min']:.3f}")
        print(f"  Max:  {stats['max']:.3f}")

    # Group by signal type (clean vs noisy)
    def get_group(result: dict) -> str:
        if "noisy" in result["file"]:
            return "noisy"
        elif "distorted" in result["file"]:
            return "distorted"
        return "clean"

    # Add group labels
    for r in results:
        r["group"] = get_group(r)

    grouped = aggregate_results(
        results,
        metrics=["snr_db"],
        group_by="group",
    )

    print("\nSNR by signal type:")
    print("-" * 30)
    for group, stats in grouped.items():
        if isinstance(stats, dict) and "snr_db" in stats:
            print(f"  {group}: {stats['snr_db']['mean']:.1f} dB (avg)")


def demo_batch_stats(files: list[Path]) -> None:
    """Demonstrate batch performance statistics."""
    print("Collecting batch processing statistics...")

    # Use BatchLogger for detailed tracking
    logger = BatchLogger()

    def analyze_with_logging(file_path: Path) -> dict:
        import time

        start_time = time.time()

        data = np.load(file_path)
        sample_rate = 100e6

        metadata = TraceMetadata(sample_rate=sample_rate, channel_name=file_path.stem)
        trace = WaveformTrace(data=data, metadata=metadata)

        import tracekit as tk

        result = {
            "file": file_path.name,
            "frequency_hz": tk.frequency(trace),
            "rms": tk.rms(trace),
        }

        # Log file processing
        elapsed = time.time() - start_time
        logger.log_file(
            file_path=file_path,
            success=True,
            duration=elapsed,
            metrics=result,
        )

        return result

    # Process files
    results = batch_analyze(files, analyze_with_logging, max_workers=1)

    # Get statistics
    stats = get_batch_stats(logger)

    print("\nBatch Performance Statistics:")
    print("-" * 40)
    print(f"  Total files: {stats.total_files}")
    print(f"  Successful: {stats.successful}")
    print(f"  Failed: {stats.failed}")
    print(f"  Total time: {stats.total_time:.2f} s")
    print(f"  Avg time/file: {stats.avg_time_per_file:.3f} s")
    print(f"  Throughput: {stats.files_per_second:.1f} files/s")

    if stats.timing_breakdown:
        print("\nTiming breakdown:")
        for phase, duration in stats.timing_breakdown.items():
            print(f"  {phase}: {duration:.3f} s")


def demo_checkpointing(files: list[Path], work_dir: Path) -> None:
    """Demonstrate checkpointing and resume capabilities."""
    print("Demonstrating checkpointing for resumable processing...")

    checkpoint_dir = work_dir / "checkpoints"
    checkpoint_dir.mkdir(exist_ok=True)

    config = BatchConfig(
        max_workers=1,
        checkpoint_interval=2,  # Checkpoint every 2 files
        checkpoint_dir=checkpoint_dir,
    )

    processor = AdvancedBatchProcessor(config)

    def analyze_func(file_path: Path) -> dict:
        data = np.load(file_path)
        return {
            "file": file_path.name,
            "samples": len(data),
            "mean": float(np.mean(data)),
        }

    # Simulate partial processing (process only first 3 files)
    partial_files = files[:3]
    results1 = processor.process(
        files=partial_files,
        analyze_func=analyze_func,
        job_id="demo_job",
    )

    print(f"\nFirst batch: processed {len(results1)} files")
    print(f"Checkpoint saved to: {checkpoint_dir}")

    # Check if checkpoint exists
    checkpoint_files = list(checkpoint_dir.glob("*.json"))
    print(f"Checkpoint files: {len(checkpoint_files)}")

    # Resume with remaining files
    remaining_files = files[3:]

    if checkpoint_files:
        print(f"\nResuming from checkpoint with {len(remaining_files)} remaining files...")

        # In real usage, resume_batch() would load state and continue
        results2 = processor.process(
            files=remaining_files,
            analyze_func=analyze_func,
            job_id="demo_job_continued",
        )

        print(f"Second batch: processed {len(results2)} files")

        total_processed = len(results1) + len(results2)
        print(f"\nTotal processed: {total_processed} files")
    else:
        print("No checkpoint found (normal if files processed quickly)")


if __name__ == "__main__":
    main()
