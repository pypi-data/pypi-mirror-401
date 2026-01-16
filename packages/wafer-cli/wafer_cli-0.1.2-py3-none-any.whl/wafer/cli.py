"""Wafer CLI - Run commands on remote GPUs in Docker containers."""

import json
import sys
from pathlib import Path

import trio
import typer

from .config import WaferConfig, WaferEnvironment
from .inference import infer_upload_files, resolve_environment

app = typer.Typer(help="Run commands on remote GPUs in Docker containers")

# Subcommand group for target management (local TOML-based)
targets_app = typer.Typer(help="Manage local GPU targets (TOML files)")
app.add_typer(targets_app, name="targets")

# Subcommand group for workspace management (remote API-backed)
workspaces_app = typer.Typer(help="Manage remote GPU workspaces")
app.add_typer(workspaces_app, name="workspaces")

# Subcommand group for Perfetto trace analysis
perfetto_app = typer.Typer(help="Perfetto trace analysis and SQL queries")
app.add_typer(perfetto_app, name="perfetto")


@app.command()
def run(
    command: str = typer.Argument(..., help="Command to run in Docker container"),
    env: str | None = typer.Option(None, "--env", "-e", help="Environment name from config"),
    upload: list[str] | None = typer.Option(  # noqa: B008
        None, "--upload", "-u", help="Files to upload (default: auto-infer)"
    ),
    target: str | None = typer.Option(None, "--target", "-t", help="Override target from config"),
    follow: bool = typer.Option(True, "--follow/--no-follow", help="Stream output in real-time"),
    detach: bool = typer.Option(False, "--detach", "-d", help="Run in background, return job ID"),
) -> None:
    """Run command on remote GPU in Docker container.

    Examples:
        # Run with auto-inferred files and default environment
        wafer run "make && ./kernel_test"

        # Specify environment
        wafer run "python train.py" --env pytorch

        # Override target
        wafer run "nvcc kernel.cu -o kernel && ./kernel" --target root@other-node:22

        # Upload specific files
        wafer run "make" --upload kernel.cu --upload Makefile

        # Run in background
        wafer run "python train.py --epochs 100" --detach
    """
    # Load config
    config_path = Path.home() / ".wafer" / "config.toml"
    if not config_path.exists():
        typer.echo(f"Error: Config not found: {config_path}", err=True)
        typer.echo(
            "Create ~/.wafer/config.toml with your settings. See documentation for format.",
            err=True,
        )
        raise typer.Exit(1)

    try:
        config = WaferConfig.from_toml(config_path)
    except (AssertionError, ValueError, KeyError) as e:
        typer.echo(f"Error: Invalid config: {e}", err=True)
        raise typer.Exit(1) from None

    # Resolve environment
    try:
        environment = resolve_environment(config, env)
    except (ValueError, AssertionError) as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from None

    # Determine files to upload
    cwd = Path.cwd()
    if upload:
        files_to_upload = [cwd / f for f in upload]
        # Validate files exist
        for f in files_to_upload:
            if not f.exists():
                typer.echo(f"Error: File not found: {f}", err=True)
                raise typer.Exit(1)
            if not f.is_file():
                typer.echo(f"Error: Not a file: {f}", err=True)
                raise typer.Exit(1)
    else:
        try:
            files_to_upload = infer_upload_files(command, cwd)
        except (AssertionError, ValueError) as e:
            typer.echo(f"Error: Failed to infer files: {e}", err=True)
            raise typer.Exit(1) from None

    # Use target override if provided
    effective_target = target or config.target

    # Run async implementation
    try:
        trio.run(
            _run_async,
            effective_target,
            config.ssh_key,
            environment,
            command,
            files_to_upload,
            follow,
            detach,
        )
    except KeyboardInterrupt:
        typer.echo("\nInterrupted by user", err=True)
        raise typer.Exit(130) from None
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from None


async def _run_async(
    target: str,
    ssh_key: str,
    environment: WaferEnvironment,
    command: str,
    files_to_upload: list[Path],
    follow: bool,
    detach: bool,
) -> None:
    """Async wrapper for run command (runs sync SSH client in thread).

    Args:
        target: SSH target string (user@host:port)
        ssh_key: Path to SSH key
        environment: Environment configuration with Docker image
        command: Command to execute
        files_to_upload: List of files to upload
        follow: Whether to stream output
        detach: Whether to run in background

    Raises:
        Exception: On any execution failure
    """
    import trio

    await trio.to_thread.run_sync(
        lambda: _run_sync(target, ssh_key, environment, command, files_to_upload, follow, detach)
    )


def _run_sync(
    target: str,
    ssh_key: str,
    environment: WaferEnvironment,
    command: str,
    files_to_upload: list[Path],
    follow: bool,
    detach: bool,
) -> None:
    """Sync implementation of run command using internal SSHClient.

    Args:
        target: SSH target string (user@host:port)
        ssh_key: Path to SSH key
        environment: Environment configuration with Docker image
        command: Command to execute
        files_to_upload: List of files to upload
        follow: Whether to stream output
        detach: Whether to run in background

    Raises:
        Exception: On any execution failure
    """

    from wafer_core.ssh import SSHClient

    workspace_name = Path.cwd().name
    remote_workspace = f"~/.wafer/workspaces/{workspace_name}"

    client = SSHClient(target, ssh_key)

    # Ensure workspace directory exists
    print(f"Setting up workspace: {remote_workspace}")
    client.exec(f"mkdir -p {remote_workspace}")

    # Upload files
    if files_to_upload:
        print(f"Uploading {len(files_to_upload)} files...")
        for f in files_to_upload:
            remote_path = f"{remote_workspace}/{f.name}"
            client.upload_files(str(f), remote_path)
            print(f"  ✓ {f.name}")
    else:
        print("No files to upload (use --upload to specify)")

    # Expand workspace path for volume mount
    expanded_workspace = client.expand_path(remote_workspace)

    print(f"\nEnvironment: {environment.docker}")
    if environment.description:
        print(f"Description: {environment.description}")
    print(f"Command: {command}")
    print("-" * 60)

    # Check if Docker is available
    docker_check = client.exec("which docker")
    if docker_check.exit_code != 0:
        raise RuntimeError(
            "Docker not found on remote machine. Please install Docker with GPU support."
        )

    # Build docker command
    docker_cmd = _build_docker_run_cmd(
        image=environment.docker,
        inner_cmd=command,
        volumes={expanded_workspace: "/workspace"},
        working_dir="/workspace",
    )

    # Execute
    if follow and not detach:
        # Stream output in real-time
        try:
            for line in client.exec_stream(docker_cmd):
                print(line)
        except Exception as e:
            print(f"\nExecution failed: {e}", file=sys.stderr)
            raise
    else:
        # Non-streaming execution
        result = client.exec(docker_cmd)

        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

        # Check exit code
        if result.exit_code != 0:
            print(
                f"\nCommand exited with code {result.exit_code}",
                file=sys.stderr,
            )
            raise typer.Exit(result.exit_code)


def _build_docker_run_cmd(
    image: str,
    inner_cmd: str,
    volumes: dict[str, str],
    working_dir: str,
    gpu_id: int = 0,
) -> str:
    """Build docker run command string."""
    import shlex

    parts = ["docker", "run", "--rm"]
    parts.extend(["--gpus", f"'device={gpu_id}'"])

    for host_path, container_path in volumes.items():
        parts.extend(["-v", f"{host_path}:{container_path}"])

    parts.extend(["-w", working_dir])
    parts.append(image)
    parts.append(f"bash -c {shlex.quote(inner_cmd)}")

    return " ".join(parts)


@app.command()
def status(job_id: str = typer.Argument(..., help="Job ID to check")) -> None:
    """Get status of a running job."""
    # TODO: Implement in Phase 3
    typer.echo(f"Status for job {job_id}: not yet implemented")
    typer.echo("Job persistence will be added in Phase 3")


@app.command()
def logs(
    job_id: str = typer.Argument(..., help="Job ID"),
    follow_logs: bool = typer.Option(False, "--follow", "-f", help="Follow log output"),
) -> None:
    """Get logs from a job."""
    # TODO: Implement in Phase 3
    typer.echo(f"Logs for job {job_id}: not yet implemented")
    typer.echo("Job persistence will be added in Phase 3")


@app.command()
def kill(job_id: str = typer.Argument(..., help="Job ID to kill")) -> None:
    """Kill a running job."""
    # TODO: Implement in Phase 3
    typer.echo(f"Kill job {job_id}: not yet implemented")
    typer.echo("Job persistence will be added in Phase 3")


@app.command()
def config_show() -> None:
    """Show current configuration."""
    config_path = Path.home() / ".wafer" / "config.toml"
    if not config_path.exists():
        typer.echo(f"Error: Config not found: {config_path}", err=True)
        raise typer.Exit(1)

    try:
        config = WaferConfig.from_toml(config_path)
        typer.echo(f"Target: {config.target}")
        typer.echo(f"SSH Key: {config.ssh_key}")
        typer.echo(f"Default Environment: {config.default_environment or '(none)'}")
        typer.echo("\nEnvironments:")
        for name, env in config.environments.items():
            typer.echo(f"  {name}:")
            typer.echo(f"    Docker: {env.docker}")
            if env.description:
                typer.echo(f"    Description: {env.description}")
    except Exception as e:
        typer.echo(f"Error reading config: {e}", err=True)
        raise typer.Exit(1) from None


@app.command()
def wevin(
    prompt: str | None = typer.Argument(
        None,
        help="Prompt to send (reads from stdin if not provided and not interactive)",
    ),
    interactive: bool = typer.Option(
        False,
        "--interactive",
        "-i",
        help="Launch interactive TUI mode",
    ),
    resume: str | None = typer.Option(
        None,
        "--resume",
        "-r",
        help="Resume session by ID (or 'last' for most recent)",
    ),
    from_turn: int | None = typer.Option(
        None,
        "--from-turn",
        help="Branch from specific turn (default: resume from end)",
    ),
    list_sessions: bool = typer.Option(
        False,
        "--list-sessions",
        help="List recent sessions and exit",
    ),
    tools: str | None = typer.Option(
        None,
        "--tools",
        help="Comma-separated list of tools to enable (default: all)",
    ),
    allow_spawn: bool = typer.Option(
        False,
        "--allow-spawn",
        help="Allow wafer tool to spawn sub-wevin agents (blocked by default)",
    ),
    max_tool_fails: int | None = typer.Option(
        None,
        "--max-tool-fails",
        help="Exit after N consecutive tool failures",
    ),
    max_turns: int | None = typer.Option(
        None,
        "--max-turns",
        help="Max conversation turns (default: 10)",
    ),
    model: str | None = typer.Option(
        None,
        "--model",
        "-m",
        help="Model override (default: claude-sonnet-4-5)",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output in JSON format (stream-json style)",
    ),
    # Legacy kernel optimization options (hidden, for backwards compat)
    problem: Path | None = typer.Option(
        None,
        "--problem",
        hidden=True,
        help="[Legacy] Path to problem YAML config file",
    ),
    reference: Path | None = typer.Option(
        None,
        "--reference",
        "--ref",
        hidden=True,
        help="[Legacy] Path to reference kernel file",
    ),
    description: str | None = typer.Option(
        None,
        "--description",
        "--desc",
        hidden=True,
        help="[Legacy] Problem description",
    ),
    test: list[str] | None = typer.Option(
        None,
        "--test",
        "-t",
        hidden=True,
        help="[Legacy] Test case",
    ),
    benchmark: list[str] | None = typer.Option(
        None,
        "--benchmark",
        "-b",
        hidden=True,
        help="[Legacy] Benchmark case",
    ),
    speedup_target: float | None = typer.Option(
        None,
        "--speedup",
        hidden=True,
        help="[Legacy] Speedup target",
    ),
) -> None:
    """Wevin - GPU programming assistant.

    By default, runs in one-shot mode: answer the prompt and exit.
    Use -i/--interactive for full TUI mode.

    Examples:
        # One-shot query
        wafer wevin "What is TMEM in CuTeDSL?"

        # Pipe from stdin
        cat kernel.py | wafer wevin "optimize this kernel"

        # JSON output for scripting
        wafer wevin "explain shared memory" --json

        # Interactive TUI
        wafer wevin -i

        # Resume a session
        wafer wevin --resume last "follow up question"

        # Limit tools
        wafer wevin --tools read,wafer "What is TMEM?"

        # Legacy kernel optimization mode
        wafer wevin --problem my_kernel.yaml
    """
    from wafer.wevin_cli import main as wevin_main

    # Read from stdin if no prompt and not interactive
    actual_prompt = prompt
    if not actual_prompt and not interactive and not sys.stdin.isatty():
        actual_prompt = sys.stdin.read().strip()

    wevin_main(
        prompt=actual_prompt,
        interactive=interactive,
        problem=str(problem) if problem else None,
        reference=str(reference) if reference else None,
        description=description,
        tests=list(test) if test else None,
        benchmarks=list(benchmark) if benchmark else None,
        model=model,
        max_turns=max_turns,
        speedup_target=speedup_target,
        resume=resume,
        from_turn=from_turn,
        list_sessions=list_sessions,
        tools=tools.split(",") if tools else None,
        allow_spawn=allow_spawn,
        max_tool_fails=max_tool_fails,
        json_output=json_output,
    )


# =============================================================================
# Evaluate command
# =============================================================================


@app.command()
def evaluate(
    implementation: Path = typer.Option(
        ..., "--implementation", "--impl", help="Path to implementation kernel file"
    ),
    reference: Path = typer.Option(..., "--reference", help="Path to reference kernel file"),
    test_cases: Path = typer.Option(..., "--test-cases", help="Path to test cases JSON file"),
    target: str | None = typer.Option(None, "--target", "-t", help="Target name (or uses default)"),
    benchmark: bool = typer.Option(False, "--benchmark", help="Run performance benchmarks"),
    profile: bool = typer.Option(False, "--profile", help="Enable profiling"),
    sync_artifacts: bool = typer.Option(
        True, "--sync-artifacts/--no-sync-artifacts", help="Download artifacts"
    ),
    gpu_id: int | None = typer.Option(None, "--gpu-id", help="Override GPU ID"),
) -> None:
    """Run kernel evaluation on a remote GPU target.

    Same interface as evaluate.py, but runs remotely.

    Examples:
        wafer evaluate --impl kernel.py --reference ref.py --test-cases tests.json

        wafer evaluate --impl kernel.py --reference ref.py --test-cases tests.json \\
            --target vultr-b200 --benchmark
    """
    from .evaluate import EvaluateArgs, run_evaluate

    args = EvaluateArgs(
        implementation=implementation,
        reference=reference,
        test_cases=test_cases,
        target_name=target or "",
        benchmark=benchmark,
        profile=profile,
        sync_artifacts=sync_artifacts,
        gpu_id=gpu_id,
    )

    try:
        # Use trio_asyncio to run async code that uses both trio and asyncio
        # (AsyncSSHClient uses asyncssh which is asyncio-based, bridged via trio_asyncio)
        import trio_asyncio

        result = trio_asyncio.run(run_evaluate, args)
    except KeyboardInterrupt:
        typer.echo("\nInterrupted by user", err=True)
        raise typer.Exit(130) from None
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from None

    # Print results
    if result.success:
        typer.echo("")
        typer.echo("=" * 60)
        status = "PASS" if result.all_correct else "FAIL"
        typer.echo(f"Result: {status}")
        score_pct = f"{result.correctness_score:.1%}"
        typer.echo(f"Correctness: {result.passed_tests}/{result.total_tests} ({score_pct})")
        if result.geomean_speedup > 0:
            typer.echo(f"Speedup: {result.geomean_speedup:.2f}x")
        if result.artifact_path:
            typer.echo(f"Artifacts: {result.artifact_path}")
        typer.echo("=" * 60)

        if not result.all_correct:
            raise typer.Exit(1)
    else:
        typer.echo(f"Error: {result.error_message}", err=True)
        raise typer.Exit(1)


# =============================================================================
# Push and Remote-Run commands
# =============================================================================


@app.command("push")
def push(
    local_path: Path = typer.Argument(..., help="Local directory to upload"),
    workspace: str | None = typer.Option(None, "--workspace", "-w", help="Workspace name override"),
    direct: bool = typer.Option(False, "--direct", "-d", help="Use direct SSH instead of API"),
    target_name: str | None = typer.Option(
        None, "--target", "-t", help="Target name (for --direct mode)"
    ),
) -> None:
    """Push directory to remote GPU.

    By default, uses wafer-api. Use --direct for direct SSH mode.

    Examples:
        wafer push ./my_project
        wafer push . --workspace my-kernel
        wafer push ./my_project --direct --target vultr-b200
    """
    # Validate path
    if not local_path.exists():
        typer.echo(f"Error: Path not found: {local_path}", err=True)
        raise typer.Exit(1)

    if not local_path.is_dir():
        typer.echo(f"Error: Not a directory: {local_path}", err=True)
        raise typer.Exit(1)

    # Resolve to absolute path
    local_path = local_path.resolve()

    if direct:
        # Direct SSH mode (requires target)
        if not target_name:
            typer.echo("Error: --target required for --direct mode", err=True)
            raise typer.Exit(1)

        from .gpu_run import push_directory as push_direct
        from .targets import load_target

        try:
            target = load_target(target_name)
        except FileNotFoundError:
            typer.echo(f"Error: Target not found: {target_name}", err=True)
            typer.echo("List targets with: wafer targets list", err=True)
            raise typer.Exit(1) from None

        typer.echo(f"Connecting to {target.ssh_target}...")
        try:
            result = push_direct(local_path, target)
        except Exception as e:
            typer.echo(f"Error: {e}", err=True)
            raise typer.Exit(1) from None

        typer.echo(f"Uploading {len(result.files_uploaded)} files to {result.workspace_path}")
        for f in result.files_uploaded:
            typer.echo(f"  ✓ {f}")
        typer.echo(f"Pushed to: {result.workspace_path}")
    else:
        # API mode (default)
        from .api_client import push_directory as push_api

        workspace_name = workspace or local_path.name
        typer.echo(f"Pushing {local_path.name} to wafer-api...")

        try:
            result = push_api(local_path, workspace_name)
        except Exception as e:
            typer.echo(f"Error: {e}", err=True)
            raise typer.Exit(1) from None

        typer.echo(f"Uploaded {len(result.files_uploaded)} files")
        for f in result.files_uploaded:
            typer.echo(f"  ✓ {f}")
        typer.echo(f"Workspace ID: {result.workspace_id}")


def _run_direct_mode(
    cmd_str: str,
    target_name: str,
    upload_dir: Path | None,
    workspace_id: str | None,
    gpu_id: int | None,
) -> int:
    """Run command via direct SSH mode. Returns exit code."""
    from .gpu_run import push_directory as push_direct
    from .gpu_run import run_command as run_direct
    from .targets import load_target

    try:
        target = load_target(target_name)
    except FileNotFoundError:
        typer.echo(f"Error: Target not found: {target_name}", err=True)
        typer.echo("List targets with: wafer targets list", err=True)
        raise typer.Exit(1) from None

    if not target.docker_image:
        typer.echo(f"Error: Target '{target_name}' has no docker_image configured", err=True)
        raise typer.Exit(1)

    # If upload_dir provided, push first
    workspace_name = workspace_id
    if upload_dir:
        typer.echo(f"Uploading {upload_dir.name}...")
        try:
            push_result = push_direct(upload_dir, target)
            workspace_name = push_result.workspace_path
            typer.echo(f"Uploaded {len(push_result.files_uploaded)} files")
        except Exception as e:
            typer.echo(f"Error uploading: {e}", err=True)
            raise typer.Exit(1) from None
    elif not workspace_name:
        workspace_name = "tmp"

    effective_gpu = gpu_id if gpu_id is not None else target.gpu_ids[0]
    typer.echo(f"Target: {target_name} (docker: {target.docker_image})")
    typer.echo(f"Workspace: {workspace_name}")
    typer.echo(f"GPU: {effective_gpu}")
    typer.echo(f"Command: {cmd_str}")
    typer.echo("-" * 60)

    try:
        return run_direct(cmd_str, workspace_name, target, gpu_id)
    except KeyboardInterrupt:
        typer.echo("\nInterrupted by user", err=True)
        raise typer.Exit(130) from None
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from None


def _run_api_mode(
    cmd_str: str,
    upload_dir: Path | None,
    workspace_id: str | None,
    gpu_id: int | None,
    docker_image: str | None,
    docker_entrypoint: str | None,
    pull_image: bool,
    require_hwc: bool,
) -> int:
    """Run command via wafer-api. Returns exit code."""
    from .api_client import run_command_stream

    if upload_dir:
        typer.echo(f"Uploading: {upload_dir}")
    elif workspace_id:
        typer.echo(f"Workspace: {workspace_id}")
    if gpu_id is not None:
        typer.echo(f"GPU: {gpu_id}")
    if docker_image:
        typer.echo(f"Image: {docker_image}")
    if docker_entrypoint:
        typer.echo(f"Entrypoint: {docker_entrypoint}")
    if pull_image:
        typer.echo("Pull image: yes")
    typer.echo(f"Command: {cmd_str}")
    if require_hwc:
        typer.echo("Hardware counters: required (baremetal)")
    typer.echo("-" * 60)

    try:
        return run_command_stream(
            command=cmd_str,
            upload_dir=upload_dir,
            workspace_id=workspace_id,
            gpu_id=gpu_id,
            docker_image=docker_image,
            docker_entrypoint=docker_entrypoint,
            pull_image=pull_image,
            require_hardware_counters=require_hwc,
        )
    except KeyboardInterrupt:
        typer.echo("\nInterrupted by user", err=True)
        raise typer.Exit(130) from None
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from None


@app.command("remote-run")
def remote_run(  # noqa: PLR0913
    command: list[str] = typer.Argument(..., help="Command to run"),
    upload_dir: Path | None = typer.Option(
        None, "--upload-dir", "-u", help="Directory to upload (stateless mode)"
    ),
    workspace_id: str | None = typer.Option(
        None, "--workspace-id", "-w", help="Workspace ID (from wafer push)"
    ),
    gpu_id: int | None = typer.Option(None, "--gpu", "-g", help="GPU ID"),
    docker_image: str | None = typer.Option(None, "--image", "-i", help="Docker image override"),
    docker_entrypoint: str | None = typer.Option(
        None, "--docker-entrypoint", help="Override Docker entrypoint (e.g., 'bash')"
    ),
    pull_image: bool = typer.Option(
        False, "--pull-image", help="Pull image if not available on target"
    ),
    require_hwc: bool = typer.Option(
        False, "--require-hwc", help="Require hardware counters (baremetal)"
    ),
    direct: bool = typer.Option(False, "--direct", "-d", help="Use direct SSH instead of API"),
    target_name: str | None = typer.Option(
        None, "--target", "-t", help="Target name (for --direct mode)"
    ),
) -> None:
    """Run command on remote GPU in Docker.

    Two modes:
    - High-level (stateless): --upload-dir uploads files and runs command
    - Low-level: --workspace-id uses existing workspace from 'wafer push'

    By default, uses wafer-api. Use --direct for direct SSH mode.

    Examples:
        # Stateless: upload and run
        wafer remote-run --upload-dir ./my_project -- python train.py

        # Run without files
        wafer remote-run -- nvidia-smi

        # Low-level: use existing workspace
        wafer remote-run --workspace-id ws_abc123 -- python train.py

        # Direct SSH mode
        wafer remote-run --upload-dir ./my_project --direct --target vultr-b200 -- python train.py
    """
    cmd_str = " ".join(command)
    if not cmd_str.strip():
        typer.echo("Error: Empty command", err=True)
        raise typer.Exit(1)

    if upload_dir and workspace_id:
        typer.echo("Error: --upload-dir and --workspace-id are mutually exclusive", err=True)
        raise typer.Exit(1)

    if upload_dir:
        if not upload_dir.exists():
            typer.echo(f"Error: Directory not found: {upload_dir}", err=True)
            raise typer.Exit(1)
        if not upload_dir.is_dir():
            typer.echo(f"Error: Not a directory: {upload_dir}", err=True)
            raise typer.Exit(1)
        upload_dir = upload_dir.resolve()

    if direct:
        if not target_name:
            typer.echo("Error: --target required for --direct mode", err=True)
            raise typer.Exit(1)
        exit_code = _run_direct_mode(cmd_str, target_name, upload_dir, workspace_id, gpu_id)
    else:
        exit_code = _run_api_mode(
            cmd_str,
            upload_dir,
            workspace_id,
            gpu_id,
            docker_image,
            docker_entrypoint,
            pull_image,
            require_hwc,
        )

    raise typer.Exit(exit_code)


# =============================================================================
# Authentication commands
# =============================================================================


@app.command("login")
def login(
    token: str | None = typer.Option(
        None, "--token", "-t", help="Access token (skip browser OAuth)"
    ),
) -> None:
    """Authenticate CLI with wafer-api via GitHub OAuth.

    Opens browser for GitHub authentication. Use --token to skip browser.

    Examples:
        wafer login              # opens browser for GitHub OAuth
        wafer login --token xyz  # use existing token
    """
    import httpx

    from .auth import browser_login, save_credentials, verify_token

    # Browser OAuth if no token provided
    if token is None:
        try:
            token = browser_login()
        except TimeoutError as e:
            typer.echo(f"Error: {e}", err=True)
            raise typer.Exit(1) from None
        except RuntimeError as e:
            typer.echo(f"Error: {e}", err=True)
            raise typer.Exit(1) from None
        except KeyboardInterrupt:
            typer.echo("\nCancelled", err=True)
            raise typer.Exit(1) from None

    if not token.strip():
        typer.echo("Error: Token cannot be empty", err=True)
        raise typer.Exit(1)

    token = token.strip()

    # Verify token with API
    typer.echo("Verifying token...")
    try:
        user_info = verify_token(token)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            typer.echo("Error: Invalid token", err=True)
        else:
            typer.echo(f"Error: API returned {e.response.status_code}", err=True)
        raise typer.Exit(1) from None
    except httpx.RequestError as e:
        typer.echo(f"Error: Could not reach API: {e}", err=True)
        raise typer.Exit(1) from None

    # Save credentials
    save_credentials(token, user_info.email)

    if user_info.email:
        typer.echo(f"Logged in as {user_info.email}")
    else:
        typer.echo(f"Logged in (user_id: {user_info.user_id})")
    typer.echo("Token saved to ~/.wafer/credentials.json")


@app.command("logout")
def logout() -> None:
    """Remove stored credentials."""
    from .auth import clear_credentials

    if clear_credentials():
        typer.echo("Logged out. Credentials removed.")
    else:
        typer.echo("Not logged in (no credentials found).")


@app.command("whoami")
def whoami() -> None:
    """Show current authenticated user."""
    from .auth import load_credentials

    creds = load_credentials()
    if creds is None:
        typer.echo("Not logged in. Run: wafer login")
        raise typer.Exit(1)

    if creds.email:
        typer.echo(creds.email)
    else:
        typer.echo("Logged in (email not available)")


@app.command("guide")
def guide() -> None:
    """Show the Wafer CLI usage guide.

    Displays a comprehensive guide covering:
    - Common workflows for kernel profiling and optimization
    - NCU/NSYS/Perfetto analysis commands
    - Understanding NCU recommendations
    - Workspace and target management
    """
    guide_path = Path(__file__).parent / "GUIDE.md"
    if not guide_path.exists():
        typer.echo("Error: GUIDE.md not found", err=True)
        raise typer.Exit(1)

    content = guide_path.read_text()
    typer.echo(content)


# =============================================================================
# Ask-docs command
# =============================================================================


@app.command("ask-docs")
def ask_docs(
    query: str = typer.Argument(..., help="Question about GPU programming/documentation"),
    session_id: str | None = typer.Option(
        None,
        "--session-id",
        "-s",
        help="Session ID for follow-up questions (returned from previous query)",
    ),
    docs_url: str = typer.Option(
        "https://www.api.wafer.ai",
        "--docs-url",
        envvar="WAFER_DOCS_URL",
        help="URL of docs-tool service",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output raw JSON events instead of streaming text",
    ),
) -> None:
    """Query GPU documentation using the docs-tool service.

    NOTE: Requires docs-tool service to be running locally:
        cd services/docs-tool && uv run uvicorn src.main:app --reload

    Examples:
        # Ask a question (requires local docs-tool)
        wafer ask-docs "What is TMEM in CuTeDSL?"

        # Follow-up question using session ID
        wafer ask-docs "How do I use it for fp4?" --session-id abc123
    """
    import httpx

    url = f"{docs_url.rstrip('/')}/v1/docs/rag/stream"
    payload = {"query": query}
    # Note: session_id not yet supported by /v1/docs/rag/stream endpoint
    # TODO: Add conversation_history support for follow-up questions

    try:
        with httpx.Client(timeout=120.0) as client:
            with client.stream("POST", url, json=payload) as response:
                if response.status_code != 200:
                    # Read the error response body
                    error_body = response.read().decode("utf-8", errors="replace")
                    typer.echo(f"Error: {response.status_code} - {error_body}", err=True)
                    raise typer.Exit(1)

                current_session_id = None
                for line in response.iter_lines():
                    if not line.startswith("data: "):
                        continue

                    try:
                        event = json.loads(line[6:])  # Skip "data: " prefix
                    except json.JSONDecodeError:
                        continue

                    if json_output:
                        typer.echo(json.dumps(event))
                        continue

                    # Handle different event types
                    event_type = event.get("type", "")

                    if event_type == "sources":
                        # Optionally show sources
                        pass
                    elif event_type == "chunk":
                        # Stream text to stdout
                        text = event.get("text", "")
                        if text:
                            sys.stdout.write(text)
                            sys.stdout.flush()
                    elif event_type == "done":
                        # Final chunk - get session ID for follow-ups
                        text = event.get("text", "")
                        if text:
                            sys.stdout.write(text)
                            sys.stdout.flush()
                        current_session_id = event.get("session_id")

                # Print newline and session info
                if not json_output:
                    print()  # Final newline
                    if current_session_id:
                        typer.echo(
                            f"\n[Session: {current_session_id}] "
                            f"Use --session-id {current_session_id} for follow-up questions",
                            err=True,
                        )

    except httpx.ConnectError:
        typer.echo(
            f"Error: Could not connect to docs-tool at {docs_url}\n"
            "Make sure the docs-tool service is running:\n"
            "  cd services/docs-tool && uv run uvicorn src.main:app --reload",
            err=True,
        )
        raise typer.Exit(1)
    except httpx.TimeoutException:
        typer.echo("Error: Request timed out", err=True)
        raise typer.Exit(1)


# =============================================================================
# Targets subcommands
# =============================================================================


@targets_app.command("add")
def targets_add(
    file_path: Path = typer.Argument(..., help="Path to target TOML file"),
) -> None:
    """Add a target from a TOML config file.

    Example:
        wafer targets add ~/configs/modal-b200.toml
    """
    from .targets import add_target_from_file, get_target_info

    try:
        target = add_target_from_file(file_path)
        typer.echo(f"Added target: {target.name}")
        info = get_target_info(target)
        for key, value in info.items():
            typer.echo(f"  {key}: {value}")
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from None
    except (ValueError, AssertionError) as e:
        typer.echo(f"Error: Invalid target config: {e}", err=True)
        raise typer.Exit(1) from None


@targets_app.command("list")
def targets_list() -> None:
    """List all configured targets.

    Example:
        wafer targets list
    """
    from .targets import get_default_target, list_targets

    targets = list_targets()
    default = get_default_target()

    if not targets:
        typer.echo("No targets configured.")
        typer.echo("Add one with: wafer targets add <path/to/target.toml>")
        return

    typer.echo("Configured targets:")
    for name in targets:
        marker = " (default)" if name == default else ""
        typer.echo(f"  {name}{marker}")


@targets_app.command("show")
def targets_show(
    name: str = typer.Argument(..., help="Target name"),
) -> None:
    """Show details for a target.

    Example:
        wafer targets show modal-b200
    """
    from .targets import get_target_info, load_target

    try:
        target = load_target(name)
        typer.echo(f"Target: {name}")
        info = get_target_info(target)
        for key, value in info.items():
            typer.echo(f"  {key}: {value}")
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from None


@targets_app.command("remove")
def targets_remove(
    name: str = typer.Argument(..., help="Target name"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
) -> None:
    """Remove a target.

    Example:
        wafer targets remove modal-b200
    """
    from .targets import remove_target

    if not force:
        confirm = typer.confirm(f"Remove target '{name}'?")
        if not confirm:
            typer.echo("Cancelled.")
            raise typer.Exit(0)

    try:
        remove_target(name)
        typer.echo(f"Removed target: {name}")
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from None


@targets_app.command("default")
def targets_default(
    name: str = typer.Argument(..., help="Target name to set as default"),
) -> None:
    """Set the default target.

    Example:
        wafer targets default modal-b200
    """
    from .targets import set_default_target

    try:
        set_default_target(name)
        typer.echo(f"Default target set to: {name}")
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from None


# =============================================================================
# Workspaces commands
# =============================================================================


@workspaces_app.command("list")
def workspaces_list(
    json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
) -> None:
    """List all workspaces.

    Example:
        wafer workspaces list
        wafer workspaces list --json
    """
    from .workspaces import list_workspaces

    try:
        result = list_workspaces(json_output=json_output)
        typer.echo(result)
    except RuntimeError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from None


@workspaces_app.command("create")
def workspaces_create(
    name: str = typer.Argument(..., help="Workspace name"),
    gpu_type: str = typer.Option("B200", "--gpu", "-g", help="GPU type (default: B200)"),
    image: str | None = typer.Option(None, "--image", "-i", help="Docker image (optional)"),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
) -> None:
    """Create a new workspace.

    Example:
        wafer workspaces create my-kernel
        wafer workspaces create my-kernel --gpu H100
        wafer workspaces create my-kernel --image pytorch/pytorch:2.5.1-cuda12.4-cudnn9-devel
    """
    from .workspaces import create_workspace

    try:
        result = create_workspace(name, gpu_type=gpu_type, image=image, json_output=json_output)
        typer.echo(result)
    except RuntimeError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from None


@workspaces_app.command("delete")
def workspaces_delete(
    workspace_id: str = typer.Argument(..., help="Workspace ID to delete"),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
) -> None:
    """Delete a workspace.

    Example:
        wafer workspaces delete ws_abc123
    """
    from .workspaces import delete_workspace

    try:
        result = delete_workspace(workspace_id, json_output=json_output)
        typer.echo(result)
    except RuntimeError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from None


@workspaces_app.command("attach")
def workspaces_attach(
    workspace_id: str = typer.Argument(..., help="Workspace ID to attach to"),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
) -> None:
    """Attach to a workspace (get SSH credentials).

    This will:
    1. Start the workspace if needed
    2. Return SSH connection details
    3. Save the private key to ~/.wafer/keys/

    Example:
        wafer workspaces attach ws_abc123
        wafer workspaces attach ws_abc123 --json
    """
    from .workspaces import attach_workspace

    try:
        result = attach_workspace(workspace_id, json_output=json_output)
        typer.echo(result)
    except RuntimeError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from None


@workspaces_app.command("show")
def workspaces_show(
    workspace_id: str = typer.Argument(..., help="Workspace ID to show"),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
) -> None:
    """Show details of a workspace.

    Example:
        wafer workspaces show ws_abc123
        wafer workspaces show ws_abc123 --json
    """
    from .workspaces import get_workspace

    try:
        result = get_workspace(workspace_id, json_output=json_output)
        typer.echo(result)
    except RuntimeError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from None


# =============================================================================
# Perfetto trace analysis commands
# =============================================================================


@perfetto_app.command("query")
def perfetto_query(
    trace_path: Path = typer.Argument(..., help="Path to Perfetto trace file"),
    sql: str = typer.Argument(..., help="SQL query to execute"),
    json_output: bool = typer.Option(True, "--json", "-j", help="Output as JSON"),
) -> None:
    """Execute SQL query against a Perfetto trace.

    Starts trace_processor, loads the trace, executes the query, and returns results.

    Examples:
        wafer perfetto query trace.perfetto "SELECT * FROM slice LIMIT 10"
        wafer perfetto query trace.perfetto "SELECT name, dur FROM slice ORDER BY dur DESC LIMIT 5"
    """
    from wafer_core.lib.perfetto.perfetto_tool import PerfettoConfig, PerfettoTool

    config = PerfettoConfig(
        workspace_root=".",
        storage_dir=str(Path.home() / ".wafer" / "perfetto"),
    )
    tool = PerfettoTool(config)

    try:
        results, err = tool.query(sql, str(trace_path))
        if err:
            typer.echo(f"Error: {err}", err=True)
            raise typer.Exit(1)

        if json_output:
            typer.echo(json.dumps({"results": results, "count": len(results or [])}, indent=2))
        else:
            if not results:
                typer.echo("No results")
            else:
                # Simple table output
                if results:
                    headers = list(results[0].keys())
                    typer.echo("\t".join(headers))
                    for row in results:
                        typer.echo("\t".join(str(row.get(h, "")) for h in headers))
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from None


@perfetto_app.command("tables")
def perfetto_tables(
    trace_path: Path = typer.Argument(..., help="Path to Perfetto trace file"),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
) -> None:
    """List available tables in a Perfetto trace.

    Examples:
        wafer perfetto tables trace.perfetto
        wafer perfetto tables trace.perfetto --json
    """
    from wafer_core.lib.perfetto.perfetto_tool import PerfettoConfig, PerfettoTool

    config = PerfettoConfig(
        workspace_root=".",
        storage_dir=str(Path.home() / ".wafer" / "perfetto"),
    )
    tool = PerfettoTool(config)

    try:
        tables, err = tool.get_tables(str(trace_path))
        if err:
            typer.echo(f"Error: {err}", err=True)
            raise typer.Exit(1)

        if json_output:
            typer.echo(json.dumps({"tables": tables}, indent=2))
        else:
            typer.echo(f"Found {len(tables or [])} tables:")
            for table in tables or []:
                typer.echo(f"  {table}")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from None


@perfetto_app.command("schema")
def perfetto_schema(
    trace_path: Path = typer.Argument(..., help="Path to Perfetto trace file"),
    table: str = typer.Argument(..., help="Table name"),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
) -> None:
    """Get schema for a table in a Perfetto trace.

    Examples:
        wafer perfetto schema trace.perfetto slice
        wafer perfetto schema trace.perfetto thread --json
    """
    from wafer_core.lib.perfetto.perfetto_tool import PerfettoConfig, PerfettoTool

    config = PerfettoConfig(
        workspace_root=".",
        storage_dir=str(Path.home() / ".wafer" / "perfetto"),
    )
    tool = PerfettoTool(config)

    try:
        columns, err = tool.get_schema(table, str(trace_path))
        if err:
            typer.echo(f"Error: {err}", err=True)
            raise typer.Exit(1)

        if json_output:
            typer.echo(json.dumps({"table": table, "columns": columns}, indent=2))
        else:
            typer.echo(f"Schema for table '{table}':")
            for col in columns or []:
                nullable = "NULL" if col.get("nullable") else "NOT NULL"
                typer.echo(f"  {col['name']}: {col['type']} {nullable}")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from None


@perfetto_app.command("check")
def perfetto_check(
    json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
) -> None:
    """Check if trace_processor is available.

    Examples:
        wafer perfetto check
        wafer perfetto check --json
    """
    from wafer_core.lib.perfetto.perfetto_tool import PerfettoConfig, PerfettoTool

    config = PerfettoConfig(
        workspace_root=".",
        storage_dir=str(Path.home() / ".wafer" / "perfetto"),
    )
    tool = PerfettoTool(config)

    status = tool.check_processor()

    if json_output:
        typer.echo(json.dumps(status.to_dict(), indent=2))
    else:
        if status.available:
            typer.echo(f"✓ trace_processor available at {status.binary_path}")
            typer.echo(f"  Version: {status.version}")
            if not status.version_matches_ui:
                typer.echo(f"  ⚠ Version mismatch with UI (expected: {status.ui_version})")
        else:
            typer.echo(f"✗ trace_processor not available: {status.error}")
            typer.echo("  Run 'wafer perfetto check' to auto-download")


# =============================================================================
# NCU Analyze command
# =============================================================================


@app.command("ncu-analyze")
def ncu_analyze(
    filepath: Path = typer.Argument(..., help="Path to .ncu-rep profile file"),
    output_dir: Path | None = typer.Option(
        None, "--output-dir", "-o", help="Output directory for analysis files"
    ),
    json_output: bool = typer.Option(
        False, "--json", help="Output raw JSON instead of formatted text"
    ),
    remote: bool | None = typer.Option(
        None,
        "--remote/--local",
        help="Force remote (via API) or local analysis. Default: auto-detect (remote if NCU not installed locally)",
    ),
    target: str | None = typer.Option(
        None,
        "--target",
        "-t",
        help="Target name for direct SSH mode (e.g., 'vultr-b200'). Bypasses API.",
    ),
    include_source: bool = typer.Option(
        False,
        "--include-source",
        "-s",
        help="Include SASS source correlation for each kernel (requires --remote)",
    ),
) -> None:
    """Analyze an NVIDIA Nsight Compute profile (.ncu-rep file).

    Returns kernel performance metrics including duration, occupancy,
    compute/memory throughput, and optimization recommendations.

    By default, uses local NCU if available, otherwise runs analysis
    remotely via wafer-api (requires authentication: wafer login).

    Use --target for direct SSH mode (like wafer remote-run --direct).
    Use --include-source to fetch SASS assembly with register/instruction data.

    Examples:
        wafer ncu-analyze profile.ncu-rep
        wafer ncu-analyze profile.ncu-rep --json
        wafer ncu-analyze profile.ncu-rep --output-dir ./analysis
        wafer ncu-analyze profile.ncu-rep --remote  # Force remote via API
        wafer ncu-analyze profile.ncu-rep --target vultr-b200  # Direct SSH
        wafer ncu-analyze profile.ncu-rep --include-source --json  # With SASS source
    """
    from .ncu_analyze import analyze_ncu_profile

    if not filepath.exists():
        typer.echo(f"Error: File not found: {filepath}", err=True)
        raise typer.Exit(1)

    if filepath.suffix != ".ncu-rep":
        typer.echo(f"Error: Expected .ncu-rep file, got: {filepath.suffix}", err=True)
        raise typer.Exit(1)

    try:
        result = analyze_ncu_profile(
            filepath,
            output_dir=output_dir,
            json_output=json_output,
            remote=remote,
            target=target,
            include_source=include_source,
        )
        typer.echo(result)
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from None
    except RuntimeError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from None


# =============================================================================
# NSYS Analyze command
# =============================================================================


@app.command("nsys-analyze")
def nsys_analyze(
    filepath: Path = typer.Argument(..., help="Path to .nsys-rep profile file"),
    json_output: bool = typer.Option(
        False, "--json", help="Output raw JSON instead of formatted text"
    ),
    remote: bool | None = typer.Option(
        None,
        "--remote/--local",
        help="Force remote (via API) or local analysis. Default: auto-detect (remote if nsys not installed locally)",
    ),
) -> None:
    """Analyze an NVIDIA Nsight Systems profile (.nsys-rep file).

    Returns timeline events, kernel information, memory usage, and diagnostics.

    By default, uses local nsys if available, otherwise runs analysis
    remotely via wafer-api (requires authentication: wafer login).

    Examples:
        wafer nsys-analyze profile.nsys-rep
        wafer nsys-analyze profile.nsys-rep --json
        wafer nsys-analyze profile.nsys-rep --remote  # Force remote via API
    """
    from .nsys_analyze import analyze_nsys_profile

    if not filepath.exists():
        typer.echo(f"Error: File not found: {filepath}", err=True)
        raise typer.Exit(1)

    if filepath.suffix != ".nsys-rep":
        typer.echo(f"Error: Expected .nsys-rep file, got: {filepath.suffix}", err=True)
        raise typer.Exit(1)

    try:
        result = analyze_nsys_profile(
            filepath,
            json_output=json_output,
            remote=remote,
        )
        typer.echo(result)
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from None
    except (RuntimeError, ValueError, NotImplementedError) as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from None


# =============================================================================
# ROCprof-Compute commands
# =============================================================================

# Create rocprof-sdk subcommand group
rocprof_sdk_app = typer.Typer(help="ROCprofiler-SDK profiling tool commands")
app.add_typer(rocprof_sdk_app, name="rocprof-sdk")


@rocprof_sdk_app.command("check")
def rocprof_sdk_check(
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
) -> None:
    """Check if rocprofv3 is installed.

    Examples:
        wafer rocprof-sdk check
        wafer rocprof-sdk check --json
    """
    from .rocprof_sdk import check_command

    try:
        result = check_command(json_output)
        if json_output:
            typer.echo(result)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@rocprof_sdk_app.command("list-counters")
def rocprof_sdk_list_counters() -> None:
    """List available hardware counters for your GPU.

    Examples:
        wafer rocprof-sdk list-counters
        wafer rocprof-sdk list-counters | grep SQ_
    """
    from .rocprof_sdk import list_counters_command

    try:
        list_counters_command()
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@rocprof_sdk_app.command("profile")
def rocprof_sdk_profile(
    command: str = typer.Argument(..., help="Command to profile"),
    output_dir: str | None = typer.Option(None, "--output-dir", "-o", help="Output directory"),
    output_format: str = typer.Option(
        "csv", "--format", "-f", help="Output format (csv, json, rocpd, pftrace, otf2)"
    ),
    counters: str | None = typer.Option(
        None, "--counters", "-c", help="Comma-separated hardware counters"
    ),
    kernel_include: str | None = typer.Option(
        None, "--kernel-include", help="Include only kernels matching this regex"
    ),
    kernel_exclude: str | None = typer.Option(
        None, "--kernel-exclude", help="Exclude kernels matching this regex"
    ),
    trace_hip_runtime: bool = typer.Option(
        False, "--trace-hip-runtime", help="Enable HIP runtime API tracing"
    ),
    trace_hip_compiler: bool = typer.Option(
        False, "--trace-hip-compiler", help="Enable HIP compiler code tracing"
    ),
    trace_hsa: bool = typer.Option(False, "--trace-hsa", help="Enable HSA API tracing"),
    trace_marker: bool = typer.Option(False, "--trace-marker", help="Enable ROCTx marker tracing"),
    trace_memory_copy: bool = typer.Option(
        False, "--trace-memory-copy", help="Enable memory copy tracing"
    ),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
) -> None:
    """Profile a command with rocprofv3.

    Examples:
        wafer rocprof-sdk profile './my_kernel'
        wafer rocprof-sdk profile './app' --format csv --output-dir ./results
        wafer rocprof-sdk profile './kernel' --counters SQ_WAVES,L2_CACHE_HITS
        wafer rocprof-sdk profile './app' --kernel-include 'vectorAdd|matmul'
        wafer rocprof-sdk profile './app' --trace-hip-runtime --trace-memory-copy
    """
    from .rocprof_sdk import profile_command

    counter_list = counters.split(",") if counters else None

    try:
        result = profile_command(
            command,
            output_dir,
            output_format,
            counter_list,
            kernel_include,
            kernel_exclude,
            trace_hip_runtime,
            trace_hip_compiler,
            trace_hsa,
            trace_marker,
            trace_memory_copy,
            json_output,
        )
        if json_output:
            typer.echo(result)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@rocprof_sdk_app.command("analyze")
def rocprof_sdk_analyze(
    file_path: Path = typer.Argument(
        ..., help="Path to rocprofiler output file (.csv, .json, .db)"
    ),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
) -> None:
    """Analyze a rocprofiler output file.

    Supports:
    - CSV stats files (stats_*.csv)
    - JSON trace files (*.json)
    - rocpd databases (*_results.db, *.rocpd)

    Examples:
        wafer rocprof-sdk analyze stats_kernel.csv
        wafer rocprof-sdk analyze results.json
        wafer rocprof-sdk analyze profile_results.db --json
    """
    from .rocprof_sdk import analyze_command

    if not file_path.exists():
        typer.echo(f"Error: File not found: {file_path}", err=True)
        raise typer.Exit(1)

    try:
        result = analyze_command(str(file_path), json_output)
        if json_output:
            typer.echo(result)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


# Create rocprof-systems subcommand group
rocprof_systems_app = typer.Typer(help="ROCprofiler-Systems profiling tool commands")
app.add_typer(rocprof_systems_app, name="rocprof-systems")


@rocprof_systems_app.command("check")
def rocprof_systems_check(
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
) -> None:
    """Check if rocprof-sys tools are installed.

    Examples:
        wafer rocprof-systems check
        wafer rocprof-systems check --json
    """
    from .rocprof_systems import check_command

    try:
        result = check_command(json_output)
        if json_output:
            typer.echo(result)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@rocprof_systems_app.command("run")
def rocprof_systems_run(
    command: str = typer.Argument(..., help="Command to profile"),
    output_dir: str | None = typer.Option(None, "--output-dir", "-o", help="Output directory"),
    trace: bool = typer.Option(
        True, "--trace/--no-trace", help="Generate detailed trace (Perfetto)"
    ),
    profile: bool = typer.Option(False, "--profile", help="Generate call-stack-based profile"),
    flat_profile: bool = typer.Option(False, "--flat-profile", help="Generate flat profile"),
    sample: bool = typer.Option(False, "--sample", help="Enable sampling profiling"),
    host: bool = typer.Option(False, "--host", help="Enable host metrics"),
    device: bool = typer.Option(False, "--device", help="Enable device metrics"),
    wait: float | None = typer.Option(None, "--wait", help="Wait time before collecting (seconds)"),
    duration: float | None = typer.Option(
        None, "--duration", help="Duration of collection (seconds)"
    ),
    use_rocm: bool = typer.Option(True, "--use-rocm/--no-rocm", help="Enable ROCm backend"),
    use_sampling: bool = typer.Option(False, "--use-sampling", help="Enable sampling backend"),
    use_kokkosp: bool = typer.Option(
        False, "--use-kokkosp", help="Enable Kokkos profiling backend"
    ),
    use_mpip: bool = typer.Option(False, "--use-mpip", help="Enable MPI profiling backend"),
    use_rocpd: bool = typer.Option(False, "--use-rocpd", help="Enable rocpd database output"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
) -> None:
    """Run system profiling with rocprof-sys-run.

    Examples:
        wafer rocprof-systems run './my_app'
        wafer rocprof-systems run './app' --trace --profile --output-dir ./results
        wafer rocprof-systems run './kernel' --host --device --duration 10
        wafer rocprof-systems run './app' --use-kokkosp --use-mpip
    """
    from .rocprof_systems import run_command

    try:
        result = run_command(
            command=command,
            output_dir=output_dir,
            trace=trace,
            profile=profile,
            flat_profile=flat_profile,
            sample=sample,
            host=host,
            device=device,
            wait=wait,
            duration=duration,
            use_rocm=use_rocm,
            use_sampling=use_sampling,
            use_kokkosp=use_kokkosp,
            use_mpip=use_mpip,
            use_rocpd=use_rocpd,
            json_output=json_output,
        )
        if json_output:
            typer.echo(result)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@rocprof_systems_app.command("analyze")
def rocprof_systems_analyze(
    file_path: Path = typer.Argument(..., help="Path to rocprof-sys output file (.json, .txt)"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
) -> None:
    """Analyze a rocprof-sys output file.

    Supports:
    - JSON files (wall_clock-*.json, metadata-*.json, functions-*.json)
    - Text files (wall-clock.txt)

    Examples:
        wafer rocprof-systems analyze wall_clock-12345.json
        wafer rocprof-systems analyze wall-clock.txt --json
    """
    from .rocprof_systems import analyze_command

    if not file_path.exists():
        typer.echo(f"Error: File not found: {file_path}", err=True)
        raise typer.Exit(1)

    try:
        result = analyze_command(str(file_path), json_output)
        if json_output:
            typer.echo(result)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@rocprof_systems_app.command("sample")
def rocprof_systems_sample(
    command: str = typer.Argument(..., help="Command to profile"),
    output_dir: str | None = typer.Option(None, "--output-dir", "-o", help="Output directory"),
    frequency: int | None = typer.Option(
        None, "--frequency", "--freq", "-f", help="Sampling frequency in Hz"
    ),
    trace: bool = typer.Option(False, "--trace", help="Generate detailed trace"),
    profile: bool = typer.Option(False, "--profile", help="Generate call-stack profile"),
    flat_profile: bool = typer.Option(False, "--flat-profile", help="Generate flat profile"),
    host: bool = typer.Option(False, "--host", help="Enable host metrics"),
    device: bool = typer.Option(False, "--device", help="Enable device metrics"),
    wait: float | None = typer.Option(None, "--wait", help="Wait time (seconds)"),
    duration: float | None = typer.Option(None, "--duration", help="Duration (seconds)"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
) -> None:
    """Run sampling profiling with rocprof-sys-sample.

    Examples:
        wafer rocprof-systems sample ./my_app --frequency 100
        wafer rocprof-systems sample ./kernel --freq 500 --output-dir ./results
    """
    from .rocprof_systems import sample_command

    try:
        result = sample_command(
            command=command,
            output_dir=output_dir,
            frequency=frequency,
            trace=trace,
            profile=profile,
            flat_profile=flat_profile,
            host=host,
            device=device,
            wait=wait,
            duration=duration,
            json_output=json_output,
        )
        if json_output:
            typer.echo(result)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@rocprof_systems_app.command("instrument")
def rocprof_systems_instrument(
    command: str = typer.Argument(..., help="Command to instrument"),
    output_dir: str | None = typer.Option(None, "--output-dir", "-o", help="Output directory"),
    simulate: bool = typer.Option(False, "--simulate", help="Simulate without creating binary"),
    function_include: list[str] | None = typer.Option(
        None, "--function-include", help="Function patterns to include"
    ),
    function_exclude: list[str] | None = typer.Option(
        None, "--function-exclude", help="Function patterns to exclude"
    ),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
) -> None:
    """Run binary instrumentation with rocprof-sys-instrument.

    Examples:
        wafer rocprof-systems instrument ./my_app --simulate
        wafer rocprof-systems instrument ./kernel --output-dir ./results
    """
    from .rocprof_systems import instrument_command

    try:
        result = instrument_command(
            command=command,
            output_dir=output_dir,
            simulate=simulate,
            function_include=function_include,
            function_exclude=function_exclude,
            json_output=json_output,
        )
        if json_output:
            typer.echo(result)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@rocprof_systems_app.command("query")
def rocprof_systems_query(
    components: bool = typer.Option(False, "--components", help="Query available components"),
    hw_counters: bool = typer.Option(False, "--hw-counters", help="Query hardware counters"),
    all_metrics: bool = typer.Option(False, "--all", help="Query all metrics"),
    filter_pattern: str | None = typer.Option(None, "--filter", help="Filter results"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
) -> None:
    """Query available profiling metrics and components.

    Examples:
        wafer rocprof-systems query --components
        wafer rocprof-systems query --hw-counters
        wafer rocprof-systems query --components --filter cpu
    """
    from .rocprof_systems import query_command

    try:
        result = query_command(
            components=components,
            hw_counters=hw_counters,
            all_metrics=all_metrics,
            filter_pattern=filter_pattern,
            json_output=json_output,
        )
        if json_output:
            typer.echo(result)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


# Create rocprof-compute subcommand group
rocprof_compute_app = typer.Typer(help="ROCprofiler-Compute profiling tool commands")
app.add_typer(rocprof_compute_app, name="rocprof-compute")


@rocprof_compute_app.command("check")
def rocprof_compute_check(
    json_output: bool = typer.Option(False, "--json", help="Output status as JSON"),
) -> None:
    """Check if rocprof-compute is installed.

    Examples:
        wafer rocprof-compute check
        wafer rocprof-compute check --json
    """
    from .rocprof_compute import check_command

    try:
        result = check_command(json_output=json_output)
        if json_output:
            typer.echo(result)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@rocprof_compute_app.command("profile")
def rocprof_compute_profile(
    command: str = typer.Argument(..., help="Command to profile"),
    name: str = typer.Option(..., "--name", "-n", help="Workload name"),
    path: str | None = typer.Option(None, "--path", "-p", help="Workload base path"),
    kernel: str | None = typer.Option(
        None, "--kernel", "-k", help="Kernel filter (comma-separated)"
    ),
    dispatch: str | None = typer.Option(
        None, "--dispatch", "-d", help="Dispatch filter (comma-separated)"
    ),
    block: str | None = typer.Option(None, "--block", "-b", help="Block filter (comma-separated)"),
    no_roof: bool = typer.Option(False, "--no-roof", help="Skip roofline data"),
    roof_only: bool = typer.Option(False, "--roof-only", help="Profile roofline only (fastest)"),
    hip_trace: bool = typer.Option(False, "--hip-trace", help="Enable HIP trace"),
    verbose: int = typer.Option(0, "--verbose", "-v", count=True, help="Increase verbosity"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
) -> None:
    """Profile a command with rocprof-compute.

    Executes rocprof-compute profiling on the target command and generates
    analysis results including roofline data, memory analysis, and kernel statistics.

    Examples:
        wafer rocprof-compute profile --name vcopy -- './vcopy -n 1048576'
        wafer rocprof-compute profile -n test -b SQ,TCC -- './kernel'
        wafer rocprof-compute profile -n trace --hip-trace -- './app'
        wafer rocprof-compute profile -n test --roof-only -- './app'
    """
    from .rocprof_compute import profile_command

    try:
        result = profile_command(
            command,
            name,
            path,
            kernel,
            dispatch,
            block,
            no_roof,
            roof_only,
            hip_trace,
            verbose,
            json_output,
        )
        if json_output:
            typer.echo(result)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@rocprof_compute_app.command("analyze")
def rocprof_compute_analyze(
    workload_path: Path = typer.Argument(..., help="Path to workload directory"),
    kernel: str | None = typer.Option(None, "--kernel", "-k", help="Kernel filter"),
    dispatch: str | None = typer.Option(None, "--dispatch", "-d", help="Dispatch filter"),
    block: str | None = typer.Option(None, "--block", "-b", help="Block filter"),
    output: str | None = typer.Option(None, "--output", "-o", help="Output file"),
    list_stats: bool = typer.Option(
        False, "--list-stats", help="List all detected kernels and dispatches"
    ),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
    gui: bool = typer.Option(
        False, "--gui", help="Launch interactive GUI viewer (bundled Python viewer by default)"
    ),
    port: int = typer.Option(8050, "--port", "-p", help="Port for GUI server"),
    external: bool = typer.Option(
        False,
        "--external",
        help="Use AMD's native rocprof-compute GUI instead of bundled (requires ROCm)",
    ),
) -> None:
    """Analyze a rocprof-compute workload directory.

    Parses workload data and displays kernel statistics, roofline analysis,
    and performance metrics. Can optionally launch an interactive GUI viewer.

    GUI Modes:
        --gui           Uses Wafer's bundled Python viewer (works anywhere, no ROCm needed)
        --gui --external Uses AMD's native rocprof-compute GUI (requires ROCm installation)

    Examples:
        wafer rocprof-compute analyze ./workloads/vcopy
        wafer rocprof-compute analyze ./workloads/test --json
        wafer rocprof-compute analyze ./workloads/app -d 0,1 -o filtered.csv
        wafer rocprof-compute analyze ./workloads/app --list-stats
        wafer rocprof-compute analyze ./workloads/app --gui
        wafer rocprof-compute analyze ./workloads/app --gui --port 9000
        wafer rocprof-compute analyze ./workloads/app --gui --external
    """
    from .rocprof_compute import analyze_command

    if not workload_path.exists():
        typer.echo(f"Error: Workload path not found: {workload_path}", err=True)
        raise typer.Exit(1)

    try:
        result = analyze_command(
            str(workload_path),
            kernel,
            dispatch,
            block,
            output,
            list_stats,
            json_output,
            gui,
            port,
            external,
        )
        if json_output or not gui:
            typer.echo(result)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@rocprof_compute_app.command("list-metrics")
def rocprof_compute_list_metrics(
    arch: str = typer.Argument(..., help="Architecture (gfx90a, gfx942, etc.)"),
) -> None:
    """List available metrics for an architecture.

    Examples:
        wafer rocprof-compute list-metrics gfx90a
        wafer rocprof-compute list-metrics gfx942
    """
    from .rocprof_compute import list_metrics_command

    try:
        result = list_metrics_command(arch)
        if result:
            typer.echo(result)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


# =============================================================================
# Compiler Analyze command
# =============================================================================


@app.command("compiler-analyze")
def compiler_analyze(
    mlir_file: Path | None = typer.Option(None, "--mlir", help="Path to MLIR file"),
    ptx_file: Path | None = typer.Option(None, "--ptx", help="Path to PTX file"),
    sass_file: Path | None = typer.Option(None, "--sass", help="Path to SASS file"),
    source_file: Path | None = typer.Option(None, "--source", help="Path to source file"),
    mlir_text: str | None = typer.Option(None, "--mlir-text", help="MLIR text content"),
    ptx_text: str | None = typer.Option(None, "--ptx-text", help="PTX text content"),
    sass_text: str | None = typer.Option(None, "--sass-text", help="SASS text content"),
    source_text: str | None = typer.Option(None, "--source-text", help="Source code text"),
    kernel_name: str | None = typer.Option(None, "--kernel-name", help="Kernel name"),
    json_output: bool = typer.Option(True, "--json/--no-json", help="Output JSON"),
) -> None:
    """Analyze compiler kernel (MLIR/PTX/SASS).

    Examples:
        wafer compiler-analyze --mlir-text "..." --ptx-text "..." --sass-text "..."
        wafer compiler-analyze --mlir file.mlir --ptx file.ptx --sass file.sass
    """
    import sys

    from .compiler_analyze import analyze_compiler_kernel

    try:
        result = analyze_compiler_kernel(
            mlir_file=mlir_file,
            ptx_file=ptx_file,
            sass_file=sass_file,
            source_file=source_file,
            mlir_text=mlir_text,
            ptx_text=ptx_text,
            sass_text=sass_text,
            source_text=source_text,
            kernel_name=kernel_name,
            json_output=json_output,
        )
        if json_output:
            print(result)
        else:
            typer.echo(result)
    except ValueError as e:
        if json_output:
            import json

            error_json = json.dumps({"success": False, "error": str(e)}, indent=2)
            print(error_json, file=sys.stderr)
        else:
            typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from None
    except Exception as e:
        if json_output:
            import json

            error_json = json.dumps({"success": False, "error": str(e)}, indent=2)
            print(error_json, file=sys.stderr)
        else:
            typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from None


@app.command("capture")
def capture_command(
    label: str = typer.Argument(
        ..., help="Label for this capture (e.g., 'baseline', 'optimized-v2')"
    ),
    command: str = typer.Argument(..., help="Command to execute and capture"),
    variant: str | None = typer.Option(
        None, "--variant", "-v", help="Variant identifier for grouping related captures"
    ),
    tags: list[str] | None = typer.Option(
        None, "--tag", "-t", help="Tags for categorization (can be specified multiple times)"
    ),  # noqa: B008
    working_dir: Path | None = typer.Option(
        None, "--dir", "-d", help="Working directory (default: current directory)"
    ),
    sweep: list[str] | None = typer.Option(
        None, "--sweep", "-s", help="Parameter sweep (format: VAR=val1,val2,val3)"
    ),  # noqa: B008
    code_denylist: list[str] | None = typer.Option(
        None,
        "--code-denylist",
        help="Patterns to exclude from code files (e.g., '*.log', '**/test/**')",
    ),  # noqa: B008
    artifact_denylist: list[str] | None = typer.Option(
        None,
        "--artifact-denylist",
        help="Patterns to exclude from artifacts (e.g., '*.tmp', '*.o')",
    ),  # noqa: B008
) -> None:
    """Capture a complete execution snapshot for reproducibility.

    Captures everything needed to reproduce a benchmark run:
    - Command output (stdout/stderr), exit code, duration
    - Generated artifacts (outputs, profiles, logs)
    - Code files used in execution
    - Git context (repo, commit, branch, dirty status)
    - System context (GPU model, CUDA version, hostname)
    - Metrics extracted from stdout (latency, throughput, etc.)

    All data is uploaded to Supabase for later analysis and comparison.

    Denylist Configuration (precedence: CLI > Project > Global > Defaults):
        1. CLI flags: --code-denylist and --artifact-denylist
        2. Project config: .wafer-capture.toml in working directory
        3. Global config: ~/.wafer/capture.toml
        4. Built-in defaults (excludes common binaries, dependencies, etc.)

    Examples:
        # Basic capture
        wafer capture baseline "python benchmark.py"

        # With variant for A/B testing
        wafer capture optimized "python benchmark.py" --variant v2

        # With tags
        wafer capture test-run "make && ./kernel" --tag cuda --tag fp16

        # Different working directory
        wafer capture training "python train.py" --dir ./experiments/run1

        # Custom denylists via CLI
        wafer capture test "make" --code-denylist "*.log" --code-denylist "**/test/**"

        # Parameter sweep (runs multiple captures with different values)
        wafer capture batch-sizes "python train.py --batch-size {BATCH}" --sweep "BATCH=16,32,64,128"

        # Multiple variable sweep (cartesian product)
        wafer capture grid-search "python train.py --lr {LR} --bs {BS}" --sweep "LR=0.001,0.01,0.1" --sweep "BS=16,32"
    """
    import itertools
    import tomllib

    import trio
    from wafer_core.tools.capture_tool import (  # pragma: no cover
        CaptureConfig,
        capture,
        execute_command,
    )

    # Resolve working directory
    work_dir = working_dir.resolve() if working_dir else Path.cwd()

    # Load denylists from config files (precedence: project > global > defaults)
    config_code_denylist = None
    config_artifact_denylist = None

    # 1. Try global config (~/.wafer/capture.toml)
    global_config_path = Path.home() / ".wafer" / "capture.toml"
    if global_config_path.exists():
        try:
            with open(global_config_path, "rb") as f:
                capture_config_data = tomllib.load(f)
            config_code_denylist = capture_config_data.get("code_denylist")
            config_artifact_denylist = capture_config_data.get("artifact_denylist")
        except Exception as e:
            typer.echo(f"⚠️  Warning: Failed to load {global_config_path}: {e}", err=True)

    # 2. Try project-specific config (.wafer-capture.toml in working dir)
    project_config_path = work_dir / ".wafer-capture.toml"
    if project_config_path.exists():
        try:
            with open(project_config_path, "rb") as f:
                project_config_data = tomllib.load(f)
            # Project config overrides global config
            if "code_denylist" in project_config_data:
                config_code_denylist = project_config_data["code_denylist"]
            if "artifact_denylist" in project_config_data:
                config_artifact_denylist = project_config_data["artifact_denylist"]
        except Exception as e:
            typer.echo(f"⚠️  Warning: Failed to load {project_config_path}: {e}", err=True)

    # Parse sweep parameters (format: "VAR=val1,val2,val3")
    sweep_vars: dict[str, list[str]] = {}
    if sweep:
        for sweep_spec in sweep:
            if "=" not in sweep_spec:
                typer.echo(f"❌ Invalid sweep format: {sweep_spec}", err=True)
                typer.echo("   Expected format: VAR=val1,val2,val3", err=True)
                raise typer.Exit(1)

            var_name, values_str = sweep_spec.split("=", 1)
            values = [v.strip() for v in values_str.split(",")]
            sweep_vars[var_name] = values

    # Generate all combinations (cartesian product) of sweep variables
    if sweep_vars:
        var_names = list(sweep_vars.keys())
        var_values = [sweep_vars[name] for name in var_names]
        combinations = list(itertools.product(*var_values))

        typer.echo(f"🔬 Running sweep: {label}")
        typer.echo(f"   Variables: {', '.join(var_names)}")
        typer.echo(f"   Total runs: {len(combinations)}")
        typer.echo()
    else:
        # Single run (no sweep)
        combinations = [()]
        var_names = []

    # Progress callback
    def progress(msg: str) -> None:
        typer.echo(f"  {msg}")

    async def run_capture_sweep() -> None:
        successful = 0
        failed = 0

        for idx, combo in enumerate(combinations, 1):
            # Substitute variables in command
            substituted_cmd = command
            sweep_info = {}
            for var_name, value in zip(var_names, combo, strict=True):
                substituted_cmd = substituted_cmd.replace(f"{{{var_name}}}", value)
                sweep_info[var_name] = value

            # Create variant name for sweep runs
            if sweep_vars:
                variant_parts = [f"{k}={v}" for k, v in sweep_info.items()]
                run_variant = "_".join(variant_parts)
                if variant:
                    run_variant = f"{variant}_{run_variant}"
            else:
                run_variant = variant

            # Create config for this run
            # Build denylist kwargs with precedence: CLI > Config File > Defaults
            denylist_kwargs = {}

            # Code denylist: CLI flag takes precedence over config file
            if code_denylist:
                denylist_kwargs["code_denylist"] = code_denylist
            elif config_code_denylist:
                denylist_kwargs["code_denylist"] = config_code_denylist
            # Otherwise use CaptureConfig defaults

            # Artifact denylist: CLI flag takes precedence over config file
            if artifact_denylist:
                denylist_kwargs["artifact_denylist"] = artifact_denylist
            elif config_artifact_denylist:
                denylist_kwargs["artifact_denylist"] = config_artifact_denylist
            # Otherwise use CaptureConfig defaults

            config = CaptureConfig(
                label=label,
                command=substituted_cmd,
                working_dir=work_dir,
                variant=run_variant,
                tags=tags or [],
                **denylist_kwargs,
            )

            try:
                if sweep_vars:
                    typer.echo(
                        f"[{idx}/{len(combinations)}] {', '.join(f'{k}={v}' for k, v in sweep_info.items())}"
                    )
                else:
                    typer.echo(f"🔬 Capturing: {label}")

                typer.echo(f"   Command: {substituted_cmd}")
                typer.echo(f"   Working dir: {work_dir}")
                typer.echo()

                result = await capture(
                    config=config, runner=execute_command, progress_callback=progress
                )

                typer.echo()
                typer.echo("✅ Capture complete!")
                typer.echo(f"   ID: {result.id}")
                typer.echo(f"   Exit code: {result.exit_code}")
                typer.echo(f"   Duration: {result.duration_seconds:.2f}s")
                typer.echo(f"   Code files: {len(result.code_files)}")
                typer.echo(f"   Artifacts: {len(result.artifacts)}")
                if result.metrics.stdout_metrics:
                    typer.echo(f"   Metrics: {len(result.metrics.stdout_metrics)}")
                typer.echo()

                successful += 1

            except Exception as e:
                typer.echo(f"\n❌ Capture failed: {e}", err=True)
                typer.echo()
                failed += 1

        # Summary for sweep runs
        if sweep_vars and len(combinations) > 1:
            typer.echo("=" * 60)
            typer.echo(f"Sweep complete: {successful} successful, {failed} failed")

        if failed > 0:
            raise typer.Exit(1)

    trio.run(run_capture_sweep)


@app.command("capture-list")
def capture_list_command(
    label: str | None = typer.Option(None, "--label", "-l", help="Filter by label"),
    limit: int = typer.Option(100, "--limit", "-n", help="Maximum number of results"),
    offset: int = typer.Option(0, "--offset", "-o", help="Offset for pagination"),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
) -> None:
    """List captured executions.

    Query captures from the backend with optional filtering and pagination.
    Output can be formatted as a table (default) or JSON.

    Examples:
        # List all captures
        wafer capture-list

        # Filter by label
        wafer capture-list --label baseline

        # Get JSON output for scripting
        wafer capture-list --json --limit 10

        # Pagination
        wafer capture-list --limit 20 --offset 20
    """

    import trio
    from wafer_core.utils.backend import list_captures  # pragma: no cover

    async def run_list() -> None:
        try:
            captures = await list_captures(label=label, limit=limit, offset=offset)

            if json_output:
                # JSON output for machine consumption
                typer.echo(json.dumps(captures, indent=2))
            else:
                # Human-readable table output
                if not captures:
                    typer.echo("No captures found.")
                    return

                typer.echo(f"Found {len(captures)} captures:\n")

                # Print table header
                typer.echo(
                    f"{'ID':<36}  {'Label':<20}  {'Variant':<20}  {'Exit':<4}  {'Duration':<8}  {'Created'}"
                )
                typer.echo("-" * 120)

                # Print each capture
                for cap in captures:
                    cap_id = cap.get("id", "")[:36]
                    cap_label = cap.get("label", "")[:20]
                    cap_variant = (cap.get("variant") or "")[:20]
                    exit_code = cap.get("exit_code", "")
                    duration = f"{cap.get('duration_seconds', 0):.2f}s"
                    created = cap.get("created_at", "")[:19]  # Strip microseconds

                    typer.echo(
                        f"{cap_id:<36}  {cap_label:<20}  {cap_variant:<20}  {exit_code:<4}  {duration:<8}  {created}"
                    )

        except Exception as e:
            typer.echo(f"❌ Failed to list captures: {e}", err=True)
            raise typer.Exit(1) from None

    trio.run(run_list)


def main() -> None:
    """Entry point for wafer CLI."""
    app()


if __name__ == "__main__":
    main()
