# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from ..._models import BaseModel
from .schedule_state import ScheduleState

__all__ = ["ScheduleListItem"]


class ScheduleListItem(BaseModel):
    """Abbreviated schedule info for list responses"""

    agent_id: str
    """ID of the agent this schedule belongs to"""

    name: str
    """Human-readable name for the schedule"""

    schedule_id: str
    """Unique identifier for the schedule"""

    state: ScheduleState
    """Current state of the schedule"""

    next_action_time: Optional[datetime] = None
    """Next scheduled execution time"""

    workflow_name: Optional[str] = None
    """Name of the scheduled workflow"""
