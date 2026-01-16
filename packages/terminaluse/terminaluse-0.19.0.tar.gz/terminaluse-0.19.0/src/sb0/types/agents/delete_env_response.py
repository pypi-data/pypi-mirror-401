# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel

__all__ = ["DeleteEnvResponse"]


class DeleteEnvResponse(BaseModel):
    """Response after deleting an environment."""

    deleted: bool
    """Whether the environment was deleted"""

    name: str
    """The name of the deleted environment"""
