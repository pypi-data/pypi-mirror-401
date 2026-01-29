"""warpdata info command - show dataset information."""

from __future__ import annotations

import json
import sys
from argparse import Namespace

import warpdata as wd
from warpdata.util.errors import WarpDatasetsError


def run(args: Namespace) -> int:
    """Run the info command.

    Args:
        args: Parsed command line arguments

    Returns:
        Exit code
    """
    try:
        ds = wd.dataset(args.dataset, version=args.ds_version)
    except WarpDatasetsError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    info = ds.info()

    # Check for UI format
    output_format = getattr(args, "format", "table")
    from warpdata.cli.ui import should_use_ui_format, output_ui, table_block, card_block

    if should_use_ui_format(output_format):
        blocks = []

        # Main info card
        bindings_str = ", ".join(info["bindings"]) if info["bindings"] else "none"
        blocks.append(card_block(
            info["id"],
            subtitle=f"Version: {info['version']}",
            body=f"Bindings: {bindings_str}",
        ))

        # Tables table
        table_rows = []
        for name, table_info in info["tables"].items():
            table_rows.append([
                name,
                table_info["row_count"] or 0,
                table_info["shards"],
            ])
        if table_rows:
            blocks.append(table_block("Tables", ["Name", "Rows", "Shards"], table_rows))

        # Artifacts table
        if info["artifacts"]:
            artifact_rows = [[name, "artifact", 1] for name in info["artifacts"]]
            blocks.append(table_block("Artifacts", ["Name", "Kind", "Shards"], artifact_rows))

        output_ui(blocks)
        return 0

    if output_format == "json":
        print(json.dumps(info, indent=2))
        return 0

    # Print formatted info
    print(f"Dataset: {info['id']}")
    print(f"Version: {info['version']}")
    print()

    print("Tables:")
    for name, table_info in info["tables"].items():
        print(f"  {name}:")
        print(f"    Format: {table_info['format']}")
        print(f"    Shards: {table_info['shards']}")
        if table_info["row_count"]:
            print(f"    Rows: {table_info['row_count']:,}")
        if table_info["schema"]:
            print(f"    Columns: {len(table_info['schema'])}")

    if info["artifacts"]:
        print()
        print("Artifacts:")
        for name in info["artifacts"]:
            print(f"  - {name}")

    if info["bindings"]:
        print()
        print(f"Bindings: {info['bindings']}")

    return 0
