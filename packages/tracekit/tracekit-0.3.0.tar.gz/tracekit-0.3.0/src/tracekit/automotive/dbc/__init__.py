"""DBC database support for CAN signal definitions.

This module provides DBC file parsing and generation capabilities.
"""

from __future__ import annotations

__all__ = ["DBCGenerator", "DBCParser", "load_dbc"]

try:
    from tracekit.automotive.dbc.generator import DBCGenerator
    from tracekit.automotive.dbc.parser import DBCParser, load_dbc
except ImportError:
    # Optional dependencies not installed
    pass
