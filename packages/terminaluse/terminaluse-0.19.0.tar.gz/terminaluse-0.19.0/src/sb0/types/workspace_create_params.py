# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["WorkspaceCreateParams"]


class WorkspaceCreateParams(TypedDict, total=False):
    namespace_id: Required[str]
    """Namespace ID for tenant isolation"""

    project_id: Required[str]
    """Project ID this workspace belongs to (required for authorization)."""

    name: Optional[str]
    """Optional human-readable name for the workspace (unique per namespace)."""
