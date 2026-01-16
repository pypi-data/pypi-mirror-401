# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["RollbackCreateParams"]


class RollbackCreateParams(TypedDict, total=False):
    namespace_slug: Required[str]

    agent_name: Required[str]

    target_version_id: Optional[str]
    """Version ID to rollback to (defaults to previous version if not specified)"""
