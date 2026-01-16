# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sb0 import Sb0, AsyncSb0
from sb0.types import RegistryAuthResponse
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRegistry:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_auth(self, client: Sb0) -> None:
        registry = client.registry.auth(
            namespace="acme",
        )
        assert_matches_type(RegistryAuthResponse, registry, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_auth(self, client: Sb0) -> None:
        response = client.registry.with_raw_response.auth(
            namespace="acme",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        registry = response.parse()
        assert_matches_type(RegistryAuthResponse, registry, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_auth(self, client: Sb0) -> None:
        with client.registry.with_streaming_response.auth(
            namespace="acme",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            registry = response.parse()
            assert_matches_type(RegistryAuthResponse, registry, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncRegistry:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_auth(self, async_client: AsyncSb0) -> None:
        registry = await async_client.registry.auth(
            namespace="acme",
        )
        assert_matches_type(RegistryAuthResponse, registry, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_auth(self, async_client: AsyncSb0) -> None:
        response = await async_client.registry.with_raw_response.auth(
            namespace="acme",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        registry = await response.parse()
        assert_matches_type(RegistryAuthResponse, registry, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_auth(self, async_client: AsyncSb0) -> None:
        async with async_client.registry.with_streaming_response.auth(
            namespace="acme",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            registry = await response.parse()
            assert_matches_type(RegistryAuthResponse, registry, path=["response"])

        assert cast(Any, response.is_closed) is True
