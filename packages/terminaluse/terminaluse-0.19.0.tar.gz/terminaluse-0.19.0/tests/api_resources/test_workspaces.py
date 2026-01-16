# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sb0 import Sb0, AsyncSb0
from sb0.types import (
    WorkspaceResponse,
    PresignedURLResponse,
    SyncCompleteResponse,
    WorkspaceFileResponse,
    WorkspaceListResponse,
    WorkspaceListFilesResponse,
)
from sb0._utils import parse_datetime
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestWorkspaces:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: Sb0) -> None:
        workspace = client.workspaces.create(
            namespace_id="namespace_id",
            project_id="project_id",
        )
        assert_matches_type(WorkspaceResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Sb0) -> None:
        workspace = client.workspaces.create(
            namespace_id="namespace_id",
            project_id="project_id",
            name="name",
        )
        assert_matches_type(WorkspaceResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Sb0) -> None:
        response = client.workspaces.with_raw_response.create(
            namespace_id="namespace_id",
            project_id="project_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = response.parse()
        assert_matches_type(WorkspaceResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Sb0) -> None:
        with client.workspaces.with_streaming_response.create(
            namespace_id="namespace_id",
            project_id="project_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = response.parse()
            assert_matches_type(WorkspaceResponse, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Sb0) -> None:
        workspace = client.workspaces.retrieve(
            "workspace_id",
        )
        assert_matches_type(WorkspaceResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Sb0) -> None:
        response = client.workspaces.with_raw_response.retrieve(
            "workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = response.parse()
        assert_matches_type(WorkspaceResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Sb0) -> None:
        with client.workspaces.with_streaming_response.retrieve(
            "workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = response.parse()
            assert_matches_type(WorkspaceResponse, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            client.workspaces.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Sb0) -> None:
        workspace = client.workspaces.list()
        assert_matches_type(WorkspaceListResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Sb0) -> None:
        response = client.workspaces.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = response.parse()
        assert_matches_type(WorkspaceListResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Sb0) -> None:
        with client.workspaces.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = response.parse()
            assert_matches_type(WorkspaceListResponse, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_download_url(self, client: Sb0) -> None:
        workspace = client.workspaces.get_download_url(
            workspace_id="workspace_id",
        )
        assert_matches_type(PresignedURLResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_download_url_with_all_params(self, client: Sb0) -> None:
        workspace = client.workspaces.get_download_url(
            workspace_id="workspace_id",
            expiration_seconds=60,
            workspace_directory="ROOT",
        )
        assert_matches_type(PresignedURLResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_get_download_url(self, client: Sb0) -> None:
        response = client.workspaces.with_raw_response.get_download_url(
            workspace_id="workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = response.parse()
        assert_matches_type(PresignedURLResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_get_download_url(self, client: Sb0) -> None:
        with client.workspaces.with_streaming_response.get_download_url(
            workspace_id="workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = response.parse()
            assert_matches_type(PresignedURLResponse, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_get_download_url(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            client.workspaces.with_raw_response.get_download_url(
                workspace_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_file(self, client: Sb0) -> None:
        workspace = client.workspaces.get_file(
            file_path="file_path",
            workspace_id="workspace_id",
        )
        assert_matches_type(WorkspaceFileResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_file_with_all_params(self, client: Sb0) -> None:
        workspace = client.workspaces.get_file(
            file_path="file_path",
            workspace_id="workspace_id",
            include_content=True,
        )
        assert_matches_type(WorkspaceFileResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_get_file(self, client: Sb0) -> None:
        response = client.workspaces.with_raw_response.get_file(
            file_path="file_path",
            workspace_id="workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = response.parse()
        assert_matches_type(WorkspaceFileResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_get_file(self, client: Sb0) -> None:
        with client.workspaces.with_streaming_response.get_file(
            file_path="file_path",
            workspace_id="workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = response.parse()
            assert_matches_type(WorkspaceFileResponse, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_get_file(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            client.workspaces.with_raw_response.get_file(
                file_path="file_path",
                workspace_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_path` but received ''"):
            client.workspaces.with_raw_response.get_file(
                file_path="",
                workspace_id="workspace_id",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_upload_url(self, client: Sb0) -> None:
        workspace = client.workspaces.get_upload_url(
            workspace_id="workspace_id",
        )
        assert_matches_type(PresignedURLResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_upload_url_with_all_params(self, client: Sb0) -> None:
        workspace = client.workspaces.get_upload_url(
            workspace_id="workspace_id",
            expiration_seconds=60,
            workspace_directory="ROOT",
        )
        assert_matches_type(PresignedURLResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_get_upload_url(self, client: Sb0) -> None:
        response = client.workspaces.with_raw_response.get_upload_url(
            workspace_id="workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = response.parse()
        assert_matches_type(PresignedURLResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_get_upload_url(self, client: Sb0) -> None:
        with client.workspaces.with_streaming_response.get_upload_url(
            workspace_id="workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = response.parse()
            assert_matches_type(PresignedURLResponse, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_get_upload_url(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            client.workspaces.with_raw_response.get_upload_url(
                workspace_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_files(self, client: Sb0) -> None:
        workspace = client.workspaces.list_files(
            workspace_id="workspace_id",
        )
        assert_matches_type(WorkspaceListFilesResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_files_with_all_params(self, client: Sb0) -> None:
        workspace = client.workspaces.list_files(
            workspace_id="workspace_id",
            directory="directory",
            include_content=True,
            limit=1,
            mime_type="mime_type",
            offset=0,
            recursive=True,
        )
        assert_matches_type(WorkspaceListFilesResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list_files(self, client: Sb0) -> None:
        response = client.workspaces.with_raw_response.list_files(
            workspace_id="workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = response.parse()
        assert_matches_type(WorkspaceListFilesResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list_files(self, client: Sb0) -> None:
        with client.workspaces.with_streaming_response.list_files(
            workspace_id="workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = response.parse()
            assert_matches_type(WorkspaceListFilesResponse, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_list_files(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            client.workspaces.with_raw_response.list_files(
                workspace_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_sync_complete(self, client: Sb0) -> None:
        workspace = client.workspaces.sync_complete(
            workspace_id="workspace_id",
            direction="direction",
            status="status",
            sync_id="sync_id",
            workspace_directory="ROOT",
        )
        assert_matches_type(SyncCompleteResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_sync_complete_with_all_params(self, client: Sb0) -> None:
        workspace = client.workspaces.sync_complete(
            workspace_id="workspace_id",
            direction="direction",
            status="status",
            sync_id="sync_id",
            workspace_directory="ROOT",
            archive_checksum="archive_checksum",
            archive_size_bytes=0,
            files=[
                {
                    "modified_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "path": "path",
                    "checksum": "checksum",
                    "content": "content",
                    "content_truncated": True,
                    "is_binary": True,
                    "is_directory": True,
                    "mime_type": "mime_type",
                    "size_bytes": 0,
                }
            ],
        )
        assert_matches_type(SyncCompleteResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_sync_complete(self, client: Sb0) -> None:
        response = client.workspaces.with_raw_response.sync_complete(
            workspace_id="workspace_id",
            direction="direction",
            status="status",
            sync_id="sync_id",
            workspace_directory="ROOT",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = response.parse()
        assert_matches_type(SyncCompleteResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_sync_complete(self, client: Sb0) -> None:
        with client.workspaces.with_streaming_response.sync_complete(
            workspace_id="workspace_id",
            direction="direction",
            status="status",
            sync_id="sync_id",
            workspace_directory="ROOT",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = response.parse()
            assert_matches_type(SyncCompleteResponse, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_sync_complete(self, client: Sb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            client.workspaces.with_raw_response.sync_complete(
                workspace_id="",
                direction="direction",
                status="status",
                sync_id="sync_id",
                workspace_directory="ROOT",
            )


class TestAsyncWorkspaces:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncSb0) -> None:
        workspace = await async_client.workspaces.create(
            namespace_id="namespace_id",
            project_id="project_id",
        )
        assert_matches_type(WorkspaceResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSb0) -> None:
        workspace = await async_client.workspaces.create(
            namespace_id="namespace_id",
            project_id="project_id",
            name="name",
        )
        assert_matches_type(WorkspaceResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSb0) -> None:
        response = await async_client.workspaces.with_raw_response.create(
            namespace_id="namespace_id",
            project_id="project_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = await response.parse()
        assert_matches_type(WorkspaceResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSb0) -> None:
        async with async_client.workspaces.with_streaming_response.create(
            namespace_id="namespace_id",
            project_id="project_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = await response.parse()
            assert_matches_type(WorkspaceResponse, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSb0) -> None:
        workspace = await async_client.workspaces.retrieve(
            "workspace_id",
        )
        assert_matches_type(WorkspaceResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSb0) -> None:
        response = await async_client.workspaces.with_raw_response.retrieve(
            "workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = await response.parse()
        assert_matches_type(WorkspaceResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSb0) -> None:
        async with async_client.workspaces.with_streaming_response.retrieve(
            "workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = await response.parse()
            assert_matches_type(WorkspaceResponse, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            await async_client.workspaces.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncSb0) -> None:
        workspace = await async_client.workspaces.list()
        assert_matches_type(WorkspaceListResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSb0) -> None:
        response = await async_client.workspaces.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = await response.parse()
        assert_matches_type(WorkspaceListResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSb0) -> None:
        async with async_client.workspaces.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = await response.parse()
            assert_matches_type(WorkspaceListResponse, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_download_url(self, async_client: AsyncSb0) -> None:
        workspace = await async_client.workspaces.get_download_url(
            workspace_id="workspace_id",
        )
        assert_matches_type(PresignedURLResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_download_url_with_all_params(self, async_client: AsyncSb0) -> None:
        workspace = await async_client.workspaces.get_download_url(
            workspace_id="workspace_id",
            expiration_seconds=60,
            workspace_directory="ROOT",
        )
        assert_matches_type(PresignedURLResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_get_download_url(self, async_client: AsyncSb0) -> None:
        response = await async_client.workspaces.with_raw_response.get_download_url(
            workspace_id="workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = await response.parse()
        assert_matches_type(PresignedURLResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_get_download_url(self, async_client: AsyncSb0) -> None:
        async with async_client.workspaces.with_streaming_response.get_download_url(
            workspace_id="workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = await response.parse()
            assert_matches_type(PresignedURLResponse, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_get_download_url(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            await async_client.workspaces.with_raw_response.get_download_url(
                workspace_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_file(self, async_client: AsyncSb0) -> None:
        workspace = await async_client.workspaces.get_file(
            file_path="file_path",
            workspace_id="workspace_id",
        )
        assert_matches_type(WorkspaceFileResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_file_with_all_params(self, async_client: AsyncSb0) -> None:
        workspace = await async_client.workspaces.get_file(
            file_path="file_path",
            workspace_id="workspace_id",
            include_content=True,
        )
        assert_matches_type(WorkspaceFileResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_get_file(self, async_client: AsyncSb0) -> None:
        response = await async_client.workspaces.with_raw_response.get_file(
            file_path="file_path",
            workspace_id="workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = await response.parse()
        assert_matches_type(WorkspaceFileResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_get_file(self, async_client: AsyncSb0) -> None:
        async with async_client.workspaces.with_streaming_response.get_file(
            file_path="file_path",
            workspace_id="workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = await response.parse()
            assert_matches_type(WorkspaceFileResponse, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_get_file(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            await async_client.workspaces.with_raw_response.get_file(
                file_path="file_path",
                workspace_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_path` but received ''"):
            await async_client.workspaces.with_raw_response.get_file(
                file_path="",
                workspace_id="workspace_id",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_upload_url(self, async_client: AsyncSb0) -> None:
        workspace = await async_client.workspaces.get_upload_url(
            workspace_id="workspace_id",
        )
        assert_matches_type(PresignedURLResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_upload_url_with_all_params(self, async_client: AsyncSb0) -> None:
        workspace = await async_client.workspaces.get_upload_url(
            workspace_id="workspace_id",
            expiration_seconds=60,
            workspace_directory="ROOT",
        )
        assert_matches_type(PresignedURLResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_get_upload_url(self, async_client: AsyncSb0) -> None:
        response = await async_client.workspaces.with_raw_response.get_upload_url(
            workspace_id="workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = await response.parse()
        assert_matches_type(PresignedURLResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_get_upload_url(self, async_client: AsyncSb0) -> None:
        async with async_client.workspaces.with_streaming_response.get_upload_url(
            workspace_id="workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = await response.parse()
            assert_matches_type(PresignedURLResponse, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_get_upload_url(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            await async_client.workspaces.with_raw_response.get_upload_url(
                workspace_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_files(self, async_client: AsyncSb0) -> None:
        workspace = await async_client.workspaces.list_files(
            workspace_id="workspace_id",
        )
        assert_matches_type(WorkspaceListFilesResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_files_with_all_params(self, async_client: AsyncSb0) -> None:
        workspace = await async_client.workspaces.list_files(
            workspace_id="workspace_id",
            directory="directory",
            include_content=True,
            limit=1,
            mime_type="mime_type",
            offset=0,
            recursive=True,
        )
        assert_matches_type(WorkspaceListFilesResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list_files(self, async_client: AsyncSb0) -> None:
        response = await async_client.workspaces.with_raw_response.list_files(
            workspace_id="workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = await response.parse()
        assert_matches_type(WorkspaceListFilesResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list_files(self, async_client: AsyncSb0) -> None:
        async with async_client.workspaces.with_streaming_response.list_files(
            workspace_id="workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = await response.parse()
            assert_matches_type(WorkspaceListFilesResponse, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_list_files(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            await async_client.workspaces.with_raw_response.list_files(
                workspace_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_sync_complete(self, async_client: AsyncSb0) -> None:
        workspace = await async_client.workspaces.sync_complete(
            workspace_id="workspace_id",
            direction="direction",
            status="status",
            sync_id="sync_id",
            workspace_directory="ROOT",
        )
        assert_matches_type(SyncCompleteResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_sync_complete_with_all_params(self, async_client: AsyncSb0) -> None:
        workspace = await async_client.workspaces.sync_complete(
            workspace_id="workspace_id",
            direction="direction",
            status="status",
            sync_id="sync_id",
            workspace_directory="ROOT",
            archive_checksum="archive_checksum",
            archive_size_bytes=0,
            files=[
                {
                    "modified_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "path": "path",
                    "checksum": "checksum",
                    "content": "content",
                    "content_truncated": True,
                    "is_binary": True,
                    "is_directory": True,
                    "mime_type": "mime_type",
                    "size_bytes": 0,
                }
            ],
        )
        assert_matches_type(SyncCompleteResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_sync_complete(self, async_client: AsyncSb0) -> None:
        response = await async_client.workspaces.with_raw_response.sync_complete(
            workspace_id="workspace_id",
            direction="direction",
            status="status",
            sync_id="sync_id",
            workspace_directory="ROOT",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = await response.parse()
        assert_matches_type(SyncCompleteResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_sync_complete(self, async_client: AsyncSb0) -> None:
        async with async_client.workspaces.with_streaming_response.sync_complete(
            workspace_id="workspace_id",
            direction="direction",
            status="status",
            sync_id="sync_id",
            workspace_directory="ROOT",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = await response.parse()
            assert_matches_type(SyncCompleteResponse, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_sync_complete(self, async_client: AsyncSb0) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            await async_client.workspaces.with_raw_response.sync_complete(
                workspace_id="",
                direction="direction",
                status="status",
                sync_id="sync_id",
                workspace_directory="ROOT",
            )
