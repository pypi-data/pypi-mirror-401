# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from .._models import BaseModel
from .workspace_file_response import WorkspaceFileResponse

__all__ = ["WorkspaceListFilesResponse"]


class WorkspaceListFilesResponse(BaseModel):
    """Response model for listing files in a workspace."""

    files: List[WorkspaceFileResponse]
    """List of file entries."""

    total_count: int
    """Total number of matching files."""

    workspace_id: str
    """The workspace ID."""

    synced_at: Optional[datetime] = None
    """When the manifest was last synced."""
