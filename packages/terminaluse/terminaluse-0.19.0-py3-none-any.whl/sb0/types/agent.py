# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime

from .._models import BaseModel
from .agent_status import AgentStatus
from .agent_input_type import AgentInputType

__all__ = ["Agent"]


class Agent(BaseModel):
    id: str
    """The unique identifier of the agent."""

    created_at: datetime
    """The timestamp when the agent was created"""

    description: str
    """The description of the action."""

    name: str
    """The agent name (unique within namespace)."""

    namespace_id: str
    """The namespace slug this agent belongs to."""

    updated_at: datetime
    """The timestamp when the agent was last updated"""

    agent_input_type: Optional[AgentInputType] = None
    """The type of input the agent expects."""

    registered_at: Optional[datetime] = None
    """The timestamp when the agent was last registered"""

    registration_metadata: Optional[Dict[str, object]] = None
    """The metadata for the agent's registration."""

    status: Optional[AgentStatus] = None
    """Agent status. Runtime statuses (Ready/Failed/Unhealthy) now live on Deployment."""

    status_reason: Optional[str] = None
    """The reason for the status of the action."""
