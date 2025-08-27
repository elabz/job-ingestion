from datetime import datetime
from enum import Enum
from typing import Any

from sqlalchemy import Boolean, DateTime, Float, Integer, Numeric, String, Text, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class ApprovalStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class Base(DeclarativeBase):  # type: ignore[misc,unused-ignore]
    type_annotation_map = {
        dict[str, Any]: SQLiteJSON,
        dict[str, Any]: SQLiteJSON,
        list[Any]: SQLiteJSON,
        list[Any]: SQLiteJSON,
    }


class Job(Base):
    __tablename__ = "jobs"

    # Primary fields
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    external_id: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    approval_status: Mapped[ApprovalStatus] = mapped_column(
        SAEnum(ApprovalStatus),
        nullable=False,
        server_default=ApprovalStatus.PENDING.value,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Salary information
    salary_min: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    salary_max: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    estimated_salary_min: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    estimated_salary_max: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    base_salary: Mapped[str | None] = mapped_column(String(100), nullable=True)
    salary_currency: Mapped[str | None] = mapped_column(String(10), nullable=True)
    salary_unit: Mapped[str | None] = mapped_column(String(20), nullable=True)
    is_salary_estimate: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    is_salary_confidential: Mapped[bool] = mapped_column(Boolean, default=False)

    # Company information
    company_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_company_confidential: Mapped[bool] = mapped_column(Boolean, default=False)

    # Job descriptions
    short_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    full_description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Location information
    primary_location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    zipcode: Mapped[str | None] = mapped_column(String(20), nullable=True)
    county: Mapped[str | None] = mapped_column(String(100), nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Experience requirements
    years_experience: Mapped[str | None] = mapped_column(String(50), nullable=True)
    years_experience_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Industry and job type
    industry_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    industry_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    job_type_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    remote_flag: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Important dates
    posting_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    entry_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    update_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # URLs and links
    external_application_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    seo_job_link: Mapped[str | None] = mapped_column(Text, nullable=True)
    seo_location: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Job flags and metadata
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    allows_external_apply: Mapped[bool] = mapped_column(Boolean, default=True)
    is_promoted: Mapped[bool] = mapped_column(Boolean, default=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    is_marketing: Mapped[bool] = mapped_column(Boolean, default=False)
    recruiter_anonymous: Mapped[bool] = mapped_column(Boolean, default=False)
    score: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Complex data stored as JSON
    locations_data: Mapped[dict[str, Any] | None] = mapped_column(SQLiteJSON, nullable=True)
    classifications_data: Mapped[dict[str, Any] | None] = mapped_column(SQLiteJSON, nullable=True)
    posted_dates: Mapped[list[Any] | None] = mapped_column(SQLiteJSON, nullable=True)
    candidate_residency: Mapped[list[Any] | None] = mapped_column(SQLiteJSON, nullable=True)
    questions: Mapped[list[Any] | None] = mapped_column(SQLiteJSON, nullable=True)
    featured_data: Mapped[list[Any] | None] = mapped_column(SQLiteJSON, nullable=True)
    additional_metadata: Mapped[dict[str, Any] | None] = mapped_column(SQLiteJSON, nullable=True)

    # Internal tracking
    collapse_key: Mapped[str | None] = mapped_column(String(255), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class RejectedJob(Base):
    __tablename__ = "rejected_jobs"

    # Primary fields
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    rejection_reasons: Mapped[str] = mapped_column(Text, nullable=False)
    external_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)

    # All the same fields as Job (except approval_status)
    salary_min: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    salary_max: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    estimated_salary_min: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    estimated_salary_max: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    base_salary: Mapped[str | None] = mapped_column(String(100), nullable=True)
    salary_currency: Mapped[str | None] = mapped_column(String(10), nullable=True)
    salary_unit: Mapped[str | None] = mapped_column(String(20), nullable=True)
    is_salary_estimate: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    is_salary_confidential: Mapped[bool] = mapped_column(Boolean, default=False)

    company_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_company_confidential: Mapped[bool] = mapped_column(Boolean, default=False)

    short_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    full_description: Mapped[str | None] = mapped_column(Text, nullable=True)

    primary_location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    zipcode: Mapped[str | None] = mapped_column(String(20), nullable=True)
    county: Mapped[str | None] = mapped_column(String(100), nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)

    years_experience: Mapped[str | None] = mapped_column(String(50), nullable=True)
    years_experience_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    industry_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    industry_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    job_type_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    remote_flag: Mapped[str | None] = mapped_column(String(50), nullable=True)

    posting_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    entry_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    update_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    external_application_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    seo_job_link: Mapped[str | None] = mapped_column(Text, nullable=True)
    seo_location: Mapped[str | None] = mapped_column(String(255), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    allows_external_apply: Mapped[bool] = mapped_column(Boolean, default=True)
    is_promoted: Mapped[bool] = mapped_column(Boolean, default=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    is_marketing: Mapped[bool] = mapped_column(Boolean, default=False)
    recruiter_anonymous: Mapped[bool] = mapped_column(Boolean, default=False)
    score: Mapped[float | None] = mapped_column(Float, nullable=True)

    locations_data: Mapped[dict[str, Any] | None] = mapped_column(SQLiteJSON, nullable=True)
    classifications_data: Mapped[dict[str, Any] | None] = mapped_column(SQLiteJSON, nullable=True)
    posted_dates: Mapped[list[Any] | None] = mapped_column(SQLiteJSON, nullable=True)
    candidate_residency: Mapped[list[Any] | None] = mapped_column(SQLiteJSON, nullable=True)
    questions: Mapped[list[Any] | None] = mapped_column(SQLiteJSON, nullable=True)
    featured_data: Mapped[list[Any] | None] = mapped_column(SQLiteJSON, nullable=True)
    additional_metadata: Mapped[dict[str, Any] | None] = mapped_column(SQLiteJSON, nullable=True)

    collapse_key: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
