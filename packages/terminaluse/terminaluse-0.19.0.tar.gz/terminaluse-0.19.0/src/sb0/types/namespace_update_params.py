# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["NamespaceUpdateParams"]


class NamespaceUpdateParams(TypedDict, total=False):
    gcp_sa_email: Optional[str]
    """GCP service account email (set by infra)."""

    gcs_bucket: Optional[str]
    """GCS bucket name (set by infra)."""

    k8s_namespace: Optional[str]
    """K8s namespace name (set by infra)."""

    name: Optional[str]
    """Human-readable name."""
