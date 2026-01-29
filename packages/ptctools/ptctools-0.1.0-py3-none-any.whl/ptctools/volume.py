"""Volume backup and restore commands."""

from __future__ import annotations

import os
import sys

import click

from ptctools._portainer import run_ephemeral_container
from ptctools._s3 import (
    parse_s3_uri,
    get_s3_endpoint,
    get_s3_credentials,
    build_duplicati_s3_url,
)


def backup_volume(
    portainer_url: str,
    api_key: str,
    endpoint_id: int,
    volume_name: str,
    s3_endpoint: str,
    s3_bucket: str,
    s3_access_key: str,
    s3_secret_key: str,
    keep_versions: int,
    passphrase: str,
) -> bool:
    """Backup a single volume to S3 using Duplicati CLI."""
    s3_dest = build_duplicati_s3_url(s3_bucket, volume_name, s3_endpoint)

    click.echo(f"Backing up {volume_name} using Duplicati...")

    # Common options for both repair and backup
    common_opts = " ".join([
        f"--aws-access-key-id={s3_access_key}",
        f"--aws-secret-access-key={s3_secret_key}",
        f"--passphrase={passphrase}" if passphrase else "--no-encryption",
        "--dbpath=/tmp/duplicati.sqlite",
    ])

    # Repair command to rebuild local database from remote
    repair_cmd = f"duplicati-cli repair '{s3_dest}' {common_opts}"

    # Backup command
    backup_cmd = " ".join([
        "duplicati-cli",
        "backup",
        f"'{s3_dest}'",
        "/data",
        common_opts,
        f"--keep-versions={keep_versions}",
        "--retention-policy=",
    ])

    # Run repair first (rebuilds local DB from remote), then backup
    # Use ; instead of && because repair may return non-zero for warnings
    full_cmd = f"{repair_cmd}; {backup_cmd}"

    backup_config = {
        "Image": "duplicati/duplicati:latest",
        "Entrypoint": ["/bin/sh", "-c"],
        "Cmd": [full_cmd],
        "HostConfig": {
            "Binds": [f"{volume_name}:/data:ro"],
            "AutoRemove": False,
        },
    }

    exit_code, logs = run_ephemeral_container(
        portainer_url, api_key, endpoint_id, backup_config
    )

    # Check for backup failure
    # Exit code 1 with "0 files need to be examined" = success (no changes)
    no_changes = exit_code == 1 and logs and "0 files need to be examined" in logs
    if exit_code != 0 and not no_changes:
        click.echo(f"  ✗ Backup failed with exit code {exit_code}")
        if logs:
            click.echo(f"  Logs: {logs}")
        return False

    click.echo(f"  ✓ Backup completed: s3://{s3_bucket}/{volume_name}")
    if logs:
        for line in logs.split("\n"):
            if any(
                k in line.lower()
                for k in ["uploaded", "added", "deleted", "modified", "examined"]
            ):
                click.echo(f"    {line.strip()}")

    return True


def restore_volume(
    portainer_url: str,
    api_key: str,
    endpoint_id: int,
    volume_name: str,
    s3_endpoint: str,
    s3_bucket: str,
    s3_path: str,
    s3_access_key: str,
    s3_secret_key: str,
    passphrase: str,
    version: int | None,
    restore_time: str | None,
) -> bool:
    """Restore a single volume from S3 using Duplicati CLI.
    
    Args:
        s3_path: S3 path to restore from (used directly, no modification).
    """
    s3_dest = build_duplicati_s3_url(s3_bucket, s3_path, s3_endpoint)

    click.echo(f"Restoring {volume_name} using Duplicati...")

    restore_cmd = [
        "duplicati-cli",
        "restore",
        s3_dest,
        "/data/",
        f"--aws-access-key-id={s3_access_key}",
        f"--aws-secret-access-key={s3_secret_key}",
        f"--passphrase={passphrase}",
        "--overwrite=true",
        "--dbpath=/tmp/duplicati.sqlite",
        "--no-encryption" if not passphrase else "",
    ]

    if version is not None:
        restore_cmd.append(f"--version={version}")
    if restore_time:
        restore_cmd.append(f"--time={restore_time}")

    restore_cmd = [c for c in restore_cmd if c]

    restore_config = {
        "Image": "duplicati/duplicati:latest",
        "Cmd": restore_cmd,
        "HostConfig": {
            "Binds": [f"{volume_name}:/data"],
            "AutoRemove": False,
        },
    }

    exit_code, logs = run_ephemeral_container(
        portainer_url, api_key, endpoint_id, restore_config
    )

    # Success if exit_code == 0, or exit_code == 2 with no files needing restore (already up-to-date)
    already_up_to_date = exit_code == 2 and logs and "0 files need to be restored" in logs
    if exit_code != 0 and not already_up_to_date:
        click.echo(f"  ✗ Restore failed with exit code {exit_code}")
        if logs:
            click.echo(f"  Logs: {logs}")
        return False

    click.echo(f"  ✓ Restore completed from s3://{s3_bucket}/{volume_name}")
    if logs:
        for line in logs.split("\n"):
            if any(
                k in line.lower() for k in ["restored", "downloaded", "files", "bytes"]
            ):
                click.echo(f"    {line.strip()}")

    return True


@click.group()
def cli():
    """Volume backup and restore commands."""
    pass


@cli.command()
@click.option("--url", "-u", required=True, help="Portainer base URL")
@click.option(
    "--volumes", "-v", required=True, help="Comma-separated list of volume names"
)
@click.option(
    "--output",
    "-o",
    required=True,
    help="S3 URI (e.g., s3://bucket or s3://endpoint/bucket)",
)
@click.option("--s3-endpoint", help="S3/MinIO endpoint URL (or S3_ENDPOINT env var)")
@click.option("--endpoint-id", "-e", type=int, default=1, help="Portainer endpoint ID")
@click.option(
    "--keep-versions", type=int, default=7, help="Keep N versions of backups"
)
@click.option("--passphrase", type=str, default="", help="Encryption passphrase")
def backup(
    url: str,
    volumes: str,
    output: str,
    s3_endpoint: str | None,
    endpoint_id: int,
    keep_versions: int,
    passphrase: str,
):
    """Backup Docker volumes to S3 using Duplicati."""
    access_token = os.environ.get("PORTAINER_ACCESS_TOKEN")
    if not access_token:
        click.echo("Error: Missing PORTAINER_ACCESS_TOKEN", err=True)
        sys.exit(1)

    try:
        s3_access_key, s3_secret_key = get_s3_credentials()
    except click.ClickException as e:
        click.echo(f"Error: {e.message}", err=True)
        sys.exit(1)

    # Parse S3 URI
    try:
        uri_endpoint, s3_bucket, _ = parse_s3_uri(output)
        endpoint = get_s3_endpoint(uri_endpoint, s3_endpoint)
    except click.ClickException as e:
        click.echo(f"Error: {e.message}", err=True)
        sys.exit(1)

    passphrase = passphrase or os.environ.get("DUPLICATI_PASSPHRASE", "")
    portainer_url = url.rstrip("/")
    volume_list = [v.strip() for v in volumes.split(",")]

    click.echo(f"Portainer URL: {portainer_url}")
    click.echo(f"S3 Endpoint: {endpoint}")
    click.echo(f"S3 Bucket: {s3_bucket}")
    click.echo(f"Volumes: {len(volume_list)}")
    click.echo(f"Keep Versions: {keep_versions}")
    click.echo(f"Encryption: {'Enabled' if passphrase else 'Disabled'}")
    click.echo()
    click.echo("=== Backing up volumes with Duplicati ===")

    success_count = 0
    for vol in volume_list:
        if backup_volume(
            portainer_url,
            access_token,
            endpoint_id,
            vol,
            endpoint,
            s3_bucket,
            s3_access_key,
            s3_secret_key,
            keep_versions,
            passphrase,
        ):
            success_count += 1
        click.echo()

    click.echo("=== Volume backup complete ===")
    click.echo(f"Successfully backed up {success_count}/{len(volume_list)} volumes")
    sys.exit(0 if success_count == len(volume_list) else 1)


@cli.command()
@click.option("--url", "-u", required=True, help="Portainer base URL")
@click.option(
    "--volume",
    "-v",
    default=None,
    help="Volume name (derived from input URI path if not provided)",
)
@click.option(
    "--input",
    "-i",
    "input_uri",
    required=True,
    help="S3 URI (e.g., s3://bucket/volume-name or s3://endpoint/bucket/volume-name)",
)
@click.option("--s3-endpoint", help="S3/MinIO endpoint URL (or S3_ENDPOINT env var)")
@click.option("--endpoint-id", "-e", type=int, default=1, help="Portainer endpoint ID")
@click.option(
    "--version", type=int, default=None, help="Backup version to restore (0=latest)"
)
@click.option(
    "--time", "restore_time", type=str, default=None, help="Restore to specific time"
)
@click.option("--passphrase", type=str, default="", help="Encryption passphrase")
def restore(
    url: str,
    volume: str | None,
    input_uri: str,
    s3_endpoint: str | None,
    endpoint_id: int,
    version: int | None,
    restore_time: str | None,
    passphrase: str,
):
    """Restore Docker volumes from S3 using Duplicati."""
    access_token = os.environ.get("PORTAINER_ACCESS_TOKEN")
    if not access_token:
        click.echo("Error: Missing PORTAINER_ACCESS_TOKEN", err=True)
        sys.exit(1)

    try:
        s3_access_key, s3_secret_key = get_s3_credentials()
    except click.ClickException as e:
        click.echo(f"Error: {e.message}", err=True)
        sys.exit(1)

    # Parse S3 URI
    try:
        uri_endpoint, s3_bucket, uri_path = parse_s3_uri(input_uri)
        endpoint = get_s3_endpoint(uri_endpoint, s3_endpoint)
    except click.ClickException as e:
        click.echo(f"Error: {e.message}", err=True)
        sys.exit(1)

    # Get s3_path from URI (use as-is)
    s3_path = uri_path.strip("/") if uri_path else ""

    # Determine volume name: 1) from --volume arg, 2) from s3_path
    if volume:
        volume_name = volume
    elif s3_path:
        # Use the first path segment as volume name
        volume_name = s3_path.split("/")[0]
    else:
        click.echo("Error: No volume specified. Use --volume or include path in input URI", err=True)
        sys.exit(1)

    passphrase = passphrase or os.environ.get("DUPLICATI_PASSPHRASE", "")
    portainer_url = url.rstrip("/")

    click.echo(f"Portainer URL: {portainer_url}")
    click.echo(f"S3 Endpoint: {endpoint}")
    click.echo(f"S3 Bucket: {s3_bucket}")
    click.echo(f"S3 Path: {s3_path}")
    click.echo(f"Volume: {volume_name}")
    click.echo(f"Encryption: {'Enabled' if passphrase else 'Disabled'}")
    if version is not None:
        click.echo(f"Version: {version}")
    if restore_time:
        click.echo(f"Time: {restore_time}")
    click.echo()
    click.echo("=== Restoring volumes with Duplicati ===")

    success = restore_volume(
        portainer_url,
        access_token,
        endpoint_id,
        volume_name,
        endpoint,
        s3_bucket,
        s3_path,
        s3_access_key,
        s3_secret_key,
        passphrase,
        version,
        restore_time,
    )

    click.echo()
    click.echo("=== Volume restore complete ===")
    sys.exit(0 if success else 1)
