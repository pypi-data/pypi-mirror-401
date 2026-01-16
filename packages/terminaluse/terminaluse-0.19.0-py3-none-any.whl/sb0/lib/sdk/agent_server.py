"""
AgentServer - Simplified API for creating Sb0 agents.

This module provides a clean, simple interface for creating async agents
with optional Temporal support.

Example usage:

    # Basic async agent (no Temporal)
    from sb0.lib.sdk.agent_server import AgentServer

    server = AgentServer()

    @server.on_task_create
    async def handle_task_create(params):
        pass

    @server.on_task_event_send
    async def handle_event(params):
        await adk.messages.create(task_id=params.task.id, content=...)

    @server.on_task_cancel
    async def handle_cancel(params):
        pass


    # Agent with Temporal workflows
    server = AgentServer(temporal=True)
    # Handlers are managed by Temporal workflow
"""

from __future__ import annotations

import os
from typing import Any

from sb0.lib.types.fastacp import AsyncACPConfig, TemporalACPConfig
from sb0.lib.sandbox.config import SandboxConfig
from sb0.lib.sdk.fastacp.fastacp import FastACP
from sb0.lib.sdk.fastacp.impl.temporal_acp import TemporalACP
from sb0.lib.sdk.fastacp.impl.async_base_acp import AsyncBaseACP


class AgentServer:
    """
    Simplified factory for creating Sb0 agent servers.

    All agents are async by default. Use `temporal=True` to enable
    Temporal workflows for reliability and long-running tasks.

    Args:
        temporal: Enable Temporal workflows (default: False)
        temporal_address: Temporal server address (only used if temporal=True)
        plugins: Temporal client plugins (only used if temporal=True)
        interceptors: Temporal worker interceptors (only used if temporal=True)
        sandbox_config: Optional sandbox configuration for nsjail isolation

    Example:
        # Basic agent
        server = AgentServer()

        @server.on_task_event_send
        async def handle_event(params):
            await adk.messages.create(...)

        # Agent with Temporal workflows
        server = AgentServer(temporal=True)

        # Agent with custom sandbox configuration
        from sb0.lib.sandbox.config import SandboxConfig
        server = AgentServer(sandbox_config=SandboxConfig(enabled=False))
    """

    def __init__(
        self,
        temporal: bool = False,
        temporal_address: str | None = None,
        plugins: list[Any] | None = None,
        interceptors: list[Any] | None = None,
        sandbox_config: SandboxConfig | None = None,
    ):
        """Create a new AgentServer instance."""
        self._temporal = temporal
        self._sandbox_config = sandbox_config

        if temporal:
            # Create Temporal-backed server
            config = TemporalACPConfig(
                type="temporal",
                temporal_address=temporal_address or os.getenv("TEMPORAL_ADDRESS", "localhost:7233"),
                plugins=plugins or [],
                interceptors=interceptors or [],
            )
            self._server: AsyncBaseACP | TemporalACP = FastACP.create(
                acp_type="async",
                config=config,
                sandbox_config=sandbox_config,
            )
        else:
            # Create basic async server
            config = AsyncACPConfig(type="base")
            self._server = FastACP.create(
                acp_type="async",
                config=config,
                sandbox_config=sandbox_config,
            )

    @property
    def on_task_create(self):
        """Decorator for handling task creation.

        Called when a new task is created. Use this to initialize
        state or resources needed for the task.

        Example:
            @server.on_task_create
            async def handle_task_create(params: CreateTaskParams):
                logger.info(f"Task created: {params.task.id}")
        """
        return self._server.on_task_create

    @property
    def on_task_event_send(self):
        """Decorator for handling incoming messages/events.

        Called when a user sends a message to the agent. This is
        where you implement your main agent logic.

        Example:
            @server.on_task_event_send
            async def handle_event(params: SendEventParams):
                user_message = params.event.content
                await adk.messages.create(
                    task_id=params.task.id,
                    content=TextContent(author="agent", content="Hello!")
                )
        """
        return self._server.on_task_event_send

    @property
    def on_task_cancel(self):
        """Decorator for handling task cancellation.

        Called when a task is cancelled. Use this to clean up
        resources or state.

        Example:
            @server.on_task_cancel
            async def handle_cancel(params: CancelTaskParams):
                logger.info(f"Task cancelled: {params.task.id}")
        """
        return self._server.on_task_cancel

    # Expose the underlying ASGI app for uvicorn
    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access to the underlying server."""
        return getattr(self._server, name)

    async def __call__(self, scope: dict, receive: Any, send: Any) -> None:
        """ASGI interface - delegate to underlying server.

        This is needed because Python doesn't look up special methods
        like __call__ through __getattr__.
        """
        await self._server(scope, receive, send)
