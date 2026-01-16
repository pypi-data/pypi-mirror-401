"""Log sender for shipping agent logs to Nucleus."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import ClassVar

import httpx

from sb0.lib.utils.logging import make_logger

logger = make_logger(__name__)


class LogSource(str, Enum):
    """Source of the log entry."""

    STDOUT = "stdout"
    STDERR = "stderr"
    SERVER = "server"


class LogSender:
    """
    Sends agent logs to Nucleus for ingestion into Tinybird.

    This class is responsible for capturing stdout/stderr from sandbox
    execution and shipping them to the Nucleus /logs endpoint.
    """

    # Class-level cached client
    _client: ClassVar[httpx.AsyncClient | None] = None

    def __init__(
        self,
        nucleus_url: str,
        agent_api_key: str | None,
    ):
        """
        Initialize the log sender.

        Args:
            nucleus_url: Base URL for Nucleus API (e.g., "https://api.sb0.dev")
            agent_api_key: API key for agent authentication
        """
        self.nucleus_url = nucleus_url.rstrip("/")
        self.agent_api_key = agent_api_key

    @classmethod
    def _get_client(cls) -> httpx.AsyncClient:
        """Get or create the shared HTTP client."""
        if cls._client is None:
            cls._client = httpx.AsyncClient(
                timeout=httpx.Timeout(
                    connect=10.0,
                    read=30.0,
                    write=30.0,
                    pool=10.0,
                ),
            )
        return cls._client

    @classmethod
    async def close_client(cls) -> None:
        """Close the shared HTTP client."""
        if cls._client:
            await cls._client.aclose()
            cls._client = None

    def is_configured(self) -> bool:
        """Check if the log sender is properly configured."""
        return bool(self.agent_api_key)

    async def send_logs(
        self,
        method: str,
        stdout: str,
        stderr: str,
        task_id: str | None = None,
    ) -> None:
        """
        Send captured stdout/stderr to Nucleus.

        Args:
            method: The RPC method that was called
            stdout: Captured stdout from sandbox execution
            stderr: Captured stderr from sandbox execution
            task_id: Optional task ID for correlation
        """
        if not self.is_configured():
            logger.debug("Log sender not configured, skipping log ingestion")
            return

        logs = self._build_log_entries(method, stdout, stderr, task_id)
        if not logs:
            return

        await self._send_to_nucleus(logs)

    def _build_log_entries(
        self,
        method: str,
        stdout: str,
        stderr: str,
        task_id: str | None,
    ) -> list[dict]:
        """Build log entries from stdout/stderr."""
        logs = []
        timestamp = datetime.now(timezone.utc).isoformat()

        # Process stdout
        for line in stdout.splitlines():
            if line.strip():
                logs.append({
                    "timestamp": timestamp,
                    "task_id": task_id,
                    "method": method,
                    "source": LogSource.STDOUT.value,
                    "message": line,
                })

        # Process stderr
        for line in stderr.splitlines():
            if line.strip():
                logs.append({
                    "timestamp": timestamp,
                    "task_id": task_id,
                    "method": method,
                    "source": LogSource.STDERR.value,
                    "message": line,
                })

        return logs

    async def _send_to_nucleus(self, logs: list[dict]) -> None:
        """Send logs to Nucleus API."""
        client = self._get_client()
        url = f"{self.nucleus_url}/logs"

        try:
            response = await client.post(
                url,
                json={"logs": logs},
                headers={
                    "x-agent-api-key": self.agent_api_key,
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()
            logger.debug(f"Sent {len(logs)} log entries to Nucleus")
        except httpx.HTTPStatusError as e:
            logger.warning(f"Failed to send logs to Nucleus: {e.response.status_code}")
        except Exception as e:
            logger.warning(f"Error sending logs to Nucleus: {e}")


# Global log sender instance
_log_sender: LogSender | None = None


def get_log_sender() -> LogSender | None:
    """
    Get the global log sender instance.

    Returns None if logging is not configured.
    """
    global _log_sender
    if _log_sender is None:
        from sb0.lib.environment_variables import EnvironmentVariables

        env = EnvironmentVariables.refresh()
        if env.SB0_BASE_URL and env.AGENT_API_KEY:
            _log_sender = LogSender(
                nucleus_url=env.SB0_BASE_URL,
                agent_api_key=env.AGENT_API_KEY,
            )
        else:
            logger.debug("Log sender not configured: missing SB0_BASE_URL or AGENT_API_KEY")
    return _log_sender


def reset_log_sender() -> None:
    """Reset the global log sender (primarily for testing)."""
    global _log_sender
    _log_sender = None
