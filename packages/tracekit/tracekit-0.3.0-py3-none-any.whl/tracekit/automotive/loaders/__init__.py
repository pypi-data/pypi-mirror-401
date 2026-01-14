"""Automotive file format loaders.

This module provides loaders for common automotive logging file formats:
- BLF (Vector Binary Logging Format)
- ASC (Vector ASCII Format)
- MDF/MF4 (ASAM Measurement Data Format)
- CSV (Comma-Separated Values)
- PCAP (Packet Capture - SocketCAN)
"""

from __future__ import annotations

__all__ = [
    "detect_format",
    "load_asc",
    "load_automotive_log",
    "load_blf",
    "load_csv_can",
    "load_mdf",
]

try:
    from tracekit.automotive.loaders.asc import load_asc
    from tracekit.automotive.loaders.blf import load_blf
    from tracekit.automotive.loaders.csv_can import load_csv_can
    from tracekit.automotive.loaders.dispatcher import (
        detect_format,
        load_automotive_log,
    )
    from tracekit.automotive.loaders.mdf import load_mdf
except ImportError:
    # Optional dependencies not installed
    pass
