"""
Debug utilities for Sb0 development.

Provides debugging setup functionality that can be used across different components.
"""

import os

import debugpy  # type: ignore

from sb0.lib.utils.logging import make_logger

logger = make_logger(__name__)


def setup_debug_if_enabled() -> None:
    """
    Setup debugpy if debug mode is enabled via environment variables.

    This function checks for Sb0 debug environment variables and configures
    debugpy accordingly. It's designed to be called early in worker startup.

    Environment Variables:
        SB0_DEBUG_ENABLED: Set to "true" to enable debug mode
        SB0_DEBUG_PORT: Port for debug server (default: 5678)
        SB0_DEBUG_TYPE: Type identifier for logging (default: "worker")
        SB0_DEBUG_WAIT_FOR_ATTACH: Set to "true" to wait for debugger attachment

    Raises:
        Any exception from debugpy setup (will bubble up naturally)
    """
    if os.getenv("SB0_DEBUG_ENABLED") == "true":
        debug_port = int(os.getenv("SB0_DEBUG_PORT", "5678"))
        debug_type = os.getenv("SB0_DEBUG_TYPE", "worker")
        wait_for_attach = os.getenv("SB0_DEBUG_WAIT_FOR_ATTACH", "false").lower() == "true"

        # Configure debugpy
        debugpy.configure(subProcess=False)
        debugpy.listen(debug_port)

        logger.info(f"🐛 [{debug_type.upper()}] Debug server listening on port {debug_port}")

        if wait_for_attach:
            logger.info(f"⏳ [{debug_type.upper()}] Waiting for debugger to attach...")
            debugpy.wait_for_client()
            logger.info(f"✅ [{debug_type.upper()}] Debugger attached!")
        else:
            logger.info(f"📡 [{debug_type.upper()}] Ready for debugger attachment")


def is_debug_enabled() -> bool:
    """
    Check if debug mode is currently enabled.

    Returns:
        bool: True if SB0_DEBUG_ENABLED is set to "true"
    """
    return os.getenv("SB0_DEBUG_ENABLED", "false").lower() == "true"


def get_debug_port() -> int:
    """
    Get the debug port from environment variables.

    Returns:
        int: Debug port (default: 5678)
    """
    return int(os.getenv("SB0_DEBUG_PORT", "5678"))
