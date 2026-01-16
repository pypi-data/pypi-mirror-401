# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel
from .cross_env_secret_response import CrossEnvSecretResponse

__all__ = ["CrossEnvSecretsListResponse"]


class CrossEnvSecretsListResponse(BaseModel):
    """Cross-environment secrets view."""

    all_environments: List[str]
    """All environment names for the agent"""

    variables: List[CrossEnvSecretResponse]
    """All secret keys across environments"""
