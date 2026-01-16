# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from ..._models import BaseModel
from .schedule_state import ScheduleState
from .schedule_spec_info import ScheduleSpecInfo
from .schedule_action_info import ScheduleActionInfo

__all__ = ["ScheduleResponse"]


class ScheduleResponse(BaseModel):
    """Response model for schedule operations"""

    action: ScheduleActionInfo
    """Information about the scheduled action"""

    agent_id: str
    """ID of the agent this schedule belongs to"""

    name: str
    """Human-readable name for the schedule"""

    schedule_id: str
    """Unique identifier for the schedule"""

    spec: ScheduleSpecInfo
    """Schedule specification"""

    state: ScheduleState
    """Current state of the schedule"""

    created_at: Optional[datetime] = None
    """When the schedule was created"""

    last_action_time: Optional[datetime] = None
    """When the schedule last executed"""

    next_action_times: Optional[List[datetime]] = None
    """Upcoming scheduled execution times"""

    num_actions_missed: Optional[int] = None
    """Number of scheduled executions that were missed"""

    num_actions_taken: Optional[int] = None
    """Number of times the schedule has executed"""
