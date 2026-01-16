# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from ..._models import BaseModel

__all__ = ["EnvResponse"]


class EnvResponse(BaseModel):
    """Full environment details."""

    id: str
    """Unique identifier"""

    agent_id: str
    """Parent agent ID"""

    branch_rules: List[str]
    """Branch patterns for matching (e.g., ['main'], ['feature/*'])"""

    is_prod: bool
    """Whether this is the production environment (protected)"""

    name: str
    """Environment name (e.g., 'production', 'staging')"""

    created_at: Optional[datetime] = None
    """Creation timestamp"""

    updated_at: Optional[datetime] = None
    """Last update timestamp"""
