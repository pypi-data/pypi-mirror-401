# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel
from .deployment_status import DeploymentStatus

__all__ = ["RedeployResponse"]


class RedeployResponse(BaseModel):
    """Response from a redeploy operation."""

    deployment_id: str
    """Deployment ID"""

    message: str
    """Human-readable status message"""

    status: DeploymentStatus
    """Deployment status after redeploy"""

    version_id: str
    """New version ID created for redeploy"""
