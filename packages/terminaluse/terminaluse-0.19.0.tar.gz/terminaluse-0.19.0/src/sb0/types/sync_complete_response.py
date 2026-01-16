# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["SyncCompleteResponse"]


class SyncCompleteResponse(BaseModel):
    """Response model for sync-complete operation."""

    files_count: int
    """Number of files processed."""

    status: str
    """Result status: 'COMPLETED' or 'ALREADY_PROCESSED'."""

    sync_id: str
    """The sync operation ID (for idempotency)."""

    workspace_id: str
    """The workspace ID."""
