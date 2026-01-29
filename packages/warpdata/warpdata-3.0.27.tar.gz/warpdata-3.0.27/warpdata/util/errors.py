"""Typed exceptions with user-facing messages.

All exceptions include:
- A short message describing the problem
- Remediation hints for how to fix it
"""

from __future__ import annotations


class WarpDatasetsError(Exception):
    """Base exception for all warpdata errors."""

    def __init__(self, message: str, remediation: str | None = None):
        self.message = message
        self.remediation = remediation
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        if self.remediation:
            return f"{self.message}\n\nHow to fix: {self.remediation}"
        return self.message


class DatasetNotFoundError(WarpDatasetsError):
    """Dataset does not exist or is not accessible."""

    def __init__(self, dataset_id: str, details: str | None = None):
        message = f"Dataset '{dataset_id}' not found."
        if details:
            message = f"{message} {details}"
        super().__init__(
            message=message,
            remediation=(
                "Check that the dataset ID is correct (format: workspace/name). "
                "Verify the dataset has been published and you have access permissions."
            ),
        )
        self.dataset_id = dataset_id


class ManifestNotFoundError(WarpDatasetsError):
    """Manifest version does not exist."""

    def __init__(self, dataset_id: str, version: str):
        super().__init__(
            message=f"Manifest version '{version}' not found for dataset '{dataset_id}'.",
            remediation=(
                "Check that the version hash is correct. "
                "Use version='latest' or omit version to get the latest published version."
            ),
        )
        self.dataset_id = dataset_id
        self.version = version


class ManifestInvalidError(WarpDatasetsError):
    """Manifest content is invalid or corrupted."""

    def __init__(self, dataset_id: str, details: str):
        super().__init__(
            message=f"Invalid manifest for dataset '{dataset_id}': {details}",
            remediation=(
                "The manifest may be corrupted. Try clearing the cache with "
                "'warpdata cache gc' and retry. If the problem persists, "
                "contact the dataset publisher."
            ),
        )
        self.dataset_id = dataset_id


class EngineNotReadyError(WarpDatasetsError):
    """DuckDB engine is not properly configured."""

    def __init__(self, details: str):
        super().__init__(
            message=f"Query engine not ready: {details}",
            remediation=(
                "Ensure DuckDB is installed with remote access extensions. "
                "For S3 access, configure AWS credentials via environment variables "
                "(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) or AWS profile. "
                "Run 'warpdata doctor' to diagnose configuration issues."
            ),
        )


class LargeDataError(WarpDatasetsError):
    """Operation would load too much data into memory."""

    def __init__(self, row_count: int | None, threshold: int):
        if row_count is not None:
            message = (
                f"Dataset has {row_count:,} rows, which exceeds the safety threshold "
                f"of {threshold:,} rows for loading into memory."
            )
        else:
            message = (
                f"Dataset size is unknown but appears large. "
                f"Safety threshold is {threshold:,} rows."
            )
        super().__init__(
            message=message,
            remediation=(
                "Options:\n"
                "  1. Use .to_pandas(limit=N) to load only N rows\n"
                "  2. Use .to_pandas(allow_large=True) to bypass this check\n"
                "  3. Use .duckdb() for lazy evaluation and streaming\n"
                "  4. Use .batches() for memory-efficient iteration"
            ),
        )
        self.row_count = row_count
        self.threshold = threshold


class AuthenticationError(WarpDatasetsError):
    """Authentication/credentials issue."""

    def __init__(self, details: str):
        super().__init__(
            message=f"Authentication failed: {details}",
            remediation=(
                "For AWS/S3:\n"
                "  - Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env vars, or\n"
                "  - Set AWS_PROFILE to use a named profile, or\n"
                "  - Configure credentials in ~/.aws/credentials\n"
                "Run 'warpdata doctor' to verify your configuration."
            ),
        )


class PermissionError(WarpDatasetsError):
    """Permission denied accessing a resource."""

    def __init__(self, resource: str, details: str | None = None):
        message = f"Permission denied accessing '{resource}'."
        if details:
            message = f"{message} {details}"
        super().__init__(
            message=message,
            remediation=(
                "Check that your credentials have the required permissions. "
                "For S3, ensure your IAM role/user has s3:GetObject permission "
                "on the bucket and prefix. Contact the dataset owner if you "
                "need access granted."
            ),
        )
        self.resource = resource


class RefNotFoundError(WarpDatasetsError):
    """Reference to raw data member not found in artifact shards."""

    def __init__(self, ref_value: str, artifact_name: str, shards_searched: int = 0):
        message = f"Reference '{ref_value}' not found in artifact '{artifact_name}'."
        if shards_searched > 0:
            message = f"{message} Searched {shards_searched} shard(s)."
        super().__init__(
            message=message,
            remediation=(
                "Verify that the reference value in your data matches a member "
                "in the artifact tar shards. The binding may be incorrect, or "
                "the raw data archive may be incomplete."
            ),
        )
        self.ref_value = ref_value
        self.artifact_name = artifact_name
        self.shards_searched = shards_searched


class ShardNotFoundError(WarpDatasetsError):
    """Shard referenced in manifest is not accessible (404 or missing)."""

    def __init__(self, uri: str, dataset_id: str | None = None):
        message = f"Shard not found: {uri}"
        if dataset_id:
            message = f"Shard not found for dataset '{dataset_id}': {uri}"

        remediation_parts = [
            "The manifest references a shard that doesn't exist at the expected location.",
            "",
            "Possible causes:",
            "  1. Dataset was not fully published (shards missing from storage)",
            "  2. Manifest was migrated but data was not copied to new location",
            "  3. Storage bucket/prefix configuration doesn't match manifest",
            "",
            "To diagnose:",
            "  warpdata doctor <dataset>  # Check dataset accessibility",
            "",
            "To fix:",
            "  1. Try 'warpdata sync pull' to get latest manifests",
            "  2. Re-publish the dataset with 'warpdata publish --verify'",
            "  3. Check storage configuration with 'warpdata config'",
        ]
        super().__init__(
            message=message,
            remediation="\n".join(remediation_parts),
        )
        self.uri = uri
        self.dataset_id = dataset_id


class DatasetIntegrityError(WarpDatasetsError):
    """Dataset has integrity issues (missing shards, corrupted data)."""

    def __init__(self, dataset_id: str, missing_count: int, total_count: int):
        message = (
            f"Dataset '{dataset_id}' has integrity issues: "
            f"{missing_count} of {total_count} shards are inaccessible."
        )
        super().__init__(
            message=message,
            remediation=(
                "The dataset manifest references shards that cannot be accessed.\n"
                "This may indicate the dataset was partially published or data was deleted.\n\n"
                "Options:\n"
                "  1. Run 'warpdata sync pull' to get the latest manifest\n"
                "  2. Contact the dataset publisher to verify data availability\n"
                "  3. Re-publish with 'warpdata publish --verify' to ensure all shards exist"
            ),
        )
        self.dataset_id = dataset_id
        self.missing_count = missing_count
        self.total_count = total_count


class StaleManifestError(WarpDatasetsError):
    """Manifest is stale - referenced shards no longer exist.

    This error is raised when a shard returns 404, indicating the cached
    manifest is outdated and a newer version may be available.
    """

    def __init__(self, dataset_id: str, shard_uri: str):
        super().__init__(
            message=(
                f"Stale manifest for '{dataset_id}': shard not found at {shard_uri}. "
                "A newer version may be available."
            ),
            remediation=(
                "The cached manifest references shards that no longer exist.\n"
                "This usually means a newer version has been published.\n\n"
                "Run: warpdata sync pull\n"
                "Or reload the dataset to auto-refresh."
            ),
        )
        self.dataset_id = dataset_id
        self.shard_uri = shard_uri


class StorageMisconfigurationError(WarpDatasetsError):
    """Storage backend is misconfigured (wrong endpoint, bucket, or credentials)."""

    def __init__(self, endpoint: str | None, bucket: str | None, details: str):
        remediation = self._build_remediation(endpoint, bucket)
        super().__init__(
            message=f"Storage misconfiguration: {details}",
            remediation=remediation,
        )
        self.endpoint = endpoint
        self.bucket = bucket

    def _build_remediation(self, endpoint: str | None, bucket: str | None) -> str:
        """Build context-aware remediation hints."""
        endpoint = endpoint or ""
        bucket = bucket or ""

        # B2 endpoint with old AWS bucket name
        if "backblazeb2.com" in endpoint and "warpbucket-warp" in bucket:
            return (
                "You're using a B2 endpoint with the old AWS bucket name 'warpbucket-warp'.\n"
                "The default bucket is now 'warpdata' on B2.\n\n"
                "Quick fix:\n"
                "  Unset any custom bucket configuration - warpdata uses B2 by default.\n\n"
                "Or set B2_BUCKET explicitly:\n"
                "  export B2_BUCKET=warpdata\n"
                "  export B2_REGION=us-east-005\n\n"
                "Run 'warp doctor --repair' for interactive help."
            )

        # AWS endpoint with B2 bucket name
        if "amazonaws.com" in endpoint and bucket == "warpdata":
            return (
                "You're using an AWS endpoint but the bucket 'warpdata' is on Backblaze B2.\n\n"
                "Quick fix (use B2 - recommended):\n"
                "  export B2_REGION=us-east-005\n"
                "  # or unset all storage env vars to use defaults\n\n"
                "Run 'warp doctor --repair' for interactive help."
            )

        # B2 endpoint but bucket not found (likely credentials issue)
        if "backblazeb2.com" in endpoint:
            return (
                "Cannot access bucket on B2. Possible causes:\n"
                "  1. Bucket name is incorrect\n"
                "  2. B2 credentials are missing or invalid\n"
                "  3. Application key doesn't have access to this bucket\n\n"
                "For B2 authentication, set:\n"
                "  export AWS_ACCESS_KEY_ID=<your-b2-key-id>\n"
                "  export AWS_SECRET_ACCESS_KEY=<your-b2-application-key>\n\n"
                "Run 'warp doctor' to diagnose the issue."
            )

        # Generic fallback
        return (
            "Storage configuration issue. Check:\n"
            "  1. Endpoint URL matches your storage provider\n"
            "  2. Bucket name is correct\n"
            "  3. Credentials are valid for this endpoint\n\n"
            "For B2 (default):\n"
            "  export B2_REGION=us-east-005\n"
            "  export AWS_ACCESS_KEY_ID=<b2-key-id>\n"
            "  export AWS_SECRET_ACCESS_KEY=<b2-app-key>\n\n"
            "Run 'warp doctor' to diagnose configuration issues."
        )
