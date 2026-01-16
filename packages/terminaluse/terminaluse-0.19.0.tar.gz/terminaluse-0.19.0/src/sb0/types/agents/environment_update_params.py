# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from ..._types import SequenceNotStr

__all__ = ["EnvironmentUpdateParams"]


class EnvironmentUpdateParams(TypedDict, total=False):
    namespace_slug: Required[str]

    agent_name: Required[str]

    branch_rules: Optional[SequenceNotStr[str]]
    """Branch patterns for matching"""
