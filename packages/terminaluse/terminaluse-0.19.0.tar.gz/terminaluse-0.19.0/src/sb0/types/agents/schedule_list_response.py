# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel
from .schedule_list_item import ScheduleListItem

__all__ = ["ScheduleListResponse"]


class ScheduleListResponse(BaseModel):
    """Response model for listing schedules"""

    schedules: List[ScheduleListItem]
    """List of schedules"""

    total: int
    """Total number of schedules"""
