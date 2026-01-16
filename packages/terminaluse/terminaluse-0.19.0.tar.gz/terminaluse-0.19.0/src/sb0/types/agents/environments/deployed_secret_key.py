# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ...._models import BaseModel

__all__ = ["DeployedSecretKey"]


class DeployedSecretKey(BaseModel):
    """A key from deployed secrets snapshot."""

    key: str
    """Secret key name"""

    is_secret: Optional[bool] = None
    """Whether this is a secret. Derived from snapshot metadata."""
