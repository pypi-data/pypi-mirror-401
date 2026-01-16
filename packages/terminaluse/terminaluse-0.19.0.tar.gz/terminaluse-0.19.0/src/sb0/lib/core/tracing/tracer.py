from __future__ import annotations

from sb0 import Sb0, AsyncSb0
from sb0.lib.core.tracing.trace import Trace, AsyncTrace
from sb0.lib.core.tracing.tracing_processor_manager import (
    get_sync_tracing_processors,
    get_async_tracing_processors,
)


class Tracer:
    """
    Tracer is the main entry point for tracing in Sb0.
    It manages the client connection and creates traces.
    """

    def __init__(self, client: Sb0):
        """
        Initialize a new sync tracer with the provided client.

        Args:
            client: Sb0 client instance used for API communication.
        """
        self.client = client

    def trace(self, trace_id: str | None = None) -> Trace:
        """
        Create a new trace with the given trace ID.

        Args:
            trace_id: The trace ID to use.

        Returns:
            A new Trace instance.
        """
        return Trace(
            processors=get_sync_tracing_processors(),
            client=self.client,
            trace_id=trace_id,
        )


class AsyncTracer:
    """
    AsyncTracer is the async version of Tracer.
    It manages the async client connection and creates async traces.
    """

    def __init__(self, client: AsyncSb0):
        """
        Initialize a new async tracer with the provided client.

        Args:
            client: AsyncSb0 client instance used for API communication.
        """
        self.client = client

    def trace(self, trace_id: str | None = None) -> AsyncTrace:
        """
        Create a new trace with the given trace ID.

        Args:
            trace_id: The trace ID to use.

        Returns:
            A new AsyncTrace instance.
        """
        return AsyncTrace(
            processors=get_async_tracing_processors(),
            client=self.client,
            trace_id=trace_id,
        )
