# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["LogAuthParams"]


class LogAuthParams(TypedDict, total=False):
    agent_name: Required[str]
    """Name of the agent to get logs for"""
