"""TraceKit Command-Line Interface.

This module provides command-line tools for signal analysis workflows.


Example:
    $ tracekit --help
    $ tracekit characterize signal.wfm
    $ tracekit decode uart.wfm --protocol uart
"""

from tracekit.cli.main import cli

__all__ = ["cli"]
