"""
Common utility functions for Portainer API scripts.
"""

from __future__ import annotations

import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def api_request(
    url: str,
    api_key: str,
    method: str = "GET",
    data: dict | None = None,
) -> tuple[dict | list | None, int]:
    """Make an API request to Portainer."""
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
    }

    body = json.dumps(data).encode("utf-8") if data else None
    req = Request(url, data=body, headers=headers, method=method)

    try:
        with urlopen(req) as response:
            response_body = response.read().decode("utf-8")
            return json.loads(response_body) if response_body else None, response.status
    except HTTPError as e:
        response_body = e.read().decode("utf-8")
        try:
            return json.loads(response_body), e.code
        except json.JSONDecodeError:
            return {"error": response_body}, e.code
    except URLError as e:
        return {"error": str(e.reason)}, 0


def create_container(
    portainer_url: str,
    api_key: str,
    endpoint_id: int,
    config: dict,
) -> str | None:
    """Create a container and return its ID."""
    url = f"{portainer_url}/api/endpoints/{endpoint_id}/docker/containers/create"
    response, status_code = api_request(url, api_key, method="POST", data=config)

    if 200 <= status_code < 300 and response:
        return response.get("Id")
    else:
        print(f"Error creating container (HTTP {status_code}):")
        print(json.dumps(response, indent=2))
        return None


def pull_image(
    portainer_url: str,
    api_key: str,
    endpoint_id: int,
    image: str,
) -> bool:
    """Pull a Docker image."""
    from urllib.request import Request, urlopen
    from urllib.parse import quote

    url = f"{portainer_url}/api/endpoints/{endpoint_id}/docker/images/create?fromImage={quote(image)}"
    headers = {"X-API-Key": api_key}
    req = Request(url, data=b"", headers=headers, method="POST")

    try:
        with urlopen(req) as response:
            # Read streaming response (Docker sends progress updates)
            response.read()
            return response.status == 200
    except Exception:
        return False


def start_container(
    portainer_url: str,
    api_key: str,
    endpoint_id: int,
    container_id: str,
) -> bool:
    """Start a container."""
    url = f"{portainer_url}/api/endpoints/{endpoint_id}/docker/containers/{container_id}/start"
    _, status_code = api_request(url, api_key, method="POST")
    return 200 <= status_code < 300


def wait_container(
    portainer_url: str,
    api_key: str,
    endpoint_id: int,
    container_id: str,
) -> int:
    """Wait for a container to finish and return exit code."""
    url = f"{portainer_url}/api/endpoints/{endpoint_id}/docker/containers/{container_id}/wait"
    response, status_code = api_request(url, api_key, method="POST")

    if 200 <= status_code < 300 and response:
        return response.get("StatusCode", -1)
    return -1


def get_container_logs(
    portainer_url: str,
    api_key: str,
    endpoint_id: int,
    container_id: str,
) -> str:
    """Get container logs."""
    url = f"{portainer_url}/api/endpoints/{endpoint_id}/docker/containers/{container_id}/logs?stdout=true&stderr=true"

    headers = {"X-API-Key": api_key}
    req = Request(url, headers=headers, method="GET")

    try:
        with urlopen(req) as response:
            # Docker logs have stream headers, strip them
            raw_logs = response.read()
            # Simple cleanup - remove Docker stream headers (8 bytes each)
            logs = ""
            i = 0
            while i < len(raw_logs):
                if i + 8 <= len(raw_logs):
                    size = int.from_bytes(raw_logs[i + 4 : i + 8], "big")
                    if i + 8 + size <= len(raw_logs):
                        logs += raw_logs[i + 8 : i + 8 + size].decode(
                            "utf-8", errors="replace"
                        )
                        i += 8 + size
                        continue
                break
            return logs
    except Exception as e:
        return f"Error getting logs: {e}"


def remove_container(
    portainer_url: str,
    api_key: str,
    endpoint_id: int,
    container_id: str,
) -> bool:
    """Remove a container."""
    url = f"{portainer_url}/api/endpoints/{endpoint_id}/docker/containers/{container_id}?force=true"
    _, status_code = api_request(url, api_key, method="DELETE")
    return 200 <= status_code < 300


def find_container_by_name(
    portainer_url: str,
    api_key: str,
    endpoint_id: int,
    name_filter: str,
) -> str | None:
    """Find a running container by name filter and return its ID."""
    url = f'{portainer_url}/api/endpoints/{endpoint_id}/docker/containers/json?filters={{"name":["{name_filter}"]}}'
    response, status_code = api_request(url, api_key)

    if 200 <= status_code < 300 and isinstance(response, list) and len(response) > 0:
        return response[0].get("Id")
    return None


def get_network_id(
    portainer_url: str,
    api_key: str,
    endpoint_id: int,
    network_name: str,
) -> str | None:
    """Find a network by name and return its ID."""
    url = f'{portainer_url}/api/endpoints/{endpoint_id}/docker/networks?filters={{"name":["{network_name}"]}}'
    response, status_code = api_request(url, api_key)

    if 200 <= status_code < 300 and isinstance(response, list) and len(response) > 0:
        return response[0].get("Id")
    return None


def create_exec(
    portainer_url: str,
    api_key: str,
    endpoint_id: int,
    container_id: str,
    cmd: list[str],
) -> str | None:
    """Create an exec instance in a container and return the exec ID."""
    url = f"{portainer_url}/api/endpoints/{endpoint_id}/docker/containers/{container_id}/exec"
    config = {
        "AttachStdout": True,
        "AttachStderr": True,
        "Cmd": cmd,
    }
    response, status_code = api_request(url, api_key, method="POST", data=config)

    if 200 <= status_code < 300 and response:
        return response.get("Id")
    return None


def start_exec(
    portainer_url: str,
    api_key: str,
    endpoint_id: int,
    exec_id: str,
) -> tuple[int, str]:
    """Start an exec instance and return (exit_code, output)."""
    from urllib.request import Request, urlopen

    url = f"{portainer_url}/api/endpoints/{endpoint_id}/docker/exec/{exec_id}/start"
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
    }
    body = json.dumps({"Detach": False, "Tty": False}).encode("utf-8")
    req = Request(url, data=body, headers=headers, method="POST")

    try:
        with urlopen(req) as response:
            # Read raw output (has Docker stream headers like logs)
            raw_output = response.read()
            # Strip Docker stream headers
            output = ""
            i = 0
            while i < len(raw_output):
                if i + 8 <= len(raw_output):
                    size = int.from_bytes(raw_output[i + 4 : i + 8], "big")
                    if i + 8 + size <= len(raw_output):
                        output += raw_output[i + 8 : i + 8 + size].decode(
                            "utf-8", errors="replace"
                        )
                        i += 8 + size
                        continue
                break
    except Exception as e:
        return -1, f"Error: {e}"

    # Get exec exit code
    inspect_url = (
        f"{portainer_url}/api/endpoints/{endpoint_id}/docker/exec/{exec_id}/json"
    )
    inspect_resp, _ = api_request(inspect_url, api_key)
    exit_code = inspect_resp.get("ExitCode", -1) if inspect_resp else -1

    return exit_code, output


def run_ephemeral_container(
    portainer_url: str,
    api_key: str,
    endpoint_id: int,
    config: dict,
    pull: bool = True,
) -> tuple[int, str]:
    """Run an ephemeral container and return (exit_code, logs)."""
    image = config.get("Image")
    if pull and image:
        if not pull_image(portainer_url, api_key, endpoint_id, image):
            print(f"Warning: Failed to pull image {image}, trying to run anyway...")

    container_id = create_container(portainer_url, api_key, endpoint_id, config)
    if not container_id:
        return -1, "Failed to create container"

    try:
        if not start_container(portainer_url, api_key, endpoint_id, container_id):
            return -1, "Failed to start container"

        exit_code = wait_container(portainer_url, api_key, endpoint_id, container_id)
        logs = get_container_logs(portainer_url, api_key, endpoint_id, container_id)

        return exit_code, logs
    finally:
        remove_container(portainer_url, api_key, endpoint_id, container_id)
