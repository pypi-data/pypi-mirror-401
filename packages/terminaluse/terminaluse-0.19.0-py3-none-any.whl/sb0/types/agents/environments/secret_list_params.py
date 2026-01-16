# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["SecretListParams"]


class SecretListParams(TypedDict, total=False):
    namespace_slug: Required[str]

    agent_name: Required[str]

    include_values: bool
    """Include values for non-secrets (is_secret=False only)"""
