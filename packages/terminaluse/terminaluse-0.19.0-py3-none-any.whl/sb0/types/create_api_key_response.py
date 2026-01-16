# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel
from .agent_api_key_type import AgentAPIKeyType

__all__ = ["CreateAPIKeyResponse"]


class CreateAPIKeyResponse(BaseModel):
    id: str
    """The unique identifier of the agent API key."""

    agent_id: str
    """The UUID of the agent"""

    api_key: str
    """The value of the newly created API key."""

    api_key_type: AgentAPIKeyType
    """The type of the created agent API key (external)."""

    created_at: datetime
    """When the agent API key was created"""

    name: Optional[str] = None
    """The optional name of the agent API key."""
