# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from ...._models import BaseModel
from .deployed_secret_key import DeployedSecretKey

__all__ = ["DeployedSecretsResponse"]


class DeployedSecretsResponse(BaseModel):
    """Response for deployed secrets (from Version.secrets_snapshot)."""

    deployed_at: datetime
    """When this version was deployed"""

    secrets: List[DeployedSecretKey]
    """List of secret keys (no values)"""

    version_id: str
    """Version ID this snapshot came from"""

    state: Optional[str] = None
    """Always 'deployed' for this response"""
