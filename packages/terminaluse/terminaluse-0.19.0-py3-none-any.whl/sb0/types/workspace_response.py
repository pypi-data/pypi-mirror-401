# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel
from .workspace_status import WorkspaceStatus

__all__ = ["WorkspaceResponse"]


class WorkspaceResponse(BaseModel):
    """Response model for workspace operations."""

    id: str
    """The unique identifier of the workspace."""

    namespace_id: str
    """The namespace this workspace belongs to."""

    status: WorkspaceStatus
    """The current status of the workspace."""

    created_at: Optional[datetime] = None
    """The timestamp when the workspace was created."""

    dot_claude_archive_checksum: Optional[str] = None
    """SHA256 checksum of the ~/.claude archive for detecting changes."""

    dot_claude_archive_size_bytes: Optional[int] = None
    """Size of the ~/.claude archive in bytes after last sync."""

    dot_claude_last_synced_at: Optional[datetime] = None
    """Timestamp of the last successful sync operation for ~/.claude."""

    dot_claude_path: Optional[str] = None
    """GCS path for the workspace's ~/.claude archive."""

    name: Optional[str] = None
    """Optional human-readable name (unique per namespace)."""

    project_id: Optional[str] = None
    """The project this workspace belongs to (optional)."""

    updated_at: Optional[datetime] = None
    """The timestamp when the workspace was last updated."""

    workspace_archive_checksum: Optional[str] = None
    """SHA256 checksum of the workspace archive for detecting changes."""

    workspace_archive_size_bytes: Optional[int] = None
    """Size of the workspace archive in bytes after last sync."""

    workspace_last_synced_at: Optional[datetime] = None
    """Timestamp of the last successful sync operation for the workspace."""

    workspace_path: Optional[str] = None
    """GCS path for the workspace's archive."""
