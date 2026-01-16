# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from .._models import BaseModel

__all__ = ["JsonRpcErrorObject"]


class JsonRpcErrorObject(BaseModel):
    """JSON-RPC 2.0 Error Object

    See: https://www.jsonrpc.org/specification#error_object
    """

    code: int
    """A number that indicates the error type"""

    message: str
    """A short description of the error"""

    data: Optional[Dict[str, object]] = None
    """Additional information about the error (usually an object with details)"""
