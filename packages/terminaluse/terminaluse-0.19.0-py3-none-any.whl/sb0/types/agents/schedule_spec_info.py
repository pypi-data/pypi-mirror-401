# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from ..._models import BaseModel

__all__ = ["ScheduleSpecInfo"]


class ScheduleSpecInfo(BaseModel):
    """Information about the schedule specification"""

    cron_expressions: Optional[List[str]] = None
    """Cron expressions for the schedule"""

    end_at: Optional[datetime] = None
    """When the schedule stops being active"""

    intervals_seconds: Optional[List[int]] = None
    """Interval specifications in seconds"""

    start_at: Optional[datetime] = None
    """When the schedule starts being active"""
