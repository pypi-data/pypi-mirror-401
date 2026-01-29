"""Sync command - push/pull manifests to/from S3."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _run_preflight_check() -> bool:
    """Run pre-flight connectivity check before sync.

    Returns:
        True if checks pass, False otherwise
    """
    from warpdata.config.settings import get_settings
    from warpdata.tools.doctor.checks import (
        CheckStatus,
        check_storage_config,
        check_connectivity,
    )

    settings = get_settings()

    # Check storage configuration
    config_result = check_storage_config(settings)
    if config_result.status == CheckStatus.FAIL:
        print(f"Pre-flight check failed: {config_result.message}", file=sys.stderr)
        if config_result.details:
            print(f"  {config_result.details}", file=sys.stderr)
        if config_result.suggestion:
            print(f"\nHow to fix:\n  {config_result.suggestion}", file=sys.stderr)
        print(f"\nRun 'warp doctor --repair' for interactive help.", file=sys.stderr)
        return False

    # Check connectivity
    conn_result = check_connectivity(settings)
    if conn_result.status == CheckStatus.FAIL:
        print(f"Pre-flight check failed: {conn_result.message}", file=sys.stderr)
        if conn_result.details:
            print(f"  {conn_result.details}", file=sys.stderr)
        if conn_result.suggestion:
            print(f"\nHow to fix:\n  {conn_result.suggestion}", file=sys.stderr)
        print(f"\nRun 'warp doctor' for detailed diagnostics.", file=sys.stderr)
        return False

    return True


def run(args: argparse.Namespace) -> int:
    """Run sync command."""
    subcommand = getattr(args, "sync_command", None)

    if subcommand == "push":
        return _run_push(args)
    elif subcommand == "pull":
        return _run_pull(args)
    elif subcommand == "status":
        return _run_status(args)
    else:
        print("Usage: warpdata sync {push|pull|status}")
        print("\nSubcommands:")
        print("  push    Upload local manifests to S3")
        print("  pull    Download manifests from S3 to local")
        print("  status  Show sync status between local and S3")
        return 1


def _get_s3_client():
    """Get boto3 S3 client with custom endpoint support."""
    from warpdata.config.settings import get_settings

    try:
        import boto3
    except ImportError:
        print("Error: boto3 is required for S3 sync. Install with: pip install boto3", file=sys.stderr)
        sys.exit(1)

    settings = get_settings()
    kwargs = {}
    if settings.s3_endpoint_url:
        kwargs["endpoint_url"] = settings.s3_endpoint_url
    if settings.s3_region:
        kwargs["region_name"] = settings.s3_region
    return boto3.client("s3", **kwargs)


def _get_bucket_and_prefix(args) -> tuple[str, str]:
    """Get S3 bucket and prefix from args or settings."""
    from warpdata.config.settings import get_settings, DEFAULT_S3_BUCKET, DEFAULT_S3_PREFIX
    from urllib.parse import urlparse

    # Check args first
    if getattr(args, "bucket", None):
        bucket = args.bucket
        prefix = getattr(args, "prefix", None) or f"{DEFAULT_S3_PREFIX}/manifests"
        return bucket, prefix

    # Use manifest_base from settings (respects WARPDATASETS_MANIFEST_BASE env var)
    settings = get_settings()
    if settings.manifest_base and settings.manifest_base.startswith("s3://"):
        parsed = urlparse(settings.manifest_base)
        bucket = parsed.netloc
        base_prefix = parsed.path.lstrip("/")
        prefix = f"{base_prefix}/manifests" if base_prefix else "manifests"
        return bucket, prefix

    # Fall back to defaults
    bucket = DEFAULT_S3_BUCKET
    prefix = f"{DEFAULT_S3_PREFIX}/manifests"
    return bucket, prefix


def _get_workspace_root(args) -> Path:
    """Get workspace root from args or settings."""
    if hasattr(args, "workspace_root") and args.workspace_root:
        return Path(args.workspace_root)

    from warpdata.config.settings import get_settings
    settings = get_settings()
    return Path(settings.workspace_root)


def _list_local_manifests(workspace_root: Path) -> dict[str, dict]:
    """List local manifests with their versions.

    Returns:
        Dict mapping dataset_id to {version, path, size}
    """
    manifests = {}
    manifest_dir = workspace_root / "manifests"

    if not manifest_dir.exists():
        return manifests

    for workspace_path in manifest_dir.iterdir():
        if not workspace_path.is_dir():
            continue
        workspace = workspace_path.name

        for dataset_path in workspace_path.iterdir():
            if not dataset_path.is_dir():
                continue
            name = dataset_path.name
            dataset_id = f"{workspace}/{name}"

            # Read latest.json
            latest_path = dataset_path / "latest.json"
            if not latest_path.exists():
                continue

            try:
                with open(latest_path) as f:
                    latest = json.load(f)
                version = latest.get("version")
                if not version:
                    continue

                manifest_path = dataset_path / f"{version}.json"
                if manifest_path.exists():
                    manifests[dataset_id] = {
                        "version": version,
                        "path": manifest_path,
                        "size": manifest_path.stat().st_size,
                    }
            except Exception:
                continue

    return manifests


def _list_s3_manifests(s3, bucket: str, prefix: str) -> dict[str, dict]:
    """List S3 manifests with their versions.

    Returns:
        Dict mapping dataset_id to {version, key, size}
    """
    manifests = {}
    paginator = s3.get_paginator("list_objects_v2")

    for page in paginator.paginate(Bucket=bucket, Prefix=prefix + "/"):
        for obj in page.get("Contents", []):
            key = obj["Key"]

            # Skip non-latest.json
            if not key.endswith("/latest.json"):
                continue

            # Parse: prefix/workspace/name/latest.json
            rel_key = key[len(prefix) + 1:]  # Remove prefix/
            parts = rel_key.split("/")
            if len(parts) != 3:
                continue

            workspace, name, _ = parts
            dataset_id = f"{workspace}/{name}"

            # Fetch latest.json to get version
            try:
                response = s3.get_object(Bucket=bucket, Key=key)
                latest = json.loads(response["Body"].read().decode("utf-8"))
                version = latest.get("version") or latest.get("version_hash")
                if not version:
                    continue

                # Get manifest key - check for explicit manifest path first
                # latest.json may have: {"version": "abc", "manifest": "s3://bucket/path/xyz.json"}
                manifest_uri = latest.get("manifest")
                if manifest_uri:
                    # Extract key from full S3 URI
                    from urllib.parse import urlparse
                    parsed = urlparse(manifest_uri)
                    manifest_key = parsed.path.lstrip("/")
                else:
                    # Fall back to version-based naming
                    manifest_key = f"{prefix}/{workspace}/{name}/{version}.json"

                # Get manifest size
                try:
                    head = s3.head_object(Bucket=bucket, Key=manifest_key)
                    size = head.get("ContentLength", 0)
                except Exception:
                    size = 0

                manifests[dataset_id] = {
                    "version": version,
                    "key": manifest_key,
                    "size": size,
                }
            except Exception:
                continue

    return manifests


def _run_status(args: argparse.Namespace) -> int:
    """Show sync status."""
    s3 = _get_s3_client()
    bucket, prefix = _get_bucket_and_prefix(args)
    workspace_root = _get_workspace_root(args)

    print(f"Comparing local ({workspace_root}) with S3 (s3://{bucket}/{prefix}/)...\n")

    local = _list_local_manifests(workspace_root)
    remote = _list_s3_manifests(s3, bucket, prefix)

    all_datasets = sorted(set(local.keys()) | set(remote.keys()))

    local_only = []
    remote_only = []
    synced = []
    different = []

    for ds in all_datasets:
        in_local = ds in local
        in_remote = ds in remote

        if in_local and not in_remote:
            local_only.append(ds)
        elif in_remote and not in_local:
            remote_only.append(ds)
        elif local[ds]["version"] == remote[ds]["version"]:
            synced.append(ds)
        else:
            different.append((ds, local[ds]["version"], remote[ds]["version"]))

    # Check for UI format
    output_format = getattr(args, "format", "table")
    from warpdata.cli.ui import should_use_ui_format, output_ui, table_block

    if should_use_ui_format(output_format):
        rows = []
        for ds in synced:
            rows.append([ds, local[ds]["version"][:8], remote[ds]["version"][:8], "Synced"])
        for ds in local_only:
            rows.append([ds, local[ds]["version"][:8], "-", "Local Only"])
        for ds in remote_only:
            rows.append([ds, "-", remote[ds]["version"][:8], "Remote Only"])
        for ds, local_v, remote_v in different:
            rows.append([ds, local_v[:8], remote_v[:8], "Different"])
        output_ui(table_block(
            "Sync Status",
            ["Dataset", "Local Version", "Remote Version", "Status"],
            rows,
        ))
        return 0

    if synced:
        print(f"Synced ({len(synced)}):")
        for ds in synced[:10]:
            print(f"  {ds}")
        if len(synced) > 10:
            print(f"  ... and {len(synced) - 10} more")
        print()

    if local_only:
        print(f"Local only ({len(local_only)}) - use 'sync push' to upload:")
        for ds in local_only:
            print(f"  {ds} (v{local[ds]['version'][:8]})")
        print()

    if remote_only:
        print(f"Remote only ({len(remote_only)}) - use 'sync pull' to download:")
        for ds in remote_only:
            print(f"  {ds} (v{remote[ds]['version'][:8]})")
        print()

    if different:
        print(f"Different versions ({len(different)}):")
        for ds, local_v, remote_v in different:
            print(f"  {ds}: local={local_v[:8]} remote={remote_v[:8]}")
        print()

    print(f"Summary: {len(synced)} synced, {len(local_only)} local-only, {len(remote_only)} remote-only, {len(different)} different")
    return 0


def _run_push(args: argparse.Namespace) -> int:
    """Push local manifests to S3."""
    # Pre-flight check
    if not _run_preflight_check():
        return 1

    s3 = _get_s3_client()
    bucket, prefix = _get_bucket_and_prefix(args)
    workspace_root = _get_workspace_root(args)

    local = _list_local_manifests(workspace_root)

    if not local:
        print("No local manifests found.")
        return 0

    # Filter by dataset if specified
    if hasattr(args, "dataset") and args.dataset:
        if args.dataset not in local:
            print(f"Dataset not found locally: {args.dataset}", file=sys.stderr)
            return 1
        local = {args.dataset: local[args.dataset]}

    # Get remote to check what needs updating
    remote = _list_s3_manifests(s3, bucket, prefix)

    to_push = []
    for ds, info in local.items():
        if ds not in remote or remote[ds]["version"] != info["version"]:
            to_push.append((ds, info))

    if not to_push:
        print("All manifests already synced.")
        return 0

    print(f"Pushing {len(to_push)} manifest(s) to s3://{bucket}/{prefix}/...\n")

    pushed = 0
    for ds, info in to_push:
        workspace, name = ds.split("/", 1)
        version = info["version"]

        # Read manifest
        with open(info["path"]) as f:
            manifest_data = f.read()

        # Upload manifest
        manifest_key = f"{prefix}/{workspace}/{name}/{version}.json"
        s3.put_object(
            Bucket=bucket,
            Key=manifest_key,
            Body=manifest_data.encode("utf-8"),
            ContentType="application/json",
        )

        # Upload latest.json
        latest_key = f"{prefix}/{workspace}/{name}/latest.json"
        latest_data = json.dumps({"version": version})
        s3.put_object(
            Bucket=bucket,
            Key=latest_key,
            Body=latest_data.encode("utf-8"),
            ContentType="application/json",
        )

        print(f"  {ds} (v{version[:8]})")
        pushed += 1

    print(f"\nPushed {pushed} manifest(s)")
    return 0


def _validate_manifest_shards(s3, bucket: str, manifest_data: str) -> tuple[bool, list[str]]:
    """Validate all shards in a manifest exist in S3.

    Args:
        s3: boto3 S3 client
        bucket: S3 bucket name
        manifest_data: JSON string of manifest

    Returns:
        (is_valid, list of missing shard URIs)
    """
    manifest = json.loads(manifest_data)
    missing = []

    def check_uri(uri):
        if not uri or not uri.startswith("s3://"):
            return True  # Skip non-S3 URIs
        parts = uri[5:].split("/", 1)
        if len(parts) < 2:
            return True
        s3_key = parts[1]
        try:
            s3.head_object(Bucket=bucket, Key=s3_key)
            return True
        except:
            return False

    # Check table shards
    for table_name, table_data in manifest.get("tables", {}).items():
        for shard in table_data.get("shards", []):
            uri = shard.get("uri") if isinstance(shard, dict) else shard
            if uri and not check_uri(uri):
                missing.append(uri)

    # Check artifact shards
    for art_name, art_data in manifest.get("artifacts", {}).items():
        for shard in art_data.get("shards", []):
            uri = shard.get("uri") if isinstance(shard, dict) else shard
            if uri and not check_uri(uri):
                missing.append(f"artifact:{art_name}")
        # Check index
        if art_data.get("index", {}).get("uri"):
            if not check_uri(art_data["index"]["uri"]):
                missing.append(f"artifact:{art_name}:index")

    return len(missing) == 0, missing


def _run_pull(args: argparse.Namespace) -> int:
    """Pull manifests from S3.

    Only pulls manifests where all data shards exist. This prevents
    ending up with broken datasets that have manifests but no data.

    If --data is specified, also downloads data shards into the local mirror.
    """
    # Pre-flight check
    if not _run_preflight_check():
        return 1

    s3 = _get_s3_client()
    bucket, prefix = _get_bucket_and_prefix(args)
    workspace_root = _get_workspace_root(args)

    # Check if we should also pull data
    pull_data = getattr(args, "data", False)

    # Check if we should skip validation (for advanced users)
    skip_validation = getattr(args, "skip_validation", False)

    remote = _list_s3_manifests(s3, bucket, prefix)

    if not remote:
        print("No remote manifests found.")
        return 0

    # Filter by dataset if specified
    if hasattr(args, "dataset") and args.dataset:
        if args.dataset not in remote:
            print(f"Dataset not found on S3: {args.dataset}", file=sys.stderr)
            return 1
        remote = {args.dataset: remote[args.dataset]}

    # Get local to check what needs updating
    local = _list_local_manifests(workspace_root)

    to_pull = []
    for ds, info in remote.items():
        if ds not in local or local[ds]["version"] != info["version"]:
            to_pull.append((ds, info))

    if not to_pull:
        print("All manifests already synced.")
        if pull_data:
            # Still need to check for missing data shards
            for ds, info in remote.items():
                _pull_data_shards(s3, bucket, prefix, workspace_root, ds, info["version"])
        return 0

    print(f"Checking {len(to_pull)} manifest(s) from s3://{bucket}/{prefix}/...\n")

    pulled = 0
    skipped = 0
    skipped_datasets = []

    for ds, info in to_pull:
        workspace, name = ds.split("/", 1)
        version = info["version"]

        # Download manifest first to validate
        manifest_key = info["key"]
        response = s3.get_object(Bucket=bucket, Key=manifest_key)
        manifest_data = response["Body"].read().decode("utf-8")

        # Validate all shards exist before saving
        if not skip_validation:
            is_valid, missing = _validate_manifest_shards(s3, bucket, manifest_data)
            if not is_valid:
                skipped += 1
                skipped_datasets.append((ds, len(missing)))
                continue

        # Create local directory
        manifest_dir = workspace_root / "manifests" / workspace / name
        manifest_dir.mkdir(parents=True, exist_ok=True)

        # Write manifest
        manifest_path = manifest_dir / f"{version}.json"
        with open(manifest_path, "w") as f:
            f.write(manifest_data)

        # Write latest.json
        latest_path = manifest_dir / "latest.json"
        with open(latest_path, "w") as f:
            json.dump({"version": version}, f)

        print(f"  {ds} (v{version[:8]})")
        pulled += 1

        # Pull data shards if requested
        if pull_data:
            _pull_data_shards(s3, bucket, prefix, workspace_root, ds, version)

    print(f"\nPulled {pulled} manifest(s)")

    if skipped > 0:
        sys.stdout.flush()  # Ensure stdout is flushed before stderr
        print(f"\nSkipped {skipped} dataset(s) with missing data:", file=sys.stderr)
        for ds, num_missing in skipped_datasets:
            print(f"  {ds} ({num_missing} missing shards)", file=sys.stderr)
        print(f"\nThese datasets have manifests on S3 but their data shards are missing.", file=sys.stderr)
        print(f"Use --skip-validation to pull anyway (not recommended).", file=sys.stderr)

    return 0


def _pull_data_shards(
    s3,
    bucket: str,
    prefix: str,
    workspace_root: Path,
    dataset_id: str,
    version: str,
) -> None:
    """Pull data shards for a dataset into the local mirror.

    Downloads shards from S3 to:
        workspace_root/data/{workspace}/{name}/{version}/...

    This creates a local mirror matching the remote layout.
    """
    from warpdata.manifest.model import Manifest

    workspace, name = dataset_id.split("/", 1)

    # Load manifest
    manifest_path = workspace_root / "manifests" / workspace / name / f"{version}.json"
    if not manifest_path.exists():
        print(f"    Warning: Manifest not found for {dataset_id}, skipping data pull")
        return

    with open(manifest_path) as f:
        manifest_data = json.load(f)

    manifest = Manifest.from_dict(manifest_data)

    # Use computed version_hash for local data paths (matches resolver behavior)
    # The manifest filename (version param) may differ from the computed hash
    computed_version = manifest.version_hash

    # Compute data prefix on S3
    # Extract from manifest.locations or derive from base prefix
    data_prefix = prefix.replace("/manifests", "/data")
    data_base = f"{data_prefix}/{workspace}/{name}/{version}"

    # Create local data directory using computed version_hash
    local_data_base = workspace_root / "data" / workspace / name / computed_version
    local_data_base.mkdir(parents=True, exist_ok=True)

    # Track shards to download
    shards_to_download = []

    def extract_s3_key_and_local_path(shard_key, shard_uri, byte_size):
        """Extract S3 key and local path from shard, handling both key-based and URI-based shards."""
        if shard_key:
            # Key-based: use data_base prefix
            s3_key = f"{data_base}/{shard_key}"
            local_path = local_data_base / shard_key
            return s3_key, local_path, byte_size
        elif shard_uri and shard_uri.startswith("s3://"):
            # URI-based: extract full path after bucket
            # URI format: s3://bucket/prefix/path/to/file
            parts = shard_uri.split("/", 3)
            if len(parts) >= 4:
                s3_key = parts[3]  # Everything after bucket
                # Derive cache key same way as resolver._derive_cache_key()
                # For paths containing "objects/", extract from there
                if "objects/" in s3_key:
                    cache_key = s3_key[s3_key.index("objects/"):]
                else:
                    # Fallback: use hash of URI for uniqueness
                    import hashlib
                    cache_key = f"cache/{hashlib.sha256(shard_uri.encode()).hexdigest()[:16]}"
                local_path = local_data_base / cache_key
                return s3_key, local_path, byte_size
        return None, None, None

    # Collect table shards
    for table_name, table in manifest.tables.items():
        for shard in table.shards:
            s3_key, local_path, byte_size = extract_s3_key_and_local_path(
                shard.key, shard.uri, shard.byte_size
            )
            if s3_key and local_path and not local_path.exists():
                shards_to_download.append((s3_key, local_path, byte_size))

    # Collect artifact shards
    for artifact_name, artifact in manifest.artifacts.items():
        for shard in artifact.shards:
            s3_key, local_path, byte_size = extract_s3_key_and_local_path(
                shard.key, shard.uri, shard.byte_size
            )
            if s3_key and local_path and not local_path.exists():
                shards_to_download.append((s3_key, local_path, byte_size))

        # Collect index if present
        if artifact.index:
            s3_key, local_path, byte_size = extract_s3_key_and_local_path(
                artifact.index.key, artifact.index.uri, artifact.index.byte_size
            )
            if s3_key and local_path and not local_path.exists():
                shards_to_download.append((s3_key, local_path, byte_size))

    # Deduplicate by s3_key (content-addressed storage may have same object referenced multiple times)
    seen_keys = set()
    unique_shards = []
    for s3_key, local_path, byte_size in shards_to_download:
        if s3_key not in seen_keys:
            seen_keys.add(s3_key)
            unique_shards.append((s3_key, local_path, byte_size))
    shards_to_download = unique_shards

    if not shards_to_download:
        print(f"    All data shards for {dataset_id} already present (version: {computed_version[:8]})")
        return

    total_bytes = sum(size or 0 for _, _, size in shards_to_download)
    total_mb = total_bytes / (1024 * 1024)
    print(f"    Downloading {len(shards_to_download)} shard(s) ({total_mb:.1f} MB) for {dataset_id} (version: {computed_version[:8]})...")

    # Try to use tqdm for progress
    try:
        from tqdm import tqdm
        has_tqdm = True
    except ImportError:
        has_tqdm = False

    downloaded = 0
    failed = 0

    if has_tqdm:
        # Download with overall progress bar
        with tqdm(
            total=total_bytes,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            desc=f"    {dataset_id}",
            bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{rate_fmt}]"
        ) as pbar:
            for s3_key, local_path, byte_size in shards_to_download:
                try:
                    local_path.parent.mkdir(parents=True, exist_ok=True)

                    # Download with callback to update progress
                    def make_callback(pbar):
                        def callback(bytes_transferred):
                            pbar.update(bytes_transferred)
                        return callback

                    s3.download_file(bucket, s3_key, str(local_path), Callback=make_callback(pbar))
                    downloaded += 1
                except Exception as e:
                    failed += 1
                    pbar.write(f"    Warning: Failed to download {s3_key}: {e}")
                    # Update progress bar even on failure
                    if byte_size:
                        pbar.update(byte_size)
    else:
        # Fallback without tqdm
        for s3_key, local_path, _ in shards_to_download:
            try:
                local_path.parent.mkdir(parents=True, exist_ok=True)
                s3.download_file(bucket, s3_key, str(local_path))
                downloaded += 1
            except Exception as e:
                failed += 1
                print(f"    Warning: Failed to download {s3_key}: {e}")

    if failed:
        print(f"    Downloaded {downloaded}/{len(shards_to_download)} shard(s), {failed} failed")
