#!/usr/bin/env python3
"""Example 04: Signal Quality Analysis.

This example demonstrates digital signal quality and integrity analysis
including noise margins, overshoot/undershoot, rise/fall times, and ringing.

Time: 20 minutes
Prerequisites: Edge detection basics

Run:
    uv run python examples/02_digital_analysis/04_signal_quality.py
"""
# mypy: disable-error-code="no-untyped-def,no-untyped-call,type-arg,attr-defined,arg-type,union-attr,call-arg,index,no-any-return,override,return-value,var-annotated,func-returns-value,unreachable,assignment,str-bytes-safe,misc,operator,call-overload"

import numpy as np

from tracekit.analyzers.digital import SignalQualityAnalyzer


def main() -> None:
    """Demonstrate signal quality analysis capabilities."""
    print("=" * 60)
    print("TraceKit Example: Signal Quality Analysis")
    print("=" * 60)

    # --- Basic Signal Quality ---
    print("\n--- Basic TTL Signal Quality ---")

    demo_basic_quality()

    # --- Overshoot and Undershoot Detection ---
    print("\n--- Overshoot/Undershoot Analysis ---")

    demo_overshoot_undershoot()

    # --- Noise Analysis ---
    print("\n--- Noise Margin Analysis ---")

    demo_noise_margins()

    # --- Rise/Fall Time Measurement ---
    print("\n--- Rise/Fall Time Measurement ---")

    demo_rise_fall_times()

    # --- Ringing Detection ---
    print("\n--- Ringing Detection ---")

    demo_ringing_detection()

    # --- Summary ---
    print("\n" + "=" * 60)
    print("Key Points:")
    print("  1. SignalQualityAnalyzer provides comprehensive analysis")
    print("  2. Supports TTL, CMOS, LVTTL, LVCMOS logic families")
    print("  3. Detects overshoot, undershoot, and ringing")
    print("  4. Measures rise/fall times and slew rates")
    print("  5. Evaluates noise margins against specifications")
    print("=" * 60)


def demo_basic_quality() -> None:
    """Demonstrate basic signal quality analysis."""
    # Generate a clean digital signal
    sample_rate = 1e9  # 1 GHz
    duration = 2e-6  # 2 microseconds

    signal = generate_clean_signal(sample_rate, duration)

    # Analyze signal quality
    analyzer = SignalQualityAnalyzer(sample_rate, logic_family="TTL")
    report = analyzer.analyze(signal)

    print("Logic Family: TTL")
    print(f"Signal Quality Rating: {report.signal_quality.upper()}")
    print(f"SNR: {report.snr_db:.1f} dB")

    print("\nNoise Margins:")
    print(f"  High level mean: {report.noise_margins.high_mean:.3f} V")
    print(f"  High level margin: {report.noise_margins.high_margin:.3f} V")
    print(f"  Low level mean: {report.noise_margins.low_mean:.3f} V")
    print(f"  Low level margin: {report.noise_margins.low_margin:.3f} V")

    if report.issues:
        print(f"\nIssues detected: {len(report.issues)}")
        for issue in report.issues:
            print(f"  - {issue}")
    else:
        print("\nNo issues detected - signal is clean!")


def demo_overshoot_undershoot() -> None:
    """Demonstrate overshoot and undershoot detection."""
    sample_rate = 1e9  # 1 GHz
    duration = 1e-6

    # Generate signal with significant overshoot and undershoot
    signal = generate_signal_with_overshoot(
        sample_rate,
        duration,
        overshoot_pct=25,  # 25% overshoot
        undershoot_pct=15,  # 15% undershoot
    )

    analyzer = SignalQualityAnalyzer(sample_rate, logic_family="CMOS")
    report = analyzer.analyze(signal)

    print("Transition Metrics:")
    print(f"  Overshoot: {report.transitions.overshoot:.1f}%")
    print(f"  Undershoot: {report.transitions.undershoot:.1f}%")
    print(f"  Slew rate (rising): {report.transitions.slew_rate_rising / 1e9:.2f} V/ns")
    print(f"  Slew rate (falling): {abs(report.transitions.slew_rate_falling) / 1e9:.2f} V/ns")

    # Typical limits
    overshoot_limit = 10.0  # 10% typically acceptable
    undershoot_limit = 10.0

    print("\nSpecification check (max 10%):")
    print(
        f"  Overshoot: {report.transitions.overshoot:.1f}% - "
        f"{'FAIL' if report.transitions.overshoot > overshoot_limit else 'PASS'}"
    )
    print(
        f"  Undershoot: {report.transitions.undershoot:.1f}% - "
        f"{'FAIL' if report.transitions.undershoot > undershoot_limit else 'PASS'}"
    )

    if report.recommendations:
        print("\nRecommendations:")
        for rec in report.recommendations:
            print(f"  - {rec}")


def demo_noise_margins() -> None:
    """Demonstrate noise margin analysis with different noise levels."""
    sample_rate = 1e9
    duration = 2e-6

    print("Testing different noise levels:\n")

    noise_levels = [0.05, 0.1, 0.2, 0.3]  # Noise amplitude in volts

    for noise_amp in noise_levels:
        signal = generate_signal_with_noise(sample_rate, duration, noise_amplitude=noise_amp)

        analyzer = SignalQualityAnalyzer(sample_rate, logic_family="TTL")
        report = analyzer.analyze(signal)

        # TTL specs: VIH min = 2.0V, VIL max = 0.8V
        vih_min = 2.0
        vil_max = 0.8

        high_ok = report.noise_margins.high_mean - 3 * report.noise_margins.high_std > vih_min
        low_ok = report.noise_margins.low_mean + 3 * report.noise_margins.low_std < vil_max

        status = "PASS" if (high_ok and low_ok) else "FAIL"

        print(f"Noise amplitude: {noise_amp:.2f}V")
        print(
            f"  High: {report.noise_margins.high_mean:.3f}V +/- {report.noise_margins.high_std:.3f}V"
        )
        print(
            f"  Low:  {report.noise_margins.low_mean:.3f}V +/- {report.noise_margins.low_std:.3f}V"
        )
        print(f"  SNR:  {report.snr_db:.1f} dB")
        print(f"  Status: {status}")
        print()


def demo_rise_fall_times() -> None:
    """Demonstrate rise and fall time measurements."""
    sample_rate = 10e9  # 10 GHz for accurate timing
    duration = 1e-6

    # Test different rise/fall times
    edge_times = [1e-9, 2e-9, 5e-9, 10e-9]  # 1ns, 2ns, 5ns, 10ns

    print("Measuring rise/fall times at different speeds:\n")

    for edge_time in edge_times:
        signal = generate_signal_with_edge_times(
            sample_rate,
            duration,
            rise_time=edge_time,
            fall_time=edge_time * 1.2,  # Fall slightly slower than rise
        )

        analyzer = SignalQualityAnalyzer(sample_rate, logic_family="CMOS")
        report = analyzer.analyze(signal)

        print(f"Target edge time: {edge_time * 1e9:.1f} ns")
        print(f"  Measured rise time: {report.transitions.rise_time * 1e9:.2f} ns")
        print(f"  Measured fall time: {report.transitions.fall_time * 1e9:.2f} ns")
        print(f"  Rise slew rate: {report.transitions.slew_rate_rising / 1e9:.1f} V/ns")
        print(f"  Fall slew rate: {abs(report.transitions.slew_rate_falling) / 1e9:.1f} V/ns")
        print()


def demo_ringing_detection() -> None:
    """Demonstrate ringing detection on signal edges."""
    sample_rate = 5e9  # 5 GHz
    duration = 500e-9  # 500 ns

    # Generate signal with ringing
    signal = generate_signal_with_ringing(
        sample_rate,
        duration,
        ringing_freq=200e6,  # 200 MHz ringing
        ringing_amplitude=0.3,  # 0.3V ringing amplitude
        damping_factor=0.7,
    )

    analyzer = SignalQualityAnalyzer(sample_rate, logic_family="CMOS")
    report = analyzer.analyze(signal)

    print("Signal with ringing:")
    print(f"  Signal quality: {report.signal_quality.upper()}")

    if report.transitions.ringing_frequency:
        print(f"  Ringing frequency: {report.transitions.ringing_frequency / 1e6:.1f} MHz")
        print(f"  Ringing amplitude: {report.transitions.ringing_amplitude:.3f} V")
    else:
        print("  Ringing: Not detected (below threshold)")

    if report.issues:
        print("\nDetected issues:")
        for issue in report.issues:
            print(f"  - {issue}")

    if report.recommendations:
        print("\nRecommendations:")
        for rec in report.recommendations:
            print(f"  - {rec}")


# --- Helper Functions ---


def generate_clean_signal(sample_rate: float, duration: float) -> np.ndarray:
    """Generate a clean TTL-level square wave."""
    n_samples = int(sample_rate * duration)
    freq = 5e6  # 5 MHz square wave

    t = np.arange(n_samples) / sample_rate
    signal = (np.sin(2 * np.pi * freq * t) > 0).astype(float) * 3.3  # 3.3V levels

    return signal


def generate_signal_with_overshoot(
    sample_rate: float,
    duration: float,
    overshoot_pct: float = 20,
    undershoot_pct: float = 10,
) -> np.ndarray:
    """Generate signal with overshoot and undershoot on edges."""
    n_samples = int(sample_rate * duration)
    signal = np.zeros(n_samples)

    # Create transition points
    edge_samples = 50  # Samples for edge transition
    settle_samples = 100  # Samples to settle

    # Rising edge at 25% of signal
    rise_start = n_samples // 4
    rise_end = rise_start + edge_samples

    # Build rising edge with overshoot
    high_level = 3.3
    overshoot_level = high_level * (1 + overshoot_pct / 100)

    # Ramp up
    signal[rise_start:rise_end] = np.linspace(0, overshoot_level, edge_samples)
    # Overshoot decay
    decay_end = rise_end + settle_samples
    decay = np.exp(-np.arange(settle_samples) / 20) * (overshoot_level - high_level)
    signal[rise_end:decay_end] = high_level + decay
    # Steady high
    signal[decay_end : 3 * n_samples // 4] = high_level

    # Falling edge at 75% of signal
    fall_start = 3 * n_samples // 4
    fall_end = fall_start + edge_samples
    undershoot_level = -high_level * (undershoot_pct / 100)

    # Ramp down
    signal[fall_start:fall_end] = np.linspace(high_level, undershoot_level, edge_samples)
    # Undershoot recovery
    recovery_end = min(fall_end + settle_samples, n_samples)
    recovery_samples = recovery_end - fall_end
    if recovery_samples > 0:
        recovery = np.exp(-np.arange(recovery_samples) / 20) * undershoot_level
        signal[fall_end:recovery_end] = recovery
    # Rest stays at 0

    # Add small noise
    signal += np.random.randn(n_samples) * 0.02

    return signal


def generate_signal_with_noise(
    sample_rate: float,
    duration: float,
    noise_amplitude: float = 0.1,
) -> np.ndarray:
    """Generate signal with specified noise level."""
    signal = generate_clean_signal(sample_rate, duration)
    noise = np.random.randn(len(signal)) * noise_amplitude
    return signal + noise


def generate_signal_with_edge_times(
    sample_rate: float,
    duration: float,
    rise_time: float,
    fall_time: float,
) -> np.ndarray:
    """Generate signal with specified rise and fall times."""
    n_samples = int(sample_rate * duration)
    signal = np.zeros(n_samples)

    rise_samples = int(rise_time * sample_rate)
    fall_samples = int(fall_time * sample_rate)

    high_level = 3.3

    # Rising edge at 25%
    rise_start = n_samples // 4
    rise_end = rise_start + rise_samples

    # S-curve for smooth transition (10-90%)
    t_rise = np.linspace(-2, 2, rise_samples)
    sigmoid_rise = 1 / (1 + np.exp(-t_rise * 2))
    signal[rise_start:rise_end] = sigmoid_rise * high_level

    # High level
    signal[rise_end : 3 * n_samples // 4] = high_level

    # Falling edge at 75%
    fall_start = 3 * n_samples // 4
    fall_end = min(fall_start + fall_samples, n_samples)

    t_fall = np.linspace(2, -2, fall_end - fall_start)
    sigmoid_fall = 1 / (1 + np.exp(-t_fall * 2))
    signal[fall_start:fall_end] = sigmoid_fall * high_level

    # Add minimal noise
    signal += np.random.randn(n_samples) * 0.01

    return signal


def generate_signal_with_ringing(
    sample_rate: float,
    duration: float,
    ringing_freq: float,
    ringing_amplitude: float,
    damping_factor: float = 0.8,
) -> np.ndarray:
    """Generate signal with ringing on edges."""
    n_samples = int(sample_rate * duration)
    signal = np.zeros(n_samples)

    high_level = 3.3
    edge_samples = 10  # Fast edge

    # Rising edge with ringing
    rise_start = n_samples // 4
    rise_end = rise_start + edge_samples

    signal[rise_start:rise_end] = np.linspace(0, high_level, edge_samples)

    # Add damped ringing after rising edge
    ringing_duration = 100e-9  # 100 ns of ringing
    ringing_samples = int(ringing_duration * sample_rate)

    t_ring = np.arange(ringing_samples) / sample_rate
    damping = np.exp(-t_ring / (ringing_duration * (1 - damping_factor)))
    ringing = ringing_amplitude * np.sin(2 * np.pi * ringing_freq * t_ring) * damping

    ring_end = min(rise_end + ringing_samples, n_samples)
    signal[rise_end:ring_end] = high_level + ringing[: ring_end - rise_end]

    # Steady high
    signal[ring_end : 3 * n_samples // 4] = high_level

    # Falling edge with ringing
    fall_start = 3 * n_samples // 4
    fall_end = fall_start + edge_samples
    signal[fall_start:fall_end] = np.linspace(high_level, 0, edge_samples)

    # Add damped ringing after falling edge
    fall_ring_end = min(fall_end + ringing_samples, n_samples)
    if fall_ring_end > fall_end:
        t_ring2 = np.arange(fall_ring_end - fall_end) / sample_rate
        damping2 = np.exp(-t_ring2 / (ringing_duration * (1 - damping_factor)))
        ringing2 = ringing_amplitude * 0.8 * np.sin(2 * np.pi * ringing_freq * t_ring2) * damping2
        signal[fall_end:fall_ring_end] = ringing2

    return signal


if __name__ == "__main__":
    main()
