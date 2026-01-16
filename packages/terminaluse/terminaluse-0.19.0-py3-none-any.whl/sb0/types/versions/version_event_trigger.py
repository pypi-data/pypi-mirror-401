# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal, TypeAlias

__all__ = ["VersionEventTrigger"]

VersionEventTrigger: TypeAlias = Literal[
    "deploy", "container_register", "rollback", "hot_swap", "helm_failure", "redeploy"
]
