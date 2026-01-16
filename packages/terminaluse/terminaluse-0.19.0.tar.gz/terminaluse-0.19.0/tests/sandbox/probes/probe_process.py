"""Probe handler for testing process isolation.

This probe runs inside a sandbox and enumerates visible processes,
reporting which PIDs are visible and attempting to signal them.
"""

from __future__ import annotations

import os
import json
import signal
from pathlib import Path

from sb0.lib.types.acp import CreateTaskParams


def probe_process_visibility(params: CreateTaskParams) -> None:
    """Enumerate visible processes and report findings.

    Expects params.params to contain:
        pids_to_signal: list[int] - PIDs to attempt signaling (optional)
    """
    config = params.params or {}
    results: dict[str, dict] = {
        "own_pid": os.getpid(),
        "own_ppid": os.getppid(),
        "visible_pids": [],
        "proc_enumeration": {},
        "signal_attempts": {},
    }

    # Enumerate /proc to find visible PIDs
    proc_path = Path("/proc")
    if proc_path.exists():
        for entry in proc_path.iterdir():
            if entry.name.isdigit():
                pid = int(entry.name)
                results["visible_pids"].append(pid)

                # Try to read process info
                try:
                    cmdline_path = entry / "cmdline"
                    if cmdline_path.exists():
                        cmdline = cmdline_path.read_bytes().replace(b"\x00", b" ").decode("utf-8", errors="replace")
                        results["proc_enumeration"][str(pid)] = {
                            "cmdline": cmdline[:200],
                            "readable": True,
                        }
                    else:
                        results["proc_enumeration"][str(pid)] = {"readable": False}
                except Exception as e:
                    results["proc_enumeration"][str(pid)] = {
                        "readable": False,
                        "error": str(e),
                    }

    # Attempt to signal specified PIDs
    pids_to_signal = config.get("pids_to_signal", [])
    for pid in pids_to_signal:
        try:
            # Signal 0 just checks if we can signal the process
            os.kill(pid, 0)
            results["signal_attempts"][str(pid)] = {
                "can_signal": True,
            }
        except ProcessLookupError:
            results["signal_attempts"][str(pid)] = {
                "can_signal": False,
                "error": "ESRCH - No such process",
            }
        except PermissionError:
            results["signal_attempts"][str(pid)] = {
                "can_signal": False,
                "error": "EPERM - Permission denied",
            }
        except Exception as e:
            results["signal_attempts"][str(pid)] = {
                "can_signal": False,
                "error": f"{type(e).__name__}: {e}",
            }

    # Check if we appear to be PID 1 (init) in our namespace
    results["is_pid_1"] = os.getpid() == 1

    # Write results to workspace
    output_path = Path("/workspace/probe_results.json")
    output_path.write_text(json.dumps(results, indent=2))
