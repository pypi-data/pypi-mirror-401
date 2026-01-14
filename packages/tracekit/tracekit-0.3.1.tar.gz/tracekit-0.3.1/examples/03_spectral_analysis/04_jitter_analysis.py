#!/usr/bin/env python3
"""Example 04: Jitter Analysis.

This example demonstrates comprehensive jitter measurement including
period jitter, cycle-to-cycle jitter, and duty cycle distortion.

Time: 25 minutes
Prerequisites: FFT basics, edge detection

Run:
    uv run python examples/03_spectral_analysis/04_jitter_analysis.py
"""

import numpy as np

from tracekit.analyzers.jitter import (
    CycleJitterResult,
    DutyCycleDistortionResult,
    cycle_to_cycle_jitter,
    measure_dcd,
    period_jitter,
    tie_from_edges,
)
from tracekit.core.types import TraceMetadata, WaveformTrace


def main() -> None:
    """Demonstrate jitter analysis capabilities."""
    print("=" * 60)
    print("TraceKit Example: Jitter Analysis")
    print("=" * 60)

    # --- Period Jitter ---
    print("\n--- Period Jitter Measurement ---")

    demo_period_jitter()

    # --- Cycle-to-Cycle Jitter ---
    print("\n--- Cycle-to-Cycle Jitter ---")

    demo_c2c_jitter()

    # --- Duty Cycle Distortion ---
    print("\n--- Duty Cycle Distortion (DCD) ---")

    demo_dcd()

    # --- Time Interval Error ---
    print("\n--- Time Interval Error (TIE) ---")

    demo_tie()

    # --- Jitter Decomposition ---
    print("\n--- Jitter Components ---")

    demo_jitter_decomposition()

    # --- Summary ---
    print("\n" + "=" * 60)
    print("Key Points:")
    print("  1. Period jitter: deviation from nominal period")
    print("  2. Cycle-to-cycle jitter: period variation between adjacent cycles")
    print("  3. DCD: asymmetry between high and low times")
    print("  4. TIE: cumulative timing error (detects drift)")
    print("  5. Use appropriate jitter metric for application")
    print("=" * 60)


def demo_period_jitter() -> None:
    """Demonstrate period jitter measurement."""
    sample_rate = 10e9  # 10 GHz for accurate timing
    clock_freq = 100e6  # 100 MHz clock
    nominal_period = 1 / clock_freq

    # Generate clock with different jitter levels
    jitter_levels = [10e-12, 50e-12, 100e-12]  # 10ps, 50ps, 100ps RMS

    for jitter_rms in jitter_levels:
        # Generate periods with Gaussian jitter
        n_periods = 1000
        periods = nominal_period + np.random.randn(n_periods) * jitter_rms

        # Measure period jitter
        result: CycleJitterResult = period_jitter(periods, nominal_period=nominal_period)

        print(f"\nInjected jitter: {jitter_rms * 1e12:.0f} ps RMS")
        print("  Measured period jitter:")
        print(f"    RMS: {result.period_std * 1e12:.1f} ps")
        print(f"    Peak-to-peak: {result.c2c_pp * 1e12:.1f} ps")
        print(f"    Mean period: {result.period_mean * 1e9:.3f} ns")
        print(f"    Periods analyzed: {result.n_cycles}")


def demo_c2c_jitter() -> None:
    """Demonstrate cycle-to-cycle jitter measurement."""
    sample_rate = 10e9  # 10 GHz
    clock_freq = 100e6  # 100 MHz
    nominal_period = 1 / clock_freq

    # Generate clock with random walk (correlated) jitter
    # This type of jitter has low C2C but high period jitter
    n_periods = 1000

    # Random walk: each period error depends on previous
    random_walk_scale = 5e-12  # 5 ps step
    period_errors = np.cumsum(np.random.randn(n_periods) * random_walk_scale)

    # Add some uncorrelated jitter
    uncorrelated_jitter = np.random.randn(n_periods) * 20e-12  # 20 ps RMS

    periods = nominal_period + period_errors + uncorrelated_jitter

    # Measure both types of jitter
    c2c_result = cycle_to_cycle_jitter(periods)
    pj_result = period_jitter(periods, nominal_period=nominal_period)

    print("Clock with mixed jitter sources:")
    print("  Random walk step: 5 ps")
    print("  Uncorrelated jitter: 20 ps RMS")
    print("\nPeriod jitter (total):")
    print(f"  RMS: {pj_result.period_std * 1e12:.1f} ps")
    print(f"  Peak-to-peak: {pj_result.c2c_pp * 1e12:.1f} ps")
    print("\nCycle-to-cycle jitter:")
    print(f"  RMS: {c2c_result.c2c_rms * 1e12:.1f} ps")
    print(f"  Peak-to-peak: {c2c_result.c2c_pp * 1e12:.1f} ps")

    print("\nNote: C2C jitter is lower because it filters out low-frequency drift")


def demo_dcd() -> None:
    """Demonstrate duty cycle distortion measurement."""
    sample_rate = 10e9  # 10 GHz
    clock_freq = 50e6  # 50 MHz clock
    n_samples = int(sample_rate * 10e-6)  # 10 us of data

    t = np.arange(n_samples) / sample_rate

    # Test different duty cycles
    duty_cycles = [0.50, 0.45, 0.55, 0.40]  # 50%, 45%, 55%, 40%

    print(f"DCD measurement for {clock_freq / 1e6:.0f} MHz clock:")
    print(f"Expected period: {1 / clock_freq * 1e9:.1f} ns")

    for target_duty in duty_cycles:
        # Generate signal with specified duty cycle
        period = 1 / clock_freq
        high_time = period * target_duty

        # Create PWM signal
        signal = np.zeros(n_samples)
        for start in np.arange(0, t[-1], period):
            rise_idx = int(start * sample_rate)
            fall_idx = int((start + high_time) * sample_rate)
            if fall_idx < n_samples:
                signal[rise_idx:fall_idx] = 3.3  # 3.3V logic

        # Add small noise
        signal += np.random.randn(n_samples) * 0.02

        # Create trace
        metadata = TraceMetadata(sample_rate=sample_rate, channel_name="clock")
        trace = WaveformTrace(data=signal, metadata=metadata)

        # Measure DCD
        try:
            result: DutyCycleDistortionResult = measure_dcd(trace, clock_period=period)

            ideal_dcd = abs(target_duty - 0.5) * period
            print(f"\nTarget duty: {target_duty * 100:.0f}%")
            print(f"  Measured duty: {result.duty_cycle * 100:.1f}%")
            print(f"  DCD: {result.dcd_seconds * 1e12:.1f} ps ({result.dcd_percent:.1f}%)")
            print(f"  High time: {result.mean_high_time * 1e9:.2f} ns")
            print(f"  Low time: {result.mean_low_time * 1e9:.2f} ns")
            print(f"  Expected DCD: {ideal_dcd * 1e12:.1f} ps")
        except Exception as e:
            print(f"\nTarget duty: {target_duty * 100:.0f}%")
            print(f"  Measurement failed: {e}")


def demo_tie() -> None:
    """Demonstrate Time Interval Error analysis."""
    sample_rate = 10e9  # 10 GHz
    clock_freq = 100e6  # 100 MHz
    nominal_period = 1 / clock_freq

    # Generate edge timestamps with different jitter characteristics
    n_edges = 500

    print("Time Interval Error (TIE) analysis:")
    print("TIE shows cumulative timing deviation from ideal\n")

    # Case 1: Random jitter (bounded TIE)
    jitter = np.random.randn(n_edges) * 20e-12  # 20 ps RMS
    edges_random = np.cumsum(nominal_period + jitter * np.random.randn(n_edges))
    edges_random = np.insert(edges_random, 0, 0)

    tie_random = tie_from_edges(edges_random, nominal_period=nominal_period)

    print("Case 1: Random jitter only")
    print(f"  TIE range: {np.ptp(tie_random) * 1e12:.1f} ps")
    print(f"  TIE RMS: {np.std(tie_random) * 1e12:.1f} ps")
    print(f"  Final TIE: {tie_random[-1] * 1e12:.1f} ps")

    # Case 2: Frequency offset (unbounded TIE)
    freq_offset = 100  # 100 ppm offset
    actual_period = nominal_period * (1 + freq_offset / 1e6)
    edges_offset = np.cumsum(np.full(n_edges, actual_period))
    edges_offset = np.insert(edges_offset, 0, 0)

    tie_offset = tie_from_edges(edges_offset, nominal_period=nominal_period)

    print(f"\nCase 2: Frequency offset ({freq_offset} ppm)")
    print(f"  TIE range: {np.ptp(tie_offset) * 1e9:.1f} ns")
    print(f"  TIE drift rate: {(tie_offset[-1] - tie_offset[0]) / n_edges * 1e12:.2f} ps/cycle")
    print(f"  Final TIE: {tie_offset[-1] * 1e9:.2f} ns")

    # Case 3: Periodic jitter (bounded oscillating TIE)
    modulation_freq = 10e3  # 10 kHz modulation
    modulation_depth = 50e-12  # 50 ps peak
    t = np.arange(n_edges) * nominal_period
    periodic_jitter = modulation_depth * np.sin(2 * np.pi * modulation_freq * t)
    edges_periodic = np.cumsum(nominal_period + periodic_jitter)
    edges_periodic = np.insert(edges_periodic, 0, 0)

    tie_periodic = tie_from_edges(edges_periodic, nominal_period=nominal_period)

    print(f"\nCase 3: Periodic jitter ({modulation_freq / 1e3:.0f} kHz)")
    print(f"  TIE range: {np.ptp(tie_periodic) * 1e12:.1f} ps")
    print(f"  TIE RMS: {np.std(tie_periodic) * 1e12:.1f} ps")
    print("  Note: Bounded oscillation visible in TIE")


def demo_jitter_decomposition() -> None:
    """Demonstrate separation of jitter components."""
    sample_rate = 10e9  # 10 GHz
    clock_freq = 100e6  # 100 MHz
    nominal_period = 1 / clock_freq

    n_periods = 2000

    # Create signal with multiple jitter components
    # 1. Random jitter (RJ) - Gaussian
    rj_rms = 15e-12  # 15 ps RMS
    rj = np.random.randn(n_periods) * rj_rms

    # 2. Deterministic periodic jitter (PJ) - sinusoidal
    pj_freq = 10e3  # 10 kHz
    pj_amplitude = 30e-12  # 30 ps peak
    t = np.arange(n_periods) * nominal_period
    pj = pj_amplitude * np.sin(2 * np.pi * pj_freq * t)

    # 3. Data-dependent jitter (DDJ) - pattern dependent
    # Simulate with alternating pattern effect
    ddj_amplitude = 20e-12  # 20 ps
    ddj = ddj_amplitude * (np.arange(n_periods) % 2 - 0.5) * 2

    # Combined jitter
    total_jitter = rj + pj + ddj
    periods = nominal_period + total_jitter

    # Measure overall jitter
    c2c_result = cycle_to_cycle_jitter(periods)
    pj_result = period_jitter(periods, nominal_period=nominal_period)

    print("Jitter decomposition analysis:")
    print("-" * 40)
    print("\nInjected components:")
    print(f"  Random jitter (RJ): {rj_rms * 1e12:.0f} ps RMS")
    print(f"  Periodic jitter (PJ): {pj_amplitude * 1e12:.0f} ps peak at {pj_freq / 1e3:.0f} kHz")
    print(f"  Data-dependent jitter (DDJ): {ddj_amplitude * 1e12:.0f} ps")

    # Calculate expected totals
    # Total jitter approximately: sqrt(RJ^2 + (PJ/sqrt(2))^2 + DDJ^2)
    expected_rms = np.sqrt(rj_rms**2 + (pj_amplitude / np.sqrt(2)) ** 2 + ddj_amplitude**2)

    print(f"\nExpected total RMS: {expected_rms * 1e12:.1f} ps")
    print(f"Measured period jitter RMS: {pj_result.period_std * 1e12:.1f} ps")
    print(f"Measured C2C jitter RMS: {c2c_result.c2c_rms * 1e12:.1f} ps")

    # Spectral analysis of periods can reveal periodic components
    from scipy import fft

    # Analyze period variations
    period_variations = periods - nominal_period
    freqs = fft.rfftfreq(n_periods, nominal_period)
    spectrum = np.abs(fft.rfft(period_variations)) / n_periods

    # Find peak at PJ frequency
    pj_bin = np.argmin(np.abs(freqs - pj_freq))
    measured_pj_amplitude = spectrum[pj_bin] * 2  # Convert to peak

    print("\nSpectral analysis:")
    print(f"  Detected PJ at {freqs[pj_bin] / 1e3:.1f} kHz")
    print(f"  Measured PJ amplitude: {measured_pj_amplitude * 1e12:.1f} ps")
    print(f"  Expected PJ amplitude: {pj_amplitude * 1e12:.0f} ps")


if __name__ == "__main__":
    main()
