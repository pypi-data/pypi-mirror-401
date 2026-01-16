# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sb0 import Sb0, AsyncSb0
from sb0.types import Agent, DeleteResponse, AgentRpcResponse
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestName:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Sb0) -> None:
        name = client.agents.name.retrieve(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
        )
        assert_matches_type(Agent, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Sb0) -> None:
        response = client.agents.name.with_raw_response.retrieve(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        name = response.parse()
        assert_matches_type(Agent, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Sb0) -> None:
        with client.agents.name.with_streaming_response.retrieve(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            name = response.parse()
            assert_matches_type(Agent, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            client.agents.name.with_raw_response.retrieve(
                agent_name="agent_name",
                namespace_slug="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            client.agents.name.with_raw_response.retrieve(
                agent_name="",
                namespace_slug="namespace_slug",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_delete(self, client: Sb0) -> None:
        name = client.agents.name.delete(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
        )
        assert_matches_type(DeleteResponse, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_delete(self, client: Sb0) -> None:
        response = client.agents.name.with_raw_response.delete(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        name = response.parse()
        assert_matches_type(DeleteResponse, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_delete(self, client: Sb0) -> None:
        with client.agents.name.with_streaming_response.delete(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            name = response.parse()
            assert_matches_type(DeleteResponse, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_delete(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            client.agents.name.with_raw_response.delete(
                agent_name="agent_name",
                namespace_slug="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            client.agents.name.with_raw_response.delete(
                agent_name="",
                namespace_slug="namespace_slug",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_handle_rpc(self, client: Sb0) -> None:
        name = client.agents.name.handle_rpc(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
            namespace_id="namespace_id",
            method="event/send",
            params={},
        )
        assert_matches_type(AgentRpcResponse, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_handle_rpc_with_all_params(self, client: Sb0) -> None:
        name = client.agents.name.handle_rpc(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
            namespace_id="namespace_id",
            method="event/send",
            params={
                "name": "name",
                "params": {"foo": "bar"},
                "workspace_id": "workspace_id",
            },
            id=0,
            jsonrpc="2.0",
        )
        assert_matches_type(AgentRpcResponse, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_handle_rpc(self, client: Sb0) -> None:
        response = client.agents.name.with_raw_response.handle_rpc(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
            namespace_id="namespace_id",
            method="event/send",
            params={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        name = response.parse()
        assert_matches_type(AgentRpcResponse, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_handle_rpc(self, client: Sb0) -> None:
        with client.agents.name.with_streaming_response.handle_rpc(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
            namespace_id="namespace_id",
            method="event/send",
            params={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            name = response.parse()
            assert_matches_type(AgentRpcResponse, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_handle_rpc(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            client.agents.name.with_raw_response.handle_rpc(
                agent_name="agent_name",
                namespace_slug="",
                namespace_id="namespace_id",
                method="event/send",
                params={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            client.agents.name.with_raw_response.handle_rpc(
                agent_name="",
                namespace_slug="namespace_slug",
                namespace_id="namespace_id",
                method="event/send",
                params={},
            )


class TestAsyncName:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSb0) -> None:
        name = await async_client.agents.name.retrieve(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
        )
        assert_matches_type(Agent, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSb0) -> None:
        response = await async_client.agents.name.with_raw_response.retrieve(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        name = await response.parse()
        assert_matches_type(Agent, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSb0) -> None:
        async with async_client.agents.name.with_streaming_response.retrieve(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            name = await response.parse()
            assert_matches_type(Agent, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            await async_client.agents.name.with_raw_response.retrieve(
                agent_name="agent_name",
                namespace_slug="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            await async_client.agents.name.with_raw_response.retrieve(
                agent_name="",
                namespace_slug="namespace_slug",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_delete(self, async_client: AsyncSb0) -> None:
        name = await async_client.agents.name.delete(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
        )
        assert_matches_type(DeleteResponse, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSb0) -> None:
        response = await async_client.agents.name.with_raw_response.delete(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        name = await response.parse()
        assert_matches_type(DeleteResponse, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSb0) -> None:
        async with async_client.agents.name.with_streaming_response.delete(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            name = await response.parse()
            assert_matches_type(DeleteResponse, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            await async_client.agents.name.with_raw_response.delete(
                agent_name="agent_name",
                namespace_slug="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            await async_client.agents.name.with_raw_response.delete(
                agent_name="",
                namespace_slug="namespace_slug",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_handle_rpc(self, async_client: AsyncSb0) -> None:
        name = await async_client.agents.name.handle_rpc(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
            namespace_id="namespace_id",
            method="event/send",
            params={},
        )
        assert_matches_type(AgentRpcResponse, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_handle_rpc_with_all_params(self, async_client: AsyncSb0) -> None:
        name = await async_client.agents.name.handle_rpc(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
            namespace_id="namespace_id",
            method="event/send",
            params={
                "name": "name",
                "params": {"foo": "bar"},
                "workspace_id": "workspace_id",
            },
            id=0,
            jsonrpc="2.0",
        )
        assert_matches_type(AgentRpcResponse, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_handle_rpc(self, async_client: AsyncSb0) -> None:
        response = await async_client.agents.name.with_raw_response.handle_rpc(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
            namespace_id="namespace_id",
            method="event/send",
            params={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        name = await response.parse()
        assert_matches_type(AgentRpcResponse, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_handle_rpc(self, async_client: AsyncSb0) -> None:
        async with async_client.agents.name.with_streaming_response.handle_rpc(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
            namespace_id="namespace_id",
            method="event/send",
            params={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            name = await response.parse()
            assert_matches_type(AgentRpcResponse, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_handle_rpc(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            await async_client.agents.name.with_raw_response.handle_rpc(
                agent_name="agent_name",
                namespace_slug="",
                namespace_id="namespace_id",
                method="event/send",
                params={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            await async_client.agents.name.with_raw_response.handle_rpc(
                agent_name="",
                namespace_slug="namespace_slug",
                namespace_id="namespace_id",
                method="event/send",
                params={},
            )
