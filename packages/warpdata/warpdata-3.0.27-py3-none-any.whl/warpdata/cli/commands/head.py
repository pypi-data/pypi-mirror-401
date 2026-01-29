"""warpdata head command - preview first rows."""

from __future__ import annotations

import json
import sys
from argparse import Namespace

import warpdata as wd
from warpdata.util.errors import WarpDatasetsError


def run(args: Namespace) -> int:
    """Run the head command.

    Args:
        args: Parsed command line arguments

    Returns:
        Exit code
    """
    try:
        ds = wd.dataset(args.dataset, version=args.ds_version)
        table = ds.table(args.table)
    except WarpDatasetsError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Get first n rows
    relation = table.head(args.rows)

    # Check for UI format
    from warpdata.cli.ui import should_use_ui_format, output_ui, table_block

    if should_use_ui_format(args.format):
        df = relation.df()
        columns = list(df.columns)
        # Convert rows to lists, handling special types
        rows = []
        for _, row in df.iterrows():
            row_data = []
            for val in row:
                if hasattr(val, 'tobytes'):  # bytes-like
                    row_data.append(f"<binary {len(val)} bytes>")
                elif isinstance(val, bytes):
                    row_data.append(f"<binary {len(val)} bytes>")
                else:
                    row_data.append(val)
            rows.append(row_data)
        output_ui(table_block(
            f"Preview ({len(rows)} rows)",
            columns,
            rows,
        ))
        return 0

    if args.format == "json":
        # Convert to list of dicts
        df = relation.df()
        records = df.to_dict(orient="records")
        print(json.dumps(records, indent=2, default=str))

    elif args.format == "csv":
        df = relation.df()
        print(df.to_csv(index=False))

    else:  # table format
        # Use DuckDB's built-in display
        print(relation)

    return 0
