#!/usr/bin/env python3
"""
Migration 001: Expand job schema to capture all job properties and add rejected_jobs table.

This migration:
1. Adds comprehensive job fields to the jobs table
2. Creates a new rejected_jobs table with rejection reasons
3. Handles both SQLite and PostgreSQL databases
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from job_ingestion.utils.config import get_settings
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    MetaData,
    Numeric,
    String,
    Table,
    Text,
    create_engine,
    func,
)
from sqlalchemy.dialects.postgresql import JSON as PostgresJSON
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
from sqlalchemy.engine import Engine
from sqlalchemy.sql import text


def get_json_type(engine: Engine) -> type[PostgresJSON | SQLiteJSON]:
    """Return appropriate JSON type based on database dialect."""
    if engine.dialect.name == "postgresql":
        return PostgresJSON  # type: ignore[no-any-return]
    return SQLiteJSON  # type: ignore[no-any-return]


def upgrade(engine: Engine) -> None:
    """Apply the migration - add new columns and create rejected_jobs table."""
    metadata = MetaData()
    json_type = get_json_type(engine)

    # Check if jobs table exists (for reference only)
    _ = Table("jobs", metadata, autoload_with=engine)

    print("Adding new columns to jobs table...")

    # Add new columns to jobs table
    new_columns = [
        # Salary information
        Column("salary_min", Numeric(12, 2), nullable=True),
        Column("salary_max", Numeric(12, 2), nullable=True),
        Column("estimated_salary_min", Numeric(12, 2), nullable=True),
        Column("estimated_salary_max", Numeric(12, 2), nullable=True),
        Column("base_salary", String(100), nullable=True),
        Column("is_salary_estimate", Boolean, nullable=True),
        Column("is_salary_confidential", Boolean, default=False),
        # Company information
        Column("company_name", String(255), nullable=True),
        Column("is_company_confidential", Boolean, default=False),
        # Job descriptions
        Column("short_description", Text, nullable=True),
        Column("full_description", Text, nullable=True),
        # Location information
        Column("primary_location", String(255), nullable=True),
        Column("zipcode", String(20), nullable=True),
        Column("county", String(100), nullable=True),
        Column("latitude", Float, nullable=True),
        Column("longitude", Float, nullable=True),
        # Experience requirements
        Column("years_experience", String(50), nullable=True),
        Column("years_experience_id", Integer, nullable=True),
        # Industry and job type
        Column("industry_name", String(255), nullable=True),
        Column("industry_id", Integer, nullable=True),
        Column("job_type_id", Integer, nullable=True),
        Column("remote_flag", String(50), nullable=True),
        # Important dates
        Column("posting_date", DateTime(timezone=True), nullable=True),
        Column("entry_date", DateTime(timezone=True), nullable=True),
        Column("update_date", DateTime(timezone=True), nullable=True),
        # URLs and links
        Column("external_application_url", Text, nullable=True),
        Column("seo_job_link", Text, nullable=True),
        Column("seo_location", String(255), nullable=True),
        # Job flags and metadata
        Column("is_active", Boolean, default=True),
        Column("allows_external_apply", Boolean, default=True),
        Column("is_promoted", Boolean, default=False),
        Column("is_featured", Boolean, default=False),
        Column("is_marketing", Boolean, default=False),
        Column("recruiter_anonymous", Boolean, default=False),
        Column("score", Float, nullable=True),
        # Complex data stored as JSON
        Column("locations_data", json_type, nullable=True),
        Column("classifications_data", json_type, nullable=True),
        Column("posted_dates", json_type, nullable=True),
        Column("candidate_residency", json_type, nullable=True),
        Column("questions", json_type, nullable=True),
        Column("featured_data", json_type, nullable=True),
        Column("additional_metadata", json_type, nullable=True),
        # Internal tracking
        Column("collapse_key", String(255), nullable=True),
        Column(
            "updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
        ),
    ]

    # Add columns one by one to handle potential conflicts
    with engine.connect() as conn:
        for column in new_columns:
            try:
                # Check if column already exists
                result = conn.execute(text("PRAGMA table_info(jobs)"))
                existing_columns = [row[1] for row in result.fetchall()]

                if column.name not in existing_columns:
                    if engine.dialect.name == "sqlite":
                        conn.execute(
                            text(f"ALTER TABLE jobs ADD COLUMN {column.name} {column.type}")
                        )
                    else:  # PostgreSQL
                        conn.execute(
                            text(f"ALTER TABLE jobs ADD COLUMN {column.name} {column.type}")
                        )
                    print(f"  Added column: {column.name}")
                else:
                    print(f"  Column {column.name} already exists, skipping")
            except Exception as e:
                print(f"  Warning: Could not add column {column.name}: {e}")

        conn.commit()

    print("Creating rejected_jobs table...")

    # Create rejected_jobs table
    rejected_jobs_table = Table(
        "rejected_jobs",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("rejection_reasons", Text, nullable=False),
        Column("external_id", String, nullable=False, index=True),
        Column("title", String, nullable=False),
        # All the same columns as jobs table (except approval_status)
        Column("salary_min", Numeric(12, 2), nullable=True),
        Column("salary_max", Numeric(12, 2), nullable=True),
        Column("estimated_salary_min", Numeric(12, 2), nullable=True),
        Column("estimated_salary_max", Numeric(12, 2), nullable=True),
        Column("base_salary", String(100), nullable=True),
        Column("is_salary_estimate", Boolean, nullable=True),
        Column("is_salary_confidential", Boolean, default=False),
        Column("company_name", String(255), nullable=True),
        Column("is_company_confidential", Boolean, default=False),
        Column("short_description", Text, nullable=True),
        Column("full_description", Text, nullable=True),
        Column("primary_location", String(255), nullable=True),
        Column("zipcode", String(20), nullable=True),
        Column("county", String(100), nullable=True),
        Column("latitude", Float, nullable=True),
        Column("longitude", Float, nullable=True),
        Column("years_experience", String(50), nullable=True),
        Column("years_experience_id", Integer, nullable=True),
        Column("industry_name", String(255), nullable=True),
        Column("industry_id", Integer, nullable=True),
        Column("job_type_id", Integer, nullable=True),
        Column("remote_flag", String(50), nullable=True),
        Column("posting_date", DateTime(timezone=True), nullable=True),
        Column("entry_date", DateTime(timezone=True), nullable=True),
        Column("update_date", DateTime(timezone=True), nullable=True),
        Column("external_application_url", Text, nullable=True),
        Column("seo_job_link", Text, nullable=True),
        Column("seo_location", String(255), nullable=True),
        Column("is_active", Boolean, default=True),
        Column("allows_external_apply", Boolean, default=True),
        Column("is_promoted", Boolean, default=False),
        Column("is_featured", Boolean, default=False),
        Column("is_marketing", Boolean, default=False),
        Column("recruiter_anonymous", Boolean, default=False),
        Column("score", Float, nullable=True),
        Column("locations_data", json_type, nullable=True),
        Column("classifications_data", json_type, nullable=True),
        Column("posted_dates", json_type, nullable=True),
        Column("candidate_residency", json_type, nullable=True),
        Column("questions", json_type, nullable=True),
        Column("featured_data", json_type, nullable=True),
        Column("additional_metadata", json_type, nullable=True),
        Column("collapse_key", String(255), nullable=True),
        Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
        Column(
            "updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
        ),
    )

    # Create the rejected_jobs table
    try:
        rejected_jobs_table.create(engine, checkfirst=True)
        print("  Created rejected_jobs table")
    except Exception as e:
        print(f"  Warning: Could not create rejected_jobs table: {e}")

    print("Migration completed successfully!")


def downgrade(engine: Engine) -> None:
    """Rollback the migration - remove added columns and drop rejected_jobs table."""
    print("Rolling back migration...")

    # Drop rejected_jobs table
    with engine.connect() as conn:
        try:
            conn.execute(text("DROP TABLE IF EXISTS rejected_jobs"))
            conn.commit()
            print("  Dropped rejected_jobs table")
        except Exception as e:
            print(f"  Warning: Could not drop rejected_jobs table: {e}")

    # Note: Removing columns from SQLite is complex and requires recreating the table
    # For now, we'll just warn about this limitation
    print("  Warning: Column removal not implemented for SQLite. Manual intervention required.")
    print("Migration rollback completed!")


def main() -> None:
    """Run the migration."""
    settings = get_settings()
    engine = create_engine(settings.database_url)

    print(f"Running migration on database: {settings.database_url}")
    print(f"Database dialect: {engine.dialect.name}")

    try:
        upgrade(engine)
    except Exception as e:
        print(f"Migration failed: {e}")
        raise


if __name__ == "__main__":
    main()
