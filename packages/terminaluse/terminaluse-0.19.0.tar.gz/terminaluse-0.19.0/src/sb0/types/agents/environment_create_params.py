# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from ..._types import SequenceNotStr

__all__ = ["EnvironmentCreateParams"]


class EnvironmentCreateParams(TypedDict, total=False):
    namespace_slug: Required[str]

    branch_rules: Required[SequenceNotStr[str]]
    """Branch patterns for matching (e.g., ['feature/*'], ['develop'])"""

    name: Required[str]
    """Environment name (lowercase alphanumeric and hyphens only)"""
