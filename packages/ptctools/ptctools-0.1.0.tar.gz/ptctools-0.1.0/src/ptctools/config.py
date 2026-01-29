"""Docker Swarm Config management commands via Portainer API."""

from __future__ import annotations

import base64
import json
import os
import sys
from pathlib import Path

import click

from ptctools._portainer import api_request


def list_configs(
    portainer_url: str,
    api_key: str,
    endpoint_id: int,
) -> tuple[list | None, int]:
    """List all Docker configs."""
    url = f"{portainer_url}/api/endpoints/{endpoint_id}/docker/configs"
    return api_request(url, api_key)


def get_config(
    portainer_url: str,
    api_key: str,
    endpoint_id: int,
    config_id: str,
) -> tuple[dict | None, int]:
    """Get a specific Docker config by ID."""
    url = f"{portainer_url}/api/endpoints/{endpoint_id}/docker/configs/{config_id}"
    return api_request(url, api_key)


def create_config(
    portainer_url: str,
    api_key: str,
    endpoint_id: int,
    name: str,
    data: str,
    labels: dict | None = None,
) -> tuple[dict | None, int]:
    """Create a new Docker config."""
    url = f"{portainer_url}/api/endpoints/{endpoint_id}/docker/configs/create"

    # Docker API requires base64 encoded data
    encoded_data = base64.b64encode(data.encode("utf-8")).decode("utf-8")

    payload = {
        "Name": name,
        "Data": encoded_data,
    }

    if labels:
        payload["Labels"] = labels

    return api_request(url, api_key, method="POST", data=payload)


def delete_config(
    portainer_url: str,
    api_key: str,
    endpoint_id: int,
    config_id: str,
) -> tuple[dict | None, int]:
    """Delete a Docker config."""
    url = f"{portainer_url}/api/endpoints/{endpoint_id}/docker/configs/{config_id}"
    return api_request(url, api_key, method="DELETE")


def find_config_by_name(
    portainer_url: str,
    api_key: str,
    endpoint_id: int,
    name: str,
) -> dict | None:
    """Find a config by name and return its details."""
    configs, status_code = list_configs(portainer_url, api_key, endpoint_id)

    if status_code != 200 or not isinstance(configs, list):
        return None

    for config in configs:
        spec = config.get("Spec", {})
        if spec.get("Name") == name:
            return config

    return None


@click.group()
def cli():
    """Docker Swarm Config management commands."""
    pass


@cli.command("set")
@click.option("--url", "-u", required=True, help="Portainer base URL")
@click.option("--name", "-n", required=True, help="Config name")
@click.option("--data", "-d", default=None, help="Config data (string content)")
@click.option(
    "--file",
    "-f",
    "file_path",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Read config data from file",
)
@click.option("--endpoint-id", "-e", type=int, default=1, help="Portainer endpoint ID")
@click.option(
    "--force", is_flag=True, help="Replace existing config if it exists"
)
def set_config(
    url: str,
    name: str,
    data: str | None,
    file_path: Path | None,
    endpoint_id: int,
    force: bool,
):
    """Create or update a Docker Swarm config.

    Examples:

        # Create from inline data
        ptctools config set -u https://portainer.example.com -n my-config -d "config content"

        # Create from file
        ptctools config set -u https://portainer.example.com -n nginx.conf -f ./nginx.conf

        # Replace existing config
        ptctools config set -u https://portainer.example.com -n my-config -d "new content" --force
    """
    # Validate that exactly one of --data or --file is provided
    if data is None and file_path is None:
        click.echo("Error: Either --data or --file must be provided", err=True)
        sys.exit(1)
    if data is not None and file_path is not None:
        click.echo("Error: Cannot use both --data and --file", err=True)
        sys.exit(1)

    # Read data from file if provided
    if file_path is not None:
        data = file_path.read_text()

    access_token = os.environ.get("PORTAINER_ACCESS_TOKEN")
    if not access_token:
        click.echo(
            "Error: Missing PORTAINER_ACCESS_TOKEN environment variable", err=True
        )
        sys.exit(1)

    portainer_url = url.rstrip("/")

    # Check if config already exists
    existing = find_config_by_name(portainer_url, access_token, endpoint_id, name)

    if existing:
        if not force:
            click.echo(
                f"Error: Config '{name}' already exists. Use --force to replace.",
                err=True,
            )
            sys.exit(1)

        # Delete existing config first (Docker doesn't support updating configs)
        # Docker Swarm configs are immutable - no update API exists.
        # The only way to change a config is to delete and recreate it.
        click.echo(f"Removing existing config: {name}")
        config_id = existing.get("ID")
        _, status_code = delete_config(
            portainer_url, access_token, endpoint_id, config_id
        )
        if status_code not in (200, 204):
            click.echo(
                f"Error: Failed to delete existing config (HTTP {status_code})",
                err=True,
            )
            sys.exit(1)

    click.echo(f"Creating config: {name}")
    response, status_code = create_config(
        portainer_url, access_token, endpoint_id, name, data
    )

    if 200 <= status_code < 300:
        config_id = response.get("ID") if response else "unknown"
        click.echo(f"✓ Config '{name}' created successfully (ID: {config_id})")
    else:
        click.echo(f"Error: Failed to create config (HTTP {status_code})", err=True)
        if response:
            click.echo(json.dumps(response, indent=2), err=True)
        sys.exit(1)


@cli.command("get")
@click.option("--url", "-u", required=True, help="Portainer base URL")
@click.option("--name", "-n", required=True, help="Config name")
@click.option("--endpoint-id", "-e", type=int, default=1, help="Portainer endpoint ID")
def get_config_cmd(url: str, name: str, endpoint_id: int):
    """Get details of a Docker Swarm config by name.

    Note: Docker API does not return the actual config data for security reasons.
    """
    access_token = os.environ.get("PORTAINER_ACCESS_TOKEN")
    if not access_token:
        click.echo(
            "Error: Missing PORTAINER_ACCESS_TOKEN environment variable", err=True
        )
        sys.exit(1)

    portainer_url = url.rstrip("/")

    config = find_config_by_name(portainer_url, access_token, endpoint_id, name)

    if config:
        click.echo(json.dumps(config, indent=2))
    else:
        click.echo(f"Error: Config '{name}' not found", err=True)
        sys.exit(1)


@cli.command("list")
@click.option("--url", "-u", required=True, help="Portainer base URL")
@click.option("--endpoint-id", "-e", type=int, default=1, help="Portainer endpoint ID")
def list_configs_cmd(url: str, endpoint_id: int):
    """List all Docker Swarm configs."""
    access_token = os.environ.get("PORTAINER_ACCESS_TOKEN")
    if not access_token:
        click.echo(
            "Error: Missing PORTAINER_ACCESS_TOKEN environment variable", err=True
        )
        sys.exit(1)

    portainer_url = url.rstrip("/")

    configs, status_code = list_configs(portainer_url, access_token, endpoint_id)

    if status_code != 200:
        click.echo(f"Error: Failed to list configs (HTTP {status_code})", err=True)
        if configs:
            click.echo(json.dumps(configs, indent=2), err=True)
        sys.exit(1)

    if not configs:
        click.echo("No configs found.")
        return

    click.echo(f"Found {len(configs)} config(s):\n")
    for config in configs:
        spec = config.get("Spec", {})
        config_id = config.get("ID", "unknown")
        config_name = spec.get("Name", "unknown")
        created = config.get("CreatedAt", "unknown")
        click.echo(f"  {config_name}")
        click.echo(f"    ID: {config_id}")
        click.echo(f"    Created: {created}")
        click.echo()


@cli.command("delete")
@click.option("--url", "-u", required=True, help="Portainer base URL")
@click.option("--name", "-n", required=True, help="Config name")
@click.option("--endpoint-id", "-e", type=int, default=1, help="Portainer endpoint ID")
def delete_config_cmd(url: str, name: str, endpoint_id: int):
    """Delete a Docker Swarm config by name."""
    access_token = os.environ.get("PORTAINER_ACCESS_TOKEN")
    if not access_token:
        click.echo(
            "Error: Missing PORTAINER_ACCESS_TOKEN environment variable", err=True
        )
        sys.exit(1)

    portainer_url = url.rstrip("/")

    config = find_config_by_name(portainer_url, access_token, endpoint_id, name)

    if not config:
        click.echo(f"Error: Config '{name}' not found", err=True)
        sys.exit(1)

    config_id = config.get("ID")
    click.echo(f"Deleting config: {name} (ID: {config_id})")

    _, status_code = delete_config(portainer_url, access_token, endpoint_id, config_id)

    if status_code in (200, 204):
        click.echo(f"✓ Config '{name}' deleted successfully")
    else:
        click.echo(f"Error: Failed to delete config (HTTP {status_code})", err=True)
        sys.exit(1)
