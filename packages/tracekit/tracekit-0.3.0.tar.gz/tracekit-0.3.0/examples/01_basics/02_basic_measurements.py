#!/usr/bin/env python3
"""Example 02: Basic Measurements.

This example demonstrates fundamental waveform measurements
including frequency, amplitude, and timing measurements.

Time: 10 minutes
Prerequisites: Example 01 (loading data)

Run:
    uv run python examples/01_basics/02_basic_measurements.py
"""
# mypy: disable-error-code="no-untyped-def,no-untyped-call,type-arg,attr-defined,arg-type,union-attr,call-arg,index,no-any-return,override,return-value,var-annotated,func-returns-value,unreachable,assignment,str-bytes-safe,misc,operator,call-overload"

import math

import tracekit as tk
from tracekit.testing import generate_dc, generate_sine_wave, generate_square_wave


def main() -> None:
    """Demonstrate basic measurements."""
    print("=" * 60)
    print("TraceKit Example: Basic Measurements")
    print("=" * 60)

    # --- Generate Test Signals ---
    print("\n--- Generating Test Signals ---")

    # 1 MHz sine wave
    sine = generate_sine_wave(
        frequency=1e6,
        amplitude=2.0,  # 2V peak amplitude (4V peak-to-peak)
        sample_rate=100e6,
        duration=20e-6,
    )
    print("Generated 1 MHz sine wave")

    # 500 kHz square wave with 30% duty cycle
    square = generate_square_wave(
        frequency=500e3,
        duty_cycle=0.3,
        sample_rate=100e6,
        duration=20e-6,
    )
    print("Generated 500 kHz square wave (30% duty cycle)")

    # --- Frequency Measurements ---
    print("\n--- Frequency Measurements ---")

    sine_freq = tk.frequency(sine)
    sine_period = tk.period(sine)

    print("Sine wave:")
    print(f"  Frequency: {sine_freq / 1e6:.6f} MHz (expected: 1.000000 MHz)")
    print(f"  Period: {sine_period * 1e9:.1f} ns (expected: 1000.0 ns)")

    square_freq = tk.frequency(square)
    print("\nSquare wave:")
    print(f"  Frequency: {square_freq / 1e3:.3f} kHz (expected: 500.000 kHz)")

    # --- Amplitude Measurements ---
    print("\n--- Amplitude Measurements ---")

    amp = tk.amplitude(sine)
    rms_val = tk.rms(sine)

    print("Sine wave:")
    print(f"  Peak-to-peak amplitude: {amp:.3f} V (expected: ~4.0 V)")
    print(f"  RMS voltage: {rms_val:.3f} V (expected: ~1.414 V)")

    # Complete statistics using basic_stats
    stats = tk.basic_stats(sine)
    print("\nComplete statistics:")
    print(f"  Minimum: {stats['min']:.3f} V")
    print(f"  Maximum: {stats['max']:.3f} V")
    print(f"  Mean (DC): {stats['mean']:.3f} V")
    print(f"  Range (Vpp): {stats['range']:.3f} V")

    # --- Duty Cycle ---
    print("\n--- Duty Cycle Measurement ---")

    duty = tk.duty_cycle(square)
    print(f"Square wave duty cycle: {duty * 100:.1f}% (expected: 30.0%)")

    # --- Edge Detection ---
    print("\n--- Edge Detection ---")

    # Use find_rising_edges and find_falling_edges from triggering
    rising = tk.find_rising_edges(square)
    falling = tk.find_falling_edges(square)

    print("Square wave edges detected:")
    print(f"  Total edges: {len(rising) + len(falling)}")
    print(f"  Rising edges: {len(rising)}")
    print(f"  Falling edges: {len(falling)}")

    # First few edges
    print("\n  First 5 rising edge times:")
    for i, edge_time in enumerate(rising[:5]):
        print(f"    {i + 1}. {edge_time * 1e6:.3f} us")

    # --- Handling NaN Results ---
    print("\n--- Handling NaN Results ---")

    # Generate DC signal (will return NaN for frequency)
    dc_signal = generate_dc(level=1.5, sample_rate=100e6, duration=10e-6)

    dc_freq = tk.frequency(dc_signal)
    if math.isnan(dc_freq):
        print("DC signal frequency: NaN (expected - DC has no frequency)")
    else:
        print(f"DC signal frequency: {dc_freq}")

    # Safe measurement pattern
    def safe_measure_frequency(trace, default=0.0) -> None:
        """Measure frequency with default fallback."""
        freq = tk.frequency(trace)
        return default if math.isnan(freq) else freq

    safe_freq = safe_measure_frequency(dc_signal, default=0.0)
    print(f"Safe measurement result: {safe_freq}")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("Key Points:")
    print("  1. tk.frequency(trace) returns frequency in Hz")
    print("  2. tk.amplitude(trace) returns peak-to-peak voltage")
    print("  3. tk.basic_stats(trace) gives complete statistics")
    print("  4. tk.find_rising_edges(trace) returns edge times in seconds")
    print("  5. Check for NaN when signal may not match measurement")
    print("=" * 60)


if __name__ == "__main__":
    main()
