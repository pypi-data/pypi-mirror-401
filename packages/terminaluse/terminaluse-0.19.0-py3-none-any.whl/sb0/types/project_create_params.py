# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["ProjectCreateParams"]


class ProjectCreateParams(TypedDict, total=False):
    name: Required[str]
    """Project name (unique within namespace)."""

    namespace_id: Required[str]
    """The namespace this project belongs to."""

    description: Optional[str]
    """Optional project description."""
