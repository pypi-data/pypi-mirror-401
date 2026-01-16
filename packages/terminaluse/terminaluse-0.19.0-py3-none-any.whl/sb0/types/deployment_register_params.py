# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["DeploymentRegisterParams"]


class DeploymentRegisterParams(TypedDict, total=False):
    acp_url: Required[str]
    """ACP server URL (e.g., 'http://agent-main-abc123.agents.svc.cluster.local:8000')"""

    deployment_id: Required[str]
    """Deployment ID"""

    version_id: Required[str]
    """Version ID being registered"""
