# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel
from .env_response import EnvResponse

__all__ = ["EnvListResponse"]


class EnvListResponse(BaseModel):
    """Response for listing environments."""

    environments: List[EnvResponse]
    """List of environments"""

    total: int
    """Total count"""
