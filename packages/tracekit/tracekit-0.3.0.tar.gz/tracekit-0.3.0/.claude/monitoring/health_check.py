#!/usr/bin/env python3
"""
Orchestration Health Check System

Monitors:
- Hook execution times
- Agent states
- Context usage metrics
- Error rates

Provides dashboard output for quick status assessment.

Version: 1.0.0
Created: 2025-12-25
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

# Configuration
SCRIPT_DIR = Path(__file__).parent.resolve()
REPO_ROOT = SCRIPT_DIR.parent.parent
PROJECT_DIR = Path(os.environ.get("CLAUDE_PROJECT_DIR", str(REPO_ROOT)))

HOOKS_DIR = PROJECT_DIR / ".claude" / "hooks"
REGISTRY_FILE = PROJECT_DIR / ".claude" / "agent-registry.json"
METRICS_FILE = HOOKS_DIR / "orchestration-metrics.json"
HOOK_LOG = HOOKS_DIR / "hook.log"
ERROR_LOG = HOOKS_DIR / "errors.log"
CONTEXT_METRICS = HOOKS_DIR / "context_metrics.log"


def get_agent_health() -> dict[str, Any]:
    """Check agent registry health."""
    result = {
        "status": "unknown",
        "total": 0,
        "running": 0,
        "completed": 0,
        "failed": 0,
        "stale": 0,
        "issues": [],
    }

    if not REGISTRY_FILE.exists():
        result["status"] = "missing"
        result["issues"].append("Registry file not found")
        return result

    try:
        with open(REGISTRY_FILE) as f:
            registry = json.load(f)

        agents = registry.get("agents", {})
        result["total"] = len(agents)

        now = datetime.now(timezone.utc)
        stale_threshold = timedelta(hours=24)

        for agent_id, agent in agents.items():
            status = agent.get("status", "unknown")

            if status == "running":
                result["running"] += 1

                # Check if stale
                launched = agent.get("launched_at")
                if launched:
                    try:
                        launch_time = datetime.fromisoformat(launched.replace("Z", "+00:00"))
                        if (now - launch_time) > stale_threshold:
                            result["stale"] += 1
                    except (ValueError, TypeError):
                        pass

            elif status == "completed":
                result["completed"] += 1
            elif status == "failed":
                result["failed"] += 1

        # Determine overall status
        if result["stale"] > 0:
            result["status"] = "warning"
            result["issues"].append(f"{result['stale']} stale agents detected")
        elif result["failed"] > result["completed"] and result["failed"] > 0:
            result["status"] = "warning"
            result["issues"].append("High failure rate")
        else:
            result["status"] = "healthy"

    except json.JSONDecodeError:
        result["status"] = "error"
        result["issues"].append("Registry file is corrupted")
    except Exception as e:
        result["status"] = "error"
        result["issues"].append(str(e))

    return result


def get_hook_health() -> dict[str, Any]:
    """Check hook execution health."""
    result = {
        "status": "unknown",
        "hooks_available": 0,
        "hooks_executable": 0,
        "recent_errors": 0,
        "issues": [],
    }

    # Check hook files
    hooks = list(HOOKS_DIR.glob("*.sh")) + list(HOOKS_DIR.glob("*.py"))
    result["hooks_available"] = len(hooks)

    for hook in hooks:
        if hook.suffix == ".sh" and os.access(hook, os.X_OK):
            result["hooks_executable"] += 1
        elif hook.suffix == ".py":
            result["hooks_executable"] += 1

    # Check for recent errors
    if ERROR_LOG.exists():
        try:
            content = ERROR_LOG.read_text()
            lines = content.strip().split("\n") if content.strip() else []

            now = datetime.now()
            recent_threshold = timedelta(hours=1)

            for line in lines[-100:]:  # Check last 100 lines
                try:
                    # Parse timestamp from log line
                    if line.startswith("["):
                        timestamp_str = line[1 : line.index("]")]
                        log_time = datetime.fromisoformat(timestamp_str)
                        if (now - log_time) < recent_threshold:
                            result["recent_errors"] += 1
                except (ValueError, IndexError):
                    pass

        except Exception:
            pass

    # Determine status
    if result["hooks_executable"] < result["hooks_available"]:
        result["status"] = "warning"
        result["issues"].append(
            f"{result['hooks_available'] - result['hooks_executable']} hooks not executable"
        )
    elif result["recent_errors"] > 5:
        result["status"] = "warning"
        result["issues"].append(f"{result['recent_errors']} errors in last hour")
    else:
        result["status"] = "healthy"

    return result


def get_context_health() -> dict[str, Any]:
    """Check context usage health."""
    result = {
        "status": "unknown",
        "estimated_usage_percent": 0,
        "warning_level": "unknown",
        "issues": [],
    }

    # Run context check
    context_script = HOOKS_DIR / "check_context_usage.sh"
    if not context_script.exists():
        result["status"] = "unavailable"
        result["issues"].append("Context check script not found")
        return result

    try:
        proc = subprocess.run(
            [str(context_script)],
            capture_output=True,
            text=True,
            timeout=10,
            env={**os.environ, "CLAUDE_PROJECT_DIR": str(PROJECT_DIR)},
        )

        if proc.returncode in [0, 1, 2]:  # OK, high, critical
            data = json.loads(proc.stdout)
            result["estimated_usage_percent"] = data.get("percentage", 0)
            result["warning_level"] = data.get("warning_level", "unknown")

            if result["warning_level"] in ["critical"]:
                result["status"] = "critical"
                result["issues"].append("Context usage critical - compact immediately")
            elif result["warning_level"] in ["high"]:
                result["status"] = "warning"
                result["issues"].append("Context usage high - consider cleanup")
            else:
                result["status"] = "healthy"
        else:
            result["status"] = "error"
            result["issues"].append(f"Context check failed: {proc.stderr}")

    except subprocess.TimeoutExpired:
        result["status"] = "timeout"
        result["issues"].append("Context check timed out")
    except json.JSONDecodeError:
        result["status"] = "error"
        result["issues"].append("Invalid context check output")
    except Exception as e:
        result["status"] = "error"
        result["issues"].append(str(e))

    return result


def get_metrics_health() -> dict[str, Any]:
    """Check orchestration metrics health."""
    result = {
        "status": "unknown",
        "batches_executed": 0,
        "recovery_actions": 0,
        "compaction_events": 0,
        "context_peak_percent": 0,
        "issues": [],
    }

    if not METRICS_FILE.exists():
        result["status"] = "no_data"
        result["issues"].append("No metrics data available")
        return result

    try:
        with open(METRICS_FILE) as f:
            metrics = json.load(f)

        result["batches_executed"] = metrics.get("batches_executed", 0)
        result["recovery_actions"] = metrics.get("recovery_actions", 0)
        result["compaction_events"] = metrics.get("compaction_events", 0)
        result["context_peak_percent"] = metrics.get("context_usage_peak_percent", 0)

        # High recovery/compaction may indicate issues
        if result["recovery_actions"] > 5:
            result["status"] = "warning"
            result["issues"].append(f"High recovery action count: {result['recovery_actions']}")
        elif result["compaction_events"] > 10:
            result["status"] = "warning"
            result["issues"].append(f"High compaction count: {result['compaction_events']}")
        else:
            result["status"] = "healthy"

    except Exception as e:
        result["status"] = "error"
        result["issues"].append(str(e))

    return result


def run_health_check() -> dict[str, Any]:
    """Run comprehensive health check."""
    now = datetime.now(timezone.utc)

    health = {
        "timestamp": now.isoformat(),
        "overall_status": "healthy",
        "components": {
            "agents": get_agent_health(),
            "hooks": get_hook_health(),
            "context": get_context_health(),
            "metrics": get_metrics_health(),
        },
        "all_issues": [],
    }

    # Aggregate issues and determine overall status
    critical_count = 0
    warning_count = 0

    for component, data in health["components"].items():
        status = data.get("status", "unknown")
        issues = data.get("issues", [])

        for issue in issues:
            health["all_issues"].append(f"[{component}] {issue}")

        if status == "critical":
            critical_count += 1
        elif status in ["warning", "error"]:
            warning_count += 1

    if critical_count > 0:
        health["overall_status"] = "critical"
    elif warning_count > 0:
        health["overall_status"] = "warning"
    else:
        health["overall_status"] = "healthy"

    return health


def format_dashboard(health: dict[str, Any]) -> str:
    """Format health check as dashboard."""
    status_icons = {
        "healthy": "[OK]",
        "warning": "[WARN]",
        "critical": "[CRIT]",
        "error": "[ERR]",
        "unknown": "[?]",
        "unavailable": "[N/A]",
        "no_data": "[N/A]",
    }

    lines = [
        "=" * 60,
        "ORCHESTRATION HEALTH DASHBOARD",
        f"Timestamp: {health['timestamp']}",
        "=" * 60,
        "",
        f"Overall Status: {status_icons.get(health['overall_status'], '[?]')} {health['overall_status'].upper()}",
        "",
        "-" * 40,
        "Component Status",
        "-" * 40,
    ]

    for component, data in health["components"].items():
        status = data.get("status", "unknown")
        icon = status_icons.get(status, "[?]")
        lines.append(f"  {component.capitalize():12} {icon} {status}")

    # Agent details
    agents = health["components"]["agents"]
    if agents.get("total", 0) > 0:
        lines.extend(
            [
                "",
                "-" * 40,
                "Agent Details",
                "-" * 40,
                f"  Total:     {agents.get('total', 0)}",
                f"  Running:   {agents.get('running', 0)}",
                f"  Completed: {agents.get('completed', 0)}",
                f"  Failed:    {agents.get('failed', 0)}",
                f"  Stale:     {agents.get('stale', 0)}",
            ]
        )

    # Context details
    context = health["components"]["context"]
    if context.get("status") not in ["unavailable", "unknown"]:
        lines.extend(
            [
                "",
                "-" * 40,
                "Context Usage",
                "-" * 40,
                f"  Usage:  {context.get('estimated_usage_percent', 0)}%",
                f"  Level:  {context.get('warning_level', 'unknown')}",
            ]
        )

    # Issues
    if health["all_issues"]:
        lines.extend(
            [
                "",
                "-" * 40,
                "Issues",
                "-" * 40,
            ]
        )
        for issue in health["all_issues"]:
            lines.append(f"  - {issue}")

    lines.extend(["", "=" * 60])

    return "\n".join(lines)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Orchestration health check")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument(
        "--component",
        choices=["agents", "hooks", "context", "metrics"],
        help="Check specific component",
    )
    args = parser.parse_args()

    if args.component:
        # Check specific component
        if args.component == "agents":
            result = get_agent_health()
        elif args.component == "hooks":
            result = get_hook_health()
        elif args.component == "context":
            result = get_context_health()
        elif args.component == "metrics":
            result = get_metrics_health()

        print(json.dumps(result, indent=2))
        sys.exit(0 if result.get("status") == "healthy" else 1)

    # Full health check
    health = run_health_check()

    if args.json:
        print(json.dumps(health, indent=2))
    else:
        print(format_dashboard(health))

    # Exit code based on status
    if health["overall_status"] == "critical":
        sys.exit(2)
    elif health["overall_status"] == "warning":
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
