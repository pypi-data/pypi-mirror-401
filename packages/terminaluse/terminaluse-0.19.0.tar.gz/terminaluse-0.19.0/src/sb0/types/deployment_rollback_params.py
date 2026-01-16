# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["DeploymentRollbackParams"]


class DeploymentRollbackParams(TypedDict, total=False):
    target_version_id: Optional[str]
    """Version ID to rollback to (defaults to previous version if not specified)"""
