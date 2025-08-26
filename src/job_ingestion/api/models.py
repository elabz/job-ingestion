from __future__ import annotations

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


__all__ = ["JobPosting", "PingResponse"]
