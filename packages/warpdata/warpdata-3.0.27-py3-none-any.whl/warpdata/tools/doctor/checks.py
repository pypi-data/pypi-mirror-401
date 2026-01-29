"""Doctor checks for warpdata environment.

Each check returns a CheckResult with pass/fail status and details.
"""

from __future__ import annotations

import os
import tempfile
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING

from warpdata.config.settings import (
    DEFAULT_S3_BUCKET,
    DEFAULT_S3_REGION,
    DEFAULT_S3_ENDPOINT_URL,
    LEGACY_S3_BUCKET,
)

if TYPE_CHECKING:
    from warpdata.config.settings import Settings


class CheckStatus(Enum):
    """Status of a check."""

    PASS = "pass"
    FAIL = "fail"
    WARN = "warn"
    SKIP = "skip"


@dataclass
class CheckResult:
    """Result of a single check."""

    name: str
    status: CheckStatus
    message: str
    details: str | None = None
    suggestion: str | None = None


def check_settings(settings: Settings) -> CheckResult:
    """Check that settings are valid and parseable.

    Args:
        settings: Settings instance

    Returns:
        CheckResult
    """
    try:
        # Check mode is valid
        valid_modes = ("remote", "hybrid", "local", "auto")
        if settings.mode not in valid_modes:
            return CheckResult(
                name="settings",
                status=CheckStatus.FAIL,
                message=f"Invalid mode: {settings.mode}",
                suggestion=f"Set mode to one of: {', '.join(valid_modes)}",
            )

        # Check prefetch is valid
        valid_prefetch = ("off", "auto", "aggressive")
        if settings.prefetch not in valid_prefetch:
            return CheckResult(
                name="settings",
                status=CheckStatus.FAIL,
                message=f"Invalid prefetch: {settings.prefetch}",
                suggestion=f"Set prefetch to one of: {', '.join(valid_prefetch)}",
            )

        # Check workspace root
        if settings.workspace_root and not settings.workspace_root.exists():
            return CheckResult(
                name="settings",
                status=CheckStatus.WARN,
                message=f"Workspace root does not exist: {settings.workspace_root}",
                details="Will be created on first dataset registration",
            )

        # Check cache directory
        if settings.cache_dir:
            cache_path = Path(settings.cache_dir)
            if cache_path.exists() and not os.access(cache_path, os.W_OK):
                return CheckResult(
                    name="settings",
                    status=CheckStatus.FAIL,
                    message=f"Cache directory not writable: {settings.cache_dir}",
                    suggestion="Check permissions or set a different cache_dir",
                )

        return CheckResult(
            name="settings",
            status=CheckStatus.PASS,
            message="Settings are valid",
            details=f"mode={settings.mode}, prefetch={settings.prefetch}",
        )

    except Exception as e:
        return CheckResult(
            name="settings",
            status=CheckStatus.FAIL,
            message=f"Error parsing settings: {e}",
            suggestion="Check your .warpdata.toml or environment variables",
        )


def check_duckdb() -> CheckResult:
    """Check that DuckDB is available and functional.

    Returns:
        CheckResult
    """
    try:
        import duckdb

        version = duckdb.__version__

        # Test basic query
        conn = duckdb.connect(":memory:")
        result = conn.execute("SELECT 1").fetchone()
        if result != (1,):
            return CheckResult(
                name="duckdb",
                status=CheckStatus.FAIL,
                message="DuckDB query returned unexpected result",
            )

        # Test parquet reading capability
        with tempfile.NamedTemporaryFile(suffix=".parquet", delete=False) as f:
            temp_path = f.name

        try:
            # Create a minimal parquet file
            conn.execute(
                f"COPY (SELECT 1 as x) TO '{temp_path}' (FORMAT PARQUET)"
            )

            # Read it back
            result = conn.execute(f"SELECT * FROM '{temp_path}'").fetchone()
            if result != (1,):
                return CheckResult(
                    name="duckdb",
                    status=CheckStatus.FAIL,
                    message="DuckDB parquet read returned unexpected result",
                )
        finally:
            Path(temp_path).unlink(missing_ok=True)

        return CheckResult(
            name="duckdb",
            status=CheckStatus.PASS,
            message=f"DuckDB {version} is working",
            details="Parquet read/write verified",
        )

    except ImportError:
        return CheckResult(
            name="duckdb",
            status=CheckStatus.FAIL,
            message="DuckDB not installed",
            suggestion="pip install duckdb",
        )
    except Exception as e:
        return CheckResult(
            name="duckdb",
            status=CheckStatus.FAIL,
            message=f"DuckDB error: {e}",
            suggestion="Try reinstalling DuckDB: pip install --force-reinstall duckdb",
        )


def check_pyarrow() -> CheckResult:
    """Check that PyArrow is available and functional.

    Returns:
        CheckResult
    """
    try:
        import pyarrow as pa

        version = pa.__version__

        # Test basic table creation
        table = pa.table({"x": [1, 2, 3]})
        if len(table) != 3:
            return CheckResult(
                name="pyarrow",
                status=CheckStatus.FAIL,
                message="PyArrow table creation returned unexpected result",
            )

        return CheckResult(
            name="pyarrow",
            status=CheckStatus.PASS,
            message=f"PyArrow {version} is working",
        )

    except ImportError:
        return CheckResult(
            name="pyarrow",
            status=CheckStatus.FAIL,
            message="PyArrow not installed",
            suggestion="pip install pyarrow",
        )
    except Exception as e:
        return CheckResult(
            name="pyarrow",
            status=CheckStatus.FAIL,
            message=f"PyArrow error: {e}",
            suggestion="Try reinstalling PyArrow: pip install --force-reinstall pyarrow",
        )


def check_connectivity(settings: Settings) -> CheckResult:
    """Check connectivity to remote storage.

    Args:
        settings: Settings instance

    Returns:
        CheckResult
    """
    if not settings.manifest_base:
        return CheckResult(
            name="connectivity",
            status=CheckStatus.SKIP,
            message="No manifest_base configured",
            details="Local-only mode - remote connectivity not required",
        )

    manifest_base = settings.manifest_base

    # Check HTTP/HTTPS connectivity
    if manifest_base.startswith("http://") or manifest_base.startswith("https://"):
        try:
            import urllib.request
            import urllib.error

            # Just check if we can reach the host (HEAD request)
            req = urllib.request.Request(manifest_base, method="HEAD")
            req.add_header("User-Agent", "warpdata-doctor/1.0")

            try:
                with urllib.request.urlopen(req, timeout=5):
                    pass
                return CheckResult(
                    name="connectivity",
                    status=CheckStatus.PASS,
                    message=f"Can reach {manifest_base}",
                )
            except urllib.error.HTTPError as e:
                # 4xx/5xx is still "reachable"
                if e.code < 500:
                    return CheckResult(
                        name="connectivity",
                        status=CheckStatus.PASS,
                        message=f"Can reach {manifest_base}",
                        details=f"HTTP {e.code} (expected for base URI)",
                    )
                return CheckResult(
                    name="connectivity",
                    status=CheckStatus.WARN,
                    message=f"Server error from {manifest_base}",
                    details=f"HTTP {e.code}",
                )
        except Exception as e:
            return CheckResult(
                name="connectivity",
                status=CheckStatus.FAIL,
                message=f"Cannot reach {manifest_base}",
                details=str(e),
                suggestion="Check your network connection or manifest_base URL",
            )

    # Check S3 connectivity
    if manifest_base.startswith("s3://"):
        try:
            import boto3
            from botocore.exceptions import ClientError, NoCredentialsError

            # Parse bucket from URI
            parts = manifest_base[5:].split("/", 1)
            bucket = parts[0]
            endpoint = settings.s3_endpoint_url or ""

            # Detect common misconfigurations before making requests
            is_b2_endpoint = "backblazeb2.com" in endpoint
            is_aws_endpoint = "amazonaws.com" in endpoint or not endpoint
            is_legacy_bucket = bucket == LEGACY_S3_BUCKET
            is_default_bucket = bucket == DEFAULT_S3_BUCKET

            # B2 endpoint with old AWS bucket name
            if is_b2_endpoint and is_legacy_bucket:
                return CheckResult(
                    name="connectivity",
                    status=CheckStatus.FAIL,
                    message=f"Bucket/endpoint mismatch: '{bucket}' on B2",
                    details=(
                        f"You're using the B2 endpoint but the bucket '{LEGACY_S3_BUCKET}' "
                        f"was on AWS. The default bucket is now '{DEFAULT_S3_BUCKET}'."
                    ),
                    suggestion=(
                        f"Unset custom bucket configs to use defaults, or:\n"
                        f"  export B2_BUCKET={DEFAULT_S3_BUCKET}\n"
                        f"  export B2_REGION={DEFAULT_S3_REGION}\n"
                        f"Run 'warp doctor --repair' for interactive help."
                    ),
                )

            # AWS endpoint with B2 bucket name
            if is_aws_endpoint and is_default_bucket:
                return CheckResult(
                    name="connectivity",
                    status=CheckStatus.FAIL,
                    message=f"Bucket/endpoint mismatch: '{bucket}' is on B2, not AWS",
                    details=(
                        f"The bucket '{DEFAULT_S3_BUCKET}' is on Backblaze B2, "
                        f"but you're using an AWS endpoint."
                    ),
                    suggestion=(
                        f"Use B2 endpoint (recommended):\n"
                        f"  export B2_REGION={DEFAULT_S3_REGION}\n"
                        f"Or unset all storage env vars to use defaults."
                    ),
                )

            # Create S3 client with custom endpoint support
            s3_kwargs = {}
            if settings.s3_endpoint_url:
                s3_kwargs["endpoint_url"] = settings.s3_endpoint_url
            if settings.s3_region:
                s3_kwargs["region_name"] = settings.s3_region
            s3 = boto3.client("s3", **s3_kwargs)
            try:
                s3.head_bucket(Bucket=bucket)
                # Show endpoint info for clarity
                endpoint_info = f" (via {endpoint})" if is_b2_endpoint else ""
                return CheckResult(
                    name="connectivity",
                    status=CheckStatus.PASS,
                    message=f"Can access S3 bucket: {bucket}{endpoint_info}",
                )
            except NoCredentialsError:
                if is_b2_endpoint:
                    suggestion = (
                        "B2 credentials required. Set:\n"
                        "  export AWS_ACCESS_KEY_ID=<your-b2-key-id>\n"
                        "  export AWS_SECRET_ACCESS_KEY=<your-b2-application-key>"
                    )
                else:
                    suggestion = "Configure AWS credentials (aws configure or environment variables)"
                return CheckResult(
                    name="connectivity",
                    status=CheckStatus.FAIL,
                    message="No credentials found",
                    suggestion=suggestion,
                )
            except ClientError as e:
                error_code = e.response.get("Error", {}).get("Code", "Unknown")
                error_msg = e.response.get("Error", {}).get("Message", str(e))

                if error_code == "403":
                    if is_b2_endpoint:
                        suggestion = (
                            "B2 access denied. Check that:\n"
                            "  1. Your B2 application key has access to this bucket\n"
                            "  2. AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set correctly"
                        )
                    else:
                        suggestion = "Check your AWS permissions for this bucket"
                    return CheckResult(
                        name="connectivity",
                        status=CheckStatus.FAIL,
                        message=f"Access denied to bucket: {bucket}",
                        details=error_msg,
                        suggestion=suggestion,
                    )
                elif error_code == "404":
                    if is_b2_endpoint and is_legacy_bucket:
                        # This case is already handled above, but just in case
                        suggestion = f"Use B2_BUCKET={DEFAULT_S3_BUCKET} instead"
                    elif is_b2_endpoint:
                        suggestion = (
                            f"Bucket '{bucket}' not found on B2.\n"
                            f"Default bucket is '{DEFAULT_S3_BUCKET}'.\n"
                            f"Check B2_BUCKET environment variable."
                        )
                    else:
                        suggestion = "Check the manifest_base URL"
                    return CheckResult(
                        name="connectivity",
                        status=CheckStatus.FAIL,
                        message=f"Bucket not found: {bucket}",
                        suggestion=suggestion,
                    )
                return CheckResult(
                    name="connectivity",
                    status=CheckStatus.FAIL,
                    message=f"S3 error: {error_code}",
                    details=error_msg,
                )
        except ImportError:
            return CheckResult(
                name="connectivity",
                status=CheckStatus.WARN,
                message="boto3 not installed (required for S3)",
                suggestion="pip install boto3",
            )
        except Exception as e:
            return CheckResult(
                name="connectivity",
                status=CheckStatus.FAIL,
                message=f"S3 connectivity error: {e}",
            )

    # Check GCS connectivity
    if manifest_base.startswith("gs://"):
        try:
            from google.cloud import storage
            from google.auth.exceptions import DefaultCredentialsError

            # Parse bucket from URI
            parts = manifest_base[5:].split("/", 1)
            bucket = parts[0]

            try:
                client = storage.Client()
                bucket_obj = client.bucket(bucket)
                bucket_obj.exists()
                return CheckResult(
                    name="connectivity",
                    status=CheckStatus.PASS,
                    message=f"Can access GCS bucket: {bucket}",
                )
            except DefaultCredentialsError:
                return CheckResult(
                    name="connectivity",
                    status=CheckStatus.FAIL,
                    message="No GCP credentials found",
                    suggestion="Set GOOGLE_APPLICATION_CREDENTIALS or run 'gcloud auth application-default login'",
                )
        except ImportError:
            return CheckResult(
                name="connectivity",
                status=CheckStatus.WARN,
                message="google-cloud-storage not installed (required for GCS)",
                suggestion="pip install google-cloud-storage",
            )
        except Exception as e:
            return CheckResult(
                name="connectivity",
                status=CheckStatus.FAIL,
                message=f"GCS connectivity error: {e}",
            )

    return CheckResult(
        name="connectivity",
        status=CheckStatus.SKIP,
        message=f"Unknown URI scheme: {manifest_base}",
    )


def check_storage_config(settings: Settings) -> CheckResult:
    """Check storage configuration and detect mismatches.

    Args:
        settings: Settings instance

    Returns:
        CheckResult with storage configuration details
    """
    manifest_base = settings.manifest_base or ""
    endpoint = settings.s3_endpoint_url or ""
    region = settings.s3_region or ""

    # Parse bucket from manifest_base
    bucket = ""
    if manifest_base.startswith("s3://"):
        parts = manifest_base[5:].split("/", 1)
        bucket = parts[0]

    # Detect backend type
    is_b2 = "backblazeb2.com" in endpoint
    is_aws = "amazonaws.com" in endpoint or (not endpoint and bucket)
    is_default_config = (
        bucket == DEFAULT_S3_BUCKET
        and region == DEFAULT_S3_REGION
        and endpoint == DEFAULT_S3_ENDPOINT_URL
    )

    # Build details string
    details_parts = []
    if bucket:
        details_parts.append(f"bucket={bucket}")
    if region:
        details_parts.append(f"region={region}")
    if endpoint:
        if is_b2:
            details_parts.append("endpoint=B2")
        elif is_aws:
            details_parts.append("endpoint=AWS")
        else:
            details_parts.append(f"endpoint={endpoint[:30]}...")

    details = ", ".join(details_parts) if details_parts else "no remote storage"

    # Check for misconfigurations
    is_legacy_bucket = bucket == LEGACY_S3_BUCKET

    if is_b2 and is_legacy_bucket:
        return CheckResult(
            name="storage_config",
            status=CheckStatus.FAIL,
            message="Storage misconfiguration detected",
            details=f"B2 endpoint with legacy AWS bucket '{LEGACY_S3_BUCKET}'",
            suggestion=(
                f"The bucket '{LEGACY_S3_BUCKET}' was on AWS, not B2.\n"
                f"Default is now '{DEFAULT_S3_BUCKET}' on B2.\n"
                f"Unset custom configs or run 'warp doctor --repair'."
            ),
        )

    if is_aws and bucket == DEFAULT_S3_BUCKET:
        return CheckResult(
            name="storage_config",
            status=CheckStatus.FAIL,
            message="Storage misconfiguration detected",
            details=f"AWS endpoint with B2 bucket '{DEFAULT_S3_BUCKET}'",
            suggestion=(
                f"The bucket '{DEFAULT_S3_BUCKET}' is on B2, not AWS.\n"
                f"Set B2_REGION={DEFAULT_S3_REGION} or unset all storage vars."
            ),
        )

    if is_default_config:
        return CheckResult(
            name="storage_config",
            status=CheckStatus.PASS,
            message="Using default B2 storage",
            details=details,
        )

    if is_b2:
        return CheckResult(
            name="storage_config",
            status=CheckStatus.PASS,
            message="Using B2 storage",
            details=details,
        )

    if is_aws:
        return CheckResult(
            name="storage_config",
            status=CheckStatus.PASS,
            message="Using AWS S3 storage",
            details=details,
        )

    if not manifest_base:
        return CheckResult(
            name="storage_config",
            status=CheckStatus.WARN,
            message="No remote storage configured",
            details="Local-only mode",
            suggestion="This is fine for local datasets only.",
        )

    return CheckResult(
        name="storage_config",
        status=CheckStatus.PASS,
        message="Custom storage configuration",
        details=details,
    )


def check_credentials() -> CheckResult:
    """Check cloud credentials availability.

    Returns:
        CheckResult
    """
    issues = []
    found = []

    # Check AWS credentials
    aws_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_profile = os.environ.get("AWS_PROFILE")
    aws_creds_file = Path.home() / ".aws" / "credentials"

    if aws_key:
        found.append("AWS (env)")
    elif aws_profile:
        found.append(f"AWS ({aws_profile})")
    elif aws_creds_file.exists():
        found.append("AWS (~/.aws)")

    # Check GCP credentials
    gcp_creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    gcp_adc = Path.home() / ".config" / "gcloud" / "application_default_credentials.json"

    if gcp_creds:
        found.append("GCP (env)")
    elif gcp_adc.exists():
        found.append("GCP (ADC)")

    # Check Azure credentials (basic check)
    azure_tenant = os.environ.get("AZURE_TENANT_ID")
    if azure_tenant:
        found.append("Azure (env)")

    if found:
        return CheckResult(
            name="credentials",
            status=CheckStatus.PASS,
            message=f"Found credentials: {', '.join(found)}",
        )
    else:
        return CheckResult(
            name="credentials",
            status=CheckStatus.WARN,
            message="No cloud credentials detected",
            details="This is fine for local-only usage",
            suggestion="For remote datasets, configure AWS/GCP/Azure credentials",
        )


def check_dataset_access(dataset_id: str, settings: Settings) -> CheckResult:
    """Check that a specific dataset is accessible.

    Args:
        dataset_id: Dataset ID to check
        settings: Settings instance

    Returns:
        CheckResult
    """
    try:
        import warpdata as wd

        # Load dataset
        ds = wd.dataset(dataset_id)

        # Try to get info
        info = ds.info()
        version = info.get("version", "unknown")[:12]

        # Try to read schema
        table = ds.table("main")
        schema = table.schema()

        return CheckResult(
            name=f"dataset:{dataset_id}",
            status=CheckStatus.PASS,
            message=f"Dataset accessible (version: {version})",
            details=f"{len(schema)} columns in main table",
        )

    except Exception as e:
        error_str = str(e).lower()

        if "not found" in error_str:
            suggestion = "Check the dataset ID or register it with 'warpdata register'"
        elif "permission" in error_str or "access" in error_str:
            suggestion = "Check your credentials and permissions"
        elif "connection" in error_str or "network" in error_str:
            suggestion = "Check your network connection"
        else:
            suggestion = None

        return CheckResult(
            name=f"dataset:{dataset_id}",
            status=CheckStatus.FAIL,
            message=f"Cannot access dataset: {e}",
            suggestion=suggestion,
        )


def check_streaming_performance(dataset_id: str, settings: Settings) -> CheckResult:
    """Check streaming performance for a dataset.

    Args:
        dataset_id: Dataset ID to test
        settings: Settings instance

    Returns:
        CheckResult
    """
    try:
        import warpdata as wd

        ds = wd.dataset(dataset_id)
        table = ds.table("main")

        # Stream a limited number of rows and measure
        start = time.time()
        row_count = 0
        batch_count = 0

        for batch in table.batches(batch_size=10000, limit=50000):
            row_count += batch.num_rows
            batch_count += 1
            if time.time() - start > 5:  # Max 5 seconds
                break

        elapsed = time.time() - start

        if elapsed == 0:
            return CheckResult(
                name="performance",
                status=CheckStatus.SKIP,
                message="Could not measure performance (too fast)",
            )

        rows_per_sec = row_count / elapsed

        if rows_per_sec > 100000:
            status = CheckStatus.PASS
            message = f"Excellent: {rows_per_sec:,.0f} rows/sec"
        elif rows_per_sec > 10000:
            status = CheckStatus.PASS
            message = f"Good: {rows_per_sec:,.0f} rows/sec"
        elif rows_per_sec > 1000:
            status = CheckStatus.WARN
            message = f"Slow: {rows_per_sec:,.0f} rows/sec"
            suggestion = "Consider warming the cache with 'warpdata warm'"
        else:
            status = CheckStatus.WARN
            message = f"Very slow: {rows_per_sec:,.0f} rows/sec"
            suggestion = "Network may be slow, consider downloading locally"

        return CheckResult(
            name="performance",
            status=status,
            message=message,
            details=f"{row_count:,} rows in {batch_count} batches ({elapsed:.2f}s)",
        )

    except Exception as e:
        return CheckResult(
            name="performance",
            status=CheckStatus.FAIL,
            message=f"Performance test failed: {e}",
        )


def run_all_checks(
    settings: Settings,
    dataset_id: str | None = None,
    include_performance: bool = False,
) -> list[CheckResult]:
    """Run all doctor checks.

    Args:
        settings: Settings instance
        dataset_id: Optional dataset to test
        include_performance: Whether to run performance check

    Returns:
        List of CheckResults
    """
    results = []

    # Core checks
    results.append(check_settings(settings))
    results.append(check_duckdb())
    results.append(check_pyarrow())
    results.append(check_storage_config(settings))  # Check config before connectivity
    results.append(check_connectivity(settings))
    results.append(check_credentials())

    # Dataset-specific checks
    if dataset_id:
        results.append(check_dataset_access(dataset_id, settings))

        if include_performance:
            results.append(check_streaming_performance(dataset_id, settings))

    return results
