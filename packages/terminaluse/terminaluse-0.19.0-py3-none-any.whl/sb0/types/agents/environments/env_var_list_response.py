# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ...._models import BaseModel
from .env_var_response import EnvVarResponse

__all__ = ["EnvVarListResponse"]


class EnvVarListResponse(BaseModel):
    """Response for listing environment variables."""

    env_vars: List[EnvVarResponse]
    """List of environment variables"""

    state: Optional[str] = None
    """Indicates this is pending state (vs deployed).

    Pending = what will be used on next deploy. Deployed = what's currently running
    (from Version.secrets_snapshot).
    """
