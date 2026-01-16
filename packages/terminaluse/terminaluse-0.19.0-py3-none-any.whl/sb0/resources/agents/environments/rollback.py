# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

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
from ....types.agents.environments import rollback_create_params
from ....types.agents.environments.rollback_response import RollbackResponse

__all__ = ["RollbackResource", "AsyncRollbackResource"]


class RollbackResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RollbackResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return RollbackResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RollbackResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return RollbackResourceWithStreamingResponse(self)

    def create(
        self,
        env_name: str,
        *,
        namespace_slug: str,
        agent_name: str,
        target_version_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RollbackResponse:
        """
        Roll back an environment to a previous version.

            Resolves environment to deployment via branch rules.
            Only works for environments with a single, literal branch rule (no wildcards).

            Key behavior:
            - EnvVar table is NOT modified (remains pending state for next deploy)
            - Uses Version.secrets_snapshot as deployed state

        Args:
          target_version_id: Version ID to rollback to (defaults to previous version if not specified)

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
        return self._post(
            f"/agents/{namespace_slug}/{agent_name}/environments/{env_name}/rollback",
            body=maybe_transform({"target_version_id": target_version_id}, rollback_create_params.RollbackCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RollbackResponse,
        )


class AsyncRollbackResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRollbackResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncRollbackResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRollbackResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return AsyncRollbackResourceWithStreamingResponse(self)

    async def create(
        self,
        env_name: str,
        *,
        namespace_slug: str,
        agent_name: str,
        target_version_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RollbackResponse:
        """
        Roll back an environment to a previous version.

            Resolves environment to deployment via branch rules.
            Only works for environments with a single, literal branch rule (no wildcards).

            Key behavior:
            - EnvVar table is NOT modified (remains pending state for next deploy)
            - Uses Version.secrets_snapshot as deployed state

        Args:
          target_version_id: Version ID to rollback to (defaults to previous version if not specified)

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
        return await self._post(
            f"/agents/{namespace_slug}/{agent_name}/environments/{env_name}/rollback",
            body=await async_maybe_transform(
                {"target_version_id": target_version_id}, rollback_create_params.RollbackCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RollbackResponse,
        )


class RollbackResourceWithRawResponse:
    def __init__(self, rollback: RollbackResource) -> None:
        self._rollback = rollback

        self.create = to_raw_response_wrapper(
            rollback.create,
        )


class AsyncRollbackResourceWithRawResponse:
    def __init__(self, rollback: AsyncRollbackResource) -> None:
        self._rollback = rollback

        self.create = async_to_raw_response_wrapper(
            rollback.create,
        )


class RollbackResourceWithStreamingResponse:
    def __init__(self, rollback: RollbackResource) -> None:
        self._rollback = rollback

        self.create = to_streamed_response_wrapper(
            rollback.create,
        )


class AsyncRollbackResourceWithStreamingResponse:
    def __init__(self, rollback: AsyncRollbackResource) -> None:
        self._rollback = rollback

        self.create = async_to_streamed_response_wrapper(
            rollback.create,
        )
