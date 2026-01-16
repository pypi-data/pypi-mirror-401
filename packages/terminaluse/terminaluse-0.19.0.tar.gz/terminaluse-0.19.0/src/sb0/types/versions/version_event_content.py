# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel
from ..version_status import VersionStatus
from .version_event_trigger import VersionEventTrigger

__all__ = ["VersionEventContent"]


class VersionEventContent(BaseModel):
    """Typed content for version events stored as JSONB."""

    actor_email: Optional[str] = None
    """Email of the user who triggered this event"""

    error_message: Optional[str] = None
    """Error message for failure events"""

    from_version_id: Optional[str] = None
    """Version ID tasks were migrated FROM (for TASKS_MIGRATED events)"""

    git_hash: Optional[str] = None
    """Git hash for context"""

    migrated_task_count: Optional[int] = None
    """Number of tasks migrated (for TASKS_MIGRATED events)"""

    new_status: Optional[VersionStatus] = None
    """Status of a version in its lifecycle."""

    previous_status: Optional[VersionStatus] = None
    """Status of a version in its lifecycle."""

    target_version_id: Optional[str] = None
    """Target version ID for rollback events"""

    triggered_by: Optional[VersionEventTrigger] = None
    """What triggered a version event."""
