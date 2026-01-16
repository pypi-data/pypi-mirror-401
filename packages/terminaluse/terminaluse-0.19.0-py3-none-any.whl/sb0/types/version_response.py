# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel
from .version_status import VersionStatus

__all__ = ["VersionResponse"]


class VersionResponse(BaseModel):
    """Full version details."""

    id: str
    """Version ID"""

    author_email: str
    """Commit author email"""

    author_name: str
    """Commit author name"""

    deployed_at: datetime
    """When this version was deployed"""

    deployment_id: str
    """Parent deployment ID"""

    git_branch: str
    """Git branch name"""

    git_hash: str
    """Git commit hash"""

    image_url: str
    """Container image URL"""

    status: VersionStatus
    """Version lifecycle status"""

    created_at: Optional[datetime] = None
    """Creation timestamp"""

    git_message: Optional[str] = None
    """Git commit message"""

    image_expires_at: Optional[datetime] = None
    """When image expires (for rollback window)"""

    is_dirty: Optional[bool] = None
    """Whether the commit had uncommitted changes"""

    last_rollback_at: Optional[datetime] = None
    """Timestamp when this version was last rolled back TO"""

    replicas: Optional[int] = None
    """Current pod count for this version"""

    retired_at: Optional[datetime] = None
    """When version was retired"""

    rollback_count: Optional[int] = None
    """Number of rollbacks to this version"""

    rolled_back_at: Optional[datetime] = None
    """Timestamp when this version was rolled back FROM"""

    updated_at: Optional[datetime] = None
    """Last update timestamp"""
