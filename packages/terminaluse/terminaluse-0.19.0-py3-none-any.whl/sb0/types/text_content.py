# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .text_format import TextFormat
from .message_style import MessageStyle
from .message_author import MessageAuthor
from .file_attachment import FileAttachment

__all__ = ["TextContent"]


class TextContent(BaseModel):
    author: MessageAuthor
    """
    The role of the messages author, in this case `system`, `user`, `assistant`, or
    `tool`.
    """

    content: str
    """The contents of the text message."""

    attachments: Optional[List[FileAttachment]] = None
    """Optional list of file attachments with structured metadata."""

    format: Optional[TextFormat] = None
    """The format of the message.

    This is used by the client to determine how to display the message.
    """

    style: MessageStyle = "static"
    """The style of the message.

    This is used by the client to determine how to display the message.
    """

    type: Literal["text"] = "text"
    """The type of the message, in this case `text`."""
