# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["ScheduleActionInfo"]


class ScheduleActionInfo(BaseModel):
    """Information about the scheduled action"""

    task_queue: str
    """Task queue for the workflow"""

    workflow_id_prefix: str
    """Prefix for workflow execution IDs"""

    workflow_name: str
    """Name of the workflow being executed"""

    workflow_params: Optional[List[object]] = None
    """Parameters passed to the workflow"""
