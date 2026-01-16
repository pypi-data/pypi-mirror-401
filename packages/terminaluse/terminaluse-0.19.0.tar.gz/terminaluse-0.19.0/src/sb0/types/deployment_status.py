# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal, TypeAlias

__all__ = ["DeploymentStatus"]

DeploymentStatus: TypeAlias = Literal["DEPLOYING", "READY", "FAILED", "TIMEOUT", "UNHEALTHY", "RETIRED"]
