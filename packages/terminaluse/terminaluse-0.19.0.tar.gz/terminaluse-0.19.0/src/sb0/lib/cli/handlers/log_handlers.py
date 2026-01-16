"""Handlers for agent log viewing."""

from __future__ import annotations

import time
from datetime import datetime

import httpx
from rich.console import Console

from sb0 import Sb0
from sb0.lib.utils.logging import make_logger

logger = make_logger(__name__)
console = Console()


class LogsError(Exception):
    """Custom exception for logs-related errors with user-friendly messages."""

    pass


def get_logs(agent_name: str, limit: int = 100) -> None:
    """
    Fetch and display logs for an agent.

    Args:
        agent_name: Name of the agent to get logs for
        limit: Maximum number of log entries to fetch
    """
    client = Sb0()

    # Get JWT from Nucleus
    try:
        auth_response = _get_log_auth_token(client, agent_name)
    except LogsError as e:
        console.print(f"[red]{e}[/red]")
        return
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        return

    # Query Tinybird
    try:
        logs = _query_tinybird(
            auth_response["tinybird_pipe_url"],
            auth_response["token"],
            limit=limit,
        )
    except Exception as e:
        console.print(f"[red]Failed to fetch logs: {e}[/red]")
        return

    if not logs:
        console.print(f"[dim]No logs found for agent '{agent_name}'[/dim]")
        return

    # Display logs in chronological order (API returns DESC, so reverse)
    for log in reversed(logs):
        _print_log_line(log)


def stream_logs(agent_name: str) -> None:
    """
    Stream logs for an agent (polling mode).

    Args:
        agent_name: Name of the agent to stream logs for
    """
    client = Sb0()
    last_timestamp: str | None = None
    token: str | None = None
    tinybird_url: str | None = None
    token_refresh_time: float = 0

    console.print(f"[dim]Streaming logs for agent '{agent_name}'... (Ctrl+C to stop)[/dim]")

    try:
        while True:
            # Refresh JWT every 10 minutes
            if token is None or time.time() - token_refresh_time > 600:
                try:
                    auth_response = _get_log_auth_token(client, agent_name)
                    token = auth_response["token"]
                    tinybird_url = auth_response["tinybird_pipe_url"]
                    token_refresh_time = time.time()
                except LogsError as e:
                    console.print(f"[red]{e}[/red]")
                    return
                except Exception as e:
                    console.print(f"[red]Unexpected error: {e}[/red]")
                    time.sleep(5)
                    continue

            # Query for new logs
            try:
                logs = _query_tinybird(
                    tinybird_url,
                    token,
                    limit=100,
                    since=last_timestamp,
                )

                # Display new logs (in chronological order)
                for log in reversed(logs):
                    _print_log_line(log)
                    # Update last_timestamp to the newest log we've seen
                    log_ts = log.get("timestamp")
                    if log_ts and (last_timestamp is None or log_ts > last_timestamp):
                        last_timestamp = log_ts

            except Exception as e:
                logger.warning(f"Error fetching logs: {e}")

            time.sleep(1)

    except KeyboardInterrupt:
        console.print("\n[dim]Stopped streaming logs[/dim]")


def _get_log_auth_token(client: Sb0, agent_name: str) -> dict:
    """Get JWT token for log access from Nucleus."""
    try:
        response = client._client.get(
            "/logs/auth",
            params={"agent_name": agent_name},
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        status = e.response.status_code
        if status == 404:
            raise LogsError(
                f"Agent '{agent_name}' not found. Use `sb0 agents list` to see available agents."
            ) from e
        elif status == 503:
            raise LogsError(
                "Logging service is temporarily unavailable. Please try again in a few moments."
            ) from e
        elif status == 401:
            raise LogsError(
                "Authentication failed. Please check your API credentials with `sb0 auth status`."
            ) from e
        elif status == 403:
            raise LogsError(
                f"Permission denied. You don't have access to view logs for agent '{agent_name}'."
            ) from e
        else:
            raise LogsError(
                f"Failed to get log access (HTTP {status}). Please try again."
            ) from e


def _query_tinybird(
    pipe_url: str,
    token: str,
    limit: int = 100,
    since: str | None = None,
) -> list[dict]:
    """Query Tinybird for logs."""
    params = {"limit": limit}
    if since:
        params["since"] = since

    with httpx.Client(timeout=30.0) as client:
        response = client.get(
            pipe_url,
            params=params,
            headers={"Authorization": f"Bearer {token}"},
        )
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])


def _print_log_line(log: dict) -> None:
    """Print a single log line with color formatting."""
    timestamp = log.get("timestamp", "")
    source = log.get("source", "")
    message = log.get("message", "")

    # Format timestamp (show HH:MM:SS)
    try:
        if isinstance(timestamp, str):
            # Parse ISO format timestamp
            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            timestamp_str = dt.strftime("%H:%M:%S")
        else:
            timestamp_str = str(timestamp)
    except Exception:
        timestamp_str = timestamp[:8] if len(timestamp) >= 8 else timestamp

    # Color by log level (detected from message content)
    # Python logging formats: "ERROR", "WARNING", "INFO", "DEBUG"
    if " ERROR " in message or message.startswith("ERROR"):
        console.print(f"[dim][{timestamp_str}][/dim] [red]{message}[/red]")
    elif " WARNING " in message or message.startswith("WARNING"):
        console.print(f"[dim][{timestamp_str}][/dim] [yellow]{message}[/yellow]")
    elif source == "server":
        console.print(f"[dim][{timestamp_str}] {message}[/dim]")
    else:
        console.print(f"[dim][{timestamp_str}][/dim] {message}")
