# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["NamespaceListParams"]


class NamespaceListParams(TypedDict, total=False):
    limit: int
    """Maximum number of results"""

    page_number: int
    """Page number"""
