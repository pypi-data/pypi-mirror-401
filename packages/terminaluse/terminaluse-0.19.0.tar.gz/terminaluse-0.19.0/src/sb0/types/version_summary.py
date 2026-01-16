# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel
from .version_status import VersionStatus

__all__ = ["VersionSummary"]


class VersionSummary(BaseModel):
    """Abbreviated version info for embedding in deployment responses."""

    id: str
    """Version ID"""

    deployed_at: datetime
    """When this version was deployed"""

    git_hash: str
    """Git commit hash"""

    status: VersionStatus
    """Version lifecycle status"""

    git_message: Optional[str] = None
    """Git commit message"""
