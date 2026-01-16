# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal, TypeAlias

__all__ = ["AgentRpcMethod"]

AgentRpcMethod: TypeAlias = Literal["event/send", "task/create", "message/send", "task/cancel"]
