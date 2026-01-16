# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime

from .._models import BaseModel
from .acp_type import AcpType
from .agent_status import AgentStatus
from .agent_input_type import AgentInputType

__all__ = ["RegisterAgentResponse"]


class RegisterAgentResponse(BaseModel):
    """Response model for registering an agent."""

    id: str
    """The unique identifier of the agent."""

    acp_type: AcpType
    """The type of the ACP Server (Either sync or async)"""

    created_at: datetime
    """The timestamp when the agent was created"""

    description: str
    """The description of the action."""

    name: str
    """The unique name of the agent."""

    updated_at: datetime
    """The timestamp when the agent was last updated"""

    agent_api_key: Optional[str] = None
    """The API key for the agent, if applicable."""

    agent_input_type: Optional[AgentInputType] = None
    """The type of input the agent expects."""

    registered_at: Optional[datetime] = None
    """The timestamp when the agent was last registered"""

    registration_metadata: Optional[Dict[str, object]] = None
    """The metadata for the agent's registration."""

    status: Optional[AgentStatus] = None
    """The status of the action, indicating if it's building, ready, failed, etc."""

    status_reason: Optional[str] = None
    """The reason for the status of the action."""
