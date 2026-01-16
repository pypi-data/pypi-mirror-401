# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from .workspace_directory import WorkspaceDirectory

__all__ = ["WorkspaceGetUploadURLParams"]


class WorkspaceGetUploadURLParams(TypedDict, total=False):
    expiration_seconds: int
    """URL expiration time in seconds (default 1 hour, max 7 days)."""

    workspace_directory: WorkspaceDirectory
    """Which storage target to access: workspace or dot_claude archive."""
