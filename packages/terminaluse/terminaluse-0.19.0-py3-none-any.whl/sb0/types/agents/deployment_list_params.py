# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["DeploymentListParams"]


class DeploymentListParams(TypedDict, total=False):
    namespace_slug: Required[str]

    include_retired: bool
    """Include retired deployments in results"""
