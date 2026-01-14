#!/usr/bin/env python3
"""Analyze real Tektronix WFM captures.

This example demonstrates loading and analyzing real oscilloscope captures
from the test_data/real_captures directory.

Prerequisites:
    Run prepare_real_captures.py first to populate the real_captures directory:
    $ python scripts/prepare_real_captures.py /path/to/minimal_testset
"""
# mypy: disable-error-code="no-untyped-def,no-untyped-call,type-arg,attr-defined,arg-type,union-attr,call-arg,index,no-any-return,override,return-value,var-annotated,func-returns-value,unreachable,assignment,str-bytes-safe,misc,operator,call-overload"

from pathlib import Path

import numpy as np


def main() -> None:
    """Load and analyze real WFM captures."""
    from tracekit.loaders.tektronix import load_tektronix_wfm

    # Find real captures directory
    project_root = Path(__file__).parent.parent.parent
    real_captures = project_root / "test_data" / "real_captures" / "waveforms"

    if not real_captures.exists():
        print("Real captures not found. Run prepare_real_captures.py first.")
        print(f"Expected directory: {real_captures}")
        return

    # Find available WFM files across all size categories
    wfm_files = []
    for category in ["small", "medium", "large"]:
        cat_dir = real_captures / category
        if cat_dir.exists():
            wfm_files.extend(cat_dir.glob("*.wfm"))

    if not wfm_files:
        print("No WFM files found in real_captures directory.")
        return

    print(f"Found {len(wfm_files)} real WFM capture files\n")
    print("=" * 70)

    for wfm_file in sorted(wfm_files)[:5]:  # Analyze first 5
        print(f"\nFile: {wfm_file.name}")
        print(f"Size: {wfm_file.stat().st_size / 1024:.1f} KB")
        print("-" * 40)

        try:
            # Load the waveform
            trace = load_tektronix_wfm(wfm_file)

            # Basic info
            print(f"  Samples: {len(trace.data):,}")
            if hasattr(trace.metadata, "sample_rate") and trace.metadata.sample_rate:
                sr = trace.metadata.sample_rate
                print(f"  Sample Rate: {sr / 1e6:.2f} MHz")
                duration = len(trace.data) / sr
                print(f"  Duration: {duration * 1e6:.2f} us")

            # Signal statistics
            data = trace.data
            print("\n  Statistics:")
            print(f"    Mean: {np.mean(data):.4f}")
            print(f"    Std Dev: {np.std(data):.4f}")
            print(f"    Min: {np.min(data):.4f}")
            print(f"    Max: {np.max(data):.4f}")
            print(f"    Peak-to-Peak: {np.ptp(data):.4f}")
            print(f"    RMS: {np.sqrt(np.mean(data**2)):.4f}")

            # Check for NaN/Inf
            nan_count = np.sum(np.isnan(data))
            inf_count = np.sum(np.isinf(data))
            if nan_count > 0 or inf_count > 0:
                print("\n  Warnings:")
                if nan_count > 0:
                    print(f"    Contains {nan_count} NaN values")
                if inf_count > 0:
                    print(f"    Contains {inf_count} Inf values")

        except Exception as e:
            print(f"  Error loading file: {e}")

    print("\n" + "=" * 70)
    print("\nUse these files for:")
    print("  - Integration testing with real data")
    print("  - Performance benchmarking")
    print("  - Algorithm validation")


if __name__ == "__main__":
    main()
