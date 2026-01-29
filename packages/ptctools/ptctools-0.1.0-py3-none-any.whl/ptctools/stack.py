"""Stack management commands."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import click

from ptctools._portainer import api_request


def load_stack_env_file(env_path: Path) -> list[dict]:
    """Parse .env file into Portainer environment variable format."""
    env_vars = []

    if not env_path.exists():
        return env_vars

    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                name, value = line.split("=", 1)
                name = name.strip()
                if name:
                    env_vars.append({"name": name, "value": value})

    return env_vars


def get_swarm_id(portainer_url: str, api_key: str, endpoint_id: int) -> str | None:
    """Get swarm ID from the endpoint."""
    url = f"{portainer_url}/api/endpoints/{endpoint_id}/docker/swarm"
    swarm_info, status_code = api_request(url, api_key)

    if status_code == 200 and isinstance(swarm_info, dict):
        return swarm_info.get("ID")
    return None


def get_stack_id(portainer_url: str, api_key: str, stack_name: str) -> int | None:
    """Get stack ID by name, returns None if not found."""
    url = f"{portainer_url}/api/stacks"
    stacks, status_code = api_request(url, api_key)

    if status_code != 200 or not isinstance(stacks, list):
        return None

    for stack in stacks:
        if stack.get("Name") == stack_name:
            return stack.get("Id")
    return None


def get_user_teams(portainer_url: str, api_key: str) -> list[dict]:
    """Get teams that the current user belongs to."""
    url = f"{portainer_url}/api/users/me"
    user_info, status_code = api_request(url, api_key)

    if status_code != 200 or not user_info:
        return []

    user_id = user_info.get("Id")
    if not user_id:
        return []

    url = f"{portainer_url}/api/users/{user_id}/memberships"
    memberships, status_code = api_request(url, api_key)

    if status_code != 200 or not isinstance(memberships, list):
        return []

    teams = []
    for m in memberships:
        team_id = m.get("TeamID")
        if team_id:
            teams.append({"Id": team_id, "Name": f"Team {team_id}"})

    return teams


def create_stack(
    portainer_url: str,
    api_key: str,
    endpoint_id: int,
    stack_name: str,
    stack_content: str,
    env_vars: list[dict],
    swarm_id: str,
) -> bool:
    """Create a new stack in Portainer."""
    click.echo(f"Creating new stack: {stack_name}...")

    url = f"{portainer_url}/api/stacks/create/swarm/string?endpointId={endpoint_id}"
    data = {
        "name": stack_name,
        "stackFileContent": stack_content,
        "env": env_vars,
        "swarmID": swarm_id,
    }

    response, status_code = api_request(url, api_key, method="POST", data=data)

    if 200 <= status_code < 300:
        click.echo("Stack created successfully!")
        click.echo(json.dumps(response, indent=2))
        return True
    else:
        click.echo(f"Error creating stack (HTTP {status_code}):")
        click.echo(json.dumps(response, indent=2))
        return False


def update_stack(
    portainer_url: str,
    api_key: str,
    endpoint_id: int,
    stack_id: int,
    stack_name: str,
    stack_content: str,
    env_vars: list[dict],
) -> bool:
    """Update an existing stack in Portainer."""
    click.echo(f"Updating existing stack: {stack_name} (ID: {stack_id})...")

    url = f"{portainer_url}/api/stacks/{stack_id}?endpointId={endpoint_id}"
    data = {
        "stackFileContent": stack_content,
        "env": env_vars,
        "prune": True,
        "pullImage": True,
    }

    response, status_code = api_request(url, api_key, method="PUT", data=data)

    if 200 <= status_code < 300:
        click.echo("Stack updated successfully!")
        click.echo(json.dumps(response, indent=2))
        return True
    else:
        click.echo(f"Error updating stack (HTTP {status_code}):")
        click.echo(json.dumps(response, indent=2))
        return False


def update_resource_control(
    portainer_url: str,
    api_key: str,
    resource_control_id: int,
    public: bool = False,
    team_ids: list[int] | None = None,
    user_ids: list[int] | None = None,
) -> bool:
    """Update resource control with specified access settings."""
    url = f"{portainer_url}/api/resource_controls/{resource_control_id}"
    data = {
        "Public": public,
        "Teams": team_ids or [],
        "Users": user_ids or [],
    }

    _, status_code = api_request(url, api_key, method="PUT", data=data)
    return 200 <= status_code < 300


def create_resource_control(
    portainer_url: str,
    api_key: str,
    stack_id: int,
    public: bool = False,
    team_ids: list[int] | None = None,
    user_ids: list[int] | None = None,
) -> bool:
    """Create resource control for a stack with specified access settings."""
    url = f"{portainer_url}/api/resource_controls"
    data = {
        "Type": "stack",
        "ResourceID": str(stack_id),
        "Public": public,
        "Teams": team_ids or [],
        "Users": user_ids or [],
    }

    _, status_code = api_request(url, api_key, method="POST", data=data)
    return 200 <= status_code < 300


@click.group()
def cli():
    """Stack management commands."""
    pass


@cli.command()
@click.option("--url", "-u", required=True, help="Portainer base URL")
@click.option("--stack-name", "-n", required=True, help="Stack name")
@click.option(
    "--stack-file",
    "-f",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Path to compose file",
)
@click.option("--endpoint-id", "-e", type=int, default=1, help="Portainer endpoint ID")
@click.option(
    "--env-file", type=click.Path(path_type=Path), help="Path to stack .env file"
)
@click.option(
    "--ownership",
    type=click.Choice(["private", "team", "public"]),
    help="Access control",
)
@click.option("--team-id", "-t", type=int, help="Team ID for team ownership")
def deploy(
    url: str,
    stack_name: str,
    stack_file: Path,
    endpoint_id: int,
    env_file: Path | None,
    ownership: str | None,
    team_id: int | None,
):
    """Deploy or update a stack in Portainer."""
    access_token = os.environ.get("PORTAINER_ACCESS_TOKEN")
    if not access_token:
        click.echo(
            "Error: Missing PORTAINER_ACCESS_TOKEN environment variable", err=True
        )
        sys.exit(1)

    portainer_url = url.rstrip("/")
    stack_file = stack_file.resolve()
    env_file = env_file.resolve() if env_file else stack_file.parent / ".env"

    # Auto-detect team if needed
    if ownership == "team" and not team_id:
        user_teams = get_user_teams(portainer_url, access_token)
        if user_teams:
            team_id = user_teams[0]["Id"]
            click.echo(f"Auto-detected team: {user_teams[0]['Name']} (ID: {team_id})")
        else:
            click.echo(
                "Error: ownership=team but no team found and --team-id not specified",
                err=True,
            )
            sys.exit(1)

    stack_content = stack_file.read_text()
    env_vars = load_stack_env_file(env_file)

    click.echo(f"Portainer URL: {portainer_url}")
    click.echo(f"Stack Name: {stack_name}")
    click.echo(f"Stack File: {stack_file}")
    click.echo(f"Endpoint ID: {endpoint_id}")
    click.echo(f"Environment Variables: {len(env_vars)} loaded")
    if ownership:
        click.echo(f"Ownership: {ownership}")
        if ownership == "team":
            click.echo(f"Team ID: {team_id}")
    click.echo()

    # Check if stack exists
    click.echo("Checking if stack already exists...")
    existing_stack_id = get_stack_id(portainer_url, access_token, stack_name)

    if existing_stack_id is not None:
        success = update_stack(
            portainer_url,
            access_token,
            endpoint_id,
            existing_stack_id,
            stack_name,
            stack_content,
            env_vars,
        )
    else:
        click.echo("Getting swarm ID...")
        swarm_id = get_swarm_id(portainer_url, access_token, endpoint_id)
        if not swarm_id:
            click.echo("Error: Could not get swarm ID from endpoint", err=True)
            sys.exit(1)
        click.echo(f"Swarm ID: {swarm_id}")

        success = create_stack(
            portainer_url,
            access_token,
            endpoint_id,
            stack_name,
            stack_content,
            env_vars,
            swarm_id,
        )

    # Apply access control
    if success and ownership:
        click.echo()
        final_stack_id = get_stack_id(portainer_url, access_token, stack_name)
        if final_stack_id:
            stack_url = f"{portainer_url}/api/stacks/{final_stack_id}"
            stack_info, status_code = api_request(stack_url, access_token)
            if status_code == 200 and stack_info:
                rc = stack_info.get("ResourceControl")

                if ownership == "private":
                    if rc and rc.get("Id"):
                        user_url = f"{portainer_url}/api/users/me"
                        user_info, _ = api_request(user_url, access_token)
                        user_id = user_info.get("Id") if user_info else None
                        if user_id:
                            click.echo("Setting access control to private...")
                            if update_resource_control(
                                portainer_url,
                                access_token,
                                rc["Id"],
                                user_ids=[user_id],
                            ):
                                click.echo("✓ Access control set to private")
                            else:
                                click.echo("Warning: Failed to set private access")

                elif ownership == "team" and team_id:
                    click.echo(f"Setting access control for team {team_id}...")
                    if rc and rc.get("Id"):
                        if update_resource_control(
                            portainer_url, access_token, rc["Id"], team_ids=[team_id]
                        ):
                            click.echo(f"✓ Access control set to team {team_id}")
                        else:
                            click.echo("Warning: Failed to update access control")
                    else:
                        if create_resource_control(
                            portainer_url,
                            access_token,
                            final_stack_id,
                            team_ids=[team_id],
                        ):
                            click.echo(f"✓ Access control created for team {team_id}")
                        else:
                            click.echo("Warning: Failed to create access control")

                elif ownership == "public":
                    click.echo("Setting access control to public...")
                    if rc and rc.get("Id"):
                        if update_resource_control(
                            portainer_url, access_token, rc["Id"], public=True
                        ):
                            click.echo("✓ Access control set to public")
                        else:
                            click.echo("Warning: Failed to set public access")
                    else:
                        if create_resource_control(
                            portainer_url, access_token, final_stack_id, public=True
                        ):
                            click.echo("✓ Access control created as public")
                        else:
                            click.echo(
                                "Warning: Failed to create public access control"
                            )

    click.echo()
    click.echo("Done!" if success else "Failed!")
    sys.exit(0 if success else 1)
