# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["RegistryAuthResponse"]


class RegistryAuthResponse(BaseModel):
    """Response containing short-lived registry credentials for pushing agent images."""

    token: str
    """Short-lived OAuth2 access token for docker login"""

    expires_at: datetime
    """Token expiration timestamp (typically ~1 hour from issuance)"""

    registry_url: str
    """Docker registry host URL (e.g., us-east4-docker.pkg.dev)"""

    repository: str
    """Repository path within the registry (e.g., project-id/agents)"""

    username: Optional[str] = None
    """Username for docker login (always 'oauth2accesstoken' for GCP)"""
