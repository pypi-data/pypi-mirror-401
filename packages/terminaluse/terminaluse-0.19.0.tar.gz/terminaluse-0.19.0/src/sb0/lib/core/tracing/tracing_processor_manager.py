from __future__ import annotations

from typing import TYPE_CHECKING
from threading import Lock

from sb0.lib.types.tracing import TracingProcessorConfig, Sb0TracingProcessorConfig
from sb0.lib.core.tracing.processors.tracing_processor_interface import (
    SyncTracingProcessor,
    AsyncTracingProcessor,
)

if TYPE_CHECKING:
    from sb0.lib.core.tracing.processors.sb0_tracing_processor import (  # noqa: F401
        Sb0SyncTracingProcessor,
        Sb0AsyncTracingProcessor,
    )


class TracingProcessorManager:
    def __init__(self):
        # Mapping of processor config type to processor class
        # Use lazy loading for sb0 processors to avoid circular imports
        self.sync_config_registry: dict[str, type[SyncTracingProcessor]] = {}
        self.async_config_registry: dict[str, type[AsyncTracingProcessor]] = {}
        # Cache for processors
        self.sync_processors: list[SyncTracingProcessor] = []
        self.async_processors: list[AsyncTracingProcessor] = []
        self.lock = Lock()
        self._sb0_registered = False

    def _ensure_sb0_registered(self):
        """Lazily register sb0 processors to avoid circular imports."""
        if not self._sb0_registered:
            from sb0.lib.core.tracing.processors.sb0_tracing_processor import (
                Sb0SyncTracingProcessor,
                Sb0AsyncTracingProcessor,
            )

            self.sync_config_registry["sb0"] = Sb0SyncTracingProcessor
            self.async_config_registry["sb0"] = Sb0AsyncTracingProcessor
            self._sb0_registered = True

    def add_processor_config(self, processor_config: TracingProcessorConfig) -> None:
        with self.lock:
            self._ensure_sb0_registered()
            sync_processor = self.sync_config_registry[processor_config.type]
            async_processor = self.async_config_registry[processor_config.type]
            self.sync_processors.append(sync_processor(processor_config))
            self.async_processors.append(async_processor(processor_config))

    def set_processor_configs(self, processor_configs: list[TracingProcessorConfig]):
        with self.lock:
            for processor_config in processor_configs:
                self.add_processor_config(processor_config)

    def get_sync_processors(self) -> list[SyncTracingProcessor]:
        return self.sync_processors

    def get_async_processors(self) -> list[AsyncTracingProcessor]:
        return self.async_processors


# Global instance
GLOBAL_TRACING_PROCESSOR_MANAGER = TracingProcessorManager()

add_tracing_processor_config = GLOBAL_TRACING_PROCESSOR_MANAGER.add_processor_config
set_tracing_processor_configs = GLOBAL_TRACING_PROCESSOR_MANAGER.set_processor_configs

# Lazy initialization to avoid circular imports
_default_initialized = False


def _ensure_default_initialized():
    """Ensure default processor is initialized (lazy to avoid circular imports)."""
    global _default_initialized
    if not _default_initialized:
        add_tracing_processor_config(Sb0TracingProcessorConfig())
        _default_initialized = True


def get_sync_tracing_processors():
    """Get sync processors, initializing defaults if needed."""
    _ensure_default_initialized()
    return GLOBAL_TRACING_PROCESSOR_MANAGER.get_sync_processors()


def get_async_tracing_processors():
    """Get async processors, initializing defaults if needed."""
    _ensure_default_initialized()
    return GLOBAL_TRACING_PROCESSOR_MANAGER.get_async_processors()
