# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["FileAttachmentParam"]


class FileAttachmentParam(TypedDict, total=False):
    """Represents a file attachment in messages."""

    file_id: Required[str]
    """The unique ID of the attached file"""

    name: Required[str]
    """The name of the file"""

    size: Required[int]
    """The size of the file in bytes"""

    type: Required[str]
    """The MIME type or content type of the file"""
