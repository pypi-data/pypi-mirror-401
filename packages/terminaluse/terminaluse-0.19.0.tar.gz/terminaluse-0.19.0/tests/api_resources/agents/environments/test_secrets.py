# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sb0 import Sb0, AsyncSb0
from tests.utils import assert_matches_type
from sb0.types.agents.environments import (
    SetEnvVarResponse,
    EnvVarListResponse,
    DeleteEnvVarResponse,
    DeployedSecretsResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSecrets:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Sb0) -> None:
        secret = client.agents.environments.secrets.list(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )
        assert_matches_type(EnvVarListResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Sb0) -> None:
        secret = client.agents.environments.secrets.list(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
            include_values=True,
        )
        assert_matches_type(EnvVarListResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Sb0) -> None:
        response = client.agents.environments.secrets.with_raw_response.list(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = response.parse()
        assert_matches_type(EnvVarListResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Sb0) -> None:
        with client.agents.environments.secrets.with_streaming_response.list(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = response.parse()
            assert_matches_type(EnvVarListResponse, secret, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_list(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            client.agents.environments.secrets.with_raw_response.list(
                env_name="env_name",
                namespace_slug="",
                agent_name="agent_name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            client.agents.environments.secrets.with_raw_response.list(
                env_name="env_name",
                namespace_slug="namespace_slug",
                agent_name="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `env_name` but received ''"):
            client.agents.environments.secrets.with_raw_response.list(
                env_name="",
                namespace_slug="namespace_slug",
                agent_name="agent_name",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_delete(self, client: Sb0) -> None:
        secret = client.agents.environments.secrets.delete(
            key="key",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
            env_name="env_name",
        )
        assert_matches_type(DeleteEnvVarResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_delete_with_all_params(self, client: Sb0) -> None:
        secret = client.agents.environments.secrets.delete(
            key="key",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
            env_name="env_name",
            redeploy=True,
        )
        assert_matches_type(DeleteEnvVarResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_delete(self, client: Sb0) -> None:
        response = client.agents.environments.secrets.with_raw_response.delete(
            key="key",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
            env_name="env_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = response.parse()
        assert_matches_type(DeleteEnvVarResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_delete(self, client: Sb0) -> None:
        with client.agents.environments.secrets.with_streaming_response.delete(
            key="key",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
            env_name="env_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = response.parse()
            assert_matches_type(DeleteEnvVarResponse, secret, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_delete(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            client.agents.environments.secrets.with_raw_response.delete(
                key="key",
                namespace_slug="",
                agent_name="agent_name",
                env_name="env_name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            client.agents.environments.secrets.with_raw_response.delete(
                key="key",
                namespace_slug="namespace_slug",
                agent_name="",
                env_name="env_name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `env_name` but received ''"):
            client.agents.environments.secrets.with_raw_response.delete(
                key="key",
                namespace_slug="namespace_slug",
                agent_name="agent_name",
                env_name="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `key` but received ''"):
            client.agents.environments.secrets.with_raw_response.delete(
                key="",
                namespace_slug="namespace_slug",
                agent_name="agent_name",
                env_name="env_name",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_deployed(self, client: Sb0) -> None:
        secret = client.agents.environments.secrets.list_deployed(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )
        assert_matches_type(DeployedSecretsResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list_deployed(self, client: Sb0) -> None:
        response = client.agents.environments.secrets.with_raw_response.list_deployed(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = response.parse()
        assert_matches_type(DeployedSecretsResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list_deployed(self, client: Sb0) -> None:
        with client.agents.environments.secrets.with_streaming_response.list_deployed(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = response.parse()
            assert_matches_type(DeployedSecretsResponse, secret, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_list_deployed(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            client.agents.environments.secrets.with_raw_response.list_deployed(
                env_name="env_name",
                namespace_slug="",
                agent_name="agent_name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            client.agents.environments.secrets.with_raw_response.list_deployed(
                env_name="env_name",
                namespace_slug="namespace_slug",
                agent_name="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `env_name` but received ''"):
            client.agents.environments.secrets.with_raw_response.list_deployed(
                env_name="",
                namespace_slug="namespace_slug",
                agent_name="agent_name",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_set(self, client: Sb0) -> None:
        secret = client.agents.environments.secrets.set(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
            secrets={
                "LOG_LEVEL": {"value": "debug"},
                "OPENAI_API_KEY": {"value": "sk-xxx"},
            },
        )
        assert_matches_type(SetEnvVarResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_set_with_all_params(self, client: Sb0) -> None:
        secret = client.agents.environments.secrets.set(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
            secrets={
                "LOG_LEVEL": {
                    "value": "debug",
                    "is_secret": False,
                },
                "OPENAI_API_KEY": {
                    "value": "sk-xxx",
                    "is_secret": True,
                },
            },
            redeploy=True,
        )
        assert_matches_type(SetEnvVarResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_set(self, client: Sb0) -> None:
        response = client.agents.environments.secrets.with_raw_response.set(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
            secrets={
                "LOG_LEVEL": {"value": "debug"},
                "OPENAI_API_KEY": {"value": "sk-xxx"},
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = response.parse()
        assert_matches_type(SetEnvVarResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_set(self, client: Sb0) -> None:
        with client.agents.environments.secrets.with_streaming_response.set(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
            secrets={
                "LOG_LEVEL": {"value": "debug"},
                "OPENAI_API_KEY": {"value": "sk-xxx"},
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = response.parse()
            assert_matches_type(SetEnvVarResponse, secret, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_set(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            client.agents.environments.secrets.with_raw_response.set(
                env_name="env_name",
                namespace_slug="",
                agent_name="agent_name",
                secrets={
                    "LOG_LEVEL": {"value": "debug"},
                    "OPENAI_API_KEY": {"value": "sk-xxx"},
                },
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            client.agents.environments.secrets.with_raw_response.set(
                env_name="env_name",
                namespace_slug="namespace_slug",
                agent_name="",
                secrets={
                    "LOG_LEVEL": {"value": "debug"},
                    "OPENAI_API_KEY": {"value": "sk-xxx"},
                },
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `env_name` but received ''"):
            client.agents.environments.secrets.with_raw_response.set(
                env_name="",
                namespace_slug="namespace_slug",
                agent_name="agent_name",
                secrets={
                    "LOG_LEVEL": {"value": "debug"},
                    "OPENAI_API_KEY": {"value": "sk-xxx"},
                },
            )


class TestAsyncSecrets:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncSb0) -> None:
        secret = await async_client.agents.environments.secrets.list(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )
        assert_matches_type(EnvVarListResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSb0) -> None:
        secret = await async_client.agents.environments.secrets.list(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
            include_values=True,
        )
        assert_matches_type(EnvVarListResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSb0) -> None:
        response = await async_client.agents.environments.secrets.with_raw_response.list(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = await response.parse()
        assert_matches_type(EnvVarListResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSb0) -> None:
        async with async_client.agents.environments.secrets.with_streaming_response.list(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = await response.parse()
            assert_matches_type(EnvVarListResponse, secret, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_list(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            await async_client.agents.environments.secrets.with_raw_response.list(
                env_name="env_name",
                namespace_slug="",
                agent_name="agent_name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            await async_client.agents.environments.secrets.with_raw_response.list(
                env_name="env_name",
                namespace_slug="namespace_slug",
                agent_name="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `env_name` but received ''"):
            await async_client.agents.environments.secrets.with_raw_response.list(
                env_name="",
                namespace_slug="namespace_slug",
                agent_name="agent_name",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_delete(self, async_client: AsyncSb0) -> None:
        secret = await async_client.agents.environments.secrets.delete(
            key="key",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
            env_name="env_name",
        )
        assert_matches_type(DeleteEnvVarResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncSb0) -> None:
        secret = await async_client.agents.environments.secrets.delete(
            key="key",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
            env_name="env_name",
            redeploy=True,
        )
        assert_matches_type(DeleteEnvVarResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSb0) -> None:
        response = await async_client.agents.environments.secrets.with_raw_response.delete(
            key="key",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
            env_name="env_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = await response.parse()
        assert_matches_type(DeleteEnvVarResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSb0) -> None:
        async with async_client.agents.environments.secrets.with_streaming_response.delete(
            key="key",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
            env_name="env_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = await response.parse()
            assert_matches_type(DeleteEnvVarResponse, secret, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            await async_client.agents.environments.secrets.with_raw_response.delete(
                key="key",
                namespace_slug="",
                agent_name="agent_name",
                env_name="env_name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            await async_client.agents.environments.secrets.with_raw_response.delete(
                key="key",
                namespace_slug="namespace_slug",
                agent_name="",
                env_name="env_name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `env_name` but received ''"):
            await async_client.agents.environments.secrets.with_raw_response.delete(
                key="key",
                namespace_slug="namespace_slug",
                agent_name="agent_name",
                env_name="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `key` but received ''"):
            await async_client.agents.environments.secrets.with_raw_response.delete(
                key="",
                namespace_slug="namespace_slug",
                agent_name="agent_name",
                env_name="env_name",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_deployed(self, async_client: AsyncSb0) -> None:
        secret = await async_client.agents.environments.secrets.list_deployed(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )
        assert_matches_type(DeployedSecretsResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list_deployed(self, async_client: AsyncSb0) -> None:
        response = await async_client.agents.environments.secrets.with_raw_response.list_deployed(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = await response.parse()
        assert_matches_type(DeployedSecretsResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list_deployed(self, async_client: AsyncSb0) -> None:
        async with async_client.agents.environments.secrets.with_streaming_response.list_deployed(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = await response.parse()
            assert_matches_type(DeployedSecretsResponse, secret, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_list_deployed(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            await async_client.agents.environments.secrets.with_raw_response.list_deployed(
                env_name="env_name",
                namespace_slug="",
                agent_name="agent_name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            await async_client.agents.environments.secrets.with_raw_response.list_deployed(
                env_name="env_name",
                namespace_slug="namespace_slug",
                agent_name="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `env_name` but received ''"):
            await async_client.agents.environments.secrets.with_raw_response.list_deployed(
                env_name="",
                namespace_slug="namespace_slug",
                agent_name="agent_name",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_set(self, async_client: AsyncSb0) -> None:
        secret = await async_client.agents.environments.secrets.set(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
            secrets={
                "LOG_LEVEL": {"value": "debug"},
                "OPENAI_API_KEY": {"value": "sk-xxx"},
            },
        )
        assert_matches_type(SetEnvVarResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_set_with_all_params(self, async_client: AsyncSb0) -> None:
        secret = await async_client.agents.environments.secrets.set(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
            secrets={
                "LOG_LEVEL": {
                    "value": "debug",
                    "is_secret": False,
                },
                "OPENAI_API_KEY": {
                    "value": "sk-xxx",
                    "is_secret": True,
                },
            },
            redeploy=True,
        )
        assert_matches_type(SetEnvVarResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_set(self, async_client: AsyncSb0) -> None:
        response = await async_client.agents.environments.secrets.with_raw_response.set(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
            secrets={
                "LOG_LEVEL": {"value": "debug"},
                "OPENAI_API_KEY": {"value": "sk-xxx"},
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        secret = await response.parse()
        assert_matches_type(SetEnvVarResponse, secret, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_set(self, async_client: AsyncSb0) -> None:
        async with async_client.agents.environments.secrets.with_streaming_response.set(
            env_name="env_name",
            namespace_slug="namespace_slug",
            agent_name="agent_name",
            secrets={
                "LOG_LEVEL": {"value": "debug"},
                "OPENAI_API_KEY": {"value": "sk-xxx"},
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            secret = await response.parse()
            assert_matches_type(SetEnvVarResponse, secret, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_set(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace_slug` but received ''"):
            await async_client.agents.environments.secrets.with_raw_response.set(
                env_name="env_name",
                namespace_slug="",
                agent_name="agent_name",
                secrets={
                    "LOG_LEVEL": {"value": "debug"},
                    "OPENAI_API_KEY": {"value": "sk-xxx"},
                },
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_name` but received ''"):
            await async_client.agents.environments.secrets.with_raw_response.set(
                env_name="env_name",
                namespace_slug="namespace_slug",
                agent_name="",
                secrets={
                    "LOG_LEVEL": {"value": "debug"},
                    "OPENAI_API_KEY": {"value": "sk-xxx"},
                },
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `env_name` but received ''"):
            await async_client.agents.environments.secrets.with_raw_response.set(
                env_name="",
                namespace_slug="namespace_slug",
                agent_name="agent_name",
                secrets={
                    "LOG_LEVEL": {"value": "debug"},
                    "OPENAI_API_KEY": {"value": "sk-xxx"},
                },
            )
