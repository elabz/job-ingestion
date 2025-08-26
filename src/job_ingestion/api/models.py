from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class JobPosting(BaseModel):
    """Minimal JobPosting schema for OpenAPI exposure (Pydantic v1).

    Fields are a subset per PRD: title, company, location are required.
    salary_min, salary_max, description are optional.
    """

    title: str = Field(..., example="Senior Data Engineer")
    company: str = Field(..., example="Acme Corp")
    location: str = Field(..., example="San Francisco, CA")
    salary_min: float | None = Field(None, example=140000)
    salary_max: float | None = Field(None, example=180000)
    description: str | None = Field(
        None, example="We are seeking a Senior Data Engineer to join our team..."
    )

    class Config:
        schema_extra = {
            "example": {
                "title": "Senior Data Engineer",
                "company": "Acme Corp",
                "location": "San Francisco, CA",
                "salary_min": 140000,
                "salary_max": 180000,
                "description": "We are seeking a Senior Data Engineer to join our team...",
            }
        }


class PingResponse(BaseModel):
    message: str = Field(example="pong")


class SingleJobPostingRequest(BaseModel):
    """Single job ingestion request accepting arbitrary JSON fields."""

    class Config:
        extra = "allow"


class IngestBatchRequest(BaseModel):
    """Batch ingestion request wrapper.

    Accepts a list of raw job payloads. Each job is an arbitrary JSON object; the
    service will normalize/validate downstream.
    """

    jobs: list[dict[str, Any]] = Field(
        ...,
        example=[
            {
                "title": "Data Engineer",
                "description": "Build pipelines",
                "employment_type": "full-time",
                "hiring_organization": {"name": "Acme Inc"},
                "date_posted": "2024-01-01T00:00:00Z",
            }
        ],
    )


class IngestResponse(BaseModel):
    """Response returned for accepted ingestion requests (HTTP 202)."""

    processing_id: UUID = Field(..., description="Batch processing identifier")
    message: str = Field(..., example="Batch accepted for processing")
    estimated_completion: datetime | None = Field(None, description="Optional ETA for completion")


__all__ = [
    "JobPosting",
    "PingResponse",
    "SingleJobPostingRequest",
    "IngestBatchRequest",
    "IngestResponse",
]
