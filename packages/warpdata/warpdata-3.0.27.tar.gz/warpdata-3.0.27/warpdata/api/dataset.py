"""Dataset and Table API - primary user-facing interface."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterator, Literal, Sequence
from urllib.parse import urlparse

import duckdb

from warpdata.catalog.cache import ManifestCache
from warpdata.catalog.resolver import CatalogResolver
from warpdata.catalog.store import ManifestStore
from warpdata.config.settings import Settings, get_settings
from warpdata.engines.duckdb import DuckDBEngine, get_engine
from warpdata.manifest.model import Manifest, ShardInfo, TableDescriptor
from warpdata.streaming.shard import ShardConfig, assign_shards, resolve_shard
from warpdata.streaming.batching import build_batch_query, stream_batches
from warpdata.util.errors import LargeDataError, StaleManifestError
from warpdata.util.uris import join_base_and_key, local_path_from_uri, file_uri_from_path, is_localish_uri
from warpdata.cache.context import CacheContext

if TYPE_CHECKING:
    import pandas as pd
    import pyarrow as pa


def _check_local_uris_exist(manifest: Manifest, settings: Settings) -> list[str]:
    """Check if local URIs in manifest exist.

    Returns list of missing URIs. Only checks legacy uri-based manifests.
    For portable key-based manifests, this is a no-op since resolution
    happens dynamically.
    """
    missing = []

    for table in manifest.tables.values():
        for shard in table.shards:
            # Skip portable key-based shards - they're resolved dynamically
            if shard.uri is None:
                continue

            uri = shard.uri
            if uri.startswith("local://"):
                # Resolve local:// to workspace path
                rel_path = uri[8:]  # Remove "local://"
                full_path = settings.workspace_root / rel_path
                if not full_path.exists():
                    missing.append(uri)
            elif uri.startswith("file://"):
                path = uri[7:]  # Remove "file://"
                if not Path(path).exists():
                    missing.append(uri)

    return missing


def _try_s3_fallback_if_local_missing(
    manifest: Manifest,
    dataset_id: str,
    settings: Settings
) -> Manifest:
    """If manifest has missing local URIs, try to pull S3 version.

    For portable manifests (with locations), this is largely unnecessary
    since the resolver will automatically try remote locations.

    Returns the S3 manifest if successful, otherwise the original manifest.
    """
    # For portable manifests with locations, no fallback needed
    # The resolver will try remote locations automatically
    if manifest.is_portable and manifest.locations:
        return manifest

    missing = _check_local_uris_exist(manifest, settings)

    if not missing:
        return manifest

    # Legacy manifest with missing local files - provide helpful error
    missing_list = "\n  ".join(missing[:5])
    if len(missing) > 5:
        missing_list += f"\n  ... and {len(missing) - 5} more"

    raise FileNotFoundError(
        f"Dataset '{dataset_id}' has local files that don't exist:\n  {missing_list}\n\n"
        f"This dataset was registered with local paths that aren't available here.\n"
        f"Options:\n"
        f"  1. Run 'warpdata sync pull' to get the remote version (if available)\n"
        f"  2. Copy the data files to the expected paths\n"
        f"  3. Re-register the dataset with 'warpdata register'"
    )


def _create_store(settings: Settings) -> ManifestStore:
    """Create appropriate manifest store based on settings.

    Always checks local workspace first, then falls back to remote.
    This ensures locally registered datasets are always accessible.
    """
    from warpdata.catalog.stores.file import FileManifestStore
    from warpdata.catalog.stores.chain import ChainManifestStore

    stores: list[ManifestStore] = []

    # Always add local store first (for locally registered datasets)
    local_path = settings.workspace_root / "manifests"
    if local_path.exists():
        stores.append(FileManifestStore(base_path=local_path))

    # Local-only mode: just use local store
    if not settings.manifest_base and settings.is_local_mode():
        if not stores:
            return FileManifestStore(base_path=local_path)
        return stores[0] if len(stores) == 1 else ChainManifestStore(stores)

    if not settings.manifest_base:
        raise ValueError(
            "WARPDATASETS_MANIFEST_BASE must be set. "
            "Example: s3://mybucket/warp or https://example.com/warp"
        )

    # Add remote store based on manifest_base
    parsed = urlparse(settings.manifest_base)

    if parsed.scheme == "s3":
        from warpdata.catalog.stores.s3 import S3ManifestStore

        # Extract bucket and prefix from s3://bucket/prefix/path
        bucket = parsed.netloc
        prefix = parsed.path.lstrip("/")
        if prefix:
            prefix = f"{prefix}/manifests"
        else:
            prefix = "manifests"

        stores.append(S3ManifestStore(
            bucket=bucket,
            prefix=prefix,
            region=settings.s3_region,
            endpoint_url=settings.s3_endpoint_url,
        ))

    elif parsed.scheme in ("http", "https"):
        from warpdata.catalog.stores.http import HttpManifestStore

        base_url = settings.manifest_base
        if not base_url.endswith("/manifests"):
            base_url = f"{base_url.rstrip('/')}/manifests/"

        stores.append(HttpManifestStore(base_url=base_url))

    elif parsed.scheme == "file" or not parsed.scheme:
        # File-based store (explicit path or local mode)
        path = parsed.path if parsed.scheme == "file" else settings.manifest_base
        remote_store = FileManifestStore(base_path=Path(path) / "manifests")
        if remote_store not in stores:  # Avoid duplicate if same path
            stores.append(remote_store)

    else:
        raise ValueError(f"Unsupported manifest store scheme: {parsed.scheme}")

    # Return chain store (local first, then remote)
    if len(stores) == 1:
        return stores[0]
    return ChainManifestStore(stores)


def _parse_dataset_id(dataset_id: str) -> tuple[str, str | None]:
    """Parse dataset ID with optional @version suffix.

    Args:
        dataset_id: Dataset ID, optionally with @version suffix
                   e.g., "vision/coco" or "vision/coco@abc123"

    Returns:
        Tuple of (dataset_id, version) where version may be None
    """
    if "@" in dataset_id:
        parts = dataset_id.rsplit("@", 1)
        return parts[0], parts[1]
    return dataset_id, None


def dataset(
    dataset_id: str,
    *,
    version: str | None = None,
    mode: Literal["remote", "hybrid", "local", "auto"] | None = None,
    cache_dir: str | Path | None = None,
    prefetch: Literal["off", "auto", "aggressive"] | None = None,
    settings: Settings | None = None,
) -> Dataset:
    """Load a dataset by ID.

    This is the primary entrypoint for accessing datasets.

    Args:
        dataset_id: Dataset identifier in "workspace/name" format, optionally
                   with @version suffix (e.g., "vision/coco@abc123")
        version: Version hash or "latest" (default: "latest"). If both
                version param and @version suffix are provided, raises error.
        mode: Access mode - None (use settings), "remote", "hybrid", "local", or "auto"
        cache_dir: Override cache directory
        prefetch: Prefetch mode - None (use settings), "off", "auto", or "aggressive"
        settings: Override settings (uses global settings if not provided)

    Returns:
        Dataset handle for accessing tables and metadata

    Raises:
        DatasetNotFoundError: If dataset doesn't exist
        ManifestNotFoundError: If version doesn't exist
        ManifestInvalidError: If manifest is malformed
        ValueError: If both version param and @version suffix are provided

    Example:
        >>> import warpdata as wd
        >>> ds = wd.dataset("vision/coco")
        >>> ds = wd.dataset("vision/coco@abc123")  # specific version
        >>> table = ds.table("main")
        >>> df = table.head(10).to_pandas()
    """
    from dataclasses import replace

    # Parse @version syntax
    dataset_id, inline_version = _parse_dataset_id(dataset_id)

    # Handle version precedence
    if inline_version and version:
        raise ValueError(
            f"Cannot specify version both in dataset ID ('{inline_version}') "
            f"and as parameter ('{version}'). Use one or the other."
        )
    if inline_version:
        version = inline_version

    # Get settings
    if settings is None:
        settings = get_settings()

    # Create copy of settings if any overrides are needed (avoid mutating global)
    overrides = {}
    if cache_dir is not None:
        overrides["cache_dir"] = Path(cache_dir)
    if mode is not None:
        overrides["mode"] = mode
    if prefetch is not None:
        overrides["prefetch"] = prefetch

    if overrides:
        settings = replace(settings, **overrides)

    # Create resolver
    store = _create_store(settings)
    cache = ManifestCache(cache_dir=settings.cache_dir / "manifests")
    resolver = CatalogResolver(store=store, cache=cache)

    # Resolve manifest
    manifest = resolver.resolve(dataset_id, version=version)

    # Check if manifest has inaccessible local URIs - try S3 fallback
    manifest = _try_s3_fallback_if_local_missing(manifest, dataset_id, settings)

    # Create engine
    engine = DuckDBEngine(settings=settings)

    # Create cache context if caching/prefetch enabled
    cache_context = None
    if settings.mode in ("hybrid", "local") or settings.prefetch != "off":
        cache_context = CacheContext(
            cache_dir=settings.cache_dir,
            prefetch_mode=settings.prefetch,
        )

    return Dataset(
        id=dataset_id,
        manifest=manifest,
        settings=settings,
        engine=engine,
        cache_context=cache_context,
        resolver=resolver,  # Pass resolver for auto-refresh capability
    )


def from_manifest(
    path: str | Path,
    *,
    mode: Literal["remote", "hybrid", "local", "auto"] | None = None,
    settings: Settings | None = None,
) -> "Dataset":
    """Load a dataset directly from a manifest file.

    Useful for testing locally registered datasets before publishing,
    or for loading manifests from non-standard locations.

    Args:
        path: Path to the manifest JSON file
        mode: Access mode (default: use settings)
        settings: Override settings (uses global settings if not provided)

    Returns:
        Dataset handle

    Example:
        >>> ds = wd.from_manifest("~/.warpdata/manifests/vision/my-dataset/abc123.json")
        >>> for row in ds.rows(limit=5):
        ...     print(row)
    """
    import json
    from dataclasses import replace

    path = Path(path).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"Manifest not found: {path}")

    # Load manifest
    manifest_data = json.loads(path.read_text())
    manifest = Manifest.from_dict(manifest_data)

    # Get settings
    if settings is None:
        settings = get_settings()

    if mode is not None:
        settings = replace(settings, mode=mode)

    # Create engine
    engine = DuckDBEngine(settings=settings)

    # Create cache context if needed
    cache_context = None
    if settings.mode in ("hybrid", "strict", "local") or settings.prefetch != "off":
        cache_context = CacheContext(
            cache_dir=settings.cache_dir,
            prefetch_mode=settings.prefetch,
        )

    return Dataset(
        id=manifest.dataset,
        manifest=manifest,
        settings=settings,
        engine=engine,
        cache_context=cache_context,
    )


class Dataset:
    """Handle to a resolved dataset.

    Provides access to tables and dataset metadata.
    Automatically refreshes manifest when stale data is detected.
    """

    def __init__(
        self,
        id: str,
        manifest: Manifest,
        settings: Settings,
        engine: DuckDBEngine,
        cache_context: CacheContext | None = None,
        resolver: CatalogResolver | None = None,
    ):
        """Initialize dataset handle.

        Args:
            id: Dataset identifier
            manifest: Resolved manifest
            settings: Configuration settings
            engine: DuckDB engine for queries
            cache_context: Optional cache context for caching/prefetch
            resolver: Optional catalog resolver for manifest refresh
        """
        self.id = id
        self.manifest = manifest
        self.settings = settings
        self._engine = engine
        self._cache_context = cache_context
        self._resolver = resolver
        self._refresh_attempted = False  # Prevent infinite refresh loops

    def _refresh_manifest(self) -> bool:
        """Refresh the manifest by fetching the latest version.

        Returns:
            True if manifest was refreshed, False if refresh not possible
        """
        import sys

        if self._resolver is None:
            return False

        if self._refresh_attempted:
            # Already tried refresh, don't loop
            return False

        self._refresh_attempted = True

        try:
            print(f"[auto-refresh] Stale manifest detected, fetching latest...", file=sys.stderr)

            # Clear the cache entry for this dataset's latest pointer
            # This forces a fresh fetch from remote
            self._resolver.cache.invalidate(self.id, "latest")

            # Re-resolve with fresh manifest
            new_manifest = self._resolver.resolve(self.id, version=None)

            if new_manifest.version_hash != self.manifest.version_hash:
                print(f"[auto-refresh] Updated {self.id}: {self.manifest.version_hash[:8]} -> {new_manifest.version_hash[:8]}", file=sys.stderr)
                self.manifest = new_manifest
                return True
            else:
                print(f"[auto-refresh] Manifest unchanged, shard may be truly missing", file=sys.stderr)
                return False

        except Exception as e:
            print(f"[auto-refresh] Failed to refresh manifest: {e}", file=sys.stderr)
            return False

    @property
    def version_hash(self) -> str:
        """Get the version hash of this dataset."""
        return self.manifest.version_hash

    @property
    def tables(self) -> list[str]:
        """List available table names."""
        return list(self.manifest.tables.keys())

    @property
    def artifacts(self) -> list[str]:
        """List available artifact names.

        Artifacts contain binary data (images, audio, etc.) that are
        referenced from table columns via bindings.

        Example:
            >>> ds.artifacts
            ['train_images', 'train_labels', 'test_images']

            >>> # Read artifact data directly
            >>> data = ds.read_artifact("train_images", "sample.tif")

            >>> # Or iterate with automatic loading
            >>> for row in ds.rows(wrap_refs=True):
            ...     img = row["train_images"].as_pil()
        """
        return list(self.manifest.artifacts.keys()) if self.manifest.artifacts else []

    @property
    def bindings(self) -> list[dict[str, str]]:
        """List column-to-artifact bindings.

        Shows which table columns reference which artifacts.

        Example:
            >>> ds.bindings
            [{'table': 'main', 'column': 'train_images', 'artifact': 'train_images'},
             {'table': 'main', 'column': 'train_labels', 'artifact': 'train_labels'}]
        """
        if not self.manifest.bindings:
            return []
        return [
            {
                "table": b.table,
                "column": b.column,
                "artifact": b.artifact,
                "media_type": b.media_type,
            }
            for b in self.manifest.bindings
        ]

    def list_tables(self) -> list[str]:
        """List available table names.

        This is an alias for the `tables` property, provided for
        consistency with users who expect a method call.

        Returns:
            List of table names
        """
        return self.tables

    def table(self, name: str = "main") -> Table:
        """Get a table by name.

        Args:
            name: Table name (default: "main")

        Returns:
            Table handle for queries

        Raises:
            KeyError: If table doesn't exist
        """
        if name not in self.manifest.tables:
            available = ", ".join(self.manifest.tables.keys())
            raise KeyError(
                f"Table '{name}' not found. Available tables: {available}"
            )

        return Table(
            name=name,
            descriptor=self.manifest.tables[name],
            manifest=self.manifest,
            settings=self.settings,
            engine=self._engine,
            cache_context=self._cache_context,
            dataset=self,  # Pass reference for auto-refresh
        )

    def rows(
        self,
        table: str = "main",
        columns: list[str] | None = None,
        batch_size: int = 1000,
        limit: int | None = None,
        wrap_refs: bool = False,
    ) -> Iterator[dict[str, Any]]:
        """Iterate over rows as dictionaries.

        Convenience method for simple iteration over dataset rows.
        For better performance with large datasets, use table().batch_dicts().

        Args:
            table: Table name (default: "main")
            columns: Columns to include (default: all)
            batch_size: Internal batch size for streaming
            limit: Maximum number of rows to yield (default: all)
            wrap_refs: If True, wrap artifact-bound columns as typed refs that
                      can load actual data (e.g., ImageRef with .as_pil(), .read_bytes())

        Yields:
            Row dictionaries. If wrap_refs=True, bound columns contain Ref objects
            instead of raw filenames.

        Example:
            >>> # Basic iteration (filenames only)
            >>> for row in ds.rows(limit=10):
            ...     print(row["id"], row["label"])

            >>> # With artifact data loading
            >>> for row in ds.rows(wrap_refs=True, limit=1):
            ...     image_ref = row["image"]  # ImageRef object
            ...     pil_image = image_ref.as_pil()  # Load actual image
            ...     numpy_array = image_ref.as_numpy()
            ...     raw_bytes = image_ref.read_bytes()
        """
        tbl = self.table(table)
        count = 0
        for batch_dict in tbl.batch_dicts(batch_size=batch_size, columns=columns, wrap_refs=wrap_refs):
            # batch_dict is {col: [values...]}
            n_rows = len(next(iter(batch_dict.values())))
            for i in range(n_rows):
                if limit is not None and count >= limit:
                    return
                yield {col: values[i] for col, values in batch_dict.items()}
                count += 1

    def read_artifact(self, artifact_name: str, filename: str) -> bytes:
        """Read raw bytes from an artifact.

        Convenience method for directly accessing artifact data without
        going through table iteration.

        Args:
            artifact_name: Name of the artifact (e.g., "train_images")
            filename: Filename/member path within the artifact

        Returns:
            Raw bytes of the file

        Example:
            >>> # Direct artifact access
            >>> data = ds.read_artifact("train_images", "1407735.tif")
            >>> from PIL import Image
            >>> import io
            >>> img = Image.open(io.BytesIO(data))

            >>> # Or use rows(wrap_refs=True) for automatic loading
            >>> for row in ds.rows(wrap_refs=True, limit=1):
            ...     img = row["train_images"].as_pil()
        """
        from warpdata.artifacts.resolver import ArtifactResolver

        resolver = ArtifactResolver(
            manifest=self.manifest,
            settings=self.settings,
        )
        return resolver.read_bytes(artifact_name, filename)

    def info(self) -> dict[str, Any]:
        """Get dataset information.

        Returns:
            Dictionary with dataset metadata
        """
        info = {
            "id": self.id,
            "version": self.version_hash,
            "tables": {
                name: {
                    "format": table.format,
                    "shards": len(table.shards),
                    "row_count": table.row_count,
                    "schema": table.schema,
                }
                for name, table in self.manifest.tables.items()
            },
            "artifacts": list(self.manifest.artifacts.keys()),
            "bindings": len(self.manifest.bindings),
        }

        # Include addons
        if self.manifest.addons:
            info["addons"] = {
                name: {
                    "kind": addon.kind,
                    "base_table": addon.base_table,
                }
                for name, addon in self.manifest.addons.items()
            }

        return info

    def stream(
        self,
        table: str = "main",
        **kwargs,
    ) -> Iterator["pa.RecordBatch"] | Iterator[dict[str, list]]:
        """Stream batches from a table.

        Convenience method that wraps Table.batches().

        Args:
            table: Table name (default: "main")
            **kwargs: Arguments passed to Table.batches()

        Yields:
            Arrow RecordBatch or dict-of-lists depending on as_format
        """
        return self.table(table).batches(**kwargs)

    # Addon methods

    @property
    def addon_names(self) -> list[str]:
        """List available addon names."""
        return list(self.manifest.addons.keys())

    def addon(self, name: str):
        """Get an addon by name.

        Args:
            name: Addon name

        Returns:
            Addon handle (type depends on addon kind)

        Raises:
            KeyError: If addon doesn't exist
        """
        if name not in self.manifest.addons:
            available = ", ".join(self.manifest.addons.keys())
            raise KeyError(
                f"Addon '{name}' not found. Available addons: {available}"
            )

        descriptor = self.manifest.addons[name]

        if descriptor.is_embedding:
            from warpdata.addons import EmbeddingSpace

            return EmbeddingSpace(
                name=name,
                descriptor=descriptor,
                manifest=self.manifest,
                settings=self.settings,
                engine=self._engine,
                cache_context=self._cache_context,
            )

        # Generic addon - return descriptor for now
        return descriptor

    def embeddings(self, name: str = None):
        """Get an embedding space by name.

        Convenience method that wraps addon() for embedding addons.

        Args:
            name: Embedding space name. If None, returns the first
                embedding addon if exactly one exists.

        Returns:
            EmbeddingSpace handle

        Raises:
            KeyError: If embedding space doesn't exist
            ValueError: If name is None and there are 0 or 2+ embedding addons
        """
        from warpdata.addons import EmbeddingSpace

        # Find all embedding addons
        embedding_addons = {
            k: v for k, v in self.manifest.addons.items()
            if v.is_embedding
        }

        if name is None:
            if len(embedding_addons) == 0:
                raise KeyError("No embedding addons found in this dataset")
            if len(embedding_addons) > 1:
                names = ", ".join(embedding_addons.keys())
                raise ValueError(
                    f"Multiple embedding addons found: {names}. "
                    "Please specify a name."
                )
            name = next(iter(embedding_addons.keys()))

        if name not in self.manifest.addons:
            available = ", ".join(embedding_addons.keys()) or "(none)"
            raise KeyError(
                f"Embedding space '{name}' not found. "
                f"Available embedding addons: {available}"
            )

        descriptor = self.manifest.addons[name]
        if not descriptor.is_embedding:
            raise ValueError(f"Addon '{name}' is not an embedding space")

        return EmbeddingSpace(
            name=name,
            descriptor=descriptor,
            manifest=self.manifest,
            settings=self.settings,
            engine=self._engine,
            cache_context=self._cache_context,
        )

    def build_embeddings(
        self,
        name: str,
        provider: str,
        model: str,
        dims: int,
        *,
        source_columns: list[str] | None = None,
        table: str = "main",
        key_column: str = "rid",
        metric: str = "cosine",
        normalized: bool = True,
        batch_size: int = 100,
        build_index: bool = False,
        index_type: str = "flat",
        output_dir: Path | str | None = None,
        api_key: str | None = None,
        device: str | None = None,
        progress: bool = True,
    ):
        """Build embeddings for this dataset.

        Computes embeddings using the specified provider and stores them
        as a local addon.

        Args:
            name: Addon name (e.g., "clip-vit-l14@openai")
            provider: Embedding provider ("openai", "sentence-transformers")
            model: Model identifier
            dims: Expected output dimensions
            source_columns: Columns to embed (concatenated)
            table: Table to embed
            key_column: Column to use as join key
            metric: Distance metric
            normalized: Whether to normalize vectors
            batch_size: Rows per embedding batch
            build_index: Whether to build FAISS index
            index_type: Type of FAISS index ("flat", "hnsw")
            output_dir: Output directory (default: workspace)
            api_key: API key for provider (or use env var)
            device: Device for local models ("cuda", "cpu")
            progress: Show progress bar

        Returns:
            AddonDescriptor for the built embeddings

        Example:
            >>> ds = wd.dataset("test/texts")
            >>> addon = ds.build_embeddings(
            ...     name="mini-lm",
            ...     provider="sentence-transformers",
            ...     model="all-MiniLM-L6-v2",
            ...     dims=384,
            ...     source_columns=["text"],
            ... )
        """
        from warpdata.addons import build_embeddings

        return build_embeddings(
            dataset=self,
            name=name,
            provider=provider,
            model=model,
            dims=dims,
            source_columns=source_columns,
            table=table,
            key_column=key_column,
            metric=metric,
            normalized=normalized,
            batch_size=batch_size,
            build_index=build_index,
            index_type=index_type,
            output_dir=output_dir,
            api_key=api_key,
            device=device,
            progress=progress,
        )


class Table:
    """Handle to a table within a dataset.

    Provides methods for querying and accessing table data.
    Supports auto-refresh when stale manifest is detected.
    """

    def __init__(
        self,
        name: str,
        descriptor: TableDescriptor,
        manifest: Manifest,
        settings: Settings,
        engine: DuckDBEngine,
        cache_context: CacheContext | None = None,
        dataset: "Dataset | None" = None,
    ):
        """Initialize table handle.

        Args:
            name: Table name
            descriptor: Table descriptor from manifest
            manifest: Parent manifest
            settings: Configuration settings
            engine: DuckDB engine for queries
            cache_context: Optional cache context for caching/prefetch
            dataset: Parent dataset for auto-refresh capability
        """
        self.name = name
        self.descriptor = descriptor
        self.manifest = manifest
        self._settings = settings
        self._engine = engine
        self._cache_context = cache_context
        self._dataset = dataset

    def _try_refresh_manifest(self) -> bool:
        """Try to refresh the manifest via parent dataset.

        Returns:
            True if manifest was refreshed successfully
        """
        if self._dataset is None:
            return False

        refreshed = self._dataset._refresh_manifest()
        if refreshed:
            # Update our reference to the new manifest
            self.manifest = self._dataset.manifest
            self.descriptor = self.manifest.tables.get(self.name, self.descriptor)
        return refreshed

    def _is_stale_manifest_error(self, error: Exception) -> bool:
        """Check if an error indicates a stale manifest (404 on shard).

        Catches both our StaleManifestError and DuckDB/boto3 404 errors.
        """
        # Our explicit StaleManifestError
        if isinstance(error, StaleManifestError):
            return True

        # DuckDB httpfs 404 errors
        error_str = str(error).lower()
        if "404" in error_str or "not found" in error_str:
            if "http" in error_str or "s3" in error_str or "parquet" in error_str:
                return True

        # boto3 ClientError with 404/NoSuchKey
        if hasattr(error, "response"):
            error_code = getattr(error, "response", {}).get("Error", {}).get("Code", "")
            if error_code in ("404", "NoSuchKey"):
                return True

        return False

    def _with_auto_refresh(self, operation, *args, **kwargs):
        """Execute an operation with auto-refresh on stale manifest.

        If the operation fails due to a 404/stale manifest error,
        refreshes the manifest and retries once.
        """
        try:
            return operation(*args, **kwargs)
        except Exception as e:
            if self._is_stale_manifest_error(e):
                if self._try_refresh_manifest():
                    # Retry with refreshed manifest
                    return operation(*args, **kwargs)
            raise

    def _wrap_iterator_with_refresh(self, iterator_factory):
        """Wrap an iterator factory with auto-refresh on first error.

        If an error occurs during iteration that indicates a stale manifest,
        refreshes the manifest and creates a new iterator to restart.

        Args:
            iterator_factory: A callable that returns a fresh iterator

        Yields:
            Items from the iterator
        """
        iterator = iterator_factory()
        refresh_attempted = False

        while True:
            try:
                yield next(iterator)
            except StopIteration:
                return
            except Exception as e:
                if not refresh_attempted and self._is_stale_manifest_error(e):
                    if self._try_refresh_manifest():
                        # Restart with fresh iterator
                        refresh_attempted = True
                        iterator = iterator_factory()
                        continue
                raise

    @property
    def row_count(self) -> int | None:
        """Get row count if known."""
        return self.descriptor.row_count

    @property
    def shard_count(self) -> int:
        """Get number of shards."""
        return len(self.descriptor.shards)

    def _data_locations(self) -> list[str]:
        """Get ordered list of data locations to try when resolving shard keys.

        Priority order:
        1. Local mirror (if in local/hybrid/auto mode)
        2. Manifest locations
        3. Derived remote location from settings.manifest_base

        Returns:
            List of base URIs to try, in priority order
        """
        ws, name = self.manifest.dataset.split("/", 1)
        version = self.manifest.version_hash

        locs: list[str] = []

        # Local mirror - try first if in local/hybrid/auto mode
        if self._settings.mode in ("local", "hybrid", "auto"):
            local_base = f"local://data/{ws}/{name}/{version}/"
            locs.append(local_base)

        # Manifest-specified locations
        if self.manifest.locations:
            locs.extend(self.manifest.locations)

        # Derived remote location from manifest_base
        if self._settings.manifest_base:
            derived = f"{self._settings.manifest_base.rstrip('/')}/data/{ws}/{name}/{version}/"
            if derived not in locs:
                locs.append(derived)

        # De-duplicate while preserving order
        seen: set[str] = set()
        result: list[str] = []
        for loc in locs:
            if loc and loc not in seen:
                seen.add(loc)
                result.append(loc)

        return result

    def _resolve_shard_uri(self, shard: ShardInfo) -> str:
        """Resolve a shard to a usable URI.

        For legacy shards with uri, returns the uri directly.
        For portable shards with key, tries locations in priority order.

        Args:
            shard: ShardInfo with either uri or key

        Returns:
            Resolved URI (file://, s3://, etc.)

        Raises:
            FileNotFoundError: If no valid location found for the shard
        """
        # Legacy: if shard has uri, use it directly
        if shard.uri is not None:
            return shard.uri

        # Portable: resolve key against locations
        key = shard.key
        if key is None:
            raise ValueError("Shard has neither uri nor key")

        # Try each location in priority order
        for base in self._data_locations():
            candidate = join_base_and_key(base, key)

            # Check if it's a local-ish URI and if the file exists
            local_path = local_path_from_uri(candidate, self._settings.workspace_root)
            if local_path is not None:
                if local_path.exists():
                    return file_uri_from_path(local_path)
                # Local path doesn't exist, try next location
                continue

            # Remote candidate - apply cache context if available
            if self._cache_context is not None:
                candidate = self._cache_context.resolve_uri(candidate)

            # Return first remote candidate (assume it exists)
            return candidate

        raise FileNotFoundError(
            f"No valid location found for shard key={key}. "
            f"Tried locations: {self._data_locations()}"
        )

    def _resolve_all_shards(self) -> list[str]:
        """Resolve all shards to usable URIs.

        Returns:
            List of resolved URIs for all shards in this table
        """
        return [self._resolve_shard_uri(s) for s in self.descriptor.shards]

    def schema(self) -> dict[str, str]:
        """Get table schema.

        Returns:
            Dictionary mapping column names to types
        """
        # If manifest has schema, use it
        if self.descriptor.schema:
            return self.descriptor.schema
        # Otherwise, get schema from first resolved shard
        resolved_uris = self._resolve_all_shards()
        resolved_uris = self._resolve_local_uris(resolved_uris)
        return self._engine.describe_schema_from_uris(resolved_uris)

    def duckdb(self) -> duckdb.DuckDBPyRelation:
        """Get a lazy DuckDB relation for this table.

        Returns:
            DuckDB relation (not materialized)
        """
        # Resolve all shard URIs and create relation with resolved URIs
        resolved_uris = self._resolve_all_shards()
        # Resolve local:// URIs to file:// paths
        resolved_uris = self._resolve_local_uris(resolved_uris)
        return self._engine.create_relation_from_uris(resolved_uris)

    def head(self, n: int = 5) -> duckdb.DuckDBPyRelation:
        """Preview first n rows.

        Args:
            n: Number of rows (default: 5)

        Returns:
            DuckDB relation limited to n rows
        """
        return self.duckdb().limit(n)

    def select(self, *columns: str) -> duckdb.DuckDBPyRelation:
        """Select specific columns.

        Args:
            *columns: Column names to select

        Returns:
            DuckDB relation with selected columns
        """
        return self.duckdb().select(*columns)

    def _resolve_local_uris(self, uris: list[str]) -> list[str]:
        """Resolve local:// URIs to file:// URIs.

        Args:
            uris: List of URIs (may include local://, file://, s3://, etc.)

        Returns:
            List with local:// URIs converted to file:// paths
        """
        resolved = []
        for uri in uris:
            if uri.startswith("local://"):
                # Resolve against workspace root
                path = self._settings.resolve_local_uri(uri)
                resolved.append(path.as_uri())  # Convert to file:// URI
            else:
                resolved.append(uri)
        return resolved

    def filter(self, condition: str) -> duckdb.DuckDBPyRelation:
        """Filter rows by condition.

        Args:
            condition: SQL WHERE condition

        Returns:
            DuckDB relation with filter applied
        """
        return self.duckdb().filter(condition)

    def query(self, sql: str) -> "pd.DataFrame":
        """Execute a SQL query against this table.

        The table is available as "{table_name}" (e.g., "main") in your SQL.
        This is a convenience method that creates a DuckDB connection,
        registers the table, and executes your query.

        Automatically refreshes manifest and retries if data returns 404.

        Args:
            sql: SQL query string. Use the table name (e.g., "main") to
                 reference this table's data.

        Returns:
            pandas DataFrame with query results

        Example:
            >>> df = table.query("SELECT label, COUNT(*) as n FROM main GROUP BY label")
            >>> df = table.query("SELECT * FROM main WHERE score > 0.9 LIMIT 100")
        """
        def _do_query():
            # Get a fresh connection and register this table
            conn = self._engine._get_connection()

            # Resolve URIs and create a view for this table
            resolved_uris = self._resolve_all_shards()
            resolved_uris = self._resolve_local_uris(resolved_uris)

            # Build parquet read expression
            if len(resolved_uris) == 1:
                parquet_expr = f"read_parquet('{resolved_uris[0]}')"
            else:
                uri_list = ", ".join(f"'{uri}'" for uri in resolved_uris)
                parquet_expr = f"read_parquet([{uri_list}])"

            # Create view with table name
            conn.execute(f"CREATE OR REPLACE VIEW {self.name} AS SELECT * FROM {parquet_expr}")

            # Execute user query
            try:
                result = conn.execute(sql).df()
            finally:
                # Clean up view
                conn.execute(f"DROP VIEW IF EXISTS {self.name}")

            return result

        return self._with_auto_refresh(_do_query)

    def to_pandas(
        self,
        *,
        limit: int | None = None,
        allow_large: bool = False,
    ) -> "pd.DataFrame":
        """Convert to pandas DataFrame.

        Automatically refreshes manifest and retries if data returns 404.

        Args:
            limit: Maximum rows to return (required for large datasets)
            allow_large: Bypass large data guardrail

        Returns:
            pandas DataFrame

        Raises:
            LargeDataError: If dataset is large and no limit/override provided
        """
        # Check guardrails
        if not allow_large and limit is None:
            self._check_large_data_guardrail()

        def _do_pandas():
            relation = self.duckdb()
            if limit is not None:
                relation = relation.limit(limit)
            return relation.df()

        return self._with_auto_refresh(_do_pandas)

    def to_arrow(
        self,
        *,
        limit: int | None = None,
        allow_large: bool = False,
    ) -> "pa.Table":
        """Convert to PyArrow Table.

        Automatically refreshes manifest and retries if data returns 404.

        Args:
            limit: Maximum rows to return
            allow_large: Bypass large data guardrail

        Returns:
            PyArrow Table
        """
        if not allow_large and limit is None:
            self._check_large_data_guardrail()

        def _do_arrow():
            relation = self.duckdb()
            if limit is not None:
                relation = relation.limit(limit)
            return relation.arrow()

        return self._with_auto_refresh(_do_arrow)

    def _check_large_data_guardrail(self) -> None:
        """Check if dataset is too large for memory materialization."""
        from warpdata.config.settings import get_settings

        settings = get_settings()
        threshold = settings.large_data_threshold

        # Check by row count
        if self.row_count is not None and self.row_count > threshold:
            raise LargeDataError(self.row_count, threshold)

        # Check by shard count (conservative estimate)
        if (
            self.row_count is None
            and self.shard_count >= settings.large_shard_threshold
        ):
            raise LargeDataError(None, threshold)

    def batches(
        self,
        *,
        batch_size: int = 50_000,
        columns: Sequence[str] | None = None,
        shard: tuple[int, int] | str | None = None,
        limit: int | None = None,
        as_format: Literal["arrow", "dict"] = "arrow",
        wrap_refs: bool = False,
    ) -> Iterator["pa.RecordBatch"] | Iterator[dict[str, list]]:
        """Stream batches from this table.

        This is the primary method for training-native data access.
        Streaming is remote-first and does not require prefetch/pull.

        Args:
            batch_size: Rows per batch (default: 50,000)
            columns: Column names to select (None for all)
            shard: Sharding configuration:
                - None: All shards (single worker)
                - (rank, world_size): Explicit sharding
                - "auto": Parse from RANK/WORLD_SIZE env vars
            limit: Maximum total rows to return (None for unlimited)
            as_format: Output format - "arrow" (default) or "dict"
            wrap_refs: If True, wrap bound columns as typed refs (Phase 3).
                Requires as_format="dict".

        Yields:
            Arrow RecordBatch if as_format="arrow"
            dict[str, list] if as_format="dict"

        Example:
            >>> for batch in table.batches(batch_size=10000, columns=["id", "text"]):
            ...     # Process Arrow batch
            ...     pass

            >>> for batch in table.batches(shard="auto", as_format="dict"):
            ...     # Process dict-of-lists batch
            ...     ids = batch["id"]

            >>> for batch in table.batches(as_format="dict", wrap_refs=True):
            ...     # Access typed refs
            ...     img = batch["image"][0].as_pil()
        """
        import pyarrow as pa

        # Validate wrap_refs usage
        if wrap_refs and as_format != "dict":
            raise ValueError("wrap_refs=True requires as_format='dict'")

        # Resolve sharding
        shard_config = resolve_shard(shard)

        # Resolve all shard URIs (handles both legacy uri and portable key)
        all_uris = self._resolve_all_shards()
        assigned_uris = assign_shards(all_uris, shard_config)

        # Handle case where worker has no shards
        if not assigned_uris:
            return iter([])

        # Resolve URIs through cache (if cache context available)
        if self._cache_context is not None:
            resolved_uris = self._cache_context.resolve_uris(assigned_uris)
            # Trigger prefetch for upcoming shards (non-blocking)
            self._cache_context.trigger_prefetch(assigned_uris, current_index=-1)
        else:
            resolved_uris = list(assigned_uris)

        # Resolve any remaining local:// URIs to absolute paths
        resolved_uris = self._resolve_local_uris(resolved_uris)

        # Build query with resolved URIs
        query = build_batch_query(
            uris=resolved_uris,
            columns=list(columns) if columns else None,
            limit=limit,
        )

        # Get connection and stream
        conn = self._engine._get_connection()
        batch_iter = stream_batches(conn, query, batch_size, as_format)

        # Wrap refs if requested
        if wrap_refs:
            return self._wrap_batches_with_refs(batch_iter)

        return batch_iter

    def _wrap_batches_with_refs(
        self,
        batch_iter: Iterator[dict[str, list]],
    ) -> Iterator[dict[str, list]]:
        """Wrap bound columns in batches with typed refs.

        Args:
            batch_iter: Iterator of dict batches

        Yields:
            Dict batches with bound columns wrapped as typed refs.
        """
        from warpdata.artifacts.resolver import ArtifactResolver
        from warpdata.refs.factory import create_ref

        # Get bindings for this table
        bindings = [b for b in self.manifest.bindings if b.table == self.name]

        if not bindings:
            # No bindings, pass through unchanged
            yield from batch_iter
            return

        # Create resolver with cache context and settings
        resolver = ArtifactResolver(
            self.manifest,
            cache_context=self._cache_context,
            settings=self._settings,
        )

        # Build binding lookup: column -> (artifact, media_type)
        binding_map = {
            b.column: (b.artifact, b.media_type)
            for b in bindings
        }

        for batch in batch_iter:
            wrapped_batch = {}
            for col_name, values in batch.items():
                if col_name in binding_map:
                    artifact_name, media_type = binding_map[col_name]
                    wrapped_batch[col_name] = [
                        create_ref(
                            artifact_name=artifact_name,
                            ref_value=v,
                            media_type=media_type,
                            resolver=resolver,
                        )
                        for v in values
                    ]
                else:
                    wrapped_batch[col_name] = values
            yield wrapped_batch

    def batch_dicts(
        self,
        *,
        batch_size: int = 50_000,
        columns: Sequence[str] | None = None,
        shard: tuple[int, int] | str | None = None,
        limit: int | None = None,
        wrap_refs: bool = False,
    ) -> Iterator[dict[str, list]]:
        """Stream batches as dict-of-lists.

        Convenience wrapper for batches(as_format="dict").

        Args:
            batch_size: Rows per batch (default: 50,000)
            columns: Column names to select (None for all)
            shard: Sharding configuration
            limit: Maximum total rows to return
            wrap_refs: If True, wrap bound columns as typed refs

        Yields:
            dict[str, list] for each batch
        """
        return self.batches(
            batch_size=batch_size,
            columns=columns,
            shard=shard,
            limit=limit,
            as_format="dict",
            wrap_refs=wrap_refs,
        )
