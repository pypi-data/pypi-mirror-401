# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["WorkspaceFileResponse"]


class WorkspaceFileResponse(BaseModel):
    """File metadata response - adds server-side fields."""

    modified_at: datetime
    """File's last modification time."""

    path: str
    """Relative path within workspace (e.g., 'src/index.ts')."""

    synced_at: datetime
    """When this entry was last synced."""

    checksum: Optional[str] = None
    """SHA256 checksum (None for directories)."""

    content: Optional[str] = None
    """File contents (None for binary/large files)."""

    content_truncated: Optional[bool] = None
    """True if content was truncated due to size."""

    is_binary: Optional[bool] = None
    """True if file is binary."""

    is_directory: Optional[bool] = None
    """Whether this entry is a directory."""

    mime_type: Optional[str] = None
    """MIME type (None for directories)."""

    size_bytes: Optional[int] = None
    """File size in bytes (None for directories)."""
