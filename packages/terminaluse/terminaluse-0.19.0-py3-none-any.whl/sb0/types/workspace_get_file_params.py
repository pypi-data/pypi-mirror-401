# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["WorkspaceGetFileParams"]


class WorkspaceGetFileParams(TypedDict, total=False):
    workspace_id: Required[str]

    include_content: bool
    """Include file content in response"""
