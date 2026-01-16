# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sb0 import Sb0, AsyncSb0
from sb0.types import LogAuthResponse, LogIngestionResponse
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestLogs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_auth(self, client: Sb0) -> None:
        log = client.logs.auth(
            agent_name="agent_name",
        )
        assert_matches_type(LogAuthResponse, log, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_auth(self, client: Sb0) -> None:
        response = client.logs.with_raw_response.auth(
            agent_name="agent_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        log = response.parse()
        assert_matches_type(LogAuthResponse, log, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_auth(self, client: Sb0) -> None:
        with client.logs.with_streaming_response.auth(
            agent_name="agent_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            log = response.parse()
            assert_matches_type(LogAuthResponse, log, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_ingest(self, client: Sb0) -> None:
        log = client.logs.ingest(
            logs=[
                {
                    "message": "message",
                    "source": "stdout",
                    "timestamp": "timestamp",
                }
            ],
        )
        assert_matches_type(LogIngestionResponse, log, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_ingest(self, client: Sb0) -> None:
        response = client.logs.with_raw_response.ingest(
            logs=[
                {
                    "message": "message",
                    "source": "stdout",
                    "timestamp": "timestamp",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        log = response.parse()
        assert_matches_type(LogIngestionResponse, log, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_ingest(self, client: Sb0) -> None:
        with client.logs.with_streaming_response.ingest(
            logs=[
                {
                    "message": "message",
                    "source": "stdout",
                    "timestamp": "timestamp",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            log = response.parse()
            assert_matches_type(LogIngestionResponse, log, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncLogs:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_auth(self, async_client: AsyncSb0) -> None:
        log = await async_client.logs.auth(
            agent_name="agent_name",
        )
        assert_matches_type(LogAuthResponse, log, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_auth(self, async_client: AsyncSb0) -> None:
        response = await async_client.logs.with_raw_response.auth(
            agent_name="agent_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        log = await response.parse()
        assert_matches_type(LogAuthResponse, log, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_auth(self, async_client: AsyncSb0) -> None:
        async with async_client.logs.with_streaming_response.auth(
            agent_name="agent_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            log = await response.parse()
            assert_matches_type(LogAuthResponse, log, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_ingest(self, async_client: AsyncSb0) -> None:
        log = await async_client.logs.ingest(
            logs=[
                {
                    "message": "message",
                    "source": "stdout",
                    "timestamp": "timestamp",
                }
            ],
        )
        assert_matches_type(LogIngestionResponse, log, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_ingest(self, async_client: AsyncSb0) -> None:
        response = await async_client.logs.with_raw_response.ingest(
            logs=[
                {
                    "message": "message",
                    "source": "stdout",
                    "timestamp": "timestamp",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        log = await response.parse()
        assert_matches_type(LogIngestionResponse, log, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_ingest(self, async_client: AsyncSb0) -> None:
        async with async_client.logs.with_streaming_response.ingest(
            logs=[
                {
                    "message": "message",
                    "source": "stdout",
                    "timestamp": "timestamp",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            log = await response.parse()
            assert_matches_type(LogIngestionResponse, log, path=["response"])

        assert cast(Any, response.is_closed) is True
