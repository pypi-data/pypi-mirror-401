# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["ProjectListParams"]


class ProjectListParams(TypedDict, total=False):
    limit: int
    """Maximum number of results"""

    namespace_id: Optional[str]
    """Filter by namespace ID"""

    page_number: int
    """Page number"""
