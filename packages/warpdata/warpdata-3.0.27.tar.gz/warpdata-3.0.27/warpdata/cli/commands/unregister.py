"""Unregister command - remove a dataset from the local workspace."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def run(args: argparse.Namespace) -> int:
    """Remove a registered dataset from the local workspace.

    This only removes the manifest files - it does not delete remote data
    or cached blobs.
    """
    from warpdata.config.settings import get_settings

    settings = get_settings()

    # Allow override of workspace root
    workspace_root = Path(args.workspace_root) if args.workspace_root else settings.workspace_root
    manifests_dir = workspace_root / "manifests"

    # Parse dataset ID
    dataset_id = args.dataset
    if "/" not in dataset_id:
        print(f"Error: Invalid dataset ID '{dataset_id}'. Expected format: workspace/name", file=sys.stderr)
        return 1

    workspace, name = dataset_id.split("/", 1)
    dataset_dir = manifests_dir / workspace / name

    if not dataset_dir.exists():
        print(f"Error: Dataset '{dataset_id}' not found in {manifests_dir}", file=sys.stderr)
        return 1

    # List versions
    versions = list(dataset_dir.glob("*.json"))
    latest_file = dataset_dir / "latest.json"

    if not versions:
        print(f"Error: No manifest versions found for '{dataset_id}'", file=sys.stderr)
        return 1

    # Handle specific version removal
    if args.ds_version:
        version_file = dataset_dir / f"{args.ds_version}.json"
        if not version_file.exists():
            # Try partial match
            matches = [v for v in versions if v.stem.startswith(args.ds_version)]
            if len(matches) == 1:
                version_file = matches[0]
            elif len(matches) > 1:
                print(f"Error: Ambiguous version '{args.ds_version}'. Matches: {[m.stem for m in matches]}", file=sys.stderr)
                return 1
            else:
                print(f"Error: Version '{args.ds_version}' not found for '{dataset_id}'", file=sys.stderr)
                return 1

        # Confirm deletion
        if not args.yes:
            response = input(f"Remove version {version_file.stem} of {dataset_id}? [y/N]: ")
            if response.lower() != "y":
                print("Cancelled.")
                return 0

        version_file.unlink()
        print(f"Removed: {version_file}")

        # Check if this was the only version
        remaining = list(dataset_dir.glob("*.json"))
        remaining = [v for v in remaining if v.name != "latest.json"]
        if not remaining:
            # Remove the whole directory
            shutil.rmtree(dataset_dir)
            print(f"Removed empty dataset directory: {dataset_dir}")
            # Check if workspace is empty
            workspace_dir = dataset_dir.parent
            if workspace_dir.exists() and not list(workspace_dir.iterdir()):
                workspace_dir.rmdir()
                print(f"Removed empty workspace directory: {workspace_dir}")
        return 0

    # Remove all versions
    version_count = len([v for v in versions if v.name != "latest.json"])

    if not args.yes:
        if args.all_versions or version_count == 1:
            response = input(f"Remove dataset '{dataset_id}' ({version_count} version(s))? [y/N]: ")
        else:
            print(f"Dataset '{dataset_id}' has {version_count} version(s).")
            print("Use --all-versions to remove all, or --version to remove a specific version.")
            return 1

        if response.lower() != "y":
            print("Cancelled.")
            return 0

    # Remove the directory
    shutil.rmtree(dataset_dir)
    print(f"Removed: {dataset_id} ({version_count} version(s))")

    # Check if workspace is empty
    workspace_dir = dataset_dir.parent
    if workspace_dir.exists() and not list(workspace_dir.iterdir()):
        workspace_dir.rmdir()
        print(f"Removed empty workspace directory: {workspace_dir}")

    return 0
