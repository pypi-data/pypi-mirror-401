# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

from .log_entry_param import LogEntryParam

__all__ = ["LogIngestParams"]


class LogIngestParams(TypedDict, total=False):
    logs: Required[Iterable[LogEntryParam]]
