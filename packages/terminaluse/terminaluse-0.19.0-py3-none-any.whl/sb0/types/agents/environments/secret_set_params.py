# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Required, TypedDict

__all__ = ["SecretSetParams", "Secrets"]


class SecretSetParams(TypedDict, total=False):
    namespace_slug: Required[str]

    agent_name: Required[str]

    secrets: Required[Dict[str, Secrets]]
    """Dict of {key: {value, is_secret}} to set"""

    redeploy: bool
    """If true and env has active deployment, trigger redeploy with new secrets"""


class Secrets(TypedDict, total=False):
    """Value with is_secret flag for setting environment variables."""

    value: Required[str]
    """The plaintext value to encrypt and store"""

    is_secret: bool
    """If true, value is write-only via API (cannot retrieve).

    If false, value can be read back via API.
    """
