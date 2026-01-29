"""warpdata doctor command - diagnose environment issues.

Runs checks and reports on environment configuration.
"""

from __future__ import annotations

import json
import shutil
import sys
from argparse import Namespace
from pathlib import Path

from warpdata.config import get_settings
from warpdata.tools.doctor import (
    run_all_checks,
    format_report,
    format_json,
    has_failures,
)


def _check_dataset_integrity(settings, dataset_id: str) -> tuple[bool, str]:
    """Check if a dataset has all its data shards available.

    Args:
        settings: Settings object
        dataset_id: Dataset ID (workspace/name)

    Returns:
        (is_valid, reason) - True if all shards exist, False with reason if not
    """
    import boto3
    from botocore.config import Config

    workspace, name = dataset_id.split("/", 1)
    manifest_dir = settings.workspace_root / "manifests" / workspace / name

    # Load manifest
    latest_path = manifest_dir / "latest.json"
    if not latest_path.exists():
        return False, "no manifest"

    with open(latest_path) as f:
        latest = json.load(f)
    version = latest.get("version")

    manifest_path = manifest_dir / f"{version}.json"
    if not manifest_path.exists():
        return False, "manifest file missing"

    with open(manifest_path) as f:
        manifest = json.load(f)

    # Setup S3 client for remote checks
    s3 = None
    if settings.s3_endpoint_url:
        try:
            s3 = boto3.client(
                's3',
                endpoint_url=settings.s3_endpoint_url,
                region_name=settings.s3_region,
                config=Config(signature_version='s3v4')
            )
        except Exception:
            pass

    def check_uri(uri: str) -> bool:
        """Check if a URI is accessible."""
        if not uri:
            return True

        if uri.startswith("file://"):
            return Path(uri[7:]).exists()

        if uri.startswith("local://"):
            return (settings.workspace_root / uri[8:]).exists()

        if uri.startswith("s3://") and s3:
            parts = uri[5:].split("/", 1)
            if len(parts) < 2:
                return True
            uri_bucket = parts[0]
            s3_key = parts[1]
            try:
                s3.head_object(Bucket=uri_bucket, Key=s3_key)
                return True
            except:
                return False

        # Unknown scheme - assume ok
        return True

    # Check all table shards
    for table_name, table_data in manifest.get("tables", {}).items():
        for shard in table_data.get("shards", []):
            uri = shard.get("uri") if isinstance(shard, dict) else shard
            if uri and not check_uri(uri):
                return False, f"missing shard in table '{table_name}'"

    # Check artifact shards
    for art_name, art_data in manifest.get("artifacts", {}).items():
        for shard in art_data.get("shards", []):
            uri = shard.get("uri") if isinstance(shard, dict) else shard
            if uri and not check_uri(uri):
                return False, f"missing shard in artifact '{art_name}'"

    return True, "ok"


def _run_prune(settings) -> int:
    """Find and remove datasets with missing data shards.

    Args:
        settings: Settings object

    Returns:
        Exit code
    """
    manifest_root = settings.workspace_root / "manifests"

    if not manifest_root.exists():
        print("No manifests directory found.")
        return 0

    # Find all datasets
    datasets = []
    for ws_dir in manifest_root.iterdir():
        if not ws_dir.is_dir() or ws_dir.name.startswith("."):
            continue
        for ds_dir in ws_dir.iterdir():
            if not ds_dir.is_dir() or ds_dir.name.startswith("."):
                continue
            if (ds_dir / "latest.json").exists():
                datasets.append(f"{ws_dir.name}/{ds_dir.name}")

    if not datasets:
        print("No datasets found.")
        return 0

    print(f"Checking {len(datasets)} dataset(s) for integrity...\n")

    valid = []
    broken = []

    for ds_id in sorted(datasets):
        is_valid, reason = _check_dataset_integrity(settings, ds_id)
        if is_valid:
            valid.append(ds_id)
            print(f"✓ {ds_id}")
        else:
            broken.append((ds_id, reason))
            print(f"✗ {ds_id}: {reason}")
        sys.stdout.flush()

    print(f"\n{'='*60}")
    print(f"Valid: {len(valid)}")
    print(f"Broken: {len(broken)}")

    if not broken:
        print("\nAll datasets are healthy!")
        return 0

    # Ask for confirmation
    print(f"\nThe following {len(broken)} dataset(s) have missing data:")
    for ds_id, reason in broken:
        print(f"  {ds_id}")

    response = input(f"\nRemove these {len(broken)} broken dataset(s)? [y/N]: ")
    if response.lower() != "y":
        print("Aborted.")
        return 0

    # Remove broken datasets
    removed = 0
    for ds_id, _ in broken:
        workspace, name = ds_id.split("/", 1)
        ds_dir = manifest_root / workspace / name
        try:
            shutil.rmtree(ds_dir)
            print(f"  Removed: {ds_id}")
            removed += 1

            # Clean up empty parent
            ws_dir = manifest_root / workspace
            if ws_dir.exists() and not any(ws_dir.iterdir()):
                ws_dir.rmdir()
        except Exception as e:
            print(f"  Error removing {ds_id}: {e}", file=sys.stderr)

    print(f"\nRemoved {removed} broken dataset(s)")
    return 0


def run(args: Namespace) -> int:
    """Run the doctor command.

    Args:
        args: Parsed command line arguments

    Returns:
        Exit code
    """
    # Load settings
    try:
        settings = get_settings()
    except Exception as e:
        print(f"Error loading settings: {e}", file=sys.stderr)
        return 1

    # Check if prune mode requested
    if getattr(args, "prune", False):
        return _run_prune(settings)

    # Check if repair mode requested
    if getattr(args, "repair", False):
        from warpdata.tools.doctor.repair import run_repair_mode
        return run_repair_mode(settings)

    # Get dataset ID if provided
    dataset_id = getattr(args, "dataset", None)

    # Determine if color should be used
    use_color = not args.no_color and sys.stdout.isatty()

    # Determine verbosity
    verbose = args.verbose

    # Determine if performance check should be run
    include_performance = args.performance

    # Run checks
    results = run_all_checks(
        settings=settings,
        dataset_id=dataset_id,
        include_performance=include_performance,
    )

    # Format output
    from warpdata.cli.ui import should_use_ui_format, output_ui, table_block

    if should_use_ui_format(args.format):
        from warpdata.tools.doctor.checks import CheckStatus
        rows = []
        for result in results:
            status = "PASS" if result.status == CheckStatus.PASS else "FAIL"
            rows.append([result.name, status, result.message or ""])
        output_ui(table_block(
            "System Check",
            ["Check", "Status", "Message"],
            rows,
        ))
    elif args.format == "json":
        output = format_json(results)
        print(output)
    else:
        output = format_report(results, use_color=use_color, verbose=verbose)
        print(output)

    # Return exit code based on results
    if has_failures(results):
        return 1
    return 0
