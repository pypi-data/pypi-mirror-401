# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["PresignedURLResponse"]


class PresignedURLResponse(BaseModel):
    """Response model for presigned URL operations."""

    expires_at: datetime
    """When the presigned URL expires."""

    instructions: str
    """Instructions for using the presigned URL."""

    method: str
    """HTTP method to use: 'PUT' for upload, 'GET' for download."""

    url: str
    """The presigned URL for direct GCS upload/download."""

    content_type: Optional[str] = None
    """Content-Type header to use (required for PUT uploads)."""
