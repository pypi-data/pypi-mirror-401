"""
Workspace archive operations for tar.zst compression/decompression and HTTP transfer.

This module handles creating and extracting tar.zst archives and transferring them
via presigned URLs for workspace sync operations.
"""

from __future__ import annotations

import io
import asyncio
import hashlib
import tarfile
from pathlib import Path
from dataclasses import dataclass
from collections.abc import Iterable

import httpx
import pyzstd
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

from sb0.lib.utils.logging import make_logger

logger = make_logger(__name__)


# HTTP retry configuration: 1 retry with exponential backoff
HTTP_RETRY_CONFIG = {
    "stop": stop_after_attempt(2),  # Initial attempt + 1 retry
    "wait": wait_exponential(multiplier=1, min=1, max=10),
    "retry": retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError)),
}


class WorkspaceSyncError(Exception):
    """Base exception for workspace sync operations."""

    pass


class CorruptArchiveError(WorkspaceSyncError):
    """Raised when archive cannot be decompressed or extracted."""

    pass


class WorkspaceNotFoundError(WorkspaceSyncError):
    """Raised when workspace archive doesn't exist in GCS (new workspace)."""

    pass


@dataclass
class ArchiveResult:
    """Result of archive creation."""

    data: bytes
    checksum: str  # SHA256 of compressed data
    size_bytes: int
    files_count: int


@dataclass
class ExtractResult:
    """Result of archive extraction."""

    files_count: int
    bytes_extracted: int


def should_skip_path(path: Path, skip_patterns: Iterable[str]) -> bool:
    """
    Check if path matches any skip patterns.

    A path matches if any of its components equals or starts with a skip pattern.
    E.g., "node_modules/foo/bar.js" matches pattern "node_modules".

    Args:
        path: Path to check (can be relative)
        skip_patterns: Patterns to match against

    Returns:
        True if path should be skipped, False otherwise
    """
    for part in path.parts:
        for pattern in skip_patterns:
            if part == pattern or part.startswith(pattern):
                return True
    return False


def _create_archive_sync(
    local_path: Path,
    skip_patterns: Iterable[str],
) -> ArchiveResult:
    """
    Synchronous archive creation (runs in thread pool).

    Creates a tar.zst archive from directory contents.
    """
    files_count = 0
    tar_buffer = io.BytesIO()

    # Resolve the local path to handle symlinks
    local_path = local_path.resolve()

    with tarfile.open(fileobj=tar_buffer, mode="w") as tar:
        for file_path in local_path.rglob("*"):
            # Skip directories, only add files
            if not file_path.is_file():
                continue

            # Get relative path
            try:
                rel_path = file_path.relative_to(local_path)
            except ValueError:
                # Path is not relative to local_path (shouldn't happen)
                continue

            # Check skip patterns
            if should_skip_path(rel_path, skip_patterns):
                continue

            try:
                # Read file content
                content = file_path.read_bytes()

                # Create tar entry
                tarinfo = tarfile.TarInfo(name=str(rel_path))
                tarinfo.size = len(content)
                tarinfo.mtime = int(file_path.stat().st_mtime)
                tar.addfile(tarinfo, io.BytesIO(content))
                files_count += 1
            except (OSError, PermissionError) as e:
                logger.warning(f"Skipping file {rel_path}: {e}")
                continue

    # Compress with zstd (level=1 for fast compression)
    tar_data = tar_buffer.getvalue()
    compressed = pyzstd.compress(tar_data, level_or_option=1)

    # Compute checksum of compressed data
    checksum = f"sha256:{hashlib.sha256(compressed).hexdigest()}"

    return ArchiveResult(
        data=compressed,
        checksum=checksum,
        size_bytes=len(compressed),
        files_count=files_count,
    )


async def create_archive(
    local_path: Path,
    skip_patterns: Iterable[str],
) -> ArchiveResult:
    """
    Create tar.zst archive from directory.

    Args:
        local_path: Directory to archive
        skip_patterns: Patterns to skip (e.g., [".git", "node_modules"])

    Returns:
        ArchiveResult with bytes, checksum, size
    """
    return await asyncio.to_thread(_create_archive_sync, local_path, skip_patterns)


def _extract_archive_sync(archive_data: bytes, local_path: Path) -> ExtractResult:
    """Synchronous archive extraction (runs in thread pool)."""
    files_count = 0
    bytes_extracted = 0

    # Verify zstd magic bytes (0x28B52FFD in little-endian)
    if len(archive_data) < 4:
        raise CorruptArchiveError("Archive too small to be valid")

    magic = int.from_bytes(archive_data[:4], "little")
    if magic != 0xFD2FB528:  # zstd magic (little-endian)
        raise CorruptArchiveError(f"Invalid archive magic: expected zstd (0xFD2FB528), got 0x{magic:08X}")

    # Decompress zstd
    try:
        tar_data = pyzstd.decompress(archive_data)
    except pyzstd.ZstdError as e:
        raise CorruptArchiveError(f"Failed to decompress zstd archive: {e}") from e

    # Extract tar
    try:
        tar_buffer = io.BytesIO(tar_data)
        with tarfile.open(fileobj=tar_buffer, mode="r") as tar:
            for member in tar.getmembers():
                # Safety: skip absolute paths and parent references
                if member.name.startswith("/") or ".." in member.name:
                    logger.warning(f"Skipping suspicious path in archive: {member.name}")
                    continue

                # Use filter="data" for security (prevents path traversal)
                tar.extract(member, path=local_path, filter="data")
                files_count += 1
                if member.isfile():
                    bytes_extracted += member.size

    except tarfile.TarError as e:
        raise CorruptArchiveError(f"Failed to extract tar archive: {e}") from e

    return ExtractResult(files_count=files_count, bytes_extracted=bytes_extracted)


async def extract_archive(archive_data: bytes, local_path: Path) -> ExtractResult:
    """
    Extract tar.zst archive to directory with comprehensive error handling.

    Handles:
    - Corrupt/invalid zstd data
    - Invalid tar format
    - Path traversal attacks (via filter="data")

    Args:
        archive_data: Compressed archive bytes
        local_path: Directory to extract to

    Returns:
        ExtractResult with file count

    Raises:
        CorruptArchiveError: If archive cannot be decompressed or extracted
    """
    return await asyncio.to_thread(_extract_archive_sync, archive_data, local_path)


@retry(**HTTP_RETRY_CONFIG)
async def upload_to_presigned_url(
    url: str,
    data: bytes,
    content_type: str = "application/zstd",
    timeout: float = 300.0,  # 5 minutes
) -> None:
    """
    Upload bytes to presigned PUT URL with retry.

    Retries once on:
    - TimeoutException: Network timeout
    - ConnectError: Connection failed

    Does NOT retry on:
    - 4xx errors: Client error (bad request, forbidden)
    - 5xx errors: Server error (let GCS handle internally)

    Args:
        url: Presigned PUT URL
        data: Bytes to upload
        content_type: Content-Type header value
        timeout: Request timeout in seconds
    """
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.put(
            url,
            content=data,
            headers={"Content-Type": content_type},
        )
        response.raise_for_status()


@retry(**HTTP_RETRY_CONFIG)
async def download_from_presigned_url(
    url: str,
    timeout: float = 300.0,  # 5 minutes
) -> bytes:
    """
    Download bytes from presigned GET URL with retry.

    Args:
        url: Presigned GET URL
        timeout: Request timeout in seconds

    Returns:
        Archive bytes on success

    Raises:
        WorkspaceNotFoundError: If 404 (archive doesn't exist)
        httpx.HTTPStatusError: On other HTTP errors
    """
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(url)

        # Handle 404 specially - workspace archive doesn't exist
        if response.status_code == 404:
            raise WorkspaceNotFoundError("Workspace archive not found. This may be a new workspace.")

        response.raise_for_status()
        return response.content
