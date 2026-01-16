# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sb0 import Sb0, AsyncSb0
from sb0.types import AgentAPIKey
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestName:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Sb0) -> None:
        name = client.agent_api_keys.name.retrieve(
            name="name",
        )
        assert_matches_type(AgentAPIKey, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Sb0) -> None:
        name = client.agent_api_keys.name.retrieve(
            name="name",
            agent_id="agent_id",
            agent_name="agent_name",
            api_key_type="internal",
        )
        assert_matches_type(AgentAPIKey, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Sb0) -> None:
        response = client.agent_api_keys.name.with_raw_response.retrieve(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        name = response.parse()
        assert_matches_type(AgentAPIKey, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Sb0) -> None:
        with client.agent_api_keys.name.with_streaming_response.retrieve(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            name = response.parse()
            assert_matches_type(AgentAPIKey, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `name` but received ''"):
            client.agent_api_keys.name.with_raw_response.retrieve(
                name="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_delete(self, client: Sb0) -> None:
        name = client.agent_api_keys.name.delete(
            api_key_name="api_key_name",
        )
        assert_matches_type(str, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_delete_with_all_params(self, client: Sb0) -> None:
        name = client.agent_api_keys.name.delete(
            api_key_name="api_key_name",
            agent_id="agent_id",
            agent_name="agent_name",
            api_key_type="internal",
        )
        assert_matches_type(str, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_delete(self, client: Sb0) -> None:
        response = client.agent_api_keys.name.with_raw_response.delete(
            api_key_name="api_key_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        name = response.parse()
        assert_matches_type(str, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_delete(self, client: Sb0) -> None:
        with client.agent_api_keys.name.with_streaming_response.delete(
            api_key_name="api_key_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            name = response.parse()
            assert_matches_type(str, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_delete(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `api_key_name` but received ''"):
            client.agent_api_keys.name.with_raw_response.delete(
                api_key_name="",
            )


class TestAsyncName:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSb0) -> None:
        name = await async_client.agent_api_keys.name.retrieve(
            name="name",
        )
        assert_matches_type(AgentAPIKey, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSb0) -> None:
        name = await async_client.agent_api_keys.name.retrieve(
            name="name",
            agent_id="agent_id",
            agent_name="agent_name",
            api_key_type="internal",
        )
        assert_matches_type(AgentAPIKey, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSb0) -> None:
        response = await async_client.agent_api_keys.name.with_raw_response.retrieve(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        name = await response.parse()
        assert_matches_type(AgentAPIKey, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSb0) -> None:
        async with async_client.agent_api_keys.name.with_streaming_response.retrieve(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            name = await response.parse()
            assert_matches_type(AgentAPIKey, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `name` but received ''"):
            await async_client.agent_api_keys.name.with_raw_response.retrieve(
                name="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_delete(self, async_client: AsyncSb0) -> None:
        name = await async_client.agent_api_keys.name.delete(
            api_key_name="api_key_name",
        )
        assert_matches_type(str, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncSb0) -> None:
        name = await async_client.agent_api_keys.name.delete(
            api_key_name="api_key_name",
            agent_id="agent_id",
            agent_name="agent_name",
            api_key_type="internal",
        )
        assert_matches_type(str, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSb0) -> None:
        response = await async_client.agent_api_keys.name.with_raw_response.delete(
            api_key_name="api_key_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        name = await response.parse()
        assert_matches_type(str, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSb0) -> None:
        async with async_client.agent_api_keys.name.with_streaming_response.delete(
            api_key_name="api_key_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            name = await response.parse()
            assert_matches_type(str, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `api_key_name` but received ''"):
            await async_client.agent_api_keys.name.with_raw_response.delete(
                api_key_name="",
            )
