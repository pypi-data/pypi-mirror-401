#!/usr/bin/env python3
"""Basic waveform loading example.

This example demonstrates how to load waveform data from various file formats
and inspect basic properties.

Prerequisites:
    - Python 3.12+
    - TraceKit installed (uv pip install tracekit)

Estimated time: 5 minutes

Run:
    uv run python examples/01_basics/01_load_waveform.py
"""
# mypy: disable-error-code="no-untyped-def,no-untyped-call,type-arg,attr-defined,arg-type,union-attr,call-arg,index,no-any-return,override,return-value,var-annotated,func-returns-value,unreachable,assignment,str-bytes-safe,misc,operator,call-overload"

import numpy as np

# For this demo, we'll create a simple synthetic waveform
# In real usage, you would load from oscilloscope files


def create_demo_waveform() -> None:
    """Create a simple demo waveform for demonstration purposes.

    In practice, you would load real waveform files like:
        - Tektronix .wfm files
        - Rigol .wfm files
        - CSV exports
        - VCD logic analyzer captures

    Returns:
        dict: Waveform data with metadata
    """
    # Generate 1ms of data at 1 MHz sample rate
    sample_rate = 1e6  # 1 MHz
    duration = 1e-3  # 1 ms
    num_samples = int(sample_rate * duration)

    # Create time array
    time = np.linspace(0, duration, num_samples)

    # Create a 1 kHz sine wave with 1V amplitude
    frequency = 1000  # 1 kHz
    amplitude = 1.0  # 1 V
    voltage = amplitude * np.sin(2 * np.pi * frequency * time)

    return {
        "time": time,
        "voltage": voltage,
        "sample_rate": sample_rate,
        "num_samples": num_samples,
        "duration": duration,
    }


def main() -> None:
    """Demonstrate basic waveform loading and inspection."""

    print("=" * 60)
    print("TraceKit Example: Load Waveform")
    print("=" * 60)
    print()

    # Step 1: Load (or create) waveform data
    print("Step 1: Loading waveform data...")
    waveform = create_demo_waveform()
    print("✓ Waveform loaded successfully")
    print()

    # Step 2: Inspect metadata
    print("Step 2: Inspecting waveform properties...")
    print("-" * 60)
    print(f"Sample rate:    {waveform['sample_rate'] / 1e6:.1f} MHz")
    print(f"Duration:       {waveform['duration'] * 1000:.2f} ms")
    print(f"Number of samples: {waveform['num_samples']:,}")
    print(f"Time resolution:   {1 / waveform['sample_rate'] * 1e9:.1f} ns per sample")
    print()

    # Step 3: Inspect signal characteristics
    print("Step 3: Analyzing signal characteristics...")
    print("-" * 60)
    print(f"Voltage range:  {waveform['voltage'].min():.3f} V to {waveform['voltage'].max():.3f} V")
    print(f"Peak-to-peak:   {waveform['voltage'].ptp():.3f} V")
    print(f"RMS voltage:    {np.sqrt(np.mean(waveform['voltage'] ** 2)):.3f} V")
    print(f"Mean voltage:   {waveform['voltage'].mean():.6f} V")
    print()

    # Step 4: Extract time windows
    print("Step 4: Extracting time windows...")
    print("-" * 60)

    # Get first 100 microseconds
    time_window = 100e-6  # 100 μs
    window_samples = int(time_window * waveform["sample_rate"])

    time_subset = waveform["time"][:window_samples]
    voltage_subset = waveform["voltage"][:window_samples]

    print(f"Extracted first {time_window * 1e6:.0f} μs")
    print(f"  Samples in window: {len(voltage_subset)}")
    print(f"  Time range: {time_subset[0]:.6f} s to {time_subset[-1]:.6f} s")
    print(f"  Voltage range: {voltage_subset.min():.3f} V to {voltage_subset.max():.3f} V")
    print()

    # Step 5: Sample data points
    print("Step 5: Sampling data points...")
    print("-" * 60)
    print("First 10 samples:")
    print(f"{'Index':<10} {'Time (μs)':<15} {'Voltage (V)':<15}")
    print("-" * 40)
    for i in range(10):
        print(f"{i:<10} {waveform['time'][i] * 1e6:<15.3f} {waveform['voltage'][i]:<15.6f}")
    print()

    # Summary
    print("=" * 60)
    print("Summary:")
    print("=" * 60)
    print("✓ Loaded waveform data successfully")
    print("✓ Inspected metadata (sample rate, duration, sample count)")
    print("✓ Analyzed signal characteristics (voltage range, RMS)")
    print("✓ Extracted time windows")
    print("✓ Sampled individual data points")
    print()
    print("Next steps:")
    print("  - Run 02_basic_measurements.py to perform measurements")
    print("  - Run 03_plot_waveform.py to visualize the data")
    print()
    print("In real usage, you would load files like:")
    print("  import tracekit as tk")
    print("  waveform = tk.load('oscilloscope_capture.wfm')")
    print("=" * 60)


if __name__ == "__main__":
    main()
