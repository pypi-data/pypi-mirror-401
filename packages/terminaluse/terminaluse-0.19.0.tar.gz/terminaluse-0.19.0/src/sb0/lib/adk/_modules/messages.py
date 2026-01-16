# ruff: noqa: I001
from __future__ import annotations
from datetime import timedelta
from typing import Any, Union

from temporalio.common import RetryPolicy

from sb0.lib.adk.utils._modules.client import create_async_sb0_client
from sb0.lib.core.adapters.streams.adapter_redis import RedisStreamRepository
from sb0.lib.core.claude.delta_accumulator import AccumulatorRegistry
from sb0.lib.core.claude.message_converter import (
    claude_message_to_content,
    claude_message_to_platform_contents,
    blocks_to_platform_contents,
    get_session_id,
)
from sb0.lib.core.services.adk.messages import MessagesService
from sb0.lib.core.services.adk.streaming import StreamingService
from sb0.lib.core.temporal.activities.activity_helpers import ActivityHelpers
from sb0.lib.core.temporal.activities.adk.messages_activities import (
    CreateMessageParams,
    CreateMessagesBatchParams,
    ListMessagesParams,
    MessagesActivityName,
    UpdateMessageParams,
    UpdateMessagesBatchParams,
)
from sb0.lib.core.tracing.tracer import AsyncTracer
from sb0.lib.utils.logging import make_logger
from sb0.lib.utils.temporal import in_temporal_workflow
from sb0.types.task_message import TaskMessage, TaskMessageContent
from sb0.types.claude_message_content import ClaudeMessageContent
from sb0.types.task_message_delta import TaskMessageDelta
from sb0.types.task_message_update import StreamTaskMessageDelta, StreamTaskMessageFull
from sb0.types.text_content import TextContent
from claude_agent_sdk.types import (
    StreamEvent,
    AssistantMessage,
    ResultMessage,
    Message as ClaudeMessage,
)

logger = make_logger(__name__)
DEFAULT_RETRY_POLICY = RetryPolicy(maximum_attempts=1)


class MessagesModule:
    """Module for managing task messages. Supports both platform and Claude SDK message types."""

    def __init__(self, messages_service: MessagesService | None = None):
        if messages_service is None:
            sb0_client = create_async_sb0_client()
            stream_repository = RedisStreamRepository()
            streaming_service = StreamingService(sb0_client=sb0_client, stream_repository=stream_repository)
            tracer = AsyncTracer(sb0_client)
            self._messages_service = MessagesService(
                sb0_client=sb0_client, streaming_service=streaming_service, tracer=tracer
            )
        else:
            self._messages_service = messages_service
        self._streaming_contexts: dict[str, Any] = {}
        self._accumulator_registry = AccumulatorRegistry.get_instance()

    async def create(
        self,
        task_id: str,
        content: Union[TaskMessageContent, ClaudeMessage],
        emit_updates: bool = True,
        store_raw_claude_message: bool = False,
        trace_id: str | None = None,
        parent_span_id: str | None = None,
        start_to_close_timeout: timedelta = timedelta(seconds=5),
        heartbeat_timeout: timedelta = timedelta(seconds=5),
        retry_policy: RetryPolicy = DEFAULT_RETRY_POLICY,
    ) -> TaskMessage | list[TaskMessage] | None:
        """Create a message. Accepts platform TaskMessageContent or Claude SDK message types."""
        # Check if this is a Claude SDK message type
        if isinstance(content, ClaudeMessage):
            return await self._handle_claude_message(
                task_id=task_id,
                message=content,
                emit_updates=emit_updates,
                store_raw_claude_message=store_raw_claude_message,
                trace_id=trace_id,
                parent_span_id=parent_span_id,
                start_to_close_timeout=start_to_close_timeout,
                heartbeat_timeout=heartbeat_timeout,
                retry_policy=retry_policy,
            )

        # Standard platform content type handling
        return await self._create_platform_message(
            task_id=task_id,
            content=content,
            emit_updates=emit_updates,
            trace_id=trace_id,
            parent_span_id=parent_span_id,
            start_to_close_timeout=start_to_close_timeout,
            heartbeat_timeout=heartbeat_timeout,
            retry_policy=retry_policy,
        )

    async def _create_platform_message(
        self,
        task_id: str,
        content: TaskMessageContent,
        emit_updates: bool = True,
        trace_id: str | None = None,
        parent_span_id: str | None = None,
        start_to_close_timeout: timedelta = timedelta(seconds=5),
        heartbeat_timeout: timedelta = timedelta(seconds=5),
        retry_policy: RetryPolicy = DEFAULT_RETRY_POLICY,
    ) -> TaskMessage:
        """
        Create a new message for a task.

        Args:
            task_id (str): The ID of the task.
            message (TaskMessage): The message to create.
            trace_id (Optional[str]): The trace ID for tracing.
            parent_span_id (Optional[str]): The parent span ID for tracing.
            start_to_close_timeout (timedelta): The start to close timeout.
            heartbeat_timeout (timedelta): The heartbeat timeout.
            retry_policy (RetryPolicy): The retry policy.

        Returns:
            TaskMessageEntity: The created message.
        """
        params = CreateMessageParams(
            trace_id=trace_id,
            parent_span_id=parent_span_id,
            task_id=task_id,
            content=content,
            emit_updates=emit_updates,
        )
        if in_temporal_workflow():
            return await ActivityHelpers.execute_activity(
                activity_name=MessagesActivityName.CREATE_MESSAGE,
                request=params,
                response_type=TaskMessage,
                start_to_close_timeout=start_to_close_timeout,
                retry_policy=retry_policy,
                heartbeat_timeout=heartbeat_timeout,
            )
        return await self._messages_service.create_message(task_id=task_id, content=content, emit_updates=emit_updates)

    async def _handle_claude_message(
        self,
        task_id: str,
        message: ClaudeMessage,
        emit_updates: bool = True,
        store_raw_claude_message: bool = False,
        trace_id: str | None = None,
        parent_span_id: str | None = None,
        start_to_close_timeout: timedelta = timedelta(seconds=5),
        heartbeat_timeout: timedelta = timedelta(seconds=5),
        retry_policy: RetryPolicy = DEFAULT_RETRY_POLICY,
    ) -> TaskMessage | list[TaskMessage] | None:
        """Route Claude SDK messages to appropriate handlers."""
        kwargs = dict(
            task_id=task_id,
            emit_updates=emit_updates,
            store_raw_claude_message=store_raw_claude_message,
            trace_id=trace_id,
            parent_span_id=parent_span_id,
            start_to_close_timeout=start_to_close_timeout,
            heartbeat_timeout=heartbeat_timeout,
            retry_policy=retry_policy,
        )

        if isinstance(message, StreamEvent):
            return await self._handle_stream_event(event=message, **kwargs)

        if isinstance(message, ResultMessage):
            result = await self._store_claude_message(message=message, **kwargs)
            if session_id := get_session_id(message):
                self._accumulator_registry.cleanup(task_id, session_id)
                await self._cleanup_streaming_context(task_id, session_id)
            return result

        # Skip AssistantMessage if streaming session is active
        if isinstance(message, AssistantMessage) and self._accumulator_registry.has_active_session(task_id):
            return None

        return await self._store_claude_message(message=message, **kwargs)

    async def _handle_stream_event(
        self,
        task_id: str,
        event: ClaudeMessage,
        emit_updates: bool = True,
        store_raw_claude_message: bool = False,
        trace_id: str | None = None,
        parent_span_id: str | None = None,
        start_to_close_timeout: timedelta = timedelta(seconds=5),
        heartbeat_timeout: timedelta = timedelta(seconds=5),
        retry_policy: RetryPolicy = DEFAULT_RETRY_POLICY,
    ) -> TaskMessage | list[TaskMessage] | None:
        """Handle streaming events with accumulation.

        Accumulates deltas and streams them to UI. When message is complete,
        converts to platform types and stores them.
        """
        session_id = get_session_id(event)
        if not session_id:
            logger.warning("StreamEvent missing session_id, cannot accumulate")
            return None

        # Get or create accumulator for this session
        accumulator = self._accumulator_registry.get_or_create(task_id, session_id)

        # Process event and get any delta to stream
        delta = accumulator.process_event(event)

        # Stream delta to UI if available and updates are enabled
        if delta and emit_updates:
            await self._stream_delta(task_id, session_id, delta)

        # If message is complete, store it
        if accumulator.is_complete():
            # Build the complete message data
            message_dict = accumulator.build_message_dict()

            # Convert accumulated content to platform types using shared function
            content_blocks = accumulator.get_content_blocks()
            platform_contents = blocks_to_platform_contents(content_blocks, author="agent")

            # Finalize the streaming context with text content if available
            text_parts = [b.get("text", "") for b in content_blocks if b.get("type") == "text"]
            text_content = "\n".join(text_parts) if text_parts else None
            if text_content:
                final_content = TextContent(
                    author="agent",
                    content=text_content,
                    format="markdown",
                )
                await self._finalize_streaming_context(task_id, session_id, final_content)
            else:
                await self._cleanup_streaming_context(task_id, session_id)

            # Store non-text platform messages (text is already handled by streaming context)
            stored_messages: list[TaskMessage] = []

            # Optionally store raw ClaudeMessageContent first
            if store_raw_claude_message:
                raw_content = self._build_claude_message_content(
                    message_dict=message_dict,
                    session_id=session_id,
                )
                raw_msg = await self._create_platform_message(
                    task_id=task_id,
                    content=raw_content,
                    emit_updates=False,  # Don't emit for raw storage
                    trace_id=trace_id,
                    parent_span_id=parent_span_id,
                    start_to_close_timeout=start_to_close_timeout,
                    heartbeat_timeout=heartbeat_timeout,
                    retry_policy=retry_policy,
                )
                stored_messages.append(raw_msg)

            # Store non-text platform content types (TextContent handled by streaming context)
            # Tool requests/responses need to emit updates so they appear in the UI
            for content in platform_contents:
                if isinstance(content, TextContent):
                    continue  # Skip - already handled by streaming context finalization
                msg = await self._create_platform_message(
                    task_id=task_id,
                    content=content,
                    emit_updates=emit_updates,  # Emit tool content to UI
                    trace_id=trace_id,
                    parent_span_id=parent_span_id,
                    start_to_close_timeout=start_to_close_timeout,
                    heartbeat_timeout=heartbeat_timeout,
                    retry_policy=retry_policy,
                )
                stored_messages.append(msg)

            # Return single message or list
            if len(stored_messages) == 1:
                return stored_messages[0]
            return stored_messages if stored_messages else None

        return None  # Partial event, no storage yet

    def _build_claude_message_content(
        self,
        message_dict: dict[str, Any],
        session_id: str,
    ) -> ClaudeMessageContent:
        """Build a ClaudeMessageContent from accumulated data."""
        return ClaudeMessageContent(
            message_type="AssistantMessage",
            raw_message=message_dict,
            session_id=session_id,
            author="agent",
        )

    async def _store_claude_message(
        self,
        task_id: str,
        message: ClaudeMessage,
        emit_updates: bool = True,
        store_raw_claude_message: bool = False,
        trace_id: str | None = None,
        parent_span_id: str | None = None,
        start_to_close_timeout: timedelta = timedelta(seconds=5),
        heartbeat_timeout: timedelta = timedelta(seconds=5),
        retry_policy: RetryPolicy = DEFAULT_RETRY_POLICY,
    ) -> TaskMessage | list[TaskMessage] | None:
        """Convert Claude SDK message to platform types and store."""
        platform_contents = claude_message_to_platform_contents(message)
        stored_messages: list[TaskMessage] = []
        create_kwargs = dict(
            task_id=task_id,
            trace_id=trace_id,
            parent_span_id=parent_span_id,
            start_to_close_timeout=start_to_close_timeout,
            heartbeat_timeout=heartbeat_timeout,
            retry_policy=retry_policy,
        )

        if store_raw_claude_message:
            raw_msg = await self._create_platform_message(
                content=claude_message_to_content(message), emit_updates=False, **create_kwargs
            )
            stored_messages.append(raw_msg)

        for content in platform_contents:
            stored_messages.append(
                await self._create_platform_message(content=content, emit_updates=emit_updates, **create_kwargs)
            )

        return stored_messages[0] if len(stored_messages) == 1 else (stored_messages or None)

    async def _stream_delta(
        self,
        task_id: str,
        session_id: str,
        delta: TaskMessageDelta,
    ) -> None:
        """Stream a delta to the UI via the streaming service."""
        try:
            # Get or create streaming context for this session
            context_key = f"{task_id}:{session_id}"
            if context_key not in self._streaming_contexts:
                # Create a new streaming context with initial content
                initial_content = TextContent(
                    author="agent",
                    content="",
                    format="markdown",
                )
                ctx = await self._messages_service._streaming_service.streaming_task_message_context(
                    task_id=task_id,
                    initial_content=initial_content,
                ).__aenter__()
                self._streaming_contexts[context_key] = ctx

            ctx = self._streaming_contexts[context_key]

            # Stream the delta
            await ctx.stream_update(
                StreamTaskMessageDelta(
                    parent_task_message=ctx.task_message,
                    delta=delta,
                    type="delta",
                )
            )
        except Exception as e:
            logger.warning(f"Failed to stream delta: {e}")

    async def _finalize_streaming_context(
        self,
        task_id: str,
        session_id: str,
        final_content: TaskMessageContent,
    ) -> None:
        """Finalize and close the streaming context."""
        context_key = f"{task_id}:{session_id}"
        ctx = self._streaming_contexts.pop(context_key, None)
        if ctx:
            try:
                # Send final full content
                await ctx.stream_update(
                    StreamTaskMessageFull(
                        parent_task_message=ctx.task_message,
                        content=final_content,
                        type="full",
                    )
                )
                await ctx.close()
            except Exception as e:
                logger.warning(f"Failed to finalize streaming context: {e}")

    async def _cleanup_streaming_context(
        self,
        task_id: str,
        session_id: str,
    ) -> None:
        """Cleanup streaming context without finalizing."""
        context_key = f"{task_id}:{session_id}"
        ctx = self._streaming_contexts.pop(context_key, None)
        if ctx:
            try:
                await ctx.close()
            except Exception as e:
                logger.warning(f"Failed to cleanup streaming context: {e}")

    async def update(
        self,
        task_id: str,
        message_id: str,
        content: TaskMessageContent,
        trace_id: str | None = None,
        parent_span_id: str | None = None,
        start_to_close_timeout: timedelta = timedelta(seconds=5),
        heartbeat_timeout: timedelta = timedelta(seconds=5),
        retry_policy: RetryPolicy = DEFAULT_RETRY_POLICY,
    ) -> TaskMessage:
        """
        Update a message for a task.

        Args:
            task_id (str): The ID of the task.
            message_id (str): The ID of the message.
            message (TaskMessage): The message to update.
            start_to_close_timeout (timedelta): The start to close timeout.
            heartbeat_timeout (timedelta): The heartbeat timeout.
            retry_policy (RetryPolicy): The retry policy.

        Returns:
            TaskMessageEntity: The updated message.
        """
        params = UpdateMessageParams(
            task_id=task_id, message_id=message_id, content=content, trace_id=trace_id, parent_span_id=parent_span_id
        )
        if in_temporal_workflow():
            return await ActivityHelpers.execute_activity(
                activity_name=MessagesActivityName.UPDATE_MESSAGE,
                request=params,
                response_type=TaskMessage,
                start_to_close_timeout=start_to_close_timeout,
                retry_policy=retry_policy,
                heartbeat_timeout=heartbeat_timeout,
            )
        return await self._messages_service.update_message(task_id=task_id, message_id=message_id, content=content)

    async def create_batch(
        self,
        task_id: str,
        contents: list[TaskMessageContent],
        emit_updates: bool = True,
        trace_id: str | None = None,
        parent_span_id: str | None = None,
        start_to_close_timeout: timedelta = timedelta(seconds=5),
        heartbeat_timeout: timedelta = timedelta(seconds=5),
        retry_policy: RetryPolicy = DEFAULT_RETRY_POLICY,
    ) -> list[TaskMessage]:
        """
        Create a batch of messages for a task.

        Args:
            task_id (str): The ID of the task.
            messages (List[TaskMessage]): The messages to create.
            start_to_close_timeout (timedelta): The start to close timeout.
            heartbeat_timeout (timedelta): The heartbeat timeout.
            retry_policy (RetryPolicy): The retry policy.

        Returns:
            List[TaskMessageEntity]: The created messages.
        """
        params = CreateMessagesBatchParams(
            task_id=task_id,
            contents=contents,
            emit_updates=emit_updates,
            trace_id=trace_id,
            parent_span_id=parent_span_id,
        )
        if in_temporal_workflow():
            return await ActivityHelpers.execute_activity(
                activity_name=MessagesActivityName.CREATE_MESSAGES_BATCH,
                request=params,
                response_type=list[TaskMessage],
                start_to_close_timeout=start_to_close_timeout,
                retry_policy=retry_policy,
                heartbeat_timeout=heartbeat_timeout,
            )
        return await self._messages_service.create_messages_batch(
            task_id=task_id, contents=contents, emit_updates=emit_updates
        )

    async def update_batch(
        self,
        task_id: str,
        updates: dict[str, TaskMessageContent],
        trace_id: str | None = None,
        parent_span_id: str | None = None,
        start_to_close_timeout: timedelta = timedelta(seconds=5),
        heartbeat_timeout: timedelta = timedelta(seconds=5),
        retry_policy: RetryPolicy = DEFAULT_RETRY_POLICY,
    ) -> list[TaskMessage]:
        """
        Update a batch of messages for a task.

        Args:
            task_id (str): The ID of the task.
            updates (Dict[str, TaskMessage]): The updates to apply to the messages.
            start_to_close_timeout (timedelta): The start to close timeout.
            heartbeat_timeout (timedelta): The heartbeat timeout.
            retry_policy (RetryPolicy): The retry policy.

        Returns:
            List[TaskMessageEntity]: The updated messages.
        """
        params = UpdateMessagesBatchParams(
            task_id=task_id, updates=updates, trace_id=trace_id, parent_span_id=parent_span_id
        )
        if in_temporal_workflow():
            return await ActivityHelpers.execute_activity(
                activity_name=MessagesActivityName.UPDATE_MESSAGES_BATCH,
                request=params,
                response_type=list[TaskMessage],
                start_to_close_timeout=start_to_close_timeout,
                retry_policy=retry_policy,
                heartbeat_timeout=heartbeat_timeout,
            )
        return await self._messages_service.update_messages_batch(task_id=task_id, updates=updates)

    async def list(
        self,
        task_id: str,
        limit: int | None = None,
        trace_id: str | None = None,
        parent_span_id: str | None = None,
        start_to_close_timeout: timedelta = timedelta(seconds=5),
        heartbeat_timeout: timedelta = timedelta(seconds=5),
        retry_policy: RetryPolicy = DEFAULT_RETRY_POLICY,
    ) -> list[TaskMessage]:
        """
        List messages for a task.

        Args:
            task_id (str): The ID of the task.
            limit (Optional[int]): The maximum number of messages to return.
            start_to_close_timeout (timedelta): The start to close timeout.
            heartbeat_timeout (timedelta): The heartbeat timeout.
            retry_policy (RetryPolicy): The retry policy.

        Returns:
            List[TaskMessageEntity]: The list of messages.
        """
        params = ListMessagesParams(task_id=task_id, limit=limit, trace_id=trace_id, parent_span_id=parent_span_id)
        if in_temporal_workflow():
            return await ActivityHelpers.execute_activity(
                activity_name=MessagesActivityName.LIST_MESSAGES,
                request=params,
                response_type=list[TaskMessage],
                start_to_close_timeout=start_to_close_timeout,
                retry_policy=retry_policy,
                heartbeat_timeout=heartbeat_timeout,
            )
        return await self._messages_service.list_messages(task_id=task_id, limit=limit)
