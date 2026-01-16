# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sb0 import Sb0, AsyncSb0
from tests.utils import assert_matches_type
from sb0.types.agents import (
    EnvResponse,
    EnvListResponse,
    DeleteEnvResponse,
    ResolveEnvResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEnvironments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: Sb0) -> None:
        environment = client.agents.environments.create(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
            branch_rules=["string"],
            name="name",
        )
        assert_matches_type(EnvResponse, environment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Sb0) -> None:
        response = client.agents.environments.with_raw_response.create(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
            branch_rules=["string"],
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        environment = response.parse()
        assert_matches_type(EnvResponse, environment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Sb0) -> None:
        with client.agents.environments.with_streaming_response.create(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
            branch_rules=["string"],
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            environment = response.parse()
            assert_matches_type(EnvResponse, environment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_create(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            client.agents.environments.with_raw_response.create(
                agent_name="agent_name",
                namespace_slug="",
                branch_rules=["string"],
                name="name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            client.agents.environments.with_raw_response.create(
                agent_name="",
                namespace_slug="namespace_slug",
                branch_rules=["string"],
                name="name",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Sb0) -> None:
        environment = client.agents.environments.retrieve(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )
        assert_matches_type(EnvResponse, environment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Sb0) -> None:
        response = client.agents.environments.with_raw_response.retrieve(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        environment = response.parse()
        assert_matches_type(EnvResponse, environment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Sb0) -> None:
        with client.agents.environments.with_streaming_response.retrieve(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            environment = response.parse()
            assert_matches_type(EnvResponse, environment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            client.agents.environments.with_raw_response.retrieve(
                env_name="env_name",
                namespace_slug="",
                agent_name="agent_name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            client.agents.environments.with_raw_response.retrieve(
                env_name="env_name",
                namespace_slug="namespace_slug",
                agent_name="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `env_name` but received ''"):
            client.agents.environments.with_raw_response.retrieve(
                env_name="",
                namespace_slug="namespace_slug",
                agent_name="agent_name",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_update(self, client: Sb0) -> None:
        environment = client.agents.environments.update(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )
        assert_matches_type(EnvResponse, environment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_update_with_all_params(self, client: Sb0) -> None:
        environment = client.agents.environments.update(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
            branch_rules=["string"],
        )
        assert_matches_type(EnvResponse, environment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_update(self, client: Sb0) -> None:
        response = client.agents.environments.with_raw_response.update(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        environment = response.parse()
        assert_matches_type(EnvResponse, environment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_update(self, client: Sb0) -> None:
        with client.agents.environments.with_streaming_response.update(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            environment = response.parse()
            assert_matches_type(EnvResponse, environment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_update(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            client.agents.environments.with_raw_response.update(
                env_name="env_name",
                namespace_slug="",
                agent_name="agent_name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            client.agents.environments.with_raw_response.update(
                env_name="env_name",
                namespace_slug="namespace_slug",
                agent_name="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `env_name` but received ''"):
            client.agents.environments.with_raw_response.update(
                env_name="",
                namespace_slug="namespace_slug",
                agent_name="agent_name",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Sb0) -> None:
        environment = client.agents.environments.list(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
        )
        assert_matches_type(EnvListResponse, environment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Sb0) -> None:
        response = client.agents.environments.with_raw_response.list(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        environment = response.parse()
        assert_matches_type(EnvListResponse, environment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Sb0) -> None:
        with client.agents.environments.with_streaming_response.list(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            environment = response.parse()
            assert_matches_type(EnvListResponse, environment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_list(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            client.agents.environments.with_raw_response.list(
                agent_name="agent_name",
                namespace_slug="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            client.agents.environments.with_raw_response.list(
                agent_name="",
                namespace_slug="namespace_slug",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_delete(self, client: Sb0) -> None:
        environment = client.agents.environments.delete(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )
        assert_matches_type(DeleteEnvResponse, environment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_delete(self, client: Sb0) -> None:
        response = client.agents.environments.with_raw_response.delete(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        environment = response.parse()
        assert_matches_type(DeleteEnvResponse, environment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_delete(self, client: Sb0) -> None:
        with client.agents.environments.with_streaming_response.delete(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            environment = response.parse()
            assert_matches_type(DeleteEnvResponse, environment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_delete(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            client.agents.environments.with_raw_response.delete(
                env_name="env_name",
                namespace_slug="",
                agent_name="agent_name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            client.agents.environments.with_raw_response.delete(
                env_name="env_name",
                namespace_slug="namespace_slug",
                agent_name="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `env_name` but received ''"):
            client.agents.environments.with_raw_response.delete(
                env_name="",
                namespace_slug="namespace_slug",
                agent_name="agent_name",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_resolve_env(self, client: Sb0) -> None:
        environment = client.agents.environments.resolve_env(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
            branch="branch",
        )
        assert_matches_type(ResolveEnvResponse, environment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_resolve_env(self, client: Sb0) -> None:
        response = client.agents.environments.with_raw_response.resolve_env(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
            branch="branch",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        environment = response.parse()
        assert_matches_type(ResolveEnvResponse, environment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_resolve_env(self, client: Sb0) -> None:
        with client.agents.environments.with_streaming_response.resolve_env(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
            branch="branch",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            environment = response.parse()
            assert_matches_type(ResolveEnvResponse, environment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_resolve_env(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            client.agents.environments.with_raw_response.resolve_env(
                agent_name="agent_name",
                namespace_slug="",
                branch="branch",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            client.agents.environments.with_raw_response.resolve_env(
                agent_name="",
                namespace_slug="namespace_slug",
                branch="branch",
            )


class TestAsyncEnvironments:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncSb0) -> None:
        environment = await async_client.agents.environments.create(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
            branch_rules=["string"],
            name="name",
        )
        assert_matches_type(EnvResponse, environment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSb0) -> None:
        response = await async_client.agents.environments.with_raw_response.create(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
            branch_rules=["string"],
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        environment = await response.parse()
        assert_matches_type(EnvResponse, environment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSb0) -> None:
        async with async_client.agents.environments.with_streaming_response.create(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
            branch_rules=["string"],
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            environment = await response.parse()
            assert_matches_type(EnvResponse, environment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_create(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            await async_client.agents.environments.with_raw_response.create(
                agent_name="agent_name",
                namespace_slug="",
                branch_rules=["string"],
                name="name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            await async_client.agents.environments.with_raw_response.create(
                agent_name="",
                namespace_slug="namespace_slug",
                branch_rules=["string"],
                name="name",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSb0) -> None:
        environment = await async_client.agents.environments.retrieve(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )
        assert_matches_type(EnvResponse, environment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSb0) -> None:
        response = await async_client.agents.environments.with_raw_response.retrieve(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        environment = await response.parse()
        assert_matches_type(EnvResponse, environment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSb0) -> None:
        async with async_client.agents.environments.with_streaming_response.retrieve(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            environment = await response.parse()
            assert_matches_type(EnvResponse, environment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            await async_client.agents.environments.with_raw_response.retrieve(
                env_name="env_name",
                namespace_slug="",
                agent_name="agent_name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            await async_client.agents.environments.with_raw_response.retrieve(
                env_name="env_name",
                namespace_slug="namespace_slug",
                agent_name="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `env_name` but received ''"):
            await async_client.agents.environments.with_raw_response.retrieve(
                env_name="",
                namespace_slug="namespace_slug",
                agent_name="agent_name",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_update(self, async_client: AsyncSb0) -> None:
        environment = await async_client.agents.environments.update(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )
        assert_matches_type(EnvResponse, environment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSb0) -> None:
        environment = await async_client.agents.environments.update(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
            branch_rules=["string"],
        )
        assert_matches_type(EnvResponse, environment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSb0) -> None:
        response = await async_client.agents.environments.with_raw_response.update(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        environment = await response.parse()
        assert_matches_type(EnvResponse, environment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSb0) -> None:
        async with async_client.agents.environments.with_streaming_response.update(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            environment = await response.parse()
            assert_matches_type(EnvResponse, environment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_update(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            await async_client.agents.environments.with_raw_response.update(
                env_name="env_name",
                namespace_slug="",
                agent_name="agent_name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            await async_client.agents.environments.with_raw_response.update(
                env_name="env_name",
                namespace_slug="namespace_slug",
                agent_name="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `env_name` but received ''"):
            await async_client.agents.environments.with_raw_response.update(
                env_name="",
                namespace_slug="namespace_slug",
                agent_name="agent_name",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncSb0) -> None:
        environment = await async_client.agents.environments.list(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
        )
        assert_matches_type(EnvListResponse, environment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSb0) -> None:
        response = await async_client.agents.environments.with_raw_response.list(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        environment = await response.parse()
        assert_matches_type(EnvListResponse, environment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSb0) -> None:
        async with async_client.agents.environments.with_streaming_response.list(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            environment = await response.parse()
            assert_matches_type(EnvListResponse, environment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_list(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            await async_client.agents.environments.with_raw_response.list(
                agent_name="agent_name",
                namespace_slug="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            await async_client.agents.environments.with_raw_response.list(
                agent_name="",
                namespace_slug="namespace_slug",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_delete(self, async_client: AsyncSb0) -> None:
        environment = await async_client.agents.environments.delete(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )
        assert_matches_type(DeleteEnvResponse, environment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSb0) -> None:
        response = await async_client.agents.environments.with_raw_response.delete(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        environment = await response.parse()
        assert_matches_type(DeleteEnvResponse, environment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSb0) -> None:
        async with async_client.agents.environments.with_streaming_response.delete(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            environment = await response.parse()
            assert_matches_type(DeleteEnvResponse, environment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            await async_client.agents.environments.with_raw_response.delete(
                env_name="env_name",
                namespace_slug="",
                agent_name="agent_name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            await async_client.agents.environments.with_raw_response.delete(
                env_name="env_name",
                namespace_slug="namespace_slug",
                agent_name="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `env_name` but received ''"):
            await async_client.agents.environments.with_raw_response.delete(
                env_name="",
                namespace_slug="namespace_slug",
                agent_name="agent_name",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_resolve_env(self, async_client: AsyncSb0) -> None:
        environment = await async_client.agents.environments.resolve_env(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
            branch="branch",
        )
        assert_matches_type(ResolveEnvResponse, environment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_resolve_env(self, async_client: AsyncSb0) -> None:
        response = await async_client.agents.environments.with_raw_response.resolve_env(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
            branch="branch",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        environment = await response.parse()
        assert_matches_type(ResolveEnvResponse, environment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_resolve_env(self, async_client: AsyncSb0) -> None:
        async with async_client.agents.environments.with_streaming_response.resolve_env(
            agent_name="agent_name",
            namespace_slug="namespace_slug",
            branch="branch",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            environment = await response.parse()
            assert_matches_type(ResolveEnvResponse, environment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_resolve_env(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            await async_client.agents.environments.with_raw_response.resolve_env(
                agent_name="agent_name",
                namespace_slug="",
                branch="branch",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            await async_client.agents.environments.with_raw_response.resolve_env(
                agent_name="",
                namespace_slug="namespace_slug",
                branch="branch",
            )
