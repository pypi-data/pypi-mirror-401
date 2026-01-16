# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["Namespace"]


class Namespace(BaseModel):
    """Response model for namespace."""

    id: str
    """The unique identifier of the namespace."""

    created_by: str
    """member_id of the creator."""

    name: str
    """Human-readable name for the namespace."""

    owner_org_id: str
    """Stytch organization ID that owns this namespace."""

    slug: str
    """URL-friendly unique identifier."""

    created_at: Optional[datetime] = None
    """When the namespace was created."""

    gcp_sa_email: Optional[str] = None
    """GCP service account email."""

    gcs_bucket: Optional[str] = None
    """GCS bucket name."""

    k8s_namespace: Optional[str] = None
    """K8s namespace name."""
