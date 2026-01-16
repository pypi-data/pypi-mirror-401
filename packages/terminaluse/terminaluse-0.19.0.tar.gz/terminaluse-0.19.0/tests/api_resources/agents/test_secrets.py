# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sb0 import Sb0, AsyncSb0
from tests.utils import assert_matches_type
from sb0.types.agents import CrossEnvSecretsListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSecrets:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Sb0) -> None:
        secret = client.agents.secrets.list(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
        )
        assert_matches_type(CrossEnvSecretsListResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Sb0) -> None:
        secret = client.agents.secrets.list(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
            include_values=True,
        )
        assert_matches_type(CrossEnvSecretsListResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Sb0) -> None:
        response = client.agents.secrets.with_raw_response.list(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = response.parse()
        assert_matches_type(CrossEnvSecretsListResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Sb0) -> None:
        with client.agents.secrets.with_streaming_response.list(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = response.parse()
            assert_matches_type(CrossEnvSecretsListResponse, secret, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_list(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            client.agents.secrets.with_raw_response.list(
                agent_name="agent_name",
                namespace_slug="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            client.agents.secrets.with_raw_response.list(
                agent_name="",
                namespace_slug="namespace_slug",
            )


class TestAsyncSecrets:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncSb0) -> None:
        secret = await async_client.agents.secrets.list(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
        )
        assert_matches_type(CrossEnvSecretsListResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSb0) -> None:
        secret = await async_client.agents.secrets.list(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
            include_values=True,
        )
        assert_matches_type(CrossEnvSecretsListResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSb0) -> None:
        response = await async_client.agents.secrets.with_raw_response.list(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = await response.parse()
        assert_matches_type(CrossEnvSecretsListResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSb0) -> None:
        async with async_client.agents.secrets.with_streaming_response.list(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = await response.parse()
            assert_matches_type(CrossEnvSecretsListResponse, secret, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_list(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            await async_client.agents.secrets.with_raw_response.list(
                agent_name="agent_name",
                namespace_slug="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            await async_client.agents.secrets.with_raw_response.list(
                agent_name="",
                namespace_slug="namespace_slug",
            )
