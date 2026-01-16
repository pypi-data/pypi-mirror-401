# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Optional
from typing_extensions import Literal

import httpx

from .name import (
    NameResource,
    AsyncNameResource,
    NameResourceWithRawResponse,
    AsyncNameResourceWithRawResponse,
    NameResourceWithStreamingResponse,
    AsyncNameResourceWithStreamingResponse,
)
from ...types import (
    AgentRpcMethod,
    DeploymentAcpType,
    agent_rpc_params,
    agent_list_params,
    agent_deploy_params,
    agent_handle_rpc_params,
    agent_rpc_by_name_params,
)
from .secrets import (
    SecretsResource,
    AsyncSecretsResource,
    SecretsResourceWithRawResponse,
    AsyncSecretsResourceWithRawResponse,
    SecretsResourceWithStreamingResponse,
    AsyncSecretsResourceWithStreamingResponse,
)
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from .schedules import (
    SchedulesResource,
    AsyncSchedulesResource,
    SchedulesResourceWithRawResponse,
    AsyncSchedulesResourceWithRawResponse,
    SchedulesResourceWithStreamingResponse,
    AsyncSchedulesResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...types.agent import Agent
from ..._base_client import make_request_options
from .forward.forward import (
    ForwardResource,
    AsyncForwardResource,
    ForwardResourceWithRawResponse,
    AsyncForwardResourceWithRawResponse,
    ForwardResourceWithStreamingResponse,
    AsyncForwardResourceWithStreamingResponse,
)
from ...types.delete_response import DeleteResponse
from ...types.deploy_response import DeployResponse
from .deployments.deployments import (
    DeploymentsResource,
    AsyncDeploymentsResource,
    DeploymentsResourceWithRawResponse,
    AsyncDeploymentsResourceWithRawResponse,
    DeploymentsResourceWithStreamingResponse,
    AsyncDeploymentsResourceWithStreamingResponse,
)
from ...types.agent_rpc_method import AgentRpcMethod
from .environments.environments import (
    EnvironmentsResource,
    AsyncEnvironmentsResource,
    EnvironmentsResourceWithRawResponse,
    AsyncEnvironmentsResourceWithRawResponse,
    EnvironmentsResourceWithStreamingResponse,
    AsyncEnvironmentsResourceWithStreamingResponse,
)
from ...types.agent_rpc_response import AgentRpcResponse
from ...types.agent_list_response import AgentListResponse
from ...types.deployment_acp_type import DeploymentAcpType

__all__ = ["AgentsResource", "AsyncAgentsResource"]


class AgentsResource(SyncAPIResource):
    @cached_property
    def name(self) -> NameResource:
        return NameResource(self._client)

    @cached_property
    def forward(self) -> ForwardResource:
        return ForwardResource(self._client)

    @cached_property
    def schedules(self) -> SchedulesResource:
        return SchedulesResource(self._client)

    @cached_property
    def deployments(self) -> DeploymentsResource:
        return DeploymentsResource(self._client)

    @cached_property
    def environments(self) -> EnvironmentsResource:
        return EnvironmentsResource(self._client)

    @cached_property
    def secrets(self) -> SecretsResource:
        return SecretsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AgentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AgentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AgentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return AgentsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        agent_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Agent:
        """
        Get an agent by its unique ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        return self._get(
            f"/agents/{agent_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Agent,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        namespace_id: Optional[str] | Omit = omit,
        order_by: Optional[str] | Omit = omit,
        order_direction: str | Omit = omit,
        page_number: int | Omit = omit,
        task_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentListResponse:
        """
        List all registered agents, optionally filtered by query parameters.

        Args:
          limit: Limit

          namespace_id: Filter by namespace (currently accepts slug)

          order_by: Field to order by

          order_direction: Order direction (asc or desc)

          page_number: Page number

          task_id: Task ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/agents",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "namespace_id": namespace_id,
                        "order_by": order_by,
                        "order_direction": order_direction,
                        "page_number": page_number,
                        "task_id": task_id,
                    },
                    agent_list_params.AgentListParams,
                ),
            ),
            cast_to=AgentListResponse,
        )

    def delete(
        self,
        agent_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeleteResponse:
        """
        Delete an agent by its unique ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        return self._delete(
            f"/agents/{agent_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteResponse,
        )

    def delete_by_name(
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
    ) -> DeleteResponse:
        """
        Delete an agent by namespace slug and agent name.

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
        return self._delete(
            f"/agents/name/{namespace_slug}/{agent_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteResponse,
        )

    def deploy(
        self,
        *,
        agent_name: str,
        author_email: str,
        author_name: str,
        branch: str,
        git_hash: str,
        image_url: str,
        acp_type: DeploymentAcpType | Omit = omit,
        are_tasks_sticky: Optional[bool] | Omit = omit,
        description: Optional[str] | Omit = omit,
        git_message: Optional[str] | Omit = omit,
        is_dirty: bool | Omit = omit,
        replicas: int | Omit = omit,
        resources: Optional[Dict[str, object]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeployResponse:
        """
        Deploy an agent to the platform.

            Called by CLI after pushing the container image to the registry.
            Creates or updates agent, deployment, and version records.

            The deployment is asynchronous - poll GET /deployments/{deployment_id}
            for status updates until status is READY or FAILED.

            **Flow:**
            1. CLI builds and pushes image to registry (using /registry/auth)
            2. CLI calls POST /agents/deploy with image details
            3. Platform creates records and triggers K8s deployment
            4. Container starts and calls POST /deployments/register
            5. CLI polls GET /deployments/{id} until READY

        Args:
          agent_name: Agent name in 'namespace_slug/agent_name' format (lowercase, alphanumeric,
              hyphens only)

          author_email: Git commit author email

          author_name: Git commit author name

          branch: Git branch name (e.g., 'main', 'feature/new-tool')

          git_hash: Git commit hash (short or full)

          image_url: Full container image URL (e.g., 'us-east4-docker.pkg.dev/proj/repo/agent:hash')

          acp_type: ACP server type (SYNC or ASYNC)

          are_tasks_sticky: If true, running tasks stay on their original version until completion during
              this deploy. If false or None, tasks are migrated to the new version
              immediately.

          description: Agent description (used when creating new agent)

          git_message: Git commit message (truncated if too long)

          is_dirty: Whether the working directory had uncommitted changes at deploy time

          replicas: Desired replica count (1-10)

          resources:
              Resource requests and limits (e.g., {'requests': {'cpu': '100m', 'memory':
              '256Mi'}, 'limits': {'cpu': '1000m', 'memory': '1Gi'}})

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/agents/deploy",
            body=maybe_transform(
                {
                    "agent_name": agent_name,
                    "author_email": author_email,
                    "author_name": author_name,
                    "branch": branch,
                    "git_hash": git_hash,
                    "image_url": image_url,
                    "acp_type": acp_type,
                    "are_tasks_sticky": are_tasks_sticky,
                    "description": description,
                    "git_message": git_message,
                    "is_dirty": is_dirty,
                    "replicas": replicas,
                    "resources": resources,
                },
                agent_deploy_params.AgentDeployParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeployResponse,
        )

    def handle_rpc(
        self,
        agent_id: str,
        *,
        namespace_id: str,
        method: AgentRpcMethod,
        params: agent_handle_rpc_params.Params,
        id: Union[int, str, None] | Omit = omit,
        jsonrpc: Literal["2.0"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentRpcResponse:
        """
        Handle JSON-RPC requests for an agent by its unique ID.

        Args:
          namespace_id: Namespace ID for workspace operations

          params: The parameters for the agent RPC request

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        return self._post(
            f"/agents/{agent_id}/rpc",
            body=maybe_transform(
                {
                    "method": method,
                    "params": params,
                    "id": id,
                    "jsonrpc": jsonrpc,
                },
                agent_handle_rpc_params.AgentHandleRpcParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"namespace_id": namespace_id}, agent_handle_rpc_params.AgentHandleRpcParams),
            ),
            cast_to=AgentRpcResponse,
        )

    def retrieve_by_name(
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
    ) -> Agent:
        """
        Get an agent by namespace slug and agent name.

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
            f"/agents/name/{namespace_slug}/{agent_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Agent,
        )

    def rpc(
        self,
        agent_id: str,
        *,
        namespace_id: str,
        method: AgentRpcMethod,
        params: agent_rpc_params.Params,
        id: Union[int, str, None] | Omit = omit,
        jsonrpc: Literal["2.0"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentRpcResponse:
        """
        Handle JSON-RPC requests for an agent by its unique ID.

        Args:
          namespace_id: Namespace ID for workspace operations

          params: The parameters for the agent RPC request

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        return self._post(
            f"/agents/{agent_id}/rpc",
            body=maybe_transform(
                {
                    "method": method,
                    "params": params,
                    "id": id,
                    "jsonrpc": jsonrpc,
                },
                agent_rpc_params.AgentRpcParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"namespace_id": namespace_id}, agent_rpc_params.AgentRpcParams),
            ),
            cast_to=AgentRpcResponse,
        )

    def rpc_by_name(
        self,
        agent_name: str,
        *,
        namespace_slug: str,
        namespace_id: str,
        method: AgentRpcMethod,
        params: agent_rpc_by_name_params.Params,
        id: Union[int, str, None] | Omit = omit,
        jsonrpc: Literal["2.0"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentRpcResponse:
        """
        Handle JSON-RPC requests for an agent by namespace slug and agent name.

        Args:
          namespace_id: Namespace ID for workspace operations

          params: The parameters for the agent RPC request

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
            f"/agents/name/{namespace_slug}/{agent_name}/rpc",
            body=maybe_transform(
                {
                    "method": method,
                    "params": params,
                    "id": id,
                    "jsonrpc": jsonrpc,
                },
                agent_rpc_by_name_params.AgentRpcByNameParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"namespace_id": namespace_id}, agent_rpc_by_name_params.AgentRpcByNameParams),
            ),
            cast_to=AgentRpcResponse,
        )


class AsyncAgentsResource(AsyncAPIResource):
    @cached_property
    def name(self) -> AsyncNameResource:
        return AsyncNameResource(self._client)

    @cached_property
    def forward(self) -> AsyncForwardResource:
        return AsyncForwardResource(self._client)

    @cached_property
    def schedules(self) -> AsyncSchedulesResource:
        return AsyncSchedulesResource(self._client)

    @cached_property
    def deployments(self) -> AsyncDeploymentsResource:
        return AsyncDeploymentsResource(self._client)

    @cached_property
    def environments(self) -> AsyncEnvironmentsResource:
        return AsyncEnvironmentsResource(self._client)

    @cached_property
    def secrets(self) -> AsyncSecretsResource:
        return AsyncSecretsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncAgentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncAgentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAgentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return AsyncAgentsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        agent_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Agent:
        """
        Get an agent by its unique ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        return await self._get(
            f"/agents/{agent_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Agent,
        )

    async def list(
        self,
        *,
        limit: int | Omit = omit,
        namespace_id: Optional[str] | Omit = omit,
        order_by: Optional[str] | Omit = omit,
        order_direction: str | Omit = omit,
        page_number: int | Omit = omit,
        task_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentListResponse:
        """
        List all registered agents, optionally filtered by query parameters.

        Args:
          limit: Limit

          namespace_id: Filter by namespace (currently accepts slug)

          order_by: Field to order by

          order_direction: Order direction (asc or desc)

          page_number: Page number

          task_id: Task ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/agents",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "namespace_id": namespace_id,
                        "order_by": order_by,
                        "order_direction": order_direction,
                        "page_number": page_number,
                        "task_id": task_id,
                    },
                    agent_list_params.AgentListParams,
                ),
            ),
            cast_to=AgentListResponse,
        )

    async def delete(
        self,
        agent_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeleteResponse:
        """
        Delete an agent by its unique ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        return await self._delete(
            f"/agents/{agent_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteResponse,
        )

    async def delete_by_name(
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
    ) -> DeleteResponse:
        """
        Delete an agent by namespace slug and agent name.

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
        return await self._delete(
            f"/agents/name/{namespace_slug}/{agent_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteResponse,
        )

    async def deploy(
        self,
        *,
        agent_name: str,
        author_email: str,
        author_name: str,
        branch: str,
        git_hash: str,
        image_url: str,
        acp_type: DeploymentAcpType | Omit = omit,
        are_tasks_sticky: Optional[bool] | Omit = omit,
        description: Optional[str] | Omit = omit,
        git_message: Optional[str] | Omit = omit,
        is_dirty: bool | Omit = omit,
        replicas: int | Omit = omit,
        resources: Optional[Dict[str, object]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeployResponse:
        """
        Deploy an agent to the platform.

            Called by CLI after pushing the container image to the registry.
            Creates or updates agent, deployment, and version records.

            The deployment is asynchronous - poll GET /deployments/{deployment_id}
            for status updates until status is READY or FAILED.

            **Flow:**
            1. CLI builds and pushes image to registry (using /registry/auth)
            2. CLI calls POST /agents/deploy with image details
            3. Platform creates records and triggers K8s deployment
            4. Container starts and calls POST /deployments/register
            5. CLI polls GET /deployments/{id} until READY

        Args:
          agent_name: Agent name in 'namespace_slug/agent_name' format (lowercase, alphanumeric,
              hyphens only)

          author_email: Git commit author email

          author_name: Git commit author name

          branch: Git branch name (e.g., 'main', 'feature/new-tool')

          git_hash: Git commit hash (short or full)

          image_url: Full container image URL (e.g., 'us-east4-docker.pkg.dev/proj/repo/agent:hash')

          acp_type: ACP server type (SYNC or ASYNC)

          are_tasks_sticky: If true, running tasks stay on their original version until completion during
              this deploy. If false or None, tasks are migrated to the new version
              immediately.

          description: Agent description (used when creating new agent)

          git_message: Git commit message (truncated if too long)

          is_dirty: Whether the working directory had uncommitted changes at deploy time

          replicas: Desired replica count (1-10)

          resources:
              Resource requests and limits (e.g., {'requests': {'cpu': '100m', 'memory':
              '256Mi'}, 'limits': {'cpu': '1000m', 'memory': '1Gi'}})

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/agents/deploy",
            body=await async_maybe_transform(
                {
                    "agent_name": agent_name,
                    "author_email": author_email,
                    "author_name": author_name,
                    "branch": branch,
                    "git_hash": git_hash,
                    "image_url": image_url,
                    "acp_type": acp_type,
                    "are_tasks_sticky": are_tasks_sticky,
                    "description": description,
                    "git_message": git_message,
                    "is_dirty": is_dirty,
                    "replicas": replicas,
                    "resources": resources,
                },
                agent_deploy_params.AgentDeployParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeployResponse,
        )

    async def handle_rpc(
        self,
        agent_id: str,
        *,
        namespace_id: str,
        method: AgentRpcMethod,
        params: agent_handle_rpc_params.Params,
        id: Union[int, str, None] | Omit = omit,
        jsonrpc: Literal["2.0"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentRpcResponse:
        """
        Handle JSON-RPC requests for an agent by its unique ID.

        Args:
          namespace_id: Namespace ID for workspace operations

          params: The parameters for the agent RPC request

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        return await self._post(
            f"/agents/{agent_id}/rpc",
            body=await async_maybe_transform(
                {
                    "method": method,
                    "params": params,
                    "id": id,
                    "jsonrpc": jsonrpc,
                },
                agent_handle_rpc_params.AgentHandleRpcParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"namespace_id": namespace_id}, agent_handle_rpc_params.AgentHandleRpcParams
                ),
            ),
            cast_to=AgentRpcResponse,
        )

    async def retrieve_by_name(
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
    ) -> Agent:
        """
        Get an agent by namespace slug and agent name.

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
            f"/agents/name/{namespace_slug}/{agent_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Agent,
        )

    async def rpc(
        self,
        agent_id: str,
        *,
        namespace_id: str,
        method: AgentRpcMethod,
        params: agent_rpc_params.Params,
        id: Union[int, str, None] | Omit = omit,
        jsonrpc: Literal["2.0"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentRpcResponse:
        """
        Handle JSON-RPC requests for an agent by its unique ID.

        Args:
          namespace_id: Namespace ID for workspace operations

          params: The parameters for the agent RPC request

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        return await self._post(
            f"/agents/{agent_id}/rpc",
            body=await async_maybe_transform(
                {
                    "method": method,
                    "params": params,
                    "id": id,
                    "jsonrpc": jsonrpc,
                },
                agent_rpc_params.AgentRpcParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"namespace_id": namespace_id}, agent_rpc_params.AgentRpcParams),
            ),
            cast_to=AgentRpcResponse,
        )

    async def rpc_by_name(
        self,
        agent_name: str,
        *,
        namespace_slug: str,
        namespace_id: str,
        method: AgentRpcMethod,
        params: agent_rpc_by_name_params.Params,
        id: Union[int, str, None] | Omit = omit,
        jsonrpc: Literal["2.0"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentRpcResponse:
        """
        Handle JSON-RPC requests for an agent by namespace slug and agent name.

        Args:
          namespace_id: Namespace ID for workspace operations

          params: The parameters for the agent RPC request

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
            f"/agents/name/{namespace_slug}/{agent_name}/rpc",
            body=await async_maybe_transform(
                {
                    "method": method,
                    "params": params,
                    "id": id,
                    "jsonrpc": jsonrpc,
                },
                agent_rpc_by_name_params.AgentRpcByNameParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"namespace_id": namespace_id}, agent_rpc_by_name_params.AgentRpcByNameParams
                ),
            ),
            cast_to=AgentRpcResponse,
        )


class AgentsResourceWithRawResponse:
    def __init__(self, agents: AgentsResource) -> None:
        self._agents = agents

        self.retrieve = to_raw_response_wrapper(
            agents.retrieve,
        )
        self.list = to_raw_response_wrapper(
            agents.list,
        )
        self.delete = to_raw_response_wrapper(
            agents.delete,
        )
        self.delete_by_name = to_raw_response_wrapper(
            agents.delete_by_name,
        )
        self.deploy = to_raw_response_wrapper(
            agents.deploy,
        )
        self.handle_rpc = to_raw_response_wrapper(
            agents.handle_rpc,
        )
        self.retrieve_by_name = to_raw_response_wrapper(
            agents.retrieve_by_name,
        )
        self.rpc = to_raw_response_wrapper(
            agents.rpc,
        )
        self.rpc_by_name = to_raw_response_wrapper(
            agents.rpc_by_name,
        )

    @cached_property
    def name(self) -> NameResourceWithRawResponse:
        return NameResourceWithRawResponse(self._agents.name)

    @cached_property
    def forward(self) -> ForwardResourceWithRawResponse:
        return ForwardResourceWithRawResponse(self._agents.forward)

    @cached_property
    def schedules(self) -> SchedulesResourceWithRawResponse:
        return SchedulesResourceWithRawResponse(self._agents.schedules)

    @cached_property
    def deployments(self) -> DeploymentsResourceWithRawResponse:
        return DeploymentsResourceWithRawResponse(self._agents.deployments)

    @cached_property
    def environments(self) -> EnvironmentsResourceWithRawResponse:
        return EnvironmentsResourceWithRawResponse(self._agents.environments)

    @cached_property
    def secrets(self) -> SecretsResourceWithRawResponse:
        return SecretsResourceWithRawResponse(self._agents.secrets)


class AsyncAgentsResourceWithRawResponse:
    def __init__(self, agents: AsyncAgentsResource) -> None:
        self._agents = agents

        self.retrieve = async_to_raw_response_wrapper(
            agents.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            agents.list,
        )
        self.delete = async_to_raw_response_wrapper(
            agents.delete,
        )
        self.delete_by_name = async_to_raw_response_wrapper(
            agents.delete_by_name,
        )
        self.deploy = async_to_raw_response_wrapper(
            agents.deploy,
        )
        self.handle_rpc = async_to_raw_response_wrapper(
            agents.handle_rpc,
        )
        self.retrieve_by_name = async_to_raw_response_wrapper(
            agents.retrieve_by_name,
        )
        self.rpc = async_to_raw_response_wrapper(
            agents.rpc,
        )
        self.rpc_by_name = async_to_raw_response_wrapper(
            agents.rpc_by_name,
        )

    @cached_property
    def name(self) -> AsyncNameResourceWithRawResponse:
        return AsyncNameResourceWithRawResponse(self._agents.name)

    @cached_property
    def forward(self) -> AsyncForwardResourceWithRawResponse:
        return AsyncForwardResourceWithRawResponse(self._agents.forward)

    @cached_property
    def schedules(self) -> AsyncSchedulesResourceWithRawResponse:
        return AsyncSchedulesResourceWithRawResponse(self._agents.schedules)

    @cached_property
    def deployments(self) -> AsyncDeploymentsResourceWithRawResponse:
        return AsyncDeploymentsResourceWithRawResponse(self._agents.deployments)

    @cached_property
    def environments(self) -> AsyncEnvironmentsResourceWithRawResponse:
        return AsyncEnvironmentsResourceWithRawResponse(self._agents.environments)

    @cached_property
    def secrets(self) -> AsyncSecretsResourceWithRawResponse:
        return AsyncSecretsResourceWithRawResponse(self._agents.secrets)


class AgentsResourceWithStreamingResponse:
    def __init__(self, agents: AgentsResource) -> None:
        self._agents = agents

        self.retrieve = to_streamed_response_wrapper(
            agents.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            agents.list,
        )
        self.delete = to_streamed_response_wrapper(
            agents.delete,
        )
        self.delete_by_name = to_streamed_response_wrapper(
            agents.delete_by_name,
        )
        self.deploy = to_streamed_response_wrapper(
            agents.deploy,
        )
        self.handle_rpc = to_streamed_response_wrapper(
            agents.handle_rpc,
        )
        self.retrieve_by_name = to_streamed_response_wrapper(
            agents.retrieve_by_name,
        )
        self.rpc = to_streamed_response_wrapper(
            agents.rpc,
        )
        self.rpc_by_name = to_streamed_response_wrapper(
            agents.rpc_by_name,
        )

    @cached_property
    def name(self) -> NameResourceWithStreamingResponse:
        return NameResourceWithStreamingResponse(self._agents.name)

    @cached_property
    def forward(self) -> ForwardResourceWithStreamingResponse:
        return ForwardResourceWithStreamingResponse(self._agents.forward)

    @cached_property
    def schedules(self) -> SchedulesResourceWithStreamingResponse:
        return SchedulesResourceWithStreamingResponse(self._agents.schedules)

    @cached_property
    def deployments(self) -> DeploymentsResourceWithStreamingResponse:
        return DeploymentsResourceWithStreamingResponse(self._agents.deployments)

    @cached_property
    def environments(self) -> EnvironmentsResourceWithStreamingResponse:
        return EnvironmentsResourceWithStreamingResponse(self._agents.environments)

    @cached_property
    def secrets(self) -> SecretsResourceWithStreamingResponse:
        return SecretsResourceWithStreamingResponse(self._agents.secrets)


class AsyncAgentsResourceWithStreamingResponse:
    def __init__(self, agents: AsyncAgentsResource) -> None:
        self._agents = agents

        self.retrieve = async_to_streamed_response_wrapper(
            agents.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            agents.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            agents.delete,
        )
        self.delete_by_name = async_to_streamed_response_wrapper(
            agents.delete_by_name,
        )
        self.deploy = async_to_streamed_response_wrapper(
            agents.deploy,
        )
        self.handle_rpc = async_to_streamed_response_wrapper(
            agents.handle_rpc,
        )
        self.retrieve_by_name = async_to_streamed_response_wrapper(
            agents.retrieve_by_name,
        )
        self.rpc = async_to_streamed_response_wrapper(
            agents.rpc,
        )
        self.rpc_by_name = async_to_streamed_response_wrapper(
            agents.rpc_by_name,
        )

    @cached_property
    def name(self) -> AsyncNameResourceWithStreamingResponse:
        return AsyncNameResourceWithStreamingResponse(self._agents.name)

    @cached_property
    def forward(self) -> AsyncForwardResourceWithStreamingResponse:
        return AsyncForwardResourceWithStreamingResponse(self._agents.forward)

    @cached_property
    def schedules(self) -> AsyncSchedulesResourceWithStreamingResponse:
        return AsyncSchedulesResourceWithStreamingResponse(self._agents.schedules)

    @cached_property
    def deployments(self) -> AsyncDeploymentsResourceWithStreamingResponse:
        return AsyncDeploymentsResourceWithStreamingResponse(self._agents.deployments)

    @cached_property
    def environments(self) -> AsyncEnvironmentsResourceWithStreamingResponse:
        return AsyncEnvironmentsResourceWithStreamingResponse(self._agents.environments)

    @cached_property
    def secrets(self) -> AsyncSecretsResourceWithStreamingResponse:
        return AsyncSecretsResourceWithStreamingResponse(self._agents.secrets)
