"""Backup and restore commands using Duplicati."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import click

from ptctools._s3 import (
    parse_s3_uri,
    is_s3_uri,
    get_s3_credentials,
    get_s3_endpoint,
    build_duplicati_s3_url,
)


def is_docker_available() -> bool:
    """Check if Docker is available."""
    return shutil.which("docker") is not None


def is_duplicati_available() -> bool:
    """Check if local duplicati-cli is available."""
    return shutil.which("duplicati-cli") is not None


def detect_runner() -> str:
    """Auto-detect the best runner: docker if available, otherwise local."""
    if is_docker_available():
        return "docker"
    if is_duplicati_available():
        return "local"
    return "docker"  # Default, will fail with helpful message


def validate_runner(runner: str) -> str:
    """Validate and resolve runner, exit on error."""
    if runner == "auto":
        runner = detect_runner()
        click.echo(f"Auto-detected runner: {runner}")

    if runner == "docker" and not is_docker_available():
        click.echo(
            "Error: Docker is not available. Install Docker or use --runner local",
            err=True,
        )
        sys.exit(1)
    if runner == "local" and not is_duplicati_available():
        click.echo(
            "Error: duplicati-cli is not available. Install Duplicati or use --runner docker",
            err=True,
        )
        sys.exit(1)
    return runner


def run_duplicati_command(
    runner: str,
    command: str,
    remote_location: str,
    local_path: str,
    passphrase: str,
    extra_args: list[str] | None = None,
    volume_mounts: list[tuple[str, str]] | None = None,
) -> subprocess.CompletedProcess:
    """Run duplicati-cli command using the specified runner."""
    base_args = [command, remote_location]

    if command == "backup":
        base_args.append(local_path if runner == "local" else "/data")

    if passphrase:
        base_args.append(f"--passphrase={passphrase}")
    else:
        base_args.append("--no-encryption")

    if extra_args:
        base_args.extend(extra_args)

    if runner == "docker":
        cmd = ["docker", "run", "--rm"]
        # Add volume mounts based on command
        if command == "backup":
            cmd.extend(["-v", f"{local_path}:/data:ro"])
        elif command == "restore":
            cmd.extend(["-v", f"{local_path}:/restore"])
        if volume_mounts:
            for host_path, container_path in volume_mounts:
                cmd.extend(["-v", f"{host_path}:{container_path}"])
        # Add temp directory for Duplicati database
        cmd.extend(["--tmpfs", "/tmp:rw,noexec,nosuid"])
        cmd.extend(["-e", "TMPDIR=/tmp"])
        cmd.extend(["duplicati/duplicati", "duplicati-cli"])
        cmd.extend(["--dbpath=/tmp/duplicati.sqlite"])
        cmd.extend(base_args)
    else:
        cmd = ["duplicati-cli"]
        cmd.extend(base_args)

    return subprocess.run(cmd, capture_output=True, text=True)


def resolve_s3_destination(
    uri: str, s3_endpoint: str | None
) -> tuple[str, str, str, str]:
    """Resolve S3 URI to destination URL and display info.

    Returns: (destination_url, bucket, path, endpoint)
    """
    try:
        uri_endpoint, bucket, s3_path = parse_s3_uri(uri)
    except click.ClickException as e:
        click.echo(f"Error: {e.message}", err=True)
        sys.exit(1)

    try:
        endpoint = get_s3_endpoint(uri_endpoint, s3_endpoint)
    except click.ClickException as e:
        click.echo(f"Error: {e.message}", err=True)
        sys.exit(1)

    destination = build_duplicati_s3_url(bucket, s3_path, endpoint)
    return destination, bucket, s3_path, endpoint


# Common CLI options
runner_option = click.option(
    "--runner",
    type=click.Choice(["docker", "local", "auto"]),
    default="auto",
    help="Runner: docker, local duplicati-cli, or auto-detect (default)",
)
s3_endpoint_option = click.option(
    "--s3-endpoint",
    help="S3/MinIO endpoint URL (can also use S3_ENDPOINT env var)",
)
passphrase_option = click.option(
    "--passphrase",
    type=str,
    default="",
    help="Encryption passphrase (can also use DUPLICATI_PASSPHRASE env var)",
)


@click.group()
def cli():
    """Utility commands for backup and restore."""
    pass


@cli.command()
@click.option(
    "--input",
    "input_dir",
    required=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    help="Input directory to backup",
)
@click.option(
    "--output",
    "output_path",
    required=True,
    type=str,
    help="Output destination: local directory or S3 URI (s3://bucket/path)",
)
@s3_endpoint_option
@click.option(
    "--keep-versions",
    type=int,
    default=7,
    help="Keep N versions (default: 7)",
)
@passphrase_option
@runner_option
def backup(
    input_dir: Path,
    output_path: str,
    s3_endpoint: str | None,
    keep_versions: int,
    passphrase: str,
    runner: str,
):
    """Backup a directory to local or S3 destination.

    Examples:
        ptctools backup --input ./data --output ./backups
        ptctools backup --input ./data --output s3://mybucket/backups
        ptctools backup --input ./data --output s3://mybucket/backups --s3-endpoint https://s3.<region>.amazonaws.com
    """
    input_dir = input_dir.resolve()
    runner = validate_runner(runner)
    passphrase = passphrase or os.environ.get("DUPLICATI_PASSPHRASE", "")

    if is_s3_uri(output_path):
        destination, bucket, s3_path, endpoint = resolve_s3_destination(
            output_path, s3_endpoint
        )
        try:
            s3_access_key, s3_secret_key = get_s3_credentials()
        except click.ClickException as e:
            click.echo(f"Error: {e.message}", err=True)
            sys.exit(1)

        extra_args = [
            f"--aws-access-key-id={s3_access_key}",
            f"--aws-secret-access-key={s3_secret_key}",
            f"--keep-versions={keep_versions}",
            "--retention-policy=",
        ]

        click.echo(f"Input: {input_dir}")
        click.echo(f"Output: s3://{bucket}/{s3_path}")
        click.echo(f"Endpoint: {endpoint}")
        click.echo(f"Runner: {runner}")
        click.echo(f"Encryption: {'Enabled' if passphrase else 'Disabled'}")
        click.echo()

        result = run_duplicati_command(
            runner=runner,
            command="backup",
            remote_location=destination,
            local_path=str(input_dir),
            passphrase=passphrase,
            extra_args=extra_args,
        )
    else:
        output_dir = Path(output_path).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

        click.echo(f"Input: {input_dir}")
        click.echo(f"Output: {output_dir}")
        click.echo(f"Runner: {runner}")
        click.echo(f"Encryption: {'Enabled' if passphrase else 'Disabled'}")
        click.echo()

        extra_args = [f"--keep-versions={keep_versions}", "--retention-policy="]

        if runner == "docker":
            result = run_duplicati_command(
                runner=runner,
                command="backup",
                remote_location="file:///backup",
                local_path=str(input_dir),
                passphrase=passphrase,
                extra_args=extra_args,
                volume_mounts=[(str(output_dir), "/backup")],
            )
        else:
            result = run_duplicati_command(
                runner=runner,
                command="backup",
                remote_location=f"file://{output_dir}",
                local_path=str(input_dir),
                passphrase=passphrase,
                extra_args=extra_args,
            )

    if result.returncode != 0:
        click.echo(f"✗ Backup failed with exit code {result.returncode}")
        if result.stderr:
            click.echo(f"Error: {result.stderr}")
        if result.stdout:
            click.echo(f"Output: {result.stdout}")
        sys.exit(1)

    click.echo("✓ Backup completed successfully")
    for line in result.stdout.split("\n"):
        if any(k in line.lower() for k in ["uploaded", "added", "bytes", "file"]):
            click.echo(f"  {line.strip()}")


@cli.command()
@click.option(
    "--input",
    "input_path",
    required=True,
    type=str,
    help="Input source: local Duplicati backup directory or S3 URI",
)
@click.option(
    "--output",
    "output_dir",
    required=True,
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    help="Output directory to restore files to",
)
@s3_endpoint_option
@passphrase_option
@runner_option
@click.option(
    "--restore-path",
    type=str,
    default="",
    help="Specific path within backup to restore (default: all files)",
)
def restore(
    input_path: str,
    output_dir: Path,
    s3_endpoint: str | None,
    passphrase: str,
    runner: str,
    restore_path: str,
):
    """Restore files from a Duplicati backup.

    Examples:
        ptctools restore --input ./backups --output ./restored
        ptctools restore --input s3://mybucket/backups --output ./restored
        ptctools restore --input s3://mybucket/backups --output ./restored --restore-path "config.yaml"
    """
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    runner = validate_runner(runner)
    passphrase = passphrase or os.environ.get("DUPLICATI_PASSPHRASE", "")

    extra_args = ["--overwrite=true", "--all-versions=false"]
    if restore_path:
        extra_args.append(f"--restore-path={restore_path}")
    else:
        extra_args.append("*")  # Restore all files

    if is_s3_uri(input_path):
        source, bucket, s3_path, endpoint = resolve_s3_destination(
            input_path, s3_endpoint
        )
        try:
            s3_access_key, s3_secret_key = get_s3_credentials()
        except click.ClickException as e:
            click.echo(f"Error: {e.message}", err=True)
            sys.exit(1)

        extra_args.extend(
            [
                f"--aws-access-key-id={s3_access_key}",
                f"--aws-secret-access-key={s3_secret_key}",
            ]
        )

        click.echo(f"Input: s3://{bucket}/{s3_path}")
        click.echo(f"Output: {output_dir}")
        click.echo(f"Endpoint: {endpoint}")
        click.echo(f"Runner: {runner}")
        click.echo(f"Encryption: {'Enabled' if passphrase else 'Disabled'}")
        click.echo()

        if runner == "docker":
            extra_args.append("--restore-path=/restore")
            result = run_duplicati_command(
                runner=runner,
                command="restore",
                remote_location=source,
                local_path=str(output_dir),
                passphrase=passphrase,
                extra_args=extra_args,
            )
        else:
            extra_args.append(f"--restore-path={output_dir}")
            result = run_duplicati_command(
                runner=runner,
                command="restore",
                remote_location=source,
                local_path=str(output_dir),
                passphrase=passphrase,
                extra_args=extra_args,
            )
    else:
        input_dir = Path(input_path).resolve()
        if not input_dir.exists():
            click.echo(f"Error: Input directory does not exist: {input_dir}", err=True)
            sys.exit(1)

        click.echo(f"Input: {input_dir}")
        click.echo(f"Output: {output_dir}")
        click.echo(f"Runner: {runner}")
        click.echo(f"Encryption: {'Enabled' if passphrase else 'Disabled'}")
        click.echo()

        if runner == "docker":
            extra_args.append("--restore-path=/restore")
            result = run_duplicati_command(
                runner=runner,
                command="restore",
                remote_location="file:///backup",
                local_path=str(output_dir),
                passphrase=passphrase,
                extra_args=extra_args,
                volume_mounts=[(str(input_dir), "/backup:ro")],
            )
        else:
            extra_args.append(f"--restore-path={output_dir}")
            result = run_duplicati_command(
                runner=runner,
                command="restore",
                remote_location=f"file://{input_dir}",
                local_path=str(output_dir),
                passphrase=passphrase,
                extra_args=extra_args,
            )

    if result.returncode != 0:
        click.echo(f"✗ Restore failed with exit code {result.returncode}")
        if result.stderr:
            click.echo(f"Error: {result.stderr}")
        if result.stdout:
            click.echo(f"Output: {result.stdout}")
        sys.exit(1)

    click.echo("✓ Restore completed successfully")
    for line in result.stdout.split("\n"):
        if any(k in line.lower() for k in ["restored", "files", "bytes"]):
            click.echo(f"  {line.strip()}")
