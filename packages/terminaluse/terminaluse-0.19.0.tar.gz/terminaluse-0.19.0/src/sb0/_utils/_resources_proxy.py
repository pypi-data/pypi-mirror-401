from __future__ import annotations

from typing import Any
from typing_extensions import override

from ._proxy import LazyProxy


class ResourcesProxy(LazyProxy[Any]):
    """A proxy for the `sb0.resources` module.

    This is used so that we can lazily import `sb0.resources` only when
    needed *and* so that users can just import `sb0` and reference `sb0.resources`
    """

    @override
    def __load__(self) -> Any:
        import importlib

        mod = importlib.import_module("sb0.resources")
        return mod


resources = ResourcesProxy().__as_proxied__()
