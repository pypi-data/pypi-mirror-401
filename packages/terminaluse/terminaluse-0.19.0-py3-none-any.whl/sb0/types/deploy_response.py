# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel
from .deployment_status import DeploymentStatus

__all__ = ["DeployResponse"]


class DeployResponse(BaseModel):
    """Immediate response from deploy request.

    CLI polls GET /deployments/{deployment_id} for status updates.
    """

    agent_id: str
    """Agent ID (created or existing)"""

    deployment_id: str
    """Deployment ID for this branch"""

    message: str
    """Human-readable status message"""

    status: DeploymentStatus
    """Initial deployment status"""

    version_id: str
    """New version ID"""

    tasks_migrated: Optional[int] = None
    """Number of tasks migrated from old version (if any)"""
