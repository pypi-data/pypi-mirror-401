# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from ..agent_api_key_type import AgentAPIKeyType

__all__ = ["NameRetrieveParams"]


class NameRetrieveParams(TypedDict, total=False):
    agent_id: Optional[str]

    agent_name: Optional[str]

    api_key_type: AgentAPIKeyType
