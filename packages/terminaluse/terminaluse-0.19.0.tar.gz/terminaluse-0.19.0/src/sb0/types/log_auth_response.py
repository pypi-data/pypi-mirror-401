# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["LogAuthResponse"]


class LogAuthResponse(BaseModel):
    """Response from log auth endpoint with JWT for Tinybird access."""

    token: str

    expires_in: int

    tinybird_pipe_url: str
