# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ...._models import BaseModel
from ...deployment_status import DeploymentStatus

__all__ = ["RollbackResponse"]


class RollbackResponse(BaseModel):
    """Response from a rollback operation."""

    deployment_id: str
    """Deployment ID"""

    from_git_hash: str
    """Git hash of the previous version"""

    from_version_id: str
    """Version ID that was rolled back FROM"""

    message: str
    """Human-readable status message"""

    status: DeploymentStatus
    """Updated deployment status"""

    to_git_hash: str
    """Git hash of the target version"""

    to_version_id: str
    """Version ID that was rolled back TO"""
