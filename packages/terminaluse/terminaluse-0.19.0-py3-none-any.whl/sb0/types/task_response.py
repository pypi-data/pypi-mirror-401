# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime

from .agent import Agent
from .._models import BaseModel
from .task_status import TaskStatus

__all__ = ["TaskResponse"]


class TaskResponse(BaseModel):
    """Task response model with optional related data based on relationships"""

    id: str

    workspace_id: str

    agents: Optional[List[Agent]] = None

    created_at: Optional[datetime] = None

    name: Optional[str] = None

    params: Optional[Dict[str, object]] = None

    status: Optional[TaskStatus] = None

    status_reason: Optional[str] = None

    task_metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[datetime] = None
