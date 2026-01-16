from typing import Optional

from sb0 import AsyncSb0
from sb0.types.agent import Agent
from sb0.lib.utils.logging import make_logger
from sb0.lib.utils.temporal import heartbeat_if_in_workflow
from sb0.lib.core.tracing.tracer import AsyncTracer

logger = make_logger(__name__)


class AgentsService:
    def __init__(
        self,
        sb0_client: AsyncSb0,
        tracer: AsyncTracer,
    ):
        self._sb0_client = sb0_client
        self._tracer = tracer

    async def get_agent(
        self,
        agent_id: Optional[str] = None,
        agent_name: Optional[str] = None,
        trace_id: Optional[str] = None,
        parent_span_id: Optional[str] = None,
    ) -> Agent:
        trace = self._tracer.trace(trace_id)
        async with trace.span(
            parent_id=parent_span_id,
            name="get_agent",
            input={"agent_id": agent_id, "agent_name": agent_name},
        ) as span:
            heartbeat_if_in_workflow("get agent")
            if agent_id:
                agent = await self._sb0_client.agents.retrieve(agent_id=agent_id)
            elif agent_name:
                agent = await self._sb0_client.agents.retrieve_by_name(agent_name=agent_name)
            else:
                raise ValueError("Either agent_id or agent_name must be provided")
            if span:
                span.output = agent.model_dump()
            return agent
