# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Required, TypedDict

from .workspace_directory import WorkspaceDirectory
from .workspace_file_param import WorkspaceFileParam

__all__ = ["WorkspaceSyncCompleteParams"]


class WorkspaceSyncCompleteParams(TypedDict, total=False):
    direction: Required[str]
    """Sync direction: 'UP' or 'DOWN'."""

    status: Required[str]
    """Sync status: 'SUCCESS' or 'FAILED'."""

    sync_id: Required[str]
    """Unique ID for this sync operation (idempotency key)."""

    workspace_directory: Required[WorkspaceDirectory]
    """Which storage target to access: workspace or dot_claude archive."""

    archive_checksum: Optional[str]
    """SHA256 checksum of the archive."""

    archive_size_bytes: Optional[int]
    """Size of the archive in bytes."""

    files: Optional[Iterable[WorkspaceFileParam]]
    """List of files in the workspace (empty if status is FAILED)."""
