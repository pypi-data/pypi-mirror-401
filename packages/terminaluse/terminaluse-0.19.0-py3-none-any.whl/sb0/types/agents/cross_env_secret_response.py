# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel
from .env_secret_info import EnvSecretInfo

__all__ = ["CrossEnvSecretResponse"]


class CrossEnvSecretResponse(BaseModel):
    """A secret key across all environments."""

    environments: List[EnvSecretInfo]
    """List of environments containing this key"""

    is_secret: bool
    """Whether this is a secret"""

    key: str
    """Secret key name"""

    value: Optional[str] = None
    """Value for non-secrets (is_secret=False) only. Always None for secrets."""
