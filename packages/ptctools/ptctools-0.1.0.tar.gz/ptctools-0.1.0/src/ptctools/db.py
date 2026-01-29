"""Database backup and restore commands."""

from __future__ import annotations

import os
import sys

import click

from ptctools._portainer import create_exec, start_exec, run_ephemeral_container
from ptctools._s3 import parse_s3_uri, is_s3_uri, get_s3_endpoint, get_s3_credentials


# Database type to backup path mapping
DB_BACKUP_PATHS = {
    "postgres": "/var/lib/postgresql/data/backup.sql.gz",
}

ALLOWED_DB_TYPES = list(DB_BACKUP_PATHS.keys())


def run_mc_command(
    portainer_url: str,
    access_token: str,
    endpoint_id: int,
    volume_name: str,
    s3_endpoint: str,
    s3_access_key: str,
    s3_secret_key: str,
    mc_args: list[str],
) -> tuple[int, str]:
    """Run minio/mc command in ephemeral container.

    The volume is mounted at /data in the container.
    """
    # mc needs alias setup before running commands
    # We configure 's3' alias and run the command
    alias_cmd = f"mc alias set s3 {s3_endpoint} {s3_access_key} {s3_secret_key}"
    mc_cmd = "mc " + " ".join(mc_args)
    full_cmd = f"{alias_cmd} && {mc_cmd}"

    config = {
        "Image": "minio/mc:latest",
        "Entrypoint": ["sh", "-c"],
        "Cmd": [full_cmd],
        "HostConfig": {
            "Binds": [f"{volume_name}:/data"],
            "AutoRemove": False,
        },
    }

    return run_ephemeral_container(portainer_url, access_token, endpoint_id, config)


def backup_database(
    portainer_url: str,
    access_token: str,
    endpoint_id: int,
    container_id: str,
    volume_name: str,
    db_user: str,
    db_name: str,
    db_type: str,
    output: str,
    s3_endpoint: str | None,
    s3_access_key: str | None,
    s3_secret_key: str | None,
) -> bool:
    """Backup database using pg_dump via exec, then optionally upload to S3 with mc."""
    backup_file = DB_BACKUP_PATHS[db_type]
    backup_filename = os.path.basename(backup_file)

    click.echo(f"  Using container: {container_id[:12]}")

    # Step 1: Run pg_dump inside the database container
    click.echo("  Running pg_dump...")
    cmd = [
        "sh",
        "-c",
        f"pg_dump -U {db_user} {db_name} | gzip > {backup_file} && "
        f"stat -c %s {backup_file}",
    ]

    exec_id = create_exec(portainer_url, access_token, endpoint_id, container_id, cmd)
    if not exec_id:
        click.echo("  ✗ Failed to create exec instance")
        return False

    exit_code, output_text = start_exec(
        portainer_url, access_token, endpoint_id, exec_id
    )
    if exit_code != 0:
        click.echo(f"  ✗ pg_dump failed with exit code {exit_code}")
        if output_text.strip():
            click.echo(f"  {output_text.strip()}")
        return False

    # Parse file size from stat output
    try:
        file_size = int(output_text.strip().split("\n")[-1])
        click.echo(f"  ✓ pg_dump completed ({file_size} bytes)")
    except (ValueError, IndexError):
        click.echo("  ✓ pg_dump completed")

    # Step 2: Handle output (local file or S3)
    if is_s3_uri(output):
        # Upload to S3 using minio/mc
        try:
            uri_endpoint, bucket, s3_path = parse_s3_uri(output)
        except click.ClickException as e:
            click.echo(f"  ✗ {e.message}")
            return False

        try:
            endpoint = get_s3_endpoint(uri_endpoint, s3_endpoint)
        except click.ClickException as e:
            click.echo(f"  ✗ {e.message}")
            return False

        if not s3_access_key or not s3_secret_key:
            click.echo("  ✗ S3 credentials required (S3_ACCESS_KEY, S3_SECRET_KEY)")
            return False

        click.echo(f"  Uploading to S3: s3://{bucket}/{s3_path}...")

        mc_exit_code, mc_logs = run_mc_command(
            portainer_url,
            access_token,
            endpoint_id,
            volume_name,
            endpoint,
            s3_access_key,
            s3_secret_key,
            ["cp", f"/data/{backup_filename}", f"s3/{bucket}/{s3_path}"],
        )

        if mc_exit_code != 0:
            click.echo(f"  ✗ S3 upload failed with exit code {mc_exit_code}")
            if mc_logs:
                click.echo(f"  {mc_logs}")
            return False

        click.echo(f"  ✓ Uploaded to s3://{bucket}/{s3_path}")
        if mc_logs:
            for line in mc_logs.strip().split("\n"):
                if line.strip():
                    click.echo(f"    {line.strip()}")

    else:
        # Copy backup file to local path
        click.echo(f"  Saving to local file: {output}...")

        # Read file from container using base64 encoding
        read_cmd = ["sh", "-c", f"base64 {backup_file}"]
        read_exec_id = create_exec(
            portainer_url, access_token, endpoint_id, container_id, read_cmd
        )
        if not read_exec_id:
            click.echo("  ✗ Failed to read backup file from container")
            return False

        read_exit_code, b64_content = start_exec(
            portainer_url, access_token, endpoint_id, read_exec_id
        )
        if read_exit_code != 0:
            click.echo(f"  ✗ Failed to read backup file: exit code {read_exit_code}")
            return False

        # Decode and save to output file
        import base64

        content = base64.b64decode(b64_content.strip())

        # Ensure output directory exists
        output_dir = os.path.dirname(output)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(output, "wb") as f:
            f.write(content)

        click.echo(f"  ✓ Saved to {output} ({len(content)} bytes)")

    # Step 3: Cleanup - delete the .sql.gz file from the container volume
    click.echo("  Cleaning up temporary backup file...")
    cleanup_cmd = ["sh", "-c", f"rm -f {backup_file}"]
    cleanup_exec_id = create_exec(
        portainer_url, access_token, endpoint_id, container_id, cleanup_cmd
    )
    if cleanup_exec_id:
        start_exec(portainer_url, access_token, endpoint_id, cleanup_exec_id)
        click.echo("  ✓ Cleanup completed")

    return True


def restore_database(
    portainer_url: str,
    access_token: str,
    endpoint_id: int,
    container_id: str,
    volume_name: str,
    db_user: str,
    db_name: str,
    db_type: str,
    input_path: str,
    s3_endpoint: str | None,
    s3_access_key: str | None,
    s3_secret_key: str | None,
) -> bool:
    """Restore database from local file or S3."""
    restore_path = DB_BACKUP_PATHS[db_type]
    restore_filename = os.path.basename(restore_path)

    click.echo(f"  Using container: {container_id[:12]}")

    # Step 1: Get the backup file (from S3 or local)
    if is_s3_uri(input_path):
        # Download from S3 using minio/mc
        try:
            uri_endpoint, bucket, s3_path = parse_s3_uri(input_path)
        except click.ClickException as e:
            click.echo(f"  ✗ {e.message}")
            return False

        try:
            endpoint = get_s3_endpoint(uri_endpoint, s3_endpoint)
        except click.ClickException as e:
            click.echo(f"  ✗ {e.message}")
            return False

        if not s3_access_key or not s3_secret_key:
            click.echo("  ✗ S3 credentials required (S3_ACCESS_KEY, S3_SECRET_KEY)")
            return False

        click.echo(f"  Downloading from S3: s3://{bucket}/{s3_path}...")

        # mc cp s3/bucket/path /data/backup.sql.gz
        mc_exit_code, mc_logs = run_mc_command(
            portainer_url,
            access_token,
            endpoint_id,
            volume_name,
            endpoint,
            s3_access_key,
            s3_secret_key,
            ["cp", f"s3/{bucket}/{s3_path}", f"/data/{restore_filename}"],
        )

        if mc_exit_code != 0:
            click.echo(f"  ✗ S3 download failed with exit code {mc_exit_code}")
            if mc_logs:
                click.echo(f"  {mc_logs}")
            return False

        click.echo("  ✓ Downloaded from S3")
        if mc_logs:
            for line in mc_logs.strip().split("\n"):
                if line.strip():
                    click.echo(f"    {line.strip()}")

    else:
        # Upload local file to container volume
        click.echo(f"  Uploading from local file: {input_path}...")
        if not os.path.exists(input_path):
            click.echo(f"  ✗ File not found: {input_path}")
            return False

        import base64

        with open(input_path, "rb") as f:
            content = f.read()
        b64_content = base64.b64encode(content).decode("ascii")
        click.echo(f"  ✓ Read {len(content)} bytes")

        # Write file to container using base64 decoding (in chunks)
        click.echo("  Uploading backup to container...")
        chunk_size = 65536  # 64KB chunks
        chunks = [
            b64_content[i : i + chunk_size]
            for i in range(0, len(b64_content), chunk_size)
        ]

        # First chunk: create file
        write_cmd = ["sh", "-c", f"echo '{chunks[0]}' | base64 -d > {restore_path}"]
        write_exec_id = create_exec(
            portainer_url, access_token, endpoint_id, container_id, write_cmd
        )
        if not write_exec_id:
            click.echo("  ✗ Failed to write backup file to container")
            return False

        write_exit_code, _ = start_exec(
            portainer_url, access_token, endpoint_id, write_exec_id
        )
        if write_exit_code != 0:
            click.echo(f"  ✗ Failed to write backup file: exit code {write_exit_code}")
            return False

        # Append remaining chunks
        for chunk in chunks[1:]:
            append_cmd = ["sh", "-c", f"echo '{chunk}' | base64 -d >> {restore_path}"]
            append_exec_id = create_exec(
                portainer_url, access_token, endpoint_id, container_id, append_cmd
            )
            if append_exec_id:
                start_exec(portainer_url, access_token, endpoint_id, append_exec_id)

        click.echo("  ✓ Backup file uploaded to container")

    # Step 2: Restore the database using psql
    click.echo("  Running restore...")
    # Use gunzip for .gz files, cat for plain SQL files
    if input_path.endswith(".gz"):
        read_cmd = f"gunzip -c {restore_path}"
    else:
        read_cmd = f"cat {restore_path}"
    psql_cmd = f"{read_cmd} | psql -U {db_user} -d {db_name}"
    cmd = ["sh", "-c", psql_cmd]

    exec_id = create_exec(portainer_url, access_token, endpoint_id, container_id, cmd)
    if not exec_id:
        click.echo("  ✗ Failed to create exec instance")
        return False

    exit_code, output = start_exec(portainer_url, access_token, endpoint_id, exec_id)
    if output.strip():
        # Show last 10 lines of output
        lines = output.strip().split("\n")[-10:]
        for line in lines:
            click.echo(f"  {line}")

    # Step 3: Cleanup - delete the restore file from container
    cleanup_cmd = ["sh", "-c", f"rm -f {restore_path}"]
    cleanup_exec_id = create_exec(
        portainer_url, access_token, endpoint_id, container_id, cleanup_cmd
    )
    if cleanup_exec_id:
        start_exec(portainer_url, access_token, endpoint_id, cleanup_exec_id)

    if exit_code == 0:
        click.echo("  ✓ Database restore completed")
        return True
    else:
        click.echo(f"  ✗ Restore failed with exit code {exit_code}")
        return False


@click.group()
def cli():
    """Database backup and restore commands."""
    pass


@cli.command()
@click.option("--url", "-u", required=True, help="Portainer base URL")
@click.option("--container-id", "-c", required=True, help="Database container ID")
@click.option(
    "--volume-name", "-v", required=True, help="Volume name where database stores data"
)
@click.option(
    "--output",
    "-o",
    required=True,
    help="Output: local file.sql.gz or s3://bucket/path/file.sql.gz",
)
@click.option("--s3-endpoint", help="S3/MinIO endpoint URL (or S3_ENDPOINT env var)")
@click.option("--endpoint-id", "-e", type=int, default=1, help="Portainer endpoint ID")
@click.option(
    "--db-type",
    "-t",
    type=click.Choice(ALLOWED_DB_TYPES),
    default="postgres",
    help="Database type (default: postgres)",
)
@click.option("--db-user", required=True, help="Database user")
@click.option("--db-name", required=True, help="Database name")
def backup(
    url: str,
    container_id: str,
    volume_name: str,
    output: str,
    s3_endpoint: str | None,
    endpoint_id: int,
    db_type: str,
    db_user: str,
    db_name: str,
):
    """Backup PostgreSQL database to local file or S3.

    Examples:
        ptctools db backup -u https://portainer.example.com -c abc123 -v db_data --db-user postgres --db-name mydb -o /tmp/backup.sql.gz

        ptctools db backup -u https://portainer.example.com -c abc123 -v db_data --db-user postgres --db-name mydb -o s3://mybucket/backups/backup.sql.gz --s3-endpoint https://s3.<region>.amazonaws.com
    """
    access_token = os.environ.get("PORTAINER_ACCESS_TOKEN")
    if not access_token:
        click.echo("Error: Missing PORTAINER_ACCESS_TOKEN", err=True)
        sys.exit(1)

    s3_access_key = os.environ.get("S3_ACCESS_KEY")
    s3_secret_key = os.environ.get("S3_SECRET_KEY")

    # Check S3 credentials if output is S3 URI
    if is_s3_uri(output):
        if not s3_access_key or not s3_secret_key:
            click.echo(
                "Error: Missing S3_ACCESS_KEY or S3_SECRET_KEY for S3 upload", err=True
            )
            sys.exit(1)

    portainer_url = url.rstrip("/")

    click.echo(f"Portainer URL: {portainer_url}")
    click.echo(f"Container ID: {container_id[:12]}")
    click.echo(f"Volume Name: {volume_name}")
    click.echo(f"Database Type: {db_type}")
    click.echo(f"Database: {db_name} (user: {db_user})")
    click.echo(f"Output: {output}")
    if is_s3_uri(output):
        endpoint = s3_endpoint or os.environ.get("S3_ENDPOINT")
        click.echo(f"S3 Endpoint: {endpoint}")
    click.echo()
    click.echo("=== Backing up database ===")

    success = backup_database(
        portainer_url,
        access_token,
        endpoint_id,
        container_id,
        volume_name,
        db_user,
        db_name,
        db_type,
        output,
        s3_endpoint,
        s3_access_key,
        s3_secret_key,
    )

    click.echo()
    click.echo(
        "=== Database backup complete ==="
        if success
        else "=== Database backup failed ==="
    )
    sys.exit(0 if success else 1)


@cli.command()
@click.option("--url", "-u", required=True, help="Portainer base URL")
@click.option("--container-id", "-c", required=True, help="Database container ID")
@click.option(
    "--volume-name", "-v", required=True, help="Volume name where database stores data"
)
@click.option(
    "--input",
    "-i",
    "input_path",
    required=True,
    help="Input: local file.sql.gz or s3://bucket/path/file.sql.gz",
)
@click.option("--s3-endpoint", help="S3/MinIO endpoint URL (or S3_ENDPOINT env var)")
@click.option("--endpoint-id", "-e", type=int, default=1, help="Portainer endpoint ID")
@click.option(
    "--db-type",
    "-t",
    type=click.Choice(ALLOWED_DB_TYPES),
    default="postgres",
    help="Database type (default: postgres)",
)
@click.option("--db-user", required=True, help="Database user")
@click.option("--db-name", required=True, help="Database name")
def restore(
    url: str,
    container_id: str,
    volume_name: str,
    input_path: str,
    s3_endpoint: str | None,
    endpoint_id: int,
    db_type: str,
    db_user: str,
    db_name: str,
):
    """Restore PostgreSQL database from local file or S3.

    Examples:
        ptctools db restore -u https://portainer.example.com -c abc123 -v db_data --db-user postgres --db-name mydb -i /tmp/backup.sql.gz

        ptctools db restore -u https://portainer.example.com -c abc123 -v db_data --db-user postgres --db-name mydb -i s3://mybucket/backups/backup.sql.gz --s3-endpoint https://s3.<region>.amazonaws.com
    """
    access_token = os.environ.get("PORTAINER_ACCESS_TOKEN")
    if not access_token:
        click.echo("Error: Missing PORTAINER_ACCESS_TOKEN", err=True)
        sys.exit(1)

    s3_access_key = os.environ.get("S3_ACCESS_KEY")
    s3_secret_key = os.environ.get("S3_SECRET_KEY")

    # Check S3 credentials if input is S3 URI
    if is_s3_uri(input_path):
        if not s3_access_key or not s3_secret_key:
            click.echo(
                "Error: Missing S3_ACCESS_KEY or S3_SECRET_KEY for S3 download",
                err=True,
            )
            sys.exit(1)

    portainer_url = url.rstrip("/")

    click.echo(f"Portainer URL: {portainer_url}")
    click.echo(f"Container ID: {container_id[:12]}")
    click.echo(f"Volume Name: {volume_name}")
    click.echo(f"Database Type: {db_type}")
    click.echo(f"Database: {db_name} (user: {db_user})")
    click.echo(f"Input: {input_path}")
    if is_s3_uri(input_path):
        endpoint = s3_endpoint or os.environ.get("S3_ENDPOINT")
        click.echo(f"S3 Endpoint: {endpoint}")
    click.echo()
    click.echo("=== Restoring database ===")

    success = restore_database(
        portainer_url,
        access_token,
        endpoint_id,
        container_id,
        volume_name,
        db_user,
        db_name,
        db_type,
        input_path,
        s3_endpoint,
        s3_access_key,
        s3_secret_key,
    )

    click.echo()
    click.echo(
        "=== Database restore complete ==="
        if success
        else "=== Database restore failed ==="
    )
    sys.exit(0 if success else 1)
