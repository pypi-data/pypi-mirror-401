# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict

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
from ....types.agents.environments import secret_set_params, secret_list_params, secret_delete_params
from ....types.agents.environments.set_env_var_response import SetEnvVarResponse
from ....types.agents.environments.env_var_list_response import EnvVarListResponse
from ....types.agents.environments.delete_env_var_response import DeleteEnvVarResponse
from ....types.agents.environments.deployed_secrets_response import DeployedSecretsResponse

__all__ = ["SecretsResource", "AsyncSecretsResource"]


class SecretsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SecretsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return SecretsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SecretsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return SecretsResourceWithStreamingResponse(self)

    def list(
        self,
        env_name: str,
        *,
        namespace_slug: str,
        agent_name: str,
        include_values: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EnvVarListResponse:
        """
        List PENDING secrets for an environment (from EnvVar table).

            This is what will be used on next deploy.
            For deployed state, use GET /agents/{namespace_slug}/{agent_name}/environments/{env}/secrets/deployed

            Note: is_secret=True values are NEVER returned, only non-secrets when include_values=True.

        Args:
          include_values: Include values for non-secrets (is_secret=False only)

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
            f"/agents/{namespace_slug}/{agent_name}/environments/{env_name}/secrets",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"include_values": include_values}, secret_list_params.SecretListParams),
            ),
            cast_to=EnvVarListResponse,
        )

    def delete(
        self,
        key: str,
        *,
        namespace_slug: str,
        agent_name: str,
        env_name: str,
        redeploy: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeleteEnvVarResponse:
        """
        Delete a secret from an environment.

            If redeploy=True (default), triggers redeploy with updated secrets.

        Args:
          redeploy: If true, trigger redeploy after deletion

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
        if not key:
            raise ValueError(f"Expected a non-empty value for `key` but received {key!r}")
        return self._delete(
            f"/agents/{namespace_slug}/{agent_name}/environments/{env_name}/secrets/{key}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"redeploy": redeploy}, secret_delete_params.SecretDeleteParams),
            ),
            cast_to=DeleteEnvVarResponse,
        )

    def list_deployed(
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
    ) -> DeployedSecretsResponse:
        """
        List DEPLOYED secrets for an environment (from Version.secrets_snapshot).

            This is what's currently running. May differ from pending state after rollback.
            Only returns keys, never actual values.

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
            f"/agents/{namespace_slug}/{agent_name}/environments/{env_name}/secrets/deployed",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeployedSecretsResponse,
        )

    def set(
        self,
        env_name: str,
        *,
        namespace_slug: str,
        agent_name: str,
        secrets: Dict[str, secret_set_params.Secrets],
        redeploy: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SetEnvVarResponse:
        """
        Set one or more secrets/config values.

            If redeploy=True (default) and environment has active deployment,
            triggers redeploy with same image but new secrets_snapshot.

        Args:
          secrets: Dict of {key: {value, is_secret}} to set

          redeploy: If true and env has active deployment, trigger redeploy with new secrets

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
            f"/agents/{namespace_slug}/{agent_name}/environments/{env_name}/secrets",
            body=maybe_transform(
                {
                    "secrets": secrets,
                    "redeploy": redeploy,
                },
                secret_set_params.SecretSetParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SetEnvVarResponse,
        )


class AsyncSecretsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSecretsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncSecretsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSecretsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return AsyncSecretsResourceWithStreamingResponse(self)

    async def list(
        self,
        env_name: str,
        *,
        namespace_slug: str,
        agent_name: str,
        include_values: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EnvVarListResponse:
        """
        List PENDING secrets for an environment (from EnvVar table).

            This is what will be used on next deploy.
            For deployed state, use GET /agents/{namespace_slug}/{agent_name}/environments/{env}/secrets/deployed

            Note: is_secret=True values are NEVER returned, only non-secrets when include_values=True.

        Args:
          include_values: Include values for non-secrets (is_secret=False only)

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
            f"/agents/{namespace_slug}/{agent_name}/environments/{env_name}/secrets",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"include_values": include_values}, secret_list_params.SecretListParams
                ),
            ),
            cast_to=EnvVarListResponse,
        )

    async def delete(
        self,
        key: str,
        *,
        namespace_slug: str,
        agent_name: str,
        env_name: str,
        redeploy: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeleteEnvVarResponse:
        """
        Delete a secret from an environment.

            If redeploy=True (default), triggers redeploy with updated secrets.

        Args:
          redeploy: If true, trigger redeploy after deletion

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
        if not key:
            raise ValueError(f"Expected a non-empty value for `key` but received {key!r}")
        return await self._delete(
            f"/agents/{namespace_slug}/{agent_name}/environments/{env_name}/secrets/{key}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"redeploy": redeploy}, secret_delete_params.SecretDeleteParams),
            ),
            cast_to=DeleteEnvVarResponse,
        )

    async def list_deployed(
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
    ) -> DeployedSecretsResponse:
        """
        List DEPLOYED secrets for an environment (from Version.secrets_snapshot).

            This is what's currently running. May differ from pending state after rollback.
            Only returns keys, never actual values.

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
            f"/agents/{namespace_slug}/{agent_name}/environments/{env_name}/secrets/deployed",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeployedSecretsResponse,
        )

    async def set(
        self,
        env_name: str,
        *,
        namespace_slug: str,
        agent_name: str,
        secrets: Dict[str, secret_set_params.Secrets],
        redeploy: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SetEnvVarResponse:
        """
        Set one or more secrets/config values.

            If redeploy=True (default) and environment has active deployment,
            triggers redeploy with same image but new secrets_snapshot.

        Args:
          secrets: Dict of {key: {value, is_secret}} to set

          redeploy: If true and env has active deployment, trigger redeploy with new secrets

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
            f"/agents/{namespace_slug}/{agent_name}/environments/{env_name}/secrets",
            body=await async_maybe_transform(
                {
                    "secrets": secrets,
                    "redeploy": redeploy,
                },
                secret_set_params.SecretSetParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SetEnvVarResponse,
        )


class SecretsResourceWithRawResponse:
    def __init__(self, secrets: SecretsResource) -> None:
        self._secrets = secrets

        self.list = to_raw_response_wrapper(
            secrets.list,
        )
        self.delete = to_raw_response_wrapper(
            secrets.delete,
        )
        self.list_deployed = to_raw_response_wrapper(
            secrets.list_deployed,
        )
        self.set = to_raw_response_wrapper(
            secrets.set,
        )


class AsyncSecretsResourceWithRawResponse:
    def __init__(self, secrets: AsyncSecretsResource) -> None:
        self._secrets = secrets

        self.list = async_to_raw_response_wrapper(
            secrets.list,
        )
        self.delete = async_to_raw_response_wrapper(
            secrets.delete,
        )
        self.list_deployed = async_to_raw_response_wrapper(
            secrets.list_deployed,
        )
        self.set = async_to_raw_response_wrapper(
            secrets.set,
        )


class SecretsResourceWithStreamingResponse:
    def __init__(self, secrets: SecretsResource) -> None:
        self._secrets = secrets

        self.list = to_streamed_response_wrapper(
            secrets.list,
        )
        self.delete = to_streamed_response_wrapper(
            secrets.delete,
        )
        self.list_deployed = to_streamed_response_wrapper(
            secrets.list_deployed,
        )
        self.set = to_streamed_response_wrapper(
            secrets.set,
        )


class AsyncSecretsResourceWithStreamingResponse:
    def __init__(self, secrets: AsyncSecretsResource) -> None:
        self._secrets = secrets

        self.list = async_to_streamed_response_wrapper(
            secrets.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            secrets.delete,
        )
        self.list_deployed = async_to_streamed_response_wrapper(
            secrets.list_deployed,
        )
        self.set = async_to_streamed_response_wrapper(
            secrets.set,
        )
