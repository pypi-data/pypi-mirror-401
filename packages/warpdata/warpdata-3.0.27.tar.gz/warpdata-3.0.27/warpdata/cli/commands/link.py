"""Link CLI command - map artifacts to local paths."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def get_local_sources_path(settings) -> Path:
    """Get path to local sources mapping file."""
    return settings.workspace_root / "local_sources.json"


def load_local_sources(settings) -> dict:
    """Load local sources mapping."""
    path = get_local_sources_path(settings)
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


def save_local_sources(settings, sources: dict) -> None:
    """Save local sources mapping."""
    path = get_local_sources_path(settings)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(sources, f, indent=2)


def run(args: argparse.Namespace) -> int:
    """Run link command.

    Links dataset artifacts to local file paths, so warpdata
    can use local data instead of downloading from S3.

    Args:
        args: Parsed command line arguments

    Returns:
        Exit code (0 for success)
    """
    from warpdata.config.settings import get_settings

    settings = get_settings()
    dataset_id = args.dataset

    # Load current mappings
    sources = load_local_sources(settings)

    # Handle --show flag
    if args.show:
        if dataset_id:
            # Show links for specific dataset
            dataset_links = {k: v for k, v in sources.items() if k.startswith(f"{dataset_id}/")}
            if dataset_links:
                print(f"Local links for {dataset_id}:")
                for key, path in dataset_links.items():
                    artifact = key.split("/", 2)[-1] if "/" in key else key
                    exists = Path(path).exists()
                    status = "OK" if exists else "MISSING"
                    print(f"  {artifact}: {path} [{status}]")
            else:
                print(f"No local links for {dataset_id}")
        else:
            # Show all links
            if sources:
                print("All local links:")
                for key, path in sorted(sources.items()):
                    exists = Path(path).exists()
                    status = "OK" if exists else "MISSING"
                    print(f"  {key}: {path} [{status}]")
            else:
                print("No local links configured")
        return 0

    # Handle --clear flag
    if args.clear:
        if dataset_id:
            # Clear links for specific dataset
            keys_to_remove = [k for k in sources if k.startswith(f"{dataset_id}/")]
            for key in keys_to_remove:
                del sources[key]
            save_local_sources(settings, sources)
            print(f"Cleared {len(keys_to_remove)} local link(s) for {dataset_id}")
        else:
            # Clear all links
            count = len(sources)
            sources = {}
            save_local_sources(settings, sources)
            print(f"Cleared all {count} local link(s)")
        return 0

    # Handle linking artifacts
    if not dataset_id:
        print("Error: Dataset ID required", file=sys.stderr)
        print("Usage: warpdata link <dataset> --artifact <name>=<path>", file=sys.stderr)
        return 1

    if not args.artifact:
        print("Error: At least one --artifact is required", file=sys.stderr)
        print("Usage: warpdata link <dataset> --artifact <name>=<path>", file=sys.stderr)
        return 1

    # Parse and validate artifact paths
    for artifact_spec in args.artifact:
        if "=" not in artifact_spec:
            print(f"Error: Invalid artifact format: {artifact_spec}", file=sys.stderr)
            print("Expected: name=path/to/directory", file=sys.stderr)
            return 1

        name, dir_path = artifact_spec.split("=", 1)
        dir_path = Path(dir_path).expanduser().resolve()

        if not dir_path.exists():
            print(f"Warning: Path does not exist: {dir_path}", file=sys.stderr)
            if not args.force:
                print("Use --force to link anyway", file=sys.stderr)
                return 1

        # Store the mapping
        key = f"{dataset_id}/{name}"
        sources[key] = str(dir_path)
        print(f"Linked: {dataset_id}/{name} -> {dir_path}")

    save_local_sources(settings, sources)
    print(f"\nLocal links saved to: {get_local_sources_path(settings)}")

    return 0


def setup_parser(subparsers) -> None:
    """Set up the link subcommand parser."""
    parser = subparsers.add_parser(
        "link",
        help="Link dataset artifacts to local file paths",
        description="""
Link dataset artifacts to local file paths.

This allows warpdata to use local data instead of downloading from S3.
Useful when you have the raw data locally but the manifest points to S3.

Examples:
  # Link celeba images to local directory
  warpdata link vision/celeba --artifact image=~/data/img_align_celeba

  # Link multiple artifacts
  warpdata link vision/coco --artifact image=~/data/coco/images --artifact mask=~/data/coco/masks

  # Show current links
  warpdata link --show
  warpdata link vision/celeba --show

  # Clear links
  warpdata link vision/celeba --clear
  warpdata link --clear  # Clear all
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "dataset",
        nargs="?",
        help="Dataset ID (e.g., vision/celeba)",
    )
    parser.add_argument(
        "--artifact", "-a",
        action="append",
        help="Artifact link: name=path/to/directory",
    )
    parser.add_argument(
        "--show", "-s",
        action="store_true",
        help="Show current local links",
    )
    parser.add_argument(
        "--clear", "-c",
        action="store_true",
        help="Clear local links",
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Link even if path doesn't exist",
    )

    parser.set_defaults(func=run)
