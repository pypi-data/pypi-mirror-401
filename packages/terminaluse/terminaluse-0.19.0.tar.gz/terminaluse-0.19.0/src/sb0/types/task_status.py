# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal, TypeAlias

__all__ = ["TaskStatus"]

TaskStatus: TypeAlias = Literal["CANCELED", "COMPLETED", "FAILED", "RUNNING", "TERMINATED", "TIMED_OUT", "DELETED"]
