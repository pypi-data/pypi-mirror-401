# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel
from .deployment_status import DeploymentStatus

__all__ = ["RegisterContainerResponse"]


class RegisterContainerResponse(BaseModel):
    """Response from container registration."""

    agent_api_key: str
    """API key for the agent"""

    agent_id: str
    """Agent ID"""

    agent_name: str
    """Agent name"""

    deployment_id: str
    """Deployment ID"""

    status: DeploymentStatus
    """Updated deployment status"""
