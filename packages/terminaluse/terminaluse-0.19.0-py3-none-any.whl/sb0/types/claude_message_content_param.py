# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Literal, Required, TypedDict

from .message_author import MessageAuthor

__all__ = ["ClaudeMessageContentParam"]


class ClaudeMessageContentParam(TypedDict, total=False):
    """Content type for storing raw Claude SDK messages."""

    author: Required[MessageAuthor]
    """
    The role of the messages author, in this case `system`, `user`, `assistant`, or
    `tool`.
    """

    message_type: Required[str]
    """The type of Claude SDK message this represents"""

    raw_message: Required[Dict[str, object]]
    """The complete serialized Claude SDK message"""

    session_id: Optional[str]
    """The Claude session ID"""

    type: Literal["claude_message"]
    """The content type discriminator"""
