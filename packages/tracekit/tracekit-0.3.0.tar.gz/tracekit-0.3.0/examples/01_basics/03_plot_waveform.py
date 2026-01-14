#!/usr/bin/env python3
"""Demonstration of TraceKit Visualization API.

This example demonstrates the three main visualization functions:
- tk.plot_waveform() - Time-domain waveform plotting
- tk.plot_spectrum() - Frequency-domain spectrum plotting
- tk.plot_fft() - FFT magnitude spectrum plotting

Examples show:
1. Basic usage with default settings
2. Custom styling and labels
3. Saving plots to files
4. Non-GUI mode for server environments
5. Multiple trace overlay
6. Publication-quality plots

Usage:
    uv run python examples/visualization_demo.py
"""
# mypy: disable-error-code="no-untyped-def,no-untyped-call,type-arg,attr-defined,arg-type,union-attr,call-arg,index,no-any-return,override,return-value,var-annotated,func-returns-value,unreachable,assignment,str-bytes-safe,misc,operator,call-overload"

import tempfile
from pathlib import Path

import matplotlib
import numpy as np

# Set non-GUI backend before importing pyplot
matplotlib.use("Agg")

import matplotlib.pyplot as plt

import tracekit as tk


def create_test_signal(freq=1e6, sample_rate=100e6, duration=1e-3, noise_level=0.1) -> None:
    """Create a test signal with fundamental and harmonics.

    Args:
        freq: Fundamental frequency in Hz
        sample_rate: Sample rate in Hz
        duration: Signal duration in seconds
        noise_level: Noise amplitude relative to signal

    Returns:
        WaveformTrace object
    """
    t = np.arange(0, duration, 1 / sample_rate)

    # Create signal with fundamental and harmonics
    signal = np.sin(2 * np.pi * freq * t)
    signal += 0.3 * np.sin(2 * np.pi * 2 * freq * t)  # 2nd harmonic
    signal += 0.1 * np.sin(2 * np.pi * 3 * freq * t)  # 3rd harmonic

    # Add noise
    signal += noise_level * np.random.randn(len(t))

    metadata = tk.TraceMetadata(sample_rate=sample_rate, channel_name="Test Signal")

    return tk.WaveformTrace(data=signal, metadata=metadata)


def run_visualization_demos(output_dir: Path) -> list[Path]:
    """Run all visualization demos and return list of created files.

    Args:
        output_dir: Directory to save output files

    Returns:
        List of paths to created files
    """
    created_files = []

    # Example 1: Basic waveform plotting
    print("Example 1: Basic waveform plotting")
    print("-" * 50)

    trace = create_test_signal()

    # Simple plot with auto-configuration
    fig = tk.plot_waveform(
        trace,
        title="Test Signal - Time Domain",
        show=False,  # Don't display in non-GUI environments
    )
    plt.close(fig)

    print("Created waveform plot with automatic time unit selection")
    print(f"Signal duration: {trace.duration * 1e3:.2f} ms")
    print()

    # Example 2: Custom styled waveform plot
    print("Example 2: Custom styled waveform plot")
    print("-" * 50)

    trace = create_test_signal()

    # Custom styling
    waveform_file = output_dir / "waveform_custom.png"
    fig = tk.plot_waveform(
        trace,
        title="Custom Styled Waveform",
        xlabel="Time",
        ylabel="Voltage",
        time_unit="us",  # Microseconds
        color="blue",
        figsize=(12, 6),
        show=False,
        save_path=str(waveform_file),
    )
    plt.close(fig)
    created_files.append(waveform_file)

    print("Created custom styled waveform plot")
    print(f"Saved to: {waveform_file}")
    print()

    # Example 3: Basic spectrum plotting
    print("Example 3: Basic spectrum plotting")
    print("-" * 50)

    trace = create_test_signal()

    # Plot frequency spectrum
    fig = tk.plot_spectrum(trace, title="Frequency Spectrum", log_scale=True, show=False)
    plt.close(fig)

    print("Created spectrum plot with logarithmic frequency axis")
    print()

    # Example 4: FFT plotting with custom limits
    print("Example 4: FFT plotting with custom limits")
    print("-" * 50)

    trace = create_test_signal(freq=10e6, sample_rate=1e9)

    # Plot FFT with custom settings
    fft_file = output_dir / "fft_spectrum.png"
    fig = tk.plot_fft(
        trace,
        title="FFT Magnitude Spectrum",
        freq_unit="MHz",
        log_scale=True,
        xlim=(0.1, 100),  # Limit frequency range
        ylim=(-100, 10),  # Limit dB range
        show=False,
        save_path=str(fft_file),
    )
    plt.close(fig)
    created_files.append(fft_file)

    print("Created FFT plot with custom frequency and dB limits")
    print("Frequency range: 0.1 - 100 MHz")
    print("dB range: -100 to 10 dB")
    print(f"Saved to: {fft_file}")
    print()

    # Example 5: Using pre-computed FFT results
    print("Example 5: Using pre-computed FFT results")
    print("-" * 50)

    trace = create_test_signal()

    # Compute FFT separately
    freq, mag = tk.fft(trace)

    # Plot using pre-computed results
    fig = tk.plot_spectrum(
        trace, fft_result=(freq, mag), title="Spectrum from Pre-computed FFT", show=False
    )
    plt.close(fig)

    print("Created spectrum plot from pre-computed FFT")
    print(f"Number of frequency bins: {len(freq)}")
    print(f"Frequency resolution: {freq[1] - freq[0]:.2f} Hz")
    print()

    # Example 6: Publication-quality plot
    print("Example 6: Publication-quality plot")
    print("-" * 50)

    trace = create_test_signal()

    # High-quality plot for publications
    pub_file = output_dir / "publication_fft.png"
    fig = tk.plot_fft(
        trace,
        title="High-Quality FFT Spectrum",
        xlabel="Frequency",
        ylabel="Magnitude",
        freq_unit="MHz",
        figsize=(8, 5),
        show_grid=True,
        show=False,
        save_path=str(pub_file),
    )
    plt.close(fig)
    created_files.append(pub_file)

    print("Created publication-quality plot")
    print("Resolution: 300 DPI")
    print(f"Saved to: {pub_file}")
    print()

    # Example 7: Linear scale spectrum
    print("Example 7: Linear scale spectrum")
    print("-" * 50)

    trace = create_test_signal()

    # Linear frequency axis
    fig = tk.plot_spectrum(
        trace, title="Linear Scale Spectrum", log_scale=False, freq_unit="kHz", show=False
    )
    plt.close(fig)

    print("Created spectrum plot with linear frequency axis")
    print()

    # Example 8: Comparing multiple signals (manual overlay)
    print("Example 8: Comparing multiple signals")
    print("-" * 50)

    # Create two different signals
    trace1 = create_test_signal(freq=1e6, noise_level=0.05)
    trace2 = create_test_signal(freq=1.5e6, noise_level=0.1)

    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # Plot both waveforms
    tk.plot_waveform(trace1, ax=ax1, color="blue", label="Signal 1", show=False)
    tk.plot_waveform(trace2, ax=ax1, color="red", label="Signal 2", show=False)
    ax1.set_title("Waveform Comparison")
    ax1.legend()

    # Plot both spectra
    tk.plot_spectrum(trace1, ax=ax2, color="blue", show=False)
    tk.plot_spectrum(trace2, ax=ax2, color="red", show=False)
    ax2.set_title("Spectrum Comparison")

    plt.tight_layout()
    multi_file = output_dir / "multi_trace_comparison.png"
    fig.savefig(str(multi_file), dpi=300)
    plt.close(fig)
    created_files.append(multi_file)

    print("Created multi-trace comparison plot")
    print(f"Saved to: {multi_file}")
    print()

    # Example 9: Non-GUI mode for server environments
    print("Example 9: Non-GUI mode for server environments")
    print("-" * 50)

    trace = create_test_signal()

    # All plots will work without display
    server_waveform = output_dir / "server_waveform.png"
    server_fft = output_dir / "server_fft.png"
    fig1 = tk.plot_waveform(trace, show=False, save_path=str(server_waveform))
    plt.close(fig1)
    created_files.append(server_waveform)

    fig2 = tk.plot_fft(trace, show=False, save_path=str(server_fft))
    plt.close(fig2)
    created_files.append(server_fft)

    print("Generated plots in non-GUI mode")
    print("Backend: Agg (non-interactive)")
    print(f"Saved waveform to: {server_waveform}")
    print(f"Saved FFT to: {server_fft}")
    print()

    return created_files


def main() -> None:
    """Run all visualization examples."""
    print("=" * 60)
    print("TraceKit Visualization API Demonstration")
    print("=" * 60)
    print()

    # Create a temporary directory for output files
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)

        # Run all examples
        created_files = run_visualization_demos(output_dir)

        print("=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        print()
        print("Key Functions:")
        print("  - tk.plot_waveform() - Time-domain visualization")
        print("  - tk.plot_spectrum() - Frequency-domain visualization")
        print("  - tk.plot_fft()      - FFT magnitude spectrum")
        print()
        print("All functions support:")
        print("  - Auto unit selection (time/frequency)")
        print("  - Custom styling (colors, labels, titles)")
        print("  - Save to file (high-resolution PNG/PDF/SVG)")
        print("  - GUI and non-GUI modes")
        print("  - Publication-quality output")
        print()
        print(f"Created {len(created_files)} temporary files (cleaned up automatically)")


if __name__ == "__main__":
    main()
