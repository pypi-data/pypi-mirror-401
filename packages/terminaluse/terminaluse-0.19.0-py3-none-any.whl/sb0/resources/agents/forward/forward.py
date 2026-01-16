# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .name import (
    NameResource,
    AsyncNameResource,
    NameResourceWithRawResponse,
    AsyncNameResourceWithRawResponse,
    NameResourceWithStreamingResponse,
    AsyncNameResourceWithStreamingResponse,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["ForwardResource", "AsyncForwardResource"]


class ForwardResource(SyncAPIResource):
    @cached_property
    def name(self) -> NameResource:
        return NameResource(self._client)

    @cached_property
    def with_raw_response(self) -> ForwardResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return ForwardResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ForwardResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return ForwardResourceWithStreamingResponse(self)


class AsyncForwardResource(AsyncAPIResource):
    @cached_property
    def name(self) -> AsyncNameResource:
        return AsyncNameResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncForwardResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncForwardResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncForwardResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return AsyncForwardResourceWithStreamingResponse(self)


class ForwardResourceWithRawResponse:
    def __init__(self, forward: ForwardResource) -> None:
        self._forward = forward

    @cached_property
    def name(self) -> NameResourceWithRawResponse:
        return NameResourceWithRawResponse(self._forward.name)


class AsyncForwardResourceWithRawResponse:
    def __init__(self, forward: AsyncForwardResource) -> None:
        self._forward = forward

    @cached_property
    def name(self) -> AsyncNameResourceWithRawResponse:
        return AsyncNameResourceWithRawResponse(self._forward.name)


class ForwardResourceWithStreamingResponse:
    def __init__(self, forward: ForwardResource) -> None:
        self._forward = forward

    @cached_property
    def name(self) -> NameResourceWithStreamingResponse:
        return NameResourceWithStreamingResponse(self._forward.name)


class AsyncForwardResourceWithStreamingResponse:
    def __init__(self, forward: AsyncForwardResource) -> None:
        self._forward = forward

    @cached_property
    def name(self) -> AsyncNameResourceWithStreamingResponse:
        return AsyncNameResourceWithStreamingResponse(self._forward.name)
