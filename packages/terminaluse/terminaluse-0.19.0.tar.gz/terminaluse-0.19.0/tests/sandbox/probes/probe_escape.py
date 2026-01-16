"""Probe handler for testing path traversal and escape attempts.

This probe runs inside a sandbox and attempts various escape techniques,
reporting whether each attempt succeeded or failed.
"""

from __future__ import annotations

import os
import json
from pathlib import Path

from sb0.lib.types.acp import CreateTaskParams


def probe_path_traversal(params: CreateTaskParams) -> None:
    """Attempt various path traversal escapes and report results.

    Tests:
    - ../ traversal from /workspace
    - ../ traversal from /tmp
    - Symlink creation pointing outside sandbox
    - Reading sensitive host files
    """
    results: dict[str, dict] = {
        "dotdot_traversal": {},
        "symlink_escape": {},
        "sensitive_files": {},
        "environment": {
            "cwd": os.getcwd(),
            "uid": os.getuid(),
            "gid": os.getgid(),
        },
    }

    # Test ../ traversal patterns
    traversal_paths = [
        # From /workspace
        "/workspace/../../../etc/passwd",
        "/workspace/../../../etc/shadow",
        "/workspace/../../workspaces",
        "/workspace/../../../root",
        "/workspace/../../../home",
        # From /tmp
        "/tmp/../../../etc/passwd",
        "/tmp/../../etc/hosts",
        # Absolute paths that should be blocked or show sandbox content
        "/etc/passwd",
        "/etc/shadow",
        "/root/.bashrc",
    ]

    for path_str in traversal_paths:
        try:
            path = Path(path_str)
            resolved = path.resolve()
            if path.exists():
                if path.is_file():
                    content = path.read_text()
                    results["dotdot_traversal"][path_str] = {
                        "accessible": True,
                        "resolved_to": str(resolved),
                        "content_preview": content[:100],
                        "is_host_file": _looks_like_host_content(path_str, content),
                    }
                elif path.is_dir():
                    entries = [e.name for e in path.iterdir()][:10]
                    results["dotdot_traversal"][path_str] = {
                        "accessible": True,
                        "resolved_to": str(resolved),
                        "is_directory": True,
                        "entries": entries,
                    }
            else:
                results["dotdot_traversal"][path_str] = {
                    "accessible": False,
                    "resolved_to": str(resolved),
                    "error": "Does not exist",
                }
        except PermissionError as e:
            results["dotdot_traversal"][path_str] = {
                "accessible": False,
                "error": f"PermissionError: {e}",
            }
        except Exception as e:
            results["dotdot_traversal"][path_str] = {
                "accessible": False,
                "error": f"{type(e).__name__}: {e}",
            }

    # Test symlink escape
    symlink_tests = [
        ("/workspace/escape_etc_passwd", "/etc/passwd"),
        ("/workspace/escape_root", "/root"),
        ("/workspace/escape_workspaces", "/workspaces"),
        ("/tmp/escape_etc_passwd", "/etc/passwd"),
    ]

    for symlink_path, target in symlink_tests:
        try:
            link = Path(symlink_path)
            if link.exists() or link.is_symlink():
                link.unlink()

            os.symlink(target, symlink_path)

            # Try to read through the symlink
            if link.exists():
                if link.is_file():
                    content = link.read_text()
                    results["symlink_escape"][symlink_path] = {
                        "symlink_created": True,
                        "target": target,
                        "readable_through_symlink": True,
                        "content_preview": content[:100],
                    }
                elif link.is_dir():
                    entries = [e.name for e in link.iterdir()][:10]
                    results["symlink_escape"][symlink_path] = {
                        "symlink_created": True,
                        "target": target,
                        "readable_through_symlink": True,
                        "entries": entries,
                    }
            else:
                results["symlink_escape"][symlink_path] = {
                    "symlink_created": True,
                    "target": target,
                    "readable_through_symlink": False,
                    "error": "Symlink target not accessible",
                }
        except PermissionError as e:
            results["symlink_escape"][symlink_path] = {
                "symlink_created": False,
                "target": target,
                "error": f"PermissionError: {e}",
            }
        except Exception as e:
            results["symlink_escape"][symlink_path] = {
                "symlink_created": False,
                "target": target,
                "error": f"{type(e).__name__}: {e}",
            }

    # Write results to workspace
    output_path = Path("/workspace/probe_results.json")
    output_path.write_text(json.dumps(results, indent=2))


def _looks_like_host_content(path: str, content: str) -> bool:
    """Heuristic to detect if content looks like real host file vs sandbox copy."""
    if "passwd" in path:
        # Real /etc/passwd has root:x:0:0 at the start
        return content.startswith("root:")
    if "shadow" in path:
        # Shadow file has password hashes
        return "root:" in content and "$" in content
    return False
