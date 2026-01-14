"""Jupyter and IPython integration for TraceKit.

This package provides IPython magic commands, rich display integration,
and Jupyter notebook-specific features.

  - IPython magic commands (%tracekit, %%analyze)
  - Rich HTML display for results
  - Inline plot rendering
  - Progress bars (tqdm integration)
"""

from tracekit.jupyter.display import (
    MeasurementDisplay,
    TraceDisplay,
    display_measurements,
    display_spectrum,
    display_trace,
)
from tracekit.jupyter.magic import (
    TracekitMagics,
    load_ipython_extension,
)

__all__ = [
    "MeasurementDisplay",
    "TraceDisplay",
    "TracekitMagics",
    "display_measurements",
    "display_spectrum",
    "display_trace",
    "load_ipython_extension",
]
