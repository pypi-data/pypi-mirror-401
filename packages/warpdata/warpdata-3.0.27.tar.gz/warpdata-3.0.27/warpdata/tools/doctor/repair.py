"""Interactive repair mode for common warpdata configuration issues.

Provides guided fixes for storage misconfigurations detected by doctor checks.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from warpdata.config.settings import (
    DEFAULT_S3_BUCKET,
    DEFAULT_S3_REGION,
    DEFAULT_S3_ENDPOINT_URL,
    LEGACY_S3_BUCKET,
)
from warpdata.tools.doctor.checks import (
    CheckResult,
    CheckStatus,
    check_storage_config,
    check_connectivity,
    check_credentials,
)

if TYPE_CHECKING:
    from warpdata.config.settings import Settings


def _prompt_yes_no(question: str, default: bool = False) -> bool:
    """Prompt user for yes/no answer.

    Args:
        question: The question to ask
        default: Default answer if user just presses Enter

    Returns:
        True for yes, False for no
    """
    suffix = " [Y/n]: " if default else " [y/N]: "
    try:
        answer = input(question + suffix).strip().lower()
        if not answer:
            return default
        return answer in ("y", "yes")
    except (EOFError, KeyboardInterrupt):
        print()
        return False


def _detect_shell_config() -> Path | None:
    """Detect the user's shell configuration file.

    Returns:
        Path to shell config file, or None if not found
    """
    shell = os.environ.get("SHELL", "")
    home = Path.home()

    # Check common shell configs in order of preference
    candidates = []
    if "zsh" in shell:
        candidates = [home / ".zshrc", home / ".zprofile"]
    elif "bash" in shell:
        candidates = [home / ".bashrc", home / ".bash_profile", home / ".profile"]
    else:
        # Fallback for other shells
        candidates = [
            home / ".zshrc",
            home / ".bashrc",
            home / ".profile",
        ]

    for path in candidates:
        if path.exists():
            return path

    return None


def _append_to_shell_config(lines: list[str], config_path: Path) -> bool:
    """Append configuration lines to shell config file.

    Args:
        lines: Lines to append
        config_path: Path to shell config file

    Returns:
        True if successful
    """
    try:
        with open(config_path, "a") as f:
            f.write("\n")
            for line in lines:
                f.write(line + "\n")
        return True
    except Exception as e:
        print(f"Error writing to {config_path}: {e}", file=sys.stderr)
        return False


def _suggest_b2_bucket_fix(settings: Settings) -> bool:
    """Suggest and optionally apply fix for B2 bucket mismatch.

    Args:
        settings: Current settings

    Returns:
        True if fix was applied or user declined
    """
    print("\n" + "=" * 60)
    print("ISSUE: Bucket/endpoint mismatch")
    print("=" * 60)

    manifest_base = settings.manifest_base or ""
    bucket = ""
    if manifest_base.startswith("s3://"):
        bucket = manifest_base[5:].split("/", 1)[0]

    print(f"\nCurrent configuration:")
    print(f"  Bucket: {bucket}")
    print(f"  Endpoint: {settings.s3_endpoint_url or '(default AWS)'}")

    if bucket == LEGACY_S3_BUCKET:
        print(f"\nProblem: '{LEGACY_S3_BUCKET}' was the old AWS bucket.")
        print(f"         The new default bucket is '{DEFAULT_S3_BUCKET}' on B2.")
    else:
        print(f"\nProblem: Bucket '{bucket}' doesn't match the endpoint.")

    print(f"\nRecommended fix:")
    print(f"  Use the default B2 configuration (no env vars needed)")
    print(f"  Or set:")
    print(f"    export B2_BUCKET={DEFAULT_S3_BUCKET}")
    print(f"    export B2_REGION={DEFAULT_S3_REGION}")

    # Check for conflicting env vars
    conflicting_vars = []
    if os.environ.get("WARPDATASETS_MANIFEST_BASE"):
        conflicting_vars.append("WARPDATASETS_MANIFEST_BASE")
    if os.environ.get("B2_BUCKET"):
        conflicting_vars.append("B2_BUCKET")

    if conflicting_vars:
        print(f"\nDetected environment variables that may need to be updated:")
        for var in conflicting_vars:
            print(f"  {var}={os.environ.get(var)}")

    # Offer to add to shell config
    shell_config = _detect_shell_config()
    if shell_config:
        print(f"\nI can add the B2 configuration to {shell_config}")
        if _prompt_yes_no("Add B2 configuration?"):
            lines = [
                "",
                "# Warpdata B2 storage configuration",
                f"export B2_BUCKET={DEFAULT_S3_BUCKET}",
                f"export B2_REGION={DEFAULT_S3_REGION}",
            ]
            if _append_to_shell_config(lines, shell_config):
                print(f"\nAdded to {shell_config}")
                print(f"Run: source {shell_config}")
                print("Then run 'warp doctor' again to verify.")
                return True
            else:
                print("Failed to update shell config.")
                return False

    # Manual instructions
    print("\nTo fix manually, add these to your shell config:")
    print(f"  export B2_BUCKET={DEFAULT_S3_BUCKET}")
    print(f"  export B2_REGION={DEFAULT_S3_REGION}")

    return True


def _suggest_credentials_fix(settings: Settings) -> bool:
    """Suggest and optionally apply fix for missing credentials.

    Args:
        settings: Current settings

    Returns:
        True if fix was applied or user understood
    """
    print("\n" + "=" * 60)
    print("ISSUE: Missing or invalid credentials")
    print("=" * 60)

    endpoint = settings.s3_endpoint_url or ""
    is_b2 = "backblazeb2.com" in endpoint

    if is_b2:
        print("\nB2 requires credentials to access buckets.")
        print("\nTo set up B2 credentials:")
        print("  1. Log in to Backblaze B2: https://secure.backblaze.com/b2_buckets.htm")
        print("  2. Go to 'App Keys' and create a new application key")
        print("  3. Set environment variables:")
        print("     export AWS_ACCESS_KEY_ID=<your-key-id>")
        print("     export AWS_SECRET_ACCESS_KEY=<your-application-key>")
    else:
        print("\nAWS credentials not found.")
        print("\nTo set up AWS credentials:")
        print("  Option 1: aws configure")
        print("  Option 2: Set environment variables:")
        print("     export AWS_ACCESS_KEY_ID=<your-key>")
        print("     export AWS_SECRET_ACCESS_KEY=<your-secret>")

    shell_config = _detect_shell_config()
    if shell_config:
        print(f"\nYou can add these exports to {shell_config}")

    return True


def _suggest_endpoint_fix(settings: Settings) -> bool:
    """Suggest fix for endpoint configuration.

    Args:
        settings: Current settings

    Returns:
        True if user understood
    """
    print("\n" + "=" * 60)
    print("ISSUE: Endpoint configuration")
    print("=" * 60)

    manifest_base = settings.manifest_base or ""
    bucket = ""
    if manifest_base.startswith("s3://"):
        bucket = manifest_base[5:].split("/", 1)[0]

    print(f"\nCurrent configuration:")
    print(f"  Bucket: {bucket}")
    print(f"  Endpoint: {settings.s3_endpoint_url or '(none - using AWS default)'}")
    print(f"  Region: {settings.s3_region or '(none)'}")

    if bucket == DEFAULT_S3_BUCKET and not settings.s3_endpoint_url:
        print(f"\nProblem: Bucket '{DEFAULT_S3_BUCKET}' is on B2, not AWS.")
        print(f"\nFix: Set B2_REGION to auto-configure the endpoint:")
        print(f"  export B2_REGION={DEFAULT_S3_REGION}")

        shell_config = _detect_shell_config()
        if shell_config:
            if _prompt_yes_no(f"Add B2_REGION to {shell_config}?"):
                lines = [
                    "",
                    "# Warpdata B2 region (auto-configures endpoint)",
                    f"export B2_REGION={DEFAULT_S3_REGION}",
                ]
                if _append_to_shell_config(lines, shell_config):
                    print(f"\nAdded to {shell_config}")
                    print(f"Run: source {shell_config}")
                    return True

    return True


def run_repair_mode(settings: Settings) -> int:
    """Run interactive repair mode.

    Checks for common issues and offers to fix them.

    Args:
        settings: Current settings

    Returns:
        Exit code (0 for success, 1 for issues found, 2 for errors)
    """
    print("Warpdata Doctor - Repair Mode")
    print("=" * 60)
    print()

    issues_found = 0
    fixes_applied = 0

    # Check storage configuration
    print("Checking storage configuration...")
    storage_result = check_storage_config(settings)

    if storage_result.status == CheckStatus.FAIL:
        issues_found += 1
        if "bucket" in storage_result.message.lower():
            if _suggest_b2_bucket_fix(settings):
                fixes_applied += 1
        elif "endpoint" in storage_result.message.lower():
            if _suggest_endpoint_fix(settings):
                fixes_applied += 1
        else:
            print(f"\n{storage_result.message}")
            if storage_result.details:
                print(f"Details: {storage_result.details}")
            if storage_result.suggestion:
                print(f"Suggestion: {storage_result.suggestion}")
    else:
        print(f"  [OK] {storage_result.message}")

    # Check connectivity
    print("\nChecking connectivity...")
    conn_result = check_connectivity(settings)

    if conn_result.status == CheckStatus.FAIL:
        issues_found += 1
        error_msg = conn_result.message.lower()

        if "credentials" in error_msg or "no credentials" in error_msg:
            if _suggest_credentials_fix(settings):
                fixes_applied += 1
        elif "bucket not found" in error_msg or "mismatch" in error_msg:
            # Already handled by storage config check
            print(f"  [FAIL] {conn_result.message}")
            if conn_result.suggestion:
                print(f"         {conn_result.suggestion}")
        else:
            print(f"\n  [FAIL] {conn_result.message}")
            if conn_result.details:
                print(f"  Details: {conn_result.details}")
            if conn_result.suggestion:
                print(f"  Suggestion: {conn_result.suggestion}")
    elif conn_result.status == CheckStatus.SKIP:
        print(f"  [SKIP] {conn_result.message}")
    else:
        print(f"  [OK] {conn_result.message}")

    # Check credentials
    print("\nChecking credentials...")
    creds_result = check_credentials()

    if creds_result.status == CheckStatus.WARN:
        # Not a critical issue, just warn
        print(f"  [WARN] {creds_result.message}")
        if creds_result.suggestion:
            print(f"         {creds_result.suggestion}")
    elif creds_result.status == CheckStatus.FAIL:
        issues_found += 1
        if _suggest_credentials_fix(settings):
            fixes_applied += 1
    else:
        print(f"  [OK] {creds_result.message}")

    # Summary
    print()
    print("=" * 60)
    if issues_found == 0:
        print("No issues found! Your configuration looks good.")
        return 0
    elif fixes_applied > 0:
        print(f"Found {issues_found} issue(s). Suggested fixes provided.")
        print("After applying fixes, run 'warp doctor' to verify.")
        return 0
    else:
        print(f"Found {issues_found} issue(s). See suggestions above.")
        return 1
