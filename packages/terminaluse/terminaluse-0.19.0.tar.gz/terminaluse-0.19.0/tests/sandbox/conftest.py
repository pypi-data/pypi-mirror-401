"""Fixtures for sandbox isolation tests.

These tests verify the sandbox contract:
1. File isolation: Sandbox A cannot read/write Sandbox B's workspace
2. Process isolation: Sandbox A cannot see/signal Sandbox B's processes
3. Path traversal blocked: Cannot escape workspace via ../, symlinks, etc.
"""

from __future__ import annotations

import os
import uuid
import shutil
from typing import Generator
from pathlib import Path
from dataclasses import dataclass

import pytest

from sb0.lib.sandbox.config import SandboxConfig, configure_sandbox, reset_sandbox_config
from sb0.lib.sandbox.runner import SandboxRunner, reset_sandbox_runner


# Skip all tests in this module if nsjail is not available
def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Skip sandbox tests if nsjail is not available."""
    nsjail_path = os.getenv("SB0_NSJAIL_PATH", "/usr/local/bin/nsjail")
    if not Path(nsjail_path).exists():
        skip_reason = (
            f"nsjail not available at {nsjail_path}. "
            "Run './tests/sandbox/run_tests.sh' to execute in Docker container."
        )
        skip_marker = pytest.mark.skip(reason=skip_reason)
        for item in items:
            if "tests/sandbox" in str(item.fspath):
                item.add_marker(skip_marker)


@dataclass
class TestWorkspace:
    """Test workspace with automatic cleanup."""

    workspace_id: str
    workspace_path: Path
    dot_claude_path: Path

    def write_file(self, name: str, content: str) -> Path:
        """Write a file to the workspace."""
        file_path = self.workspace_path / name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        return file_path

    def read_file(self, name: str) -> str:
        """Read a file from the workspace."""
        return (self.workspace_path / name).read_text()

    def file_exists(self, name: str) -> bool:
        """Check if a file exists in the workspace."""
        return (self.workspace_path / name).exists()

    def cleanup(self) -> None:
        """Remove workspace directories."""
        shutil.rmtree(self.workspace_path, ignore_errors=True)
        shutil.rmtree(self.dot_claude_path, ignore_errors=True)


@pytest.fixture
def test_workspace() -> Generator[TestWorkspace, None, None]:
    """Create an isolated test workspace."""
    workspace_id = f"test_{uuid.uuid4().hex[:8]}"
    workspace_path = Path(f"/workspaces/{workspace_id}")
    dot_claude_path = Path(f"/dot_claudes/{workspace_id}")

    workspace_path.mkdir(parents=True, exist_ok=True)
    dot_claude_path.mkdir(parents=True, exist_ok=True)

    workspace = TestWorkspace(
        workspace_id=workspace_id,
        workspace_path=workspace_path,
        dot_claude_path=dot_claude_path,
    )

    yield workspace

    workspace.cleanup()


@pytest.fixture
def workspace_pair() -> Generator[tuple[TestWorkspace, TestWorkspace], None, None]:
    """Create two isolated workspaces for cross-sandbox testing."""
    id_a = f"test_a_{uuid.uuid4().hex[:8]}"
    id_b = f"test_b_{uuid.uuid4().hex[:8]}"

    ws_a = TestWorkspace(
        workspace_id=id_a,
        workspace_path=Path(f"/workspaces/{id_a}"),
        dot_claude_path=Path(f"/dot_claudes/{id_a}"),
    )
    ws_b = TestWorkspace(
        workspace_id=id_b,
        workspace_path=Path(f"/workspaces/{id_b}"),
        dot_claude_path=Path(f"/dot_claudes/{id_b}"),
    )

    ws_a.workspace_path.mkdir(parents=True, exist_ok=True)
    ws_b.workspace_path.mkdir(parents=True, exist_ok=True)
    ws_a.dot_claude_path.mkdir(parents=True, exist_ok=True)
    ws_b.dot_claude_path.mkdir(parents=True, exist_ok=True)

    yield (ws_a, ws_b)

    ws_a.cleanup()
    ws_b.cleanup()


@pytest.fixture
def sandbox_config() -> Generator[SandboxConfig, None, None]:
    """Configure sandbox for testing with probe handlers.

    Sets agent_dir to tests/sandbox/ and code_subdir to probes/
    so that probe handlers can be imported as probes.probe_name.
    """
    # Find the tests/sandbox directory
    tests_sandbox_dir = Path(__file__).parent

    config = SandboxConfig(
        agent_dir=tests_sandbox_dir,
        code_subdir="probes",
        timeout_seconds=30,  # Shorter timeout for tests
        enabled=True,
        verbose=False,
    )

    configure_sandbox(config)

    yield config

    reset_sandbox_config()
    reset_sandbox_runner()


@pytest.fixture
def sandbox_runner(sandbox_config: SandboxConfig) -> SandboxRunner:
    """Get a SandboxRunner configured for testing."""
    return SandboxRunner(sandbox_config)
