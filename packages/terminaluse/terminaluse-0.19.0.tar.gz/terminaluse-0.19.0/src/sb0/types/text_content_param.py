# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Literal, Required, TypedDict

from .text_format import TextFormat
from .message_style import MessageStyle
from .message_author import MessageAuthor
from .file_attachment_param import FileAttachmentParam

__all__ = ["TextContentParam"]


class TextContentParam(TypedDict, total=False):
    author: Required[MessageAuthor]
    """
    The role of the messages author, in this case `system`, `user`, `assistant`, or
    `tool`.
    """

    content: Required[str]
    """The contents of the text message."""

    attachments: Optional[Iterable[FileAttachmentParam]]
    """Optional list of file attachments with structured metadata."""

    format: TextFormat
    """The format of the message.

    This is used by the client to determine how to display the message.
    """

    style: MessageStyle
    """The style of the message.

    This is used by the client to determine how to display the message.
    """

    type: Literal["text"]
    """The type of the message, in this case `text`."""
