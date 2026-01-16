# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .versions import (
    VersionsResource,
    AsyncVersionsResource,
    VersionsResourceWithRawResponse,
    AsyncVersionsResourceWithRawResponse,
    VersionsResourceWithStreamingResponse,
    AsyncVersionsResourceWithStreamingResponse,
)
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
from ....types.agents import deployment_list_params
from ....types.deployment_response import DeploymentResponse
from ....types.deployment_list_response import DeploymentListResponse

__all__ = ["DeploymentsResource", "AsyncDeploymentsResource"]


class DeploymentsResource(SyncAPIResource):
    @cached_property
    def versions(self) -> VersionsResource:
        return VersionsResource(self._client)

    @cached_property
    def with_raw_response(self) -> DeploymentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return DeploymentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DeploymentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return DeploymentsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        branch: str,
        *,
        namespace_slug: str,
        agent_name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeploymentResponse:
        """
        Get a specific deployment by agent name and branch.

            The branch name will be normalized (lowercased, slashes converted to hyphens).
            For example, "feature/new-tool" becomes "feature-new-tool".

        Args:
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
            f"/agents/{namespace_slug}/{agent_name}/deployments/{branch}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeploymentResponse,
        )

    def list(
        self,
        agent_name: str,
        *,
        namespace_slug: str,
        include_retired: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeploymentListResponse:
        """
        List all deployments for an agent.

            Each deployment represents a branch (e.g., main, staging, feature-x).
            By default, retired deployments are excluded.

        Args:
          include_retired: Include retired deployments in results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not namespace_slug:
            raise ValueError(f"Expected a non-empty value for `namespace_slug` but received {namespace_slug!r}")
        if not agent_name:
            raise ValueError(f"Expected a non-empty value for `agent_name` but received {agent_name!r}")
        return self._get(
            f"/agents/{namespace_slug}/{agent_name}/deployments",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"include_retired": include_retired}, deployment_list_params.DeploymentListParams
                ),
            ),
            cast_to=DeploymentListResponse,
        )


class AsyncDeploymentsResource(AsyncAPIResource):
    @cached_property
    def versions(self) -> AsyncVersionsResource:
        return AsyncVersionsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDeploymentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncDeploymentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDeploymentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return AsyncDeploymentsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        branch: str,
        *,
        namespace_slug: str,
        agent_name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeploymentResponse:
        """
        Get a specific deployment by agent name and branch.

            The branch name will be normalized (lowercased, slashes converted to hyphens).
            For example, "feature/new-tool" becomes "feature-new-tool".

        Args:
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
            f"/agents/{namespace_slug}/{agent_name}/deployments/{branch}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeploymentResponse,
        )

    async def list(
        self,
        agent_name: str,
        *,
        namespace_slug: str,
        include_retired: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeploymentListResponse:
        """
        List all deployments for an agent.

            Each deployment represents a branch (e.g., main, staging, feature-x).
            By default, retired deployments are excluded.

        Args:
          include_retired: Include retired deployments in results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not namespace_slug:
            raise ValueError(f"Expected a non-empty value for `namespace_slug` but received {namespace_slug!r}")
        if not agent_name:
            raise ValueError(f"Expected a non-empty value for `agent_name` but received {agent_name!r}")
        return await self._get(
            f"/agents/{namespace_slug}/{agent_name}/deployments",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"include_retired": include_retired}, deployment_list_params.DeploymentListParams
                ),
            ),
            cast_to=DeploymentListResponse,
        )


class DeploymentsResourceWithRawResponse:
    def __init__(self, deployments: DeploymentsResource) -> None:
        self._deployments = deployments

        self.retrieve = to_raw_response_wrapper(
            deployments.retrieve,
        )
        self.list = to_raw_response_wrapper(
            deployments.list,
        )

    @cached_property
    def versions(self) -> VersionsResourceWithRawResponse:
        return VersionsResourceWithRawResponse(self._deployments.versions)


class AsyncDeploymentsResourceWithRawResponse:
    def __init__(self, deployments: AsyncDeploymentsResource) -> None:
        self._deployments = deployments

        self.retrieve = async_to_raw_response_wrapper(
            deployments.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            deployments.list,
        )

    @cached_property
    def versions(self) -> AsyncVersionsResourceWithRawResponse:
        return AsyncVersionsResourceWithRawResponse(self._deployments.versions)


class DeploymentsResourceWithStreamingResponse:
    def __init__(self, deployments: DeploymentsResource) -> None:
        self._deployments = deployments

        self.retrieve = to_streamed_response_wrapper(
            deployments.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            deployments.list,
        )

    @cached_property
    def versions(self) -> VersionsResourceWithStreamingResponse:
        return VersionsResourceWithStreamingResponse(self._deployments.versions)


class AsyncDeploymentsResourceWithStreamingResponse:
    def __init__(self, deployments: AsyncDeploymentsResource) -> None:
        self._deployments = deployments

        self.retrieve = async_to_streamed_response_wrapper(
            deployments.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            deployments.list,
        )

    @cached_property
    def versions(self) -> AsyncVersionsResourceWithStreamingResponse:
        return AsyncVersionsResourceWithStreamingResponse(self._deployments.versions)
