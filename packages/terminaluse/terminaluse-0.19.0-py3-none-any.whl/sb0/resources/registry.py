# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import registry_auth_params
from .._types import Body, Query, Headers, NotGiven, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.registry_auth_response import RegistryAuthResponse

__all__ = ["RegistryResource", "AsyncRegistryResource"]


class RegistryResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RegistryResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return RegistryResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RegistryResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return RegistryResourceWithStreamingResponse(self)

    def auth(
        self,
        *,
        namespace: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RegistryAuthResponse:
        """
        Get short-lived credentials for pushing images to a namespace's registry.

            Each namespace has its own isolated registry repository. The token returned
            can ONLY push images to the specified namespace's repository.

            The CLI uses this endpoint to authenticate with Docker before pushing
            agent images. Returns a token valid for approximately 1 hour.

            **Image path convention:** `{registry_url}/{repository}/{agent}:{tag}`

            **Example:** `us-east4-docker.pkg.dev/sb0-prod/agents-acme/my-agent:abc123`

            Note: The `repository` field includes the namespace (e.g., `sb0-prod/agents-acme`).

            **Usage with Docker:**
            ```bash
            docker login {registry_url} -u {username} -p {token}
            docker push {registry_url}/{repository}/{agent}:{tag}
            ```

        Args:
          namespace: Target namespace for the image push

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/registry/auth",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"namespace": namespace}, registry_auth_params.RegistryAuthParams),
            ),
            cast_to=RegistryAuthResponse,
        )


class AsyncRegistryResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRegistryResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncRegistryResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRegistryResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return AsyncRegistryResourceWithStreamingResponse(self)

    async def auth(
        self,
        *,
        namespace: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RegistryAuthResponse:
        """
        Get short-lived credentials for pushing images to a namespace's registry.

            Each namespace has its own isolated registry repository. The token returned
            can ONLY push images to the specified namespace's repository.

            The CLI uses this endpoint to authenticate with Docker before pushing
            agent images. Returns a token valid for approximately 1 hour.

            **Image path convention:** `{registry_url}/{repository}/{agent}:{tag}`

            **Example:** `us-east4-docker.pkg.dev/sb0-prod/agents-acme/my-agent:abc123`

            Note: The `repository` field includes the namespace (e.g., `sb0-prod/agents-acme`).

            **Usage with Docker:**
            ```bash
            docker login {registry_url} -u {username} -p {token}
            docker push {registry_url}/{repository}/{agent}:{tag}
            ```

        Args:
          namespace: Target namespace for the image push

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/registry/auth",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"namespace": namespace}, registry_auth_params.RegistryAuthParams),
            ),
            cast_to=RegistryAuthResponse,
        )


class RegistryResourceWithRawResponse:
    def __init__(self, registry: RegistryResource) -> None:
        self._registry = registry

        self.auth = to_raw_response_wrapper(
            registry.auth,
        )


class AsyncRegistryResourceWithRawResponse:
    def __init__(self, registry: AsyncRegistryResource) -> None:
        self._registry = registry

        self.auth = async_to_raw_response_wrapper(
            registry.auth,
        )


class RegistryResourceWithStreamingResponse:
    def __init__(self, registry: RegistryResource) -> None:
        self._registry = registry

        self.auth = to_streamed_response_wrapper(
            registry.auth,
        )


class AsyncRegistryResourceWithStreamingResponse:
    def __init__(self, registry: AsyncRegistryResource) -> None:
        self._registry = registry

        self.auth = async_to_streamed_response_wrapper(
            registry.auth,
        )
