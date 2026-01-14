"""Memory-mapped loading example for huge waveform files.

This example demonstrates how to use memory-mapped loading to work with
files that are too large to fit in RAM (GB+ files).

Memory-mapped loading allows you to:
1. Access huge files without loading all data into memory
2. Process data in chunks to avoid OOM errors
3. Work with files larger than available RAM
4. Achieve fast random access to any part of the file

Use cases:
- Processing 10+ GB oscilloscope captures
- Analyzing long-duration recordings
- Working on systems with limited RAM
- Chunked FFT analysis of huge signals
"""
# mypy: disable-error-code="no-untyped-def,no-untyped-call,type-arg,attr-defined,arg-type,union-attr,call-arg,index,no-any-return,override,return-value,var-annotated,func-returns-value,unreachable,assignment,str-bytes-safe,misc,operator,call-overload"

from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np

# Import TraceKit loaders
from tracekit.loaders import load_mmap, should_use_mmap
from tracekit.loaders.csv_loader import load_csv
from tracekit.loaders.hdf5_loader import load_hdf5


def example_1_basic_mmap_loading() -> None:
    """Example 1: Basic memory-mapped loading from NumPy file."""
    print("=" * 70)
    print("Example 1: Basic Memory-Mapped Loading")
    print("=" * 70)

    # Create a simulated large file
    with tempfile.TemporaryDirectory() as tmpdir:
        # Simulate a 1GB file (250M float32 samples = 1GB)
        # For demo, we'll use a smaller file
        print("\nCreating test file (10M samples, ~40 MB)...")
        data = np.random.randn(10_000_000).astype(np.float32)
        npy_file = Path(tmpdir) / "huge_trace.npy"
        np.save(npy_file, data)

        file_size_mb = npy_file.stat().st_size / (1024 * 1024)
        print(f"File size: {file_size_mb:.1f} MB")

        # Load with memory mapping
        print("\nLoading with memory mapping...")
        trace = load_mmap(npy_file, sample_rate=1e9)  # 1 GS/s

        print(f"Sample rate: {trace.sample_rate / 1e9:.1f} GS/s")
        print(f"Length: {trace.length:,} samples")
        print(f"Duration: {trace.duration * 1000:.2f} ms")
        print(f"Data type: {trace.dtype}")

        # Access subset without loading entire file
        print("\nAccessing subset (samples 1000-2000)...")
        subset = trace[1000:2000]
        print(f"Subset length: {len(subset):,}")
        print(f"Subset mean: {np.mean(subset):.3f}")

        print("\n✓ Memory-mapped loading successful!")
        print("  Note: Data was NOT loaded into RAM, only metadata.")


def example_2_chunked_processing() -> None:
    """Example 2: Process huge file in chunks to avoid OOM."""
    print("\n" + "=" * 70)
    print("Example 2: Chunked Processing")
    print("=" * 70)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test file
        print("\nCreating test file (5M samples)...")
        data = np.random.randn(5_000_000).astype(np.float32)
        npy_file = Path(tmpdir) / "huge_trace.npy"
        np.save(npy_file, data)

        # Load and process in chunks
        print("\nProcessing in chunks (chunk_size=100k)...")
        trace = load_mmap(npy_file, sample_rate=1e9)

        chunk_results = []
        for i, chunk in enumerate(trace.iter_chunks(chunk_size=100_000)):
            # Compute statistics on each chunk
            chunk_mean = np.mean(chunk)
            chunk_std = np.std(chunk)
            chunk_results.append((chunk_mean, chunk_std))

            if i < 3:  # Show first 3 chunks
                print(f"  Chunk {i}: mean={chunk_mean:.3f}, std={chunk_std:.3f}")

        print(f"\nProcessed {len(chunk_results)} chunks")
        print(f"Overall mean: {np.mean([r[0] for r in chunk_results]):.3f}")
        print(f"Overall std: {np.mean([r[1] for r in chunk_results]):.3f}")

        print("\n✓ Chunked processing complete!")
        print("  Note: Only one chunk in memory at a time.")


def example_3_overlapping_chunks() -> None:
    """Example 3: Windowed processing with overlapping chunks."""
    print("\n" + "=" * 70)
    print("Example 3: Overlapping Chunks (Windowed Processing)")
    print("=" * 70)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test file with a known signal
        print("\nCreating test file with sine wave...")
        t = np.linspace(0, 1, 1_000_000)
        data = np.sin(2 * np.pi * 1000 * t).astype(np.float32)  # 1 kHz sine
        npy_file = Path(tmpdir) / "sine_wave.npy"
        np.save(npy_file, data)

        # Load and process with overlap (for FFT windowing)
        print("\nProcessing with 50% overlap...")
        trace = load_mmap(npy_file, sample_rate=1e6)  # 1 MS/s

        chunk_size = 4096
        overlap = 2048

        chunk_count = 0
        for chunk in trace.iter_chunks(chunk_size=chunk_size, overlap=overlap):
            # Simulate FFT processing
            chunk_count += 1
            if chunk_count <= 3:
                print(
                    f"  Chunk {chunk_count}: length={len(chunk)}, "
                    f"first={chunk[0]:.3f}, last={chunk[-1]:.3f}"
                )

        print(f"\nProcessed {chunk_count} overlapping chunks")
        print(f"Chunk size: {chunk_size}, Overlap: {overlap}")

        print("\n✓ Overlapping chunk processing complete!")
        print("  Use case: FFT with Hanning window")


def example_4_csv_mmap_conversion() -> None:
    """Example 4: Load huge CSV and convert to memory-mapped format."""
    print("\n" + "=" * 70)
    print("Example 4: CSV to Memory-Mapped Conversion")
    print("=" * 70)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create large CSV file
        print("\nCreating CSV file (10k samples)...")
        csv_file = Path(tmpdir) / "oscilloscope.csv"
        with open(csv_file, "w") as f:
            f.write("time,voltage\n")
            for i in range(10_000):
                t = i * 1e-6  # 1 µs intervals
                v = np.sin(2 * np.pi * 1000 * t)  # 1 kHz sine
                f.write(f"{t:.9f},{v:.6f}\n")

        file_size_kb = csv_file.stat().st_size / 1024
        print(f"CSV file size: {file_size_kb:.1f} KB")

        # Load CSV with mmap conversion
        print("\nLoading CSV with mmap=True...")
        trace = load_csv(csv_file, mmap=True)

        print(f"Sample rate: {trace.sample_rate / 1e6:.1f} MS/s")
        print(f"Length: {trace.length:,} samples")
        print(f"Type: {type(trace).__name__}")

        # Access data efficiently
        subset = trace[1000:2000]
        print(f"\nSubset mean: {np.mean(subset):.3f}")

        print("\n✓ CSV converted to memory-mapped format!")
        print("  Note: CSV parsed once, then saved as .npy for efficient access")


def example_5_hdf5_lazy_loading() -> None:
    """Example 5: HDF5 lazy loading (already memory-mapped by h5py)."""
    print("\n" + "=" * 70)
    print("Example 5: HDF5 Lazy Loading")
    print("=" * 70)

    try:
        import h5py
    except ImportError:
        print("\nSkipping: h5py not installed")
        print("Install with: pip install h5py")
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create HDF5 file
        print("\nCreating HDF5 file...")
        h5_file = Path(tmpdir) / "oscilloscope.h5"

        with h5py.File(h5_file, "w") as f:
            # Create large dataset
            data = np.random.randn(1_000_000).astype(np.float32)
            f.create_dataset("waveform", data=data)
            f["waveform"].attrs["sample_rate"] = 1e9

        file_size_mb = h5_file.stat().st_size / (1024 * 1024)
        print(f"HDF5 file size: {file_size_mb:.1f} MB")

        # Load with mmap (uses h5py's lazy loading)
        print("\nLoading HDF5 with mmap=True...")
        trace = load_hdf5(h5_file, mmap=True)

        print(f"Sample rate: {trace.sample_rate / 1e9:.1f} GS/s")
        print(f"Length: {trace.length:,} samples")
        print(f"Type: {type(trace).__name__}")

        # Process in chunks
        print("\nProcessing first 3 chunks...")
        for i, chunk in enumerate(trace.iter_chunks(chunk_size=100_000)):
            if i < 3:
                print(f"  Chunk {i}: mean={np.mean(chunk):.3f}")
            else:
                break

        print("\n✓ HDF5 lazy loading complete!")
        print("  Note: h5py provides native lazy loading")


def example_6_should_use_mmap() -> None:
    """Example 6: Automatically determine if mmap should be used."""
    print("\n" + "=" * 70)
    print("Example 6: Automatic mmap Detection")
    print("=" * 70)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create small file
        small_file = Path(tmpdir) / "small.npy"
        small_data = np.random.randn(1000).astype(np.float32)
        np.save(small_file, small_data)

        # Create larger file
        large_file = Path(tmpdir) / "large.npy"
        large_data = np.random.randn(10_000_000).astype(np.float32)
        np.save(large_file, large_data)

        # Check which should use mmap
        print("\nChecking file sizes...")
        small_size_mb = small_file.stat().st_size / (1024 * 1024)
        large_size_mb = large_file.stat().st_size / (1024 * 1024)

        print(f"Small file: {small_size_mb:.2f} MB")
        print(f"  Should use mmap? {should_use_mmap(small_file)}")

        print(f"Large file: {large_size_mb:.2f} MB")
        print(f"  Should use mmap? {should_use_mmap(large_file)}")

        # Load appropriately
        print("\nLoading files...")
        if should_use_mmap(large_file):
            print("  Using memory-mapped loading for large file")
            trace = load_mmap(large_file, sample_rate=1e9)
        else:
            print("  Using regular loading for large file")
            trace = load_mmap(large_file, sample_rate=1e9)  # Still use mmap for demo

        print(f"  Loaded: {trace.length:,} samples")

        print("\n✓ Automatic detection complete!")
        print("  Threshold: 1 GB (configurable)")


def example_7_context_manager() -> None:
    """Example 7: Using context manager for proper resource cleanup."""
    print("\n" + "=" * 70)
    print("Example 7: Context Manager (Resource Cleanup)")
    print("=" * 70)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test file
        print("\nCreating test file...")
        data = np.random.randn(1_000_000).astype(np.float32)
        npy_file = Path(tmpdir) / "test.npy"
        np.save(npy_file, data)

        # Use context manager
        print("\nUsing context manager...")
        with load_mmap(npy_file, sample_rate=1e9) as trace:
            print(f"  Inside context: {trace.length:,} samples")

            # Process data
            chunk = trace[0:1000]
            print(f"  First chunk mean: {np.mean(chunk):.3f}")

        print("  Outside context: file closed automatically")

        print("\n✓ Context manager ensures proper cleanup!")
        print("  Recommended for production code")


def main() -> None:
    """Run all examples."""
    print("\n" + "=" * 70)
    print("Memory-Mapped Loading Examples for TraceKit")
    print("=" * 70)
    print("\nThese examples demonstrate efficient handling of huge waveform files")
    print("that don't fit in RAM (GB+ files).\n")

    try:
        example_1_basic_mmap_loading()
        example_2_chunked_processing()
        example_3_overlapping_chunks()
        example_4_csv_mmap_conversion()
        example_5_hdf5_lazy_loading()
        example_6_should_use_mmap()
        example_7_context_manager()

        print("\n" + "=" * 70)
        print("All examples completed successfully!")
        print("=" * 70)
        print("\nKey takeaways:")
        print("  1. Use load_mmap() for files > 1 GB")
        print("  2. Process huge files in chunks with iter_chunks()")
        print("  3. Use overlapping chunks for windowed operations (FFT, etc.)")
        print("  4. CSV and HDF5 loaders support mmap=True parameter")
        print("  5. Always use context managers for proper cleanup")
        print("  6. Memory mapping allows working with files larger than RAM")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        raise


if __name__ == "__main__":
    main()
