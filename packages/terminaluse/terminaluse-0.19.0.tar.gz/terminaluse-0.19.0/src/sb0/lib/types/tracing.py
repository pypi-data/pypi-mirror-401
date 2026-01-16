from __future__ import annotations

from typing import Literal, Annotated

from pydantic import Field

from sb0.lib.utils.model_utils import BaseModel


class BaseModelWithTraceParams(BaseModel):
    """
    Base model with trace parameters.

    Attributes:
        trace_id: The trace ID
        parent_span_id: The parent span ID
    """

    trace_id: str | None = None
    parent_span_id: str | None = None


class Sb0TracingProcessorConfig(BaseModel):
    type: Literal["sb0"] = "sb0"


TracingProcessorConfig = Annotated[
    Sb0TracingProcessorConfig,
    Field(discriminator="type"),
]
