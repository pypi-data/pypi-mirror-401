# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from .events import (
    EventsResource,
    AsyncEventsResource,
    EventsResourceWithRawResponse,
    AsyncEventsResourceWithRawResponse,
    EventsResourceWithStreamingResponse,
    AsyncEventsResourceWithStreamingResponse,
)
from ...types import deployment_register_params, deployment_rollback_params
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from .versions import (
    VersionsResource,
    AsyncVersionsResource,
    VersionsResourceWithRawResponse,
    AsyncVersionsResourceWithRawResponse,
    VersionsResourceWithStreamingResponse,
    AsyncVersionsResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.redeploy_response import RedeployResponse
from ...types.deployment_response import DeploymentResponse
from ...types.register_container_response import RegisterContainerResponse
from ...types.agents.environments.rollback_response import RollbackResponse

__all__ = ["DeploymentsResource", "AsyncDeploymentsResource"]


class DeploymentsResource(SyncAPIResource):
    @cached_property
    def versions(self) -> VersionsResource:
        return VersionsResource(self._client)

    @cached_property
    def events(self) -> EventsResource:
        return EventsResource(self._client)

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
        deployment_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeploymentResponse:
        """
        Get deployment details by ID.

            Used by CLI to poll for deployment status after calling POST /agents/deploy.
            Poll until status is READY (success) or FAILED/TIMEOUT (failure).

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
        return self._get(
            f"/deployments/{deployment_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeploymentResponse,
        )

    def redeploy(
        self,
        deployment_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RedeployResponse:
        """
        Redeploy a deployment with the current secrets from the EnvVar table.

            Creates a new Version with:
            - Same image as current version
            - Fresh secrets_snapshot from current EnvVars

            Use this after updating secrets to apply them to a running deployment.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
        return self._post(
            f"/deployments/{deployment_id}/redeploy",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RedeployResponse,
        )

    def register(
        self,
        *,
        acp_url: str,
        deployment_id: str,
        version_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RegisterContainerResponse:
        """
        Register an agent container that has started up.

            Called by the agent container on startup to:
            1. Register its ACP URL with the platform
            2. Receive its API key for authenticating subsequent requests

            This endpoint should be called from within the container's entrypoint
            after the ACP server is ready to receive traffic.

        Args:
          acp_url: ACP server URL (e.g., 'http://agent-main-abc123.agents.svc.cluster.local:8000')

          deployment_id: Deployment ID

          version_id: Version ID being registered

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/deployments/register",
            body=maybe_transform(
                {
                    "acp_url": acp_url,
                    "deployment_id": deployment_id,
                    "version_id": version_id,
                },
                deployment_register_params.DeploymentRegisterParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RegisterContainerResponse,
        )

    def rollback(
        self,
        deployment_id: str,
        *,
        target_version_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RollbackResponse:
        """
        Roll back a deployment to a previous version by deployment ID.

            Key behavior:
            - EnvVar table is NOT modified (remains pending state)
            - Uses Version.secrets_snapshot as deployed state

        Args:
          target_version_id: Version ID to rollback to (defaults to previous version if not specified)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
        return self._post(
            f"/deployments/{deployment_id}/rollback",
            body=maybe_transform(
                {"target_version_id": target_version_id}, deployment_rollback_params.DeploymentRollbackParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RollbackResponse,
        )


class AsyncDeploymentsResource(AsyncAPIResource):
    @cached_property
    def versions(self) -> AsyncVersionsResource:
        return AsyncVersionsResource(self._client)

    @cached_property
    def events(self) -> AsyncEventsResource:
        return AsyncEventsResource(self._client)

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
        deployment_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeploymentResponse:
        """
        Get deployment details by ID.

            Used by CLI to poll for deployment status after calling POST /agents/deploy.
            Poll until status is READY (success) or FAILED/TIMEOUT (failure).

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
        return await self._get(
            f"/deployments/{deployment_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeploymentResponse,
        )

    async def redeploy(
        self,
        deployment_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RedeployResponse:
        """
        Redeploy a deployment with the current secrets from the EnvVar table.

            Creates a new Version with:
            - Same image as current version
            - Fresh secrets_snapshot from current EnvVars

            Use this after updating secrets to apply them to a running deployment.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
        return await self._post(
            f"/deployments/{deployment_id}/redeploy",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RedeployResponse,
        )

    async def register(
        self,
        *,
        acp_url: str,
        deployment_id: str,
        version_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RegisterContainerResponse:
        """
        Register an agent container that has started up.

            Called by the agent container on startup to:
            1. Register its ACP URL with the platform
            2. Receive its API key for authenticating subsequent requests

            This endpoint should be called from within the container's entrypoint
            after the ACP server is ready to receive traffic.

        Args:
          acp_url: ACP server URL (e.g., 'http://agent-main-abc123.agents.svc.cluster.local:8000')

          deployment_id: Deployment ID

          version_id: Version ID being registered

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/deployments/register",
            body=await async_maybe_transform(
                {
                    "acp_url": acp_url,
                    "deployment_id": deployment_id,
                    "version_id": version_id,
                },
                deployment_register_params.DeploymentRegisterParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RegisterContainerResponse,
        )

    async def rollback(
        self,
        deployment_id: str,
        *,
        target_version_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RollbackResponse:
        """
        Roll back a deployment to a previous version by deployment ID.

            Key behavior:
            - EnvVar table is NOT modified (remains pending state)
            - Uses Version.secrets_snapshot as deployed state

        Args:
          target_version_id: Version ID to rollback to (defaults to previous version if not specified)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
        return await self._post(
            f"/deployments/{deployment_id}/rollback",
            body=await async_maybe_transform(
                {"target_version_id": target_version_id}, deployment_rollback_params.DeploymentRollbackParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RollbackResponse,
        )


class DeploymentsResourceWithRawResponse:
    def __init__(self, deployments: DeploymentsResource) -> None:
        self._deployments = deployments

        self.retrieve = to_raw_response_wrapper(
            deployments.retrieve,
        )
        self.redeploy = to_raw_response_wrapper(
            deployments.redeploy,
        )
        self.register = to_raw_response_wrapper(
            deployments.register,
        )
        self.rollback = to_raw_response_wrapper(
            deployments.rollback,
        )

    @cached_property
    def versions(self) -> VersionsResourceWithRawResponse:
        return VersionsResourceWithRawResponse(self._deployments.versions)

    @cached_property
    def events(self) -> EventsResourceWithRawResponse:
        return EventsResourceWithRawResponse(self._deployments.events)


class AsyncDeploymentsResourceWithRawResponse:
    def __init__(self, deployments: AsyncDeploymentsResource) -> None:
        self._deployments = deployments

        self.retrieve = async_to_raw_response_wrapper(
            deployments.retrieve,
        )
        self.redeploy = async_to_raw_response_wrapper(
            deployments.redeploy,
        )
        self.register = async_to_raw_response_wrapper(
            deployments.register,
        )
        self.rollback = async_to_raw_response_wrapper(
            deployments.rollback,
        )

    @cached_property
    def versions(self) -> AsyncVersionsResourceWithRawResponse:
        return AsyncVersionsResourceWithRawResponse(self._deployments.versions)

    @cached_property
    def events(self) -> AsyncEventsResourceWithRawResponse:
        return AsyncEventsResourceWithRawResponse(self._deployments.events)


class DeploymentsResourceWithStreamingResponse:
    def __init__(self, deployments: DeploymentsResource) -> None:
        self._deployments = deployments

        self.retrieve = to_streamed_response_wrapper(
            deployments.retrieve,
        )
        self.redeploy = to_streamed_response_wrapper(
            deployments.redeploy,
        )
        self.register = to_streamed_response_wrapper(
            deployments.register,
        )
        self.rollback = to_streamed_response_wrapper(
            deployments.rollback,
        )

    @cached_property
    def versions(self) -> VersionsResourceWithStreamingResponse:
        return VersionsResourceWithStreamingResponse(self._deployments.versions)

    @cached_property
    def events(self) -> EventsResourceWithStreamingResponse:
        return EventsResourceWithStreamingResponse(self._deployments.events)


class AsyncDeploymentsResourceWithStreamingResponse:
    def __init__(self, deployments: AsyncDeploymentsResource) -> None:
        self._deployments = deployments

        self.retrieve = async_to_streamed_response_wrapper(
            deployments.retrieve,
        )
        self.redeploy = async_to_streamed_response_wrapper(
            deployments.redeploy,
        )
        self.register = async_to_streamed_response_wrapper(
            deployments.register,
        )
        self.rollback = async_to_streamed_response_wrapper(
            deployments.rollback,
        )

    @cached_property
    def versions(self) -> AsyncVersionsResourceWithStreamingResponse:
        return AsyncVersionsResourceWithStreamingResponse(self._deployments.versions)

    @cached_property
    def events(self) -> AsyncEventsResourceWithStreamingResponse:
        return AsyncEventsResourceWithStreamingResponse(self._deployments.events)
