# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from .log_source import LogSource

__all__ = ["LogEntryParam"]


class LogEntryParam(TypedDict, total=False):
    """A single log entry from an agent."""

    message: Required[str]

    source: Required[LogSource]
    """Source of the log entry."""

    timestamp: Required[str]

    method: Optional[str]

    task_id: Optional[str]
