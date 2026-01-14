"""TraceKit Core CLI Framework implementing CLI-001.

Provides the main entry point for the tracekit command-line interface with
support for multiple output formats and verbose logging.


Example:
    $ tracekit --help
    $ tracekit characterize signal.wfm --output json
    $ tracekit decode uart.wfm -vv
    $ tracekit shell   # Interactive REPL
"""

from __future__ import annotations

import json
import logging
import sys
from typing import Any

import click

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING,
)
logger = logging.getLogger("tracekit")


class OutputFormat:
    """Output format handler for CLI results.

    Supports JSON, CSV, HTML, and table (default) output formats.
    """

    @staticmethod
    def json(data: dict[str, Any]) -> str:
        """Format as JSON."""
        return json.dumps(data, indent=2, default=str)

    @staticmethod
    def csv(data: dict[str, Any]) -> str:
        """Format as CSV (simplified)."""
        lines = ["key,value"]
        for key, value in data.items():
            if isinstance(value, dict):
                # Nested dict - flatten
                for subkey, subvalue in value.items():
                    lines.append(f"{key}.{subkey},{subvalue}")
            elif isinstance(value, list):
                lines.append(f'{key},"{",".join(map(str, value))}"')
            else:
                lines.append(f"{key},{value}")
        return "\n".join(lines)

    @staticmethod
    def html(data: dict[str, Any]) -> str:
        """Format as HTML."""
        html_parts = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            "<meta charset='utf-8'>",
            "<title>TraceKit Analysis Results</title>",
            "<style>",
            "body { font-family: Arial, sans-serif; margin: 20px; }",
            "table { border-collapse: collapse; width: 100%; }",
            "th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }",
            "th { background-color: #4CAF50; color: white; }",
            "tr:nth-child(even) { background-color: #f2f2f2; }",
            "</style>",
            "</head>",
            "<body>",
            "<h1>TraceKit Analysis Results</h1>",
            "<table>",
            "<tr><th>Parameter</th><th>Value</th></tr>",
        ]

        for key, value in data.items():
            html_parts.append(f"<tr><td>{key}</td><td>{value}</td></tr>")

        html_parts.extend(
            [
                "</table>",
                "</body>",
                "</html>",
            ]
        )

        return "\n".join(html_parts)

    @staticmethod
    def table(data: dict[str, Any]) -> str:
        """Format as ASCII table."""
        if not data:
            return "No data"

        # Calculate column widths
        max_key = max(len(str(k)) for k in data)
        max_val = max(len(str(v)) for v in data.values())

        # Build table
        lines = []
        lines.append("=" * (max_key + max_val + 7))
        lines.append(f"{'Parameter':{max_key}} | Value")
        lines.append("-" * (max_key + max_val + 7))

        for key, value in data.items():
            lines.append(f"{key!s:{max_key}} | {value}")

        lines.append("=" * (max_key + max_val + 7))

        return "\n".join(lines)


def format_output(data: dict[str, Any], format_type: str) -> str:
    """Format output data according to specified format.

    Args:
        data: Dictionary of results to format.
        format_type: Output format ('json', 'csv', 'html', 'table').

    Returns:
        Formatted string.
    """
    formatter = getattr(OutputFormat, format_type, OutputFormat.table)
    return formatter(data)


@click.group()  # type: ignore[misc]
@click.option(  # type: ignore[misc]
    "-v",
    "--verbose",
    count=True,
    help="Increase verbosity (-v for INFO, -vv for DEBUG).",
)
@click.version_option(version="0.1.0", prog_name="tracekit")  # type: ignore[misc]
@click.pass_context  # type: ignore[misc]
def cli(ctx: click.Context, verbose: int) -> None:
    """TraceKit - Signal Analysis Framework for Oscilloscope Data.

    Command-line tools for characterizing buffers, decoding protocols,
    analyzing spectra, and comparing signals.

    Args:
        ctx: Click context object.
        verbose: Verbosity level (0=WARNING, 1=INFO, 2+=DEBUG).

    Examples:
        tracekit characterize signal.wfm
        tracekit decode uart.wfm --protocol auto
        tracekit batch '*.wfm' --analysis characterize
        tracekit compare before.wfm after.wfm
        tracekit shell  # Interactive REPL
    """
    # Ensure ctx.obj exists
    ctx.ensure_object(dict)

    # Set logging level based on verbosity
    if verbose == 0:
        logger.setLevel(logging.WARNING)
    elif verbose == 1:
        logger.setLevel(logging.INFO)
        logger.info("Verbose mode enabled")
    else:  # verbose >= 2
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")

    ctx.obj["verbose"] = verbose


@click.command()  # type: ignore[misc]
def shell() -> None:
    """Start an interactive TraceKit shell.

    Opens a Python REPL with TraceKit pre-imported and ready to use.
    Features tab completion, persistent history, and helpful shortcuts.

    Example:
        $ tracekit shell
        TraceKit Shell v0.1.0
        >>> trace = load("signal.wfm")
        >>> rise_time(trace)
    """
    from tracekit.cli.shell import start_shell

    start_shell()


@click.command()  # type: ignore[misc]
@click.argument("tutorial_id", required=False, default=None)  # type: ignore[misc]
@click.option("--list", "list_tutorials", is_flag=True, help="List available tutorials")  # type: ignore[misc]
def tutorial(tutorial_id: str | None, list_tutorials: bool) -> None:
    """Run an interactive tutorial.

    Provides step-by-step guidance for learning TraceKit.

    Args:
        tutorial_id: ID of the tutorial to run (or None to list).
        list_tutorials: If True, list available tutorials.

    Examples:
        tracekit tutorial --list           # List available tutorials
        tracekit tutorial getting_started  # Run the getting started tutorial
    """
    from tracekit.onboarding import list_tutorials as list_tut
    from tracekit.onboarding import run_tutorial

    if list_tutorials or tutorial_id is None:
        tutorials = list_tut()
        click.echo("Available tutorials:")
        for t in tutorials:
            click.echo(f"  {t['id']}: {t['title']} ({t['difficulty']}, {t['steps']} steps)")
        if tutorial_id is None:
            click.echo("\nRun with: tracekit tutorial <tutorial_id>")
        return

    run_tutorial(tutorial_id, interactive=True)


# Import subcommands
from tracekit.cli.batch import batch  # noqa: E402
from tracekit.cli.characterize import characterize  # noqa: E402
from tracekit.cli.compare import compare  # noqa: E402
from tracekit.cli.decode import decode  # noqa: E402

# Register subcommands
cli.add_command(characterize)  # type: ignore[has-type]
cli.add_command(decode)  # type: ignore[has-type]
cli.add_command(batch)  # type: ignore[has-type]
cli.add_command(compare)  # type: ignore[has-type]
cli.add_command(shell)
cli.add_command(tutorial)


def main() -> None:
    """Entry point for the tracekit CLI."""
    try:
        cli(obj={})
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
