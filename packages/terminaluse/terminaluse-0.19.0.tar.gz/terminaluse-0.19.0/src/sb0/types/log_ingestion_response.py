# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["LogIngestionResponse"]


class LogIngestionResponse(BaseModel):
    """Response from log ingestion endpoint."""

    ingested: int
