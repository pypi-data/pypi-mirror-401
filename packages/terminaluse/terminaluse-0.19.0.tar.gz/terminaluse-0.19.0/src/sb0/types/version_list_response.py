# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .version_response import VersionResponse

__all__ = ["VersionListResponse"]


class VersionListResponse(BaseModel):
    """Response for listing versions of a deployment."""

    deployment_id: str
    """Deployment ID"""

    total: int
    """Total count"""

    versions: List[VersionResponse]
    """List of versions"""
