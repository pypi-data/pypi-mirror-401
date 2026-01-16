# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sb0 import Sb0, AsyncSb0
from tests.utils import assert_matches_type
from sb0.types.agents.environments import RollbackResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRollback:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: Sb0) -> None:
        rollback = client.agents.environments.rollback.create(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )
        assert_matches_type(RollbackResponse, rollback, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Sb0) -> None:
        rollback = client.agents.environments.rollback.create(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
            target_version_id="target_version_id",
        )
        assert_matches_type(RollbackResponse, rollback, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Sb0) -> None:
        response = client.agents.environments.rollback.with_raw_response.create(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rollback = response.parse()
        assert_matches_type(RollbackResponse, rollback, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Sb0) -> None:
        with client.agents.environments.rollback.with_streaming_response.create(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rollback = response.parse()
            assert_matches_type(RollbackResponse, rollback, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_create(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            client.agents.environments.rollback.with_raw_response.create(
                env_name="env_name",
                namespace_slug="",
                agent_name="agent_name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            client.agents.environments.rollback.with_raw_response.create(
                env_name="env_name",
                namespace_slug="namespace_slug",
                agent_name="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `env_name` but received ''"):
            client.agents.environments.rollback.with_raw_response.create(
                env_name="",
                namespace_slug="namespace_slug",
                agent_name="agent_name",
            )


class TestAsyncRollback:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncSb0) -> None:
        rollback = await async_client.agents.environments.rollback.create(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )
        assert_matches_type(RollbackResponse, rollback, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSb0) -> None:
        rollback = await async_client.agents.environments.rollback.create(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
            target_version_id="target_version_id",
        )
        assert_matches_type(RollbackResponse, rollback, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSb0) -> None:
        response = await async_client.agents.environments.rollback.with_raw_response.create(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rollback = await response.parse()
        assert_matches_type(RollbackResponse, rollback, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSb0) -> None:
        async with async_client.agents.environments.rollback.with_streaming_response.create(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rollback = await response.parse()
            assert_matches_type(RollbackResponse, rollback, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_create(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            await async_client.agents.environments.rollback.with_raw_response.create(
                env_name="env_name",
                namespace_slug="",
                agent_name="agent_name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            await async_client.agents.environments.rollback.with_raw_response.create(
                env_name="env_name",
                namespace_slug="namespace_slug",
                agent_name="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `env_name` but received ''"):
            await async_client.agents.environments.rollback.with_raw_response.create(
                env_name="",
                namespace_slug="namespace_slug",
                agent_name="agent_name",
            )
