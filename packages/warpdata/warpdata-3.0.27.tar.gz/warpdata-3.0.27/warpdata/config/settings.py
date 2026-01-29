"""Configuration settings with environment variable support."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

# Default B2 configuration for warpdata (Backblaze B2 as default storage)
# These can be overridden via environment variables
DEFAULT_S3_BUCKET = "warpdata"
DEFAULT_S3_PREFIX = "warpdatasets"
DEFAULT_S3_REGION = "us-east-005"
DEFAULT_S3_ENDPOINT_URL = f"https://s3.{DEFAULT_S3_REGION}.backblazeb2.com"
DEFAULT_MANIFEST_BASE = f"s3://{DEFAULT_S3_BUCKET}/{DEFAULT_S3_PREFIX}"

# Legacy AWS bucket (for URI migration)
LEGACY_S3_BUCKET = "warpbucket-warp"

# Legacy workspace root (for backwards compatibility with warpdatasets package)
LEGACY_WORKSPACE_ROOT = Path.home() / ".warpdatasets"


@dataclass
class Settings:
    """Configuration settings for warpdata.

    Settings are loaded from environment variables with WARPDATASETS_ prefix,
    and can be overridden programmatically.
    """

    # Workspace root for local datasets
    # Layout: workspace_root/manifests/{workspace}/{name}/{version}.json
    #         workspace_root/data/{workspace}/{name}/{version}/...
    workspace_root: Path = field(
        default_factory=lambda: Path.home() / ".warpdata"
    )

    # Manifest store configuration
    # Defaults to S3 bucket defined by DEFAULT_MANIFEST_BASE
    manifest_base: str | None = field(default_factory=lambda: DEFAULT_MANIFEST_BASE)

    # Cache configuration
    cache_dir: Path = field(default_factory=lambda: Path.home() / ".cache" / "warpdata")

    # Mode configuration
    # Default is "hybrid": local first, download from S3 on-demand and cache
    # - "hybrid": Check local cache first, download from S3 if missing (default, recommended)
    # - "strict": Download ALL shards upfront before any reads (good for batch jobs)
    # - "remote": Stream directly from S3 without caching (high latency, not recommended)
    # - "local": Only use local files, fail if not present (offline mode)
    # - "auto": Same as hybrid
    mode: Literal["strict", "remote", "hybrid", "local", "auto"] = "hybrid"
    prefetch: Literal["off", "auto", "aggressive"] = "off"

    # Scope determines validation rules
    # - "local": Allow local://, relative paths, and external:// URIs
    # - "published": Strict validation, no local or external paths
    scope: Literal["local", "published"] = "local"

    # S3 configuration
    s3_region: str | None = None
    s3_endpoint_url: str | None = None  # For MinIO, LocalStack, etc.

    # Safety thresholds
    large_data_threshold: int = 1_000_000  # Rows before pandas guardrail kicks in
    large_shard_threshold: int = 10  # Number of shards before size warning

    # Development flags (deprecated, use scope instead)
    allow_file_manifests: bool = False

    def resolve_local_uri(self, uri: str) -> Path:
        """Resolve a local:// URI to an absolute path.

        Args:
            uri: URI in form local://path/to/file or relative path

        Returns:
            Absolute path resolved against workspace_root
        """
        if uri.startswith("local://"):
            relpath = uri[8:]  # Remove "local://"
        else:
            relpath = uri
        return self.workspace_root / relpath

    def is_local_mode(self) -> bool:
        """Check if operating in local mode."""
        return self.mode == "local" or (
            self.mode == "auto" and self.manifest_base is None
        )

    @property
    def effective_manifest_base(self) -> str:
        """Get effective manifest base, defaulting to workspace root for local mode."""
        if self.manifest_base is not None:
            return self.manifest_base
        if self.is_local_mode():
            return str(self.workspace_root)
        return ""

    @classmethod
    def from_env(cls) -> Settings:
        """Load settings from environment variables."""
        # Determine workspace root (with legacy alias support)
        workspace_root_str = os.environ.get("WARPDATASETS_WORKSPACE_ROOT")
        if not workspace_root_str:
            # Check legacy env var
            workspace_root_str = os.environ.get("WARPDATASETS_ROOT")
            if workspace_root_str:
                import warnings
                warnings.warn(
                    "WARPDATASETS_ROOT is deprecated, use WARPDATASETS_WORKSPACE_ROOT instead",
                    DeprecationWarning,
                    stacklevel=2,
                )
        if not workspace_root_str:
            workspace_root_str = str(Path.home() / ".warpdata")
        workspace_root = Path(workspace_root_str)

        # Determine scope (defaults to local for frictionless local use)
        scope = os.environ.get("WARPDATASETS_SCOPE", "local")
        if scope not in ("local", "published"):
            scope = "local"

        # For backward compatibility, allow_file_manifests implies local scope
        allow_file_manifests = os.environ.get(
            "WARPDATASETS_ALLOW_FILE_MANIFESTS", ""
        ).lower() in ("1", "true", "yes")

        # Auto-derive S3 endpoint from B2_REGION if not explicitly set
        # Default to B2 endpoint if nothing is configured (B2 is the default storage)
        s3_endpoint = os.environ.get("WARPDATASETS_S3_ENDPOINT_URL")
        b2_bucket = os.environ.get("B2_BUCKET")
        b2_region = os.environ.get("B2_REGION")
        if not s3_endpoint:
            if b2_region:
                s3_endpoint = f"https://s3.{b2_region}.backblazeb2.com"
            else:
                # Default to B2 endpoint (warpdata uses B2 by default)
                s3_endpoint = DEFAULT_S3_ENDPOINT_URL

        # Auto-derive manifest_base from B2_BUCKET if set, otherwise use default
        manifest_base = os.environ.get("WARPDATASETS_MANIFEST_BASE")
        if not manifest_base:
            if b2_bucket:
                # User specified a custom B2 bucket
                manifest_base = f"s3://{b2_bucket}/warpdatasets"
            else:
                # Use default B2 bucket (warpdata)
                manifest_base = DEFAULT_MANIFEST_BASE

        return cls(
            workspace_root=workspace_root,
            manifest_base=manifest_base,
            cache_dir=Path(
                os.environ.get(
                    "WARPDATASETS_CACHE_DIR",
                    str(Path.home() / ".cache" / "warpdata"),
                )
            ),
            mode=os.environ.get("WARPDATASETS_MODE", "hybrid"),  # type: ignore
            prefetch=os.environ.get("WARPDATASETS_PREFETCH", "off"),  # type: ignore
            scope=scope,  # type: ignore
            # B2 region takes priority since B2 is the default storage
            s3_region=os.environ.get("WARPDATASETS_S3_REGION")
            or b2_region
            or os.environ.get("AWS_DEFAULT_REGION")
            or DEFAULT_S3_REGION,
            s3_endpoint_url=s3_endpoint,  # Use derived endpoint (may come from B2_REGION)
            large_data_threshold=int(
                os.environ.get("WARPDATASETS_LARGE_DATA_THRESHOLD", "1000000")
            ),
            allow_file_manifests=allow_file_manifests,
        )


# Global settings instance (lazy loaded)
_settings: Settings | None = None


def get_settings() -> Settings:
    """Get the global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings.from_env()
    return _settings


def reset_settings() -> None:
    """Reset the cached settings, forcing reload from environment on next access."""
    global _settings
    _settings = None


def configure(**kwargs) -> None:
    """Update global settings.

    Args:
        **kwargs: Settings to update
    """
    global _settings
    if _settings is None:
        _settings = Settings.from_env()

    for key, value in kwargs.items():
        if hasattr(_settings, key):
            setattr(_settings, key, value)
        else:
            raise ValueError(f"Unknown setting: {key}")
