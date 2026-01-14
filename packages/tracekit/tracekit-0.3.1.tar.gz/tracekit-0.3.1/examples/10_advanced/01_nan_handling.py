#!/usr/bin/env python3
"""Demonstration of NaN result handling in TraceKit.

This example shows:
1. How to detect and handle NaN results
2. How to validate signals before measurement
3. How to discover applicable measurements
4. Best practices for robust signal analysis

Run this example:
    uv run python examples/nan_handling_demo.py
"""
# mypy: disable-error-code="no-untyped-def,no-untyped-call,type-arg,attr-defined,arg-type,union-attr,call-arg,index,no-any-return,override,return-value,var-annotated,func-returns-value,unreachable,assignment,str-bytes-safe,misc,operator,call-overload"

import numpy as np

import tracekit as tk
from tracekit.analyzers.validation import (
    analyze_signal_characteristics,
    get_measurement_requirements,
    get_valid_measurements,
    is_suitable_for_frequency_measurement,
)
from tracekit.core.types import TraceMetadata, WaveformTrace


def create_sample_signals() -> dict[str, WaveformTrace]:
    """Create various signal types for demonstration."""
    sample_rate = 1e9  # 1 GS/s
    time_base = 1.0 / sample_rate

    signals = {}

    # 1. Periodic square wave (100 MHz, 50% duty cycle)
    t = np.arange(0, 1000) * time_base
    square_wave = np.where(np.sin(2 * np.pi * 100e6 * t) > 0, 3.3, 0.0)
    signals["periodic_square"] = WaveformTrace(
        data=square_wave,
        metadata=TraceMetadata(
            sample_rate=sample_rate,
            source_file="demo",
        ),
    )

    # 2. DC signal
    dc_signal = np.ones(1000) * 2.5
    signals["dc"] = WaveformTrace(
        data=dc_signal,
        metadata=TraceMetadata(
            sample_rate=sample_rate,
            source_file="demo",
        ),
    )

    # 3. Single pulse (aperiodic)
    single_pulse = np.zeros(1000)
    single_pulse[300:500] = 3.3
    signals["single_pulse"] = WaveformTrace(
        data=single_pulse,
        metadata=TraceMetadata(
            sample_rate=sample_rate,
            source_file="demo",
        ),
    )

    # 4. Sine wave (50 MHz)
    sine_wave = 1.65 + 1.65 * np.sin(2 * np.pi * 50e6 * t)
    signals["sine_wave"] = WaveformTrace(
        data=sine_wave,
        metadata=TraceMetadata(
            sample_rate=sample_rate,
            source_file="demo",
        ),
    )

    # 5. Noisy signal
    noise = np.random.randn(1000) * 0.1 + 1.65
    signals["noise"] = WaveformTrace(
        data=noise,
        metadata=TraceMetadata(
            sample_rate=sample_rate,
            source_file="demo",
        ),
    )

    return signals


def demo_basic_nan_handling() -> None:
    """Demonstrate basic NaN detection and handling."""
    print("=" * 70)
    print("DEMO 1: Basic NaN Handling")
    print("=" * 70)
    print()

    signals = create_sample_signals()
    dc_signal = signals["dc"]

    # Attempting frequency measurement on DC signal
    print("Attempting frequency measurement on DC signal...")
    freq = tk.frequency(dc_signal)

    # BAD: Don't use result without checking
    # period = 1.0 / freq  # Would crash with ZeroDivisionError!

    # GOOD: Check for NaN first
    if np.isnan(freq):
        print("  Result: NaN (measurement not applicable)")
        print("  [OK] This is expected - DC signals have no frequency")
    else:
        print(f"  Result: {freq:.3e} Hz")

    print()


def demo_signal_validation() -> None:
    """Demonstrate pre-validation before measurement."""
    print("=" * 70)
    print("DEMO 2: Signal Validation Before Measurement")
    print("=" * 70)
    print()

    signals = create_sample_signals()

    for signal_name, trace in signals.items():
        print(f"\nSignal: {signal_name}")
        print("-" * 50)

        # Check if suitable for frequency measurement
        suitable, reason = is_suitable_for_frequency_measurement(trace)

        if suitable:
            print(f"  [OK] {reason}")
            freq = tk.frequency(trace)
            print(f"  Frequency: {freq:.3e} Hz")
        else:
            print(f"  [--] {reason}")
            print("  Skipping frequency measurement")


def demo_measurement_discovery() -> None:
    """Demonstrate automatic discovery of applicable measurements."""
    print("\n" + "=" * 70)
    print("DEMO 3: Automatic Measurement Discovery")
    print("=" * 70)
    print()

    signals = create_sample_signals()

    for signal_name, trace in signals.items():
        print(f"\nSignal: {signal_name}")
        print("-" * 50)

        # Get list of valid measurements
        valid_measurements = get_valid_measurements(trace)

        print(f"  Applicable measurements ({len(valid_measurements)}):")
        for meas in valid_measurements:
            print(f"    - {meas}")

        # Apply only valid measurements
        print("\n  Results:")
        for meas_name in valid_measurements[:3]:  # Show first 3 for brevity
            func = getattr(tk, meas_name)
            result = func(trace)

            if not np.isnan(result):
                print(f"    {meas_name}: {result:.3e}")


def demo_comprehensive_analysis() -> None:
    """Demonstrate comprehensive signal characterization."""
    print("\n" + "=" * 70)
    print("DEMO 4: Comprehensive Signal Characterization")
    print("=" * 70)
    print()

    signals = create_sample_signals()

    for signal_name, trace in signals.items():
        print(f"\nSignal: {signal_name}")
        print("-" * 50)

        # Analyze characteristics
        chars = analyze_signal_characteristics(trace)

        print("  Characteristics:")
        print(f"    Signal type: {chars['signal_type']}")
        print(f"    Is periodic: {chars['is_periodic']}")
        print(f"    Has edges: {chars['has_edges']}")
        print(f"    Edge count: {chars['edge_count']}")
        print(f"      Rising: {chars['rising_edge_count']}")
        print(f"      Falling: {chars['falling_edge_count']}")

        recommended = chars["recommended_measurements"]
        print(f"\n  Recommended measurements ({len(recommended)}):")
        for meas in recommended:
            print(f"    - {meas}")


def demo_batch_processing() -> None:
    """Demonstrate robust batch processing with NaN handling."""
    print("\n" + "=" * 70)
    print("DEMO 5: Batch Processing with NaN Handling")
    print("=" * 70)
    print()

    signals = create_sample_signals()

    print("Measuring frequency across all signals...")
    print()

    successful = []
    failed = []

    for signal_name, trace in signals.items():
        freq = tk.frequency(trace)

        if np.isnan(freq):
            failed.append(signal_name)
            print(f"  [--] {signal_name:20s} - NaN (not periodic)")
        else:
            successful.append((signal_name, freq))
            print(f"  [OK] {signal_name:20s} - {freq:.3e} Hz")

    print()
    print("Summary:")
    print(f"  Successful: {len(successful)}/{len(signals)}")
    print(f"  Failed: {len(failed)}/{len(signals)}")

    if successful:
        frequencies = [f for _, f in successful]
        print("\nStatistics (successful measurements only):")
        print(f"  Mean frequency: {np.mean(frequencies):.3e} Hz")
        print(f"  Std frequency: {np.std(frequencies):.3e} Hz")


def demo_adaptive_measurement() -> None:
    """Demonstrate adaptive measurement strategy with fallbacks."""
    print("\n" + "=" * 70)
    print("DEMO 6: Adaptive Measurement Strategy")
    print("=" * 70)
    print()

    signals = create_sample_signals()
    sine_wave = signals["sine_wave"]

    print("Measuring sine wave frequency with fallback strategy...")
    print()

    # Strategy 1: Edge-based (may fail on sine wave)
    print("  Strategy 1: Edge-based method")
    freq = tk.frequency(sine_wave, method="edge")
    if not np.isnan(freq):
        print(f"    [OK] Success: {freq:.3e} Hz")
    else:
        print("    [--] Failed (NaN)")

    # Strategy 2: FFT-based (better for sine waves)
    print("  Strategy 2: FFT-based method")
    freq = tk.frequency(sine_wave, method="fft")
    if not np.isnan(freq):
        print(f"    [OK] Success: {freq:.3e} Hz")
    else:
        print("    [--] Failed (NaN)")

    print()
    print("  Recommendation: FFT method is better for sine waves")


def demo_measurement_requirements() -> None:
    """Demonstrate querying measurement requirements."""
    print("\n" + "=" * 70)
    print("DEMO 7: Understanding Measurement Requirements")
    print("=" * 70)
    print()

    measurements = ["frequency", "duty_cycle", "rise_time", "amplitude"]

    for meas_name in measurements:
        print(f"\nMeasurement: {meas_name}")
        print("-" * 50)

        reqs = get_measurement_requirements(meas_name)

        print(f"  Description: {reqs['description']}")
        print(f"  Minimum samples: {reqs['min_samples']}")
        print(f"  Required signal types: {', '.join(reqs['required_signal_types'])}")
        print(f"  Required features: {', '.join(reqs['required_features'])}")
        print("  Common NaN causes:")
        for cause in reqs["common_nan_causes"]:
            print(f"    - {cause}")


def demo_user_friendly_errors() -> None:
    """Demonstrate providing user-friendly error messages."""
    print("\n" + "=" * 70)
    print("DEMO 8: User-Friendly Error Messages")
    print("=" * 70)
    print()

    signals = create_sample_signals()

    def measure_with_feedback(trace: WaveformTrace, measurement_name: str) -> None:
        """Measure with helpful error messages."""
        # Pre-validate
        if measurement_name == "frequency":
            suitable, reason = is_suitable_for_frequency_measurement(trace)
            if not suitable:
                return None, f"Cannot measure frequency: {reason}"

        # Attempt measurement
        try:
            measurement_func = getattr(tk, measurement_name)
            result = measurement_func(trace)

            if np.isnan(result):
                # Provide specific guidance
                if measurement_name in ["frequency", "period"]:
                    msg = "Signal is not periodic. Try single-pulse measurements like pulse_width."
                elif measurement_name in ["rise_time", "fall_time"]:
                    msg = "No clear transitions detected. Check signal type and sample rate."
                elif measurement_name == "duty_cycle":
                    msg = "Requires periodic square wave. Signal may be aperiodic or DC."
                else:
                    msg = f"{measurement_name} not applicable for this signal."

                return None, msg

            return result, None

        except Exception as e:
            return None, f"Error: {e!s}"

    # Test on different signals
    test_signals = [
        ("periodic_square", "frequency"),
        ("dc", "frequency"),
        ("single_pulse", "duty_cycle"),
    ]

    for signal_name, meas_name in test_signals:
        trace = signals[signal_name]
        result, error = measure_with_feedback(trace, meas_name)

        print(f"\nSignal: {signal_name}, Measurement: {meas_name}")
        if error:
            print(f"  [--] {error}")
        else:
            print(f"  [OK] Result: {result:.3e}")


def main() -> None:
    """Run all demonstrations."""
    print()
    print("+" + "-" * 68 + "+")
    print("|" + " " * 20 + "NaN Handling Demonstrations" + " " * 21 + "|")
    print("+" + "-" * 68 + "+")
    print()

    demo_basic_nan_handling()
    demo_signal_validation()
    demo_measurement_discovery()
    demo_comprehensive_analysis()
    demo_batch_processing()
    demo_adaptive_measurement()
    demo_measurement_requirements()
    demo_user_friendly_errors()

    print("\n" + "=" * 70)
    print("All demonstrations complete!")
    print("=" * 70)
    print()
    print("Key Takeaways:")
    print("  1. Always check for NaN before using measurement results")
    print("  2. Pre-validate signals using validation functions")
    print("  3. Use get_valid_measurements() for discovery")
    print("  4. Provide user-friendly error messages in applications")
    print("  5. Use adaptive strategies with fallback methods")
    print()


if __name__ == "__main__":
    main()
