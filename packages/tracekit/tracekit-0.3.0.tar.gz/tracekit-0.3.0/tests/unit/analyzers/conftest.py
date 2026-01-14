"""Analyzer-specific test fixtures.

This module provides fixtures for analyzer tests:
- Signal generation fixtures
- Analysis helper fixtures
- Quality metrics fixtures
- Digital signal fixtures
- Protocol-specific signal fixtures
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pytest
from numpy.typing import NDArray

# =============================================================================
# Basic Signal Generation Fixtures
# =============================================================================
# NOTE: Some signal fixtures exist in root conftest.py:
# - sample_rate
# - sine_wave
# - square_wave
# - ramp_signal
# - noisy_sine
# - digital_signal
# These are candidates for migration in Phase 2B


@pytest.fixture
def simple_square_wave() -> NDArray[np.float64]:
    """Generate a simple square wave for testing (3.3V logic levels).

    Returns:
        1000 samples of a clean square wave at 3.3V logic levels.
    """
    pattern = np.array([0, 1, 1, 0, 1, 0, 0, 1], dtype=np.float64) * 3.3
    return np.tile(pattern, 125)  # 1000 samples


@pytest.fixture
def noisy_sine_wave() -> NDArray[np.float64]:
    """Generate a sine wave with Gaussian noise.

    Returns:
        1000 samples of 1 kHz sine wave with 10% RMS noise.
    """
    rng = np.random.default_rng(42)  # Reproducible
    t = np.linspace(0, 1, 1000)
    signal = np.sin(2 * np.pi * 10 * t)
    noise = rng.normal(0, 0.1, 1000)
    return signal + noise


@pytest.fixture
def triangle_wave() -> NDArray[np.float64]:
    """Generate a triangle wave signal.

    Returns:
        1000 samples of a triangle wave from -1 to 1.
    """
    x = np.linspace(0, 4, 1000)
    return 2 * np.abs(2 * (x / 2 - np.floor(x / 2 + 0.5))) - 1


@pytest.fixture
def sawtooth_wave() -> NDArray[np.float64]:
    """Generate a sawtooth wave signal.

    Returns:
        1000 samples of a sawtooth wave from 0 to 1.
    """
    x = np.linspace(0, 4, 1000)
    return x - np.floor(x)


@pytest.fixture
def pwm_signal() -> NDArray[np.float64]:
    """Generate a PWM signal with varying duty cycle.

    Returns:
        PWM signal with duty cycles: 25%, 50%, 75%.
    """
    signal = np.zeros(1200, dtype=np.float64)

    # 25% duty cycle
    signal[0:400] = np.tile([1, 0, 0, 0], 100) * 3.3

    # 50% duty cycle
    signal[400:800] = np.tile([1, 1, 0, 0], 100) * 3.3

    # 75% duty cycle
    signal[800:1200] = np.tile([1, 1, 1, 0], 100) * 3.3

    return signal


# =============================================================================
# Analysis Metadata Fixtures
# =============================================================================


@pytest.fixture
def analyzer_metadata() -> dict[str, Any]:
    """Common metadata for analyzer tests.

    Returns:
        Dictionary with sample_rate, duration, and signal_type.
    """
    return {
        "sample_rate": 1e6,
        "duration": 0.01,
        "signal_type": "test",
        "units": "V",
    }


@pytest.fixture
def timing_metadata() -> dict[str, Any]:
    """Timing-specific metadata for analyzer tests."""
    return {
        "sample_rate": 1e9,  # 1 GHz
        "time_resolution": 1e-9,  # 1 ns
        "edge_detection_threshold": 1.65,  # 3.3V / 2
        "hysteresis": 0.2,  # 200 mV
    }


# =============================================================================
# Digital Signal Analysis Fixtures
# =============================================================================


@pytest.fixture
def spi_signal() -> dict[str, NDArray[np.float64]]:
    """Generate SPI signal traces.

    Returns:
        Dictionary with SCLK, MOSI, MISO, and CS signals.
    """
    samples = 1000

    # Clock: 50% duty cycle
    sclk = np.tile([0, 0, 1, 1], samples // 4) * 3.3

    # MOSI: Data pattern
    mosi_pattern = [0, 1, 0, 1, 1, 0, 1, 0]
    mosi = np.tile(mosi_pattern, samples // len(mosi_pattern)) * 3.3

    # MISO: Response pattern
    miso_pattern = [1, 0, 1, 1, 0, 0, 1, 0]
    miso = np.tile(miso_pattern, samples // len(miso_pattern)) * 3.3

    # CS: Active low, toggled periodically
    cs = np.ones(samples) * 3.3
    cs[100:400] = 0  # Active for 300 samples
    cs[600:800] = 0  # Active for 200 samples

    return {
        "SCLK": sclk[:samples],
        "MOSI": mosi[:samples],
        "MISO": miso[:samples],
        "CS": cs,
    }


@pytest.fixture
def i2c_signal() -> dict[str, NDArray[np.float64]]:
    """Generate I2C signal traces.

    Returns:
        Dictionary with SCL and SDA signals.
    """
    samples = 1000

    # Clock: Periodic pulses
    scl = np.zeros(samples)
    for i in range(0, samples, 50):
        scl[i : i + 25] = 3.3

    # Data: Varying levels
    sda = np.ones(samples) * 3.3
    sda[100:150] = 0  # Start condition
    sda[200:250] = 0  # Address bit
    sda[300:350] = 0  # Data bit
    sda[850:900] = 0  # Stop condition

    return {
        "SCL": scl,
        "SDA": sda,
    }


@pytest.fixture
def can_signal() -> NDArray[np.float64]:
    """Generate CAN bus signal.

    Returns:
        Simplified CAN differential signal.
    """
    # CAN uses differential signaling, but we'll simulate single-ended
    samples = 2000

    # Dominant (0) and recessive (1) bits
    # Dominant: ~2.0V, Recessive: ~3.0V
    pattern = [2.0, 2.0, 3.0, 2.0, 3.0, 3.0, 2.0, 3.0]
    signal = np.tile(pattern, samples // len(pattern))

    return signal[:samples]


# =============================================================================
# Eye Diagram Fixtures
# =============================================================================


@pytest.fixture
def eye_diagram_signal() -> NDArray[np.float64]:
    """Generate signal suitable for eye diagram analysis.

    Returns:
        NRZ signal with ISI and jitter for eye diagram testing.
    """
    rng = np.random.default_rng(42)
    samples_per_bit = 100
    num_bits = 100

    # Generate random bit pattern
    bits = rng.integers(0, 2, num_bits)

    # Generate NRZ signal
    signal = np.repeat(bits, samples_per_bit) * 3.3

    # Add ISI (inter-symbol interference)
    from scipy.ndimage import gaussian_filter1d

    signal = gaussian_filter1d(signal, sigma=10)

    # Add jitter (timing variation)
    time_jitter = rng.normal(0, 2, len(signal))
    indices = np.arange(len(signal)) + time_jitter
    indices = np.clip(indices, 0, len(signal) - 1).astype(int)
    signal = signal[indices]

    # Add noise
    noise = rng.normal(0, 0.1, len(signal))
    return signal + noise


# =============================================================================
# Jitter Analysis Fixtures
# =============================================================================


@pytest.fixture
def jittery_clock() -> NDArray[np.float64]:
    """Generate clock signal with timing jitter.

    Returns:
        Clock signal with period jitter and edge jitter.
    """
    rng = np.random.default_rng(42)
    num_edges = 100
    nominal_period = 100  # samples

    signal = []
    for i in range(num_edges):
        # Add period jitter (±5%)
        period = int(nominal_period + rng.normal(0, 5))

        # High phase
        high_samples = period // 2
        signal.extend([3.3] * high_samples)

        # Low phase
        low_samples = period - high_samples
        signal.extend([0.0] * low_samples)

    return np.array(signal)


@pytest.fixture
def jitter_types() -> dict[str, NDArray[np.float64]]:
    """Generate signals with different jitter types.

    Returns:
        Dictionary mapping jitter type to signal.
    """
    rng = np.random.default_rng(42)
    samples = 10000

    def generate_clock(jitter_std: float) -> NDArray[np.float64]:
        """Generate clock with specified jitter."""
        signal = []
        pos = 0
        while pos < samples:
            period = int(100 + rng.normal(0, jitter_std))
            signal.extend([3.3] * (period // 2))
            signal.extend([0.0] * (period - period // 2))
            pos += period
        return np.array(signal[:samples])

    return {
        "random_jitter": generate_clock(5.0),  # Random jitter
        "deterministic_jitter": generate_clock(0.0)
        + 0.1 * np.sin(2 * np.pi * np.arange(samples) / 100),  # Periodic jitter
        "data_dependent": generate_clock(2.0),  # Data-dependent jitter
    }


# =============================================================================
# Power Analysis Fixtures
# =============================================================================


@pytest.fixture
def power_supply_signal() -> dict[str, NDArray[np.float64]]:
    """Generate power supply voltage and current signals.

    Returns:
        Dictionary with voltage and current traces.
    """
    samples = 1000
    t = np.linspace(0, 1, samples)

    # Voltage: Nominal 3.3V with ripple
    voltage = 3.3 + 0.05 * np.sin(2 * np.pi * 10 * t)

    # Current: Varying load
    current = 0.5 + 0.3 * np.sin(2 * np.pi * 2 * t)
    # Add switching events
    current[400:450] += 0.5
    current[700:750] += 0.5

    return {
        "voltage": voltage,
        "current": current,
        "time": t,
    }


# =============================================================================
# Spectral Analysis Fixtures
# =============================================================================


@pytest.fixture
def multi_tone_signal() -> NDArray[np.float64]:
    """Generate signal with multiple frequency components.

    Returns:
        Sum of sine waves at 10 Hz, 25 Hz, and 50 Hz.
    """
    t = np.linspace(0, 1, 1000)
    signal = (
        np.sin(2 * np.pi * 10 * t)
        + 0.5 * np.sin(2 * np.pi * 25 * t)
        + 0.3 * np.sin(2 * np.pi * 50 * t)
    )
    return signal


@pytest.fixture
def chirp_signal() -> NDArray[np.float64]:
    """Generate chirp signal (frequency sweep).

    Returns:
        Linear frequency sweep from 1 Hz to 50 Hz.
    """
    from scipy.signal import chirp

    t = np.linspace(0, 1, 1000)
    return chirp(t, f0=1, f1=50, t1=1, method="linear")


# =============================================================================
# Statistical Analysis Fixtures
# =============================================================================


@pytest.fixture
def statistical_test_signals() -> dict[str, NDArray[np.float64]]:
    """Generate signals for statistical analysis testing.

    Returns:
        Dictionary with signals having different statistical properties.
    """
    rng = np.random.default_rng(42)

    return {
        "gaussian_noise": rng.normal(0, 1, 1000),
        "uniform_noise": rng.uniform(-1, 1, 1000),
        "poisson_events": rng.poisson(5, 1000).astype(np.float64),
        "bimodal": np.concatenate([rng.normal(-1, 0.2, 500), rng.normal(1, 0.2, 500)]),
    }


# =============================================================================
# Pattern Detection Fixtures
# =============================================================================


@pytest.fixture
def repeating_pattern_signal() -> NDArray[np.float64]:
    """Generate signal with repeating patterns.

    Returns:
        Signal containing multiple instances of the same pattern.
    """
    pattern = np.array([0, 1, 1, 0, 1, 0, 0, 1, 1, 1], dtype=np.float64) * 3.3
    # Repeat pattern 10 times with some noise
    rng = np.random.default_rng(42)
    signal = np.tile(pattern, 10)
    noise = rng.normal(0, 0.1, len(signal))
    return signal + noise


@pytest.fixture
def anomaly_signal() -> NDArray[np.float64]:
    """Generate signal with anomalies for anomaly detection testing.

    Returns:
        Normal signal with injected anomalies.
    """
    rng = np.random.default_rng(42)

    # Base signal: Sine wave
    t = np.linspace(0, 10, 1000)
    signal = np.sin(2 * np.pi * 1 * t)

    # Inject anomalies
    signal[200:210] += 2.0  # Spike
    signal[500:520] = 0.0  # Dropout
    signal[800:850] *= -1  # Polarity inversion

    # Add some noise
    noise = rng.normal(0, 0.05, 1000)
    return signal + noise


# =============================================================================
# Quality Metrics Fixtures
# =============================================================================


@pytest.fixture
def quality_thresholds() -> dict[str, float]:
    """Quality metric thresholds for analyzer validation.

    Returns:
        Dictionary with SNR, THD, and other quality thresholds.
    """
    return {
        "min_snr_db": 40.0,  # Minimum SNR in dB
        "max_thd_percent": 1.0,  # Maximum THD in percent
        "min_sfdr_db": 60.0,  # Spurious-free dynamic range
        "max_jitter_ui": 0.1,  # Maximum jitter in UI
        "min_eye_height": 0.7,  # Minimum eye height (normalized)
        "min_eye_width": 0.8,  # Minimum eye width (normalized)
    }


# =============================================================================
# Edge Detection Fixtures
# =============================================================================


@pytest.fixture
def edge_scenarios() -> dict[str, NDArray[np.float64]]:
    """Generate signals with various edge characteristics.

    Returns:
        Dictionary mapping scenario name to signal.
    """
    samples = 200

    # Ideal edge
    ideal = np.concatenate([np.zeros(100), np.ones(100) * 3.3])

    # Slow edge (RC charging)
    t = np.linspace(0, 5, samples)
    slow = 3.3 * (1 - np.exp(-t / 1))
    slow[:100] = 0

    # Noisy edge
    rng = np.random.default_rng(42)
    noisy = ideal + rng.normal(0, 0.3, samples)

    # Ringing edge (underdamped response)
    ringing = ideal.copy()
    t_ring = np.linspace(0, 10, 100)
    ringing[100:] = 3.3 * (1 + 0.3 * np.exp(-t_ring / 2) * np.sin(2 * np.pi * t_ring))

    return {
        "ideal": ideal,
        "slow": slow,
        "noisy": noisy,
        "ringing": ringing,
    }
