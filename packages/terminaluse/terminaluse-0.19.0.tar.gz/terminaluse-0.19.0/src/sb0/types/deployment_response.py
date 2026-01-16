# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel
from .version_summary import VersionSummary
from .deployment_status import DeploymentStatus
from .deployment_acp_type import DeploymentAcpType

__all__ = ["DeploymentResponse"]


class DeploymentResponse(BaseModel):
    """Full deployment details including current version."""

    id: str
    """Deployment ID"""

    acp_type: DeploymentAcpType
    """ACP type (SYNC or ASYNC)"""

    agent_id: str
    """Parent agent ID"""

    branch: str
    """Original git branch name"""

    branch_normalized: str
    """DNS-safe branch name"""

    replicas: int
    """Desired replica count"""

    status: DeploymentStatus
    """Deployment status"""

    acp_url: Optional[str] = None
    """ACP server URL (set when container registers)"""

    created_at: Optional[datetime] = None
    """Creation timestamp"""

    current_version: Optional[VersionSummary] = None
    """Abbreviated version info for embedding in deployment responses."""

    retired_at: Optional[datetime] = None
    """When deployment was retired"""

    retired_reason: Optional[str] = None
    """Reason for retirement"""

    updated_at: Optional[datetime] = None
    """Last update timestamp"""
