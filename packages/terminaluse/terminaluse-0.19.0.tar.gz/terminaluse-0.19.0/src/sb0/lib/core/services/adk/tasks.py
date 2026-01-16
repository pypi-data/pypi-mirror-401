from __future__ import annotations

from sb0 import AsyncSb0
from sb0.types import DeleteResponse
from sb0.types.task import Task
from sb0.lib.utils.logging import make_logger
from sb0.lib.utils.temporal import heartbeat_if_in_workflow
from sb0.types.task_response import TaskResponse
from sb0.lib.core.tracing.tracer import AsyncTracer

logger = make_logger(__name__)


class TasksService:
    def __init__(
        self,
        sb0_client: AsyncSb0,
        tracer: AsyncTracer,
    ):
        self._sb0_client = sb0_client
        self._tracer = tracer

    async def get_task(
        self,
        task_id: str | None = None,
        task_name: str | None = None,
        trace_id: str | None = None,
        parent_span_id: str | None = None,
    ) -> TaskResponse:
        trace = self._tracer.trace(trace_id)
        async with trace.span(
            parent_id=parent_span_id,
            name="get_task",
            input={"task_id": task_id, "task_name": task_name},
        ) as span:
            heartbeat_if_in_workflow("get task")
            if not task_id and not task_name:
                raise ValueError("Either task_id or task_name must be provided.")
            if task_id:
                task_model = await self._sb0_client.tasks.retrieve(task_id=task_id)
            elif task_name:
                task_model = await self._sb0_client.tasks.retrieve_by_name(task_name=task_name)
            else:
                raise ValueError("Either task_id or task_name must be provided.")
            if span:
                span.output = task_model.model_dump()
            return task_model

    async def delete_task(
        self,
        task_id: str | None = None,
        task_name: str | None = None,
        trace_id: str | None = None,
        parent_span_id: str | None = None,
    ) -> Task | DeleteResponse:
        trace = self._tracer.trace(trace_id) if self._tracer else None
        if trace is None:
            # Handle case without tracing
            response = await self._sb0_client.tasks.delete(task_id)
            return Task(**response.model_dump())

        async with trace.span(
            parent_id=parent_span_id,
            name="delete_task",
            input={"task_id": task_id, "task_name": task_name},
        ) as span:
            heartbeat_if_in_workflow("delete task")
            if not task_id and not task_name:
                raise ValueError("Either task_id or task_name must be provided.")
            if task_id:
                task_model = await self._sb0_client.tasks.delete(task_id=task_id)
            elif task_name:
                task_model = await self._sb0_client.tasks.delete_by_name(task_name=task_name)
            else:
                raise ValueError("Either task_id or task_name must be provided.")
            if span:
                span.output = task_model.model_dump()
            return task_model
