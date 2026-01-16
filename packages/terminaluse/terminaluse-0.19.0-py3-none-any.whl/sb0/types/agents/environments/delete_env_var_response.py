# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ...._models import BaseModel

__all__ = ["DeleteEnvVarResponse"]


class DeleteEnvVarResponse(BaseModel):
    """Response after deleting an environment variable."""

    deleted: bool
    """Whether the variable was deleted"""

    key: str
    """The key that was deleted"""

    redeployed: Optional[bool] = None
    """Whether a redeploy was triggered"""

    version_id: Optional[str] = None
    """New version ID if redeployed"""
