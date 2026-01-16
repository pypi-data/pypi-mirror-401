# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["NamespaceCreateParams"]


class NamespaceCreateParams(TypedDict, total=False):
    name: Required[str]
    """Human-readable name."""

    owner_org_id: Required[str]
    """Stytch organization ID that owns this namespace."""

    slug: Required[str]
    """URL-friendly unique identifier (lowercase alphanumeric and hyphens)."""
