from __future__ import annotations

from typing import Any
from typing_extensions import override

from sb0.lib.types.acp import (
    SendEventParams,
    CancelTaskParams,
    CreateTaskParams,
)
from sb0.lib.utils.logging import make_logger
from sb0.lib.sandbox.config import SandboxConfig
from sb0.lib.adk.utils._modules.client import create_async_sb0_client
from sb0.lib.sdk.fastacp.base.base_acp_server import BaseACPServer

logger = make_logger(__name__)


class AsyncBaseACP(BaseACPServer):
    """
    AsyncBaseACP implementation - a synchronous ACP that provides basic functionality
    without any special async orchestration like Temporal.

    This implementation provides simple synchronous processing of tasks
    and is suitable for basic agent implementations.
    """

    def __init__(self, sandbox_config: SandboxConfig | None = None):
        super().__init__(sandbox_config=sandbox_config)
        self._setup_handlers()
        self._sb0_client = create_async_sb0_client()

    @classmethod
    @override
    def create(cls, sandbox_config: SandboxConfig | None = None, **kwargs: Any) -> "AsyncBaseACP":
        """Create and initialize AsyncBaseACP instance

        Args:
            sandbox_config: Optional sandbox configuration
            **kwargs: Additional configuration parameters

        Returns:
            Initialized AsyncBaseACP instance
        """
        logger.info("Initializing AsyncBaseACP instance")
        instance = cls(sandbox_config=sandbox_config)
        logger.info("AsyncBaseACP instance initialized with default handlers")
        return instance

    @override
    def _setup_handlers(self):
        """Set up default handlers for sync operations"""

        @self.on_task_create
        async def handle_create_task(params: CreateTaskParams) -> None:  # type: ignore[unused-function]
            """Default create task handler - logs the task"""
            logger.info(f"AsyncBaseACP creating task {params.task.id}")

        @self.on_task_event_send
        async def handle_event_send(params: SendEventParams) -> None:  # type: ignore[unused-function]
            """Default event handler - logs the event"""
            logger.info(
                f"AsyncBaseACP received event for task {params.task.id}: {params.event.id},"
                f"content: {params.event.content}"
            )
            # TODO: Implement event handling logic here

            # Implement cursor commit logic here
            await self._sb0_client.tracker.update(
                tracker_id=params.task.id,
                last_processed_event_id=params.event.id,
            )

        @self.on_task_cancel
        async def handle_cancel(params: CancelTaskParams) -> None:  # type: ignore[unused-function]
            """Default cancel handler - logs the cancellation"""
            logger.info(f"AsyncBaseACP canceling task {params.task.id}")


AgenticBaseACP = AsyncBaseACP
