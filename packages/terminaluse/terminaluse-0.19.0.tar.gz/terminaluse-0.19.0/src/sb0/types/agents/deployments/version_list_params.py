# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["VersionListParams"]


class VersionListParams(TypedDict, total=False):
    namespace_slug: Required[str]

    agent_name: Required[str]

    limit: int
    """Maximum versions to return"""
