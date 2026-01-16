"""
Tests for WorkspaceModule high-level sync operations.

These tests use real filesystem operations with temporary directories.
HTTP calls to the API and presigned URLs are mocked at the boundary.
"""

from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass
from unittest.mock import AsyncMock, patch

import httpx
import pytest

# Import the workspace module directly
from sb0.lib.adk._modules import workspace as workspace_module

# Import directly from the module files to avoid circular import through adk/__init__.py
# which has a long import chain that requires the 'agents' package
from sb0.lib.utils.workspace_archive import (
    CorruptArchiveError,
    WorkspaceNotFoundError,
    create_archive,
)
from sb0.lib.utils.workspace_manifest import SyncCache

WorkspaceModule = workspace_module.WorkspaceModule
SyncDownResult = workspace_module.SyncDownResult
SyncUpResult = workspace_module.SyncUpResult


@dataclass
class MockWorkspaceResponse:
    """Mock response from workspaces.retrieve()."""

    id: str
    archive_checksum: str | None = None


@dataclass
class MockPresignedURLResponse:
    """Mock response from get_upload_url/get_download_url."""

    url: str


class TestSyncDownSkipPath:
    """Tests for sync_down skip optimization."""

    async def test_skip_when_checksum_matches(self, tmp_path: Path) -> None:
        """sync_down should skip download when checksums match."""
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()

        # Set up local cache with checksum
        sync_cache = SyncCache(workspace_dir)
        sync_cache.set_archive_checksum("sha256:matching_checksum")

        # Mock client
        mock_client = AsyncMock()
        mock_client.workspaces.retrieve.return_value = MockWorkspaceResponse(
            id="ws-123",
            archive_checksum="sha256:matching_checksum",
        )

        module = WorkspaceModule(client=mock_client, local_workspace_path=workspace_dir)
        result = await module.sync_down("ws-123")

        assert result.skipped is True
        assert result.reason == "unchanged"
        # Should not call download URL
        mock_client.workspaces.get_download_url.assert_not_called()

    async def test_no_skip_when_checksum_differs(self, tmp_path: Path) -> None:
        """sync_down should download when checksums differ."""
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()

        # Set up local cache with OLD checksum
        sync_cache = SyncCache(workspace_dir)
        sync_cache.set_archive_checksum("sha256:old_checksum")

        # Create a valid archive to return
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        (source_dir / "file.txt").write_text("remote content")
        archive_result = await create_archive(source_dir, skip_patterns=[])

        # Mock client
        mock_client = AsyncMock()
        mock_client.workspaces.retrieve.return_value = MockWorkspaceResponse(
            id="ws-123",
            archive_checksum="sha256:new_checksum",
        )
        mock_client.workspaces.get_download_url.return_value = MockPresignedURLResponse(
            url="https://storage.example.com/download"
        )
        mock_client.workspaces.sync_complete.return_value = None

        module = WorkspaceModule(client=mock_client, local_workspace_path=workspace_dir)

        # Mock the HTTP download
        with patch(
            "sb0.lib.adk._modules.workspace.download_from_presigned_url",
            new_callable=AsyncMock,
            return_value=archive_result.data,
        ):
            result = await module.sync_down("ws-123")

        assert result.skipped is False
        assert result.files_extracted == 1
        assert (workspace_dir / "file.txt").read_text() == "remote content"

    async def test_no_skip_when_no_local_cache(self, tmp_path: Path) -> None:
        """sync_down should download when no local cache exists."""
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()
        # No cache set up

        # Create archive
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        (source_dir / "data.txt").write_text("fresh data")
        archive_result = await create_archive(source_dir, skip_patterns=[])

        mock_client = AsyncMock()
        mock_client.workspaces.retrieve.return_value = MockWorkspaceResponse(
            id="ws-123",
            archive_checksum="sha256:some_checksum",
        )
        mock_client.workspaces.get_download_url.return_value = MockPresignedURLResponse(
            url="https://storage.example.com/download"
        )
        mock_client.workspaces.sync_complete.return_value = None

        module = WorkspaceModule(client=mock_client, local_workspace_path=workspace_dir)

        with patch(
            "sb0.lib.adk._modules.workspace.download_from_presigned_url",
            new_callable=AsyncMock,
            return_value=archive_result.data,
        ):
            result = await module.sync_down("ws-123")

        assert result.skipped is False
        assert (workspace_dir / "data.txt").exists()


class TestSyncDown404Handling:
    """Tests for sync_down handling of missing archives (404)."""

    async def test_empty_workspace_on_404(self, tmp_path: Path) -> None:
        """sync_down should return empty workspace when archive not found."""
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()

        mock_client = AsyncMock()
        mock_client.workspaces.retrieve.return_value = MockWorkspaceResponse(
            id="ws-123",
            archive_checksum=None,  # No archive yet
        )
        mock_client.workspaces.get_download_url.return_value = MockPresignedURLResponse(
            url="https://storage.example.com/nonexistent"
        )

        module = WorkspaceModule(client=mock_client, local_workspace_path=workspace_dir)

        with patch(
            "sb0.lib.adk._modules.workspace.download_from_presigned_url",
            new_callable=AsyncMock,
            side_effect=WorkspaceNotFoundError("Not found"),
        ):
            result = await module.sync_down("ws-123")

        assert result.skipped is False
        assert result.reason == "empty_workspace"
        assert result.files_extracted == 0


class TestSyncDownExtraction:
    """Tests for sync_down file extraction."""

    async def test_extracts_files_correctly(self, tmp_path: Path) -> None:
        """sync_down should extract all files to workspace directory."""
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()

        # Create archive with multiple files
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        (source_dir / "src").mkdir()
        (source_dir / "src" / "main.py").write_text("print('hello')")
        (source_dir / "README.md").write_text("# Project")
        archive_result = await create_archive(source_dir, skip_patterns=[])

        mock_client = AsyncMock()
        mock_client.workspaces.retrieve.return_value = MockWorkspaceResponse(id="ws-123", archive_checksum="sha256:abc")
        mock_client.workspaces.get_download_url.return_value = MockPresignedURLResponse(
            url="https://storage.example.com/download"
        )
        mock_client.workspaces.sync_complete.return_value = None

        module = WorkspaceModule(client=mock_client, local_workspace_path=workspace_dir)

        with patch(
            "sb0.lib.adk._modules.workspace.download_from_presigned_url",
            new_callable=AsyncMock,
            return_value=archive_result.data,
        ):
            result = await module.sync_down("ws-123")

        assert result.files_extracted == 2
        assert (workspace_dir / "src" / "main.py").read_text() == "print('hello')"
        assert (workspace_dir / "README.md").read_text() == "# Project"

    async def test_corrupt_archive_raises(self, tmp_path: Path) -> None:
        """sync_down should raise on corrupt archive."""
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()

        mock_client = AsyncMock()
        mock_client.workspaces.retrieve.return_value = MockWorkspaceResponse(id="ws-123", archive_checksum="sha256:abc")
        mock_client.workspaces.get_download_url.return_value = MockPresignedURLResponse(
            url="https://storage.example.com/download"
        )

        module = WorkspaceModule(client=mock_client, local_workspace_path=workspace_dir)

        # Return invalid data
        with patch(
            "sb0.lib.adk._modules.workspace.download_from_presigned_url",
            new_callable=AsyncMock,
            return_value=b"not a valid archive",
        ):
            with pytest.raises(CorruptArchiveError):
                await module.sync_down("ws-123")


class TestSyncUpSkipPath:
    """Tests for sync_up skip optimization."""

    async def test_skip_when_no_changes(self, tmp_path: Path) -> None:
        """sync_up should skip when no files have changed."""
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()
        (workspace_dir / "file.txt").write_text("content")

        mock_client = AsyncMock()
        module = WorkspaceModule(client=mock_client, local_workspace_path=workspace_dir)

        # First sync to populate cache
        mock_client.workspaces.get_upload_url.return_value = MockPresignedURLResponse(
            url="https://storage.example.com/upload"
        )
        mock_client.workspaces.sync_complete.return_value = None

        with patch(
            "sb0.lib.adk._modules.workspace.upload_to_presigned_url",
            new_callable=AsyncMock,
        ):
            await module.sync_up("ws-123")

        # Reset mock
        mock_client.reset_mock()

        # Second sync - should skip
        result = await module.sync_up("ws-123")

        assert result.skipped is True
        assert result.reason == "unchanged"
        mock_client.workspaces.get_upload_url.assert_not_called()

    async def test_no_skip_when_file_modified(self, tmp_path: Path) -> None:
        """sync_up should upload when files have changed."""
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()
        test_file = workspace_dir / "file.txt"
        test_file.write_text("original")

        mock_client = AsyncMock()
        mock_client.workspaces.get_upload_url.return_value = MockPresignedURLResponse(
            url="https://storage.example.com/upload"
        )
        mock_client.workspaces.sync_complete.return_value = None

        module = WorkspaceModule(client=mock_client, local_workspace_path=workspace_dir)

        with patch(
            "sb0.lib.adk._modules.workspace.upload_to_presigned_url",
            new_callable=AsyncMock,
        ):
            # First sync
            await module.sync_up("ws-123")

        mock_client.reset_mock()
        mock_client.workspaces.get_upload_url.return_value = MockPresignedURLResponse(
            url="https://storage.example.com/upload"
        )
        mock_client.workspaces.sync_complete.return_value = None

        # Modify file
        import time

        time.sleep(0.01)
        test_file.write_text("modified")

        with patch(
            "sb0.lib.adk._modules.workspace.upload_to_presigned_url",
            new_callable=AsyncMock,
        ):
            result = await module.sync_up("ws-123")

        assert result.skipped is False
        mock_client.workspaces.get_upload_url.assert_called_once()

    async def test_skip_when_workspace_missing(self, tmp_path: Path) -> None:
        """sync_up should skip when workspace directory doesn't exist."""
        workspace_dir = tmp_path / "nonexistent"
        # Don't create it

        mock_client = AsyncMock()
        module = WorkspaceModule(client=mock_client, local_workspace_path=workspace_dir)

        result = await module.sync_up("ws-123")

        assert result.skipped is True
        assert result.reason == "no_workspace"


class TestSyncUpUpload:
    """Tests for sync_up archive upload."""

    async def test_uploads_archive_to_presigned_url(self, tmp_path: Path) -> None:
        """sync_up should create archive and upload to presigned URL."""
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()
        (workspace_dir / "main.py").write_text("print('hello')")

        mock_client = AsyncMock()
        mock_client.workspaces.get_upload_url.return_value = MockPresignedURLResponse(
            url="https://storage.example.com/upload"
        )
        mock_client.workspaces.sync_complete.return_value = None

        module = WorkspaceModule(client=mock_client, local_workspace_path=workspace_dir)

        uploaded_data = None

        async def capture_upload(url: str, data: bytes, **kwargs) -> None:
            nonlocal uploaded_data
            uploaded_data = data

        with patch(
            "sb0.lib.adk._modules.workspace.upload_to_presigned_url",
            new_callable=AsyncMock,
            side_effect=capture_upload,
        ):
            result = await module.sync_up("ws-123")

        assert result.skipped is False
        assert result.files_uploaded == 1
        assert uploaded_data is not None
        # Verify it's a valid zstd archive (magic bytes)
        assert uploaded_data[:4] == b"\x28\xb5\x2f\xfd"

    async def test_calls_sync_complete_with_manifest(self, tmp_path: Path) -> None:
        """sync_up should call sync_complete with file manifest."""
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()
        (workspace_dir / "file.py").write_text("code")

        mock_client = AsyncMock()
        mock_client.workspaces.get_upload_url.return_value = MockPresignedURLResponse(
            url="https://storage.example.com/upload"
        )
        mock_client.workspaces.sync_complete.return_value = None

        module = WorkspaceModule(client=mock_client, local_workspace_path=workspace_dir)

        with patch(
            "sb0.lib.adk._modules.workspace.upload_to_presigned_url",
            new_callable=AsyncMock,
        ):
            await module.sync_up("ws-123")

        # Verify sync_complete was called
        mock_client.workspaces.sync_complete.assert_called_once()
        call_kwargs = mock_client.workspaces.sync_complete.call_args.kwargs

        assert call_kwargs["direction"] == "UP"
        assert call_kwargs["status"] == "SUCCESS"
        assert "archive_checksum" in call_kwargs
        assert "files" in call_kwargs
        assert len(call_kwargs["files"]) == 1

    async def test_updates_local_cache_after_upload(self, tmp_path: Path) -> None:
        """sync_up should update local sync cache after successful upload."""
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()
        (workspace_dir / "file.txt").write_text("content")

        mock_client = AsyncMock()
        mock_client.workspaces.get_upload_url.return_value = MockPresignedURLResponse(
            url="https://storage.example.com/upload"
        )
        mock_client.workspaces.sync_complete.return_value = None

        module = WorkspaceModule(client=mock_client, local_workspace_path=workspace_dir)

        with patch(
            "sb0.lib.adk._modules.workspace.upload_to_presigned_url",
            new_callable=AsyncMock,
        ):
            await module.sync_up("ws-123")

        # Verify cache was updated
        sync_cache = SyncCache(workspace_dir)
        assert sync_cache.get_archive_checksum() is not None
        assert sync_cache.get_archive_checksum().startswith("sha256:")


class TestBackgroundTasks:
    """Tests for background task handling."""

    async def test_wait_for_background_tasks(self, tmp_path: Path) -> None:
        """wait_for_background_tasks should wait for pending tasks."""
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()
        (workspace_dir / "file.txt").write_text("content")

        # Create archive for download
        archive_result = await create_archive(workspace_dir, skip_patterns=[])

        mock_client = AsyncMock()
        mock_client.workspaces.retrieve.return_value = MockWorkspaceResponse(id="ws-123", archive_checksum="sha256:abc")
        mock_client.workspaces.get_download_url.return_value = MockPresignedURLResponse(
            url="https://storage.example.com/download"
        )
        mock_client.workspaces.sync_complete.return_value = None

        module = WorkspaceModule(client=mock_client, local_workspace_path=workspace_dir)

        with patch(
            "sb0.lib.adk._modules.workspace.download_from_presigned_url",
            new_callable=AsyncMock,
            return_value=archive_result.data,
        ):
            result = await module.sync_down("ws-123")

        # Background task should be pending
        assert result.manifest_pending is True
        assert len(module._background_tasks) == 1

        # Wait for tasks
        await module.wait_for_background_tasks(timeout=5.0)

        # Tasks should be cleared
        assert len(module._background_tasks) == 0

    async def test_background_task_errors_logged_not_raised(self, tmp_path: Path) -> None:
        """Background task errors should be logged but not raised."""
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()
        (workspace_dir / "file.txt").write_text("content")

        archive_result = await create_archive(workspace_dir, skip_patterns=[])

        mock_client = AsyncMock()
        mock_client.workspaces.retrieve.return_value = MockWorkspaceResponse(id="ws-123", archive_checksum="sha256:abc")
        mock_client.workspaces.get_download_url.return_value = MockPresignedURLResponse(
            url="https://storage.example.com/download"
        )
        # Make sync_complete fail
        mock_client.workspaces.sync_complete.side_effect = httpx.TimeoutException("timeout")

        module = WorkspaceModule(client=mock_client, local_workspace_path=workspace_dir)

        with patch(
            "sb0.lib.adk._modules.workspace.download_from_presigned_url",
            new_callable=AsyncMock,
            return_value=archive_result.data,
        ):
            # sync_down should succeed even though background task will fail
            result = await module.sync_down("ws-123")

        assert result.skipped is False

        # Wait for background task (should not raise)
        await module.wait_for_background_tasks(timeout=5.0)


class TestWorkspacePathResolution:
    """Tests for workspace path resolution logic."""

    async def test_uses_provided_local_path(self, tmp_path: Path) -> None:
        """Should use local_workspace_path when provided."""
        custom_path = tmp_path / "custom"
        custom_path.mkdir()
        (custom_path / "file.txt").write_text("custom content")

        mock_client = AsyncMock()
        mock_client.workspaces.get_upload_url.return_value = MockPresignedURLResponse(
            url="https://storage.example.com/upload"
        )
        mock_client.workspaces.sync_complete.return_value = None

        module = WorkspaceModule(client=mock_client, local_workspace_path=custom_path)

        with patch(
            "sb0.lib.adk._modules.workspace.upload_to_presigned_url",
            new_callable=AsyncMock,
        ):
            result = await module.sync_up("ws-123")

        assert result.skipped is False
        assert result.files_uploaded == 1

    async def test_uses_override_path_in_method(self, tmp_path: Path) -> None:
        """Should use local_path parameter when provided to method."""
        default_path = tmp_path / "default"
        default_path.mkdir()
        override_path = tmp_path / "override"
        override_path.mkdir()
        (override_path / "override.txt").write_text("override content")

        mock_client = AsyncMock()
        mock_client.workspaces.get_upload_url.return_value = MockPresignedURLResponse(
            url="https://storage.example.com/upload"
        )
        mock_client.workspaces.sync_complete.return_value = None

        module = WorkspaceModule(client=mock_client, local_workspace_path=default_path)

        with patch(
            "sb0.lib.adk._modules.workspace.upload_to_presigned_url",
            new_callable=AsyncMock,
        ):
            result = await module.sync_up("ws-123", local_path=override_path)

        assert result.files_uploaded == 1


class TestRoundTripIntegration:
    """Integration tests for full sync_down -> modify -> sync_up cycle."""

    async def test_full_round_trip(self, tmp_path: Path) -> None:
        """Full cycle: sync_down, modify files, sync_up."""
        # Set up source workspace
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        (source_dir / "original.txt").write_text("original content")
        original_archive = await create_archive(source_dir, skip_patterns=[])

        # Workspace directory
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()

        mock_client = AsyncMock()

        # Step 1: sync_down
        mock_client.workspaces.retrieve.return_value = MockWorkspaceResponse(
            id="ws-123", archive_checksum="sha256:original"
        )
        mock_client.workspaces.get_download_url.return_value = MockPresignedURLResponse(
            url="https://storage.example.com/download"
        )
        mock_client.workspaces.sync_complete.return_value = None

        module = WorkspaceModule(client=mock_client, local_workspace_path=workspace_dir)

        with patch(
            "sb0.lib.adk._modules.workspace.download_from_presigned_url",
            new_callable=AsyncMock,
            return_value=original_archive.data,
        ):
            down_result = await module.sync_down("ws-123")

        assert down_result.files_extracted == 1
        assert (workspace_dir / "original.txt").exists()

        # Wait for background task
        await module.wait_for_background_tasks()

        # Step 2: Modify files
        import time

        time.sleep(0.01)
        (workspace_dir / "original.txt").write_text("modified content")
        (workspace_dir / "new_file.txt").write_text("new file")

        # Step 3: sync_up
        mock_client.reset_mock()
        mock_client.workspaces.get_upload_url.return_value = MockPresignedURLResponse(
            url="https://storage.example.com/upload"
        )
        mock_client.workspaces.sync_complete.return_value = None

        uploaded_archive = None

        async def capture_upload(url: str, data: bytes, **kwargs) -> None:
            nonlocal uploaded_archive
            uploaded_archive = data

        with patch(
            "sb0.lib.adk._modules.workspace.upload_to_presigned_url",
            new_callable=AsyncMock,
            side_effect=capture_upload,
        ):
            up_result = await module.sync_up("ws-123")

        assert up_result.skipped is False
        assert up_result.files_uploaded == 2

        # Verify uploaded archive contains both files
        from sb0.lib.utils.workspace_archive import extract_archive

        verify_dir = tmp_path / "verify"
        verify_dir.mkdir()
        await extract_archive(uploaded_archive, verify_dir)

        assert (verify_dir / "original.txt").read_text() == "modified content"
        assert (verify_dir / "new_file.txt").read_text() == "new file"
