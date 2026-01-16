# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal, TypeAlias

__all__ = ["WorkspaceStatus"]

WorkspaceStatus: TypeAlias = Literal["CREATING", "READY", "SYNCING_UP", "SYNCING_DOWN", "FAILED"]
