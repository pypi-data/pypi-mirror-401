"""Cloud storage backend configuration helpers.

Convenience functions for configuring warpdata with different cloud storage backends.
"""

import os
from typing import Optional

from .settings import configure, get_settings


# Backblaze B2 region to endpoint mapping
B2_ENDPOINTS = {
    "us-west-000": "https://s3.us-west-000.backblazeb2.com",
    "us-west-001": "https://s3.us-west-001.backblazeb2.com",
    "us-west-002": "https://s3.us-west-002.backblazeb2.com",
    "us-west-004": "https://s3.us-west-004.backblazeb2.com",
    "us-east-005": "https://s3.us-east-005.backblazeb2.com",
    "eu-central-003": "https://s3.eu-central-003.backblazeb2.com",
}


def use_backblaze(
    key_id: Optional[str] = None,
    app_key: Optional[str] = None,
    bucket: Optional[str] = None,
    region: str = "us-east-005",  # Default region for warpdata bucket
    prefix: str = "warpdatasets",
) -> None:
    """Configure warpdata to use Backblaze B2 storage.

    B2 is S3-compatible and ~4x cheaper than AWS S3 ($6/TB/month vs $23/TB/month).
    This sets up the S3-compatible endpoint and credentials.

    Args:
        key_id: B2 Application Key ID (or set B2_KEY_ID env var)
        app_key: B2 Application Key (or set B2_APP_KEY env var)
        bucket: B2 bucket name (or set B2_BUCKET env var)
        region: B2 region (default: us-east-005 where warpdata bucket is). Options:
                us-west-000, us-west-001, us-west-002, us-west-004, us-east-005, eu-central-003
        prefix: Prefix within bucket for datasets (default: warpdatasets)

    Example:
        >>> from warpdata.config import use_backblaze
        >>> use_backblaze(
        ...     key_id="your-key-id",
        ...     app_key="your-app-key",
        ...     bucket="my-datasets"
        ... )
        >>> # Now use warpdata normally
        >>> from warpdata import dataset
        >>> ds = dataset("my-workspace/my-dataset")

    Environment variables (alternative to passing args):
        B2_KEY_ID: Application Key ID
        B2_APP_KEY: Application Key
        B2_BUCKET: Bucket name
        B2_REGION: Region (default: us-west-004)
    """
    # Get credentials from args or env
    key_id = key_id or os.environ.get("B2_KEY_ID")
    app_key = app_key or os.environ.get("B2_APP_KEY")
    bucket = bucket or os.environ.get("B2_BUCKET")
    region = region or os.environ.get("B2_REGION", "us-east-005")

    if not key_id or not app_key:
        raise ValueError(
            "B2 credentials required. Either pass key_id/app_key or set "
            "B2_KEY_ID and B2_APP_KEY environment variables.\n\n"
            "To get credentials:\n"
            "1. Go to https://secure.backblaze.com/app_keys.htm\n"
            "2. Create a new Application Key\n"
            "3. Copy the keyID and applicationKey"
        )

    if not bucket:
        raise ValueError(
            "B2 bucket required. Either pass bucket or set B2_BUCKET env var.\n\n"
            "To create a bucket:\n"
            "1. Go to https://secure.backblaze.com/b2_buckets.htm\n"
            "2. Create a new bucket (private recommended)\n"
            "3. Copy the bucket name"
        )

    # Get endpoint URL for region
    if region not in B2_ENDPOINTS:
        raise ValueError(
            f"Unknown B2 region: {region}. "
            f"Valid regions: {', '.join(B2_ENDPOINTS.keys())}"
        )
    endpoint_url = B2_ENDPOINTS[region]

    # Set AWS credentials (B2 is S3-compatible)
    os.environ["AWS_ACCESS_KEY_ID"] = key_id
    os.environ["AWS_SECRET_ACCESS_KEY"] = app_key

    # Configure warpdata settings
    manifest_base = f"s3://{bucket}/{prefix}"

    configure(
        s3_endpoint_url=endpoint_url,
        manifest_base=manifest_base,
    )

    # Also set env vars for subprocesses and DuckDB
    os.environ["WARPDATASETS_S3_ENDPOINT_URL"] = endpoint_url
    os.environ["WARPDATASETS_MANIFEST_BASE"] = manifest_base

    print(f"Configured warpdata for Backblaze B2:")
    print(f"  Bucket: {bucket}")
    print(f"  Region: {region}")
    print(f"  Endpoint: {endpoint_url}")
    print(f"  Manifest base: {manifest_base}")


def use_s3(
    bucket: Optional[str] = None,
    region: str = "us-east-1",
    prefix: str = "warpdatasets",
    endpoint_url: Optional[str] = None,
) -> None:
    """Configure warpdata to use AWS S3 or S3-compatible storage.

    Args:
        bucket: S3 bucket name
        region: AWS region (default: us-east-1)
        prefix: Prefix within bucket for datasets (default: warpdatasets)
        endpoint_url: Custom endpoint URL (for MinIO, LocalStack, etc.)

    Credentials are read from standard AWS environment variables:
        AWS_ACCESS_KEY_ID
        AWS_SECRET_ACCESS_KEY
        AWS_SESSION_TOKEN (optional, for temporary credentials)
    """
    if not bucket:
        bucket = os.environ.get("WARPDATASETS_S3_BUCKET")
        if not bucket:
            raise ValueError(
                "S3 bucket required. Either pass bucket or set "
                "WARPDATASETS_S3_BUCKET environment variable."
            )

    manifest_base = f"s3://{bucket}/{prefix}"

    configure(
        s3_endpoint_url=endpoint_url,
        s3_region=region,
        manifest_base=manifest_base,
    )

    if endpoint_url:
        os.environ["WARPDATASETS_S3_ENDPOINT_URL"] = endpoint_url
    os.environ["WARPDATASETS_MANIFEST_BASE"] = manifest_base

    print(f"Configured warpdata for S3:")
    print(f"  Bucket: {bucket}")
    print(f"  Region: {region}")
    if endpoint_url:
        print(f"  Endpoint: {endpoint_url}")
    print(f"  Manifest base: {manifest_base}")
