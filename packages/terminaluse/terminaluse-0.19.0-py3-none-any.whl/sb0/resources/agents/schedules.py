# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Optional
from datetime import datetime

import httpx

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
from ...types.agents import schedule_list_params, schedule_pause_params, schedule_create_params, schedule_unpause_params
from ...types.delete_response import DeleteResponse
from ...types.agents.schedule_response import ScheduleResponse
from ...types.agents.schedule_list_response import ScheduleListResponse

__all__ = ["SchedulesResource", "AsyncSchedulesResource"]


class SchedulesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SchedulesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return SchedulesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SchedulesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return SchedulesResourceWithStreamingResponse(self)

    def create(
        self,
        agent_id: str,
        *,
        name: str,
        task_queue: str,
        workflow_name: str,
        cron_expression: Optional[str] | Omit = omit,
        end_at: Union[str, datetime, None] | Omit = omit,
        execution_timeout_seconds: Optional[int] | Omit = omit,
        interval_seconds: Optional[int] | Omit = omit,
        paused: bool | Omit = omit,
        start_at: Union[str, datetime, None] | Omit = omit,
        workflow_params: Optional[Dict[str, object]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ScheduleResponse:
        """
        Create a new schedule for recurring workflow execution for an agent.

        Args:
          name: Human-readable name for the schedule (e.g., 'weekly-profiling'). Will be
              combined with agent_id to form the full schedule_id.

          task_queue: Temporal task queue where the agent's worker is listening

          workflow_name: Name of the Temporal workflow to execute (e.g., 'sae-orchestrator')

          cron_expression: Cron expression for scheduling (e.g., '0 0 \\** \\** 0' for weekly on Sunday)

          end_at: When the schedule should stop being active

          execution_timeout_seconds: Maximum time in seconds for each workflow execution

          interval_seconds: Alternative to cron - run every N seconds

          paused: Whether to create the schedule in a paused state

          start_at: When the schedule should start being active

          workflow_params: Parameters to pass to the workflow

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        return self._post(
            f"/agents/{agent_id}/schedules",
            body=maybe_transform(
                {
                    "name": name,
                    "task_queue": task_queue,
                    "workflow_name": workflow_name,
                    "cron_expression": cron_expression,
                    "end_at": end_at,
                    "execution_timeout_seconds": execution_timeout_seconds,
                    "interval_seconds": interval_seconds,
                    "paused": paused,
                    "start_at": start_at,
                    "workflow_params": workflow_params,
                },
                schedule_create_params.ScheduleCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScheduleResponse,
        )

    def retrieve(
        self,
        schedule_name: str,
        *,
        agent_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ScheduleResponse:
        """
        Get details of a schedule by its name.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        if not schedule_name:
            raise ValueError(f"Expected a non-empty value for `schedule_name` but received {schedule_name!r}")
        return self._get(
            f"/agents/{agent_id}/schedules/{schedule_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScheduleResponse,
        )

    def list(
        self,
        agent_id: str,
        *,
        page_size: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ScheduleListResponse:
        """
        List all schedules for an agent.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        return self._get(
            f"/agents/{agent_id}/schedules",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"page_size": page_size}, schedule_list_params.ScheduleListParams),
            ),
            cast_to=ScheduleListResponse,
        )

    def delete(
        self,
        schedule_name: str,
        *,
        agent_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeleteResponse:
        """
        Delete a schedule permanently.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        if not schedule_name:
            raise ValueError(f"Expected a non-empty value for `schedule_name` but received {schedule_name!r}")
        return self._delete(
            f"/agents/{agent_id}/schedules/{schedule_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteResponse,
        )

    def pause(
        self,
        schedule_name: str,
        *,
        agent_id: str,
        note: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ScheduleResponse:
        """
        Pause a schedule to stop it from executing.

        Args:
          note: Optional note explaining why the schedule was paused

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        if not schedule_name:
            raise ValueError(f"Expected a non-empty value for `schedule_name` but received {schedule_name!r}")
        return self._post(
            f"/agents/{agent_id}/schedules/{schedule_name}/pause",
            body=maybe_transform({"note": note}, schedule_pause_params.SchedulePauseParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScheduleResponse,
        )

    def trigger(
        self,
        schedule_name: str,
        *,
        agent_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ScheduleResponse:
        """
        Trigger a schedule to run immediately, regardless of its regular schedule.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        if not schedule_name:
            raise ValueError(f"Expected a non-empty value for `schedule_name` but received {schedule_name!r}")
        return self._post(
            f"/agents/{agent_id}/schedules/{schedule_name}/trigger",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScheduleResponse,
        )

    def unpause(
        self,
        schedule_name: str,
        *,
        agent_id: str,
        note: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ScheduleResponse:
        """
        Unpause/resume a schedule to allow it to execute again.

        Args:
          note: Optional note explaining why the schedule was unpaused

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        if not schedule_name:
            raise ValueError(f"Expected a non-empty value for `schedule_name` but received {schedule_name!r}")
        return self._post(
            f"/agents/{agent_id}/schedules/{schedule_name}/unpause",
            body=maybe_transform({"note": note}, schedule_unpause_params.ScheduleUnpauseParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScheduleResponse,
        )


class AsyncSchedulesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSchedulesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncSchedulesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSchedulesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return AsyncSchedulesResourceWithStreamingResponse(self)

    async def create(
        self,
        agent_id: str,
        *,
        name: str,
        task_queue: str,
        workflow_name: str,
        cron_expression: Optional[str] | Omit = omit,
        end_at: Union[str, datetime, None] | Omit = omit,
        execution_timeout_seconds: Optional[int] | Omit = omit,
        interval_seconds: Optional[int] | Omit = omit,
        paused: bool | Omit = omit,
        start_at: Union[str, datetime, None] | Omit = omit,
        workflow_params: Optional[Dict[str, object]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ScheduleResponse:
        """
        Create a new schedule for recurring workflow execution for an agent.

        Args:
          name: Human-readable name for the schedule (e.g., 'weekly-profiling'). Will be
              combined with agent_id to form the full schedule_id.

          task_queue: Temporal task queue where the agent's worker is listening

          workflow_name: Name of the Temporal workflow to execute (e.g., 'sae-orchestrator')

          cron_expression: Cron expression for scheduling (e.g., '0 0 \\** \\** 0' for weekly on Sunday)

          end_at: When the schedule should stop being active

          execution_timeout_seconds: Maximum time in seconds for each workflow execution

          interval_seconds: Alternative to cron - run every N seconds

          paused: Whether to create the schedule in a paused state

          start_at: When the schedule should start being active

          workflow_params: Parameters to pass to the workflow

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        return await self._post(
            f"/agents/{agent_id}/schedules",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "task_queue": task_queue,
                    "workflow_name": workflow_name,
                    "cron_expression": cron_expression,
                    "end_at": end_at,
                    "execution_timeout_seconds": execution_timeout_seconds,
                    "interval_seconds": interval_seconds,
                    "paused": paused,
                    "start_at": start_at,
                    "workflow_params": workflow_params,
                },
                schedule_create_params.ScheduleCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScheduleResponse,
        )

    async def retrieve(
        self,
        schedule_name: str,
        *,
        agent_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ScheduleResponse:
        """
        Get details of a schedule by its name.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        if not schedule_name:
            raise ValueError(f"Expected a non-empty value for `schedule_name` but received {schedule_name!r}")
        return await self._get(
            f"/agents/{agent_id}/schedules/{schedule_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScheduleResponse,
        )

    async def list(
        self,
        agent_id: str,
        *,
        page_size: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ScheduleListResponse:
        """
        List all schedules for an agent.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        return await self._get(
            f"/agents/{agent_id}/schedules",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"page_size": page_size}, schedule_list_params.ScheduleListParams),
            ),
            cast_to=ScheduleListResponse,
        )

    async def delete(
        self,
        schedule_name: str,
        *,
        agent_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeleteResponse:
        """
        Delete a schedule permanently.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        if not schedule_name:
            raise ValueError(f"Expected a non-empty value for `schedule_name` but received {schedule_name!r}")
        return await self._delete(
            f"/agents/{agent_id}/schedules/{schedule_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteResponse,
        )

    async def pause(
        self,
        schedule_name: str,
        *,
        agent_id: str,
        note: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ScheduleResponse:
        """
        Pause a schedule to stop it from executing.

        Args:
          note: Optional note explaining why the schedule was paused

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        if not schedule_name:
            raise ValueError(f"Expected a non-empty value for `schedule_name` but received {schedule_name!r}")
        return await self._post(
            f"/agents/{agent_id}/schedules/{schedule_name}/pause",
            body=await async_maybe_transform({"note": note}, schedule_pause_params.SchedulePauseParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScheduleResponse,
        )

    async def trigger(
        self,
        schedule_name: str,
        *,
        agent_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ScheduleResponse:
        """
        Trigger a schedule to run immediately, regardless of its regular schedule.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        if not schedule_name:
            raise ValueError(f"Expected a non-empty value for `schedule_name` but received {schedule_name!r}")
        return await self._post(
            f"/agents/{agent_id}/schedules/{schedule_name}/trigger",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScheduleResponse,
        )

    async def unpause(
        self,
        schedule_name: str,
        *,
        agent_id: str,
        note: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ScheduleResponse:
        """
        Unpause/resume a schedule to allow it to execute again.

        Args:
          note: Optional note explaining why the schedule was unpaused

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        if not schedule_name:
            raise ValueError(f"Expected a non-empty value for `schedule_name` but received {schedule_name!r}")
        return await self._post(
            f"/agents/{agent_id}/schedules/{schedule_name}/unpause",
            body=await async_maybe_transform({"note": note}, schedule_unpause_params.ScheduleUnpauseParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScheduleResponse,
        )


class SchedulesResourceWithRawResponse:
    def __init__(self, schedules: SchedulesResource) -> None:
        self._schedules = schedules

        self.create = to_raw_response_wrapper(
            schedules.create,
        )
        self.retrieve = to_raw_response_wrapper(
            schedules.retrieve,
        )
        self.list = to_raw_response_wrapper(
            schedules.list,
        )
        self.delete = to_raw_response_wrapper(
            schedules.delete,
        )
        self.pause = to_raw_response_wrapper(
            schedules.pause,
        )
        self.trigger = to_raw_response_wrapper(
            schedules.trigger,
        )
        self.unpause = to_raw_response_wrapper(
            schedules.unpause,
        )


class AsyncSchedulesResourceWithRawResponse:
    def __init__(self, schedules: AsyncSchedulesResource) -> None:
        self._schedules = schedules

        self.create = async_to_raw_response_wrapper(
            schedules.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            schedules.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            schedules.list,
        )
        self.delete = async_to_raw_response_wrapper(
            schedules.delete,
        )
        self.pause = async_to_raw_response_wrapper(
            schedules.pause,
        )
        self.trigger = async_to_raw_response_wrapper(
            schedules.trigger,
        )
        self.unpause = async_to_raw_response_wrapper(
            schedules.unpause,
        )


class SchedulesResourceWithStreamingResponse:
    def __init__(self, schedules: SchedulesResource) -> None:
        self._schedules = schedules

        self.create = to_streamed_response_wrapper(
            schedules.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            schedules.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            schedules.list,
        )
        self.delete = to_streamed_response_wrapper(
            schedules.delete,
        )
        self.pause = to_streamed_response_wrapper(
            schedules.pause,
        )
        self.trigger = to_streamed_response_wrapper(
            schedules.trigger,
        )
        self.unpause = to_streamed_response_wrapper(
            schedules.unpause,
        )


class AsyncSchedulesResourceWithStreamingResponse:
    def __init__(self, schedules: AsyncSchedulesResource) -> None:
        self._schedules = schedules

        self.create = async_to_streamed_response_wrapper(
            schedules.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            schedules.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            schedules.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            schedules.delete,
        )
        self.pause = async_to_streamed_response_wrapper(
            schedules.pause,
        )
        self.trigger = async_to_streamed_response_wrapper(
            schedules.trigger,
        )
        self.unpause = async_to_streamed_response_wrapper(
            schedules.unpause,
        )
