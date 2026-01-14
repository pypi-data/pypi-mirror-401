"""TraceKit - Signal analysis framework for oscilloscope and logic analyzer data.

TraceKit provides comprehensive tools for:
- Waveform analysis (rise/fall time, frequency, amplitude)
- Digital signal analysis (edge detection, clock recovery)
- Spectral analysis (FFT, PSD, THD, SNR, SINAD, ENOB)
- Protocol decoding (UART, SPI, I2C, CAN, 1-Wire, and more)
- Signal filtering (IIR, FIR, Butterworth, Chebyshev, Bessel, Elliptic)
- Triggering (edge, pattern, pulse width, glitch, runt, window)
- Power analysis (AC/DC, switching, SOA, efficiency, ripple)
- Arithmetic operations (add, subtract, differentiate, integrate)
- Comparison and limit testing (golden waveform, mask testing)
- Component analysis (TDR, impedance, capacitance, inductance)
- Statistical analysis and distribution metrics
- Memory management and large file handling
- Professional report generation
- EMC compliance testing
- Session management
- Data visualization and export

Example:
    >>> import tracekit as tk
    >>> trace = tk.load("capture.wfm")
    >>> print(f"Rise time: {tk.rise_time(trace):.2e} s")
    >>> freq, mag = tk.fft(trace)
    >>> print(f"THD: {tk.thd(trace):.1f} dB")
    >>> # Filtering
    >>> filtered = tk.low_pass(trace, cutoff=1e6)
    >>> # Power analysis
    >>> power = tk.instantaneous_power(v_trace, i_trace)
    >>> # Math operations
    >>> combined = tk.add(trace1, trace2)
    >>> derivative = tk.differentiate(trace)
    >>> # Session management
    >>> session = tk.Session()
    >>> session.load_trace('capture.wfm')
    >>> session.annotate(time=1.5e-6, text='Glitch')
    >>> session.save('debug_session.tks')
    >>> # Multi-channel loading
    >>> channels = tk.load_all_channels("multi_ch.wfm")
    >>> for name, ch_trace in channels.items():
    ...     print(f"{name}: {len(ch_trace.data)} samples")

For more information, see https://github.com/lair-click-bats/tracekit
"""

__version__ = "0.3.1"
__author__ = "lair-click-bats"

# Core types
# Digital analysis (top-level convenience access)
from tracekit.analyzers.digital.extraction import (
    LOGIC_FAMILIES,
    detect_edges,
    to_digital,
)

# Signal quality analysis (QUAL-001, QUAL-002, QUAL-005, QUAL-006, QUAL-007)
from tracekit.analyzers.digital.quality import (
    Glitch,
    MaskTestResult,
    NoiseMarginResult,
    PLLRecoveryResult,
    Violation,
    detect_glitches,
    detect_violations,
    noise_margin,
    pll_clock_recovery,
    signal_quality_summary,
)
from tracekit.analyzers.power.ac_power import (
    apparent_power,
    power_factor,
    reactive_power,
)

# Power analysis (top-level convenience access)
from tracekit.analyzers.power.basic import (
    average_power,
    energy,
    instantaneous_power,
    power_statistics,
)
from tracekit.analyzers.power.efficiency import (
    efficiency,
)
from tracekit.analyzers.power.ripple import (
    ripple,
    ripple_statistics,
)

# Protocol decoders (top-level convenience access)
from tracekit.analyzers.protocols import (
    decode_can,
    decode_can_fd,
    decode_flexray,
    decode_hdlc,
    decode_i2c,
    decode_i2s,
    decode_jtag,
    decode_lin,
    decode_manchester,
    decode_onewire,
    decode_spi,
    decode_swd,
    decode_uart,
    decode_usb,
)

# Statistics (top-level convenience access)
from tracekit.analyzers.statistics.basic import (
    basic_stats,
    percentiles,
    quartiles,
)
from tracekit.analyzers.statistics.distribution import (
    distribution_metrics,
    histogram,
)

# Waveform measurements (top-level convenience access)
from tracekit.analyzers.waveform.measurements import (
    amplitude,
    duty_cycle,
    fall_time,
    frequency,
    mean,
    measure,
    overshoot,
    period,
    preshoot,
    pulse_width,
    rise_time,
    rms,
    undershoot,
)

# Convenience aliases
vpp = amplitude  # Vpp (peak-to-peak voltage) is a common oscilloscope term

# Spectral analysis (top-level convenience access)
from tracekit.analyzers.waveform.spectral import (
    enob,
    fft,
    psd,
    sfdr,
    sinad,
    snr,
    spectrogram,
    thd,
)

# Comparison and limit testing
from tracekit.comparison.compare import (
    compare_traces,
    correlation,
    difference,
    similarity_score,
)
from tracekit.comparison.golden import (
    GoldenReference,
    compare_to_golden,
    create_golden,
)
from tracekit.comparison.limits import (
    LimitSpec,
    check_limits,
    create_limit_spec,
    margin_analysis,
)
from tracekit.comparison.mask import (
    Mask,
    create_mask,
    eye_mask,
    mask_test,
)

# EMC Compliance (EMC-001, EMC-002, EMC-003)
from tracekit.compliance import (
    AVAILABLE_MASKS,
    ComplianceReportFormat,
    ComplianceResult,
    ComplianceViolation,
    DetectorType,
    LimitMask,
    check_compliance,
    create_custom_mask,
    generate_compliance_report,
    load_limit_mask,
)

# Component analysis
from tracekit.component.impedance import (
    discontinuity_analysis,
    extract_impedance,
    impedance_profile,
)
from tracekit.component.reactive import (
    extract_parasitics,
    measure_capacitance,
    measure_inductance,
)
from tracekit.component.transmission_line import (
    characteristic_impedance,
    propagation_delay,
    transmission_line_analysis,
    velocity_factor,
)

# Audit trail (LOG-009)
from tracekit.core.audit import (
    AuditEntry,
    AuditTrail,
    get_global_audit_trail,
    record_audit,
)

# Configuration
from tracekit.core.config import (
    DEFAULT_CONFIG,
    SmartDefaults,
    get_config_value,
    load_config,
    save_config,
    validate_config,
)

# Exceptions - import from core.exceptions (the enhanced version)
from tracekit.core.exceptions import (
    AnalysisError,
    ConfigurationError,
    ExportError,
    FormatError,
    InsufficientDataError,
    LoaderError,
    SampleRateError,
    TraceKitError,
    UnsupportedFormatError,
    ValidationError,
)

# Logging
from tracekit.core.logging import (
    configure_logging,
    get_logger,
    set_log_level,
)

# Performance timing
from tracekit.core.performance import timed

# Expert API - Results (API-005)
from tracekit.core.results import (
    AnalysisResult,
    FFTResult,
    FilterResult,
    MeasurementResult,
    WaveletResult,
)
from tracekit.core.types import (
    DigitalTrace,
    ProtocolPacket,
    Trace,
    TraceMetadata,
    WaveformTrace,
)

# Data Export (top-level convenience access)
from tracekit.exporters import (
    export_csv,
    export_hdf5,
    export_json,
    export_mat,
)

# Expert API - Extensibility (API-006, API-007, API-008, PLUG-008)
from tracekit.extensibility import (
    AlgorithmRegistry,
    MeasurementDefinition,
    MeasurementRegistry,
    PluginError,
    PluginManager,
    PluginMetadata,
    PluginTemplate,
    PluginType,
    generate_plugin_template,
    get_algorithm,
    get_algorithms,
    get_measurement_registry,
    get_plugin_manager,
    list_measurements,
    list_plugins,
    load_plugin,
    register_algorithm,
    register_measurement,
)
from tracekit.extensibility import (
    measure as measure_custom,
)

# Filtering (top-level convenience access)
from tracekit.filtering.convenience import (
    band_pass,
    band_stop,
    high_pass,
    low_pass,
    median_filter,
    moving_average,
    notch_filter,
    savgol_filter,
)
from tracekit.filtering.design import (
    BandPassFilter,
    BandStopFilter,
    HighPassFilter,
    LowPassFilter,
    design_filter,
)

# Auto-Inference (INF-001 to INF-009)
from tracekit.inference import (
    AnalysisRecommendation,
    assess_signal_quality,
    auto_spectral_config,
    check_measurement_suitability,
    classify_signal,
    detect_logic_family,
    detect_protocol,
    get_optimal_domain_order,
    recommend_analyses,
    suggest_measurements,
)

# Loaders (including multi-channel support)
from tracekit.loaders import get_supported_formats, load, load_all_channels

# Math/arithmetic operations (top-level convenience access)
from tracekit.math.arithmetic import (
    absolute,
    add,
    differentiate,
    divide,
    integrate,
    invert,
    math_expression,
    multiply,
    offset,
    scale,
    subtract,
)
from tracekit.math.interpolation import (
    align_traces,
    downsample,
    interpolate,
    resample,
)

# Expert API - Pipeline and Composition (API-001, API-002, API-004)
from tracekit.pipeline import (
    Composable,
    Pipeline,
    TraceTransformer,
    compose,
    curry,
    make_composable,
    pipe,
)

# Reporting
from tracekit.reporting.core import (
    Report,
    ReportConfig,
    generate_report,
)
from tracekit.reporting.formatting import (
    NumberFormatter,
    format_value,
    format_with_context,
    format_with_units,
)

# Session Management (SESS-001, SESS-002, SESS-003)
from tracekit.session import (
    Annotation,
    AnnotationLayer,
    AnnotationType,
    HistoryEntry,
    OperationHistory,
    Session,
    load_session,
)

# Expert API - Streaming (API-003)
from tracekit.streaming import (
    StreamingAnalyzer,
    load_trace_chunks,
)

# Triggering (top-level convenience access)
from tracekit.triggering import (
    EdgeTrigger,
    PulseWidthTrigger,
    find_falling_edges,
    find_glitches,
    find_pulses,
    find_rising_edges,
    find_runt_pulses,
    find_triggers,
)

# Memory management
from tracekit.utils.memory import (
    MemoryCheckError,
    check_memory_available,
    estimate_memory,
    get_available_memory,
    get_memory_pressure,
    get_total_memory,
)

# Visualization (top-level convenience access)
from tracekit.visualization import (
    plot_fft,
    plot_spectrum,
    plot_waveform,
)

# Workflows (WRK-001 to WRK-005)
from tracekit.workflows import (
    characterize_buffer,
    debug_protocol,
    emc_compliance_test,
    power_analysis,
    signal_integrity_audit,
)

__all__ = [
    # EMC Compliance (EMC-001, EMC-002, EMC-003)
    "AVAILABLE_MASKS",
    "DEFAULT_CONFIG",
    "LOGIC_FAMILIES",
    # Expert API - Extensibility (API-006, API-007, API-008)
    "AlgorithmRegistry",
    "AnalysisError",
    # Auto-Inference (INF-009)
    "AnalysisRecommendation",
    # Expert API - Results (API-005)
    "AnalysisResult",
    # Session Management (SESS-002)
    "Annotation",
    "AnnotationLayer",
    "AnnotationType",
    # Audit trail (LOG-009)
    "AuditEntry",
    "AuditTrail",
    "BandPassFilter",
    "BandStopFilter",
    "ComplianceReportFormat",
    "ComplianceResult",
    "ComplianceViolation",
    "Composable",
    "ConfigurationError",
    "DetectorType",
    "DigitalTrace",
    "EdgeTrigger",
    "ExportError",
    "FFTResult",
    "FilterResult",
    "FormatError",
    # Signal quality (QUAL-005)
    "Glitch",
    "GoldenReference",
    "HighPassFilter",
    # Session Management (SESS-003)
    "HistoryEntry",
    "InsufficientDataError",
    "LimitMask",
    "LimitSpec",
    "LoaderError",
    "LowPassFilter",
    "Mask",
    # Signal quality (QUAL-006)
    "MaskTestResult",
    "MeasurementDefinition",
    "MeasurementRegistry",
    "MeasurementResult",
    "MemoryCheckError",
    # Signal quality (QUAL-001)
    "NoiseMarginResult",
    "NumberFormatter",
    "OperationHistory",
    # Signal quality (QUAL-007)
    "PLLRecoveryResult",
    # Expert API - Pipeline (API-001, API-002, API-004)
    "Pipeline",
    "PluginError",
    "PluginManager",
    "PluginMetadata",
    "PluginTemplate",
    "PluginType",
    "ProtocolPacket",
    "PulseWidthTrigger",
    # Reporting
    "Report",
    "ReportConfig",
    "SampleRateError",
    # Session Management (SESS-001)
    "Session",
    "SmartDefaults",
    "StreamingAnalyzer",
    "Trace",
    # Exceptions
    "TraceKitError",
    # Core types
    "TraceMetadata",
    "TraceTransformer",
    "UnsupportedFormatError",
    "ValidationError",
    # Signal quality (QUAL-002)
    "Violation",
    "WaveformTrace",
    "WaveletResult",
    # Version
    "__version__",
    "absolute",
    # Math operations
    "add",
    "align_traces",
    "amplitude",
    "apparent_power",
    "assess_signal_quality",
    "auto_spectral_config",
    "average_power",
    "band_pass",
    "band_stop",
    # Statistics
    "basic_stats",
    "characteristic_impedance",
    # Workflows (WRK-001 to WRK-005)
    "characterize_buffer",
    "check_compliance",
    "check_limits",
    "check_measurement_suitability",
    "check_memory_available",
    "classify_signal",
    "compare_to_golden",
    # Comparison
    "compare_traces",
    "compose",
    # Logging
    "configure_logging",
    "correlation",
    "create_custom_mask",
    "create_golden",
    "create_limit_spec",
    "create_mask",
    "curry",
    "debug_protocol",
    # Protocol decoders
    "decode_can",
    "decode_can_fd",
    "decode_flexray",
    "decode_hdlc",
    "decode_i2c",
    "decode_i2s",
    "decode_jtag",
    "decode_lin",
    "decode_manchester",
    "decode_onewire",
    "decode_spi",
    "decode_swd",
    "decode_uart",
    "decode_usb",
    "design_filter",
    "detect_edges",
    # Signal quality (QUAL-005)
    "detect_glitches",
    # Auto-Inference (INF-001 to INF-003)
    "detect_logic_family",
    "detect_protocol",
    # Signal quality (QUAL-002)
    "detect_violations",
    "difference",
    "differentiate",
    "discontinuity_analysis",
    "distribution_metrics",
    "divide",
    "downsample",
    "duty_cycle",
    "efficiency",
    "emc_compliance_test",
    "energy",
    "enob",
    # Memory management
    "estimate_memory",
    # Export functions
    "export_csv",
    "export_hdf5",
    "export_json",
    "export_mat",
    # Component analysis
    "extract_impedance",
    "extract_parasitics",
    "eye_mask",
    "fall_time",
    # Spectral analysis
    "fft",
    "find_falling_edges",
    "find_glitches",
    "find_pulses",
    "find_rising_edges",
    "find_runt_pulses",
    # Triggering
    "find_triggers",
    "format_value",
    "format_with_context",
    "format_with_units",
    "frequency",
    "generate_compliance_report",
    "generate_plugin_template",
    "generate_report",
    "get_algorithm",
    "get_algorithms",
    "get_available_memory",
    "get_config_value",
    "get_global_audit_trail",
    "get_logger",
    "get_measurement_registry",
    "get_memory_pressure",
    # Auto-Inference (INF-009)
    "get_optimal_domain_order",
    "get_plugin_manager",
    "get_supported_formats",
    "get_total_memory",
    "high_pass",
    "histogram",
    "impedance_profile",
    # Power analysis
    "instantaneous_power",
    "integrate",
    "interpolate",
    "invert",
    "list_measurements",
    "list_plugins",
    # Loaders
    "load",
    # Multi-channel loading (Phase 3)
    "load_all_channels",
    # Configuration
    "load_config",
    "load_limit_mask",
    "load_plugin",
    # Session Management
    "load_session",
    # Expert API - Streaming (API-003)
    "load_trace_chunks",
    # Filtering
    "low_pass",
    "make_composable",
    "margin_analysis",
    "mask_test",
    "math_expression",
    "mean",
    "measure",
    "measure_capacitance",
    "measure_custom",
    "measure_inductance",
    "median_filter",
    "moving_average",
    "multiply",
    # Signal quality (QUAL-001)
    "noise_margin",
    "notch_filter",
    "offset",
    "overshoot",
    "percentiles",
    "period",
    "pipe",
    # Signal quality (QUAL-007)
    "pll_clock_recovery",
    # Visualization
    "plot_fft",
    "plot_spectrum",
    "plot_waveform",
    "power_analysis",
    "power_factor",
    "power_statistics",
    "preshoot",
    "propagation_delay",
    "psd",
    "pulse_width",
    "quartiles",
    "reactive_power",
    # Auto-Inference (INF-009)
    "recommend_analyses",
    "record_audit",
    "register_algorithm",
    "register_measurement",
    "resample",
    "ripple",
    "ripple_statistics",
    # Waveform measurements
    "rise_time",
    "rms",
    "save_config",
    "savgol_filter",
    "scale",
    "set_log_level",
    "sfdr",
    "signal_integrity_audit",
    # Signal quality summary
    "signal_quality_summary",
    "similarity_score",
    "sinad",
    "snr",
    "spectrogram",
    "subtract",
    "suggest_measurements",
    "thd",
    "timed",
    # Digital analysis
    "to_digital",
    "transmission_line_analysis",
    "undershoot",
    "validate_config",
    "velocity_factor",
    "vpp",
]
