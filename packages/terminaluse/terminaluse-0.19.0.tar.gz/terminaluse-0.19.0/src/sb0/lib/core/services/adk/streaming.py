from __future__ import annotations

import json

from sb0 import AsyncSb0
from sb0.lib.utils.logging import make_logger
from sb0.types.data_content import DataContent
from sb0.types.task_message import (
    TaskMessage,
    TaskMessageContent,
)
from sb0.types.text_content import TextContent
from sb0.types.reasoning_content import ReasoningContent
from sb0.types.task_message_delta import (
    DataDelta,
    TextDelta,
    TaskMessageDelta,
    ToolRequestDelta,
    ToolResponseDelta,
    ReasoningContentDelta,
    ReasoningSummaryDelta,
)
from sb0.types.task_message_update import (
    TaskMessageUpdate,
    StreamTaskMessageDone,
    StreamTaskMessageFull,
    StreamTaskMessageDelta,
    StreamTaskMessageStart,
)
from sb0.types.tool_request_content import ToolRequestContent
from sb0.types.tool_response_content import ToolResponseContent
from sb0.lib.core.adapters.streams.port import StreamRepository

logger = make_logger(__name__)


def _get_stream_topic(task_id: str) -> str:
    return f"task:{task_id}"


class DeltaAccumulator:
    """Accumulates streaming deltas into final content. Supports multiple content types."""

    def __init__(self):
        self._text_deltas: list[TextDelta] = []
        self._data_deltas: list[DataDelta] = []
        self._tool_request_deltas: list[ToolRequestDelta] = []
        self._tool_response_deltas: list[ToolResponseDelta] = []
        self._reasoning_summaries: dict[int, str] = {}
        self._reasoning_contents: dict[int, str] = {}

    def add_delta(self, delta: TaskMessageDelta):
        """Add a delta to the accumulator."""
        if isinstance(delta, TextDelta):
            self._text_deltas.append(delta)
        elif isinstance(delta, DataDelta):
            self._data_deltas.append(delta)
        elif isinstance(delta, ToolRequestDelta):
            self._tool_request_deltas.append(delta)
        elif isinstance(delta, ToolResponseDelta):
            self._tool_response_deltas.append(delta)
        elif isinstance(delta, ReasoningSummaryDelta):
            if delta.summary_index not in self._reasoning_summaries:
                self._reasoning_summaries[delta.summary_index] = ""
            self._reasoning_summaries[delta.summary_index] += delta.summary_delta or ""
        elif isinstance(delta, ReasoningContentDelta):
            if delta.content_index not in self._reasoning_contents:
                self._reasoning_contents[delta.content_index] = ""
            self._reasoning_contents[delta.content_index] += delta.content_delta or ""

    def has_deltas(self) -> bool:
        """Check if any deltas have been accumulated."""
        return bool(
            self._text_deltas
            or self._data_deltas
            or self._tool_request_deltas
            or self._tool_response_deltas
            or self._reasoning_summaries
            or self._reasoning_contents
        )

    def convert_to_content(self) -> TaskMessageContent:
        """Convert accumulated deltas to content. Returns text content if available."""
        if self._text_deltas:
            return TextContent(
                author="agent",
                content="".join(delta.text_delta or "" for delta in self._text_deltas),
            )
        if self._data_deltas:
            data_str = "".join(delta.data_delta or "" for delta in self._data_deltas)
            return DataContent(author="agent", data=json.loads(data_str))
        if self._tool_request_deltas:
            args_str = "".join(delta.arguments_delta or "" for delta in self._tool_request_deltas)
            return ToolRequestContent(
                author="agent",
                tool_call_id=self._tool_request_deltas[0].tool_call_id,
                name=self._tool_request_deltas[0].name,
                arguments=json.loads(args_str),
            )
        if self._tool_response_deltas:
            return ToolResponseContent(
                author="agent",
                tool_call_id=self._tool_response_deltas[0].tool_call_id,
                name=self._tool_response_deltas[0].name,
                content="".join(delta.content_delta or "" for delta in self._tool_response_deltas),
            )
        if self._reasoning_summaries or self._reasoning_contents:
            summary_list = [
                self._reasoning_summaries[i]
                for i in sorted(self._reasoning_summaries.keys())
                if self._reasoning_summaries[i]
            ]
            content_list = [
                self._reasoning_contents[i]
                for i in sorted(self._reasoning_contents.keys())
                if self._reasoning_contents[i]
            ]
            if summary_list or content_list:
                return ReasoningContent(
                    author="agent",
                    summary=summary_list,
                    content=content_list if content_list else None,
                    type="reasoning",
                    style="static",
                )
        return TextContent(author="agent", content="")


class StreamingTaskMessageContext:
    def __init__(
        self,
        task_id: str,
        initial_content: TaskMessageContent,
        sb0_client: AsyncSb0,
        streaming_service: "StreamingService",
    ):
        self.task_id = task_id
        self.initial_content = initial_content
        self.task_message: TaskMessage | None = None
        self._sb0_client = sb0_client
        self._streaming_service = streaming_service
        self._is_closed = False
        self._delta_accumulator = DeltaAccumulator()

    async def __aenter__(self) -> "StreamingTaskMessageContext":
        return await self.open()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self.close()

    async def open(self) -> "StreamingTaskMessageContext":
        self._is_closed = False

        self.task_message = await self._sb0_client.messages.create(
            task_id=self.task_id,
            content=self.initial_content.model_dump(),
            streaming_status="IN_PROGRESS",
        )

        # Send the START event
        start_event = StreamTaskMessageStart(
            parent_task_message=self.task_message,
            content=self.initial_content,
            type="start",
        )
        await self._streaming_service.stream_update(start_event)

        return self

    async def close(self) -> TaskMessage:
        """Close the streaming context."""
        if not self.task_message:
            raise ValueError("Context not properly initialized - no task message")

        if self._is_closed:
            return self.task_message  # Already done

        # Send the DONE event
        done_event = StreamTaskMessageDone(
            parent_task_message=self.task_message,
            type="done",
        )
        await self._streaming_service.stream_update(done_event)

        # Update the task message with the final content
        if self._delta_accumulator.has_deltas():
            self.task_message.content = self._delta_accumulator.convert_to_content()

        await self._sb0_client.messages.update(
            task_id=self.task_id,
            message_id=self.task_message.id,
            content=self.task_message.content.model_dump(),
            streaming_status="DONE",
        )

        # Mark the context as done
        self._is_closed = True
        return self.task_message

    async def stream_update(self, update: TaskMessageUpdate) -> TaskMessageUpdate | None:
        """Stream an update to the repository."""
        if self._is_closed:
            raise ValueError("Context is already done")

        if not self.task_message:
            raise ValueError("Context not properly initialized - no task message")

        if isinstance(update, StreamTaskMessageDelta):
            if update.delta is not None:
                self._delta_accumulator.add_delta(update.delta)

        result = await self._streaming_service.stream_update(update)

        if isinstance(update, StreamTaskMessageDone):
            await self.close()
            return update
        elif isinstance(update, StreamTaskMessageFull):
            await self._sb0_client.messages.update(
                task_id=self.task_id,
                message_id=update.parent_task_message.id,  # type: ignore[union-attr]
                content=update.content.model_dump(),
                streaming_status="DONE",
            )
            # Send done event to signal stream completion to UI
            done_event = StreamTaskMessageDone(
                parent_task_message=update.parent_task_message,
                type="done",
            )
            await self._streaming_service.stream_update(done_event)
            self._is_closed = True
        return result


class StreamingService:
    def __init__(
        self,
        sb0_client: AsyncSb0,
        stream_repository: StreamRepository,
    ):
        self._sb0_client = sb0_client
        self._stream_repository = stream_repository

    def streaming_task_message_context(
        self,
        task_id: str,
        initial_content: TaskMessageContent,
    ) -> StreamingTaskMessageContext:
        return StreamingTaskMessageContext(
            task_id=task_id,
            initial_content=initial_content,
            sb0_client=self._sb0_client,
            streaming_service=self,
        )

    async def stream_update(self, update: TaskMessageUpdate) -> TaskMessageUpdate | None:
        """
        Stream an update to the repository.

        Args:
            update: The update to stream

        Returns:
            True if event was streamed successfully, False otherwise
        """
        stream_topic = _get_stream_topic(update.parent_task_message.task_id)  # type: ignore[union-attr]

        try:
            await self._stream_repository.send_event(
                topic=stream_topic,
                event=update.model_dump(mode="json"),  # type: ignore
            )
            return update
        except Exception as e:
            logger.exception(f"Failed to stream event: {e}")
            return None
