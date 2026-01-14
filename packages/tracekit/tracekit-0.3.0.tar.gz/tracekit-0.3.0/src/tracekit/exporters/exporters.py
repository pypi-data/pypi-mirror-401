"""Exporters namespace module.

This module provides a namespace for export functions to support:
    from tracekit.exporters import exporters
    exporters.csv(trace, "output.csv")

Re-exports main export functions with short names.
"""

from tracekit.exporters.csv import (
    export_csv as csv,
)
from tracekit.exporters.hdf5 import (
    export_hdf5 as hdf5,
)
from tracekit.exporters.html_export import (
    export_html as html,
)
from tracekit.exporters.json_export import (
    export_json as json,
)
from tracekit.exporters.markdown_export import (
    export_markdown as markdown,
)
from tracekit.exporters.matlab_export import (
    export_mat as mat,
)
from tracekit.exporters.npz_export import (
    export_npz as npz,
)
from tracekit.exporters.spice_export import (
    export_pwl as pwl,
)

__all__ = [
    "csv",
    "hdf5",
    "html",
    "json",
    "markdown",
    "mat",
    "npz",
    "pwl",
]
