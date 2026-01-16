# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal, TypeAlias

__all__ = ["VersionEventType"]

VersionEventType: TypeAlias = Literal[
    "VERSION_CREATED",
    "VERSION_ACTIVATED",
    "VERSION_FAILED",
    "VERSION_DRAINING",
    "VERSION_RETIRED",
    "VERSION_ROLLED_BACK_FROM",
    "VERSION_ROLLED_BACK_TO",
    "VERSION_REDEPLOYED",
    "TASKS_MIGRATED",
]
