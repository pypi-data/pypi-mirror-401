"""NSYS Analyze - Parse and analyze .nsys-rep profile files.

This module provides the implementation for the `wafer nsys-analyze` command.
Supports both local analysis (when nsys is installed) and remote analysis via API.
"""

import json
import platform
import shutil
from datetime import datetime
from pathlib import Path


def _find_nsys() -> str | None:
    """Find nsys executable on the system."""
    nsys = shutil.which("nsys")
    if nsys:
        return nsys

    # Check common installation paths
    common_paths = [
        "/usr/bin/nsys",
        "/usr/local/cuda/bin/nsys",
        "/opt/nvidia/nsight-systems/bin/nsys",
    ]

    for path in common_paths:
        if Path(path).is_file():
            return path

    return None


def _get_install_command() -> str:
    """Get platform-appropriate install command."""
    system = platform.system().lower()

    if system == "linux":
        if shutil.which("apt-get") or shutil.which("apt"):
            return "sudo apt install nvidia-cuda-toolkit"
        elif shutil.which("dnf"):
            return "sudo dnf install nsight-systems"
        elif shutil.which("yum"):
            return "sudo yum install nsight-systems"

    if shutil.which("conda"):
        return "conda install -c nvidia nsight-systems"

    return "Download from https://developer.nvidia.com/nsight-systems"


def _generate_text_output(filename: str, result: dict) -> str:
    """Generate human-readable markdown text from analysis result."""
    assert filename, "filename must be non-empty"
    assert isinstance(result, dict), "result must be a dictionary"

    timestamp = datetime.now().isoformat()
    summary = result.get("summary", {})
    kernels = result.get("kernels", [])

    lines = [
        "# NSYS Profiling Analysis",
        f"Source: {filename}",
        f"Generated: {timestamp}",
        "",
        "## Summary",
        f"- GPU: {summary.get('gpu', 'Unknown')}",
        f"- Duration: {summary.get('duration_ms', 0):.2f} ms",
        f"- Kernel Count: {summary.get('kernel_count', 0)}",
        f"- Memory Transfers: {summary.get('memory_transfers', 0)}",
        "",
    ]

    if kernels:
        lines.extend([
            "## Kernels",
            "",
        ])
        for i, kernel in enumerate(kernels, 1):
            lines.extend([
                f"### {i}. {kernel.get('name', 'Unknown')}",
                f"- Duration: {kernel.get('duration_ms', 0):.3f} ms",
                f"- Grid Size: {kernel.get('grid_size', 'N/A')}",
                f"- Block Size: {kernel.get('block_size', 'N/A')}",
                f"- Memory Throughput: {kernel.get('memory_throughput_gb_s', 0):.2f} GB/s",
                "",
            ])

    # Add diagnostics if present
    diagnostics = result.get("diagnostics", [])
    if diagnostics:
        lines.extend([
            "## Diagnostics",
            "",
        ])
        for diag in diagnostics:
            level = diag.get("level", "Info")
            text = diag.get("text", "")
            lines.append(f"- [{level}] {text}")
        lines.append("")

    return "\n".join(lines)


def _analyze_remote_api(
    filepath: Path,
    json_output: bool = False,
) -> str:
    """Analyze NSYS profile remotely via wafer-api.

    Uploads the .nsys-rep file and runs analysis on Modal.
    """
    assert filepath.exists(), f"File must exist: {filepath}"
    assert filepath.suffix == ".nsys-rep", f"File must be .nsys-rep: {filepath}"

    import sys

    import httpx

    from .api_client import get_api_url
    from .auth import get_auth_headers

    api_url = get_api_url()
    headers = get_auth_headers()

    assert api_url, "API URL must be configured"

    # Use multipart/form-data upload
    print(f"Uploading {filepath.name} for analysis...", file=sys.stderr)

    try:
        with httpx.Client(timeout=300.0, headers=headers) as client:
            with open(filepath, "rb") as f:
                files = {"file": (filepath.name, f, "application/octet-stream")}
                data = {"filename": filepath.name}

                response = client.post(
                    f"{api_url}/v1/nsys/tool/analyze",
                    files=files,
                    data=data,
                )
                response.raise_for_status()
                result = response.json()

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise RuntimeError("Not authenticated. Run: wafer login") from e
        raise RuntimeError(f"API error: {e.response.status_code} - {e.response.text}") from e
    except httpx.RequestError as e:
        raise RuntimeError(f"Could not reach API: {e}") from e

    if not result.get("success", True):
        raise RuntimeError(f"Analysis failed: {result.get('error', 'Unknown error')}")

    # Validate response structure
    assert isinstance(result, dict), "API must return a dictionary"

    if json_output:
        return json.dumps(result, indent=2)
    else:
        return _generate_text_output(filepath.name, result)


def analyze_nsys_profile(
    filepath: Path,
    json_output: bool = False,
    remote: bool | None = None,
) -> str:
    """Analyze an NSYS profile file and return results.

    Args:
        filepath: Path to .nsys-rep file
        json_output: If True, return raw JSON; otherwise return formatted text
        remote: If True, force remote analysis via API. If False, force local.
                If None (default), auto-detect: use local if nsys available, else remote.

    Returns:
        Analysis results as string (JSON or markdown)

    Raises:
        FileNotFoundError: If file doesn't exist
        RuntimeError: If analysis fails
    """
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    if filepath.suffix != ".nsys-rep":
        raise ValueError(f"Expected .nsys-rep file, got: {filepath.suffix}")

    nsys_path = _find_nsys()

    # Determine whether to use local or remote
    use_remote = remote
    if use_remote is None:
        # Auto-detect: use remote if nsys not available locally
        use_remote = nsys_path is None

    if use_remote:
        return _analyze_remote_api(filepath, json_output)
    else:
        # Local analysis not yet implemented - would need to copy nsys_parser to wafer-core
        # For now, suggest using remote
        if nsys_path is None:
            install_cmd = _get_install_command()
            raise FileNotFoundError(
                f"NSYS not installed locally. Use --remote flag or install with: {install_cmd}"
            )

        # TODO: Implement local parsing by moving nsys_parser to wafer-core
        raise NotImplementedError(
            "Local NSYS analysis not yet implemented. Use --remote flag to analyze via API."
        )
