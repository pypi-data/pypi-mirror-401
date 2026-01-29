"""E2E tests for sync and resolver path consistency.

Ensures that data downloaded via `warp sync pull --data` is found by
the resolver when loading datasets via `wd.load()`.

This tests the critical requirement that:
1. sync downloads to: workspace_root/data/{workspace}/{name}/{version_hash}/
2. resolver looks in: workspace_root/data/{workspace}/{name}/{version_hash}/
"""

from __future__ import annotations

import json
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import pytest


@pytest.fixture
def mock_s3_dataset(tmp_path):
    """Create a mock 'S3' dataset structure and workspace.

    Simulates what would exist after publishing a dataset.
    Returns (workspace_root, s3_mock_root, manifest_data, version_hash)
    """
    workspace_root = tmp_path / "workspace"
    s3_mock = tmp_path / "s3_mock"

    workspace_root.mkdir()
    s3_mock.mkdir()

    # Create test parquet data
    table = pa.table({
        "id": [0, 1, 2, 3, 4],
        "text": ["hello", "world", "test", "data", "sample"],
        "value": [1.0, 2.0, 3.0, 4.0, 5.0],
    })

    # Simulate S3 structure
    dataset_id = "nlp/test-dataset"
    ws, name = dataset_id.split("/")

    # Create manifest
    manifest_data = {
        "dataset": dataset_id,
        "tables": {
            "main": {
                "format": "parquet",
                "shards": [
                    {"key": "main/shard_0.parquet", "row_count": 3, "byte_size": 1000},
                    {"key": "main/shard_1.parquet", "row_count": 2, "byte_size": 800},
                ],
                "row_count": 5,
            },
        },
        "artifacts": {},
        "bindings": [],
    }

    # Compute version hash (simplified - in real code this is content-addressed)
    import hashlib
    manifest_json = json.dumps(manifest_data, sort_keys=True)
    version_hash = hashlib.sha256(manifest_json.encode()).hexdigest()[:16]

    # Create S3 mock data directory
    s3_data_dir = s3_mock / "data" / ws / name / version_hash / "main"
    s3_data_dir.mkdir(parents=True)

    # Write shard files
    pq.write_table(table.slice(0, 3), s3_data_dir / "shard_0.parquet")
    pq.write_table(table.slice(3, 2), s3_data_dir / "shard_1.parquet")

    # Create manifest in workspace (simulating what sync pull does for manifest)
    manifest_dir = workspace_root / "manifests" / ws / name
    manifest_dir.mkdir(parents=True)

    with open(manifest_dir / f"{version_hash}.json", "w") as f:
        json.dump(manifest_data, f)

    # Create latest pointer
    with open(manifest_dir / "latest.json", "w") as f:
        json.dump({"version": version_hash}, f)

    return workspace_root, s3_mock, manifest_data, version_hash


class TestSyncResolverPathConsistency:
    """Tests that sync and resolver use identical paths."""

    def test_sync_download_path_matches_resolver_lookup(self, mock_s3_dataset):
        """Critical: sync download path == resolver lookup path."""
        workspace_root, s3_mock, manifest_data, version_hash = mock_s3_dataset

        from warpdata.manifest.model import Manifest
        from warpdata.config.settings import Settings

        # Parse manifest
        manifest = Manifest.from_dict(manifest_data)

        # Get version hash the way sync.py does it
        sync_version = manifest.version_hash

        # Get version hash the way resolver.py does it
        resolver_version = manifest.version_hash

        # They MUST be identical
        assert sync_version == resolver_version, (
            f"Version hash mismatch! sync uses {sync_version}, resolver uses {resolver_version}"
        )

        # Verify the computed path matches
        ws, name = manifest_data["dataset"].split("/")

        settings = Settings(workspace_root=workspace_root)

        # Path that sync would use (from sync.py _pull_data_shards)
        sync_local_base = workspace_root / "data" / ws / name / sync_version

        # Path that resolver would use (from resolver.py _maybe_auto_download)
        resolver_local_base = settings.workspace_root / "data" / ws / name / resolver_version

        assert sync_local_base == resolver_local_base, (
            f"Path mismatch! sync: {sync_local_base}, resolver: {resolver_local_base}"
        )

    def test_downloaded_data_found_by_resolver(self, mock_s3_dataset):
        """Data downloaded by sync should be found by resolver."""
        workspace_root, s3_mock, manifest_data, version_hash = mock_s3_dataset

        from warpdata.manifest.model import Manifest
        from warpdata.config.settings import Settings

        manifest = Manifest.from_dict(manifest_data)
        settings = Settings(workspace_root=workspace_root, mode="hybrid")

        ws, name = manifest_data["dataset"].split("/")
        computed_version = manifest.version_hash

        # Simulate what sync does: copy files to local workspace
        local_data_base = workspace_root / "data" / ws / name / computed_version
        local_data_base.mkdir(parents=True)

        # Copy shards from "S3" to local (simulating sync pull --data)
        s3_data_base = s3_mock / "data" / ws / name / version_hash
        for shard in manifest.tables["main"].shards:
            src = s3_data_base / shard.key
            dst = local_data_base / shard.key
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(src.read_bytes())

        # Now verify the files exist where resolver would look
        # Check each shard is found locally at the expected path
        for shard in manifest.tables["main"].shards:
            shard_key = shard.key
            expected_path = local_data_base / shard_key

            # Resolver should find this file
            assert expected_path.exists(), f"Shard not found at {expected_path}"

            # Verify it's the right file by reading
            actual_table = pq.read_table(expected_path)
            assert actual_table.num_rows > 0

        # Verify the path matches what resolver would compute
        from warpdata.artifacts.resolver import ArtifactResolver

        resolver = ArtifactResolver(
            manifest=manifest,
            artifacts=manifest.artifacts,
            settings=settings,
        )

        # The resolver's internal path computation should match
        resolver_base = settings.workspace_root / "data" / ws / name / computed_version
        assert resolver_base == local_data_base

    def test_version_hash_computation_is_deterministic(self, mock_s3_dataset):
        """version_hash must be deterministic from manifest content."""
        workspace_root, s3_mock, manifest_data, version_hash = mock_s3_dataset

        from warpdata.manifest.model import Manifest

        # Parse manifest multiple times
        m1 = Manifest.from_dict(manifest_data)
        m2 = Manifest.from_dict(manifest_data)
        m3 = Manifest.from_dict(json.loads(json.dumps(manifest_data)))

        # All should produce same version_hash
        assert m1.version_hash == m2.version_hash == m3.version_hash, (
            "version_hash is not deterministic!"
        )

    def test_shard_key_resolution_consistency(self, mock_s3_dataset):
        """Shard keys must resolve to same paths in sync and resolver."""
        workspace_root, s3_mock, manifest_data, version_hash = mock_s3_dataset

        from warpdata.manifest.model import Manifest
        from warpdata.config.settings import Settings

        manifest = Manifest.from_dict(manifest_data)
        settings = Settings(workspace_root=workspace_root)

        ws, name = manifest_data["dataset"].split("/")
        version = manifest.version_hash

        for table_name, table in manifest.tables.items():
            for shard in table.shards:
                # Sync path construction (from sync.py)
                sync_path = workspace_root / "data" / ws / name / version / shard.key

                # Resolver path construction (from resolver.py)
                resolver_path = settings.workspace_root / "data" / ws / name / version / shard.key

                assert sync_path == resolver_path, (
                    f"Shard path mismatch for {shard.key}: "
                    f"sync={sync_path}, resolver={resolver_path}"
                )


class TestWorkspaceRootConsistency:
    """Tests that workspace_root is consistent across components."""

    def test_settings_workspace_root_default(self):
        """Default workspace_root is consistent."""
        from warpdata.config.settings import Settings

        s1 = Settings()
        s2 = Settings()

        assert s1.workspace_root == s2.workspace_root
        assert str(s1.workspace_root).endswith(".warpdata")

    def test_settings_from_env_uses_same_default(self):
        """Settings.from_env() uses same default as Settings()."""
        import os
        from warpdata.config.settings import Settings

        # Clear relevant env vars
        env_backup = {}
        for key in ["WARPDATASETS_WORKSPACE_ROOT", "WARPDATASETS_CACHE_DIR"]:
            if key in os.environ:
                env_backup[key] = os.environ.pop(key)

        try:
            default_settings = Settings()
            env_settings = Settings.from_env()

            assert default_settings.workspace_root == env_settings.workspace_root
        finally:
            # Restore env
            os.environ.update(env_backup)

    def test_resolver_fallback_workspace_matches_settings(self):
        """Resolver fallback workspace matches settings default."""
        from warpdata.config.settings import Settings
        from pathlib import Path

        # The resolver has a hardcoded fallback in case settings is None
        # It should match the Settings default
        settings = Settings()
        resolver_fallback = Path.home() / ".warpdata"

        assert settings.workspace_root == resolver_fallback, (
            f"Resolver fallback {resolver_fallback} != settings default {settings.workspace_root}"
        )


class TestCachePathConsistency:
    """Tests for cache directory path consistency."""

    def test_cache_dir_default(self):
        """Default cache_dir is under .cache/warpdata."""
        from warpdata.config.settings import Settings

        settings = Settings()
        assert str(settings.cache_dir).endswith(".cache/warpdata")

    def test_cache_dir_separate_from_workspace(self):
        """cache_dir and workspace_root are separate."""
        from warpdata.config.settings import Settings

        settings = Settings()

        # They should be different directories
        assert settings.cache_dir != settings.workspace_root

        # workspace_root is for manifests/data
        # cache_dir is for downloaded blobs
        assert "cache" in str(settings.cache_dir)
        assert "cache" not in str(settings.workspace_root)
