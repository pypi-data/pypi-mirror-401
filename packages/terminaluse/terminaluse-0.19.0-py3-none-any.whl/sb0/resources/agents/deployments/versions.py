# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.agents.deployments import version_list_params
from ....types.version_list_response import VersionListResponse

__all__ = ["VersionsResource", "AsyncVersionsResource"]


class VersionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> VersionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return VersionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VersionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return VersionsResourceWithStreamingResponse(self)

    def list(
        self,
        branch: str,
        *,
        namespace_slug: str,
        agent_name: str,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VersionListResponse:
        """
        List all versions for a specific branch deployment.

            Versions are ordered by deployed_at descending (most recent first).

        Args:
          limit: Maximum versions to return

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not namespace_slug:
            raise ValueError(f"Expected a non-empty value for `namespace_slug` but received {namespace_slug!r}")
        if not agent_name:
            raise ValueError(f"Expected a non-empty value for `agent_name` but received {agent_name!r}")
        if not branch:
            raise ValueError(f"Expected a non-empty value for `branch` but received {branch!r}")
        return self._get(
            f"/agents/{namespace_slug}/{agent_name}/deployments/{branch}/versions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"limit": limit}, version_list_params.VersionListParams),
            ),
            cast_to=VersionListResponse,
        )


class AsyncVersionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncVersionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncVersionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVersionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return AsyncVersionsResourceWithStreamingResponse(self)

    async def list(
        self,
        branch: str,
        *,
        namespace_slug: str,
        agent_name: str,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VersionListResponse:
        """
        List all versions for a specific branch deployment.

            Versions are ordered by deployed_at descending (most recent first).

        Args:
          limit: Maximum versions to return

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not namespace_slug:
            raise ValueError(f"Expected a non-empty value for `namespace_slug` but received {namespace_slug!r}")
        if not agent_name:
            raise ValueError(f"Expected a non-empty value for `agent_name` but received {agent_name!r}")
        if not branch:
            raise ValueError(f"Expected a non-empty value for `branch` but received {branch!r}")
        return await self._get(
            f"/agents/{namespace_slug}/{agent_name}/deployments/{branch}/versions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"limit": limit}, version_list_params.VersionListParams),
            ),
            cast_to=VersionListResponse,
        )


class VersionsResourceWithRawResponse:
    def __init__(self, versions: VersionsResource) -> None:
        self._versions = versions

        self.list = to_raw_response_wrapper(
            versions.list,
        )


class AsyncVersionsResourceWithRawResponse:
    def __init__(self, versions: AsyncVersionsResource) -> None:
        self._versions = versions

        self.list = async_to_raw_response_wrapper(
            versions.list,
        )


class VersionsResourceWithStreamingResponse:
    def __init__(self, versions: VersionsResource) -> None:
        self._versions = versions

        self.list = to_streamed_response_wrapper(
            versions.list,
        )


class AsyncVersionsResourceWithStreamingResponse:
    def __init__(self, versions: AsyncVersionsResource) -> None:
        self._versions = versions

        self.list = async_to_streamed_response_wrapper(
            versions.list,
        )
