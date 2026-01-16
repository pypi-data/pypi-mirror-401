# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel
from .env_response import EnvResponse

__all__ = ["ResolveEnvResponse"]


class ResolveEnvResponse(BaseModel):
    """Response for resolving which environment matches a branch."""

    branch: str
    """The branch that was resolved"""

    environment: EnvResponse
    """The environment that matches the branch"""
