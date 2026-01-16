"""
Sandbox module for nsjail-based handler isolation.

This module provides sandboxing capabilities for async handler execution,
isolating each handler invocation in its own nsjail sandbox.
"""

from sb0.lib.sandbox.config import SandboxConfig, configure_sandbox, get_sandbox_config
from sb0.lib.sandbox.runner import (
    SandboxResult,
    SandboxRunner,
    get_sandbox_runner,
    run_handler_sandboxed,
)
from sb0.lib.sandbox.handler_ref import (
    HandlerRef,
    HandlerValidationError,
    handler_ref_from_callable,
    validate_handler_for_sandbox,
)

__all__ = [
    # Config
    "SandboxConfig",
    "get_sandbox_config",
    "configure_sandbox",
    # Handler reference
    "HandlerRef",
    "HandlerValidationError",
    "handler_ref_from_callable",
    "validate_handler_for_sandbox",
    # Runner
    "SandboxResult",
    "SandboxRunner",
    "get_sandbox_runner",
    "run_handler_sandboxed",
]
