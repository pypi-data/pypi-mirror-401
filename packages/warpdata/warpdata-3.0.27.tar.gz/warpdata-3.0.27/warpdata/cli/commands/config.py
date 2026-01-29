"""Config command - show effective configuration."""

from __future__ import annotations

import argparse
import json
import os
import sys


# Map of setting names to their environment variable sources
ENV_VAR_MAP = {
    "workspace_root": ["WARPDATASETS_WORKSPACE_ROOT", "WARPDATASETS_ROOT"],
    "manifest_base": ["WARPDATASETS_MANIFEST_BASE", "B2_BUCKET"],
    "cache_dir": ["WARPDATASETS_CACHE_DIR"],
    "mode": ["WARPDATASETS_MODE"],
    "prefetch": ["WARPDATASETS_PREFETCH"],
    "scope": ["WARPDATASETS_SCOPE"],
    "s3_region": ["WARPDATASETS_S3_REGION", "AWS_DEFAULT_REGION", "B2_REGION"],
    "s3_endpoint_url": ["WARPDATASETS_S3_ENDPOINT_URL"],
}


def _get_source(setting_name: str) -> str:
    """Determine the source of a setting value."""
    env_vars = ENV_VAR_MAP.get(setting_name, [])
    for var in env_vars:
        if os.environ.get(var):
            return f"env:{var}"
    return "default"


def run(args: argparse.Namespace) -> int:
    """Display effective configuration and sources."""
    from warpdata.config.settings import get_settings

    settings = get_settings()

    # Build config data
    config_data = {
        "workspace_root": str(settings.workspace_root),
        "manifest_base": settings.manifest_base,
        "cache_dir": str(settings.cache_dir),
        "mode": settings.mode,
        "prefetch": settings.prefetch,
        "scope": settings.scope,
        "s3_region": settings.s3_region,
        "s3_endpoint_url": settings.s3_endpoint_url,
    }

    # Check for UI format
    from warpdata.cli.ui import should_use_ui_format, output_ui, table_block

    if should_use_ui_format(args.format):
        rows = []
        for setting_name, value in config_data.items():
            source = _get_source(setting_name)
            rows.append([setting_name, str(value) if value else "(not set)", source])
        output_ui(table_block(
            "Configuration",
            ["Setting", "Value", "Source"],
            rows,
        ))
        return 0

    if args.format == "json":
        print(json.dumps(config_data, indent=2))
        return 0

    if args.format == "env":
        # Output as exportable environment variables
        print("# WarpData configuration (copy to ~/.bashrc or ~/.zshrc)")
        print(f"export WARPDATASETS_WORKSPACE_ROOT={settings.workspace_root}")
        if settings.manifest_base:
            print(f"export WARPDATASETS_MANIFEST_BASE={settings.manifest_base}")
        print(f"export WARPDATASETS_CACHE_DIR={settings.cache_dir}")
        print(f"export WARPDATASETS_MODE={settings.mode}")
        if settings.s3_region:
            print(f"export WARPDATASETS_S3_REGION={settings.s3_region}")
        if settings.s3_endpoint_url:
            print(f"export WARPDATASETS_S3_ENDPOINT_URL={settings.s3_endpoint_url}")
        return 0

    # Table format (default)
    print("WarpData Configuration")
    print("=" * 60)
    print()

    # Core settings
    print("Core Settings:")
    print(f"  workspace_root:  {settings.workspace_root}")
    print(f"                   (source: {_get_source('workspace_root')})")
    print(f"  cache_dir:       {settings.cache_dir}")
    print(f"                   (source: {_get_source('cache_dir')})")
    print(f"  mode:            {settings.mode}")
    print(f"                   (source: {_get_source('mode')})")
    print(f"  prefetch:        {settings.prefetch}")
    print(f"                   (source: {_get_source('prefetch')})")
    print()

    # Storage settings
    print("Storage Settings:")
    print(f"  manifest_base:   {settings.manifest_base or '(not set)'}")
    print(f"                   (source: {_get_source('manifest_base')})")
    print(f"  s3_region:       {settings.s3_region or '(not set)'}")
    print(f"                   (source: {_get_source('s3_region')})")
    print(f"  s3_endpoint_url: {settings.s3_endpoint_url or '(not set)'}")
    print(f"                   (source: {_get_source('s3_endpoint_url')})")
    print()

    # Check for deprecated env vars
    deprecated_vars = []
    if os.environ.get("WARPDATASETS_ROOT"):
        deprecated_vars.append(("WARPDATASETS_ROOT", "WARPDATASETS_WORKSPACE_ROOT"))

    if deprecated_vars:
        print("Deprecated Environment Variables:")
        for old, new in deprecated_vars:
            print(f"  {old} -> use {new} instead")
        print()

    # Show paths
    print("Paths:")
    print(f"  manifests:       {settings.workspace_root / 'manifests'}")
    print(f"  local data:      {settings.workspace_root / 'data'}")
    print(f"  cache:           {settings.cache_dir}")
    print()

    print("Run 'warpdata doctor' to verify connectivity and permissions.")

    return 0
