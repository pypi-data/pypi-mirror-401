# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .deployment_response import DeploymentResponse

__all__ = ["DeploymentListResponse"]


class DeploymentListResponse(BaseModel):
    """Response for listing deployments."""

    deployments: List[DeploymentResponse]
    """List of deployments"""

    total: int
    """Total count"""
