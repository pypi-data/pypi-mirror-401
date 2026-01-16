# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["WorkspaceListFilesParams"]


class WorkspaceListFilesParams(TypedDict, total=False):
    directory: str
    """Directory prefix to filter results"""

    include_content: bool
    """Include file content in response"""

    limit: int
    """Maximum number of results"""

    mime_type: Optional[str]
    """Filter by MIME type"""

    offset: int
    """Pagination offset"""

    recursive: bool
    """Include subdirectories"""
