"""Workspaces CLI - Manage remote GPU workspaces.

This module provides the implementation for the `wafer workspaces` subcommand.
"""

import json
from pathlib import Path

import httpx

from .api_client import get_api_url
from .auth import get_auth_headers


def _get_client() -> tuple[str, dict[str, str]]:
    """Get API URL and auth headers."""
    api_url = get_api_url()
    headers = get_auth_headers()

    assert api_url, "API URL must be configured"
    assert api_url.startswith("http"), "API URL must be a valid HTTP(S) URL"

    return api_url, headers


def list_workspaces(json_output: bool = False) -> str:
    """List all workspaces for the current user.

    Args:
        json_output: If True, return raw JSON; otherwise return formatted text

    Returns:
        Workspaces list as string (JSON or formatted text)
    """
    api_url, headers = _get_client()

    try:
        with httpx.Client(timeout=30.0, headers=headers) as client:
            response = client.get(f"{api_url}/v1/workspaces")
            response.raise_for_status()
            workspaces = response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise RuntimeError("Not authenticated. Run: wafer login") from e
        raise RuntimeError(f"API error: {e.response.status_code} - {e.response.text}") from e
    except httpx.RequestError as e:
        raise RuntimeError(f"Could not reach API: {e}") from e

    # Validate API response shape
    assert isinstance(workspaces, list), "API must return a list of workspaces"

    if json_output:
        return json.dumps(workspaces, indent=2)

    if not workspaces:
        return "No workspaces found."

    lines = ["Workspaces:", ""]
    for ws in workspaces:
        status = ws.get("status", "unknown")
        status_icon = {"running": "●", "stopped": "○", "queued": "◐"}.get(status, "?")
        lines.append(f"  {status_icon} {ws['name']} ({ws['id']})")
        lines.append(f"    GPU: {ws.get('gpu_type', 'N/A')} | Image: {ws.get('image', 'N/A')}")
        lines.append(f"    Status: {status} | Created: {ws.get('created_at', 'N/A')}")
        lines.append("")

    return "\n".join(lines)


def create_workspace(
    name: str,
    gpu_type: str = "B200",
    image: str | None = None,
    json_output: bool = False,
) -> str:
    """Create a new workspace.

    Args:
        name: Workspace name
        gpu_type: GPU type (default: B200)
        image: Docker image (optional, uses default if not specified)
        json_output: If True, return raw JSON; otherwise return formatted text

    Returns:
        Created workspace info as string
    """
    # Validate inputs
    assert name, "Workspace name must be non-empty"
    assert gpu_type, "GPU type must be non-empty"

    api_url, headers = _get_client()

    request_body: dict = {
        "name": name,
        "gpu_type": gpu_type,
    }
    if image:
        request_body["image"] = image

    try:
        with httpx.Client(timeout=60.0, headers=headers) as client:
            response = client.post(f"{api_url}/v1/workspaces", json=request_body)
            response.raise_for_status()
            workspace = response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise RuntimeError("Not authenticated. Run: wafer login") from e
        if e.response.status_code == 400:
            raise RuntimeError(f"Bad request: {e.response.text}") from e
        raise RuntimeError(f"API error: {e.response.status_code} - {e.response.text}") from e
    except httpx.RequestError as e:
        raise RuntimeError(f"Could not reach API: {e}") from e

    # Validate API response has required fields
    assert "id" in workspace, "API response must contain workspace id"
    assert "name" in workspace, "API response must contain workspace name"

    if json_output:
        return json.dumps(workspace, indent=2)

    return f"Created workspace: {workspace['name']} ({workspace['id']})"


def delete_workspace(workspace_id: str, json_output: bool = False) -> str:
    """Delete a workspace.

    Args:
        workspace_id: Workspace ID to delete
        json_output: If True, return raw JSON; otherwise return formatted text

    Returns:
        Deletion status as string
    """
    assert workspace_id, "Workspace ID must be non-empty"

    api_url, headers = _get_client()

    try:
        with httpx.Client(timeout=30.0, headers=headers) as client:
            response = client.delete(f"{api_url}/v1/workspaces/{workspace_id}")
            response.raise_for_status()
            result = response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise RuntimeError("Not authenticated. Run: wafer login") from e
        if e.response.status_code == 404:
            raise RuntimeError(f"Workspace not found: {workspace_id}") from e
        raise RuntimeError(f"API error: {e.response.status_code} - {e.response.text}") from e
    except httpx.RequestError as e:
        raise RuntimeError(f"Could not reach API: {e}") from e

    if json_output:
        return json.dumps(result, indent=2)

    return f"Deleted workspace: {workspace_id}"


def attach_workspace(workspace_id: str, json_output: bool = False) -> str:
    """Attach to a workspace (get SSH credentials).

    Args:
        workspace_id: Workspace ID to attach to
        json_output: If True, return raw JSON; otherwise return formatted text

    Returns:
        SSH connection info as string
    """
    assert workspace_id, "Workspace ID must be non-empty"

    api_url, headers = _get_client()

    try:
        with httpx.Client(timeout=120.0, headers=headers) as client:
            response = client.post(f"{api_url}/v1/workspaces/{workspace_id}/attach")
            response.raise_for_status()
            attach_info = response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise RuntimeError("Not authenticated. Run: wafer login") from e
        if e.response.status_code == 404:
            raise RuntimeError(f"Workspace not found: {workspace_id}") from e
        if e.response.status_code == 503:
            raise RuntimeError("No GPU available. Please try again later.") from e
        raise RuntimeError(f"API error: {e.response.status_code} - {e.response.text}") from e
    except httpx.RequestError as e:
        raise RuntimeError(f"Could not reach API: {e}") from e

    # Validate API response has required SSH fields
    assert "ssh_host" in attach_info, "API response must contain ssh_host"
    assert "ssh_port" in attach_info, "API response must contain ssh_port"
    assert "ssh_user" in attach_info, "API response must contain ssh_user"
    assert "private_key_pem" in attach_info, "API response must contain private_key_pem"

    if json_output:
        return json.dumps(attach_info, indent=2)

    # Write private key to temp file and generate SSH config
    ssh_host = attach_info["ssh_host"]
    ssh_port = attach_info["ssh_port"]
    ssh_user = attach_info["ssh_user"]
    private_key = attach_info["private_key_pem"]

    # Validate field values before using them
    assert ssh_host, "ssh_host must be non-empty"
    assert isinstance(ssh_port, int), "ssh_port must be an integer"
    assert ssh_port > 0, "ssh_port must be positive"
    assert ssh_user, "ssh_user must be non-empty"
    assert private_key, "private_key_pem must be non-empty"

    # Save private key
    key_dir = Path.home() / ".wafer" / "keys"
    key_dir.mkdir(parents=True, exist_ok=True)
    key_path = key_dir / f"{workspace_id}.pem"
    key_path.write_text(private_key)
    key_path.chmod(0o600)

    # Generate SSH config entry
    config_entry = f"""
# Wafer workspace: {workspace_id}
Host wafer-{workspace_id}
    HostName {ssh_host}
    Port {ssh_port}
    User {ssh_user}
    IdentityFile {key_path}
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
"""

    lines = [
        f"Attached to workspace: {workspace_id}",
        "",
        "SSH Connection:",
        f"  ssh -i {key_path} -p {ssh_port} {ssh_user}@{ssh_host}",
        "",
        "Or add to ~/.ssh/config:",
        config_entry,
        f"Then connect with: ssh wafer-{workspace_id}",
    ]

    return "\n".join(lines)


def get_workspace(workspace_id: str, json_output: bool = False) -> str:
    """Get details of a specific workspace.

    Args:
        workspace_id: Workspace ID to get
        json_output: If True, return raw JSON; otherwise return formatted text

    Returns:
        Workspace details as string
    """
    assert workspace_id, "Workspace ID must be non-empty"

    api_url, headers = _get_client()

    try:
        with httpx.Client(timeout=30.0, headers=headers) as client:
            response = client.get(f"{api_url}/v1/workspaces/{workspace_id}")
            response.raise_for_status()
            workspace = response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise RuntimeError("Not authenticated. Run: wafer login") from e
        if e.response.status_code == 404:
            raise RuntimeError(f"Workspace not found: {workspace_id}") from e
        raise RuntimeError(f"API error: {e.response.status_code} - {e.response.text}") from e
    except httpx.RequestError as e:
        raise RuntimeError(f"Could not reach API: {e}") from e

    # Validate API response has required fields
    assert "id" in workspace, "API response must contain workspace id"
    assert "name" in workspace, "API response must contain workspace name"

    if json_output:
        return json.dumps(workspace, indent=2)

    lines = [
        f"Workspace: {workspace['name']} ({workspace['id']})",
        "",
        f"  Status: {workspace.get('status', 'unknown')}",
        f"  GPU Type: {workspace.get('gpu_type', 'N/A')}",
        f"  Image: {workspace.get('image', 'N/A')}",
        f"  Created: {workspace.get('created_at', 'N/A')}",
        f"  Last Used: {workspace.get('last_used_at', 'N/A')}",
    ]

    if workspace.get("ssh_host"):
        lines.extend([
            "",
            "SSH Info:",
            f"  Host: {workspace['ssh_host']}",
            f"  Port: {workspace.get('ssh_port', 22)}",
            f"  User: {workspace.get('ssh_user', 'root')}",
        ])

    return "\n".join(lines)
