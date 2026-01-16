"""Probe handler for testing file access isolation.

This probe runs inside a sandbox and attempts to access various paths,
reporting whether each access succeeded or failed.
"""

from __future__ import annotations

import os
import json
from pathlib import Path

from sb0.lib.types.acp import CreateTaskParams


def probe_file_access(params: CreateTaskParams) -> None:
    """Attempt to access various paths and report results.

    Expects params.params to contain:
        paths_to_read: list[str] - paths to attempt reading
        paths_to_write: list[str] - paths to attempt writing (optional)
        sibling_workspace_id: str - workspace ID of sibling to attempt accessing (optional)
    """
    config = params.params or {}
    results: dict[str, dict] = {
        "reads": {},
        "writes": {},
        "environment": {
            "cwd": os.getcwd(),
            "uid": os.getuid(),
            "gid": os.getgid(),
            "pid": os.getpid(),
        },
    }

    # Attempt to read paths
    paths_to_read = config.get("paths_to_read", [])
    for path_str in paths_to_read:
        try:
            path = Path(path_str)
            if path.is_file():
                content = path.read_text()
                results["reads"][path_str] = {
                    "accessible": True,
                    "content_preview": content[:100],
                    "size": len(content),
                }
            elif path.is_dir():
                entries = list(path.iterdir())
                results["reads"][path_str] = {
                    "accessible": True,
                    "is_directory": True,
                    "entries": [str(e.name) for e in entries[:20]],
                }
            else:
                results["reads"][path_str] = {
                    "accessible": False,
                    "error": "Path does not exist",
                }
        except PermissionError as e:
            results["reads"][path_str] = {
                "accessible": False,
                "error": f"PermissionError: {e}",
            }
        except Exception as e:
            results["reads"][path_str] = {
                "accessible": False,
                "error": f"{type(e).__name__}: {e}",
            }

    # Attempt to write paths
    paths_to_write = config.get("paths_to_write", [])
    for path_str in paths_to_write:
        try:
            path = Path(path_str)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("PROBE_WRITE_TEST")
            results["writes"][path_str] = {
                "writable": True,
            }
        except PermissionError as e:
            results["writes"][path_str] = {
                "writable": False,
                "error": f"PermissionError: {e}",
            }
        except Exception as e:
            results["writes"][path_str] = {
                "writable": False,
                "error": f"{type(e).__name__}: {e}",
            }

    # Try to access sibling workspace if specified
    sibling_id = config.get("sibling_workspace_id")
    if sibling_id:
        sibling_paths = [
            f"/workspaces/{sibling_id}",
            f"/workspace/../{sibling_id}",
            f"/workspace/../../workspaces/{sibling_id}",
        ]
        results["sibling_access"] = {}
        for path_str in sibling_paths:
            try:
                path = Path(path_str)
                if path.exists():
                    if path.is_dir():
                        entries = list(path.iterdir())
                        results["sibling_access"][path_str] = {
                            "accessible": True,
                            "entries": [str(e.name) for e in entries[:10]],
                        }
                    else:
                        content = path.read_text()
                        results["sibling_access"][path_str] = {
                            "accessible": True,
                            "content_preview": content[:50],
                        }
                else:
                    results["sibling_access"][path_str] = {
                        "accessible": False,
                        "error": "Does not exist",
                    }
            except Exception as e:
                results["sibling_access"][path_str] = {
                    "accessible": False,
                    "error": f"{type(e).__name__}: {e}",
                }

    # Write results to workspace
    output_path = Path("/workspace/probe_results.json")
    output_path.write_text(json.dumps(results, indent=2))
