# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["FileAttachment"]


class FileAttachment(BaseModel):
    """Represents a file attachment in messages."""

    file_id: str
    """The unique ID of the attached file"""

    name: str
    """The name of the file"""

    size: int
    """The size of the file in bytes"""

    type: str
    """The MIME type or content type of the file"""
