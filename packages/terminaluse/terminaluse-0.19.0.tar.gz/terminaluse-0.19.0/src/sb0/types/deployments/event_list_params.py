# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from ..versions.version_event_type import VersionEventType

__all__ = ["EventListParams"]


class EventListParams(TypedDict, total=False):
    after_sequence_id: Optional[int]
    """Return events after this sequence_id (for ascending pagination)"""

    before_sequence_id: Optional[int]
    """Return events before this sequence_id (for descending pagination)"""

    descending: bool
    """Order by sequence_id descending (newest first). Defaults to True."""

    event_type: Optional[VersionEventType]
    """Types of version lifecycle events."""

    limit: int
    """Maximum events to return"""
