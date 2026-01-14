#!/usr/bin/env python3
"""GPU acceleration example for TraceKit.

This example demonstrates how to use the GPU backend for accelerated
signal processing operations. The GPU backend automatically falls back
to NumPy if CuPy is not available.

Requirements:
    - Optional: cupy-cuda11x or cupy-cuda12x for GPU acceleration
    - Without CuPy: Falls back to NumPy automatically

Usage:
    # With GPU acceleration (if CuPy installed)
    uv run python examples/gpu_acceleration_example.py

    # Force CPU-only mode
    TRACEKIT_USE_GPU=0 uv run python examples/gpu_acceleration_example.py

Example output:
    GPU Backend Status
    ==================
    GPU Available: True
    Using CuPy for acceleration

    Performance Comparison
    ======================
    FFT (1M samples):      CPU: 45.2ms   GPU: 12.1ms   Speedup: 3.7x
    Convolution (100k):    CPU: 23.5ms   GPU: 5.8ms    Speedup: 4.1x
    Correlation (50k):     CPU: 156ms    GPU: 38ms     Speedup: 4.1x
"""

from __future__ import annotations

import time

import numpy as np

from tracekit.core.gpu_backend import GPUBackend, gpu


def benchmark_operation(name: str, cpu_backend: GPUBackend, gpu_backend: GPUBackend) -> None:
    """Benchmark an operation on CPU vs GPU.

    Args:
        name: Name of the operation to benchmark.
        cpu_backend: CPU-only backend.
        gpu_backend: GPU-enabled backend.

    Raises:
        ValueError: If an unknown benchmark name is provided.
    """
    # Create test data
    if "FFT" in name:
        data = np.random.randn(1000000).astype(np.float64)
        iterations = 10

        # CPU
        start = time.perf_counter()
        for _ in range(iterations):
            _ = cpu_backend.rfft(data)
        cpu_time = (time.perf_counter() - start) / iterations * 1000

        # GPU
        start = time.perf_counter()
        for _ in range(iterations):
            _ = gpu_backend.rfft(data)
        gpu_time = (time.perf_counter() - start) / iterations * 1000

    elif "Convolution" in name:
        data = np.random.randn(100000).astype(np.float64)
        kernel = np.random.randn(1000).astype(np.float64)
        iterations = 20

        # CPU
        start = time.perf_counter()
        for _ in range(iterations):
            _ = cpu_backend.convolve(data, kernel, mode="same")
        cpu_time = (time.perf_counter() - start) / iterations * 1000

        # GPU
        start = time.perf_counter()
        for _ in range(iterations):
            _ = gpu_backend.convolve(data, kernel, mode="same")
        gpu_time = (time.perf_counter() - start) / iterations * 1000

    elif "Correlation" in name:
        data = np.random.randn(50000).astype(np.float64)
        template = np.random.randn(1000).astype(np.float64)
        iterations = 10

        # CPU
        start = time.perf_counter()
        for _ in range(iterations):
            _ = cpu_backend.correlate(data, template, mode="valid")
        cpu_time = (time.perf_counter() - start) / iterations * 1000

        # GPU
        start = time.perf_counter()
        for _ in range(iterations):
            _ = gpu_backend.correlate(data, template, mode="valid")
        gpu_time = (time.perf_counter() - start) / iterations * 1000

    else:
        raise ValueError(
            f"Unknown benchmark: '{name}'. "
            f"Supported benchmarks: 'FFT (1M samples)', 'Convolution (100k)', 'Correlation (50k)'"
        )

    speedup = cpu_time / gpu_time if gpu_time > 0 else 1.0
    print(f"{name:20s}  CPU: {cpu_time:6.1f}ms   GPU: {gpu_time:6.1f}ms   Speedup: {speedup:.1f}x")


def demonstrate_basic_usage() -> None:
    """Demonstrate basic GPU backend usage."""
    print("\n" + "=" * 70)
    print("Basic Usage Examples")
    print("=" * 70)

    # Example 1: FFT
    print("\n1. GPU-Accelerated FFT:")
    print("-" * 40)
    signal = np.random.randn(10000).astype(np.float64)
    print(f"Input signal: {len(signal)} samples")

    spectrum = gpu.rfft(signal)
    print(f"Output spectrum: {len(spectrum)} frequency bins")
    print(f"GPU was used: {gpu.gpu_available}")

    # Example 2: Convolution for smoothing
    print("\n2. GPU-Accelerated Convolution:")
    print("-" * 40)
    noisy_signal = np.sin(np.linspace(0, 10 * np.pi, 1000)) + 0.2 * np.random.randn(1000)
    smoothing_kernel = np.ones(5) / 5  # Moving average

    smoothed = gpu.convolve(noisy_signal, smoothing_kernel, mode="same")
    print(f"Smoothed signal: {len(smoothed)} samples")
    print(f"Variance before: {np.var(noisy_signal):.4f}")
    print(f"Variance after:  {np.var(smoothed):.4f}")

    # Example 3: Pattern matching with correlation
    print("\n3. GPU-Accelerated Pattern Matching:")
    print("-" * 40)
    data = np.random.randn(10000).astype(np.float64)
    pattern = np.array([1, 2, 3, 2, 1], dtype=np.float64)
    data[5000:5005] = pattern  # Embed pattern

    correlation = gpu.correlate(data, pattern, mode="valid")
    peak_idx = np.argmax(correlation)
    print(f"Pattern found at index: {peak_idx} (expected: ~4997)")
    print(f"Correlation peak value: {correlation[peak_idx]:.2f}")

    # Example 4: Statistical analysis
    print("\n4. GPU-Accelerated Histogram:")
    print("-" * 40)
    samples = np.random.normal(0, 1, 100000)
    counts, edges = gpu.histogram(samples, bins=50)
    print(f"Histogram: {len(counts)} bins")
    print(f"Total samples counted: {counts.sum()}")
    print(f"Peak bin center: {(edges[np.argmax(counts)] + edges[np.argmax(counts) + 1]) / 2:.3f}")


def demonstrate_force_cpu() -> None:
    """Demonstrate forcing CPU-only operation."""
    print("\n" + "=" * 70)
    print("Force CPU Mode Example")
    print("=" * 70)

    cpu_only = GPUBackend(force_cpu=True)
    print(f"\nCPU-only backend GPU available: {cpu_only.gpu_available}")

    # Operations work identically
    signal = np.random.randn(1000).astype(np.float64)
    spectrum = cpu_only.rfft(signal)
    print(f"FFT completed using: {'GPU' if cpu_only.gpu_available else 'CPU (NumPy)'}")
    print(f"Result length: {len(spectrum)}")


def main() -> None:
    """Run GPU acceleration examples and benchmarks."""
    print("=" * 70)
    print("TraceKit GPU Acceleration Example")
    print("=" * 70)

    # Show GPU backend status
    print("\nGPU Backend Status")
    print("=" * 70)
    print(f"GPU Available: {gpu.gpu_available}")
    print(f"Using: {'CuPy (GPU acceleration)' if gpu.gpu_available else 'NumPy (CPU fallback)'}")

    # Basic usage examples
    demonstrate_basic_usage()

    # Force CPU example
    demonstrate_force_cpu()

    # Performance comparison (only if GPU is available)
    if gpu.gpu_available:
        print("\n" + "=" * 70)
        print("Performance Comparison (CPU vs GPU)")
        print("=" * 70)
        print("\nRunning benchmarks... (this may take a minute)")

        cpu_backend = GPUBackend(force_cpu=True)
        gpu_backend = gpu

        benchmark_operation("FFT (1M samples)", cpu_backend, gpu_backend)
        benchmark_operation("Convolution (100k)", cpu_backend, gpu_backend)
        benchmark_operation("Correlation (50k)", cpu_backend, gpu_backend)

        print("\nNote: Speedup depends on GPU model and data transfer overhead.")
        print("      For small arrays, CPU may be faster due to transfer costs.")
    else:
        print("\n" + "=" * 70)
        print("GPU Performance Benchmarks Skipped")
        print("=" * 70)
        print("\nCuPy not available - install with:")
        print("  uv add cupy-cuda11x  # For CUDA 11.x")
        print("  uv add cupy-cuda12x  # For CUDA 12.x")

    print("\n" + "=" * 70)
    print("Example completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
