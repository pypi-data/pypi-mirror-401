# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sb0 import Sb0, AsyncSb0
from sb0.types import (
    RedeployResponse,
    DeploymentResponse,
    RegisterContainerResponse,
)
from tests.utils import assert_matches_type
from sb0.types.agents.environments import RollbackResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDeployments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Sb0) -> None:
        deployment = client.deployments.retrieve(
            "deployment_id",
        )
        assert_matches_type(DeploymentResponse, deployment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Sb0) -> None:
        response = client.deployments.with_raw_response.retrieve(
            "deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(DeploymentResponse, deployment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Sb0) -> None:
        with client.deployments.with_streaming_response.retrieve(
            "deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(DeploymentResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            client.deployments.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_redeploy(self, client: Sb0) -> None:
        deployment = client.deployments.redeploy(
            "deployment_id",
        )
        assert_matches_type(RedeployResponse, deployment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_redeploy(self, client: Sb0) -> None:
        response = client.deployments.with_raw_response.redeploy(
            "deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(RedeployResponse, deployment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_redeploy(self, client: Sb0) -> None:
        with client.deployments.with_streaming_response.redeploy(
            "deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(RedeployResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_redeploy(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            client.deployments.with_raw_response.redeploy(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_register(self, client: Sb0) -> None:
        deployment = client.deployments.register(
            acp_url="acp_url",
            deployment_id="deployment_id",
            version_id="version_id",
        )
        assert_matches_type(RegisterContainerResponse, deployment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_register(self, client: Sb0) -> None:
        response = client.deployments.with_raw_response.register(
            acp_url="acp_url",
            deployment_id="deployment_id",
            version_id="version_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(RegisterContainerResponse, deployment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_register(self, client: Sb0) -> None:
        with client.deployments.with_streaming_response.register(
            acp_url="acp_url",
            deployment_id="deployment_id",
            version_id="version_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(RegisterContainerResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_rollback(self, client: Sb0) -> None:
        deployment = client.deployments.rollback(
            deployment_id="deployment_id",
        )
        assert_matches_type(RollbackResponse, deployment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_rollback_with_all_params(self, client: Sb0) -> None:
        deployment = client.deployments.rollback(
            deployment_id="deployment_id",
            target_version_id="target_version_id",
        )
        assert_matches_type(RollbackResponse, deployment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_rollback(self, client: Sb0) -> None:
        response = client.deployments.with_raw_response.rollback(
            deployment_id="deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(RollbackResponse, deployment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_rollback(self, client: Sb0) -> None:
        with client.deployments.with_streaming_response.rollback(
            deployment_id="deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(RollbackResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_rollback(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            client.deployments.with_raw_response.rollback(
                deployment_id="",
            )


class TestAsyncDeployments:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSb0) -> None:
        deployment = await async_client.deployments.retrieve(
            "deployment_id",
        )
        assert_matches_type(DeploymentResponse, deployment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSb0) -> None:
        response = await async_client.deployments.with_raw_response.retrieve(
            "deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(DeploymentResponse, deployment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSb0) -> None:
        async with async_client.deployments.with_streaming_response.retrieve(
            "deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(DeploymentResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            await async_client.deployments.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_redeploy(self, async_client: AsyncSb0) -> None:
        deployment = await async_client.deployments.redeploy(
            "deployment_id",
        )
        assert_matches_type(RedeployResponse, deployment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_redeploy(self, async_client: AsyncSb0) -> None:
        response = await async_client.deployments.with_raw_response.redeploy(
            "deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(RedeployResponse, deployment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_redeploy(self, async_client: AsyncSb0) -> None:
        async with async_client.deployments.with_streaming_response.redeploy(
            "deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(RedeployResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_redeploy(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            await async_client.deployments.with_raw_response.redeploy(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_register(self, async_client: AsyncSb0) -> None:
        deployment = await async_client.deployments.register(
            acp_url="acp_url",
            deployment_id="deployment_id",
            version_id="version_id",
        )
        assert_matches_type(RegisterContainerResponse, deployment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_register(self, async_client: AsyncSb0) -> None:
        response = await async_client.deployments.with_raw_response.register(
            acp_url="acp_url",
            deployment_id="deployment_id",
            version_id="version_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(RegisterContainerResponse, deployment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_register(self, async_client: AsyncSb0) -> None:
        async with async_client.deployments.with_streaming_response.register(
            acp_url="acp_url",
            deployment_id="deployment_id",
            version_id="version_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(RegisterContainerResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_rollback(self, async_client: AsyncSb0) -> None:
        deployment = await async_client.deployments.rollback(
            deployment_id="deployment_id",
        )
        assert_matches_type(RollbackResponse, deployment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_rollback_with_all_params(self, async_client: AsyncSb0) -> None:
        deployment = await async_client.deployments.rollback(
            deployment_id="deployment_id",
            target_version_id="target_version_id",
        )
        assert_matches_type(RollbackResponse, deployment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_rollback(self, async_client: AsyncSb0) -> None:
        response = await async_client.deployments.with_raw_response.rollback(
            deployment_id="deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(RollbackResponse, deployment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_rollback(self, async_client: AsyncSb0) -> None:
        async with async_client.deployments.with_streaming_response.rollback(
            deployment_id="deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(RollbackResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_rollback(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            await async_client.deployments.with_raw_response.rollback(
                deployment_id="",
            )
