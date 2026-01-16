# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Required, TypedDict

from .acp_type import AcpType
from .agent_input_type import AgentInputType

__all__ = ["AgentRegisterParams"]


class AgentRegisterParams(TypedDict, total=False):
    acp_type: Required[AcpType]
    """The type of ACP to use for the agent."""

    acp_url: Required[str]
    """The URL of the ACP server for the agent."""

    description: Required[str]
    """The description of the agent."""

    name: Required[str]
    """The unique name of the agent."""

    agent_id: Optional[str]
    """Optional agent ID if the agent already exists and needs to be updated."""

    agent_input_type: Optional[AgentInputType]
    """The type of input the agent expects."""

    principal_context: object
    """Principal used for authorization"""

    registration_metadata: Optional[Dict[str, object]]
    """The metadata for the agent's registration."""
