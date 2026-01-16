# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["WorkspaceFileParam"]


class WorkspaceFileParam(TypedDict, total=False):
    """File metadata - used for both input (sync-complete) and as base for response."""

    modified_at: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]
    """File's last modification time."""

    path: Required[str]
    """Relative path within workspace (e.g., 'src/index.ts')."""

    checksum: Optional[str]
    """SHA256 checksum (None for directories)."""

    content: Optional[str]
    """File contents (None for binary/large files)."""

    content_truncated: bool
    """True if content was truncated due to size."""

    is_binary: bool
    """True if file is binary."""

    is_directory: bool
    """Whether this entry is a directory."""

    mime_type: Optional[str]
    """MIME type (None for directories)."""

    size_bytes: Optional[int]
    """File size in bytes (None for directories)."""
