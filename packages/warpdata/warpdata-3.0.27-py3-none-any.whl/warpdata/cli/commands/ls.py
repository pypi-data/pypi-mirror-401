"""List datasets command.

Lists locally registered datasets by walking the workspace manifest directory.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator


@dataclass
class DatasetInfo:
    """Information about a discovered dataset."""

    dataset_id: str  # workspace/name
    version: str
    is_latest: bool
    manifest_path: Path
    row_count: int | None = None
    artifact_count: int = 0
    byte_size: int = 0  # Total size of all table shards
    cache_status: str = "?"  # "local", "remote", "partial", or "?"


def _check_cache_status(manifest: dict, workspace_root: Path) -> str:
    """Check if dataset data is cached locally.

    Returns:
        "local" - all data available locally
        "remote" - no data cached locally
        "partial" - some data cached locally
    """
    import re

    data_dir = workspace_root / "data"

    def is_cached(uri: str) -> bool:
        """Check if a URI's content is available locally."""
        if not uri:
            return False
        # Local URIs are always available
        if uri.startswith("local://") or uri.startswith("file://"):
            return True
        # Check for content-addressed S3 URIs
        match = re.search(r'/objects/([0-9a-f]{2})/([0-9a-f]{2})/([0-9a-f]{64})(?:\?|$)', uri)
        if match:
            prefix1, prefix2, content_hash = match.groups()
            relative_path = f"objects/{prefix1}/{prefix2}/{content_hash}"
            # Check data directories
            if data_dir.exists():
                for candidate in data_dir.glob(f"**/{relative_path}"):
                    if candidate.is_file():
                        return True
        return False

    # Collect all URIs from manifest
    all_uris = []

    # Table shards
    for table in manifest.get("tables", {}).values():
        for shard in table.get("shards", []):
            uri = shard.get("uri") or shard.get("key")
            if uri:
                all_uris.append(uri)

    # Artifact shards and indexes
    for artifact in manifest.get("artifacts", {}).values():
        for shard in artifact.get("shards", []):
            uri = shard.get("uri") or shard.get("key")
            if uri:
                all_uris.append(uri)
        index = artifact.get("index", {})
        if index.get("uri"):
            all_uris.append(index["uri"])

    if not all_uris:
        return "local"  # No data to cache

    cached_count = sum(1 for uri in all_uris if is_cached(uri))

    if cached_count == len(all_uris):
        return "local"
    elif cached_count == 0:
        return "remote"
    else:
        return "partial"


def discover_local_datasets(workspace_root: Path) -> Iterator[DatasetInfo]:
    """Discover datasets in the local workspace.

    Walks the manifest directory structure:
    workspace_root/manifests/{workspace}/{name}/{version}.json

    Args:
        workspace_root: Root of the workspace

    Yields:
        DatasetInfo for each discovered dataset version
    """
    manifest_dir = workspace_root / "manifests"
    if not manifest_dir.exists():
        return

    # Walk through workspace directories
    for workspace_path in sorted(manifest_dir.iterdir()):
        if not workspace_path.is_dir():
            continue
        workspace_name = workspace_path.name

        # Walk through dataset directories
        for dataset_path in sorted(workspace_path.iterdir()):
            if not dataset_path.is_dir():
                continue
            dataset_name = dataset_path.name
            dataset_id = f"{workspace_name}/{dataset_name}"

            # Find latest version if exists
            latest_path = dataset_path / "latest.json"
            latest_version = None
            if latest_path.exists():
                try:
                    with open(latest_path) as f:
                        latest_data = json.load(f)
                        latest_version = latest_data.get("version")
                except Exception:
                    pass

            # Discover all versions
            for manifest_file in sorted(dataset_path.glob("*.json")):
                if manifest_file.name == "latest.json":
                    continue

                version = manifest_file.stem
                is_latest = version == latest_version

                # Try to extract metadata
                row_count = None
                artifact_count = 0
                byte_size = 0
                cache_status = "?"
                try:
                    with open(manifest_file) as f:
                        manifest = json.load(f)
                        # Get row count from main table
                        if "tables" in manifest and "main" in manifest["tables"]:
                            row_count = manifest["tables"]["main"].get("row_count")
                        # Count artifacts
                        if "artifacts" in manifest:
                            artifact_count = len(manifest["artifacts"])
                        # Sum byte sizes from all table shards
                        if "tables" in manifest:
                            for table in manifest["tables"].values():
                                for shard in table.get("shards", []):
                                    byte_size += shard.get("byte_size", 0)
                        # Check cache status
                        cache_status = _check_cache_status(manifest, workspace_root)
                except Exception:
                    pass

                yield DatasetInfo(
                    dataset_id=dataset_id,
                    version=version,
                    is_latest=is_latest,
                    manifest_path=manifest_file,
                    row_count=row_count,
                    artifact_count=artifact_count,
                    cache_status=cache_status,
                    byte_size=byte_size,
                )


def format_row_count(count: int | None) -> str:
    """Format row count for display."""
    if count is None:
        return "-"
    if count >= 1_000_000:
        return f"{count / 1_000_000:.1f}M"
    if count >= 1_000:
        return f"{count / 1_000:.1f}K"
    return str(count)


def format_size(byte_size: int) -> str:
    """Format byte size for display (e.g., 1.5 GB, 256 MB)."""
    if byte_size == 0:
        return "-"
    if byte_size >= 1_000_000_000:
        return f"{byte_size / 1_000_000_000:.1f} GB"
    if byte_size >= 1_000_000:
        return f"{byte_size / 1_000_000:.1f} MB"
    if byte_size >= 1_000:
        return f"{byte_size / 1_000:.1f} KB"
    return f"{byte_size} B"


def run(args: argparse.Namespace) -> int:
    """Run the ls command.

    Args:
        args: Parsed arguments with:
            - workspace_root: Optional workspace root override
            - all_versions: Show all versions or just latest
            - format: Output format (table, json)

    Returns:
        Exit code (0 for success)
    """
    from warpdata.config.settings import get_settings, LEGACY_WORKSPACE_ROOT

    settings = get_settings()

    # Determine workspace root
    workspace_root = settings.workspace_root
    if hasattr(args, "workspace_root") and args.workspace_root:
        workspace_root = Path(args.workspace_root)

    # Collect datasets from both current and legacy paths
    datasets = list(discover_local_datasets(workspace_root))
    seen_ids = {ds.dataset_id for ds in datasets}

    # Also check legacy path if it exists
    if LEGACY_WORKSPACE_ROOT.exists() and LEGACY_WORKSPACE_ROOT != workspace_root:
        for ds in discover_local_datasets(LEGACY_WORKSPACE_ROOT):
            if ds.dataset_id not in seen_ids:
                datasets.append(ds)
                seen_ids.add(ds.dataset_id)

    # Filter to latest only if not --all
    show_all = getattr(args, "all_versions", False)
    if not show_all:
        # Group by dataset_id, keep latest or first version
        seen = {}
        for ds in datasets:
            if ds.dataset_id not in seen:
                seen[ds.dataset_id] = ds
            elif ds.is_latest:
                seen[ds.dataset_id] = ds
        datasets = list(seen.values())

    # Output format
    output_format = getattr(args, "format", "table")

    # Check for UI format
    from warpdata.cli.ui import should_use_ui_format, output_ui, table_block

    if should_use_ui_format(output_format):
        rows = []
        for ds in datasets:
            version_display = ds.version[:10]
            if ds.is_latest:
                version_display += "*"
            rows.append([
                ds.dataset_id,
                version_display,
                ds.row_count if ds.row_count else 0,
                format_size(ds.byte_size),
                ds.cache_status == "local",
            ])
        output_ui(table_block(
            f"Datasets ({len(datasets)})",
            ["Dataset", "Version", "Rows", "Size", "Cached"],
            rows,
        ))
        return 0

    if output_format == "json":
        output = []
        for ds in datasets:
            output.append({
                "dataset": ds.dataset_id,
                "version": ds.version,
                "is_latest": ds.is_latest,
                "row_count": ds.row_count,
                "byte_size": ds.byte_size,
                "artifact_count": ds.artifact_count,
                "cache_status": ds.cache_status,
                "path": str(ds.manifest_path),
            })
        print(json.dumps(output, indent=2))
        return 0

    # Table format
    if not datasets:
        print("No local datasets found.")
        print(f"\nWorkspace root: {workspace_root}")
        print("\nChecking S3 for available datasets...")

        # Try to pull from S3
        try:
            from types import SimpleNamespace
            from warpdata.cli.commands import sync

            # Create a minimal args object for sync
            sync_args = SimpleNamespace(
                bucket=None,
                prefix=None,
                workspace_root=str(workspace_root),
                dataset=None,
            )
            s3 = sync._get_s3_client()
            bucket, prefix = sync._get_bucket_and_prefix(sync_args)
            remote = sync._list_s3_manifests(s3, bucket, prefix)

            if remote:
                print(f"Found {len(remote)} dataset(s) on S3. Pulling manifests...\n")
                sync._run_pull(sync_args)

                # Re-discover after pull
                datasets = list(discover_local_datasets(workspace_root))
                if not show_all:
                    seen = {}
                    for ds in datasets:
                        if ds.dataset_id not in seen:
                            seen[ds.dataset_id] = ds
                        elif ds.is_latest:
                            seen[ds.dataset_id] = ds
                    datasets = list(seen.values())

                if datasets:
                    print()  # Add spacing before table
            else:
                print("No datasets found on S3 either.")
                print("Use 'warpdata register' to register a local dataset.")
                return 0
        except Exception as e:
            print(f"Could not check S3: {e}")
            print("Use 'warpdata register' to register a local dataset.")
            return 0

    if not datasets:
        return 0

    # Print header
    print(f"{'DATASET':<40} {'VERSION':<12} {'ROWS':>10} {'SIZE':>10} {'CACHED':>8}")
    print("-" * 85)

    # Format cache status with symbols
    def format_cache(status: str) -> str:
        if status == "local":
            return "✓"
        elif status == "remote":
            return "-"
        elif status == "partial":
            return "~"
        return "?"

    for ds in datasets:
        version_display = ds.version[:10]
        if ds.is_latest:
            version_display += "*"

        print(
            f"{ds.dataset_id:<40} "
            f"{version_display:<12} "
            f"{format_row_count(ds.row_count):>10} "
            f"{format_size(ds.byte_size):>10} "
            f"{format_cache(ds.cache_status):>8}"
        )

    print()
    # Count by cache status
    local_count = sum(1 for ds in datasets if ds.cache_status == "local")
    partial_count = sum(1 for ds in datasets if ds.cache_status == "partial")
    remote_count = sum(1 for ds in datasets if ds.cache_status == "remote")
    status_parts = []
    if local_count:
        status_parts.append(f"{local_count} cached")
    if partial_count:
        status_parts.append(f"{partial_count} partial")
    if remote_count:
        status_parts.append(f"{remote_count} remote-only")
    status_str = ", ".join(status_parts) if status_parts else "none cached"
    print(f"Total: {len(datasets)} dataset(s) ({status_str})")
    print(f"Workspace: {workspace_root}")
    if not show_all:
        print("Use --all to show all versions")

    return 0
