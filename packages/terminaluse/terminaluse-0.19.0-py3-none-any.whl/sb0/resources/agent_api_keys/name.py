# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ...types import AgentAPIKeyType
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
from ...types.agent_api_keys import name_delete_params, name_retrieve_params
from ...types.agent_api_key_type import AgentAPIKeyType

__all__ = ["NameResource", "AsyncNameResource"]


class NameResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> NameResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return NameResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> NameResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return NameResourceWithStreamingResponse(self)

    def retrieve(
        self,
        name: str,
        *,
        agent_id: Optional[str] | Omit = omit,
        agent_name: Optional[str] | Omit = omit,
        api_key_type: AgentAPIKeyType | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentAPIKey:
        """
        Return named API key for the agent ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return self._get(
            f"/agent_api_keys/name/{name}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "agent_id": agent_id,
                        "agent_name": agent_name,
                        "api_key_type": api_key_type,
                    },
                    name_retrieve_params.NameRetrieveParams,
                ),
            ),
            cast_to=AgentAPIKey,
        )

    def delete(
        self,
        api_key_name: str,
        *,
        agent_id: Optional[str] | Omit = omit,
        agent_name: Optional[str] | Omit = omit,
        api_key_type: AgentAPIKeyType | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> str:
        """
        Delete API key by name.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not api_key_name:
            raise ValueError(f"Expected a non-empty value for `api_key_name` but received {api_key_name!r}")
        return self._delete(
            f"/agent_api_keys/name/{api_key_name}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "agent_id": agent_id,
                        "agent_name": agent_name,
                        "api_key_type": api_key_type,
                    },
                    name_delete_params.NameDeleteParams,
                ),
            ),
            cast_to=str,
        )


class AsyncNameResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncNameResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncNameResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncNameResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return AsyncNameResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        name: str,
        *,
        agent_id: Optional[str] | Omit = omit,
        agent_name: Optional[str] | Omit = omit,
        api_key_type: AgentAPIKeyType | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentAPIKey:
        """
        Return named API key for the agent ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return await self._get(
            f"/agent_api_keys/name/{name}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "agent_id": agent_id,
                        "agent_name": agent_name,
                        "api_key_type": api_key_type,
                    },
                    name_retrieve_params.NameRetrieveParams,
                ),
            ),
            cast_to=AgentAPIKey,
        )

    async def delete(
        self,
        api_key_name: str,
        *,
        agent_id: Optional[str] | Omit = omit,
        agent_name: Optional[str] | Omit = omit,
        api_key_type: AgentAPIKeyType | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> str:
        """
        Delete API key by name.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not api_key_name:
            raise ValueError(f"Expected a non-empty value for `api_key_name` but received {api_key_name!r}")
        return await self._delete(
            f"/agent_api_keys/name/{api_key_name}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "agent_id": agent_id,
                        "agent_name": agent_name,
                        "api_key_type": api_key_type,
                    },
                    name_delete_params.NameDeleteParams,
                ),
            ),
            cast_to=str,
        )


class NameResourceWithRawResponse:
    def __init__(self, name: NameResource) -> None:
        self._name = name

        self.retrieve = to_raw_response_wrapper(
            name.retrieve,
        )
        self.delete = to_raw_response_wrapper(
            name.delete,
        )


class AsyncNameResourceWithRawResponse:
    def __init__(self, name: AsyncNameResource) -> None:
        self._name = name

        self.retrieve = async_to_raw_response_wrapper(
            name.retrieve,
        )
        self.delete = async_to_raw_response_wrapper(
            name.delete,
        )


class NameResourceWithStreamingResponse:
    def __init__(self, name: NameResource) -> None:
        self._name = name

        self.retrieve = to_streamed_response_wrapper(
            name.retrieve,
        )
        self.delete = to_streamed_response_wrapper(
            name.delete,
        )


class AsyncNameResourceWithStreamingResponse:
    def __init__(self, name: AsyncNameResource) -> None:
        self._name = name

        self.retrieve = async_to_streamed_response_wrapper(
            name.retrieve,
        )
        self.delete = async_to_streamed_response_wrapper(
            name.delete,
        )
