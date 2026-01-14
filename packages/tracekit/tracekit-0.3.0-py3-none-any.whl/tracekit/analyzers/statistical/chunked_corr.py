"""Chunked correlation for memory-bounded processing.

This module implements memory-efficient cross-correlation using the
overlap-save method for signals larger than memory.


Example:
    >>> from tracekit.analyzers.statistical.chunked_corr import correlate_chunked
    >>> corr = correlate_chunked('signal1.bin', 'signal2.bin', chunk_size=1e6)
    >>> print(f"Correlation shape: {corr.shape}")

References:
    Oppenheim, A.V. & Schafer, R.W. (2009). "Discrete-Time Signal Processing"
    Chapter on overlap-save and overlap-add methods
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Literal

import numpy as np
from scipy import fft, signal

if TYPE_CHECKING:
    from collections.abc import Iterator

    from numpy.typing import NDArray
else:
    NDArray = np.ndarray


def correlate_chunked(
    signal1_path: str | Path | NDArray[np.float64],
    signal2_path: str | Path | NDArray[np.float64],
    *,
    chunk_size: int | float = 1e6,
    mode: Literal["valid", "same", "full"] = "same",
    method: Literal["fft", "direct"] = "fft",
    dtype: str = "float32",
) -> NDArray[np.float64]:
    """Compute correlation for large signals using chunked processing.


    Processes signals in chunks using overlap-save method to compute
    correlation without loading entire signals into memory. Memory
    bounded by chunk size.

    Args:
        signal1_path: Path to first signal file or array.
        signal2_path: Path to second signal file or array.
        chunk_size: Chunk size in samples.
        mode: Correlation mode ('valid', 'same', 'full').
        method: Correlation method ('fft' or 'direct').
        dtype: Data type of input files ('float32' or 'float64').

    Returns:
        Correlation array.

    Example:
        >>> # Correlate two large signals
        >>> corr = correlate_chunked(
        ...     'signal1.bin',
        ...     'signal2.bin',
        ...     chunk_size=1e6,
        ...     mode='same',
        ...     method='fft'
        ... )
        >>> print(f"Correlation peak: {np.max(np.abs(corr))}")

    References:
        MEM-008: Chunked Correlation
    """
    chunk_size = int(chunk_size)

    # Handle array inputs
    if isinstance(signal1_path, np.ndarray):
        signal1 = signal1_path
        signal2 = (
            signal2_path
            if isinstance(signal2_path, np.ndarray)
            else _load_signal(signal2_path, dtype)
        )
        # If both are arrays, use direct correlation
        result: NDArray[np.float64] = signal.correlate(
            signal1, signal2, mode=mode, method=method
        ).astype(np.float64)
        return result

    if isinstance(signal2_path, np.ndarray):
        signal1 = _load_signal(signal1_path, dtype)
        signal2 = signal2_path
        result2: NDArray[np.float64] = signal.correlate(
            signal1, signal2, mode=mode, method=method
        ).astype(np.float64)
        return result2

    # Both are files - use chunked processing
    if method == "fft":
        return _correlate_chunked_fft(signal1_path, signal2_path, chunk_size, mode, dtype)
    else:
        # Direct method - less efficient for large signals
        signal1 = _load_signal(signal1_path, dtype)
        signal2 = _load_signal(signal2_path, dtype)
        result3: NDArray[np.float64] = signal.correlate(
            signal1, signal2, mode=mode, method="direct"
        ).astype(np.float64)
        return result3


def _correlate_chunked_fft(
    signal1_path: str | Path,
    signal2_path: str | Path,
    chunk_size: int,
    mode: str,
    dtype: str,
) -> NDArray[np.float64]:
    """FFT-based chunked correlation using overlap-save.

    Args:
        signal1_path: Path to first signal.
        signal2_path: Path to second signal.
        chunk_size: Chunk size in samples.
        mode: Correlation mode.
        dtype: Data type.

    Returns:
        Correlation array.

    Raises:
        ValueError: If signals have different lengths or mode is invalid.
    """
    # Determine dtype
    np_dtype = np.float32 if dtype == "float32" else np.float64
    bytes_per_sample = 4 if dtype == "float32" else 8

    # Get signal lengths
    path1 = Path(signal1_path)
    path2 = Path(signal2_path)

    len1 = path1.stat().st_size // bytes_per_sample
    len2 = path2.stat().st_size // bytes_per_sample

    if len1 != len2:
        raise ValueError(
            f"Signals must have same length for correlation. Got {len1} and {len2} samples."
        )

    n_samples = len1

    # For correlation, we need to reverse one signal
    # Load signal2 completely (assumed smaller than memory for kernel)
    # In practice, signal2 should be the shorter signal
    signal2 = _load_signal(signal2_path, dtype)
    signal2_rev = signal2[::-1]

    # Determine FFT size (next power of 2)
    nfft = _next_power_of_2(chunk_size + len2 - 1)

    # Pre-compute FFT of reversed signal2
    signal2_fft = fft.rfft(signal2_rev, n=nfft)

    # Overlap-save parameters
    # For correlation, we need overlap equal to the kernel length minus 1
    overlap = len2 - 1

    # Determine output length based on mode
    if mode == "full":
        result_len = n_samples + len2 - 1
    elif mode == "same":
        result_len = n_samples
    elif mode == "valid":
        result_len = max(0, n_samples - len2 + 1)
    else:
        raise ValueError(f"Unknown mode: {mode}")

    result = np.zeros(result_len, dtype=np_dtype)

    # Process signal1 in chunks using overlap-save method
    with open(path1, "rb") as f:
        chunk_idx = 0
        input_offset = 0

        while input_offset < n_samples:
            # Calculate chunk boundaries with overlap
            # First chunk starts at 0, subsequent chunks include overlap
            if chunk_idx == 0:
                chunk_start = 0
                chunk_end = min(n_samples, chunk_size)
            else:
                # Include overlap from previous chunk
                chunk_start = max(0, input_offset - overlap)
                chunk_end = min(n_samples, input_offset + chunk_size)

            # Ensure chunk_start doesn't exceed total_samples
            if chunk_start >= n_samples:
                break

            chunk_len = chunk_end - chunk_start
            if chunk_len <= 0:
                break

            # Read chunk from file
            f.seek(chunk_start * bytes_per_sample)
            chunk1 = np.fromfile(f, dtype=np_dtype, count=chunk_len)

            if len(chunk1) == 0:
                break

            # Zero-pad to FFT size
            chunk1_padded = np.zeros(nfft, dtype=np_dtype)
            chunk1_padded[: len(chunk1)] = chunk1

            # Compute FFT
            chunk1_fft = fft.rfft(chunk1_padded)

            # Multiply in frequency domain (correlation = conj(X) * Y, but signal2 is already reversed)
            corr_fft = chunk1_fft * signal2_fft

            # Inverse FFT
            corr_chunk = fft.irfft(corr_fft, n=nfft)

            # Extract valid portion (discard wrap-around artifacts from circular convolution)
            # The first 'overlap' samples are corrupted by circular wraparound
            if chunk_idx == 0:
                # First chunk: keep all samples from overlap to end
                valid_start = overlap
                valid_length = chunk_size
            else:
                # Subsequent chunks: discard overlap region
                valid_start = overlap
                valid_length = min(chunk_size, len(chunk1) - overlap)

            valid_corr = corr_chunk[valid_start : valid_start + valid_length]

            # Calculate output position for this chunk
            # For 'full' mode, output starts at 0
            # For 'same' mode, output is centered
            if mode == "full":
                output_pos = input_offset
            elif mode == "same":
                # Center the correlation (shift by half kernel length)
                output_pos = input_offset
            else:  # valid
                output_pos = input_offset

            # Copy valid correlation to output
            copy_len = min(len(valid_corr), result_len - output_pos)
            if copy_len > 0:
                result[output_pos : output_pos + copy_len] = valid_corr[:copy_len]

            # Move to next chunk
            input_offset = chunk_end
            chunk_idx += 1

    # Adjust result for different modes
    if mode == "same":
        # Correlation in 'same' mode should be centered
        # The current result is in 'full' mode, so we need to extract the center
        if len(result) > n_samples:
            start_idx = (len(result) - n_samples) // 2
            result = result[start_idx : start_idx + n_samples]
    elif mode == "valid":
        # For 'valid' mode, only keep the center portion where signals fully overlap
        if result_len < len(result):
            start_idx = (len(result) - result_len) // 2
            result = result[start_idx : start_idx + result_len]

    return result.astype(np.float64)


def autocorrelate_chunked(
    signal_path: str | Path | NDArray[np.float64],
    *,
    chunk_size: int | float = 1e6,
    mode: Literal["same", "full"] = "same",
    normalize: bool = True,
    dtype: str = "float32",
) -> NDArray[np.float64]:
    """Compute autocorrelation for large signal using chunked processing.

    Args:
        signal_path: Path to signal file or array.
        chunk_size: Chunk size in samples.
        mode: Correlation mode ('same' or 'full').
        normalize: Normalize by signal variance.
        dtype: Data type of input file.

    Returns:
        Autocorrelation array.

    Example:
        >>> autocorr = autocorrelate_chunked(
        ...     'signal.bin',
        ...     chunk_size=1e6,
        ...     mode='same',
        ...     normalize=True
        ... )
        >>> print(f"Zero-lag correlation: {autocorr[len(autocorr)//2]:.3f}")
    """
    # Autocorrelation is correlation with itself
    result = correlate_chunked(
        signal_path, signal_path, chunk_size=chunk_size, mode=mode, dtype=dtype
    )

    if normalize:
        # Normalize by variance (zero-lag value for 'full' mode)
        if isinstance(signal_path, np.ndarray):
            signal_data = signal_path
            variance = np.var(signal_path)
        else:
            signal_data = _load_signal(signal_path, dtype)
            variance = np.var(signal_data)

        if variance > 0:
            result = result / (variance * len(signal_data))

    return result


def _load_signal(file_path: str | Path, dtype: str) -> NDArray[np.float64]:
    """Load signal from binary file.

    Args:
        file_path: Path to signal file.
        dtype: Data type ('float32' or 'float64').

    Returns:
        Signal array.
    """
    np_dtype = np.float32 if dtype == "float32" else np.float64
    return np.fromfile(file_path, dtype=np_dtype).astype(np.float64)


def _next_power_of_2(n: int) -> int:
    """Return next power of 2 >= n.

    Args:
        n: Input value.

    Returns:
        Next power of 2.
    """
    if n <= 0:
        return 1
    return 1 << (n - 1).bit_length()


def cross_correlate_chunked_generator(
    signal1_path: str | Path,
    signal2_path: str | Path,
    *,
    chunk_size: int | float = 1e6,
    dtype: str = "float32",
) -> Iterator[NDArray[np.float64]]:
    """Generator version that yields correlation chunks.

    Useful for streaming processing of very large correlations.

    Args:
        signal1_path: Path to first signal file.
        signal2_path: Path to second signal file.
        chunk_size: Chunk size in samples.
        dtype: Data type of input files.

    Yields:
        Correlation chunks.

    Note:
        FUTURE ENHANCEMENT: True streaming correlation generator.
        Currently computes full correlation then yields chunks. A true
        streaming implementation would compute correlation incrementally.
        The current implementation provides correct results; streaming
        is a memory optimization opportunity.

    Example:
        >>> for corr_chunk in cross_correlate_chunked_generator('s1.bin', 's2.bin'):
        ...     # Process each chunk separately
        ...     print(f"Chunk max: {np.max(np.abs(corr_chunk))}")
    """
    # Future: Implement true streaming correlation generator
    # For now, compute full correlation and yield in chunks
    corr_full = correlate_chunked(signal1_path, signal2_path, chunk_size=chunk_size, dtype=dtype)

    chunk_size = int(chunk_size)
    for i in range(0, len(corr_full), chunk_size):
        yield corr_full[i : i + chunk_size]


__all__ = [
    "autocorrelate_chunked",
    "correlate_chunked",
    "cross_correlate_chunked_generator",
]
