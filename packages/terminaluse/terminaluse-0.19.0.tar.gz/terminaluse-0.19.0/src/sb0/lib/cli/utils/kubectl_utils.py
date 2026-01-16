"""Kubernetes utilities for CLI operations.

NOTE: This module is largely unused in the new deployment flow.
The platform (nucleus) now handles all Kubernetes/Helm operations.
These utilities may still be useful for local development or debugging.
"""

from __future__ import annotations

from kubernetes import client, config

from sb0.lib.utils.logging import make_logger
from sb0.lib.cli.utils.exceptions import DeploymentError

logger = make_logger(__name__)


def get_k8s_client(context: str | None = None) -> client.CoreV1Api:
    """Get a Kubernetes client for the specified context (or current if None).

    Useful for local development and debugging.
    """
    try:
        if context:
            config.load_kube_config(context=context)
        else:
            config.load_kube_config()
        return client.CoreV1Api()
    except Exception as e:
        raise DeploymentError(f"Failed to create Kubernetes client: {e}") from e
