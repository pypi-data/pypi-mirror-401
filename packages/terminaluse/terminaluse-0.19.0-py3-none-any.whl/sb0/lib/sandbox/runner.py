"""Subprocess spawning and nsjail invocation for sandboxed handlers."""

from __future__ import annotations

import json
import asyncio
import subprocess
from typing import Any
from pathlib import Path
from dataclasses import dataclass

from pydantic import BaseModel

from sb0.lib.utils.logging import make_logger
from sb0.lib.sandbox.config import SandboxConfig, get_sandbox_config
from sb0.lib.sandbox.handler_ref import HandlerRef

logger = make_logger(__name__)


@dataclass
class SandboxResult:
    """Result of a sandboxed handler invocation."""

    success: bool
    exit_code: int
    stdout: str
    stderr: str
    timed_out: bool = False

    @property
    def status_json(self) -> dict[str, Any] | None:
        """Parse stdout as JSON status, or None if invalid."""
        if not self.stdout.strip():
            return None
        try:
            return json.loads(self.stdout)
        except json.JSONDecodeError:
            return None


class SandboxRunner:
    """Runs handlers in nsjail sandboxes."""

    def __init__(self, config: SandboxConfig | None = None):
        self.config = config or get_sandbox_config()

    def _build_nsjail_command(self, workspace_id: str | None = None) -> list[str]:
        """Build the nsjail command with all arguments.

        Args:
            workspace_id: If provided, mounts /workspaces/{workspace_id} as /workspace.
                         If None, creates an ephemeral tmpfs at /workspace.
        """
        config = self.config

        cmd = [config.nsjail_path]
        cmd.extend(
            [
                "--mode",
                "o",  # ONCE mode
                "--time_limit",
                str(config.timeout_seconds),
                # Resource limits
                # Note: Claude CLI (Node.js/V8) needs elevated limits
                "--rlimit_as",
                "6144",  # 6GB virtual memory (V8 reserves address space)
                "--rlimit_cpu",
                str(config.timeout_seconds),  # CPU time matches timeout
                "--rlimit_fsize",
                "100",  # 100MB max file size (matches tmpfs)
                "--rlimit_nofile",
                "1024",  # Max open files (Node.js async I/O)
                "--rlimit_nproc",
                "256",  # Max processes (Claude CLI spawns workers)
                "--rlimit_core",
                "0",  # Disable core dumps
                # Namespaces - enabled by default, disable some for Docker compatibility
                "--disable_clone_newnet",  # Keep network for LLM API calls
                "--disable_clone_newuts",  # Docker blocks sethostname()
                # Capabilities are dropped by default (don't pass --keep_caps)
                # Run as unprivileged user inside sandbox (defense in depth)
                # Also enables bypassPermissions mode in Claude CLI (blocked when running as root)
                "--user",
                "65534",  # nobody
                "--group",
                "65534",  # nogroup
                # Bind-mount host /proc read-only instead of creating new procfs.
                # Docker masks sensitive /proc files (e.g., /dev/null on /proc/kcore)
                # which prevents mounting a new procfs. Bind-mounting preserves
                # Docker's security masking while providing /proc access for subprocesses
                # like the Claude CLI. See docs/sandboxing_adr.md.
                "--disable_proc",
                "--bindmount_ro",
                "/proc:/proc",
                # Essential /dev devices (needed for SSL, random, uuid modules)
                "--bindmount_ro",
                "/dev/null:/dev/null",
                "--bindmount_ro",
                "/dev/zero:/dev/zero",
                "--bindmount_ro",
                "/dev/urandom:/dev/urandom",
                "--bindmount_ro",
                "/dev/random:/dev/random",
                # Read-only system mounts
                "--bindmount_ro",
                "/usr:/usr",
                "--bindmount_ro",
                "/lib:/lib",
                "--bindmount_ro",
                "/bin:/bin",
                # DNS, SSL, and hostname resolution
                "--bindmount_ro",
                "/etc/resolv.conf:/etc/resolv.conf",
                "--bindmount_ro",
                "/etc/ssl:/etc/ssl",
                "--bindmount_ro",
                "/etc/hosts:/etc/hosts",
                # Dynamic linker configuration (needed for Python shared libs)
                "--bindmount_ro",
                "/etc/ld.so.cache:/etc/ld.so.cache",
                # Agent code (read-only)
                # Mount code subdir (e.g., "project") to /agent/<subdir>
                "--bindmount_ro",
                f"{config.agent_dir}/{config.code_subdir}:/agent/{config.code_subdir}",
                # Ephemeral /tmp (cleared after each task)
                "--mount",
                "none:/tmp:tmpfs:size=104857600",
            ]
        )

        # Mount workspace - per-task if workspace_id provided, otherwise ephemeral
        if workspace_id:
            # Per-task workspace: mount /workspaces/{workspace_id} to /workspace (read-write)
            # This directory is populated by sync_down before the sandbox starts
            workspace_path = f"/workspaces/{workspace_id}"
            cmd.extend(["--bindmount", f"{workspace_path}:/workspace"])
        else:
            # No workspace_id: create ephemeral tmpfs at /workspace
            cmd.extend(["--mount", "none:/workspace:tmpfs:size=104857600"])

        # Writable home directory for subprocesses (e.g., Claude CLI uses ~/.claude)
        cmd.extend(["--mount", "none:/root:tmpfs:size=104857600"])

        # Mount persistent .claude directory for Claude SDK session resumption.
        # MUST come AFTER /root tmpfs mount so it overlays correctly at /root/.claude.
        # Uses absolute path (not ~/.claude) to avoid shell expansion ambiguity.
        if workspace_id:
            dot_claude_path = f"/dot_claudes/{workspace_id}"
            cmd.extend(["--bindmount", f"{dot_claude_path}:/root/.claude"])

        # Add /lib64 if it exists (varies by distro)
        if Path("/lib64").exists():
            cmd.extend(["--bindmount_ro", "/lib64:/lib64"])

        # Add /sbin if it exists
        if Path("/sbin").exists():
            cmd.extend(["--bindmount_ro", "/sbin:/sbin"])

        # Mount /app/src if it exists (for editable/development installs of sb0)
        if Path("/app/src").exists():
            cmd.extend(["--bindmount_ro", "/app/src:/app/src"])

        # TTY device for subprocess I/O (Claude CLI may need this)
        if Path("/dev/tty").exists():
            cmd.extend(["--bindmount_ro", "/dev/tty:/dev/tty"])

        return cmd

    def _build_env_args(self, extra_env: dict[str, str] | None = None) -> list[str]:
        """Build environment variable arguments for nsjail."""
        env_args = []

        # System env vars (always set)
        # Uses system Python (installed via uv pip install --system in Dockerfile)
        system_env = {
            "PYTHONNOUSERSITE": "1",
            "PYTHONPATH": "/agent:/usr/local/lib/python3.12/site-packages",
            "PATH": "/usr/local/bin:/usr/bin:/bin",
            "LD_LIBRARY_PATH": "/usr/local/lib:/usr/lib:/lib",
            "HOME": "/root",  # Needed for subprocesses like Claude CLI (~/.claude)
        }

        for key, value in system_env.items():
            env_args.extend(["--env", f"{key}={value}"])

        # Pass through env vars from EnvironmentVariables (the single source of truth)
        from sb0.lib.environment_variables import EnvironmentVariables

        env_vars = EnvironmentVariables.refresh()
        for field_name, value in env_vars.model_dump().items():
            if value is not None:
                env_args.extend(["--env", f"{field_name}={value}"])

        # Extra env vars for this specific invocation
        if extra_env:
            for key, value in extra_env.items():
                env_args.extend(["--env", f"{key}={value}"])

        return env_args

    def run(
        self,
        method: str,
        handler_ref: HandlerRef,
        params: BaseModel,
        workspace_id: str | None = None,
        extra_env: dict[str, str] | None = None,
    ) -> SandboxResult:
        """
        Run a handler in an nsjail sandbox.

        Args:
            method: The JSON-RPC method name (e.g., "event/send")
            handler_ref: Reference to the handler to run
            params: The Pydantic params model to pass to the handler
            workspace_id: Optional workspace ID - if provided, mounts /workspaces/{id} to /workspace
            extra_env: Additional environment variables for this invocation

        Returns:
            SandboxResult with execution outcome
        """
        config = self.config

        # Ensure workspace directory exists if workspace_id is provided
        if workspace_id:
            workspace_path = Path(f"/workspaces/{workspace_id}")
            workspace_path.mkdir(parents=True, exist_ok=True)
            dot_claude_path = Path(f"/dot_claudes/{workspace_id}")
            dot_claude_path.mkdir(parents=True, exist_ok=True)

        # Build the payload
        payload = {
            "method": method,
            "params_type": type(params).__name__,
            "handler": handler_ref.to_dict(),
            "params": params.model_dump(mode="json"),
        }
        payload_json = json.dumps(payload)

        # Build the command
        cmd = self._build_nsjail_command(workspace_id=workspace_id)
        cmd.extend(self._build_env_args(extra_env))
        cmd.extend(["--", "/usr/local/bin/python", "-m", "sb0.lib.sandbox.entrypoint"])

        if config.verbose:
            logger.info(f"[SANDBOX VERBOSE] Running: {handler_ref.module}.{handler_ref.function}")
            logger.info(f"[SANDBOX VERBOSE] workspace_id: {workspace_id}")
            logger.info(f"[SANDBOX VERBOSE] Full command: {' '.join(cmd)}")
        else:
            logger.debug(f"Running sandboxed handler: {handler_ref.module}.{handler_ref.function}")
            logger.debug(f"Sandbox command: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                input=payload_json,
                capture_output=True,
                text=True,
                timeout=config.timeout_seconds + 5,  # Small buffer over nsjail timeout
            )

            # Log detailed info on failure
            if result.returncode != 0:
                signal_info = ""
                if result.returncode < 0:
                    import signal

                    try:
                        sig = signal.Signals(-result.returncode)
                        signal_info = f" (signal: {sig.name})"
                    except ValueError:
                        signal_info = f" (signal: {-result.returncode})"

                logger.error(f"Sandbox process failed: exit_code={result.returncode}{signal_info}")
                logger.error(f"Sandbox command was: {' '.join(cmd[:10])}...")  # First 10 args
                if result.stderr:
                    logger.error(f"Sandbox stderr: {result.stderr[:4000]}")
                if result.stdout:
                    logger.error(f"Sandbox stdout: {result.stdout[:1000]}")
            elif config.verbose:
                # Verbose logging even on success
                logger.info(f"[SANDBOX VERBOSE] Success, exit_code=0")
                if result.stderr:
                    logger.info(f"[SANDBOX VERBOSE] stderr: {result.stderr[:4000]}")
                if result.stdout:
                    logger.info(f"[SANDBOX VERBOSE] stdout: {result.stdout[:1000]}")

            return SandboxResult(
                success=result.returncode == 0,
                exit_code=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                timed_out=False,
            )

        except subprocess.TimeoutExpired as e:
            logger.warning(f"Handler timed out: {handler_ref.module}.{handler_ref.function}")
            return SandboxResult(
                success=False,
                exit_code=137,  # SIGKILL
                stdout=e.stdout or "",
                stderr=e.stderr or "",
                timed_out=True,
            )

        except Exception as e:
            logger.error(f"Error running sandboxed handler: {e}", exc_info=True)
            return SandboxResult(
                success=False,
                exit_code=-1,
                stdout="",
                stderr=str(e),
                timed_out=False,
            )

    def run_direct(
        self,
        method: str,
        handler_ref: HandlerRef,
        params: BaseModel,
    ) -> SandboxResult:
        """
        Run the entrypoint directly without nsjail (for local development).

        This bypasses the sandbox and runs the handler in the current process,
        useful for debugging when nsjail is not available.

        Args:
            method: The JSON-RPC method name (e.g., "event/send")
            handler_ref: Reference to the handler to run
            params: The Pydantic params model to pass to the handler

        Returns:
            SandboxResult with execution outcome
        """
        import sys

        # Build the payload
        payload = {
            "method": method,
            "params_type": type(params).__name__,
            "handler": handler_ref.to_dict(),
            "params": params.model_dump(mode="json"),
        }
        payload_json = json.dumps(payload)

        logger.debug(f"Running handler directly (no sandbox): {handler_ref.module}.{handler_ref.function}")

        try:
            result = subprocess.run(
                [sys.executable, "-m", "sb0.lib.sandbox.entrypoint"],
                input=payload_json,
                capture_output=True,
                text=True,
                timeout=self.config.timeout_seconds,
            )

            return SandboxResult(
                success=result.returncode == 0,
                exit_code=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                timed_out=False,
            )

        except subprocess.TimeoutExpired as e:
            logger.warning(f"Handler timed out: {handler_ref.module}.{handler_ref.function}")
            return SandboxResult(
                success=False,
                exit_code=137,
                stdout=e.stdout or "",
                stderr=e.stderr or "",
                timed_out=True,
            )

        except Exception as e:
            logger.error(f"Error running handler directly: {e}", exc_info=True)
            return SandboxResult(
                success=False,
                exit_code=-1,
                stdout="",
                stderr=str(e),
                timed_out=False,
            )


# Global runner instance
_runner: SandboxRunner | None = None


def get_sandbox_runner() -> SandboxRunner:
    """Get the global sandbox runner."""
    global _runner
    if _runner is None:
        _runner = SandboxRunner()
    return _runner


def reset_sandbox_runner() -> None:
    """Reset the global sandbox runner (primarily for testing)."""
    global _runner
    _runner = None


async def run_handler_sandboxed(
    method: str,
    handler_ref: HandlerRef,
    params: BaseModel,
    workspace_id: str | None = None,
    extra_env: dict[str, str] | None = None,
    task_id: str | None = None,
) -> SandboxResult:
    """
    Async wrapper for running a handler in a sandbox.

    Uses asyncio.to_thread to avoid blocking the event loop.
    If sandboxing is disabled, runs the handler directly.

    Args:
        method: The JSON-RPC method name (e.g., "event/send")
        handler_ref: Reference to the handler to run
        params: The Pydantic params model to pass to the handler
        workspace_id: Optional workspace ID for per-task workspace mounting
        extra_env: Additional environment variables for this invocation
        task_id: Optional task ID for log correlation
    """
    runner = get_sandbox_runner()

    if runner.config.enabled:
        result = await asyncio.to_thread(
            runner.run,
            method,
            handler_ref,
            params,
            workspace_id,
            extra_env,
        )
    else:
        # Run directly without sandbox (for local development)
        result = await asyncio.to_thread(
            runner.run_direct,
            method,
            handler_ref,
            params,
        )

    # Send logs to Nucleus (fire-and-forget, don't block on errors)
    await _send_logs_to_nucleus(method, result, task_id)

    return result


async def _send_logs_to_nucleus(
    method: str,
    result: SandboxResult,
    task_id: str | None,
) -> None:
    """
    Send captured stdout/stderr to Nucleus for log ingestion.

    This is a fire-and-forget operation - errors are logged but don't
    affect the handler result.
    """
    if not result.stdout and not result.stderr:
        return

    try:
        from sb0.lib.logging import get_log_sender

        log_sender = get_log_sender()
        if log_sender:
            await log_sender.send_logs(
                method=method,
                stdout=result.stdout,
                stderr=result.stderr,
                task_id=task_id,
            )
    except Exception as e:
        logger.warning(f"Failed to send logs to Nucleus: {e}")
