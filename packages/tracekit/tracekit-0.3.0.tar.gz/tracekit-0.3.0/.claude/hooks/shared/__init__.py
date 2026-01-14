"""Shared utilities for Claude Code hooks.

This package provides common functionality used across multiple hooks:
- paths.py: Path definitions and access
- config.py: Configuration file loading and access
"""

from .paths import PATHS, get_path, load_paths
from .config import (
    ConfigError,
    load_config,
    get_config_value,
    get_agent_limits,
    get_retention_policy,
    get_complexity_thresholds,
    get_context_thresholds,
    is_enforcement_enabled,
    get_denied_paths,
)

__all__ = [
    # Paths
    "PATHS",
    "get_path",
    "load_paths",
    # Config
    "ConfigError",
    "load_config",
    "get_config_value",
    "get_agent_limits",
    "get_retention_policy",
    "get_complexity_thresholds",
    "get_context_thresholds",
    "is_enforcement_enabled",
    "get_denied_paths",
]
