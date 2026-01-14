"""
Shared configuration loader for Claude Code hooks.

This module provides a centralized way to read and access the unified
config.yaml file (Single Source of Truth for all behavioral settings).

Usage in hooks:
    from shared.config import load_config

    config = load_config()
    max_agents = config['orchestration']['agents']['max_concurrent']
    retention_days = config['retention']['agent_outputs']
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigError(Exception):
    """Raised when configuration cannot be loaded or is invalid."""

    pass


def get_project_root() -> Path:
    """
    Find the project root directory (contains .claude/).

    Returns:
        Path to project root

    Raises:
        ConfigError: If project root cannot be found
    """
    current = Path(__file__).resolve()

    # Walk up from .claude/hooks/shared/config.py
    for parent in current.parents:
        if (parent / ".claude").is_dir():
            return parent

    raise ConfigError(
        f"Could not find project root (directory containing .claude/). Started from: {current}"
    )


def load_config(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Load configuration from config.yaml.

    Args:
        config_path: Optional path to config.yaml. If None, auto-detects
                     from project root.

    Returns:
        Configuration dictionary

    Raises:
        ConfigError: If config file not found or invalid YAML

    Example:
        >>> config = load_config()
        >>> max_agents = config['orchestration']['agents']['max_concurrent']
        2
    """
    if config_path is None:
        root = get_project_root()
        config_path = root / ".claude" / "config.yaml"

    if not config_path.exists():
        raise ConfigError(
            f"Configuration file not found: {config_path}\n"
            "Expected: .claude/config.yaml in project root"
        )

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ConfigError(f"Invalid YAML in config file: {e}")
    except Exception as e:
        raise ConfigError(f"Could not read config file: {e}")

    if not isinstance(config, dict):
        raise ConfigError(f"Config file must contain a YAML dictionary, got: {type(config)}")

    return config


def get_config_value(config: Dict[str, Any], *path: str, default: Any = None) -> Any:
    """
    Safely get nested configuration value with optional default.

    Args:
        config: Configuration dictionary
        *path: Path to nested key (e.g., 'orchestration', 'agents', 'max_concurrent')
        default: Default value if key not found

    Returns:
        Configuration value or default

    Example:
        >>> config = load_config()
        >>> max_agents = get_config_value(config, 'orchestration', 'agents', 'max_concurrent', default=2)
        2
    """
    current = config

    for key in path:
        if not isinstance(current, dict):
            return default
        current = current.get(key)
        if current is None:
            return default

    return current


# Convenience functions for common config access patterns


def get_agent_limits(config: Dict[str, Any]) -> Dict[str, int]:
    """
    Get agent concurrency limits.

    Returns:
        Dictionary with max_concurrent, max_batch_size, recommended_batch_size
    """
    agents_config = config.get("orchestration", {}).get("agents", {})
    return {
        "max_concurrent": agents_config.get("max_concurrent", 2),
        "max_batch_size": agents_config.get("max_batch_size", 2),
        "recommended_batch_size": agents_config.get("recommended_batch_size", 1),
        "polling_interval_seconds": agents_config.get("polling_interval_seconds", 10),
    }


def get_retention_policy(config: Dict[str, Any], resource_type: str) -> int:
    """
    Get retention policy for a resource type.

    Args:
        config: Configuration dictionary
        resource_type: One of: agent_registry, agent_outputs, checkpoints,
                       coordination_files, handoffs, summaries, archives_max_days

    Returns:
        Retention period in days (or minutes for locks_stale_minutes)
    """
    retention = config.get("retention", {})
    return retention.get(resource_type, 30)  # Default 30 days


def get_complexity_thresholds(config: Dict[str, Any]) -> Dict[str, int]:
    """
    Get workflow complexity thresholds.

    Returns:
        Dictionary with ad_hoc_max, auto_spec_max, manual_spec_min
    """
    workflow = config.get("orchestration", {}).get("workflow", {})
    return {
        "ad_hoc_max": workflow.get("ad_hoc_max", 30),
        "auto_spec_max": workflow.get("auto_spec_max", 70),
        "manual_spec_min": workflow.get("manual_spec_min", 71),
    }


def get_context_thresholds(config: Dict[str, Any]) -> Dict[str, int]:
    """
    Get context monitoring thresholds.

    Returns:
        Dictionary with warning, checkpoint, critical thresholds (percentages)
    """
    context = config.get("orchestration", {}).get("context", {})
    return {
        "warning_threshold": context.get("warning_threshold", 60),
        "checkpoint_threshold": context.get("checkpoint_threshold", 65),
        "critical_threshold": context.get("critical_threshold", 75),
    }


def is_enforcement_enabled(config: Dict[str, Any], enforcement_type: str) -> bool:
    """
    Check if a specific enforcement is enabled.

    Args:
        config: Configuration dictionary
        enforcement_type: One of: agent_limit, auto_summarize, path_validation,
                         report_limits, context_monitoring

    Returns:
        True if enforcement is enabled
    """
    if not config.get("enforcement", {}).get("enabled", True):
        return False

    return config.get("enforcement", {}).get(enforcement_type, True)


def get_denied_paths(config: Dict[str, Any], path_type: str = "reads") -> list[str]:
    """
    Get list of denied paths for security.

    Args:
        config: Configuration dictionary
        path_type: Either 'reads' or 'writes'

    Returns:
        List of glob patterns for denied paths
    """
    security = config.get("security", {})
    key = f"denied_{path_type}"
    return security.get(key, [])


# Example usage and testing
if __name__ == "__main__":
    # Test configuration loading
    try:
        config = load_config()
        print("✅ Configuration loaded successfully")

        # Test convenience functions
        limits = get_agent_limits(config)
        print(f"✅ Agent limits: {limits}")

        thresholds = get_complexity_thresholds(config)
        print(f"✅ Complexity thresholds: {thresholds}")

        context = get_context_thresholds(config)
        print(f"✅ Context thresholds: {context}")

        retention = get_retention_policy(config, "agent_outputs")
        print(f"✅ Agent output retention: {retention} days")

        enforcement = is_enforcement_enabled(config, "agent_limit")
        print(f"✅ Agent limit enforcement: {enforcement}")

        denied_reads = get_denied_paths(config, "reads")
        print(f"✅ Denied read paths: {len(denied_reads)} patterns")

        print("\n🎉 All configuration tests passed!")

    except ConfigError as e:
        print(f"❌ Configuration error: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        exit(1)
