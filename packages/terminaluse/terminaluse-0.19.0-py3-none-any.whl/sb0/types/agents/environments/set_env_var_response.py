# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ...._models import BaseModel

__all__ = ["SetEnvVarResponse"]


class SetEnvVarResponse(BaseModel):
    """Response after setting environment variables."""

    count: int
    """Number of variables set"""

    updated: List[str]
    """Keys that were set"""

    redeployed: Optional[bool] = None
    """Whether a redeploy was triggered"""

    version_id: Optional[str] = None
    """New version ID if redeployed"""
