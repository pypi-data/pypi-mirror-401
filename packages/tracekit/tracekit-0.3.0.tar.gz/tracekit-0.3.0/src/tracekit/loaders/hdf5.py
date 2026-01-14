"""Alias module for HDF5 loader - provides expected import path.

This module re-exports from hdf5_loader.py to support:
    from tracekit.loaders.hdf5 import load_hdf5
"""

from tracekit.loaders.hdf5_loader import load_hdf5

__all__ = ["load_hdf5"]
