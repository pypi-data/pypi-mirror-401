"""Data export module for TraceKit.

Provides export functionality to various file formats including CSV, HDF5,
JSON, MATLAB, Markdown, HTML, NumPy NPZ, and SPICE PWL.


Example:
    >>> from tracekit.exporters import export_csv, export_hdf5, export_json, export_mat
    >>> export_csv(trace, "waveform.csv")
    >>> export_hdf5(trace, "waveform.h5")
    >>> export_json(trace, "waveform.json")
    >>> export_mat(trace, "waveform.mat")
    >>> export_markdown(data, "report.md")
    >>> export_html(data, "report.html")
    >>> export_npz(trace, "waveform.npz")
    >>> export_pwl(trace, "stimulus.pwl")
"""

# Import exporters module as namespace for DSL compatibility
from tracekit.exporters import exporters
from tracekit.exporters.csv import (
    export_csv,
    export_multi_trace_csv,
)
from tracekit.exporters.hdf5 import (
    append_trace,
    export_hdf5,
    export_measurement_results,
)
from tracekit.exporters.html_export import (
    export_html,
    generate_html_report,
)
from tracekit.exporters.json_export import (
    TraceKitJSONEncoder,
    export_json,
    export_measurements,
    export_protocol_decode,
    load_json,
)
from tracekit.exporters.markdown_export import (
    export_markdown,
    generate_markdown_report,
)
from tracekit.exporters.matlab_export import (
    export_mat,
    export_multi_trace_mat,
)
from tracekit.exporters.npz_export import (
    export_npz,
    load_npz,
)
from tracekit.exporters.spice_export import (
    export_pwl,
    export_pwl_multi,
    generate_spice_source,
)

__all__ = [
    "TraceKitJSONEncoder",
    "append_trace",
    # CSV export (EXP-001)
    "export_csv",
    # HDF5 export (EXP-002)
    "export_hdf5",
    # HTML export (EXP-007)
    "export_html",
    # JSON export (EXP-003)
    "export_json",
    # Markdown export (EXP-006)
    "export_markdown",
    # MATLAB export (EXP-008)
    "export_mat",
    "export_measurement_results",
    "export_measurements",
    "export_multi_trace_csv",
    "export_multi_trace_mat",
    # NPZ export (EXP-004)
    "export_npz",
    "export_protocol_decode",
    # SPICE PWL export (EXP-005)
    "export_pwl",
    "export_pwl_multi",
    "exporters",
    # HTML report generation
    "generate_html_report",
    # Markdown report generation
    "generate_markdown_report",
    # SPICE source generation
    "generate_spice_source",
    "load_json",
    # NPZ loading
    "load_npz",
]
