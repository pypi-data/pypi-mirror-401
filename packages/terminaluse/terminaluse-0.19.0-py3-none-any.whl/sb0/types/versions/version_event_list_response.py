# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel
from .version_event_response import VersionEventResponse

__all__ = ["VersionEventListResponse"]


class VersionEventListResponse(BaseModel):
    """Response model for listing version events."""

    events: List[VersionEventResponse]
    """List of version events"""

    has_more: bool
    """Whether there are more events after the last one"""

    total: int
    """Total number of events returned"""
