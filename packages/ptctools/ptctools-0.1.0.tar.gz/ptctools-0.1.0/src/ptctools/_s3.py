"""S3 utility functions for URI parsing and operations."""

from __future__ import annotations

import os
import re
from urllib.parse import urlparse

import click


def parse_s3_uri(uri: str) -> tuple[str | None, str, str]:
    """Parse S3 URI into (endpoint, bucket, path).

    Supports formats:
    - s3://bucket/path
    - s3://bucket/path?s3-server-name=endpoint
    - s3://endpoint.com/bucket/path (endpoint detected by dots in first segment)
    - https://endpoint.com/bucket/path

    Returns:
        Tuple of (endpoint or None, bucket, path)
        - endpoint: The S3 endpoint URL or None if not specified
        - bucket: The bucket name
        - path: The object path within the bucket (may be empty)
    """
    if not uri:
        raise click.ClickException("Empty S3 URI")

    # Handle https:// or http:// scheme
    if uri.startswith("https://") or uri.startswith("http://"):
        parsed = urlparse(uri)
        endpoint = f"{parsed.scheme}://{parsed.netloc}"
        path_parts = parsed.path.strip("/").split("/", 1)
        bucket = path_parts[0] if path_parts else ""
        path = path_parts[1] if len(path_parts) > 1 else ""

        if not bucket:
            raise click.ClickException(f"Could not parse bucket from URI: {uri}")

        return endpoint, bucket, path

    # Handle s3:// scheme
    if not uri.startswith("s3://"):
        raise click.ClickException(
            f"Invalid S3 URI format: {uri}. Expected s3://bucket/path or https://endpoint/bucket/path"
        )

    rest = uri[5:]  # Remove "s3://"

    # Check for query parameter format: s3://bucket/path?s3-server-name=endpoint
    if "?s3-server-name=" in rest:
        match = re.match(r"([^/]+)/(.+?)\?s3-server-name=(.+)$", rest)
        if match:
            bucket = match.group(1)
            path = match.group(2)
            endpoint = match.group(3)
            # Add https:// if not present
            if not endpoint.startswith("http://") and not endpoint.startswith("https://"):
                endpoint = f"https://{endpoint}"
            return endpoint, bucket, path

    # Split by first slash
    parts = rest.split("/", 1)
    first_part = parts[0]
    remaining = parts[1] if len(parts) > 1 else ""

    # Check if first part looks like an endpoint (has dots) or just bucket name
    if "." in first_part:
        # It's an endpoint like s3://minio.example.com/bucket/path
        endpoint = f"https://{first_part}"
        # remaining is now bucket/path
        sub_parts = remaining.split("/", 1)
        bucket = sub_parts[0] if sub_parts else ""
        path = sub_parts[1] if len(sub_parts) > 1 else ""
    else:
        # It's just a bucket name like s3://bucket/path
        endpoint = None
        bucket = first_part
        path = remaining

    if not bucket:
        raise click.ClickException(f"Could not parse bucket from S3 URI: {uri}")

    return endpoint, bucket, path


def is_s3_uri(path: str) -> bool:
    """Check if path is an S3 URI."""
    return path.startswith("s3://") or path.startswith("https://") or path.startswith("http://")


def get_s3_endpoint(uri_endpoint: str | None, cli_endpoint: str | None = None) -> str:
    """Get S3 endpoint from various sources.

    Priority: CLI argument > URI embedded > environment variable

    Args:
        uri_endpoint: Endpoint parsed from URI (may be None)
        cli_endpoint: Endpoint from CLI argument (may be None)

    Returns:
        The resolved endpoint URL

    Raises:
        ClickException if no endpoint can be resolved
    """
    endpoint = cli_endpoint or uri_endpoint or os.environ.get("S3_ENDPOINT")
    if not endpoint:
        raise click.ClickException(
            "S3 endpoint required. Use --s3-endpoint, embed in URI (s3://endpoint/bucket), "
            "or set S3_ENDPOINT environment variable"
        )
    return endpoint


def get_s3_credentials() -> tuple[str, str]:
    """Get S3 credentials from environment variables.

    Returns:
        Tuple of (access_key, secret_key)

    Raises:
        ClickException if credentials are missing
    """
    s3_access_key = os.environ.get("S3_ACCESS_KEY")
    s3_secret_key = os.environ.get("S3_SECRET_KEY")
    if not s3_access_key or not s3_secret_key:
        raise click.ClickException(
            "Missing S3_ACCESS_KEY or S3_SECRET_KEY environment variables"
        )
    return s3_access_key, s3_secret_key


def build_duplicati_s3_url(bucket: str, path: str, endpoint: str) -> str:
    """Build Duplicati-compatible S3 URL with query parameter.

    Args:
        bucket: S3 bucket name
        path: Object path within bucket
        endpoint: S3 endpoint URL

    Returns:
        Duplicati-compatible S3 URL like: s3://bucket/path?s3-server-name=host
    """
    s3_host = endpoint.replace("https://", "").replace("http://", "").rstrip("/")
    if path:
        return f"s3://{bucket}/{path}?s3-server-name={s3_host}"
    else:
        return f"s3://{bucket}?s3-server-name={s3_host}"
