# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional

import httpx

from ..types import (
    WorkspaceDirectory,
    workspace_create_params,
    workspace_get_file_params,
    workspace_list_files_params,
    workspace_sync_complete_params,
    workspace_get_upload_url_params,
    workspace_get_download_url_params,
)
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.workspace_response import WorkspaceResponse
from ..types.workspace_directory import WorkspaceDirectory
from ..types.workspace_file_param import WorkspaceFileParam
from ..types.presigned_url_response import PresignedURLResponse
from ..types.sync_complete_response import SyncCompleteResponse
from ..types.workspace_file_response import WorkspaceFileResponse
from ..types.workspace_list_response import WorkspaceListResponse
from ..types.workspace_list_files_response import WorkspaceListFilesResponse

__all__ = ["WorkspacesResource", "AsyncWorkspacesResource"]


class WorkspacesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> WorkspacesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return WorkspacesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> WorkspacesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return WorkspacesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        namespace_id: str,
        project_id: str,
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WorkspaceResponse:
        """
        Create a new workspace with optional name.

        Args:
          namespace_id: Namespace ID for tenant isolation

          project_id: Project ID this workspace belongs to (required for authorization).

          name: Optional human-readable name for the workspace (unique per namespace).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/workspaces",
            body=maybe_transform(
                {
                    "project_id": project_id,
                    "name": name,
                },
                workspace_create_params.WorkspaceCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"namespace_id": namespace_id}, workspace_create_params.WorkspaceCreateParams),
            ),
            cast_to=WorkspaceResponse,
        )

    def retrieve(
        self,
        workspace_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WorkspaceResponse:
        """
        Get workspace details by ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return self._get(
            f"/workspaces/{workspace_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkspaceResponse,
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WorkspaceListResponse:
        """List all workspaces accessible to the current user."""
        return self._get(
            "/workspaces",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkspaceListResponse,
        )

    def get_download_url(
        self,
        workspace_id: str,
        *,
        expiration_seconds: int | Omit = omit,
        workspace_directory: WorkspaceDirectory | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PresignedURLResponse:
        """
        Get a presigned URL for direct download from GCS.

        Args:
          expiration_seconds: URL expiration time in seconds (default 1 hour, max 7 days).

          workspace_directory: Which storage target to access: workspace or dot_claude archive.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return self._post(
            f"/workspaces/{workspace_id}/download-url",
            body=maybe_transform(
                {
                    "expiration_seconds": expiration_seconds,
                    "workspace_directory": workspace_directory,
                },
                workspace_get_download_url_params.WorkspaceGetDownloadURLParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PresignedURLResponse,
        )

    def get_file(
        self,
        file_path: str,
        *,
        workspace_id: str,
        include_content: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WorkspaceFileResponse:
        """
        Retrieve a specific file (or directory) from the workspace manifest.

        Args:
          include_content: Include file content in response

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        if not file_path:
            raise ValueError(f"Expected a non-empty value for `file_path` but received {file_path!r}")
        return self._get(
            f"/workspaces/{workspace_id}/files/{file_path}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"include_content": include_content}, workspace_get_file_params.WorkspaceGetFileParams
                ),
            ),
            cast_to=WorkspaceFileResponse,
        )

    def get_upload_url(
        self,
        workspace_id: str,
        *,
        expiration_seconds: int | Omit = omit,
        workspace_directory: WorkspaceDirectory | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PresignedURLResponse:
        """
        Get a presigned URL for direct upload to GCS.

        Args:
          expiration_seconds: URL expiration time in seconds (default 1 hour, max 7 days).

          workspace_directory: Which storage target to access: workspace or dot_claude archive.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return self._post(
            f"/workspaces/{workspace_id}/upload-url",
            body=maybe_transform(
                {
                    "expiration_seconds": expiration_seconds,
                    "workspace_directory": workspace_directory,
                },
                workspace_get_upload_url_params.WorkspaceGetUploadURLParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PresignedURLResponse,
        )

    def list_files(
        self,
        workspace_id: str,
        *,
        directory: str | Omit = omit,
        include_content: bool | Omit = omit,
        limit: int | Omit = omit,
        mime_type: Optional[str] | Omit = omit,
        offset: int | Omit = omit,
        recursive: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WorkspaceListFilesResponse:
        """
        List files in the workspace manifest with optional filtering.

        Args:
          directory: Directory prefix to filter results

          include_content: Include file content in response

          limit: Maximum number of results

          mime_type: Filter by MIME type

          offset: Pagination offset

          recursive: Include subdirectories

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return self._get(
            f"/workspaces/{workspace_id}/files",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "directory": directory,
                        "include_content": include_content,
                        "limit": limit,
                        "mime_type": mime_type,
                        "offset": offset,
                        "recursive": recursive,
                    },
                    workspace_list_files_params.WorkspaceListFilesParams,
                ),
            ),
            cast_to=WorkspaceListFilesResponse,
        )

    def sync_complete(
        self,
        workspace_id: str,
        *,
        direction: str,
        status: str,
        sync_id: str,
        workspace_directory: WorkspaceDirectory,
        archive_checksum: Optional[str] | Omit = omit,
        archive_size_bytes: Optional[int] | Omit = omit,
        files: Optional[Iterable[WorkspaceFileParam]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCompleteResponse:
        """
        Notify that a sync operation completed and provide the file manifest.

        Args:
          direction: Sync direction: 'UP' or 'DOWN'.

          status: Sync status: 'SUCCESS' or 'FAILED'.

          sync_id: Unique ID for this sync operation (idempotency key).

          workspace_directory: Which storage target to access: workspace or dot_claude archive.

          archive_checksum: SHA256 checksum of the archive.

          archive_size_bytes: Size of the archive in bytes.

          files: List of files in the workspace (empty if status is FAILED).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return self._post(
            f"/workspaces/{workspace_id}/sync-complete",
            body=maybe_transform(
                {
                    "direction": direction,
                    "status": status,
                    "sync_id": sync_id,
                    "workspace_directory": workspace_directory,
                    "archive_checksum": archive_checksum,
                    "archive_size_bytes": archive_size_bytes,
                    "files": files,
                },
                workspace_sync_complete_params.WorkspaceSyncCompleteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SyncCompleteResponse,
        )


class AsyncWorkspacesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncWorkspacesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncWorkspacesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncWorkspacesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/terminal-use/sb0-python-sdk#with_streaming_response
        """
        return AsyncWorkspacesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        namespace_id: str,
        project_id: str,
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WorkspaceResponse:
        """
        Create a new workspace with optional name.

        Args:
          namespace_id: Namespace ID for tenant isolation

          project_id: Project ID this workspace belongs to (required for authorization).

          name: Optional human-readable name for the workspace (unique per namespace).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/workspaces",
            body=await async_maybe_transform(
                {
                    "project_id": project_id,
                    "name": name,
                },
                workspace_create_params.WorkspaceCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"namespace_id": namespace_id}, workspace_create_params.WorkspaceCreateParams
                ),
            ),
            cast_to=WorkspaceResponse,
        )

    async def retrieve(
        self,
        workspace_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WorkspaceResponse:
        """
        Get workspace details by ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return await self._get(
            f"/workspaces/{workspace_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkspaceResponse,
        )

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WorkspaceListResponse:
        """List all workspaces accessible to the current user."""
        return await self._get(
            "/workspaces",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkspaceListResponse,
        )

    async def get_download_url(
        self,
        workspace_id: str,
        *,
        expiration_seconds: int | Omit = omit,
        workspace_directory: WorkspaceDirectory | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PresignedURLResponse:
        """
        Get a presigned URL for direct download from GCS.

        Args:
          expiration_seconds: URL expiration time in seconds (default 1 hour, max 7 days).

          workspace_directory: Which storage target to access: workspace or dot_claude archive.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return await self._post(
            f"/workspaces/{workspace_id}/download-url",
            body=await async_maybe_transform(
                {
                    "expiration_seconds": expiration_seconds,
                    "workspace_directory": workspace_directory,
                },
                workspace_get_download_url_params.WorkspaceGetDownloadURLParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PresignedURLResponse,
        )

    async def get_file(
        self,
        file_path: str,
        *,
        workspace_id: str,
        include_content: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WorkspaceFileResponse:
        """
        Retrieve a specific file (or directory) from the workspace manifest.

        Args:
          include_content: Include file content in response

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        if not file_path:
            raise ValueError(f"Expected a non-empty value for `file_path` but received {file_path!r}")
        return await self._get(
            f"/workspaces/{workspace_id}/files/{file_path}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"include_content": include_content}, workspace_get_file_params.WorkspaceGetFileParams
                ),
            ),
            cast_to=WorkspaceFileResponse,
        )

    async def get_upload_url(
        self,
        workspace_id: str,
        *,
        expiration_seconds: int | Omit = omit,
        workspace_directory: WorkspaceDirectory | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PresignedURLResponse:
        """
        Get a presigned URL for direct upload to GCS.

        Args:
          expiration_seconds: URL expiration time in seconds (default 1 hour, max 7 days).

          workspace_directory: Which storage target to access: workspace or dot_claude archive.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return await self._post(
            f"/workspaces/{workspace_id}/upload-url",
            body=await async_maybe_transform(
                {
                    "expiration_seconds": expiration_seconds,
                    "workspace_directory": workspace_directory,
                },
                workspace_get_upload_url_params.WorkspaceGetUploadURLParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PresignedURLResponse,
        )

    async def list_files(
        self,
        workspace_id: str,
        *,
        directory: str | Omit = omit,
        include_content: bool | Omit = omit,
        limit: int | Omit = omit,
        mime_type: Optional[str] | Omit = omit,
        offset: int | Omit = omit,
        recursive: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WorkspaceListFilesResponse:
        """
        List files in the workspace manifest with optional filtering.

        Args:
          directory: Directory prefix to filter results

          include_content: Include file content in response

          limit: Maximum number of results

          mime_type: Filter by MIME type

          offset: Pagination offset

          recursive: Include subdirectories

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return await self._get(
            f"/workspaces/{workspace_id}/files",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "directory": directory,
                        "include_content": include_content,
                        "limit": limit,
                        "mime_type": mime_type,
                        "offset": offset,
                        "recursive": recursive,
                    },
                    workspace_list_files_params.WorkspaceListFilesParams,
                ),
            ),
            cast_to=WorkspaceListFilesResponse,
        )

    async def sync_complete(
        self,
        workspace_id: str,
        *,
        direction: str,
        status: str,
        sync_id: str,
        workspace_directory: WorkspaceDirectory,
        archive_checksum: Optional[str] | Omit = omit,
        archive_size_bytes: Optional[int] | Omit = omit,
        files: Optional[Iterable[WorkspaceFileParam]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCompleteResponse:
        """
        Notify that a sync operation completed and provide the file manifest.

        Args:
          direction: Sync direction: 'UP' or 'DOWN'.

          status: Sync status: 'SUCCESS' or 'FAILED'.

          sync_id: Unique ID for this sync operation (idempotency key).

          workspace_directory: Which storage target to access: workspace or dot_claude archive.

          archive_checksum: SHA256 checksum of the archive.

          archive_size_bytes: Size of the archive in bytes.

          files: List of files in the workspace (empty if status is FAILED).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return await self._post(
            f"/workspaces/{workspace_id}/sync-complete",
            body=await async_maybe_transform(
                {
                    "direction": direction,
                    "status": status,
                    "sync_id": sync_id,
                    "workspace_directory": workspace_directory,
                    "archive_checksum": archive_checksum,
                    "archive_size_bytes": archive_size_bytes,
                    "files": files,
                },
                workspace_sync_complete_params.WorkspaceSyncCompleteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SyncCompleteResponse,
        )


class WorkspacesResourceWithRawResponse:
    def __init__(self, workspaces: WorkspacesResource) -> None:
        self._workspaces = workspaces

        self.create = to_raw_response_wrapper(
            workspaces.create,
        )
        self.retrieve = to_raw_response_wrapper(
            workspaces.retrieve,
        )
        self.list = to_raw_response_wrapper(
            workspaces.list,
        )
        self.get_download_url = to_raw_response_wrapper(
            workspaces.get_download_url,
        )
        self.get_file = to_raw_response_wrapper(
            workspaces.get_file,
        )
        self.get_upload_url = to_raw_response_wrapper(
            workspaces.get_upload_url,
        )
        self.list_files = to_raw_response_wrapper(
            workspaces.list_files,
        )
        self.sync_complete = to_raw_response_wrapper(
            workspaces.sync_complete,
        )


class AsyncWorkspacesResourceWithRawResponse:
    def __init__(self, workspaces: AsyncWorkspacesResource) -> None:
        self._workspaces = workspaces

        self.create = async_to_raw_response_wrapper(
            workspaces.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            workspaces.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            workspaces.list,
        )
        self.get_download_url = async_to_raw_response_wrapper(
            workspaces.get_download_url,
        )
        self.get_file = async_to_raw_response_wrapper(
            workspaces.get_file,
        )
        self.get_upload_url = async_to_raw_response_wrapper(
            workspaces.get_upload_url,
        )
        self.list_files = async_to_raw_response_wrapper(
            workspaces.list_files,
        )
        self.sync_complete = async_to_raw_response_wrapper(
            workspaces.sync_complete,
        )


class WorkspacesResourceWithStreamingResponse:
    def __init__(self, workspaces: WorkspacesResource) -> None:
        self._workspaces = workspaces

        self.create = to_streamed_response_wrapper(
            workspaces.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            workspaces.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            workspaces.list,
        )
        self.get_download_url = to_streamed_response_wrapper(
            workspaces.get_download_url,
        )
        self.get_file = to_streamed_response_wrapper(
            workspaces.get_file,
        )
        self.get_upload_url = to_streamed_response_wrapper(
            workspaces.get_upload_url,
        )
        self.list_files = to_streamed_response_wrapper(
            workspaces.list_files,
        )
        self.sync_complete = to_streamed_response_wrapper(
            workspaces.sync_complete,
        )


class AsyncWorkspacesResourceWithStreamingResponse:
    def __init__(self, workspaces: AsyncWorkspacesResource) -> None:
        self._workspaces = workspaces

        self.create = async_to_streamed_response_wrapper(
            workspaces.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            workspaces.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            workspaces.list,
        )
        self.get_download_url = async_to_streamed_response_wrapper(
            workspaces.get_download_url,
        )
        self.get_file = async_to_streamed_response_wrapper(
            workspaces.get_file,
        )
        self.get_upload_url = async_to_streamed_response_wrapper(
            workspaces.get_upload_url,
        )
        self.list_files = async_to_streamed_response_wrapper(
            workspaces.list_files,
        )
        self.sync_complete = async_to_streamed_response_wrapper(
            workspaces.sync_complete,
        )
