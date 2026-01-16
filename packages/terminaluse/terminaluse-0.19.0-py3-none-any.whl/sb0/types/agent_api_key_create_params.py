# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from .agent_api_key_type import AgentAPIKeyType

__all__ = ["AgentAPIKeyCreateParams"]


class AgentAPIKeyCreateParams(TypedDict, total=False):
    name: Required[str]
    """The name of the agent's API key."""

    agent_id: Optional[str]
    """The UUID of the agent"""

    agent_name: Optional[str]
    """The name of the agent - if not provided, the agent_id must be set."""

    api_key: Optional[str]
    """Optionally provide the API key value - if not set, one will be generated."""

    api_key_type: AgentAPIKeyType
    """The type of the agent API key (external by default)."""
