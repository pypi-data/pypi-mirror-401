"""
Workspace sync module for the Agent Development Kit (ADK).

This module provides high-level async methods for workspace sync operations:
- sync_down: Download workspace from GCS if changed
- sync_up: Upload workspace to GCS if changed

Optimizations:
- Skip download if archive checksum unchanged
- Skip upload if no files modified (mtime check)
- Background manifest building for sync_down
"""

from __future__ import annotations

import uuid
import asyncio
from pathlib import Path
from dataclasses import dataclass

import httpx
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

from sb0 import AsyncSb0
from sb0.types import WorkspaceDirectory, WorkspaceFileParam
from sb0.lib.utils.logging import make_logger
from sb0.lib.environment_variables import EnvironmentVariables
from sb0.lib.utils.workspace_archive import (
    ArchiveResult,
    WorkspaceSyncError,
    CorruptArchiveError,
    WorkspaceNotFoundError,
    create_archive,
    extract_archive,
    upload_to_presigned_url,
    download_from_presigned_url,
)
from sb0.lib.utils.workspace_manifest import (
    DEFAULT_SKIP_PATTERNS,
    SyncCache,
    ManifestEntry,
    WorkspaceManifest,
    ManifestTooLargeError,
    validate_manifest_size,
)
from sb0.lib.adk.utils._modules.client import create_async_sb0_client

logger = make_logger(__name__)

# HTTP retry configuration for sync-complete API calls
SYNC_COMPLETE_RETRY_CONFIG = {
    "stop": stop_after_attempt(2),  # Initial attempt + 1 retry
    "wait": wait_exponential(multiplier=1, min=1, max=10),
    "retry": retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError)),
}

# Re-export exceptions for convenience
__all__ = [
    "WorkspaceModule",
    "SyncDownResult",
    "SyncUpResult",
    "WorkspaceSyncError",
    "CorruptArchiveError",
    "WorkspaceNotFoundError",
    "ManifestTooLargeError",
]


@dataclass
class SyncDownResult:
    """Result of sync_down operation."""

    skipped: bool
    reason: str | None = None
    files_extracted: int | None = None
    manifest_pending: bool = False  # True if background task running


@dataclass
class SyncUpResult:
    """Result of sync_up operation."""

    skipped: bool
    reason: str | None = None
    files_uploaded: int | None = None
    archive_size_bytes: int | None = None


class WorkspaceModule:
    """
    Module for workspace sync operations in Sb0.

    Provides high-level async methods for:
    - sync_down: Download workspace from GCS if changed
    - sync_up: Upload workspace to GCS if changed

    Optimizations:
    - Skip download if archive checksum unchanged
    - Skip upload if no files modified (mtime check)
    - Background manifest building for sync_down
    """

    def __init__(
        self,
        client: AsyncSb0 | None = None,
        local_workspace_path: Path | None = None,
    ):
        """
        Initialize workspace module.

        Args:
            client: Optional Sb0 client (creates new if not provided)
            local_workspace_path: Override default workspace path
        """
        self._client = client
        self._local_workspace_path = local_workspace_path
        self._background_tasks: list[asyncio.Task[None]] = []
        self._skip_patterns = list(DEFAULT_SKIP_PATTERNS)

    def _get_client(self) -> AsyncSb0:
        """Get or create the Sb0 client lazily."""
        if self._client is None:
            self._client = create_async_sb0_client()
        return self._client

    def _get_workspace_path(
        self, workspace_id: str, workspace_directory: WorkspaceDirectory = "ROOT"
    ) -> Path:
        """
        Get local path for workspace.

        Priority:
        1. self._local_workspace_path (if set for ROOT)
        2. CLAUDE_WORKSPACE_ROOT environment variable for ROOT
        3. Default: /workspaces/{workspace_id} for ROOT
        4. Default: /dot_claudes/{workspace_id} for DOT_CLAUDE
        """
        if self._local_workspace_path and workspace_directory == "ROOT":
            return self._local_workspace_path

        if workspace_directory == "ROOT":
            # Check for CLAUDE_WORKSPACE_ROOT environment variable
            env_vars = EnvironmentVariables.refresh()
            if env_vars.CLAUDE_WORKSPACE_ROOT:
                return Path(env_vars.CLAUDE_WORKSPACE_ROOT)
            # Default workspace path
            return Path(f"/workspaces/{workspace_id}")

        if workspace_directory == "DOT_CLAUDE":
            # This could be made configurable if needed.
            return Path(f"/dot_claudes/{workspace_id}")

        raise ValueError(f"Unknown workspace directory: {workspace_directory}")

    async def sync_down(
        self,
        workspace_id: str,
        local_path: Path | None = None,
        workspace_directory: WorkspaceDirectory = "ROOT",
    ) -> SyncDownResult:
        """
        Download workspace from GCS if changed.

        Flow:
        1. Load local sync cache, get archive_checksum
        2. GET /workspaces/{id} → get remote archive_checksum
        3. Compare checksums
           - SAME → return skipped=True (~50ms)
           - DIFFERENT → continue to download
        4. POST /workspaces/{id}/download-url → get presigned URL
        5. Download archive via presigned URL
        6. Extract to local_path
        7. Return immediately (agent can start)
        8. (Background) Build manifest + POST /sync-complete

        Background task allows agent to start immediately after extraction,
        saving 200-600ms of blocking time.

        Args:
            workspace_id: ID of the workspace to sync
            local_path: Optional override for local workspace path
            workspace_directory: The directory to sync (ROOT or DOT_CLAUDE)

        Returns:
            SyncDownResult with sync status
        """
        local_path = local_path or self._get_workspace_path(workspace_id, workspace_directory)
        try:
            local_path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise WorkspaceSyncError(f"Failed to create workspace directory {local_path}: {e}") from e

        client = self._get_client()

        # 1. Load local cache
        sync_cache = SyncCache(local_path)
        local_checksum = sync_cache.get_archive_checksum()

        # 2. Get remote workspace state
        workspace = await client.workspaces.retrieve(workspace_id)
        if workspace_directory == "ROOT":
            remote_checksum: str | None = getattr(workspace, "workspace_archive_checksum", None)
        else:
            remote_checksum: str | None = getattr(workspace, "dot_claude_archive_checksum", None)

        # 3. Fast path: unchanged (only skip if we have checksums to compare)
        if remote_checksum is not None and local_checksum == remote_checksum:
            logger.debug(f"Workspace {workspace_id} unchanged, skipping download")
            return SyncDownResult(skipped=True, reason="unchanged")

        # 4. Get presigned URL
        url_response = await client.workspaces.get_download_url(workspace_id, workspace_directory=workspace_directory)

        # 5. Download archive - handle 404 as empty workspace
        try:
            logger.info(f"Downloading workspace {workspace_id}")
            archive_data = await download_from_presigned_url(url_response.url)
        except WorkspaceNotFoundError:
            logger.info(f"Workspace {workspace_id} archive not found - treating as empty")
            return SyncDownResult(
                skipped=False,
                reason="empty_workspace",
                files_extracted=0,
                manifest_pending=False,
            )

        # 6. Extract to filesystem
        try:
            result = await extract_archive(archive_data, local_path)
            logger.info(f"Extracted {result.files_count} files to {local_path}")
        except CorruptArchiveError as e:
            logger.error(f"Corrupt archive for workspace {workspace_id}: {e}")
            raise

        # 7. Schedule background sync-complete (NON-BLOCKING)
        sync_id = str(uuid.uuid4())
        task = asyncio.create_task(
            self._background_sync_complete(
                workspace_id=workspace_id,
                local_path=local_path,
                sync_id=sync_id,
                direction="DOWN",
                workspace_directory=workspace_directory,
                archive_checksum=remote_checksum,
                archive_size_bytes=len(archive_data),
            )
        )
        self._background_tasks.append(task)

        # Return immediately - agent can start now
        return SyncDownResult(
            skipped=False,
            files_extracted=result.files_count,
            manifest_pending=True,
        )

    async def sync_up(
        self,
        workspace_id: str,
        local_path: Path | None = None,
        workspace_directory: WorkspaceDirectory = "ROOT",
    ) -> SyncUpResult:
        """
        Upload workspace to GCS if changed.

        Flow:
        1. Build manifest with dirty detection
           - Stat scan all files, compare mtime to cache
           - If no changes → return skipped=True (~10ms)
        2. For changed files: read, hash, build full manifest
        3. Create tar.zst archive
        4. POST /workspaces/{id}/upload-url → get presigned URL
        5. Upload archive via presigned URL
        6. POST /workspaces/{id}/sync-complete with manifest
        7. Update local caches
        8. Return result

        WARNING: sync_up CANNOT be async/background because:
        - Agent completed → results need to be persisted
        - If pod dies before upload → DATA LOSS
        - Caller needs confirmation that sync succeeded

        Args:
            workspace_id: ID of the workspace to sync
            local_path: Optional override for local workspace path
            workspace_directory: The directory to sync (ROOT or DOT_CLAUDE)

        Returns:
            SyncUpResult with sync status
        """
        local_path = local_path or self._get_workspace_path(workspace_id, workspace_directory)

        if not local_path.exists():
            logger.warning(f"Workspace path {local_path} does not exist")
            return SyncUpResult(skipped=True, reason="no_workspace")

        client = self._get_client()

        # 1. Check for changes using manifest builder
        manifest_builder = WorkspaceManifest(local_path, self._skip_patterns)
        manifest_result = await manifest_builder.check_dirty_and_build()

        # Fast path: nothing changed
        if not manifest_result.is_dirty and manifest_result.from_cache:
            logger.debug(f"Workspace {workspace_id} unchanged, skipping upload")
            return SyncUpResult(skipped=True, reason="unchanged")

        # Validate manifest size before proceeding
        if workspace_directory == "ROOT":
            try:
                validate_manifest_size(manifest_result.entries)
            except ManifestTooLargeError as e:
                logger.error(f"Workspace {workspace_id} manifest too large: {e}")
                raise

        # 2. Create archive
        logger.info(f"Creating archive for workspace {workspace_id}")
        archive_result: ArchiveResult = await create_archive(local_path, self._skip_patterns)

        # 3. Get presigned URL
        url_response = await client.workspaces.get_upload_url(workspace_id, workspace_directory=workspace_directory)

        # 4. Upload archive
        logger.info(f"Uploading {archive_result.size_bytes} bytes to GCS")
        await upload_to_presigned_url(url_response.url, archive_result.data)

        # 5. Complete sync
        sync_id = str(uuid.uuid4())
        files_payload = []
        if workspace_directory == "ROOT":
            files_payload = self._build_files_payload(manifest_result.entries)

        await self._call_sync_complete(
            workspace_id=workspace_id,
            sync_id=sync_id,
            direction="UP",
            status="SUCCESS",
            workspace_directory=workspace_directory,
            archive_size_bytes=archive_result.size_bytes,
            archive_checksum=archive_result.checksum,
            files=files_payload,
        )

        # 6. Update local cache
        sync_cache = SyncCache(local_path)
        sync_cache.set_archive_checksum(archive_result.checksum)

        return SyncUpResult(
            skipped=False,
            files_uploaded=len(manifest_result.entries),
            archive_size_bytes=archive_result.size_bytes,
        )

    def _build_files_payload(self, entries: list[ManifestEntry]) -> list[WorkspaceFileParam]:
        """Convert ManifestEntry list to API payload format."""
        return [
            WorkspaceFileParam(
                path=e.path,
                is_directory=e.is_directory,
                size_bytes=e.size_bytes,
                checksum=e.checksum,
                mime_type=e.mime_type,
                modified_at=e.modified_at.isoformat(),
                content=e.content,
                is_binary=e.is_binary,
                content_truncated=e.content_truncated,
            )
            for e in entries
        ]

    async def _background_sync_complete(
        self,
        workspace_id: str,
        local_path: Path,
        sync_id: str,
        direction: str,
        workspace_directory: WorkspaceDirectory,
        archive_checksum: str | None,
        archive_size_bytes: int,
    ) -> None:
        """
        Background task to build manifest and notify nucleus.

        Errors are logged but don't fail - agent is already running.
        """
        try:
            # Build manifest
            manifest_builder = WorkspaceManifest(local_path, self._skip_patterns)
            manifest_result = await manifest_builder.check_dirty_and_build()

            files_payload = []
            if workspace_directory == "ROOT":
                # Validate manifest size before sending
                try:
                    validate_manifest_size(manifest_result.entries)
                except ManifestTooLargeError as e:
                    logger.warning(f"Workspace {workspace_id} manifest too large, skipping sync-complete: {e}")
                    return

                files_payload = self._build_files_payload(manifest_result.entries)

            # Notify nucleus
            await self._call_sync_complete(
                workspace_id=workspace_id,
                sync_id=sync_id,
                direction=direction,
                status="SUCCESS",
                workspace_directory=workspace_directory,
                archive_size_bytes=archive_size_bytes,
                archive_checksum=archive_checksum,
                files=files_payload,
            )

            # Update local cache
            sync_cache = SyncCache(local_path)
            if archive_checksum:
                sync_cache.set_archive_checksum(archive_checksum)

            logger.debug(f"Background sync-complete finished for {workspace_id}")

        except httpx.TimeoutException:
            logger.warning(
                f"Background sync-complete timed out for {workspace_id} (manifest not stored, will retry on next sync)"
            )
        except httpx.HTTPStatusError as e:
            logger.warning(
                f"Background sync-complete HTTP error for {workspace_id}: "
                f"{e.response.status_code} - {e.response.text[:200]}"
            )
        except Exception as e:
            # Log unexpected errors at ERROR level for visibility
            logger.error(
                f"Background sync-complete failed unexpectedly for {workspace_id}: {e}",
                exc_info=True,
            )

    @retry(**SYNC_COMPLETE_RETRY_CONFIG)
    async def _call_sync_complete(
        self,
        workspace_id: str,
        sync_id: str,
        direction: str,
        status: str,
        workspace_directory: WorkspaceDirectory,
        archive_size_bytes: int | None,
        archive_checksum: str | None,
        files: list[WorkspaceFileParam],
    ) -> None:
        """
        Call POST /workspaces/{id}/sync-complete via generated SDK with retry.

        Retries once on transient network failures (TimeoutException, ConnectError).
        """
        client = self._get_client()

        await client.workspaces.sync_complete(
            workspace_id,
            sync_id=sync_id,
            direction=direction,
            status=status,
            workspace_directory=workspace_directory,
            archive_size_bytes=archive_size_bytes,
            archive_checksum=archive_checksum,
            files=files,
        )

    async def wait_for_background_tasks(self, timeout: float = 30.0) -> None:
        """
        Wait for background sync-complete tasks to finish.

        Call on graceful shutdown to ensure all manifests are stored.

        Args:
            timeout: Maximum time to wait for background tasks
        """
        if not self._background_tasks:
            return

        _, pending = await asyncio.wait(
            self._background_tasks,
            timeout=timeout,
        )

        for task in pending:
            logger.warning("Cancelling pending background sync task")
            task.cancel()

        self._background_tasks.clear()


# Singleton instance for ADK usage
workspace = WorkspaceModule()
