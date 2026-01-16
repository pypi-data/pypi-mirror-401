# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sb0 import Sb0, AsyncSb0
from sb0.types import (
    Task,
    TaskResponse,
    DeleteResponse,
    TaskListResponse,
)
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTasks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Sb0) -> None:
        task = client.tasks.retrieve(
            task_id="task_id",
        )
        assert_matches_type(TaskResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Sb0) -> None:
        task = client.tasks.retrieve(
            task_id="task_id",
            relationships=["agents"],
        )
        assert_matches_type(TaskResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Sb0) -> None:
        response = client.tasks.with_raw_response.retrieve(
            task_id="task_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = response.parse()
        assert_matches_type(TaskResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Sb0) -> None:
        with client.tasks.with_streaming_response.retrieve(
            task_id="task_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = response.parse()
            assert_matches_type(TaskResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            client.tasks.with_raw_response.retrieve(
                task_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_update(self, client: Sb0) -> None:
        task = client.tasks.update(
            task_id="task_id",
        )
        assert_matches_type(Task, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_update_with_all_params(self, client: Sb0) -> None:
        task = client.tasks.update(
            task_id="task_id",
            task_metadata={"foo": "bar"},
        )
        assert_matches_type(Task, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_update(self, client: Sb0) -> None:
        response = client.tasks.with_raw_response.update(
            task_id="task_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = response.parse()
        assert_matches_type(Task, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_update(self, client: Sb0) -> None:
        with client.tasks.with_streaming_response.update(
            task_id="task_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = response.parse()
            assert_matches_type(Task, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_update(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            client.tasks.with_raw_response.update(
                task_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Sb0) -> None:
        task = client.tasks.list()
        assert_matches_type(TaskListResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Sb0) -> None:
        task = client.tasks.list(
            agent_id="agent_id",
            agent_name="agent_name",
            limit=0,
            order_by="order_by",
            order_direction="order_direction",
            page_number=0,
            relationships=["agents"],
        )
        assert_matches_type(TaskListResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Sb0) -> None:
        response = client.tasks.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = response.parse()
        assert_matches_type(TaskListResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Sb0) -> None:
        with client.tasks.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = response.parse()
            assert_matches_type(TaskListResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_delete(self, client: Sb0) -> None:
        task = client.tasks.delete(
            "task_id",
        )
        assert_matches_type(DeleteResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_delete(self, client: Sb0) -> None:
        response = client.tasks.with_raw_response.delete(
            "task_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = response.parse()
        assert_matches_type(DeleteResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_delete(self, client: Sb0) -> None:
        with client.tasks.with_streaming_response.delete(
            "task_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = response.parse()
            assert_matches_type(DeleteResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_delete(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            client.tasks.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_delete_by_name(self, client: Sb0) -> None:
        task = client.tasks.delete_by_name(
            "task_name",
        )
        assert_matches_type(DeleteResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_delete_by_name(self, client: Sb0) -> None:
        response = client.tasks.with_raw_response.delete_by_name(
            "task_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = response.parse()
        assert_matches_type(DeleteResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_delete_by_name(self, client: Sb0) -> None:
        with client.tasks.with_streaming_response.delete_by_name(
            "task_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = response.parse()
            assert_matches_type(DeleteResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_delete_by_name(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_name` but received ''"):
            client.tasks.with_raw_response.delete_by_name(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve_by_name(self, client: Sb0) -> None:
        task = client.tasks.retrieve_by_name(
            task_name="task_name",
        )
        assert_matches_type(TaskResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve_by_name_with_all_params(self, client: Sb0) -> None:
        task = client.tasks.retrieve_by_name(
            task_name="task_name",
            relationships=["agents"],
        )
        assert_matches_type(TaskResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve_by_name(self, client: Sb0) -> None:
        response = client.tasks.with_raw_response.retrieve_by_name(
            task_name="task_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = response.parse()
        assert_matches_type(TaskResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve_by_name(self, client: Sb0) -> None:
        with client.tasks.with_streaming_response.retrieve_by_name(
            task_name="task_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = response.parse()
            assert_matches_type(TaskResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve_by_name(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_name` but received ''"):
            client.tasks.with_raw_response.retrieve_by_name(
                task_name="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_stream_events(self, client: Sb0) -> None:
        task = client.tasks.stream_events(
            "task_id",
        )
        assert_matches_type(object, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_stream_events(self, client: Sb0) -> None:
        response = client.tasks.with_raw_response.stream_events(
            "task_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = response.parse()
        assert_matches_type(object, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_stream_events(self, client: Sb0) -> None:
        with client.tasks.with_streaming_response.stream_events(
            "task_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = response.parse()
            assert_matches_type(object, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_stream_events(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            client.tasks.with_raw_response.stream_events(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_stream_events_by_name(self, client: Sb0) -> None:
        task = client.tasks.stream_events_by_name(
            "task_name",
        )
        assert_matches_type(object, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_stream_events_by_name(self, client: Sb0) -> None:
        response = client.tasks.with_raw_response.stream_events_by_name(
            "task_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = response.parse()
        assert_matches_type(object, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_stream_events_by_name(self, client: Sb0) -> None:
        with client.tasks.with_streaming_response.stream_events_by_name(
            "task_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = response.parse()
            assert_matches_type(object, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_stream_events_by_name(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_name` but received ''"):
            client.tasks.with_raw_response.stream_events_by_name(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_update_by_name(self, client: Sb0) -> None:
        task = client.tasks.update_by_name(
            task_name="task_name",
        )
        assert_matches_type(Task, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_update_by_name_with_all_params(self, client: Sb0) -> None:
        task = client.tasks.update_by_name(
            task_name="task_name",
            task_metadata={"foo": "bar"},
        )
        assert_matches_type(Task, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_update_by_name(self, client: Sb0) -> None:
        response = client.tasks.with_raw_response.update_by_name(
            task_name="task_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = response.parse()
        assert_matches_type(Task, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_update_by_name(self, client: Sb0) -> None:
        with client.tasks.with_streaming_response.update_by_name(
            task_name="task_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = response.parse()
            assert_matches_type(Task, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_update_by_name(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_name` but received ''"):
            client.tasks.with_raw_response.update_by_name(
                task_name="",
            )


class TestAsyncTasks:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSb0) -> None:
        task = await async_client.tasks.retrieve(
            task_id="task_id",
        )
        assert_matches_type(TaskResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSb0) -> None:
        task = await async_client.tasks.retrieve(
            task_id="task_id",
            relationships=["agents"],
        )
        assert_matches_type(TaskResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSb0) -> None:
        response = await async_client.tasks.with_raw_response.retrieve(
            task_id="task_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = await response.parse()
        assert_matches_type(TaskResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSb0) -> None:
        async with async_client.tasks.with_streaming_response.retrieve(
            task_id="task_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = await response.parse()
            assert_matches_type(TaskResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            await async_client.tasks.with_raw_response.retrieve(
                task_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_update(self, async_client: AsyncSb0) -> None:
        task = await async_client.tasks.update(
            task_id="task_id",
        )
        assert_matches_type(Task, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSb0) -> None:
        task = await async_client.tasks.update(
            task_id="task_id",
            task_metadata={"foo": "bar"},
        )
        assert_matches_type(Task, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSb0) -> None:
        response = await async_client.tasks.with_raw_response.update(
            task_id="task_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = await response.parse()
        assert_matches_type(Task, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSb0) -> None:
        async with async_client.tasks.with_streaming_response.update(
            task_id="task_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = await response.parse()
            assert_matches_type(Task, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_update(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            await async_client.tasks.with_raw_response.update(
                task_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncSb0) -> None:
        task = await async_client.tasks.list()
        assert_matches_type(TaskListResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSb0) -> None:
        task = await async_client.tasks.list(
            agent_id="agent_id",
            agent_name="agent_name",
            limit=0,
            order_by="order_by",
            order_direction="order_direction",
            page_number=0,
            relationships=["agents"],
        )
        assert_matches_type(TaskListResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSb0) -> None:
        response = await async_client.tasks.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = await response.parse()
        assert_matches_type(TaskListResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSb0) -> None:
        async with async_client.tasks.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = await response.parse()
            assert_matches_type(TaskListResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_delete(self, async_client: AsyncSb0) -> None:
        task = await async_client.tasks.delete(
            "task_id",
        )
        assert_matches_type(DeleteResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSb0) -> None:
        response = await async_client.tasks.with_raw_response.delete(
            "task_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = await response.parse()
        assert_matches_type(DeleteResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSb0) -> None:
        async with async_client.tasks.with_streaming_response.delete(
            "task_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = await response.parse()
            assert_matches_type(DeleteResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            await async_client.tasks.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_delete_by_name(self, async_client: AsyncSb0) -> None:
        task = await async_client.tasks.delete_by_name(
            "task_name",
        )
        assert_matches_type(DeleteResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_delete_by_name(self, async_client: AsyncSb0) -> None:
        response = await async_client.tasks.with_raw_response.delete_by_name(
            "task_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = await response.parse()
        assert_matches_type(DeleteResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_delete_by_name(self, async_client: AsyncSb0) -> None:
        async with async_client.tasks.with_streaming_response.delete_by_name(
            "task_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = await response.parse()
            assert_matches_type(DeleteResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_delete_by_name(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_name` but received ''"):
            await async_client.tasks.with_raw_response.delete_by_name(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve_by_name(self, async_client: AsyncSb0) -> None:
        task = await async_client.tasks.retrieve_by_name(
            task_name="task_name",
        )
        assert_matches_type(TaskResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve_by_name_with_all_params(self, async_client: AsyncSb0) -> None:
        task = await async_client.tasks.retrieve_by_name(
            task_name="task_name",
            relationships=["agents"],
        )
        assert_matches_type(TaskResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve_by_name(self, async_client: AsyncSb0) -> None:
        response = await async_client.tasks.with_raw_response.retrieve_by_name(
            task_name="task_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = await response.parse()
        assert_matches_type(TaskResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve_by_name(self, async_client: AsyncSb0) -> None:
        async with async_client.tasks.with_streaming_response.retrieve_by_name(
            task_name="task_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = await response.parse()
            assert_matches_type(TaskResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve_by_name(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_name` but received ''"):
            await async_client.tasks.with_raw_response.retrieve_by_name(
                task_name="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_stream_events(self, async_client: AsyncSb0) -> None:
        task = await async_client.tasks.stream_events(
            "task_id",
        )
        assert_matches_type(object, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_stream_events(self, async_client: AsyncSb0) -> None:
        response = await async_client.tasks.with_raw_response.stream_events(
            "task_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = await response.parse()
        assert_matches_type(object, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_stream_events(self, async_client: AsyncSb0) -> None:
        async with async_client.tasks.with_streaming_response.stream_events(
            "task_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = await response.parse()
            assert_matches_type(object, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_stream_events(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            await async_client.tasks.with_raw_response.stream_events(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_stream_events_by_name(self, async_client: AsyncSb0) -> None:
        task = await async_client.tasks.stream_events_by_name(
            "task_name",
        )
        assert_matches_type(object, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_stream_events_by_name(self, async_client: AsyncSb0) -> None:
        response = await async_client.tasks.with_raw_response.stream_events_by_name(
            "task_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = await response.parse()
        assert_matches_type(object, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_stream_events_by_name(self, async_client: AsyncSb0) -> None:
        async with async_client.tasks.with_streaming_response.stream_events_by_name(
            "task_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = await response.parse()
            assert_matches_type(object, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_stream_events_by_name(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_name` but received ''"):
            await async_client.tasks.with_raw_response.stream_events_by_name(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_update_by_name(self, async_client: AsyncSb0) -> None:
        task = await async_client.tasks.update_by_name(
            task_name="task_name",
        )
        assert_matches_type(Task, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_update_by_name_with_all_params(self, async_client: AsyncSb0) -> None:
        task = await async_client.tasks.update_by_name(
            task_name="task_name",
            task_metadata={"foo": "bar"},
        )
        assert_matches_type(Task, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_update_by_name(self, async_client: AsyncSb0) -> None:
        response = await async_client.tasks.with_raw_response.update_by_name(
            task_name="task_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = await response.parse()
        assert_matches_type(Task, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_update_by_name(self, async_client: AsyncSb0) -> None:
        async with async_client.tasks.with_streaming_response.update_by_name(
            task_name="task_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = await response.parse()
            assert_matches_type(Task, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_update_by_name(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_name` but received ''"):
            await async_client.tasks.with_raw_response.update_by_name(
                task_name="",
            )
