#!/usr/bin/env python3
"""Demo of DSP-001 and DSP-002 functionality.

This example demonstrates multi-channel correlation and clock recovery
features implemented in TraceKit.

Requirements demonstrated:

Usage:
    uv run python examples/dsp_correlation_clock_demo.py
"""
# mypy: disable-error-code="no-untyped-def,no-untyped-call,type-arg,attr-defined,arg-type,union-attr,call-arg,index,no-any-return,override,return-value,var-annotated,func-returns-value,unreachable,assignment,str-bytes-safe,misc,operator,call-overload"

import numpy as np

# Note: This is a demonstration script. To run it, you need to have
# tracekit installed and numpy/scipy available.


def demo_correlation() -> None:
    """Demonstrate DSP-001: Multi-Channel Time Correlation."""
    print("=" * 70)
    print("DSP-001: Multi-Channel Time Correlation Demo")
    print("=" * 70)

    # Import correlation functions
    from tracekit.analyzers.digital.correlation import (
        align_by_trigger,
        correlate_channels,
        resample_to_common_rate,
    )

    # Generate synthetic test signals
    sample_rate = 1e9  # 1 GHz
    duration = 1e-6  # 1 microsecond
    n_samples = int(sample_rate * duration)
    t = np.arange(n_samples) / sample_rate

    # Channel A: 100 MHz square wave
    freq_a = 100e6
    channel_a = np.sign(np.sin(2 * np.pi * freq_a * t))

    # Channel B: Same signal with 5 ns delay
    delay_samples = 5  # 5 samples at 1 GHz = 5 ns
    channel_b = np.roll(channel_a, delay_samples)

    # Test 1: Cross-correlation
    print("\n1. Cross-Correlation Test")
    print("-" * 70)
    result = correlate_channels(channel_a, channel_b, sample_rate)
    print(f"   Detected offset: {result.offset_samples} samples")
    print(f"   Time offset: {result.offset_seconds * 1e9:.2f} ns")
    print(f"   Correlation coefficient: {result.correlation_coefficient:.4f}")
    print(f"   Confidence: {result.confidence:.4f}")
    print(f"   Quality: {result.quality}")

    # Test 2: Trigger-based alignment
    print("\n2. Trigger-Based Alignment")
    print("-" * 70)
    channels = {
        "clock": channel_a,
        "data": channel_b,
    }
    aligned = align_by_trigger(channels, trigger_channel="clock", edge="rising")
    print(f"   Aligned channels: {aligned.channel_names}")
    print(
        f"   Channel lengths: {[len(aligned.get_channel(name)) for name in aligned.channel_names]}"
    )
    print(f"   Offsets: {aligned.offsets}")

    # Test 3: Resampling to common rate
    print("\n3. Resampling to Common Rate")
    print("-" * 70)
    # Simulate different sample rates
    channels_mixed = {
        "ch1": (channel_a[::2], sample_rate / 2),  # 500 MHz
        "ch2": (channel_b, sample_rate),  # 1 GHz
    }
    resampled = resample_to_common_rate(channels_mixed, target_rate=sample_rate)
    print(f"   Target rate: {resampled.sample_rate / 1e9:.1f} GHz")
    print(f"   Resampled channels: {resampled.channel_names}")
    print(
        f"   Channel lengths: {[len(resampled.get_channel(name)) for name in resampled.channel_names]}"
    )


def demo_clock_recovery() -> None:
    """Demonstrate DSP-002: Advanced Clock Recovery."""
    print("\n" + "=" * 70)
    print("DSP-002: Advanced Clock Recovery Demo")
    print("=" * 70)

    # Import clock recovery functions
    from tracekit.analyzers.digital.clock import (
        detect_baud_rate,
        detect_clock_frequency,
        measure_clock_jitter,
        recover_clock,
    )

    # Generate synthetic test signals
    sample_rate = 1e9  # 1 GHz
    duration = 10e-6  # 10 microseconds
    n_samples = int(sample_rate * duration)
    t = np.arange(n_samples) / sample_rate

    # Test 1: Clock frequency detection
    print("\n1. Clock Frequency Detection")
    print("-" * 70)
    clock_freq = 100e6  # 100 MHz
    clock_signal = np.sign(np.sin(2 * np.pi * clock_freq * t))

    for method in ["edge", "fft", "autocorr"]:
        detected_freq = detect_clock_frequency(clock_signal, sample_rate, method=method)
        error = abs(detected_freq - clock_freq) / clock_freq * 100
        print(f"   Method '{method}': {detected_freq / 1e6:.2f} MHz (error: {error:.2f}%)")

    # Test 2: Clock recovery
    print("\n2. Clock Recovery")
    print("-" * 70)
    # Generate data signal with embedded clock
    data_freq = 50e6  # 50 MHz data rate
    data_signal = np.sign(np.sin(2 * np.pi * data_freq * t))

    for method in ["edge", "fft"]:
        recovered = recover_clock(data_signal, sample_rate, method=method)
        print(f"   Method '{method}': Recovered {len(recovered)} samples")
        print(f"   Output range: [{recovered.min():.2f}, {recovered.max():.2f}]")

    # Test 3: Baud rate detection
    print("\n3. Baud Rate Detection")
    print("-" * 70)
    # Simulate UART at 115200 baud
    baud_rate_actual = 115200
    bit_period = 1.0 / baud_rate_actual
    # Create simple UART-like signal with transitions
    uart_signal = np.zeros(n_samples)
    bit_samples = int(sample_rate * bit_period)
    for i in range(0, n_samples, bit_samples):
        if i + bit_samples < n_samples:
            uart_signal[i : i + bit_samples] = np.random.choice([0, 1])

    result = detect_baud_rate(uart_signal, sample_rate)
    print(f"   Detected baud rate: {result.baud_rate} bps")
    print(f"   Actual baud rate: {baud_rate_actual} bps")
    print(f"   Bit period: {result.bit_period_samples:.2f} samples")
    print(f"   Confidence: {result.confidence:.4f}")
    print(f"   Method: {result.method}")

    # Test 4: Jitter measurement
    print("\n4. Clock Jitter Measurement")
    print("-" * 70)
    # Add some jitter to clock
    jitter_std = 50e-12  # 50 ps RMS jitter
    jitter = np.random.normal(0, jitter_std, n_samples)
    t_jittered = t + jitter
    clock_jittered = np.sign(np.sin(2 * np.pi * clock_freq * t_jittered))

    metrics = measure_clock_jitter(clock_jittered, sample_rate)
    print(f"   Frequency: {metrics.frequency / 1e6:.2f} MHz")
    print(f"   Period: {metrics.period_seconds * 1e9:.4f} ns")
    print(f"   RMS jitter: {metrics.jitter_rms * 1e12:.2f} ps")
    print(f"   Peak-to-peak jitter: {metrics.jitter_pp * 1e12:.2f} ps")
    print(f"   Duty cycle: {metrics.duty_cycle * 100:.2f}%")
    print(f"   Stability: {metrics.stability:.4f}")
    print(f"   Confidence: {metrics.confidence:.4f}")


def main() -> None:
    """Run all demonstrations."""
    print("\n" + "=" * 70)
    print("TraceKit DSP Modules Demonstration")
    print("Requirements: DSP-001, DSP-002")
    print("=" * 70)

    try:
        demo_correlation()
        demo_clock_recovery()

        print("\n" + "=" * 70)
        print("All demonstrations completed successfully!")
        print("=" * 70 + "\n")

    except ImportError as e:
        print(f"\nError: {e}")
        print("Please ensure tracekit is installed and dependencies are available.")
        print("Install with: uv sync")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
