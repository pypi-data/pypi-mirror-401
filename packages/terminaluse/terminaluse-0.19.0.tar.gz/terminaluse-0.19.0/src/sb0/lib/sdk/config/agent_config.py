from __future__ import annotations

from typing import Literal

from pydantic import Field

from sb0.lib.utils.logging import make_logger
from sb0.lib.utils.model_utils import BaseModel
from sb0.lib.types.agent_configs import TemporalConfig, TemporalWorkflowConfig

logger = make_logger(__name__)


class AgentConfig(BaseModel):
    name: str = Field(
        ...,
        description="Agent identifier in namespace_slug/agent_name format (e.g., 'acme-corp/my-agent')",
        pattern=r"^[a-z0-9-]+/[a-z0-9-]+$",
    )

    @property
    def namespace_slug(self) -> str:
        """Extract namespace slug from full name (e.g., 'acme-corp' from 'acme-corp/my-agent')"""
        return self.name.split("/")[0]

    @property
    def short_name(self) -> str:
        """Extract agent name from full name (e.g., 'my-agent' from 'acme-corp/my-agent')"""
        return self.name.split("/")[1]

    agent_input_type: Literal["text", "json"] | None = Field(
        default=None, description="The type of input the agent accepts."
    )
    description: str = Field(..., description="The description of the agent.")
    temporal: TemporalConfig | None = Field(default=None, description="Temporal workflow configuration for this agent")

    def is_temporal_agent(self) -> bool:
        """Check if this agent uses Temporal workflows"""
        # Check temporal config with enabled flag
        if self.temporal and self.temporal.enabled:
            return True
        return False

    def get_temporal_workflow_config(self) -> TemporalWorkflowConfig | None:
        """Get temporal workflow configuration, checking both new and legacy formats"""
        # Check new workflows list first
        if self.temporal and self.temporal.enabled and self.temporal.workflows:
            return self.temporal.workflows[0]  # Return first workflow for backward compatibility

        # Check legacy single workflow
        if self.temporal and self.temporal.enabled and self.temporal.workflow:
            return self.temporal.workflow

        return None

    def get_temporal_workflows(self) -> list[TemporalWorkflowConfig]:
        """Get all temporal workflow configurations"""
        # Check new workflows list first
        if self.temporal and self.temporal.enabled and self.temporal.workflows:
            return self.temporal.workflows

        # Check legacy single workflow
        if self.temporal and self.temporal.enabled and self.temporal.workflow:
            return [self.temporal.workflow]

        return []
