# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from ...._models import BaseModel

__all__ = ["EnvVarResponse"]


class EnvVarResponse(BaseModel):
    """Response model for a single environment variable."""

    id: str
    """Unique identifier"""

    env_id: str
    """Environment ID"""

    is_secret: bool
    """Whether value is write-only"""

    key: str
    """Variable key"""

    created_at: Optional[datetime] = None
    """Creation timestamp"""

    updated_at: Optional[datetime] = None
    """Last update timestamp"""

    value: Optional[str] = None
    """Decrypted value (only for non-secrets when requested)"""
