"""Analysis Engine for orchestrating comprehensive analysis execution.

This module provides the AnalysisEngine class that orchestrates running all
applicable analyses on input data, handling progress tracking, timeouts,
and error collection.
"""

from __future__ import annotations

import importlib
import inspect
import logging
import time
import traceback
import types
from collections.abc import Callable
from pathlib import Path
from typing import Any

import numpy as np

from tracekit.core.types import TraceMetadata, WaveformTrace
from tracekit.reporting.config import (
    ANALYSIS_CAPABILITIES,
    AnalysisConfig,
    AnalysisDomain,
    AnalysisError,
    InputType,
    ProgressInfo,
    get_available_analyses,
)

logger = logging.getLogger(__name__)


# Functions that require context-specific parameters that cannot be auto-detected
NON_INFERRABLE_FUNCTIONS: set[str] = {
    # INFERENCE domain - require specific data types
    "tracekit.inference.protocol_dsl.decode_protocol",
    "tracekit.inference.protocol_dsl.match_pattern",
    "tracekit.inference.protocol_dsl.validate_message",
    # PACKET domain - require PacketInfo objects
    "tracekit.analyzers.packet.timing.analyze_inter_packet_timing",
    "tracekit.analyzers.packet.timing.detect_bursts",
    # POWER domain - require voltage+current pairs
    "tracekit.analyzers.power.consumption.calculate_power",
    "tracekit.analyzers.power.consumption.analyze_power_efficiency",
}


class AnalysisEngine:
    """Engine for orchestrating comprehensive analysis execution.

    The AnalysisEngine accepts input data (from file or in-memory), detects
    the input type, determines applicable analysis domains, and executes
    all relevant analysis functions with progress tracking and error handling.

    Example:
        >>> from tracekit.reporting import AnalysisEngine, AnalysisConfig
        >>> config = AnalysisConfig(timeout_per_analysis=30.0)
        >>> engine = AnalysisEngine(config)
        >>> result = engine.run(input_path=Path("data.wfm"))
        >>> print(f"Ran {result['stats']['total_analyses']} analyses")
        >>> print(f"Success rate: {result['stats']['success_rate']:.1f}%")
    """

    def __init__(self, config: AnalysisConfig | None = None) -> None:
        """Initialize the analysis engine.

        Args:
            config: Analysis configuration. If None, uses defaults.
        """
        self.config = config or AnalysisConfig()
        self._start_time = 0.0
        self._input_path: Path | None = None

    def detect_input_type(self, input_path: Path | None, data: Any) -> InputType:
        """Detect input type from file path or data characteristics.

        Args:
            input_path: Path to input file (None if in-memory data).
            data: Input data object.

        Returns:
            Detected input type.

        Raises:
            ValueError: If input type cannot be determined.
        """
        # If path provided, detect from extension
        if input_path is not None:
            ext = input_path.suffix.lower()

            # Waveform formats
            if ext in {".wfm", ".csv", ".npz", ".h5", ".hdf5", ".wav", ".tdms"}:
                return InputType.WAVEFORM
            # Digital formats
            elif ext in {".vcd", ".sr"}:
                return InputType.DIGITAL
            # Packet formats
            elif ext in {".pcap", ".pcapng"}:
                return InputType.PCAP
            # Binary formats
            elif ext in {".bin", ".raw"}:
                return InputType.BINARY
            # S-parameter/Touchstone formats
            elif ext in {".s1p", ".s2p", ".s3p", ".s4p", ".s5p", ".s6p", ".s7p", ".s8p"}:
                return InputType.SPARAMS

        # Detect from data object characteristics
        if hasattr(data, "s_matrix") and hasattr(data, "frequencies"):
            # SParameterData
            return InputType.SPARAMS
        elif hasattr(data, "data") and hasattr(data, "metadata"):
            # WaveformTrace or DigitalTrace
            if hasattr(data.metadata, "is_digital") and data.metadata.is_digital:
                return InputType.DIGITAL
            return InputType.WAVEFORM
        elif isinstance(data, bytes | bytearray):
            return InputType.BINARY
        elif isinstance(data, list):
            # Assume packet list
            return InputType.PACKETS
        elif isinstance(data, np.ndarray):
            # Assume waveform
            return InputType.WAVEFORM

        raise ValueError("Unable to determine input type from path or data characteristics")

    def run(
        self,
        input_path: Path | None = None,
        data: Any = None,
        progress_callback: Callable[[ProgressInfo], None] | None = None,
    ) -> dict[str, Any]:
        """Run comprehensive analysis on input data.

        Args:
            input_path: Path to input file (or None for in-memory data).
            data: Input data object (or None to load from input_path).
            progress_callback: Optional callback for progress updates.

        Returns:
            Dictionary with keys:
                - 'results': Dict mapping AnalysisDomain to analysis results
                - 'errors': List of AnalysisError objects
                - 'stats': Execution statistics dict

        Raises:
            ValueError: If neither input_path nor data provided.
            FileNotFoundError: If input_path doesn't exist.

        Example:
            >>> def progress(info: ProgressInfo):
            ...     print(f"{info.phase}: {info.percent:.1f}%")
            >>> result = engine.run(input_path=Path("data.wfm"), progress_callback=progress)
        """
        if input_path is None and data is None:
            raise ValueError("Must provide either input_path or data")

        self._start_time = time.time()
        self._input_path = input_path

        # Check available memory and adjust parallelism if needed
        from tracekit.core.memory_guard import check_memory_available

        min_required_mb = 500  # Minimum 500MB needed for analysis
        if not check_memory_available(min_required_mb):
            logger.warning(
                f"Low memory available (< {min_required_mb} MB). "
                f"Reducing parallel workers to conserve memory."
            )
            # Temporarily reduce parallelism to conserve memory
            self.config.parallel_domains = False

        # Phase 1: Load data
        if progress_callback:
            progress_callback(
                ProgressInfo(
                    phase="loading",
                    domain=None,
                    function=None,
                    percent=0.0,
                    message="Loading input data",
                    elapsed_seconds=0.0,
                    estimated_remaining_seconds=None,
                )
            )

        if data is None:
            if input_path is None or not input_path.exists():
                raise FileNotFoundError(f"Input file not found: {input_path}")

            # Load using tracekit loaders
            from tracekit.loaders import load

            data = load(input_path)

        # Phase 2: Detect input type
        input_type = self.detect_input_type(input_path, data)

        if progress_callback:
            progress_callback(
                ProgressInfo(
                    phase="detecting",
                    domain=None,
                    function=None,
                    percent=5.0,
                    message=f"Detected input type: {input_type.value}",
                    elapsed_seconds=time.time() - self._start_time,
                    estimated_remaining_seconds=None,
                )
            )

        # Phase 3: Determine applicable domains
        applicable_domains = get_available_analyses(input_type)

        # Filter by configuration
        enabled_domains = [d for d in applicable_domains if self.config.is_domain_enabled(d)]

        if progress_callback:
            progress_callback(
                ProgressInfo(
                    phase="planning",
                    domain=None,
                    function=None,
                    percent=10.0,
                    message=f"Planning analysis across {len(enabled_domains)} domains",
                    elapsed_seconds=time.time() - self._start_time,
                    estimated_remaining_seconds=None,
                )
            )

        # Phase 4: Execute analyses
        results: dict[AnalysisDomain, dict[str, Any]] = {}
        errors: list[AnalysisError] = []

        total_domains = len(enabled_domains)

        # Execute domains in parallel if enabled and multiple domains exist
        if self.config.parallel_domains and len(enabled_domains) > 1:
            import concurrent.futures

            # Use ThreadPoolExecutor with bounded workers from config
            max_workers = min(self.config.max_parallel_workers, len(enabled_domains))

            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Submit all domain executions
                futures = {
                    executor.submit(self._execute_domain, domain, data): domain
                    for domain in enabled_domains
                }

                # Process results as they complete
                for completed, future in enumerate(concurrent.futures.as_completed(futures), 1):
                    domain = futures[future]
                    domain_percent = 10.0 + (completed / total_domains) * 80.0

                    if progress_callback:
                        progress_callback(
                            ProgressInfo(
                                phase="analyzing",
                                domain=domain,
                                function=None,
                                percent=domain_percent,
                                message=f"Completed domain: {domain.value}",
                                elapsed_seconds=time.time() - self._start_time,
                                estimated_remaining_seconds=None,
                            )
                        )

                    try:
                        # Retrieve result with timeout
                        timeout_seconds = self.config.timeout_per_analysis or 30.0
                        domain_results, domain_errors = future.result(timeout=timeout_seconds * 10)
                        if domain_results:
                            results[domain] = domain_results
                        errors.extend(domain_errors)
                    except concurrent.futures.TimeoutError:
                        logger.error(f"Domain {domain.value} exceeded timeout")
                        errors.append(
                            AnalysisError(
                                domain=domain,
                                function=f"{domain.value}.*",
                                error_type="TimeoutError",
                                error_message="Domain execution exceeded timeout",
                                traceback=None,
                                duration_ms=timeout_seconds * 10 * 1000,
                            )
                        )
                    except Exception as e:
                        logger.error(f"Domain {domain.value} failed: {e}")
                        errors.append(
                            AnalysisError(
                                domain=domain,
                                function=f"{domain.value}.*",
                                error_type=type(e).__name__,
                                error_message=str(e),
                                traceback=traceback.format_exc(),
                                duration_ms=0.0,
                            )
                        )
        else:
            # Sequential fallback (existing code)
            for idx, domain in enumerate(enabled_domains):
                domain_percent = 10.0 + (idx / total_domains) * 80.0

                if progress_callback:
                    progress_callback(
                        ProgressInfo(
                            phase="analyzing",
                            domain=domain,
                            function=None,
                            percent=domain_percent,
                            message=f"Analyzing domain: {domain.value}",
                            elapsed_seconds=time.time() - self._start_time,
                            estimated_remaining_seconds=None,
                        )
                    )

                domain_results, domain_errors = self._execute_domain(domain, data)
                if domain_results:
                    results[domain] = domain_results
                errors.extend(domain_errors)

        # Phase 5: Complete
        total_duration = time.time() - self._start_time

        if progress_callback:
            progress_callback(
                ProgressInfo(
                    phase="complete",
                    domain=None,
                    function=None,
                    percent=100.0,
                    message="Analysis complete",
                    elapsed_seconds=total_duration,
                    estimated_remaining_seconds=0.0,
                )
            )

        # Calculate statistics
        total_analyses = sum(len(dr) for dr in results.values())
        successful_analyses = sum(
            1 for dr in results.values() for v in dr.values() if not isinstance(v, Exception)
        )
        failed_analyses = len(errors)

        stats = {
            "input_type": input_type.value,
            "total_domains": len(enabled_domains),
            "total_analyses": total_analyses,
            "successful_analyses": successful_analyses,
            "failed_analyses": failed_analyses,
            "success_rate": (successful_analyses / total_analyses * 100.0)
            if total_analyses > 0
            else 0.0,
            "duration_seconds": total_duration,
        }

        return {
            "results": results,
            "errors": errors,
            "stats": stats,
        }

    def _execute_domain(
        self, domain: AnalysisDomain, data: Any
    ) -> tuple[dict[str, Any], list[AnalysisError]]:
        """Execute all analyses for a specific domain.

        Args:
            domain: Analysis domain to execute.
            data: Input data object.

        Returns:
            Tuple of (results_dict, errors_list).
        """
        results: dict[str, Any] = {}
        errors: list[AnalysisError] = []

        # Preprocess data for specific domains
        data = self._preprocess_for_domain(domain, data)

        # Get domain capabilities
        cap = ANALYSIS_CAPABILITIES.get(domain, {})
        module_names = cap.get("modules", [])

        # Fallback to old single-module format
        if not module_names:
            single_module = cap.get("module", "")
            if single_module:
                module_names = [single_module]

        if not module_names:
            logger.debug(f"No modules configured for domain {domain.value}")
            return results, errors

        # Get domain-specific config
        domain_config = self.config.get_domain_config(domain)
        timeout = domain_config.timeout or self.config.timeout_per_analysis

        # Track executed functions to prevent duplicates
        executed_functions: set[str] = set()

        # Iterate through all modules for this domain
        for module_name in module_names:
            try:
                module = importlib.import_module(module_name)
            except ImportError as e:
                logger.warning(f"Failed to import module {module_name}: {e}")
                if not self.config.continue_on_error:
                    errors.append(
                        AnalysisError(
                            domain=domain,
                            function=module_name,
                            error_type="ImportError",
                            error_message=str(e),
                            traceback=traceback.format_exc(),
                            duration_ms=0.0,
                        )
                    )
                continue

            # Discover public functions in the module
            for func_name, func_obj in inspect.getmembers(module):
                # Skip private functions and non-functions
                if func_name.startswith("_") or not inspect.isfunction(func_obj):
                    continue

                # Skip functions not defined in this module (imported from elsewhere)
                if func_obj.__module__ != module_name:
                    continue

                # Skip if already executed (prevent duplicates)
                func_path = f"{module_name}.{func_name}"
                if func_path in executed_functions:
                    logger.debug(f"Skipping duplicate function: {func_path}")
                    continue
                executed_functions.add(func_path)

                # Execute the function
                try:
                    result = self._execute_function(module_name, func_name, data, timeout)
                    results[f"{module_name}.{func_name}"] = result
                except Exception as e:
                    error = AnalysisError(
                        domain=domain,
                        function=f"{module_name}.{func_name}",
                        error_type=type(e).__name__,
                        error_message=str(e),
                        traceback=traceback.format_exc(),
                        duration_ms=0.0,
                    )
                    errors.append(error)

                    if not self.config.continue_on_error:
                        # Stop execution for this domain
                        return results, errors

        return results, errors

    def _preprocess_for_domain(self, domain: AnalysisDomain, data: Any) -> Any:
        """Preprocess data for domain-specific requirements.

        Some domains require specialized data structures. This method
        converts raw data into the appropriate format.

        Args:
            domain: Target analysis domain.
            data: Input data object.

        Returns:
            Preprocessed data suitable for the domain.
        """
        if domain == AnalysisDomain.EYE:
            # EYE domain requires an EyeDiagram object
            # Try to generate one from waveform data
            return self._preprocess_for_eye_domain(data)

        return data

    def _get_effective_sample_rate(self, data: Any, context: str = "general") -> float:
        """Get effective sample rate from data metadata or config defaults.

        Priority order:
        1. Data metadata (e.g., WaveformTrace.metadata.sample_rate)
        2. AnalysisConfig.default_sample_rate
        3. Context-appropriate default constant

        Args:
            data: Input data object (may have .metadata.sample_rate).
            context: Analysis context for selecting appropriate default.
                Options: "general" (1 MHz), "highspeed" (1 GHz), "binary" (1 Hz).

        Returns:
            Effective sample rate in Hz.

        Note:
            This method logs a debug message when falling back to defaults,
            as sample rate should ideally be provided in the data metadata
            for accurate time-domain analysis.
        """
        # Try to extract from data metadata
        data_sample_rate = None
        if hasattr(data, "metadata") and hasattr(data.metadata, "sample_rate"):
            data_sample_rate = data.metadata.sample_rate
            if data_sample_rate is not None and data_sample_rate > 0:
                return float(data_sample_rate)

        # Use config's get_effective_sample_rate method
        effective_rate = self.config.get_effective_sample_rate(
            data_sample_rate=data_sample_rate,
            context=context,
        )

        # Log when using defaults (indicates missing metadata)
        logger.debug(
            f"Using default sample rate {effective_rate:.2e} Hz (context: {context}). "
            f"For accurate analysis, provide sample_rate in data metadata."
        )

        return effective_rate

    def _preprocess_for_eye_domain(self, data: Any) -> Any:
        """Preprocess data for eye diagram analysis.

        Attempts to generate an EyeDiagram from waveform data using
        automatic unit interval detection via FFT-based period detection
        with fallback to zero-crossing analysis.

        Args:
            data: Input waveform data.

        Returns:
            EyeDiagram object if successful, original data otherwise.
        """
        # Check if already an EyeDiagram
        if hasattr(data, "samples_per_ui") and hasattr(data, "time_axis"):
            return data

        # Try to extract waveform data
        if hasattr(data, "data") and hasattr(data, "metadata"):
            # WaveformTrace
            raw_data = data.data
            sample_rate = getattr(data.metadata, "sample_rate", None)
        elif isinstance(data, np.ndarray):
            raw_data = data
            sample_rate = None
        else:
            # Can't preprocess, return as-is
            return data

        if raw_data is None or len(raw_data) == 0:
            return data

        try:
            from tracekit.analyzers.eye.diagram import generate_eye
            from tracekit.core.types import TraceMetadata, WaveformTrace

            # Get effective sample rate using config-aware method
            # Use "highspeed" context for eye diagram (typically high-speed serial)
            if sample_rate is None or sample_rate <= 0:
                sample_rate = self._get_effective_sample_rate(data, context="highspeed")

            # Estimate unit interval using FFT-based period detection
            unit_interval = self._detect_unit_interval_fft(raw_data, sample_rate)

            # If FFT detection fails, try zero-crossing analysis
            if unit_interval is None:
                unit_interval = self._detect_unit_interval_zero_crossing(raw_data, sample_rate)

            # If both methods fail, use default fallback
            if unit_interval is None:
                # Fallback: assume 100 UI in the data
                unit_interval = len(raw_data) / sample_rate / 100
                logger.debug("Using default unit interval fallback (100 UI in data)")

            # Ensure unit interval is reasonable
            min_ui = 10 / sample_rate  # At least 10 samples per UI
            max_ui = len(raw_data) / sample_rate / 10  # At least 10 UI in data
            unit_interval = np.clip(unit_interval, min_ui, max_ui)

            # Create a WaveformTrace if we only have raw data
            if not hasattr(data, "data"):
                metadata = TraceMetadata(sample_rate=sample_rate)
                trace = WaveformTrace(data=raw_data.astype(np.float64), metadata=metadata)
            else:
                trace = data

            # Generate eye diagram
            eye_diagram = generate_eye(
                trace=trace,
                unit_interval=unit_interval,
                n_ui=2,
                generate_histogram=True,
            )

            logger.debug(
                f"Generated eye diagram: {eye_diagram.n_traces} traces, "
                f"{eye_diagram.samples_per_ui} samples/UI"
            )
            return eye_diagram

        except Exception as e:
            logger.debug(f"Could not generate eye diagram: {e}")
            # Return original data if preprocessing fails
            return data

    def _detect_unit_interval_fft(
        self, raw_data: np.ndarray[Any, Any], sample_rate: float
    ) -> float | None:
        """Detect unit interval using FFT-based period detection.

        Computes the FFT of the waveform, finds the dominant frequency
        (excluding DC), and calculates the unit interval for NRZ data.

        Args:
            raw_data: Input waveform samples.
            sample_rate: Sample rate in Hz.

        Returns:
            Estimated unit interval in seconds, or None if detection fails.
        """
        try:
            # Remove DC component
            data_ac = raw_data - np.mean(raw_data)

            # Compute FFT
            fft_result = np.fft.rfft(data_ac)
            fft_freqs = np.fft.rfftfreq(len(data_ac), d=1.0 / sample_rate)

            # Get magnitude spectrum (exclude DC bin at index 0)
            magnitude = np.abs(fft_result[1:])
            freqs = fft_freqs[1:]

            if len(magnitude) == 0:
                return None

            # Find dominant frequency (peak in magnitude spectrum)
            peak_idx = np.argmax(magnitude)
            dominant_freq = freqs[peak_idx]

            # For NRZ data, unit interval = 1 / (2 * dominant_freq)
            # For periodic signals like sine waves, unit interval = 1 / dominant_freq
            # We'll use the period as the unit interval for general signals
            if dominant_freq > 0:
                unit_interval = float(1.0 / dominant_freq)

                # Sanity check: dominant frequency should be reasonable
                min_freq = sample_rate / len(raw_data)  # At least one full cycle
                max_freq = sample_rate / 20  # At least 20 samples per cycle

                if min_freq <= dominant_freq <= max_freq:
                    logger.debug(
                        f"FFT detected dominant frequency: {dominant_freq:.2f} Hz, "
                        f"unit interval: {unit_interval * 1e6:.3f} us"
                    )
                    return unit_interval
                else:
                    logger.debug(
                        f"FFT dominant frequency {dominant_freq:.2f} Hz out of range "
                        f"[{min_freq:.2f}, {max_freq:.2f}] Hz"
                    )
                    return None

            return None

        except Exception as e:
            logger.debug(f"FFT-based unit interval detection failed: {e}")
            return None

    def _detect_unit_interval_zero_crossing(
        self, raw_data: np.ndarray[Any, Any], sample_rate: float
    ) -> float | None:
        """Detect unit interval using zero-crossing analysis.

        Estimates the signal period from the average interval between
        zero crossings.

        Args:
            raw_data: Input waveform samples.
            sample_rate: Sample rate in Hz.

        Returns:
            Estimated unit interval in seconds, or None if detection fails.
        """
        try:
            # Find zero crossings
            zero_crossings = np.where(np.diff(np.sign(raw_data - np.mean(raw_data))))[0]

            if len(zero_crossings) > 10:
                # Estimate period from average crossing interval
                avg_half_period = float(np.mean(np.diff(zero_crossings))) / sample_rate
                unit_interval = avg_half_period * 2  # Full period

                logger.debug(
                    f"Zero-crossing detected unit interval: {unit_interval * 1e6:.3f} us "
                    f"({len(zero_crossings)} crossings)"
                )
                return unit_interval
            else:
                logger.debug(f"Insufficient zero crossings ({len(zero_crossings)}) for detection")
                return None

        except Exception as e:
            logger.debug(f"Zero-crossing unit interval detection failed: {e}")
            return None

    def _detect_baud_rate_from_filename(self, path: Path | None) -> float | None:
        """Extract baud rate from filename patterns like 'capture_9600baud.vcd'.

        Supports patterns such as:
        - 9600baud, 115200baud
        - 9600_baud, 115200_baud
        - 1Mbaud, 1.5Mbaud (with M/m prefix for megabaud)
        - 9600bps, 115200bps

        Args:
            path: Path to the input file (None if in-memory data).

        Returns:
            Detected baud rate in bps, or None if not detected.
        """
        if path is None:
            return None

        import re

        # Match patterns: 9600baud, 115200_baud, 1Mbaud, etc.
        patterns = [
            r"(\d+(?:\.\d+)?)[_\s]*[Mm]?baud",
            r"(\d+(?:\.\d+)?)[_\s]*bps",
            r"baud[_-]?(\d+)",
        ]
        filename = path.stem.lower()

        for pattern in patterns:
            match = re.search(pattern, filename, re.IGNORECASE)
            if match:
                value = float(match.group(1))
                # Handle M prefix (megabaud)
                matched_text = filename[match.start() : match.end()].lower()
                if "m" in matched_text and "baud" in matched_text:
                    value *= 1_000_000
                logger.debug(f"Detected baud rate from filename '{path.name}': {value} bps")
                return value

        return None

    def _detect_logic_family(self, data: np.ndarray[Any, Any]) -> str:
        """Detect logic family from voltage levels.

        Analyzes the voltage swing in the data to determine the likely
        logic family standard.

        Args:
            data: Input waveform samples (voltage levels).

        Returns:
            Detected logic family name (e.g., "TTL", "LVCMOS33", "LVDS").
        """
        vmax = float(np.max(data))
        vmin = float(np.min(data))
        voltage_swing = vmax - vmin

        # Classify based on voltage swing
        if voltage_swing < 1.0:
            logic_family = "LVDS"  # ~0.35V swing
        elif voltage_swing < 2.0:
            logic_family = "LVCMOS18"  # 1.8V
        elif voltage_swing < 3.0:
            logic_family = "LVCMOS25"  # 2.5V
        elif voltage_swing < 4.0:
            logic_family = "LVCMOS33"  # 3.3V
        else:
            logic_family = "TTL"  # 5V

        logger.debug(
            f"Detected logic family from voltage swing {voltage_swing:.2f}V: {logic_family}"
        )
        return logic_family

    def _detect_frequency_range(
        self, data: np.ndarray[Any, Any], sample_rate: float
    ) -> tuple[float, float] | None:
        """Detect dominant frequency range from FFT analysis.

        Computes the FFT of the input signal and identifies the range
        of frequencies containing significant spectral content.

        Args:
            data: Input waveform samples.
            sample_rate: Sample rate in Hz.

        Returns:
            Tuple of (min_freq, max_freq) in Hz for significant spectral content,
            or None if detection fails.
        """
        try:
            # Compute FFT
            fft_result = np.fft.rfft(data - np.mean(data))
            freqs = np.fft.rfftfreq(len(data), d=1.0 / sample_rate)
            magnitude = np.abs(fft_result)

            # Find frequencies with significant power (> 10% of max)
            threshold = 0.1 * np.max(magnitude)
            significant = freqs[magnitude > threshold]

            if len(significant) > 0:
                min_freq = float(np.min(significant))
                max_freq = float(np.max(significant))
                logger.debug(f"Detected frequency range: {min_freq:.2f} Hz - {max_freq:.2f} Hz")
                return (min_freq, max_freq)
            return None
        except Exception as e:
            logger.debug(f"Frequency range detection failed: {e}")
            return None

    def _detect_noise_floor(self, data: np.ndarray[Any, Any]) -> float | None:
        """Estimate noise floor using median absolute deviation.

        Uses robust statistical methods to estimate the noise level in
        the signal, which is useful for setting thresholds in various
        analysis functions.

        Args:
            data: Input waveform samples.

        Returns:
            Estimated noise level (standard deviation of noise), or None if detection fails.
        """
        try:
            try:
                from scipy import stats

                # Use MAD for robust noise estimation
                mad = stats.median_abs_deviation(data, scale="normal")
                logger.debug(f"Detected noise floor (scipy MAD): {mad:.6f}")
                return float(mad)
            except ImportError:
                # Fallback without scipy
                median = np.median(data)
                mad = np.median(np.abs(data - median)) * 1.4826
                logger.debug(f"Detected noise floor (numpy MAD): {mad:.6f}")
                return float(mad)
        except Exception as e:
            logger.debug(f"Noise floor detection failed: {e}")
            return None

    def _detect_protocol_hints(
        self, data: np.ndarray[Any, Any], sample_rate: float
    ) -> dict[str, Any]:
        """Detect hints about potential protocols in the signal.

        Analyzes signal characteristics such as edge timing and periodicity
        to provide hints about the communication protocol that may be present.

        Args:
            data: Input waveform samples.
            sample_rate: Sample rate in Hz.

        Returns:
            Dictionary with detected characteristics such as:
                - 'detected_baud': Estimated baud rate (if detected)
                - 'clock_regularity': 'high', 'medium', or 'low'
        """
        hints: dict[str, Any] = {}
        try:
            # Check for common baud rates by looking at edge timing
            zero_crossings = np.where(np.diff(np.sign(data - np.mean(data))))[0]
            if len(zero_crossings) > 10:
                intervals = np.diff(zero_crossings) / sample_rate
                avg_interval = float(np.median(intervals))

                # Map to standard baud rates
                common_bauds = [
                    300,
                    1200,
                    2400,
                    4800,
                    9600,
                    19200,
                    38400,
                    57600,
                    115200,
                ]
                for baud in common_bauds:
                    expected_interval = 1.0 / baud
                    if 0.8 < avg_interval / expected_interval < 1.2:
                        hints["detected_baud"] = baud
                        logger.debug(f"Protocol hint: detected baud rate {baud} bps")
                        break

            # Check for clock-like periodicity
            if len(zero_crossings) > 20:
                interval_std = float(np.std(np.diff(zero_crossings)))
                if interval_std < 2:
                    regularity = "high"
                elif interval_std < 5:
                    regularity = "medium"
                else:
                    regularity = "low"
                hints["clock_regularity"] = regularity
                logger.debug(f"Protocol hint: clock regularity {regularity}")

        except Exception as e:
            logger.debug(f"Protocol hints detection failed: {e}")

        return hints

    def _execute_function(
        self, module_name: str, func_name: str, data: Any, timeout: float | None
    ) -> Any:
        """Execute a single analysis function with quality scoring.

        Args:
            module_name: Name of the module containing the function.
            func_name: Name of the function to execute.
            data: Input data object.
            timeout: Timeout in seconds (None for no timeout).

        Returns:
            Analysis result with optional quality score attached.

        Raises:
            ValueError: If function is non-inferrable or invalid.
        """
        # Check if function is in non-inferrable skip list
        func_path = f"{module_name}.{func_name}"
        if func_path in NON_INFERRABLE_FUNCTIONS:
            logger.debug(f"Skipping non-inferrable function: {func_path}")
            raise ValueError(
                f"Function {func_path} requires context-specific parameters that cannot be auto-detected"
            )

        module = importlib.import_module(module_name)
        func = getattr(module, func_name)

        # Prepare function arguments
        args, kwargs = self._prepare_arguments(func, data)

        if args is None:
            # Function not applicable to this data type
            raise ValueError(f"Function {func_name} not applicable to data type")

        start_time = time.time()

        # Execute with timeout if specified
        if timeout is not None:
            # Note: Python doesn't have built-in function timeout without threads/processes
            # For simplicity, we'll just execute directly and check elapsed time afterward
            # A production implementation would use threading.Timer or signal.alarm
            result = func(*args, **kwargs)

            elapsed = time.time() - start_time
            if elapsed > timeout:
                logger.warning(
                    f"Function {module_name}.{func_name} exceeded timeout "
                    f"({elapsed:.2f}s > {timeout:.2f}s)"
                )
        else:
            result = func(*args, **kwargs)

        # Consume generators to avoid serialization issues
        if isinstance(result, types.GeneratorType):
            try:
                result = list(result)
                logger.debug(f"Consumed generator from {module_name}.{func_name}")
            except Exception as e:
                logger.warning(f"Failed to consume generator from {module_name}.{func_name}: {e}")
                result = f"<generator error: {type(e).__name__}>"

        # Add quality scoring if enabled in config
        if self.config.enable_quality_scoring:
            result = self._add_quality_score(result, func_path, data)

        return result

    def _add_quality_score(self, result: Any, method_name: str, data: Any) -> Any:
        """Add quality score to analysis result.

        Args:
            result: Analysis result to score.
            method_name: Name of the analysis method.
            data: Input data object.

        Returns:
            Result with quality score attached (if applicable).
        """
        try:
            from tracekit.quality import score_analysis_result

            # Extract raw data array for quality assessment
            if hasattr(data, "data"):
                raw_data = data.data
            elif isinstance(data, np.ndarray):
                raw_data = data
            else:
                # Can't assess quality for non-array data
                return result

            # Score the result
            quality_score = score_analysis_result(
                result=result,
                method_name=method_name,
                data=raw_data,
            )

            # Attach quality score to result if it's a dict
            if isinstance(result, dict):
                result["_quality_score"] = quality_score.to_dict()
            # For other types, wrap in dict
            elif result is not None:
                return {
                    "value": result,
                    "_quality_score": quality_score.to_dict(),
                }

        except Exception as e:
            logger.debug(f"Failed to add quality score: {e}")

        return result

    def _prepare_arguments(
        self, func: Callable[..., Any], data: Any
    ) -> tuple[list[Any] | None, dict[str, Any]]:
        """Prepare arguments for an analysis function.

        Examines the function signature and prepares appropriate arguments
        from the input data.

        Args:
            func: Function to prepare arguments for.
            data: Input data object.

        Returns:
            Tuple of (args_list, kwargs_dict), or (None, {}) if not applicable.
        """
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())

        if not params:
            return [], {}

        first_param = params[0]

        # Check for EyeDiagram - these functions expect 'eye' parameter
        if hasattr(data, "samples_per_ui") and hasattr(data, "time_axis"):
            # EyeDiagram object
            if first_param == "eye" or "EyeDiagram" in str(sig.parameters.get(first_param, "")):
                return [data], {}
            # Skip functions that don't work with EyeDiagram
            return None, {}

        # Check for SParameterData
        if hasattr(data, "s_matrix") and hasattr(data, "frequencies"):
            # S-parameter object
            if first_param in ("s_params", "s_param", "s_data", "sparams"):
                return [data], {}
            if "SParameter" in str(sig.parameters.get(first_param, "")):
                return [data], {}
            # Skip functions that don't work with S-params
            return None, {}

        # Check type annotation for packet-specific handling
        first_param_info = sig.parameters.get(first_param)
        param_annotation = first_param_info.annotation if first_param_info else None
        annotation_str = str(param_annotation) if param_annotation else ""

        # Handle PACKET domain - convert to PacketInfo objects if needed
        if "PacketInfo" in annotation_str or first_param == "packets":
            if isinstance(data, list):
                # Check if already PacketInfo objects
                if data and hasattr(data[0], "timestamp"):
                    return [data], {}
                # Convert list of dicts to PacketInfo objects
                elif data and isinstance(data[0], dict):
                    try:
                        from tracekit.analyzers.packet.metrics import PacketInfo

                        packets = [
                            PacketInfo(
                                timestamp=p.get("timestamp", 0.0),
                                size=p.get("size", 0),
                                sequence=p.get("sequence"),
                            )
                            for p in data
                        ]
                        return [packets], {}
                    except Exception as e:
                        logger.debug(f"Failed to convert to PacketInfo: {e}")
                        return None, {}
            return None, {}

        # Check if data is a trace-like object (has .data and .metadata)
        is_trace = hasattr(data, "data") and hasattr(data, "metadata")

        # Extract raw data and sample rate using config-aware method
        if is_trace:
            raw_data = data.data
            sample_rate = self._get_effective_sample_rate(data, context="general")
        elif isinstance(data, np.ndarray):
            raw_data = data
            sample_rate = self._get_effective_sample_rate(data, context="general")
        elif isinstance(data, bytes | bytearray):
            raw_data = np.frombuffer(data, dtype=np.uint8)
            sample_rate = self._get_effective_sample_rate(data, context="binary")
        else:
            # Try to convert to array
            try:
                raw_data = np.array(data) if hasattr(data, "__iter__") else None
            except (ValueError, TypeError):
                raw_data = None
            sample_rate = self._get_effective_sample_rate(data, context="general")

        if raw_data is None or (hasattr(raw_data, "__len__") and len(raw_data) == 0):
            return None, {}

        kwargs: dict[str, Any] = {}

        # Common parameter mappings
        if "sample_rate" in params:
            kwargs["sample_rate"] = sample_rate
        if "fs" in params:
            kwargs["fs"] = sample_rate
        if "rate" in params:
            kwargs["rate"] = sample_rate

        # DIGITAL domain parameter auto-detection
        if "baud_rate" in params:
            # Check if baud_rate parameter has a default value
            param_info = sig.parameters.get("baud_rate")
            has_default = (
                param_info is not None and param_info.default is not inspect.Parameter.empty
            )

            # Only auto-detect if no default or default is None
            if not has_default or (param_info and param_info.default is None):
                # Try to detect from filename
                detected_baud = self._detect_baud_rate_from_filename(self._input_path)
                if detected_baud is not None:
                    kwargs["baud_rate"] = detected_baud

        if "logic_family" in params:
            # Check if logic_family parameter has a default value
            param_info = sig.parameters.get("logic_family")
            has_default = (
                param_info is not None and param_info.default is not inspect.Parameter.empty
            )

            # Only auto-detect if no default or default is "auto"
            if not has_default or (param_info and param_info.default in (None, "auto")):
                # Try to detect from voltage levels
                try:
                    detected_family = self._detect_logic_family(raw_data)
                    kwargs["logic_family"] = detected_family
                except Exception as e:
                    logger.debug(f"Could not auto-detect logic family: {e}")

        # Auto-detect frequency range for frequency-related parameters
        if "freq_min" in params or "freq_max" in params:
            try:
                freq_range = self._detect_frequency_range(raw_data, sample_rate)
                if freq_range is not None:
                    min_freq, max_freq = freq_range
                    if "freq_min" in params:
                        param_info = sig.parameters.get("freq_min")
                        has_default = (
                            param_info is not None
                            and param_info.default is not inspect.Parameter.empty
                        )
                        if not has_default or (param_info and param_info.default is None):
                            kwargs["freq_min"] = min_freq
                    if "freq_max" in params:
                        param_info = sig.parameters.get("freq_max")
                        has_default = (
                            param_info is not None
                            and param_info.default is not inspect.Parameter.empty
                        )
                        if not has_default or (param_info and param_info.default is None):
                            kwargs["freq_max"] = max_freq
            except Exception as e:
                logger.debug(f"Could not auto-detect frequency range: {e}")

        # Auto-detect noise floor for threshold parameters
        if "noise_threshold" in params or "snr_threshold" in params:
            try:
                noise_floor = self._detect_noise_floor(raw_data)
                if noise_floor is not None:
                    if "noise_threshold" in params:
                        param_info = sig.parameters.get("noise_threshold")
                        has_default = (
                            param_info is not None
                            and param_info.default is not inspect.Parameter.empty
                        )
                        if not has_default or (param_info and param_info.default is None):
                            # Set threshold to 3 sigma (99.7% confidence)
                            kwargs["noise_threshold"] = noise_floor * 3.0
                    if "snr_threshold" in params:
                        param_info = sig.parameters.get("snr_threshold")
                        has_default = (
                            param_info is not None
                            and param_info.default is not inspect.Parameter.empty
                        )
                        if not has_default or (param_info and param_info.default is None):
                            # Calculate signal RMS and set reasonable SNR threshold
                            signal_rms = float(np.std(raw_data))
                            if noise_floor > 0:
                                detected_snr = signal_rms / noise_floor
                                # Use half the detected SNR as threshold
                                kwargs["snr_threshold"] = detected_snr / 2.0
            except Exception as e:
                logger.debug(f"Could not auto-detect noise floor: {e}")

        # Use protocol hints to assist with baud rate detection if not already set
        if "baud_rate" in params and "baud_rate" not in kwargs:
            try:
                protocol_hints = self._detect_protocol_hints(raw_data, sample_rate)
                if "detected_baud" in protocol_hints:
                    param_info = sig.parameters.get("baud_rate")
                    has_default = (
                        param_info is not None and param_info.default is not inspect.Parameter.empty
                    )
                    if not has_default or (param_info and param_info.default is None):
                        kwargs["baud_rate"] = protocol_hints["detected_baud"]
                        logger.debug(
                            f"Using protocol-detected baud rate: {protocol_hints['detected_baud']} bps"
                        )
            except Exception as e:
                logger.debug(f"Could not use protocol hints for baud detection: {e}")

        # Add intelligent defaults for common missing parameters (data-dependent)
        data_length = len(raw_data) if hasattr(raw_data, "__len__") else 0

        if "window_size" in params:
            param_info = sig.parameters.get("window_size")
            has_default = (
                param_info is not None and param_info.default is not inspect.Parameter.empty
            )
            if not has_default and "window_size" not in kwargs:
                # Default to 10% of signal length, minimum 10 samples
                kwargs["window_size"] = max(10, data_length // 10)
                logger.debug(f"Using auto-detected window_size: {kwargs['window_size']}")

        if "min_width" in params:
            param_info = sig.parameters.get("min_width")
            has_default = (
                param_info is not None and param_info.default is not inspect.Parameter.empty
            )
            if not has_default and "min_width" not in kwargs:
                # Default to 10 samples in time, minimum 1ns
                kwargs["min_width"] = max(1e-9, 10.0 / sample_rate)
                logger.debug(f"Using auto-detected min_width: {kwargs['min_width']:.2e}s")

        if "max_width" in params:
            param_info = sig.parameters.get("max_width")
            has_default = (
                param_info is not None and param_info.default is not inspect.Parameter.empty
            )
            if not has_default and "max_width" not in kwargs:
                # Default to signal duration, maximum 1ms
                total_duration = data_length / sample_rate if data_length > 0 else 1e-3
                kwargs["max_width"] = min(1e-3, total_duration)
                logger.debug(f"Using auto-detected max_width: {kwargs['max_width']:.2e}s")

        if "threshold" in params and "threshold" not in kwargs:
            param_info = sig.parameters.get("threshold")
            has_default = (
                param_info is not None and param_info.default is not inspect.Parameter.empty
            )
            if not has_default or (param_info and param_info.default in (None, "auto")):
                # Auto-detect threshold from histogram or use midpoint
                try:
                    if isinstance(raw_data, np.ndarray) and raw_data.size > 0:
                        kwargs["threshold"] = float(np.median(raw_data))
                        logger.debug(f"Using auto-detected threshold: {kwargs['threshold']:.3f}")
                except Exception as e:
                    logger.debug(f"Could not auto-detect threshold: {e}")

        if "window_duration" in params:
            param_info = sig.parameters.get("window_duration")
            has_default = (
                param_info is not None and param_info.default is not inspect.Parameter.empty
            )
            if not has_default and "window_duration" not in kwargs:
                # Default to 1 second or total duration / 10
                total_duration = data_length / sample_rate if data_length > 0 else 1.0
                kwargs["window_duration"] = min(1.0, total_duration / 10.0)
                logger.debug(
                    f"Using auto-detected window_duration: {kwargs['window_duration']:.3f}s"
                )

        # Create trace wrapper if function expects trace but we have raw array
        if not is_trace and (
            "Trace" in annotation_str or "WaveformTrace" in annotation_str or first_param == "trace"
        ):
            # Wrap raw array in WaveformTrace with default metadata
            try:
                # Convert memoryview to ndarray if needed
                trace_data = np.asarray(raw_data) if isinstance(raw_data, memoryview) else raw_data
                metadata = TraceMetadata(sample_rate=sample_rate)
                data = WaveformTrace(data=trace_data, metadata=metadata)
                is_trace = True
                logger.debug("Created WaveformTrace wrapper for raw array data")
            except Exception as e:
                logger.debug(f"Could not create trace wrapper: {e}")
                return None, {}

        # If function expects WaveformTrace and we have a trace, pass it directly
        if is_trace and (
            "Trace" in annotation_str or "WaveformTrace" in annotation_str or first_param == "trace"
        ):
            return [data], kwargs

        if first_param in ("data", "signal", "x", "samples", "waveform"):
            return [raw_data], kwargs
        elif first_param == "trace" and not is_trace:
            # Function expects trace but we don't have one, skip
            return None, {}
        elif first_param == "edges":
            # Jitter/timing functions need edge timestamps
            # Try to detect edges from the data
            try:
                from tracekit.analyzers.digital import detect_edges

                if is_trace:
                    edges = detect_edges(data)
                    edge_times = edges.tolist() if len(edges) > 0 else []
                    if len(edge_times) < 3:
                        return None, {}
                    return [edge_times], kwargs
            except Exception:
                return None, {}
        elif first_param == "periods":
            # Timing functions need period measurements
            # Compute periods from waveform or digital trace
            try:
                if is_trace:
                    from tracekit.analyzers.waveform.measurements import period

                    # Get all periods
                    periods_result = period(data, return_all=True)
                    if isinstance(periods_result, np.ndarray) and len(periods_result) >= 3:
                        return [periods_result], kwargs
                return None, {}
            except Exception as e:
                logger.debug(f"Could not compute periods: {e}")
                return None, {}
        elif first_param in ("stream", "data") and "bytes" in annotation_str:
            # Functions expecting bytes - convert ndarray to bytes if needed
            if isinstance(data, bytes | bytearray):
                return [data], kwargs
            elif isinstance(raw_data, np.ndarray):
                return [raw_data.astype(np.uint8).tobytes()], kwargs
            else:
                return None, {}
        elif first_param == "bytes" or (first_param == "data" and "bytes" in str(sig)):
            # Entropy/binary functions need bytes
            if isinstance(data, bytes | bytearray):
                return [data], kwargs
            elif hasattr(raw_data, "astype"):
                return [raw_data.astype(np.uint8).tobytes()], kwargs
            else:
                return None, {}

        # Default: pass raw data
        return [raw_data], kwargs


__all__ = [
    "AnalysisEngine",
]
