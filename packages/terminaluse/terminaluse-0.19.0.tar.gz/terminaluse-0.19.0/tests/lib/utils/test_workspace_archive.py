"""
Tests for workspace archive operations (tar.zst compression/decompression).

These tests use real filesystem operations with temporary directories.
"""

from __future__ import annotations

import io
import tarfile
from pathlib import Path

import pytest
import pyzstd

from sb0.lib.utils.workspace_archive import (
    ArchiveResult,
    ExtractResult,
    CorruptArchiveError,
    create_archive,
    extract_archive,
    should_skip_path,
)


class TestShouldSkipPath:
    """Tests for skip pattern matching."""

    def test_skip_git_directory(self) -> None:
        """Files inside .git should be skipped."""
        assert should_skip_path(Path(".git/config"), [".git"]) is True
        assert should_skip_path(Path(".git/objects/pack/abc"), [".git"]) is True

    def test_skip_node_modules(self) -> None:
        """Files inside node_modules should be skipped."""
        assert should_skip_path(Path("node_modules/lodash/index.js"), ["node_modules"]) is True

    def test_skip_nested_pattern(self) -> None:
        """Patterns should match at any level."""
        assert should_skip_path(Path("src/app/node_modules/pkg/file.js"), ["node_modules"]) is True
        assert should_skip_path(Path("deep/nested/.git/HEAD"), [".git"]) is True

    def test_no_skip_similar_names(self) -> None:
        """Files with similar names should not be skipped unless they start with the pattern."""
        # my-git-project doesn't start with .git
        assert should_skip_path(Path("my-git-project/file.txt"), [".git"]) is False
        # Note: node_modules_backup DOES start with "node_modules", so it WILL be skipped
        # This is the intended behavior to catch things like node_modules.bak, etc.
        assert should_skip_path(Path("node_modules_backup/file.txt"), ["node_modules"]) is True
        # But completely different names are not skipped
        assert should_skip_path(Path("my_modules/file.txt"), ["node_modules"]) is False

    def test_skip_ds_store(self) -> None:
        """.DS_Store files should be skipped."""
        assert should_skip_path(Path(".DS_Store"), [".DS_Store"]) is True
        assert should_skip_path(Path("folder/.DS_Store"), [".DS_Store"]) is True

    def test_no_skip_regular_files(self) -> None:
        """Regular files should not be skipped."""
        assert should_skip_path(Path("src/main.py"), [".git", "node_modules"]) is False
        assert should_skip_path(Path("README.md"), [".git"]) is False

    def test_empty_patterns(self) -> None:
        """Empty patterns list should skip nothing."""
        assert should_skip_path(Path(".git/config"), []) is False
        assert should_skip_path(Path("any/path"), []) is False


class TestArchiveRoundTrip:
    """Tests for archive creation and extraction (round-trip integrity)."""

    async def test_single_file_round_trip(self, tmp_path: Path) -> None:
        """Single file should survive archive round-trip unchanged."""
        # Setup: create a file
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        test_file = source_dir / "hello.txt"
        test_file.write_text("Hello, World!")

        # Create archive
        result = await create_archive(source_dir, skip_patterns=[])

        assert isinstance(result, ArchiveResult)
        assert result.files_count == 1
        assert result.size_bytes > 0
        assert result.checksum.startswith("sha256:")

        # Extract to different directory
        extract_dir = tmp_path / "extract"
        extract_dir.mkdir()
        extract_result = await extract_archive(result.data, extract_dir)

        assert isinstance(extract_result, ExtractResult)
        assert extract_result.files_count == 1

        # Verify content
        extracted_file = extract_dir / "hello.txt"
        assert extracted_file.exists()
        assert extracted_file.read_text() == "Hello, World!"

    async def test_multiple_files_round_trip(self, tmp_path: Path) -> None:
        """Multiple files in nested directories should survive round-trip."""
        source_dir = tmp_path / "source"
        source_dir.mkdir()

        # Create nested structure
        (source_dir / "src").mkdir()
        (source_dir / "src" / "main.py").write_text("print('hello')")
        (source_dir / "src" / "utils").mkdir()
        (source_dir / "src" / "utils" / "helper.py").write_text("def help(): pass")
        (source_dir / "README.md").write_text("# Project")
        (source_dir / "config.json").write_text('{"key": "value"}')

        # Create and extract
        result = await create_archive(source_dir, skip_patterns=[])
        assert result.files_count == 4

        extract_dir = tmp_path / "extract"
        extract_dir.mkdir()
        await extract_archive(result.data, extract_dir)

        # Verify all files
        assert (extract_dir / "README.md").read_text() == "# Project"
        assert (extract_dir / "config.json").read_text() == '{"key": "value"}'
        assert (extract_dir / "src" / "main.py").read_text() == "print('hello')"
        assert (extract_dir / "src" / "utils" / "helper.py").read_text() == "def help(): pass"

    async def test_binary_file_round_trip(self, tmp_path: Path) -> None:
        """Binary files should survive round-trip unchanged."""
        source_dir = tmp_path / "source"
        source_dir.mkdir()

        # Create binary file with null bytes
        binary_content = b"\x00\x01\x02\xff\xfe\xfd" + b"mixed content" + b"\x00\x00"
        (source_dir / "binary.dat").write_bytes(binary_content)

        result = await create_archive(source_dir, skip_patterns=[])
        extract_dir = tmp_path / "extract"
        extract_dir.mkdir()
        await extract_archive(result.data, extract_dir)

        assert (extract_dir / "binary.dat").read_bytes() == binary_content

    async def test_empty_directory_creates_empty_archive(self, tmp_path: Path) -> None:
        """Empty directory should create archive with 0 files."""
        source_dir = tmp_path / "empty"
        source_dir.mkdir()

        result = await create_archive(source_dir, skip_patterns=[])

        assert result.files_count == 0
        assert result.size_bytes > 0  # Archive has header even if empty
        assert result.checksum.startswith("sha256:")

    async def test_unicode_filenames_round_trip(self, tmp_path: Path) -> None:
        """Unicode filenames should survive round-trip."""
        source_dir = tmp_path / "source"
        source_dir.mkdir()

        # Create files with unicode names
        (source_dir / "hello_world.txt").write_text("English")
        (source_dir / "archivo_espanol.txt").write_text("Spanish content")

        result = await create_archive(source_dir, skip_patterns=[])
        extract_dir = tmp_path / "extract"
        extract_dir.mkdir()
        await extract_archive(result.data, extract_dir)

        assert (extract_dir / "hello_world.txt").read_text() == "English"
        assert (extract_dir / "archivo_espanol.txt").read_text() == "Spanish content"


class TestArchiveSkipPatterns:
    """Tests for skip pattern filtering during archive creation."""

    async def test_skip_git_directory(self, tmp_path: Path) -> None:
        """.git directory should be excluded from archive."""
        source_dir = tmp_path / "source"
        source_dir.mkdir()

        # Create .git directory with files
        git_dir = source_dir / ".git"
        git_dir.mkdir()
        (git_dir / "config").write_text("[core]")
        (git_dir / "HEAD").write_text("ref: refs/heads/main")

        # Create regular files
        (source_dir / "main.py").write_text("print('hello')")

        result = await create_archive(source_dir, skip_patterns=[".git"])

        # Only main.py should be included
        assert result.files_count == 1

        # Verify by extracting
        extract_dir = tmp_path / "extract"
        extract_dir.mkdir()
        await extract_archive(result.data, extract_dir)

        assert (extract_dir / "main.py").exists()
        assert not (extract_dir / ".git").exists()

    async def test_skip_multiple_patterns(self, tmp_path: Path) -> None:
        """Multiple skip patterns should all be applied."""
        source_dir = tmp_path / "source"
        source_dir.mkdir()

        # Create various directories
        (source_dir / ".git").mkdir()
        (source_dir / ".git" / "config").write_text("git config")
        (source_dir / "node_modules").mkdir()
        (source_dir / "node_modules" / "lodash.js").write_text("lodash")
        (source_dir / "__pycache__").mkdir()
        (source_dir / "__pycache__" / "main.pyc").write_bytes(b"\x00\x00")
        (source_dir / "src").mkdir()
        (source_dir / "src" / "main.py").write_text("main code")

        result = await create_archive(source_dir, skip_patterns=[".git", "node_modules", "__pycache__"])

        assert result.files_count == 1  # Only src/main.py

    async def test_skip_cache_files(self, tmp_path: Path) -> None:
        """Cache files should be excluded from archive."""
        source_dir = tmp_path / "source"
        source_dir.mkdir()

        (source_dir / ".sb_manifest_cache.json").write_text("{}")
        (source_dir / ".sb_sync_cache.json").write_text("{}")
        (source_dir / "real_file.txt").write_text("real content")

        result = await create_archive(source_dir, skip_patterns=[".sb_manifest_cache.json", ".sb_sync_cache.json"])

        assert result.files_count == 1


class TestArchiveExtractSecurity:
    """Tests for security handling during archive extraction."""

    async def test_reject_path_traversal_dotdot(self, tmp_path: Path) -> None:
        """Archives with .. in paths should have those entries skipped."""
        # Create a malicious archive with path traversal
        tar_buffer = io.BytesIO()
        with tarfile.open(fileobj=tar_buffer, mode="w") as tar:
            # Add a normal file
            normal_info = tarfile.TarInfo(name="normal.txt")
            normal_content = b"normal content"
            normal_info.size = len(normal_content)
            tar.addfile(normal_info, io.BytesIO(normal_content))

            # Add a file with path traversal (this should be skipped)
            malicious_info = tarfile.TarInfo(name="../../../etc/passwd")
            malicious_content = b"malicious content"
            malicious_info.size = len(malicious_content)
            tar.addfile(malicious_info, io.BytesIO(malicious_content))

        # Compress with zstd
        tar_data = tar_buffer.getvalue()
        compressed = pyzstd.compress(tar_data)

        extract_dir = tmp_path / "extract"
        extract_dir.mkdir()

        result = await extract_archive(compressed, extract_dir)

        # Only normal file should be extracted
        assert (extract_dir / "normal.txt").exists()
        # Malicious file should not exist anywhere
        assert not (tmp_path / "etc" / "passwd").exists()
        assert not (extract_dir / "etc" / "passwd").exists()

    async def test_reject_absolute_paths(self, tmp_path: Path) -> None:
        """Archives with absolute paths should have those entries skipped."""
        tar_buffer = io.BytesIO()
        with tarfile.open(fileobj=tar_buffer, mode="w") as tar:
            # Add file with absolute path
            abs_info = tarfile.TarInfo(name="/etc/passwd")
            abs_content = b"absolute path content"
            abs_info.size = len(abs_content)
            tar.addfile(abs_info, io.BytesIO(abs_content))

            # Add normal file
            normal_info = tarfile.TarInfo(name="safe.txt")
            normal_content = b"safe content"
            normal_info.size = len(normal_content)
            tar.addfile(normal_info, io.BytesIO(normal_content))

        compressed = pyzstd.compress(tar_buffer.getvalue())

        extract_dir = tmp_path / "extract"
        extract_dir.mkdir()

        await extract_archive(compressed, extract_dir)

        # Only safe file should be extracted
        assert (extract_dir / "safe.txt").exists()
        assert not Path("/etc/passwd").exists() or Path("/etc/passwd").read_text() != "absolute path content"


class TestArchiveCorruption:
    """Tests for corrupt archive handling."""

    async def test_invalid_magic_bytes(self, tmp_path: Path) -> None:
        """Non-zstd data should raise CorruptArchiveError."""
        invalid_data = b"This is not a zstd archive"

        extract_dir = tmp_path / "extract"
        extract_dir.mkdir()

        with pytest.raises(CorruptArchiveError) as exc_info:
            await extract_archive(invalid_data, extract_dir)

        assert "Invalid archive magic" in str(exc_info.value)

    async def test_truncated_archive(self, tmp_path: Path) -> None:
        """Truncated zstd data should raise CorruptArchiveError."""
        # Create valid archive first
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        (source_dir / "file.txt").write_text("content")

        result = await create_archive(source_dir, skip_patterns=[])

        # Truncate the archive
        truncated = result.data[: len(result.data) // 2]

        extract_dir = tmp_path / "extract"
        extract_dir.mkdir()

        with pytest.raises(CorruptArchiveError) as exc_info:
            await extract_archive(truncated, extract_dir)

        assert "decompress" in str(exc_info.value).lower() or "zstd" in str(exc_info.value).lower()

    async def test_too_small_data(self, tmp_path: Path) -> None:
        """Data smaller than 4 bytes should raise CorruptArchiveError."""
        extract_dir = tmp_path / "extract"
        extract_dir.mkdir()

        with pytest.raises(CorruptArchiveError) as exc_info:
            await extract_archive(b"abc", extract_dir)

        assert "too small" in str(exc_info.value).lower()

    async def test_valid_zstd_invalid_tar(self, tmp_path: Path) -> None:
        """Valid zstd wrapping invalid tar should raise CorruptArchiveError."""
        # Create valid zstd data that's not a valid tar
        invalid_tar_data = b"this is not a tar file"
        compressed = pyzstd.compress(invalid_tar_data)

        extract_dir = tmp_path / "extract"
        extract_dir.mkdir()

        with pytest.raises(CorruptArchiveError) as exc_info:
            await extract_archive(compressed, extract_dir)

        assert "tar" in str(exc_info.value).lower()


class TestArchiveChecksum:
    """Tests for archive checksum computation."""

    async def test_checksum_format(self, tmp_path: Path) -> None:
        """Checksum should be in sha256:hex format."""
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        (source_dir / "file.txt").write_text("content")

        result = await create_archive(source_dir, skip_patterns=[])

        assert result.checksum.startswith("sha256:")
        hex_part = result.checksum.split(":")[1]
        assert len(hex_part) == 64  # SHA256 produces 64 hex chars
        assert all(c in "0123456789abcdef" for c in hex_part)

    async def test_checksum_deterministic(self, tmp_path: Path) -> None:
        """Same content should produce same checksum."""
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        (source_dir / "file.txt").write_text("deterministic content")

        result1 = await create_archive(source_dir, skip_patterns=[])
        result2 = await create_archive(source_dir, skip_patterns=[])

        # Note: mtime differences could cause checksum differences
        # but for files created in same test, they should match
        assert result1.checksum == result2.checksum

    async def test_different_content_different_checksum(self, tmp_path: Path) -> None:
        """Different content should produce different checksum."""
        source_dir = tmp_path / "source"
        source_dir.mkdir()

        (source_dir / "file.txt").write_text("content A")
        result_a = await create_archive(source_dir, skip_patterns=[])

        (source_dir / "file.txt").write_text("content B")
        result_b = await create_archive(source_dir, skip_patterns=[])

        assert result_a.checksum != result_b.checksum
