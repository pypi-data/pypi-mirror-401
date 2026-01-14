#!/usr/bin/env python3
"""Demonstration of Adaptive Parameter Tuning.

This example shows how to use the AdaptiveParameterTuner to automatically
configure analysis parameters based on signal characteristics.


Usage:
    uv run python examples/adaptive_parameter_tuning_demo.py
"""

import numpy as np

from tracekit.inference import (
    AdaptiveParameterTuner,
    get_adaptive_parameters,
)


def demo_spectral_tuning() -> None:
    """Demonstrate spectral parameter tuning."""
    print("=" * 70)
    print("Spectral Parameter Tuning Demo")
    print("=" * 70)

    # Create a test signal - noisy sine wave
    sample_rate = 1e6  # 1 MHz
    duration = 0.01  # 10 ms
    t = np.linspace(0, duration, int(sample_rate * duration))
    frequency = 10e3  # 10 kHz
    np.random.seed(42)
    signal = np.sin(2 * np.pi * frequency * t) + 0.1 * np.random.randn(len(t))

    # Create tuner
    tuner = AdaptiveParameterTuner(signal, sample_rate)

    # Get spectral parameters
    params = tuner.get_spectral_params()

    print("\nSignal characteristics:")
    print(f"  Samples: {len(signal)}")
    print(f"  Sample rate: {sample_rate:.0e} Hz")
    print(f"  Dominant frequency: {tuner._characteristics['dominant_freq']:.1f} Hz")
    print(f"  SNR: {tuner._characteristics['snr_db']:.1f} dB")

    print("\nTuned spectral parameters:")
    print(f"  NFFT: {params.get('nfft')}")
    print(f"  Window: {params.get('window')}")
    print(f"  Overlap: {params.get('overlap')}")
    print(
        f"  Frequency range: {params.get('freq_min', 0):.0f} - {params.get('freq_max', sample_rate / 2):.0f} Hz"
    )
    print(f"  Confidence: {params.confidence:.2f}")

    print("\nReasoning:")
    for key, reason in params.reasoning.items():
        print(f"  {key}: {reason}")


def demo_digital_tuning() -> None:
    """Demonstrate digital parameter tuning."""
    print("\n" + "=" * 70)
    print("Digital Parameter Tuning Demo")
    print("=" * 70)

    # Create a digital signal - square wave
    sample_rate = 1e6  # 1 MHz
    duration = 0.001  # 1 ms
    t = np.linspace(0, duration, int(sample_rate * duration))
    frequency = 9600  # 9600 Hz (common baud rate)
    digital_signal = np.where(np.sin(2 * np.pi * frequency * t) > 0, 3.3, 0.0)

    # Create tuner
    tuner = AdaptiveParameterTuner(digital_signal, sample_rate)

    # Get digital parameters
    params = tuner.get_digital_params()

    print("\nSignal characteristics:")
    print(f"  Likely digital: {tuner._characteristics['likely_digital']}")
    print(f"  Range: {tuner._characteristics['range']:.2f} V")

    print("\nTuned digital parameters:")
    print(f"  Threshold: {params.get('threshold'):.2f} V")
    print(f"  Threshold low: {params.get('threshold_low'):.2f} V")
    print(f"  Threshold high: {params.get('threshold_high'):.2f} V")
    print(f"  Baud rate hint: {params.get('baud_rate_hint')} baud")
    print(f"  Confidence: {params.confidence:.2f}")

    print("\nReasoning:")
    for key, reason in params.reasoning.items():
        print(f"  {key}: {reason}")


def demo_timing_tuning() -> None:
    """Demonstrate timing parameter tuning."""
    print("\n" + "=" * 70)
    print("Timing Parameter Tuning Demo")
    print("=" * 70)

    # Create periodic signal
    sample_rate = 1e6  # 1 MHz
    duration = 0.01  # 10 ms
    t = np.linspace(0, duration, int(sample_rate * duration))
    frequency = 1e3  # 1 kHz
    signal = np.sin(2 * np.pi * frequency * t)

    # Create tuner
    tuner = AdaptiveParameterTuner(signal, sample_rate)

    # Get timing parameters
    params = tuner.get_timing_params()

    print("\nSignal characteristics:")
    print(f"  Sample rate: {sample_rate:.0e} Hz")
    print(f"  Dominant frequency: {tuner._characteristics['dominant_freq']:.1f} Hz")

    print("\nTuned timing parameters:")
    print(f"  Time resolution: {params.get('time_resolution'):.2e} s")
    if params.get("expected_period") is not None:
        print(f"  Expected period: {params.get('expected_period'):.2e} s")
        print(f"  Period tolerance: {params.get('period_tolerance'):.2e} s")
    print(f"  Edge threshold: {params.get('edge_threshold'):.3f}")
    print(f"  Confidence: {params.confidence:.2f}")

    print("\nReasoning:")
    for key, reason in params.reasoning.items():
        print(f"  {key}: {reason}")


def demo_convenience_function() -> None:
    """Demonstrate convenience function usage."""
    print("\n" + "=" * 70)
    print("Convenience Function Demo")
    print("=" * 70)

    # Create test signal
    sample_rate = 1e6
    t = np.linspace(0, 0.01, int(sample_rate * 0.01))
    signal = np.sin(2 * np.pi * 5e3 * t)

    # Use convenience function for different domains
    domains = ["spectral", "digital", "timing", "jitter", "pattern"]

    print("\nUsing get_adaptive_parameters() for different domains:")
    print(f"Signal: 5 kHz sine wave, {len(signal)} samples @ {sample_rate:.0e} Hz\n")

    for domain in domains:
        params = get_adaptive_parameters(signal, sample_rate, domain)
        print(f"{domain.upper()}:")
        print(f"  Parameters: {list(params.parameters.keys())}")
        print(f"  Confidence: {params.confidence:.2f}")


def demo_multi_domain_analysis() -> None:
    """Demonstrate analyzing a signal across multiple domains."""
    print("\n" + "=" * 70)
    print("Multi-Domain Analysis Demo")
    print("=" * 70)

    # Create complex signal
    sample_rate = 1e6
    duration = 0.01
    t = np.linspace(0, duration, int(sample_rate * duration))

    # Composite signal: fundamental + harmonics + noise
    signal = (
        1.0 * np.sin(2 * np.pi * 1e3 * t)  # Fundamental
        + 0.3 * np.sin(2 * np.pi * 3e3 * t)  # 3rd harmonic
        + 0.1 * np.sin(2 * np.pi * 5e3 * t)  # 5th harmonic
        + 0.05 * np.random.randn(len(t))  # Noise
    )

    # Create tuner
    tuner = AdaptiveParameterTuner(signal, sample_rate)

    print("\nSignal characteristics:")
    print(f"  Samples: {len(signal)}")
    print(f"  Dominant frequency: {tuner._characteristics['dominant_freq']:.1f} Hz")
    print(f"  SNR: {tuner._characteristics['snr_db']:.1f} dB")
    print(f"  Likely digital: {tuner._characteristics['likely_digital']}")

    # Get parameters for all domains
    domains = {
        "Spectral": tuner.get_spectral_params(),
        "Digital": tuner.get_digital_params(),
        "Timing": tuner.get_timing_params(),
        "Jitter": tuner.get_jitter_params(),
        "Pattern": tuner.get_pattern_params(),
    }

    print("\nAuto-tuned parameters by domain:")
    for domain_name, params in domains.items():
        print(f"\n{domain_name}:")
        print(f"  Confidence: {params.confidence:.2f}")
        print("  Key parameters:")
        for key, value in list(params.parameters.items())[:3]:  # Show first 3
            if isinstance(value, float):
                print(f"    {key}: {value:.3g}")
            else:
                print(f"    {key}: {value}")


if __name__ == "__main__":
    print("\nAdaptive Parameter Tuning Demonstration\n")
    print("This demo shows how TraceKit automatically configures analysis")
    print("parameters based on signal characteristics, reducing the need")
    print("for manual parameter specification.\n")

    demo_spectral_tuning()
    demo_digital_tuning()
    demo_timing_tuning()
    demo_convenience_function()
    demo_multi_domain_analysis()

    print("\n" + "=" * 70)
    print("Demo Complete!")
    print("=" * 70)
