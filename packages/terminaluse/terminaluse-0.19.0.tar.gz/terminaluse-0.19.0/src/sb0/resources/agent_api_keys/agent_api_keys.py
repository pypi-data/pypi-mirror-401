# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from .name import (
    NameResource,
    AsyncNameResource,
    NameResourceWithRawResponse,
    AsyncNameResourceWithRawResponse,
    NameResourceWithStreamingResponse,
    AsyncNameResourceWithStreamingResponse,
)
from ...types import AgentAPIKeyType, agent_api_key_list_params, agent_api_key_create_params
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
from ...types.agent_api_key import AgentAPIKey
from ...types.agent_api_key_type import AgentAPIKeyType
from ...types.create_api_key_response import CreateAPIKeyResponse
from ...types.agent_api_key_list_response import AgentAPIKeyListResponse

__all__ = ["AgentAPIKeysResource", "AsyncAgentAPIKeysResource"]


class AgentAPIKeysResource(SyncAPIResource):
    @cached_property
    def name(self) -> NameResource:
        return NameResource(self._client)

    @cached_property
    def with_raw_response(self) -> AgentAPIKeysResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AgentAPIKeysResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AgentAPIKeysResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return AgentAPIKeysResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        agent_id: Optional[str] | Omit = omit,
        agent_name: Optional[str] | Omit = omit,
        api_key: Optional[str] | Omit = omit,
        api_key_type: AgentAPIKeyType | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CreateAPIKeyResponse:
        """
        Create Api Key

        Args:
          name: The name of the agent's API key.

          agent_id: The UUID of the agent

          agent_name: The name of the agent - if not provided, the agent_id must be set.

          api_key: Optionally provide the API key value - if not set, one will be generated.

          api_key_type: The type of the agent API key (external by default).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/agent_api_keys",
            body=maybe_transform(
                {
                    "name": name,
                    "agent_id": agent_id,
                    "agent_name": agent_name,
                    "api_key": api_key,
                    "api_key_type": api_key_type,
                },
                agent_api_key_create_params.AgentAPIKeyCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CreateAPIKeyResponse,
        )

    def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentAPIKey:
        """
        Return API key by ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/agent_api_keys/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentAPIKey,
        )

    def list(
        self,
        *,
        agent_id: Optional[str] | Omit = omit,
        agent_name: Optional[str] | Omit = omit,
        limit: int | Omit = omit,
        page_number: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentAPIKeyListResponse:
        """
        List API keys for an agent ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/agent_api_keys",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "agent_id": agent_id,
                        "agent_name": agent_name,
                        "limit": limit,
                        "page_number": page_number,
                    },
                    agent_api_key_list_params.AgentAPIKeyListParams,
                ),
            ),
            cast_to=AgentAPIKeyListResponse,
        )

    def delete(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> str:
        """
        Delete API key by ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._delete(
            f"/agent_api_keys/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )


class AsyncAgentAPIKeysResource(AsyncAPIResource):
    @cached_property
    def name(self) -> AsyncNameResource:
        return AsyncNameResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncAgentAPIKeysResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncAgentAPIKeysResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAgentAPIKeysResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return AsyncAgentAPIKeysResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        agent_id: Optional[str] | Omit = omit,
        agent_name: Optional[str] | Omit = omit,
        api_key: Optional[str] | Omit = omit,
        api_key_type: AgentAPIKeyType | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CreateAPIKeyResponse:
        """
        Create Api Key

        Args:
          name: The name of the agent's API key.

          agent_id: The UUID of the agent

          agent_name: The name of the agent - if not provided, the agent_id must be set.

          api_key: Optionally provide the API key value - if not set, one will be generated.

          api_key_type: The type of the agent API key (external by default).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/agent_api_keys",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "agent_id": agent_id,
                    "agent_name": agent_name,
                    "api_key": api_key,
                    "api_key_type": api_key_type,
                },
                agent_api_key_create_params.AgentAPIKeyCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CreateAPIKeyResponse,
        )

    async def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentAPIKey:
        """
        Return API key by ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/agent_api_keys/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentAPIKey,
        )

    async def list(
        self,
        *,
        agent_id: Optional[str] | Omit = omit,
        agent_name: Optional[str] | Omit = omit,
        limit: int | Omit = omit,
        page_number: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentAPIKeyListResponse:
        """
        List API keys for an agent ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/agent_api_keys",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "agent_id": agent_id,
                        "agent_name": agent_name,
                        "limit": limit,
                        "page_number": page_number,
                    },
                    agent_api_key_list_params.AgentAPIKeyListParams,
                ),
            ),
            cast_to=AgentAPIKeyListResponse,
        )

    async def delete(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> str:
        """
        Delete API key by ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._delete(
            f"/agent_api_keys/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )


class AgentAPIKeysResourceWithRawResponse:
    def __init__(self, agent_api_keys: AgentAPIKeysResource) -> None:
        self._agent_api_keys = agent_api_keys

        self.create = to_raw_response_wrapper(
            agent_api_keys.create,
        )
        self.retrieve = to_raw_response_wrapper(
            agent_api_keys.retrieve,
        )
        self.list = to_raw_response_wrapper(
            agent_api_keys.list,
        )
        self.delete = to_raw_response_wrapper(
            agent_api_keys.delete,
        )

    @cached_property
    def name(self) -> NameResourceWithRawResponse:
        return NameResourceWithRawResponse(self._agent_api_keys.name)


class AsyncAgentAPIKeysResourceWithRawResponse:
    def __init__(self, agent_api_keys: AsyncAgentAPIKeysResource) -> None:
        self._agent_api_keys = agent_api_keys

        self.create = async_to_raw_response_wrapper(
            agent_api_keys.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            agent_api_keys.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            agent_api_keys.list,
        )
        self.delete = async_to_raw_response_wrapper(
            agent_api_keys.delete,
        )

    @cached_property
    def name(self) -> AsyncNameResourceWithRawResponse:
        return AsyncNameResourceWithRawResponse(self._agent_api_keys.name)


class AgentAPIKeysResourceWithStreamingResponse:
    def __init__(self, agent_api_keys: AgentAPIKeysResource) -> None:
        self._agent_api_keys = agent_api_keys

        self.create = to_streamed_response_wrapper(
            agent_api_keys.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            agent_api_keys.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            agent_api_keys.list,
        )
        self.delete = to_streamed_response_wrapper(
            agent_api_keys.delete,
        )

    @cached_property
    def name(self) -> NameResourceWithStreamingResponse:
        return NameResourceWithStreamingResponse(self._agent_api_keys.name)


class AsyncAgentAPIKeysResourceWithStreamingResponse:
    def __init__(self, agent_api_keys: AsyncAgentAPIKeysResource) -> None:
        self._agent_api_keys = agent_api_keys

        self.create = async_to_streamed_response_wrapper(
            agent_api_keys.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            agent_api_keys.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            agent_api_keys.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            agent_api_keys.delete,
        )

    @cached_property
    def name(self) -> AsyncNameResourceWithStreamingResponse:
        return AsyncNameResourceWithStreamingResponse(self._agent_api_keys.name)
