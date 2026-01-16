# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["SecretDeleteParams"]


class SecretDeleteParams(TypedDict, total=False):
    namespace_slug: Required[str]

    agent_name: Required[str]

    env_name: Required[str]

    redeploy: bool
    """If true, trigger redeploy after deletion"""
