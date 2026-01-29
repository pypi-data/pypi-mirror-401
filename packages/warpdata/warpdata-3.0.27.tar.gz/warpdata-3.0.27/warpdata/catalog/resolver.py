"""Catalog resolver - resolves dataset IDs to manifests."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from warpdata.catalog.cache import CacheEntry, ManifestCache
from warpdata.catalog.store import FetchResult, ManifestStore
from warpdata.manifest.model import Manifest
from warpdata.manifest.validate import validate_manifest
from warpdata.util.errors import (
    DatasetNotFoundError,
    ManifestInvalidError,
    ManifestNotFoundError,
)
from warpdata.config.settings import LEGACY_S3_BUCKET, DEFAULT_S3_BUCKET

if TYPE_CHECKING:
    from pathlib import Path


def _migrate_manifest_uris(manifest_data: dict) -> dict:
    """Auto-migrate URIs from legacy AWS bucket to B2.

    This allows old manifests cached with warpbucket-warp URIs to work
    seamlessly with the new B2 default storage.

    Args:
        manifest_data: Raw manifest dictionary

    Returns:
        Manifest with migrated URIs
    """
    old_prefix = f"s3://{LEGACY_S3_BUCKET}/"
    new_prefix = f"s3://{DEFAULT_S3_BUCKET}/"

    def rewrite_uri(uri: str | None) -> str | None:
        if uri and uri.startswith(old_prefix):
            return uri.replace(old_prefix, new_prefix, 1)
        return uri

    # Rewrite table shard URIs
    for table in manifest_data.get("tables", {}).values():
        for shard in table.get("shards", []):
            if "uri" in shard:
                shard["uri"] = rewrite_uri(shard["uri"])

    # Rewrite artifact shard and index URIs
    for artifact in manifest_data.get("artifacts", {}).values():
        for shard in artifact.get("shards", []):
            if "uri" in shard:
                shard["uri"] = rewrite_uri(shard["uri"])
        if "index" in artifact and isinstance(artifact["index"], dict):
            if "uri" in artifact["index"]:
                artifact["index"]["uri"] = rewrite_uri(artifact["index"]["uri"])

    return manifest_data


class CatalogResolver:
    """Resolves dataset IDs to manifests with caching.

    Resolution flow:
    1. If version is None or "latest":
       - Fetch latest.json to get version hash
       - Fetch version.json
    2. If version is a hash:
       - Fetch version.json directly

    Caching:
    - Uses ETag/Last-Modified for conditional requests
    - Cache is keyed by (dataset_id, version)
    """

    def __init__(
        self,
        store: ManifestStore,
        cache: ManifestCache,
    ):
        self.store = store
        self.cache = cache

    def resolve(
        self,
        dataset_id: str,
        version: str | None = None,
    ) -> Manifest:
        """Resolve a dataset ID to a manifest.

        Args:
            dataset_id: Dataset identifier (workspace/name)
            version: Version hash or "latest" (default: "latest")

        Returns:
            Resolved and validated Manifest

        Raises:
            DatasetNotFoundError: If dataset doesn't exist
            ManifestNotFoundError: If version doesn't exist
            ManifestInvalidError: If manifest is malformed
        """
        # Determine version hash
        if version is None or version == "latest":
            version_hash = self._resolve_latest(dataset_id)
        else:
            version_hash = version

        # Fetch and parse manifest
        manifest = self._fetch_manifest(dataset_id, version_hash)

        # Validate
        try:
            validate_manifest(manifest)
        except Exception as e:
            raise ManifestInvalidError(dataset_id, str(e)) from e

        return manifest

    def _resolve_latest(self, dataset_id: str) -> str:
        """Resolve 'latest' pointer to version hash."""
        latest_path = f"{dataset_id}/latest.json"

        # Check cache for latest pointer
        cached = self.cache.get(dataset_id, "latest")
        etag = cached.etag if cached else None

        # Fetch with conditional request
        result = self.store.fetch(latest_path, if_none_match=etag)

        if result.is_not_found:
            raise DatasetNotFoundError(dataset_id)

        if result.is_not_modified and cached:
            # Use cached latest pointer
            content = cached.content
        elif result.is_success and result.content:
            # Update cache
            self.cache.put(
                dataset_id,
                "latest",
                CacheEntry(
                    content=result.content,
                    etag=result.etag,
                    last_modified=result.last_modified,
                ),
            )
            content = result.content
        else:
            raise DatasetNotFoundError(
                dataset_id,
                f"Failed to fetch latest pointer (status: {result.status})",
            )

        # Parse latest.json
        try:
            latest_data = json.loads(content)
            return latest_data["version"]
        except (json.JSONDecodeError, KeyError) as e:
            raise ManifestInvalidError(
                dataset_id,
                f"Invalid latest.json: {e}",
            ) from e

    def _fetch_manifest(self, dataset_id: str, version_hash: str) -> Manifest:
        """Fetch and parse a version manifest."""
        manifest_path = f"{dataset_id}/{version_hash}.json"

        # Check cache
        cached = self.cache.get(dataset_id, version_hash)
        etag = cached.etag if cached else None

        # Fetch with conditional request
        result = self.store.fetch(manifest_path, if_none_match=etag)

        if result.is_not_found:
            raise ManifestNotFoundError(dataset_id, version_hash)

        if result.is_not_modified and cached:
            content = cached.content
        elif result.is_success and result.content:
            # Update cache
            self.cache.put(
                dataset_id,
                version_hash,
                CacheEntry(
                    content=result.content,
                    etag=result.etag,
                    last_modified=result.last_modified,
                ),
            )
            content = result.content
        else:
            raise ManifestNotFoundError(dataset_id, version_hash)

        # Parse manifest
        try:
            manifest_data = json.loads(content)
            # Auto-migrate URIs from legacy AWS bucket to B2
            manifest_data = _migrate_manifest_uris(manifest_data)
            return Manifest.from_dict(manifest_data)
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            raise ManifestInvalidError(
                dataset_id,
                f"Invalid manifest JSON: {e}",
            ) from e
