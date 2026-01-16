# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from .secrets import (
    SecretsResource,
    AsyncSecretsResource,
    SecretsResourceWithRawResponse,
    AsyncSecretsResourceWithRawResponse,
    SecretsResourceWithStreamingResponse,
    AsyncSecretsResourceWithStreamingResponse,
)
from .rollback import (
    RollbackResource,
    AsyncRollbackResource,
    RollbackResourceWithRawResponse,
    AsyncRollbackResourceWithRawResponse,
    RollbackResourceWithStreamingResponse,
    AsyncRollbackResourceWithStreamingResponse,
)
from ...._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from .deployments import (
    DeploymentsResource,
    AsyncDeploymentsResource,
    DeploymentsResourceWithRawResponse,
    AsyncDeploymentsResourceWithRawResponse,
    DeploymentsResourceWithStreamingResponse,
    AsyncDeploymentsResourceWithStreamingResponse,
)
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.agents import environment_create_params, environment_update_params, environment_resolve_env_params
from ....types.agents.env_response import EnvResponse
from ....types.agents.env_list_response import EnvListResponse
from ....types.agents.delete_env_response import DeleteEnvResponse
from ....types.agents.resolve_env_response import ResolveEnvResponse

__all__ = ["EnvironmentsResource", "AsyncEnvironmentsResource"]


class EnvironmentsResource(SyncAPIResource):
    @cached_property
    def deployments(self) -> DeploymentsResource:
        return DeploymentsResource(self._client)

    @cached_property
    def secrets(self) -> SecretsResource:
        return SecretsResource(self._client)

    @cached_property
    def rollback(self) -> RollbackResource:
        return RollbackResource(self._client)

    @cached_property
    def with_raw_response(self) -> EnvironmentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return EnvironmentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EnvironmentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return EnvironmentsResourceWithStreamingResponse(self)

    def create(
        self,
        agent_name: str,
        *,
        namespace_slug: str,
        branch_rules: SequenceNotStr[str],
        name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EnvResponse:
        """
        Create a new environment for an agent.

            Environments define deployment targets with branch matching rules.
            The is_prod flag cannot be set via API - production environment is protected.

            **Branch Rules:**
            - Exact match: ["main"] or ["develop"]
            - Wildcard: ["feature/*"] matches feature/foo, feature/bar
            - Catch-all: ["*"] matches any branch

        Args:
          branch_rules: Branch patterns for matching (e.g., ['feature/*'], ['develop'])

          name: Environment name (lowercase alphanumeric and hyphens only)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not namespace_slug:
            raise ValueError(f"Expected a non-empty value for `namespace_slug` but received {namespace_slug!r}")
        if not agent_name:
            raise ValueError(f"Expected a non-empty value for `agent_name` but received {agent_name!r}")
        return self._post(
            f"/agents/{namespace_slug}/{agent_name}/environments",
            body=maybe_transform(
                {
                    "branch_rules": branch_rules,
                    "name": name,
                },
                environment_create_params.EnvironmentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EnvResponse,
        )

    def retrieve(
        self,
        env_name: str,
        *,
        namespace_slug: str,
        agent_name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EnvResponse:
        """
        Get environment details by name.

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
        if not env_name:
            raise ValueError(f"Expected a non-empty value for `env_name` but received {env_name!r}")
        return self._get(
            f"/agents/{namespace_slug}/{agent_name}/environments/{env_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EnvResponse,
        )

    def update(
        self,
        env_name: str,
        *,
        namespace_slug: str,
        agent_name: str,
        branch_rules: Optional[SequenceNotStr[str]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EnvResponse:
        """
        Update an existing environment.

            All fields are optional - only provided fields will be updated.

            **Production Environment Constraints:**
            - branch_rules must be exactly one literal string (no wildcards)
            - is_prod cannot be changed via API

        Args:
          branch_rules: Branch patterns for matching

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not namespace_slug:
            raise ValueError(f"Expected a non-empty value for `namespace_slug` but received {namespace_slug!r}")
        if not agent_name:
            raise ValueError(f"Expected a non-empty value for `agent_name` but received {agent_name!r}")
        if not env_name:
            raise ValueError(f"Expected a non-empty value for `env_name` but received {env_name!r}")
        return self._put(
            f"/agents/{namespace_slug}/{agent_name}/environments/{env_name}",
            body=maybe_transform({"branch_rules": branch_rules}, environment_update_params.EnvironmentUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EnvResponse,
        )

    def list(
        self,
        agent_name: str,
        *,
        namespace_slug: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EnvListResponse:
        """
        List all environments for an agent.

            Environments define deployment targets (e.g., production, staging, preview).

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
        return self._get(
            f"/agents/{namespace_slug}/{agent_name}/environments",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EnvListResponse,
        )

    def delete(
        self,
        env_name: str,
        *,
        namespace_slug: str,
        agent_name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeleteEnvResponse:
        """
        Delete an environment.

            **Note:** Production environments (is_prod=True) cannot be deleted.

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
        if not env_name:
            raise ValueError(f"Expected a non-empty value for `env_name` but received {env_name!r}")
        return self._delete(
            f"/agents/{namespace_slug}/{agent_name}/environments/{env_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteEnvResponse,
        )

    def resolve_env(
        self,
        agent_name: str,
        *,
        namespace_slug: str,
        branch: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ResolveEnvResponse:
        """
        Resolve which environment matches a given branch.

            Uses specificity-based matching:
            - Exact match wins over wildcards (e.g., "main" matches production before preview)
            - Prefix wildcards match by length (e.g., "feature/*" beats "*")
            - Catch-all "*" has lowest priority

            Returns 404 if no environment matches the branch.

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
        return self._get(
            f"/agents/{namespace_slug}/{agent_name}/resolve-env",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"branch": branch}, environment_resolve_env_params.EnvironmentResolveEnvParams),
            ),
            cast_to=ResolveEnvResponse,
        )


class AsyncEnvironmentsResource(AsyncAPIResource):
    @cached_property
    def deployments(self) -> AsyncDeploymentsResource:
        return AsyncDeploymentsResource(self._client)

    @cached_property
    def secrets(self) -> AsyncSecretsResource:
        return AsyncSecretsResource(self._client)

    @cached_property
    def rollback(self) -> AsyncRollbackResource:
        return AsyncRollbackResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncEnvironmentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncEnvironmentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEnvironmentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return AsyncEnvironmentsResourceWithStreamingResponse(self)

    async def create(
        self,
        agent_name: str,
        *,
        namespace_slug: str,
        branch_rules: SequenceNotStr[str],
        name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EnvResponse:
        """
        Create a new environment for an agent.

            Environments define deployment targets with branch matching rules.
            The is_prod flag cannot be set via API - production environment is protected.

            **Branch Rules:**
            - Exact match: ["main"] or ["develop"]
            - Wildcard: ["feature/*"] matches feature/foo, feature/bar
            - Catch-all: ["*"] matches any branch

        Args:
          branch_rules: Branch patterns for matching (e.g., ['feature/*'], ['develop'])

          name: Environment name (lowercase alphanumeric and hyphens only)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not namespace_slug:
            raise ValueError(f"Expected a non-empty value for `namespace_slug` but received {namespace_slug!r}")
        if not agent_name:
            raise ValueError(f"Expected a non-empty value for `agent_name` but received {agent_name!r}")
        return await self._post(
            f"/agents/{namespace_slug}/{agent_name}/environments",
            body=await async_maybe_transform(
                {
                    "branch_rules": branch_rules,
                    "name": name,
                },
                environment_create_params.EnvironmentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EnvResponse,
        )

    async def retrieve(
        self,
        env_name: str,
        *,
        namespace_slug: str,
        agent_name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EnvResponse:
        """
        Get environment details by name.

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
        if not env_name:
            raise ValueError(f"Expected a non-empty value for `env_name` but received {env_name!r}")
        return await self._get(
            f"/agents/{namespace_slug}/{agent_name}/environments/{env_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EnvResponse,
        )

    async def update(
        self,
        env_name: str,
        *,
        namespace_slug: str,
        agent_name: str,
        branch_rules: Optional[SequenceNotStr[str]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EnvResponse:
        """
        Update an existing environment.

            All fields are optional - only provided fields will be updated.

            **Production Environment Constraints:**
            - branch_rules must be exactly one literal string (no wildcards)
            - is_prod cannot be changed via API

        Args:
          branch_rules: Branch patterns for matching

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not namespace_slug:
            raise ValueError(f"Expected a non-empty value for `namespace_slug` but received {namespace_slug!r}")
        if not agent_name:
            raise ValueError(f"Expected a non-empty value for `agent_name` but received {agent_name!r}")
        if not env_name:
            raise ValueError(f"Expected a non-empty value for `env_name` but received {env_name!r}")
        return await self._put(
            f"/agents/{namespace_slug}/{agent_name}/environments/{env_name}",
            body=await async_maybe_transform(
                {"branch_rules": branch_rules}, environment_update_params.EnvironmentUpdateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EnvResponse,
        )

    async def list(
        self,
        agent_name: str,
        *,
        namespace_slug: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EnvListResponse:
        """
        List all environments for an agent.

            Environments define deployment targets (e.g., production, staging, preview).

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
        return await self._get(
            f"/agents/{namespace_slug}/{agent_name}/environments",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EnvListResponse,
        )

    async def delete(
        self,
        env_name: str,
        *,
        namespace_slug: str,
        agent_name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeleteEnvResponse:
        """
        Delete an environment.

            **Note:** Production environments (is_prod=True) cannot be deleted.

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
        if not env_name:
            raise ValueError(f"Expected a non-empty value for `env_name` but received {env_name!r}")
        return await self._delete(
            f"/agents/{namespace_slug}/{agent_name}/environments/{env_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteEnvResponse,
        )

    async def resolve_env(
        self,
        agent_name: str,
        *,
        namespace_slug: str,
        branch: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ResolveEnvResponse:
        """
        Resolve which environment matches a given branch.

            Uses specificity-based matching:
            - Exact match wins over wildcards (e.g., "main" matches production before preview)
            - Prefix wildcards match by length (e.g., "feature/*" beats "*")
            - Catch-all "*" has lowest priority

            Returns 404 if no environment matches the branch.

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
        return await self._get(
            f"/agents/{namespace_slug}/{agent_name}/resolve-env",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"branch": branch}, environment_resolve_env_params.EnvironmentResolveEnvParams
                ),
            ),
            cast_to=ResolveEnvResponse,
        )


class EnvironmentsResourceWithRawResponse:
    def __init__(self, environments: EnvironmentsResource) -> None:
        self._environments = environments

        self.create = to_raw_response_wrapper(
            environments.create,
        )
        self.retrieve = to_raw_response_wrapper(
            environments.retrieve,
        )
        self.update = to_raw_response_wrapper(
            environments.update,
        )
        self.list = to_raw_response_wrapper(
            environments.list,
        )
        self.delete = to_raw_response_wrapper(
            environments.delete,
        )
        self.resolve_env = to_raw_response_wrapper(
            environments.resolve_env,
        )

    @cached_property
    def deployments(self) -> DeploymentsResourceWithRawResponse:
        return DeploymentsResourceWithRawResponse(self._environments.deployments)

    @cached_property
    def secrets(self) -> SecretsResourceWithRawResponse:
        return SecretsResourceWithRawResponse(self._environments.secrets)

    @cached_property
    def rollback(self) -> RollbackResourceWithRawResponse:
        return RollbackResourceWithRawResponse(self._environments.rollback)


class AsyncEnvironmentsResourceWithRawResponse:
    def __init__(self, environments: AsyncEnvironmentsResource) -> None:
        self._environments = environments

        self.create = async_to_raw_response_wrapper(
            environments.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            environments.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            environments.update,
        )
        self.list = async_to_raw_response_wrapper(
            environments.list,
        )
        self.delete = async_to_raw_response_wrapper(
            environments.delete,
        )
        self.resolve_env = async_to_raw_response_wrapper(
            environments.resolve_env,
        )

    @cached_property
    def deployments(self) -> AsyncDeploymentsResourceWithRawResponse:
        return AsyncDeploymentsResourceWithRawResponse(self._environments.deployments)

    @cached_property
    def secrets(self) -> AsyncSecretsResourceWithRawResponse:
        return AsyncSecretsResourceWithRawResponse(self._environments.secrets)

    @cached_property
    def rollback(self) -> AsyncRollbackResourceWithRawResponse:
        return AsyncRollbackResourceWithRawResponse(self._environments.rollback)


class EnvironmentsResourceWithStreamingResponse:
    def __init__(self, environments: EnvironmentsResource) -> None:
        self._environments = environments

        self.create = to_streamed_response_wrapper(
            environments.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            environments.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            environments.update,
        )
        self.list = to_streamed_response_wrapper(
            environments.list,
        )
        self.delete = to_streamed_response_wrapper(
            environments.delete,
        )
        self.resolve_env = to_streamed_response_wrapper(
            environments.resolve_env,
        )

    @cached_property
    def deployments(self) -> DeploymentsResourceWithStreamingResponse:
        return DeploymentsResourceWithStreamingResponse(self._environments.deployments)

    @cached_property
    def secrets(self) -> SecretsResourceWithStreamingResponse:
        return SecretsResourceWithStreamingResponse(self._environments.secrets)

    @cached_property
    def rollback(self) -> RollbackResourceWithStreamingResponse:
        return RollbackResourceWithStreamingResponse(self._environments.rollback)


class AsyncEnvironmentsResourceWithStreamingResponse:
    def __init__(self, environments: AsyncEnvironmentsResource) -> None:
        self._environments = environments

        self.create = async_to_streamed_response_wrapper(
            environments.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            environments.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            environments.update,
        )
        self.list = async_to_streamed_response_wrapper(
            environments.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            environments.delete,
        )
        self.resolve_env = async_to_streamed_response_wrapper(
            environments.resolve_env,
        )

    @cached_property
    def deployments(self) -> AsyncDeploymentsResourceWithStreamingResponse:
        return AsyncDeploymentsResourceWithStreamingResponse(self._environments.deployments)

    @cached_property
    def secrets(self) -> AsyncSecretsResourceWithStreamingResponse:
        return AsyncSecretsResourceWithStreamingResponse(self._environments.secrets)

    @cached_property
    def rollback(self) -> AsyncRollbackResourceWithStreamingResponse:
        return AsyncRollbackResourceWithStreamingResponse(self._environments.rollback)
