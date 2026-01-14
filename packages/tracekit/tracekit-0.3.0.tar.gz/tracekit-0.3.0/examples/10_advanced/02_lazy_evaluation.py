#!/usr/bin/env python3
"""Example demonstrating lazy evaluation in TraceKit.

This example shows how to use lazy evaluation to defer expensive computations
until results are actually needed, improving memory efficiency and performance.

Requirements demonstrated:

Dependencies:
    - numpy: Required for array operations
    - scipy: Required for signal processing (spectrogram, find_peaks, periodogram)

Usage:
    uv run python examples/lazy_evaluation_example.py
"""
# mypy: disable-error-code="no-untyped-def,no-untyped-call,type-arg,attr-defined,arg-type,union-attr,call-arg,index,no-any-return,override,return-value,var-annotated,func-returns-value,unreachable,assignment,str-bytes-safe,misc,operator,call-overload"

from __future__ import annotations

import time

import numpy as np

from tracekit.core.lazy import (
    LazyAnalysisResult,
    LazyDict,
    LazyResult,
    get_lazy_stats,
    lazy,
    reset_lazy_stats,
)


def example_basic_lazy_result() -> None:
    """Example 1: Basic lazy result usage."""
    print("=" * 70)
    print("Example 1: Basic Lazy Result")
    print("=" * 70)

    # Define an expensive computation
    def expensive_fft(signal: np.ndarray, nfft: int) -> np.ndarray:
        print(f"  Computing FFT with nfft={nfft}...")
        time.sleep(0.1)  # Simulate expensive operation
        return np.fft.fft(signal, n=nfft)

    # Create signal
    signal = np.sin(2 * np.pi * 100 * np.linspace(0, 1, 1000))

    # Wrap in LazyResult - computation not performed yet
    print("\nCreating lazy FFT result...")
    lazy_fft = LazyResult(lambda: expensive_fft(signal, 2048), name="fft_2048")
    print(f"  is_computed: {lazy_fft.is_computed()}")

    # Access triggers computation
    print("\nAccessing value (triggers computation)...")
    spectrum = lazy_fft.value
    print(f"  Computed spectrum shape: {spectrum.shape}")
    print(f"  is_computed: {lazy_fft.is_computed()}")

    # Second access uses cache
    print("\nAccessing value again (uses cache)...")
    spectrum2 = lazy_fft.value
    print(f"  Same result: {spectrum is spectrum2}")
    print()


def example_lazy_decorator() -> None:
    """Example 2: Using @lazy decorator."""
    print("=" * 70)
    print("Example 2: Lazy Decorator")
    print("=" * 70)

    @lazy
    def compute_spectrogram(
        signal: np.ndarray, nperseg: int, noverlap: int
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        print(f"  Computing spectrogram (nperseg={nperseg}, noverlap={noverlap})...")
        time.sleep(0.1)  # Simulate expensive operation
        from scipy import signal as sp_signal

        f, t, Sxx = sp_signal.spectrogram(signal, nperseg=nperseg, noverlap=noverlap)
        return f, t, Sxx

    # Create signal
    signal = np.random.randn(10000)

    # Call returns LazyResult, not computed yet
    print("\nCalling compute_spectrogram (returns LazyResult)...")
    lazy_spec = compute_spectrogram(signal, nperseg=256, noverlap=128)
    print(f"  Type: {type(lazy_spec)}")
    print(f"  is_computed: {lazy_spec.is_computed()}")

    # Access triggers computation
    print("\nAccessing result...")
    f, t, Sxx = lazy_spec.value
    print(f"  Frequency bins: {len(f)}")
    print(f"  Time bins: {len(t)}")
    print(f"  Spectrogram shape: {Sxx.shape}")
    print()


def example_lazy_dict() -> None:
    """Example 3: LazyDict for multiple analysis results."""
    print("=" * 70)
    print("Example 3: LazyDict for Multiple Results")
    print("=" * 70)

    # Create signal
    signal = np.random.randn(10000)

    # Store multiple lazy results
    results = LazyDict()

    print("\nCreating lazy results (nothing computed yet)...")
    results["fft"] = LazyResult(lambda: (print("  Computing FFT..."), np.fft.fft(signal))[1])
    results["power"] = LazyResult(
        lambda: (print("  Computing power..."), np.abs(results["fft"]) ** 2)[1]
    )
    results["peak_freq"] = LazyResult(
        lambda: (print("  Finding peak..."), np.argmax(results["power"]))[1]
    )
    results["constant"] = 42  # Non-lazy value

    print(f"  Deferred: {results.deferred_keys()}")
    print(f"  Computed: {results.computed_keys()}")

    # Access peak_freq triggers entire dependency chain
    print("\nAccessing peak_freq (triggers FFT -> power -> peak)...")
    peak = results["peak_freq"]
    print(f"  Peak frequency bin: {peak}")

    print(f"\n  Deferred: {results.deferred_keys()}")
    print(f"  Computed: {results.computed_keys()}")
    print()


def example_map_chaining() -> None:
    """Example 4: Chaining operations with map()."""
    print("=" * 70)
    print("Example 4: Chaining with map()")
    print("=" * 70)

    signal = np.random.randn(1000)

    print("\nBuilding computation chain (nothing computed yet)...")

    # Chain operations using map
    lazy_fft = LazyResult(lambda: (print("  Computing FFT..."), np.fft.fft(signal))[1], name="fft")
    lazy_magnitude = lazy_fft.map(lambda x: (print("  Computing magnitude..."), np.abs(x))[1])
    lazy_db = lazy_magnitude.map(
        lambda x: (print("  Converting to dB..."), 20 * np.log10(x + 1e-10))[1]
    )

    print(f"  FFT computed: {lazy_fft.is_computed()}")
    print(f"  Magnitude computed: {lazy_magnitude.is_computed()}")
    print(f"  dB computed: {lazy_db.is_computed()}")

    # Access final result triggers entire chain
    print("\nAccessing dB result (triggers entire chain)...")
    db_spectrum = lazy_db.value

    print(f"  Result shape: {db_spectrum.shape}")
    print(f"  All computed: {lazy_fft.is_computed()}")
    print()


def example_multi_domain_analysis() -> None:
    """Example 5: Multi-domain analysis with LazyAnalysisResult."""
    print("=" * 70)
    print("Example 5: Multi-Domain Analysis")
    print("=" * 70)

    class SignalAnalyzer:
        """Example analyzer with multiple analysis domains."""

        def analyze(self, data: np.ndarray, domain: str) -> dict[str, float]:
            print(f"  Computing {domain} domain...")
            time.sleep(0.05)  # Simulate computation

            if domain == "time":
                return {
                    "mean": float(np.mean(data)),
                    "std": float(np.std(data)),
                    "rms": float(np.sqrt(np.mean(data**2))),
                }
            elif domain == "frequency":
                spectrum = np.fft.fft(data)
                power = np.abs(spectrum) ** 2
                return {
                    "peak_freq": float(np.argmax(power)),
                    "bandwidth": float(np.std(power)),
                }
            elif domain == "statistics":
                return {
                    "min": float(np.min(data)),
                    "max": float(np.max(data)),
                    "median": float(np.median(data)),
                    "skewness": float(np.mean(((data - np.mean(data)) / np.std(data)) ** 3)),
                }
            return {}

    # Create signal and analyzer
    signal = np.random.randn(10000)
    analyzer = SignalAnalyzer()

    # Wrap in lazy analysis result
    print("\nCreating lazy multi-domain analysis...")
    lazy_analysis = LazyAnalysisResult(
        analyzer, signal, domains=["time", "frequency", "statistics"]
    )

    print(f"  Domains: {lazy_analysis.domains}")
    print(f"  Computed: {lazy_analysis.computed_domains()}")
    print(f"  Deferred: {lazy_analysis.deferred_domains()}")

    # Access only time domain (others not computed)
    print("\nAccessing time domain only...")
    time_results = lazy_analysis["time"]
    print(f"  Mean: {time_results['mean']:.4f}")
    print(f"  Std: {time_results['std']:.4f}")
    print(f"  RMS: {time_results['rms']:.4f}")

    print(f"\n  Computed: {lazy_analysis.computed_domains()}")
    print(f"  Deferred: {lazy_analysis.deferred_domains()}")

    # Now access frequency domain
    print("\nAccessing frequency domain...")
    freq_results = lazy_analysis["frequency"]
    print(f"  Peak freq: {freq_results['peak_freq']}")

    print(f"\n  Computed: {lazy_analysis.computed_domains()}")
    print(f"  Deferred: {lazy_analysis.deferred_domains()}")
    print()


def example_statistics() -> None:
    """Example 6: Global statistics tracking."""
    print("=" * 70)
    print("Example 6: Global Statistics")
    print("=" * 70)

    reset_lazy_stats()

    # Create and use several lazy results
    print("\nCreating and using lazy results...")
    lazy1 = LazyResult(lambda: np.random.randn(1000))
    lazy2 = LazyResult(lambda: np.random.randn(1000))
    lazy3 = LazyResult(lambda: np.random.randn(1000))

    # Compute some
    _ = lazy1.value
    _ = lazy2.value

    # Access lazy1 again (cache hit)
    _ = lazy1.value
    _ = lazy1.value

    # Show statistics
    print("\nGlobal Statistics:")
    stats = get_lazy_stats()
    print(stats)


def example_practical_workflow() -> None:
    """Example 7: Practical analysis workflow."""
    print("=" * 70)
    print("Example 7: Practical Analysis Workflow")
    print("=" * 70)

    # Simulate loading a large dataset
    print("\nLoading signal data...")
    signal = np.sin(2 * np.pi * 50 * np.linspace(0, 10, 100000))
    signal += 0.5 * np.sin(2 * np.pi * 120 * np.linspace(0, 10, 100000))
    signal += 0.1 * np.random.randn(100000)

    # Create lazy analysis pipeline
    print("\nBuilding lazy analysis pipeline...")
    analysis = LazyDict()

    @lazy
    def compute_fft(sig: np.ndarray) -> np.ndarray:
        print("  [FFT] Computing...")
        return np.fft.fft(sig)

    @lazy
    def compute_psd(sig: np.ndarray) -> np.ndarray:
        print("  [PSD] Computing...")
        from scipy import signal as sp_signal

        freqs, psd = sp_signal.periodogram(sig, fs=10000)
        return psd

    @lazy
    def find_peaks(psd: np.ndarray) -> np.ndarray:
        print("  [Peaks] Finding...")
        from scipy import signal as sp_signal

        peaks, _ = sp_signal.find_peaks(psd, height=np.max(psd) * 0.1)
        return peaks

    analysis["fft"] = compute_fft(signal)
    analysis["psd"] = compute_psd(signal)
    analysis["peaks"] = LazyResult(lambda: find_peaks(analysis["psd"]).value)

    print(f"  Pipeline created. Computed: {analysis.computed_keys()}")

    # User decides they only need peak information
    print("\nUser requests: Show me the dominant frequencies")
    print("  Accessing peaks (triggers PSD and peaks, but NOT FFT)...")
    peaks = analysis["peaks"]
    print(f"  Found {len(peaks)} peaks")

    print(f"\n  Computed: {analysis.computed_keys()}")
    print(f"  Deferred: {analysis.deferred_keys()}")
    print("  -> FFT was never computed (saved computation time!)")
    print()


def main() -> None:
    """Run all examples."""
    print("\n" + "=" * 70)
    print("TraceKit Lazy Evaluation Examples")
    print("=" * 70 + "\n")

    example_basic_lazy_result()
    example_lazy_decorator()
    example_lazy_dict()
    example_map_chaining()
    example_multi_domain_analysis()
    example_statistics()
    example_practical_workflow()

    print("=" * 70)
    print("All examples completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
