# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sb0 import Sb0, AsyncSb0
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestName:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get(self, client: Sb0) -> None:
        name = client.agents.forward.name.get(
            path="path",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )
        assert_matches_type(object, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_get(self, client: Sb0) -> None:
        response = client.agents.forward.name.with_raw_response.get(
            path="path",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        name = response.parse()
        assert_matches_type(object, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_get(self, client: Sb0) -> None:
        with client.agents.forward.name.with_streaming_response.get(
            path="path",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            name = response.parse()
            assert_matches_type(object, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_get(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            client.agents.forward.name.with_raw_response.get(
                path="path",
                namespace_slug="",
                agent_name="agent_name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            client.agents.forward.name.with_raw_response.get(
                path="path",
                namespace_slug="namespace_slug",
                agent_name="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path` but received ''"):
            client.agents.forward.name.with_raw_response.get(
                path="",
                namespace_slug="namespace_slug",
                agent_name="agent_name",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_post(self, client: Sb0) -> None:
        name = client.agents.forward.name.post(
            path="path",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )
        assert_matches_type(object, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_post(self, client: Sb0) -> None:
        response = client.agents.forward.name.with_raw_response.post(
            path="path",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        name = response.parse()
        assert_matches_type(object, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_post(self, client: Sb0) -> None:
        with client.agents.forward.name.with_streaming_response.post(
            path="path",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            name = response.parse()
            assert_matches_type(object, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_post(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            client.agents.forward.name.with_raw_response.post(
                path="path",
                namespace_slug="",
                agent_name="agent_name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            client.agents.forward.name.with_raw_response.post(
                path="path",
                namespace_slug="namespace_slug",
                agent_name="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path` but received ''"):
            client.agents.forward.name.with_raw_response.post(
                path="",
                namespace_slug="namespace_slug",
                agent_name="agent_name",
            )


class TestAsyncName:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get(self, async_client: AsyncSb0) -> None:
        name = await async_client.agents.forward.name.get(
            path="path",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )
        assert_matches_type(object, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_get(self, async_client: AsyncSb0) -> None:
        response = await async_client.agents.forward.name.with_raw_response.get(
            path="path",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        name = await response.parse()
        assert_matches_type(object, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncSb0) -> None:
        async with async_client.agents.forward.name.with_streaming_response.get(
            path="path",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            name = await response.parse()
            assert_matches_type(object, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_get(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            await async_client.agents.forward.name.with_raw_response.get(
                path="path",
                namespace_slug="",
                agent_name="agent_name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            await async_client.agents.forward.name.with_raw_response.get(
                path="path",
                namespace_slug="namespace_slug",
                agent_name="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path` but received ''"):
            await async_client.agents.forward.name.with_raw_response.get(
                path="",
                namespace_slug="namespace_slug",
                agent_name="agent_name",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_post(self, async_client: AsyncSb0) -> None:
        name = await async_client.agents.forward.name.post(
            path="path",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )
        assert_matches_type(object, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_post(self, async_client: AsyncSb0) -> None:
        response = await async_client.agents.forward.name.with_raw_response.post(
            path="path",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        name = await response.parse()
        assert_matches_type(object, name, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_post(self, async_client: AsyncSb0) -> None:
        async with async_client.agents.forward.name.with_streaming_response.post(
            path="path",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            name = await response.parse()
            assert_matches_type(object, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_post(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            await async_client.agents.forward.name.with_raw_response.post(
                path="path",
                namespace_slug="",
                agent_name="agent_name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            await async_client.agents.forward.name.with_raw_response.post(
                path="path",
                namespace_slug="namespace_slug",
                agent_name="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path` but received ''"):
            await async_client.agents.forward.name.with_raw_response.post(
                path="",
                namespace_slug="namespace_slug",
                agent_name="agent_name",
            )
