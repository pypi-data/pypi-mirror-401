"""Tests for file isolation between sandboxes.

Verifies that:
- Sandbox A cannot read files from Sandbox B's workspace
- Sandbox A cannot write files to Sandbox B's workspace
- Multiple concurrent sandboxes maintain isolation
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

import pytest

from sb0.types.task import Task
from sb0.types.agent import Agent
from sb0.lib.types.acp import CreateTaskParams
from sb0.lib.sandbox.runner import SandboxRunner
from sb0.lib.sandbox.handler_ref import HandlerRef


def _make_params(workspace_id: str, probe_config: dict) -> CreateTaskParams:
    """Create test params for a probe handler."""
    return CreateTaskParams(
        task=Task(
            id="test-task",
            workspace_id=workspace_id,
        ),
        agent=Agent(
            id="test-agent",
            name="test",
            description="test agent",
            acp_type="async",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        ),
        params=probe_config,
    )


class TestFileIsolation:
    """Test that sandboxes cannot access each other's files."""

    def test_cannot_read_sibling_workspace(
        self,
        sandbox_runner: SandboxRunner,
        workspace_pair: tuple,
    ) -> None:
        """Sandbox A cannot read files from Sandbox B's workspace."""
        ws_a, ws_b = workspace_pair

        # Create a secret file in workspace B
        secret_content = "SECRET_DATA_FROM_WORKSPACE_B"
        ws_b.write_file("secret.txt", secret_content)

        # Run probe in sandbox A, attempting to access workspace B
        handler_ref = HandlerRef(module="probes.probe_file_access", function="probe_file_access")
        params = _make_params(
            workspace_id=ws_a.workspace_id,
            probe_config={
                "sibling_workspace_id": ws_b.workspace_id,
                "paths_to_read": [
                    f"/workspaces/{ws_b.workspace_id}/secret.txt",
                ],
            },
        )

        result = sandbox_runner.run(
            method="task/create",
            handler_ref=handler_ref,
            params=params,
            workspace_id=ws_a.workspace_id,
        )

        assert result.success, f"Sandbox failed: {result.stderr}"

        # Read probe results
        probe_results = json.loads(ws_a.read_file("probe_results.json"))

        # Verify sibling access failed
        sibling_access = probe_results.get("sibling_access", {})
        for path, access_result in sibling_access.items():
            assert not access_result.get("accessible"), (
                f"Sandbox A could access sibling workspace path {path}: {access_result}"
            )

        # Verify direct path read failed
        reads = probe_results.get("reads", {})
        sibling_path = f"/workspaces/{ws_b.workspace_id}/secret.txt"
        if sibling_path in reads:
            assert not reads[sibling_path].get("accessible"), (
                f"Sandbox A could read sibling file directly: {reads[sibling_path]}"
            )

    def test_cannot_write_sibling_workspace(
        self,
        sandbox_runner: SandboxRunner,
        workspace_pair: tuple,
    ) -> None:
        """Sandbox A cannot write files to Sandbox B's workspace."""
        ws_a, ws_b = workspace_pair

        # Run probe in sandbox A, attempting to write to workspace B
        handler_ref = HandlerRef(module="probes.probe_file_access", function="probe_file_access")
        params = _make_params(
            workspace_id=ws_a.workspace_id,
            probe_config={
                "paths_to_write": [
                    f"/workspaces/{ws_b.workspace_id}/malicious.txt",
                    f"/workspace/../{ws_b.workspace_id}/malicious.txt",
                ],
            },
        )

        result = sandbox_runner.run(
            method="task/create",
            handler_ref=handler_ref,
            params=params,
            workspace_id=ws_a.workspace_id,
        )

        assert result.success, f"Sandbox failed: {result.stderr}"

        # Verify no malicious file was created in workspace B
        assert not ws_b.file_exists("malicious.txt"), (
            "Sandbox A was able to create file in Sandbox B's workspace!"
        )

        # Read probe results and verify writes failed
        probe_results = json.loads(ws_a.read_file("probe_results.json"))
        writes = probe_results.get("writes", {})

        for path, write_result in writes.items():
            if ws_b.workspace_id in path:
                assert not write_result.get("writable"), (
                    f"Sandbox A could write to sibling path {path}: {write_result}"
                )

    def test_workspace_isolation_concurrent(
        self,
        sandbox_runner: SandboxRunner,
    ) -> None:
        """Multiple sandboxes running concurrently maintain isolation."""
        import uuid
        import concurrent.futures
        from pathlib import Path
        import shutil

        num_sandboxes = 5
        workspaces = []

        try:
            # Create workspaces
            for i in range(num_sandboxes):
                workspace_id = f"concurrent_test_{uuid.uuid4().hex[:8]}"
                workspace_path = Path(f"/workspaces/{workspace_id}")
                dot_claude_path = Path(f"/dot_claudes/{workspace_id}")
                workspace_path.mkdir(parents=True, exist_ok=True)
                dot_claude_path.mkdir(parents=True, exist_ok=True)
                workspaces.append((workspace_id, workspace_path, dot_claude_path))

            def run_probe(workspace_info: tuple) -> dict:
                workspace_id, workspace_path, _ = workspace_info
                unique_id = f"UNIQUE_{workspace_id}"

                # Write unique identifier
                (workspace_path / "identity.txt").write_text(unique_id)

                handler_ref = HandlerRef(module="probes.probe_file_access", function="probe_file_access")
                params = _make_params(
                    workspace_id=workspace_id,
                    probe_config={
                        "paths_to_read": ["/workspace/identity.txt"],
                    },
                )

                result = sandbox_runner.run(
                    method="task/create",
                    handler_ref=handler_ref,
                    params=params,
                    workspace_id=workspace_id,
                )

                if not result.success:
                    return {"error": result.stderr, "workspace_id": workspace_id}

                probe_results = json.loads((workspace_path / "probe_results.json").read_text())
                return {
                    "workspace_id": workspace_id,
                    "expected_id": unique_id,
                    "reads": probe_results.get("reads", {}),
                }

            # Run sandboxes concurrently
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_sandboxes) as executor:
                results = list(executor.map(run_probe, workspaces))

            # Verify each sandbox only saw its own identity
            for result in results:
                if "error" in result:
                    pytest.fail(f"Sandbox {result['workspace_id']} failed: {result['error']}")

                identity_read = result["reads"].get("/workspace/identity.txt", {})
                assert identity_read.get("accessible"), (
                    f"Sandbox {result['workspace_id']} couldn't read its own identity file"
                )

                content = identity_read.get("content_preview", "")
                assert result["expected_id"] in content, (
                    f"Sandbox {result['workspace_id']} read wrong identity: "
                    f"expected {result['expected_id']}, got {content}"
                )

        finally:
            # Cleanup
            for workspace_id, workspace_path, dot_claude_path in workspaces:
                shutil.rmtree(workspace_path, ignore_errors=True)
                shutil.rmtree(dot_claude_path, ignore_errors=True)

    def test_can_read_own_workspace(
        self,
        sandbox_runner: SandboxRunner,
        test_workspace,
    ) -> None:
        """Sanity check: sandbox can read and write to its own workspace."""
        # Write a file before sandbox runs
        test_workspace.write_file("existing.txt", "EXISTING_CONTENT")

        handler_ref = HandlerRef(module="probes.probe_file_access", function="probe_file_access")
        params = _make_params(
            workspace_id=test_workspace.workspace_id,
            probe_config={
                "paths_to_read": ["/workspace/existing.txt", "/workspace"],
                "paths_to_write": ["/workspace/new_file.txt"],
            },
        )

        result = sandbox_runner.run(
            method="task/create",
            handler_ref=handler_ref,
            params=params,
            workspace_id=test_workspace.workspace_id,
        )

        assert result.success, f"Sandbox failed: {result.stderr}"

        # Verify probe could read existing file
        probe_results = json.loads(test_workspace.read_file("probe_results.json"))
        reads = probe_results.get("reads", {})

        existing_read = reads.get("/workspace/existing.txt", {})
        assert existing_read.get("accessible"), "Sandbox couldn't read its own existing file"
        assert "EXISTING_CONTENT" in existing_read.get("content_preview", "")

        # Verify probe could write new file
        writes = probe_results.get("writes", {})
        new_write = writes.get("/workspace/new_file.txt", {})
        assert new_write.get("writable"), "Sandbox couldn't write to its own workspace"

        # Verify the file actually exists
        assert test_workspace.file_exists("new_file.txt")
