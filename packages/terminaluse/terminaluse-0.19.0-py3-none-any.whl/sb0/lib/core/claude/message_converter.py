"""Message converter for Claude SDK types to platform types.

This module provides utilities to convert Claude Agent SDK message types
to the platform's TaskMessageContent types.

Key functions:
- `claude_message_to_platform_contents()`: Converts a Claude message to a list
  of platform content types (TextContent, ToolRequestContent, etc.)
- `claude_message_to_content()`: Converts to ClaudeMessageContent for raw storage.
- `blocks_to_platform_contents()`: Converts content blocks to platform types.
"""

from __future__ import annotations

import dataclasses
from typing import Any

from claude_agent_sdk.types import (
    Message as ClaudeMessage,
    TextBlock,
    StreamEvent,
    UserMessage,
    ToolUseBlock,
    ResultMessage,
    SystemMessage,
    ThinkingBlock,
    ToolResultBlock,
    AssistantMessage,
)

from sb0.types import (
    DataContent,
    TextContent,
    MessageAuthor,
    ReasoningContent,
    TaskMessageContent,
    ToolRequestContent,
    ToolResponseContent,
    ClaudeMessageContent,
)


def claude_message_to_content(message: ClaudeMessage) -> ClaudeMessageContent:
    """Convert a Claude SDK message to ClaudeMessageContent dict."""
    # Determine author based on message type
    if isinstance(message, UserMessage):
        author = "user"
    else:
        # AssistantMessage, SystemMessage, ResultMessage, or any other type
        author = "agent"

    return ClaudeMessageContent(
        author=author,
        message_type=message.__class__.__name__,
        raw_message=dataclasses.asdict(message),
        session_id=get_session_id(message),
    )


def blocks_to_platform_contents(blocks: list[Any], author: MessageAuthor = "agent") -> list[TaskMessageContent]:
    """Convert content blocks to platform TaskMessageContent types.

    This is the shared conversion function used by both streaming accumulation
    and direct message conversion.

    Args:
        blocks: List of content blocks (dicts or SDK objects)
        author: The message author ("agent" or "user")

    Returns:
        List of TaskMessageContent items
    """
    contents: list[TaskMessageContent] = []
    text_parts: list[str] = []
    thinking_parts: list[str] = []
    thinking_summaries: list[str] = []

    for block in blocks:
        # Handle SDK block types with isinstance
        if isinstance(block, TextBlock):
            text_parts.append(block.text)

        elif isinstance(block, ThinkingBlock):
            thinking_parts.append(block.thinking)
            summary = block.thinking[:100] + "..." if len(block.thinking) > 100 else block.thinking
            thinking_summaries.append(summary)

        elif isinstance(block, ToolUseBlock):
            contents.append(
                ToolRequestContent(
                    author=author,
                    tool_call_id=block.id,
                    name=block.name,
                    arguments=block.input,
                )
            )

        elif isinstance(block, ToolResultBlock):
            tool_content = block.content
            if isinstance(tool_content, list):
                result_text = "".join(item.text for item in tool_content if isinstance(item, TextBlock))
                tool_content = result_text if result_text else str(block.content)
            contents.append(
                ToolResponseContent(
                    author=author,
                    tool_call_id=block.tool_use_id,
                    name="",
                    content=tool_content,
                )
            )

        elif isinstance(block, dict):
            # Handle dict-form blocks (from streaming accumulation)
            block_type = block.get("type", "")

            if block_type == "text":
                text_parts.append(block.get("text", ""))

            elif block_type == "thinking":
                thinking_content = block.get("thinking", "")
                thinking_parts.append(thinking_content)
                summary = thinking_content[:100] + "..." if len(thinking_content) > 100 else thinking_content
                thinking_summaries.append(summary)

            elif block_type == "tool_use":
                contents.append(
                    ToolRequestContent(
                        author=author,
                        tool_call_id=block.get("id", ""),
                        name=block.get("name", ""),
                        arguments=block.get("input", {}),
                    )
                )

            elif block_type == "tool_result":
                contents.append(
                    ToolResponseContent(
                        author=author,
                        tool_call_id=block.get("tool_use_id", ""),
                        name="",
                        content=block.get("content"),
                    )
                )

    # Create ReasoningContent for thinking blocks (insert first)
    if thinking_parts:
        contents.insert(
            0,
            ReasoningContent(
                author=author,
                summary=thinking_summaries,
                content=thinking_parts,
            ),
        )

    # Create TextContent for combined text (insert first, after reasoning)
    if text_parts:
        contents.insert(
            0,
            TextContent(
                author=author,
                content="\n".join(text_parts),
                format="markdown" if author == "agent" else "plain",
            ),
        )

    return contents


def claude_message_to_platform_contents(message: ClaudeMessage) -> list[TaskMessageContent]:
    """Convert a Claude SDK message to a list of platform TaskMessageContent types.

    This is the PRIMARY conversion function for UI compatibility. It produces
    the existing platform types (TextContent, ToolRequestContent, etc.) that
    the UI and downstream systems expect.

    Args:
        message: Any Claude SDK message type

    Returns:
        List of TaskMessageContent items (may be empty for some message types)
    """
    # Handle AssistantMessage
    if isinstance(message, AssistantMessage):
        content = getattr(message, "content", [])
        if isinstance(content, str):
            return [TextContent(author="agent", content=content, format="markdown")] if content else []
        return blocks_to_platform_contents(content, author="agent")

    # Handle UserMessage
    if isinstance(message, UserMessage):
        content = getattr(message, "content", "")
        if isinstance(content, str):
            return [TextContent(author="user", content=content, format="plain")] if content else []
        return blocks_to_platform_contents(content, author="user")

    # Handle SystemMessage
    if isinstance(message, SystemMessage):
        if message.subtype == "init":
            return []  # Skip internal system messages
        return [DataContent(author="agent", data=dataclasses.asdict(message))]

    # Handle ResultMessage
    if isinstance(message, ResultMessage):
        return [DataContent(author="agent", data=dataclasses.asdict(message))]

    return []


def is_claude_message(obj: Any) -> bool:
    """Check if an object is a Claude SDK message type."""
    return isinstance(obj, ClaudeMessage)


def is_stream_event(obj: Any) -> bool:
    """Check if an object is a StreamEvent."""
    return isinstance(obj, StreamEvent)


def is_result_message(obj: Any) -> bool:
    """Check if an object is a ResultMessage."""
    return isinstance(obj, ResultMessage)


def get_session_id(message: Any) -> str | None:
    """Extract session_id from a Claude message."""
    if isinstance(message, (StreamEvent, ResultMessage)):
        return message.session_id
    if isinstance(message, SystemMessage) and message.subtype == "init":
        return message.data.get("session_id")
    return None
