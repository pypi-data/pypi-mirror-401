# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.versions import VersionEventType
from ...types.deployments import event_list_params
from ...types.versions.version_event_type import VersionEventType
from ...types.versions.version_event_list_response import VersionEventListResponse

__all__ = ["EventsResource", "AsyncEventsResource"]


class EventsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EventsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return EventsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EventsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return EventsResourceWithStreamingResponse(self)

    def list(
        self,
        deployment_id: str,
        *,
        after_sequence_id: Optional[int] | Omit = omit,
        before_sequence_id: Optional[int] | Omit = omit,
        descending: bool | Omit = omit,
        event_type: Optional[VersionEventType] | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VersionEventListResponse:
        """
        List lifecycle events across all versions for a deployment.

        Args:
          after_sequence_id: Return events after this sequence_id (for ascending pagination)

          before_sequence_id: Return events before this sequence_id (for descending pagination)

          descending: Order by sequence_id descending (newest first). Defaults to True.

          event_type: Types of version lifecycle events.

          limit: Maximum events to return

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
        return self._get(
            f"/deployments/{deployment_id}/events",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after_sequence_id": after_sequence_id,
                        "before_sequence_id": before_sequence_id,
                        "descending": descending,
                        "event_type": event_type,
                        "limit": limit,
                    },
                    event_list_params.EventListParams,
                ),
            ),
            cast_to=VersionEventListResponse,
        )


class AsyncEventsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEventsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncEventsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEventsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return AsyncEventsResourceWithStreamingResponse(self)

    async def list(
        self,
        deployment_id: str,
        *,
        after_sequence_id: Optional[int] | Omit = omit,
        before_sequence_id: Optional[int] | Omit = omit,
        descending: bool | Omit = omit,
        event_type: Optional[VersionEventType] | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VersionEventListResponse:
        """
        List lifecycle events across all versions for a deployment.

        Args:
          after_sequence_id: Return events after this sequence_id (for ascending pagination)

          before_sequence_id: Return events before this sequence_id (for descending pagination)

          descending: Order by sequence_id descending (newest first). Defaults to True.

          event_type: Types of version lifecycle events.

          limit: Maximum events to return

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
        return await self._get(
            f"/deployments/{deployment_id}/events",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "after_sequence_id": after_sequence_id,
                        "before_sequence_id": before_sequence_id,
                        "descending": descending,
                        "event_type": event_type,
                        "limit": limit,
                    },
                    event_list_params.EventListParams,
                ),
            ),
            cast_to=VersionEventListResponse,
        )


class EventsResourceWithRawResponse:
    def __init__(self, events: EventsResource) -> None:
        self._events = events

        self.list = to_raw_response_wrapper(
            events.list,
        )


class AsyncEventsResourceWithRawResponse:
    def __init__(self, events: AsyncEventsResource) -> None:
        self._events = events

        self.list = async_to_raw_response_wrapper(
            events.list,
        )


class EventsResourceWithStreamingResponse:
    def __init__(self, events: EventsResource) -> None:
        self._events = events

        self.list = to_streamed_response_wrapper(
            events.list,
        )


class AsyncEventsResourceWithStreamingResponse:
    def __init__(self, events: AsyncEventsResource) -> None:
        self._events = events

        self.list = async_to_streamed_response_wrapper(
            events.list,
        )
