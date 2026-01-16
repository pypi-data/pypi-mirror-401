# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from ..._models import BaseModel

__all__ = ["EnvSecretInfo"]


class EnvSecretInfo(BaseModel):
    """Secret presence in one environment."""

    env_name: str
    """Environment name"""

    is_secret: bool
    """Whether this is a secret in this environment"""

    updated_at: Optional[datetime] = None
    """Last update timestamp"""

    value: Optional[str] = None
    """Value for non-secrets (is_secret=False) only. Always None for secrets."""
