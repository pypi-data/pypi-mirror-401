# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .message_author import MessageAuthor

__all__ = ["ClaudeMessageContent"]


class ClaudeMessageContent(BaseModel):
    """Content type for storing raw Claude SDK messages."""

    author: MessageAuthor
    """
    The role of the messages author, in this case `system`, `user`, `assistant`, or
    `tool`.
    """

    message_type: str
    """The type of Claude SDK message this represents"""

    raw_message: Dict[str, object]
    """The complete serialized Claude SDK message"""

    session_id: Optional[str] = None
    """The Claude session ID"""

    type: Literal["claude_message"] = "claude_message"
    """The content type discriminator"""
