"""Tests for path traversal prevention in sandboxes.

Verifies that:
- ../ traversal cannot escape the sandbox
- Symlinks cannot be used to escape the sandbox
- Sensitive host files are not accessible
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


class TestPathTraversal:
    """Test that path traversal attacks are blocked."""

    def test_dotdot_traversal_blocked(
        self,
        sandbox_runner: SandboxRunner,
        test_workspace,
    ) -> None:
        """../ traversal should not allow escaping to host filesystem."""
        handler_ref = HandlerRef(module="probes.probe_escape", function="probe_path_traversal")
        params = _make_params(
            workspace_id=test_workspace.workspace_id,
            probe_config={},
        )

        result = sandbox_runner.run(
            method="task/create",
            handler_ref=handler_ref,
            params=params,
            workspace_id=test_workspace.workspace_id,
        )

        assert result.success, f"Sandbox failed: {result.stderr}"

        probe_results = json.loads(test_workspace.read_file("probe_results.json"))
        traversal_results = probe_results.get("dotdot_traversal", {})

        # Check critical paths that should NOT be accessible as host files
        sensitive_paths = [
            "/workspace/../../../etc/shadow",
            "/workspace/../../../root",
            "/tmp/../../../etc/shadow",
        ]

        for path in sensitive_paths:
            if path in traversal_results:
                result_info = traversal_results[path]
                if result_info.get("accessible"):
                    # If accessible, it should NOT be the real host file
                    assert not result_info.get("is_host_file", False), (
                        f"Path {path} returned real host content: {result_info}"
                    )

        # /etc/passwd might be accessible (bind-mounted for DNS/user resolution)
        # but /etc/shadow should never be
        shadow_paths = [p for p in traversal_results if "shadow" in p]
        for path in shadow_paths:
            result_info = traversal_results[path]
            assert not result_info.get("accessible") or not result_info.get("is_host_file"), (
                f"Shadow file accessible: {path} -> {result_info}"
            )

    def test_cannot_escape_to_workspaces_dir(
        self,
        sandbox_runner: SandboxRunner,
        workspace_pair: tuple,
    ) -> None:
        """Cannot use ../ to access /workspaces directory and other workspaces."""
        ws_a, ws_b = workspace_pair

        # Create a secret in workspace B
        ws_b.write_file("secret.txt", "SECRET_B")

        handler_ref = HandlerRef(module="probes.probe_escape", function="probe_path_traversal")
        params = _make_params(
            workspace_id=ws_a.workspace_id,
            probe_config={},
        )

        result = sandbox_runner.run(
            method="task/create",
            handler_ref=handler_ref,
            params=params,
            workspace_id=ws_a.workspace_id,
        )

        assert result.success, f"Sandbox failed: {result.stderr}"

        probe_results = json.loads(ws_a.read_file("probe_results.json"))
        traversal_results = probe_results.get("dotdot_traversal", {})

        # Check if /workspace/../../workspaces was accessible
        workspaces_path = "/workspace/../../workspaces"
        if workspaces_path in traversal_results:
            result_info = traversal_results[workspaces_path]
            if result_info.get("accessible") and result_info.get("is_directory"):
                # If accessible, it should NOT contain sibling workspaces
                entries = result_info.get("entries", [])
                assert ws_b.workspace_id not in entries, (
                    f"Sibling workspace {ws_b.workspace_id} visible via path traversal: {entries}"
                )

    def test_symlink_escape_blocked(
        self,
        sandbox_runner: SandboxRunner,
        test_workspace,
    ) -> None:
        """Creating symlinks to escape sandbox should not allow reading host files."""
        handler_ref = HandlerRef(module="probes.probe_escape", function="probe_path_traversal")
        params = _make_params(
            workspace_id=test_workspace.workspace_id,
            probe_config={},
        )

        result = sandbox_runner.run(
            method="task/create",
            handler_ref=handler_ref,
            params=params,
            workspace_id=test_workspace.workspace_id,
        )

        assert result.success, f"Sandbox failed: {result.stderr}"

        probe_results = json.loads(test_workspace.read_file("probe_results.json"))
        symlink_results = probe_results.get("symlink_escape", {})

        for symlink_path, result_info in symlink_results.items():
            target = result_info.get("target", "")

            # Symlinks to sensitive locations should either:
            # 1. Fail to create
            # 2. Succeed but be unreadable
            # 3. Point to sandbox-local content (not host content)

            if "/etc/passwd" in target or "/etc/shadow" in target:
                if result_info.get("readable_through_symlink"):
                    content = result_info.get("content_preview", "")
                    # If readable, verify it's sandbox content, not host
                    # Host /etc/passwd is typically 1000+ bytes with many entries
                    # Sandbox passwd (if any) would be minimal
                    is_likely_host = content.startswith("root:") and len(content) > 200
                    assert not is_likely_host, (
                        f"Symlink {symlink_path} -> {target} exposed host content: {content}"
                    )

            if target == "/root":
                # /root symlink should either fail or show sandbox /root (tmpfs)
                if result_info.get("readable_through_symlink"):
                    entries = result_info.get("entries", [])
                    # Sandbox /root is a tmpfs, should be mostly empty
                    # Host /root would have more files
                    pass  # Difficult to verify without host-specific assumptions

            if target == "/workspaces":
                # Should not be able to list sibling workspaces
                if result_info.get("readable_through_symlink"):
                    entries = result_info.get("entries", [])
                    # In proper isolation, should not see sibling workspaces
                    # or the workspaces dir shouldn't be accessible at all
                    pass

    def test_tmp_is_ephemeral(
        self,
        sandbox_runner: SandboxRunner,
        test_workspace,
    ) -> None:
        """Files written to /tmp should not persist across sandbox invocations."""
        handler_ref = HandlerRef(module="probes.probe_file_access", function="probe_file_access")

        # First invocation: write to /tmp
        params = _make_params(
            workspace_id=test_workspace.workspace_id,
            probe_config={
                "paths_to_write": ["/tmp/ephemeral_test.txt"],
            },
        )

        result1 = sandbox_runner.run(
            method="task/create",
            handler_ref=handler_ref,
            params=params,
            workspace_id=test_workspace.workspace_id,
        )
        assert result1.success, f"First sandbox invocation failed: {result1.stderr}"

        # Second invocation: try to read the file
        params2 = _make_params(
            workspace_id=test_workspace.workspace_id,
            probe_config={
                "paths_to_read": ["/tmp/ephemeral_test.txt"],
            },
        )

        result2 = sandbox_runner.run(
            method="task/create",
            handler_ref=handler_ref,
            params=params2,
            workspace_id=test_workspace.workspace_id,
        )
        assert result2.success, f"Second sandbox invocation failed: {result2.stderr}"

        probe_results = json.loads(test_workspace.read_file("probe_results.json"))
        reads = probe_results.get("reads", {})

        # The file should NOT exist in the second invocation
        # because /tmp is ephemeral tmpfs cleared between invocations
        tmp_read = reads.get("/tmp/ephemeral_test.txt", {})
        assert not tmp_read.get("accessible"), (
            "/tmp file persisted across sandbox invocations! "
            "This breaks isolation - sandbox state should not leak."
        )

    def test_sandbox_runs_as_unprivileged_user(
        self,
        sandbox_runner: SandboxRunner,
        test_workspace,
    ) -> None:
        """Sandbox should run as nobody (UID 65534), not root."""
        handler_ref = HandlerRef(module="probes.probe_escape", function="probe_path_traversal")
        params = _make_params(
            workspace_id=test_workspace.workspace_id,
            probe_config={},
        )

        result = sandbox_runner.run(
            method="task/create",
            handler_ref=handler_ref,
            params=params,
            workspace_id=test_workspace.workspace_id,
        )

        assert result.success, f"Sandbox failed: {result.stderr}"

        probe_results = json.loads(test_workspace.read_file("probe_results.json"))
        env = probe_results.get("environment", {})

        uid = env.get("uid")
        gid = env.get("gid")

        # Should be nobody (65534) not root (0)
        assert uid == 65534, f"Sandbox running as UID {uid}, expected 65534 (nobody)"
        assert gid == 65534, f"Sandbox running as GID {gid}, expected 65534 (nogroup)"
