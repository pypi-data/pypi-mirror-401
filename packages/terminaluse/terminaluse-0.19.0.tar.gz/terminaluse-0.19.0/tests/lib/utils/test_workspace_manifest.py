"""
Tests for workspace manifest building with mtime-based dirty detection.

These tests use real filesystem operations with temporary directories.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from datetime import datetime, timezone

import pytest

from sb0.lib.utils.workspace_manifest import (
    MAX_FILE_COUNT,
    MAX_CONTENT_SIZE,
    MAX_PAYLOAD_SIZE,
    SyncCache,
    ManifestEntry,
    WorkspaceManifest,
    ManifestTooLargeError,
    _is_text_file,
    validate_manifest_size,
)


class TestDirtyDetection:
    """Tests for mtime-based dirty detection."""

    async def test_initial_scan_is_dirty(self, tmp_path: Path) -> None:
        """First scan should always report dirty (no cache)."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        (workspace / "file.txt").write_text("content")

        manifest = WorkspaceManifest(workspace)
        result = await manifest.check_dirty_and_build()

        assert result.is_dirty is True
        assert result.from_cache is False
        assert len(result.entries) == 1

    async def test_unchanged_files_not_dirty(self, tmp_path: Path) -> None:
        """Second scan with no changes should report not dirty."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        (workspace / "file.txt").write_text("content")

        manifest = WorkspaceManifest(workspace)

        # First scan - populates cache
        result1 = await manifest.check_dirty_and_build()
        assert result1.is_dirty is True

        # Second scan - should use cache
        result2 = await manifest.check_dirty_and_build()
        assert result2.is_dirty is False
        assert result2.from_cache is True

    async def test_modified_file_is_dirty(self, tmp_path: Path) -> None:
        """Modified file should be detected as dirty."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        test_file = workspace / "file.txt"
        test_file.write_text("original content")

        manifest = WorkspaceManifest(workspace)
        await manifest.check_dirty_and_build()

        # Modify the file (need to ensure mtime changes)
        time.sleep(0.01)  # Ensure mtime difference
        test_file.write_text("modified content")

        result = await manifest.check_dirty_and_build()
        assert result.is_dirty is True

    async def test_new_file_is_dirty(self, tmp_path: Path) -> None:
        """Adding a new file should be detected as dirty."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        (workspace / "existing.txt").write_text("existing")

        manifest = WorkspaceManifest(workspace)
        await manifest.check_dirty_and_build()

        # Add new file
        (workspace / "new_file.txt").write_text("new content")

        result = await manifest.check_dirty_and_build()
        assert result.is_dirty is True
        assert len(result.entries) == 2

    async def test_deleted_file_is_dirty(self, tmp_path: Path) -> None:
        """Deleting a file should be detected as dirty."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        file_to_delete = workspace / "to_delete.txt"
        file_to_delete.write_text("will be deleted")
        (workspace / "keep.txt").write_text("keep this")

        manifest = WorkspaceManifest(workspace)
        await manifest.check_dirty_and_build()
        assert len(manifest._cache) == 2

        # Delete file
        file_to_delete.unlink()

        result = await manifest.check_dirty_and_build()
        assert result.is_dirty is True
        assert len(result.entries) == 1
        assert result.entries[0].path == "keep.txt"


class TestCachePersistence:
    """Tests for cache persistence across WorkspaceManifest instances."""

    async def test_cache_persists_to_file(self, tmp_path: Path) -> None:
        """Cache should be saved to .sb_manifest_cache.json."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        (workspace / "file.txt").write_text("content")

        manifest = WorkspaceManifest(workspace)
        await manifest.check_dirty_and_build()

        cache_file = workspace / ".sb_manifest_cache.json"
        assert cache_file.exists()

        cache_data = json.loads(cache_file.read_text())
        assert "version" in cache_data
        assert "entries" in cache_data
        assert "file.txt" in cache_data["entries"]

    async def test_cache_loaded_by_new_instance(self, tmp_path: Path) -> None:
        """New WorkspaceManifest instance should load existing cache."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        (workspace / "file.txt").write_text("content")

        # First instance creates cache
        manifest1 = WorkspaceManifest(workspace)
        await manifest1.check_dirty_and_build()

        # Second instance should load cache
        manifest2 = WorkspaceManifest(workspace)
        result = await manifest2.check_dirty_and_build()

        assert result.is_dirty is False
        assert result.from_cache is True

    async def test_corrupted_cache_ignored(self, tmp_path: Path) -> None:
        """Corrupted cache file should be ignored gracefully."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        (workspace / "file.txt").write_text("content")

        # Write invalid cache
        cache_file = workspace / ".sb_manifest_cache.json"
        cache_file.write_text("not valid json {{{")

        manifest = WorkspaceManifest(workspace)
        result = await manifest.check_dirty_and_build()

        # Should rebuild from scratch
        assert result.is_dirty is True
        assert len(result.entries) == 1

    async def test_version_mismatch_rebuilds(self, tmp_path: Path) -> None:
        """Cache with wrong version should trigger rebuild."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        (workspace / "file.txt").write_text("content")

        # Write cache with old version
        cache_file = workspace / ".sb_manifest_cache.json"
        cache_file.write_text(json.dumps({"version": 0, "entries": {}}))

        manifest = WorkspaceManifest(workspace)
        result = await manifest.check_dirty_and_build()

        assert result.is_dirty is True


class TestBinaryDetection:
    """Tests for binary vs text file detection."""

    def test_python_file_is_text(self) -> None:
        """Python files should be detected as text."""
        assert _is_text_file(Path("main.py"), b"print('hello')") is True

    def test_javascript_file_is_text(self) -> None:
        """JavaScript files should be detected as text."""
        assert _is_text_file(Path("app.js"), b"console.log('hello')") is True

    def test_typescript_file_is_text(self) -> None:
        """TypeScript files should be detected as text."""
        assert _is_text_file(Path("app.ts"), b"const x: number = 1") is True
        assert _is_text_file(Path("component.tsx"), b"<div>hello</div>") is True

    def test_markdown_file_is_text(self) -> None:
        """Markdown files should be detected as text."""
        assert _is_text_file(Path("README.md"), b"# Title") is True

    def test_json_file_is_text(self) -> None:
        """JSON files should be detected as text."""
        assert _is_text_file(Path("config.json"), b'{"key": "value"}') is True

    def test_yaml_file_is_text(self) -> None:
        """YAML files should be detected as text."""
        assert _is_text_file(Path("config.yml"), b"key: value") is True
        assert _is_text_file(Path("config.yaml"), b"key: value") is True

    def test_makefile_is_text(self) -> None:
        """Makefile should be detected as text."""
        assert _is_text_file(Path("Makefile"), b"all: build") is True
        assert _is_text_file(Path("makefile"), b"all: build") is True

    def test_dockerfile_is_text(self) -> None:
        """Dockerfile should be detected as text."""
        assert _is_text_file(Path("Dockerfile"), b"FROM python:3.12") is True

    def test_binary_file_with_null_bytes(self) -> None:
        """Files with null bytes should be detected as binary."""
        binary_content = b"\x00\x01\x02\x03"
        assert _is_text_file(Path("unknown.dat"), binary_content) is False

    def test_png_file_is_binary(self) -> None:
        """PNG files should be detected as binary."""
        png_header = b"\x89PNG\r\n\x1a\n\x00\x00\x00"
        assert _is_text_file(Path("image.png"), png_header) is False

    def test_unknown_extension_text_content(self) -> None:
        """Unknown extension with text content should be detected as text."""
        assert _is_text_file(Path("file.xyz"), b"just plain text") is True

    def test_unknown_extension_binary_content(self) -> None:
        """Unknown extension with binary content should be detected as binary."""
        assert _is_text_file(Path("file.xyz"), b"text with \x00 null") is False


class TestManifestContent:
    """Tests for manifest entry content handling."""

    async def test_text_file_content_included(self, tmp_path: Path) -> None:
        """Text file content should be included in manifest."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        (workspace / "file.py").write_text("print('hello')")

        manifest = WorkspaceManifest(workspace)
        result = await manifest.check_dirty_and_build()

        entry = result.entries[0]
        assert entry.content == "print('hello')"
        assert entry.is_binary is False
        assert entry.content_truncated is False

    async def test_binary_file_no_content(self, tmp_path: Path) -> None:
        """Binary file content should not be included."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        (workspace / "data.bin").write_bytes(b"\x00\x01\x02\x03")

        manifest = WorkspaceManifest(workspace)
        result = await manifest.check_dirty_and_build()

        entry = result.entries[0]
        assert entry.content is None
        assert entry.is_binary is True

    async def test_large_file_truncated(self, tmp_path: Path) -> None:
        """Files larger than MAX_CONTENT_SIZE should be truncated."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()

        # Create file larger than MAX_CONTENT_SIZE
        large_content = "x" * (MAX_CONTENT_SIZE + 1000)
        (workspace / "large.txt").write_text(large_content)

        manifest = WorkspaceManifest(workspace)
        result = await manifest.check_dirty_and_build()

        entry = result.entries[0]
        assert entry.content_truncated is True
        assert len(entry.content) <= MAX_CONTENT_SIZE

    async def test_checksum_format(self, tmp_path: Path) -> None:
        """Checksum should be in sha256:hex format."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        (workspace / "file.txt").write_text("content")

        manifest = WorkspaceManifest(workspace)
        result = await manifest.check_dirty_and_build()

        entry = result.entries[0]
        assert entry.checksum.startswith("sha256:")

    async def test_modified_at_is_utc(self, tmp_path: Path) -> None:
        """Modified timestamp should be UTC timezone-aware."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        (workspace / "file.txt").write_text("content")

        manifest = WorkspaceManifest(workspace)
        result = await manifest.check_dirty_and_build()

        entry = result.entries[0]
        assert entry.modified_at.tzinfo == timezone.utc


class TestSkipPatterns:
    """Tests for skip pattern handling in manifest builder."""

    async def test_skip_git_directory(self, tmp_path: Path) -> None:
        """.git should be skipped."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        (workspace / ".git").mkdir()
        (workspace / ".git" / "config").write_text("git config")
        (workspace / "main.py").write_text("code")

        manifest = WorkspaceManifest(workspace)
        result = await manifest.check_dirty_and_build()

        assert len(result.entries) == 1
        assert result.entries[0].path == "main.py"

    async def test_skip_cache_files(self, tmp_path: Path) -> None:
        """Manifest cache files should be skipped."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        (workspace / ".sb_manifest_cache.json").write_text("{}")
        (workspace / ".sb_sync_cache.json").write_text("{}")
        (workspace / "real.txt").write_text("real")

        manifest = WorkspaceManifest(workspace)
        result = await manifest.check_dirty_and_build()

        assert len(result.entries) == 1
        assert result.entries[0].path == "real.txt"

    async def test_custom_skip_patterns(self, tmp_path: Path) -> None:
        """Custom skip patterns should be respected."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        (workspace / "include.txt").write_text("include")
        (workspace / "exclude_me").mkdir()
        (workspace / "exclude_me" / "file.txt").write_text("excluded")

        manifest = WorkspaceManifest(workspace, skip_patterns=["exclude_me"])
        result = await manifest.check_dirty_and_build()

        assert len(result.entries) == 1
        assert result.entries[0].path == "include.txt"


class TestSyncCache:
    """Tests for SyncCache (archive checksum tracking)."""

    def test_empty_cache_returns_none(self, tmp_path: Path) -> None:
        """Empty cache should return None for checksum."""
        cache = SyncCache(tmp_path)
        assert cache.get_archive_checksum() is None

    def test_set_and_get_checksum(self, tmp_path: Path) -> None:
        """Should be able to set and get checksum."""
        cache = SyncCache(tmp_path)
        cache.set_archive_checksum("sha256:abc123")

        assert cache.get_archive_checksum() == "sha256:abc123"

    def test_checksum_persists_to_file(self, tmp_path: Path) -> None:
        """Checksum should be persisted to file."""
        cache = SyncCache(tmp_path)
        cache.set_archive_checksum("sha256:abc123")

        cache_file = tmp_path / ".sb_sync_cache.json"
        assert cache_file.exists()

        data = json.loads(cache_file.read_text())
        assert data["archive_checksum"] == "sha256:abc123"
        assert "last_synced_at" in data

    def test_checksum_loaded_by_new_instance(self, tmp_path: Path) -> None:
        """New instance should load existing checksum."""
        cache1 = SyncCache(tmp_path)
        cache1.set_archive_checksum("sha256:abc123")

        cache2 = SyncCache(tmp_path)
        assert cache2.get_archive_checksum() == "sha256:abc123"

    def test_corrupted_cache_ignored(self, tmp_path: Path) -> None:
        """Corrupted cache should be ignored."""
        cache_file = tmp_path / ".sb_sync_cache.json"
        cache_file.write_text("invalid json")

        cache = SyncCache(tmp_path)
        assert cache.get_archive_checksum() is None


class TestManifestSizeValidation:
    """Tests for manifest size limit validation."""

    def test_valid_manifest_passes(self) -> None:
        """Small manifest should pass validation."""
        entries = [
            ManifestEntry(
                path="file.txt",
                is_directory=False,
                size_bytes=100,
                checksum="sha256:abc",
                mime_type="text/plain",
                modified_at=datetime.now(timezone.utc),
                content="content",
                is_binary=False,
                content_truncated=False,
            )
        ]

        # Should not raise
        validate_manifest_size(entries)

    def test_too_many_files_raises(self) -> None:
        """Exceeding MAX_FILE_COUNT should raise."""
        entries = [
            ManifestEntry(
                path=f"file_{i}.txt",
                is_directory=False,
                size_bytes=10,
                checksum="sha256:abc",
                mime_type="text/plain",
                modified_at=datetime.now(timezone.utc),
                content="x",
                is_binary=False,
            )
            for i in range(MAX_FILE_COUNT + 1)
        ]

        with pytest.raises(ManifestTooLargeError) as exc_info:
            validate_manifest_size(entries)

        assert exc_info.value.file_count == MAX_FILE_COUNT + 1

    def test_payload_too_large_raises(self) -> None:
        """Exceeding MAX_PAYLOAD_SIZE should raise."""
        # Create entry with large content
        large_content = "x" * (MAX_PAYLOAD_SIZE + 1000)
        entries = [
            ManifestEntry(
                path="large.txt",
                is_directory=False,
                size_bytes=len(large_content),
                checksum="sha256:abc",
                mime_type="text/plain",
                modified_at=datetime.now(timezone.utc),
                content=large_content,
                is_binary=False,
            )
        ]

        with pytest.raises(ManifestTooLargeError) as exc_info:
            validate_manifest_size(entries)

        assert exc_info.value.payload_size > MAX_PAYLOAD_SIZE


class TestParallelProcessing:
    """Tests for parallel file processing with large changesets."""

    async def test_large_changeset_uses_parallel(self, tmp_path: Path) -> None:
        """Changesets > 100 files should use parallel processing."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()

        # Create 150 files (above parallel threshold)
        for i in range(150):
            (workspace / f"file_{i:03d}.txt").write_text(f"content {i}")

        manifest = WorkspaceManifest(workspace)
        result = await manifest.check_dirty_and_build()

        assert len(result.entries) == 150
        # All files should have valid checksums
        for entry in result.entries:
            assert entry.checksum.startswith("sha256:")

    async def test_small_changeset_sequential(self, tmp_path: Path) -> None:
        """Small changesets should work correctly (sequential path)."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()

        for i in range(10):
            (workspace / f"file_{i}.txt").write_text(f"content {i}")

        manifest = WorkspaceManifest(workspace)
        result = await manifest.check_dirty_and_build()

        assert len(result.entries) == 10
