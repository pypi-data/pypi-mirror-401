"""Warm cache CLI command."""

from __future__ import annotations

import argparse
import sys


def _get_local_datasets(settings, workspace: str | None = None) -> list[str]:
    """Get list of local dataset IDs.

    Args:
        settings: Settings object
        workspace: Optional workspace filter

    Returns:
        List of dataset IDs (workspace/name)
    """
    manifest_root = settings.workspace_root / "manifests"
    if not manifest_root.exists():
        return []

    datasets = []
    for ws_dir in manifest_root.iterdir():
        if not ws_dir.is_dir() or ws_dir.name.startswith("."):
            continue
        if workspace and ws_dir.name != workspace:
            continue
        for ds_dir in ws_dir.iterdir():
            if not ds_dir.is_dir() or ds_dir.name.startswith("."):
                continue
            if (ds_dir / "latest.json").exists():
                datasets.append(f"{ws_dir.name}/{ds_dir.name}")

    return sorted(datasets)


def _warm_single_dataset(
    dataset_id: str,
    settings,
    table: str = "main",
    artifacts: str | None = None,
    version: str | None = None,
    yes: bool = False,
    quiet: bool = False,
) -> tuple[int, int, int]:
    """Warm a single dataset.

    Returns:
        (total_shards, already_cached, downloaded)
    """
    from warpdata.api.dataset import dataset as get_dataset
    from warpdata.cache.context import CacheContext

    # Load dataset
    ds = get_dataset(
        dataset_id,
        version=version,
        settings=settings,
    )

    # Get table
    tbl = ds.table(table)
    uris = list(tbl.descriptor.uris)

    # If artifacts specified, add artifact shards
    artifact_uris = []
    if artifacts:
        artifact_names = artifacts.split(",")
        for name in artifact_names:
            name = name.strip()
            if name in ds.manifest.artifacts:
                artifact = ds.manifest.artifacts[name]
                artifact_uris.extend(artifact.uris)

    all_uris = uris + artifact_uris

    # Create cache context for warming
    cache_context = CacheContext(
        cache_dir=settings.cache_dir,
        prefetch_mode="off",
    )

    # Count already cached
    cached = sum(1 for uri in all_uris if cache_context.is_cached(uri))
    to_download = len(all_uris) - cached

    if to_download == 0:
        return len(all_uris), cached, 0

    if not yes and not quiet:
        response = input(f"Download {to_download} shards for {dataset_id}? [y/N]: ")
        if response.lower() != "y":
            return len(all_uris), cached, 0

    # Warm cache
    downloaded = cache_context.warm(all_uris)
    return len(all_uris), cached, downloaded


def run(args: argparse.Namespace) -> int:
    """Run warm command.

    Downloads shards for a dataset to warm the cache.

    Args:
        args: Parsed command line arguments

    Returns:
        Exit code (0 for success)
    """
    from warpdata.api.dataset import dataset as get_dataset
    from warpdata.cache.context import CacheContext
    from warpdata.config.settings import get_settings

    settings = get_settings()

    # Handle --all mode
    if getattr(args, "all", False):
        workspace = getattr(args, "workspace", None)
        datasets = _get_local_datasets(settings, workspace)

        if not datasets:
            if workspace:
                print(f"No datasets found in workspace '{workspace}'")
            else:
                print("No local datasets found")
            return 0

        print(f"Warming {len(datasets)} dataset(s)...")
        if workspace:
            print(f"Workspace: {workspace}")
        print()

        total_shards = 0
        total_cached = 0
        total_downloaded = 0

        for ds_id in datasets:
            try:
                shards, cached, downloaded = _warm_single_dataset(
                    ds_id,
                    settings,
                    table=args.table,
                    artifacts=args.artifacts,
                    version=None,  # Always use latest for --all
                    yes=args.yes,
                    quiet=True,
                )
                total_shards += shards
                total_cached += cached
                total_downloaded += downloaded

                if downloaded > 0:
                    print(f"✓ {ds_id}: downloaded {downloaded} shards")
                elif cached == shards:
                    print(f"✓ {ds_id}: already cached")
                else:
                    print(f"- {ds_id}: skipped")
                sys.stdout.flush()
            except Exception as e:
                print(f"✗ {ds_id}: {e}", file=sys.stderr)

        print()
        print(f"Total shards: {total_shards}")
        print(f"Already cached: {total_cached}")
        print(f"Downloaded: {total_downloaded}")
        return 0

    # Single dataset mode - require dataset argument
    if not args.dataset:
        print("Error: dataset argument required (or use --all)", file=sys.stderr)
        return 1

    # Load dataset
    print(f"Loading dataset: {args.dataset}")
    ds = get_dataset(
        args.dataset,
        version=args.ds_version,
        settings=settings,
    )

    # Get table
    table = ds.table(args.table)
    print(f"Table: {args.table}")
    print(f"Shards: {table.shard_count}")

    # Get URIs to warm
    uris = table.descriptor.uris

    # If --artifacts specified, add artifact shards
    artifact_uris = []
    if args.artifacts:
        artifact_names = args.artifacts.split(",")
        for name in artifact_names:
            name = name.strip()
            if name in ds.manifest.artifacts:
                artifact = ds.manifest.artifacts[name]
                artifact_uris.extend(artifact.uris)
                print(f"Artifact '{name}': {len(artifact.uris)} shards")
            else:
                print(f"Warning: Artifact '{name}' not found", file=sys.stderr)

    all_uris = list(uris) + artifact_uris
    print(f"Total URIs to warm: {len(all_uris)}")

    # Create cache context for warming
    cache_context = CacheContext(
        cache_dir=settings.cache_dir,
        prefetch_mode="off",  # We'll use warm() directly
    )

    # Count already cached
    cached = sum(1 for uri in all_uris if cache_context.is_cached(uri))
    to_download = len(all_uris) - cached

    print(f"Already cached: {cached}")
    print(f"To download: {to_download}")

    if to_download == 0:
        print("All shards already cached!")
        return 0

    if not args.yes:
        response = input(f"Download {to_download} shards? [y/N]: ")
        if response.lower() != "y":
            print("Aborted.")
            return 0

    # Warm cache
    print("Warming cache...")
    downloaded = cache_context.warm(all_uris)
    print(f"Downloaded: {downloaded} shards")

    # Show stats
    stats = cache_context.stats()
    print(f"Cache size: {stats['cache']['total_bytes']:,} bytes")
    print(f"Cache entries: {stats['cache']['entry_count']}")

    return 0
