# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Required, TypedDict

from .deployment_acp_type import DeploymentAcpType

__all__ = ["AgentDeployParams"]


class AgentDeployParams(TypedDict, total=False):
    agent_name: Required[str]
    """
    Agent name in 'namespace_slug/agent_name' format (lowercase, alphanumeric,
    hyphens only)
    """

    author_email: Required[str]
    """Git commit author email"""

    author_name: Required[str]
    """Git commit author name"""

    branch: Required[str]
    """Git branch name (e.g., 'main', 'feature/new-tool')"""

    git_hash: Required[str]
    """Git commit hash (short or full)"""

    image_url: Required[str]
    """Full container image URL (e.g., 'us-east4-docker.pkg.dev/proj/repo/agent:hash')"""

    acp_type: DeploymentAcpType
    """ACP server type (SYNC or ASYNC)"""

    are_tasks_sticky: Optional[bool]
    """
    If true, running tasks stay on their original version until completion during
    this deploy. If false or None, tasks are migrated to the new version
    immediately.
    """

    description: Optional[str]
    """Agent description (used when creating new agent)"""

    git_message: Optional[str]
    """Git commit message (truncated if too long)"""

    is_dirty: bool
    """Whether the working directory had uncommitted changes at deploy time"""

    replicas: int
    """Desired replica count (1-10)"""

    resources: Optional[Dict[str, object]]
    """
    Resource requests and limits (e.g., {'requests': {'cpu': '100m', 'memory':
    '256Mi'}, 'limits': {'cpu': '1000m', 'memory': '1Gi'}})
    """
