# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["Project"]


class Project(BaseModel):
    """Response model for project."""

    id: str
    """The unique identifier of the project."""

    created_by: str
    """member_id of the creator."""

    name: str
    """Project name."""

    namespace_id: str
    """The namespace this project belongs to."""

    created_at: Optional[datetime] = None
    """When the project was created."""

    description: Optional[str] = None
    """Optional project description."""
