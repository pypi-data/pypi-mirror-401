#!/usr/bin/env python3
"""Example: Signal Quality Metrics.

This example demonstrates measuring signal quality using
SNR, THD, SINAD, and ENOB per IEEE 1241-2010.

Time: 15 minutes
Prerequisites: FFT basics

Run:
    uv run python examples/03_spectral_analysis/02_signal_quality.py
"""

import tracekit as tk
from tracekit.testing import generate_sine_wave


def main() -> None:
    """Demonstrate signal quality measurements."""
    print("=" * 60)
    print("TraceKit Example: Signal Quality Metrics (IEEE 1241-2010)")
    print("=" * 60)

    # --- Generate Test Signals ---
    print("\n--- Generating Test Signals ---")

    # Clean signal (low noise)
    clean = generate_sine_wave(
        frequency=1e6,
        amplitude=1.0,
        sample_rate=100e6,
        duration=1e-3,  # 1ms for accurate measurements
        noise_level=0.001,  # Very low noise
    )
    print("Generated clean 1 MHz sine (noise_level=0.001)")

    # Noisy signal
    noisy = generate_sine_wave(
        frequency=1e6,
        amplitude=1.0,
        sample_rate=100e6,
        duration=1e-3,
        noise_level=0.05,  # Higher noise
    )
    print("Generated noisy 1 MHz sine (noise_level=0.05)")

    # --- Signal-to-Noise Ratio (SNR) ---
    print("\n--- Signal-to-Noise Ratio (SNR) ---")
    print("SNR measures signal power relative to noise floor")
    print("Higher is better. Typical ADC: 50-80 dB")

    snr_clean = tk.snr(clean)
    snr_noisy = tk.snr(noisy)

    print(f"\n  Clean signal SNR: {snr_clean:.1f} dB")
    print(f"  Noisy signal SNR: {snr_noisy:.1f} dB")

    # --- Total Harmonic Distortion (THD) ---
    print("\n--- Total Harmonic Distortion (THD) ---")
    print("THD measures harmonic content relative to fundamental")
    print("Lower is better. High-quality: <0.01%")

    thd_clean = tk.thd(clean, return_db=False)  # Get ratio, not dB
    thd_noisy = tk.thd(noisy, return_db=False)

    print(f"\n  Clean signal THD: {thd_clean * 100:.4f}%")
    print(f"  Noisy signal THD: {thd_noisy * 100:.4f}%")

    # Also show THD in dB
    thd_clean_db = tk.thd(clean, return_db=True)
    thd_noisy_db = tk.thd(noisy, return_db=True)
    print(f"  Clean signal THD: {thd_clean_db:.1f} dB")
    print(f"  Noisy signal THD: {thd_noisy_db:.1f} dB")

    # --- SINAD (Signal-to-Noise and Distortion) ---
    print("\n--- SINAD (Signal-to-Noise and Distortion) ---")
    print("SINAD combines noise and harmonics into single metric")
    print("Higher is better. SINAD <= SNR always")

    sinad_clean = tk.sinad(clean)
    sinad_noisy = tk.sinad(noisy)

    print(f"\n  Clean signal SINAD: {sinad_clean:.1f} dB")
    print(f"  Noisy signal SINAD: {sinad_noisy:.1f} dB")

    # --- Effective Number of Bits (ENOB) ---
    print("\n--- Effective Number of Bits (ENOB) ---")
    print("ENOB converts SINAD to equivalent ADC resolution")
    print("Formula: ENOB = (SINAD - 1.76) / 6.02")

    enob_clean = tk.enob(clean)
    enob_noisy = tk.enob(noisy)

    print(f"\n  Clean signal ENOB: {enob_clean:.2f} bits")
    print(f"  Noisy signal ENOB: {enob_noisy:.2f} bits")

    # Manual ENOB calculation for verification
    manual_enob = (sinad_clean - 1.76) / 6.02
    print(f"  Manual calculation: ({sinad_clean:.1f} - 1.76) / 6.02 = {manual_enob:.2f} bits")

    # --- SFDR (Spurious-Free Dynamic Range) ---
    print("\n--- SFDR (Spurious-Free Dynamic Range) ---")
    print("SFDR measures fundamental vs largest spur")

    sfdr_clean = tk.sfdr(clean)
    sfdr_noisy = tk.sfdr(noisy)

    print(f"\n  Clean signal SFDR: {sfdr_clean:.1f} dB")
    print(f"  Noisy signal SFDR: {sfdr_noisy:.1f} dB")

    # --- Summary Report ---
    print("\n--- Summary Report ---")
    print("\n                    Clean Signal    Noisy Signal")
    print("  " + "-" * 50)
    print(f"  SNR              {snr_clean:8.1f} dB     {snr_noisy:8.1f} dB")
    print(f"  THD              {thd_clean * 100:8.4f}%     {thd_noisy * 100:8.4f}%")
    print(f"  SINAD            {sinad_clean:8.1f} dB     {sinad_noisy:8.1f} dB")
    print(f"  ENOB             {enob_clean:8.2f} bits   {enob_noisy:8.2f} bits")
    print(f"  SFDR             {sfdr_clean:8.1f} dB     {sfdr_noisy:8.1f} dB")

    # --- Interpretation Guide ---
    print("\n--- Interpretation Guide ---")
    print("\nSNR ratings:")
    print("  > 70 dB: Excellent")
    print("  50-70 dB: Good")
    print("  30-50 dB: Fair")
    print("  < 30 dB: Poor")

    print("\nTHD ratings:")
    print("  < 0.001%: Hi-Fi audio grade")
    print("  < 0.01%: Professional grade")
    print("  < 0.1%: Good")
    print("  > 1%: Significant distortion")

    print("\nENOB for typical ADCs:")
    print("  12-bit ADC: ~10.5 ENOB")
    print("  14-bit ADC: ~12 ENOB")
    print("  16-bit ADC: ~14 ENOB")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("Key Points:")
    print("  1. tk.snr() measures signal vs noise (higher = better)")
    print("  2. tk.thd() measures harmonic distortion (lower = better)")
    print("  3. tk.sinad() combines both (higher = better)")
    print("  4. tk.enob() converts SINAD to effective ADC bits")
    print("  5. tk.sfdr() measures spurious-free dynamic range")
    print("  6. All per IEEE 1241-2010 standard")
    print("=" * 60)


if __name__ == "__main__":
    main()
