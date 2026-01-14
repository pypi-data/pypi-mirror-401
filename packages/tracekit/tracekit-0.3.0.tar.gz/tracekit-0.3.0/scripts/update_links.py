#!/usr/bin/env python3
"""Update internal documentation links after migration.

This script updates all markdown links to reflect the new file locations
after the documentation reorganization.

Usage:
    python scripts/update_links.py [--dry-run] [--verbose]
"""

import argparse
import re
from pathlib import Path

# Link mappings: old_link_pattern -> new_link
# These are relative paths as they appear in markdown links
LINK_MIGRATIONS = {
    # API docs
    "LOADER_API.md": "api/loader.md",
    "ANALYSIS_API.md": "api/analysis.md",
    "EXPORT_API.md": "api/export.md",
    "REPORTING.md": "api/reporting.md",
    "visualization_api.md": "api/visualization.md",
    # Guides
    "NAN_RESULTS_GUIDE.md": "guides/nan-handling.md",
    "TROUBLESHOOTING_NAN_RESULTS.md": "guides/nan-handling.md",
    "SIGNAL_INTELLIGENCE_GUIDE.md": "guides/signal-intelligence.md",
    "gpu_acceleration.md": "guides/gpu-acceleration.md",
    "REPORT_CUSTOMIZATION_GUIDE.md": "guides/report-customization.md",
    "guides/loading_waveforms.md": "guides/loading-waveforms.md",
    "guides/synthetic_test_data.md": "guides/synthetic-test-data.md",
    "guides/test_data_migration.md": "guides/test-data-migration.md",
    "guides/public_test_data_sources.md": "guides/public-test-data-sources.md",
    # Testing docs
    "TESTING_GUIDELINES.md": "testing/index.md",
    "testing/OOM_PREVENTION_GUIDE.md": "testing/oom-prevention.md",
    "testing/TESTING_QUICK_REFERENCE.md": "testing/index.md",
    # Root files
    "DEPLOYMENT.md": "docs/guides/deployment.md",
}

# Files to process (glob patterns)
FILE_PATTERNS = [
    "**/*.md",
    "CLAUDE.md",
]

# Directories to skip
SKIP_DIRS = {
    ".git",
    ".venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "htmlcov",
    ".coordination",
    ".claude/agent-outputs",
    ".claude/checkpoints",
    ".claude/summaries",
}


def should_skip(path: Path) -> bool:
    """Check if a path should be skipped."""
    return any(part in SKIP_DIRS for part in path.parts)


def update_links_in_content(
    content: str, file_path: Path, verbose: bool = False
) -> tuple[str, int]:
    """Update all matching links in content."""
    changes = 0

    for old_link, new_link in LINK_MIGRATIONS.items():
        # Match markdown links containing the old path
        # This handles various formats: [text](path), [text](../path), [text](./path)
        pattern = rf"\[([^\]]+)\]\(([^)]*{re.escape(old_link)}[^)]*)\)"

        def replacer(match, old=old_link, new=new_link):
            nonlocal changes
            link_text = match.group(1)
            full_link = match.group(2)

            # Replace the old filename/path with new one
            updated_link = full_link.replace(old, new)
            changes += 1

            if verbose:
                print(f"  {file_path}: '{old}' -> '{new}'")

            return f"[{link_text}]({updated_link})"

        content = re.sub(pattern, replacer, content)

    return content, changes


def process_file(file_path: Path, dry_run: bool = False, verbose: bool = False) -> int:
    """Process a single file and update its links."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError) as e:
        if verbose:
            print(f"[SKIP] Cannot read: {file_path} ({e})")
        return 0

    updated_content, changes = update_links_in_content(content, file_path, verbose)

    if changes > 0:
        if dry_run:
            print(f"[DRY RUN] Would update {changes} link(s) in: {file_path}")
        else:
            file_path.write_text(updated_content, encoding="utf-8")
            if verbose:
                print(f"Updated {changes} link(s) in: {file_path}")

    return changes


def run_update(repo_root: Path, dry_run: bool = False, verbose: bool = False):
    """Execute the full link update."""
    print("=" * 60)
    print("TraceKit Link Update")
    print("=" * 60)

    if dry_run:
        print("\n[DRY RUN MODE - No changes will be made]\n")

    total_changes = 0
    files_updated = 0

    # Process all markdown files
    for pattern in FILE_PATTERNS:
        for file_path in repo_root.glob(pattern):
            if should_skip(file_path):
                continue

            changes = process_file(file_path, dry_run, verbose)
            if changes > 0:
                total_changes += changes
                files_updated += 1

    # Summary
    print("\n" + "=" * 60)
    print("Link Update Summary")
    print("=" * 60)
    print(f"  Files updated: {files_updated}")
    print(f"  Total links updated: {total_changes}")

    if dry_run:
        print("\n[DRY RUN] Re-run without --dry-run to apply changes")


def main():
    parser = argparse.ArgumentParser(description="Update TraceKit documentation links")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be done without making changes"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    # Find repo root (parent of scripts/)
    repo_root = Path(__file__).parent.parent

    run_update(repo_root, args.dry_run, args.verbose)


if __name__ == "__main__":
    main()
