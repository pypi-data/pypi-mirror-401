"""Sandbox configuration and feature flags."""

from __future__ import annotations

import os
from pathlib import Path
from dataclasses import field, dataclass


@dataclass
class SandboxConfig:
    """Configuration for nsjail sandboxing."""

    # Path to nsjail binary
    nsjail_path: str = field(default_factory=lambda: os.getenv("SB0_NSJAIL_PATH", "/usr/local/bin/nsjail"))

    # Agent directory (for bind mounts)
    agent_dir: Path = field(default_factory=lambda: Path(os.getenv("AGENT_DIR", os.getcwd())))

    # Code subdirectory within agent_dir (default: "project")
    # This is mounted to /agent/<code_subdir> and added to PYTHONPATH
    code_subdir: str = field(default_factory=lambda: os.getenv("SB0_SANDBOX_CODE_SUBDIR", "project"))

    # Timeout in seconds for handler execution
    timeout_seconds: int = field(default_factory=lambda: int(os.getenv("SB0_SANDBOX_TIMEOUT", "300")))

    # Whether sandboxing is enabled (can be disabled for local development)
    enabled: bool = field(default_factory=lambda: os.getenv("SB0_SANDBOX_ENABLED", "true").lower() == "true")

    # Enable verbose logging for debugging sandbox issues
    verbose: bool = field(default_factory=lambda: os.getenv("SB0_SANDBOX_VERBOSE", "false").lower() == "true")


# Global singleton, lazily initialized
_sandbox_config: SandboxConfig | None = None


def get_sandbox_config() -> SandboxConfig:
    """Get the global sandbox configuration."""
    global _sandbox_config
    if _sandbox_config is None:
        _sandbox_config = SandboxConfig()
    return _sandbox_config


def configure_sandbox(config: SandboxConfig) -> None:
    """Set the global sandbox configuration."""
    global _sandbox_config
    _sandbox_config = config


def reset_sandbox_config() -> None:
    """Reset the global sandbox configuration (primarily for testing)."""
    global _sandbox_config
    _sandbox_config = None
