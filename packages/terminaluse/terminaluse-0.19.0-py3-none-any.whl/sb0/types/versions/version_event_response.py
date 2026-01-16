# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from ..._models import BaseModel
from .version_event_type import VersionEventType
from .version_event_content import VersionEventContent

__all__ = ["VersionEventResponse"]


class VersionEventResponse(BaseModel):
    """Response model for a single version event."""

    id: str
    """Event ID"""

    created_at: datetime
    """When this event was created"""

    deployment_id: str
    """Deployment ID (denormalized)"""

    event_type: VersionEventType
    """Type of lifecycle event"""

    sequence_id: int
    """Monotonically increasing sequence ID for ordering"""

    version_id: str
    """Version ID this event belongs to"""

    actor_id: Optional[str] = None
    """User ID who triggered this event"""

    content: Optional[VersionEventContent] = None
    """Typed content for version events stored as JSONB."""
